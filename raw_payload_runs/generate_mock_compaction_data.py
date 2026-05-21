#!/usr/bin/env python3
"""
Generate standardized mock JSONL run data for compaction-device telemetry.

The output is intentionally modeled after the real CD2.2-006 payload:
- nested latest_message.data JSON string containing a base64-encoded CSV blob
- first CSV value is a sync/framing artifact and should be dropped by parsers
- remaining values are raw electromagnetic/power time-series readings
- summary metrics are provided both in latest_message and in a normalized run block

This script creates a large set of synthetic records spanning base cases and the
edge cases described in the case-study analysis.

NOTE:
- This script generates synthetic-only artifacts.
- It is runnable from a fresh clone using only repository files.
- Committed JSONL files remain canonical for review diffs.
"""

from __future__ import annotations

import base64
import csv
import json
import math
import random
import re
import statistics
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


RAW_PAYLOAD_DIR = Path(__file__).resolve().parent
WORKSPACE = RAW_PAYLOAD_DIR.parent
OUT_DIR = RAW_PAYLOAD_DIR
ZIP_PATH = OUT_DIR / "mock_compaction_jsonl_runs.zip"


@dataclass(frozen=True)
class Scenario:
    name: str
    count: int
    label: str
    description: str
    file_name: str


SCENARIOS = [
    Scenario(
        "base_single_light",
        80,
        "standard_single_run",
        "Clean single compaction cycles with lower load and modest peak pressure.",
        "base_single_light.jsonl",
    ),
    Scenario(
        "base_single_medium",
        100,
        "standard_single_run",
        "Clean single compaction cycles close to the case-study operating band.",
        "base_single_medium.jsonl",
    ),
    Scenario(
        "base_single_heavy_near_full",
        80,
        "standard_single_run",
        "Clean single cycles with elevated baseline and peaks suggesting high fullness.",
        "base_single_heavy_near_full.jsonl",
    ),
    Scenario(
        "double_run_clear",
        90,
        "double_run",
        "Two back-to-back compaction cycles in one payload with a sharp drop and re-ramp.",
        "double_run_clear.jsonl",
    ),
    Scenario(
        "double_run_late_boundary",
        45,
        "double_run",
        "Double-runs where the first run is longer and the boundary appears later than expected.",
        "double_run_late_boundary.jsonl",
    ),
    Scenario(
        "double_run_ambiguous_boundary",
        45,
        "double_run",
        "Double-runs with a shallower transition drop near the detector threshold.",
        "double_run_ambiguous_boundary.jsonl",
    ),
    Scenario(
        "single_run_deep_dip_false_positive_risk",
        45,
        "standard_single_run_with_dip",
        "Single cycles with a transient dip but no sustained re-ramp boundary.",
        "single_run_deep_dip_false_positive_risk.jsonl",
    ),
    Scenario(
        "startup_spike_extreme_sync",
        40,
        "startup_spike",
        "Payloads with oversized sync/startup artifacts that must not affect metrics.",
        "startup_spike_extreme_sync.jsonl",
    ),
    Scenario(
        "truncated_payload",
        40,
        "truncated",
        "Partial transmissions with too few samples to trust as full cycles.",
        "truncated_payload.jsonl",
    ),
    Scenario(
        "peak_saturation",
        35,
        "peak_saturation",
        "Runs clipping at an ADC-like ceiling, hiding true peak pressure.",
        "peak_saturation.jsonl",
    ),
    Scenario(
        "low_battery_weak_signal_noisy",
        35,
        "low_power_noisy",
        "Runs with weak signal, low battery, and high noise/dropout risk.",
        "low_battery_weak_signal_noisy.jsonl",
    ),
    Scenario(
        "baseline_drift",
        40,
        "baseline_drift",
        "Sequential-looking records where low/baseline values drift upward over time.",
        "baseline_drift.jsonl",
    ),
    Scenario(
        "dropout_missing_values",
        30,
        "dropout_missing_values",
        "Payloads that preserve blank CSV slots from intermittent sensor/transmission gaps.",
        "dropout_missing_values.jsonl",
    ),
    Scenario(
        "triple_run_buffered",
        20,
        "multi_run",
        "Three buffered cycles in one message for stress-testing split logic.",
        "triple_run_buffered.jsonl",
    ),
]


def extract_reference_b64() -> str:
    parse_script = WORKSPACE / "parse_and_graph.py"
    if parse_script.exists():
        text = parse_script.read_text()
        match = re.search(r"SAMPLE_B64\s*=\s*\((.*?)\)", text, flags=re.S)
        if match:
            return "".join(re.findall(r'"([^"]+)"', match.group(1)))

    # Public fallback: bootstrap from the first committed synthetic record.
    bundled = Path(__file__).with_name("all_runs.jsonl")
    if bundled.exists():
        for line in bundled.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            b64_data = record.get("raw_stream", {}).get("base64_data")
            if b64_data:
                return b64_data

    raise RuntimeError("No calibration base64 stream found in parse_and_graph.py or all_runs.jsonl")


def decode_blob(b64: str) -> tuple[str, int, list[int], int, int]:
    decoded = base64.b64decode(b64).decode("utf-8", errors="replace")
    lines = [line.strip() for line in decoded.strip().splitlines() if line.strip()]
    timestamp = lines[0].replace("/", "-").replace(",", " ")
    tokens = [int(t) for t in lines[1].split(",") if t.strip().lstrip("-").isdigit()]
    sync_artifact = tokens[0]
    values = tokens[1:]
    battery = int(lines[2].replace(",", "").replace("%", "").strip())
    signal = int(lines[3].replace(",", "").strip())
    return timestamp, sync_artifact, values, battery, signal


def stats(values: list[int]) -> dict:
    usable = [v for v in values if isinstance(v, int)]
    if not usable:
        return {
            "samples": 0,
            "power_low": None,
            "power_peak": None,
            "power_average": None,
            "power_total": None,
            "power_stddev": None,
        }
    return {
        "samples": len(usable),
        "power_low": min(usable),
        "power_peak": max(usable),
        "power_average": round(sum(usable) / len(usable), 4),
        "power_total": sum(usable),
        "power_stddev": round(statistics.pstdev(usable), 4) if len(usable) > 1 else 0.0,
    }


def smooth_noise(rng: random.Random, n: int, scale: float) -> list[float]:
    value = 0.0
    out = []
    for _ in range(n):
        value = 0.72 * value + rng.gauss(0, scale)
        out.append(value)
    return out


def make_single_run(
    rng: random.Random,
    n: int,
    baseline: int,
    peak: int,
    noise: float,
    fullness: float,
    mode: str = "normal",
    saturation: int | None = None,
) -> list[int]:
    values: list[int] = []
    correlated_noise = smooth_noise(rng, n, noise)
    ramp_power = rng.uniform(1.35, 2.15)
    for i in range(n):
        x = i / max(1, n - 1)
        ramp = x**ramp_power
        oscillation = math.sin(x * math.pi * rng.uniform(2.0, 4.5)) * rng.uniform(250, 900)
        compaction_pulses = 0
        if x > 0.22:
            compaction_pulses += math.sin(x * math.pi * rng.uniform(8, 15)) * rng.uniform(250, 1250)
        if mode == "heavy" and x > 0.65:
            compaction_pulses += math.sin(x * math.pi * 11) * rng.uniform(700, 1700)
        load = baseline + (peak - baseline) * ramp
        fullness_lift = (fullness - 0.45) * 1700
        value = load + fullness_lift + oscillation + compaction_pulses + correlated_noise[i]
        if mode == "light" and x > 0.70:
            value -= rng.uniform(300, 900)
        if saturation is not None and value > saturation:
            value = saturation
        values.append(int(round(value)))
    values[0] = int(round(baseline + rng.uniform(600, 3200)))
    return [max(25000, min(65535, v)) for v in values]


def make_deep_dip_single(rng: random.Random) -> list[int]:
    n = rng.randint(62, 82)
    values = make_single_run(
        rng,
        n=n,
        baseline=rng.randint(29600, 31300),
        peak=rng.randint(39200, 43200),
        noise=rng.uniform(500, 950),
        fullness=rng.uniform(0.45, 0.78),
    )
    dip_at = rng.randint(int(n * 0.42), int(n * 0.62))
    dip_depth = rng.randint(5200, 9000)
    for offset in range(-2, 4):
        idx = dip_at + offset
        if 0 <= idx < n:
            values[idx] = max(28600, values[idx] - dip_depth + abs(offset) * rng.randint(400, 950))
    # No durable re-ramp: resume near the prior trend rather than beginning a fresh cycle.
    for idx in range(dip_at + 4, min(n, dip_at + 12)):
        values[idx] = int(round((values[idx] + values[max(0, idx - 8)]) / 2 + rng.gauss(0, 400)))
    return values


def make_double_run(
    rng: random.Random,
    late: bool = False,
    ambiguous: bool = False,
    triple: bool = False,
) -> tuple[list[int], list[int]]:
    first_n = rng.randint(54, 76) if late else rng.randint(36, 49)
    second_n = rng.randint(63, 108)
    base_a = rng.randint(29600, 31350)
    peak_a = rng.randint(40500, 44500)
    base_b = rng.randint(29600, 32000)
    peak_b = rng.randint(39400, 43000)
    run_a = make_single_run(rng, first_n, base_a, peak_a, rng.uniform(450, 900), rng.uniform(0.55, 0.88), "heavy")
    run_b = make_single_run(rng, second_n, base_b, peak_b, rng.uniform(600, 1150), rng.uniform(0.42, 0.82))
    if ambiguous:
        run_b[0] = int(round(peak_a * rng.uniform(0.70, 0.77)))
        for i in range(1, min(7, len(run_b))):
            run_b[i] = int(round(run_b[0] + i * rng.uniform(350, 900) + rng.gauss(0, 350)))
    else:
        run_b[0] = rng.randint(29800, 31800)
        for i in range(1, min(7, len(run_b))):
            run_b[i] = int(round(run_b[0] + i * rng.uniform(450, 1150) + rng.gauss(0, 400)))
    values = run_a + run_b
    splits = [len(run_a)]
    if triple:
        third_n = rng.randint(48, 78)
        run_c = make_single_run(
            rng,
            third_n,
            rng.randint(29400, 31600),
            rng.randint(38600, 42700),
            rng.uniform(600, 1150),
            rng.uniform(0.35, 0.75),
        )
        run_c[0] = rng.randint(29400, 31750)
        splits.append(len(values))
        values.extend(run_c)
    return values, splits


def add_missing_slots(rng: random.Random, values: list[int]) -> list[int | None]:
    out: list[int | None] = list(values)
    dropout_count = rng.randint(3, 10)
    candidates = list(range(5, max(6, len(out) - 5)))
    rng.shuffle(candidates)
    for idx in candidates[:dropout_count]:
        out[idx] = None
    return out


def encode_stream(
    run_start: datetime,
    sync_artifact: int,
    values: list[int | None],
    battery: int,
    signal: int,
) -> tuple[str, str]:
    date_line = run_start.strftime("%Y/%m/%d,%H:%M:%S")
    value_tokens = ["", str(sync_artifact)]
    value_tokens.extend("" if value is None else str(value) for value in values)
    # Preserve a few trailing blanks because the real payload contains unused CSV slots.
    value_tokens.extend([""] * 8)
    blob = "\r\n".join(
        [
            date_line,
            ",".join(value_tokens),
            f",{battery}%",
            f",{signal}",
        ]
    ) + "\r\n"
    return blob, base64.b64encode(blob.encode("utf-8")).decode("ascii")


def make_record(
    rng: random.Random,
    index: int,
    scenario: Scenario,
    real_sync: int,
    base_time: datetime,
    drift_offset: int = 0,
) -> dict:
    if scenario.name == "base_single_light":
        values = make_single_run(rng, rng.randint(58, 75), rng.randint(29200, 30650), rng.randint(36500, 39800), rng.uniform(350, 800), rng.uniform(0.20, 0.45), "light")
        splits: list[int] = []
        battery, signal = rng.randint(120, 230), rng.randint(13, 24)
    elif scenario.name == "base_single_medium":
        values = make_single_run(rng, rng.randint(62, 82), rng.randint(29800, 31500), rng.randint(39200, 43000), rng.uniform(450, 950), rng.uniform(0.42, 0.70))
        splits = []
        battery, signal = rng.randint(115, 230), rng.randint(12, 24)
    elif scenario.name == "base_single_heavy_near_full":
        values = make_single_run(rng, rng.randint(66, 90), rng.randint(31000, 33300), rng.randint(42500, 46200), rng.uniform(550, 1150), rng.uniform(0.72, 0.95), "heavy")
        splits = []
        battery, signal = rng.randint(110, 225), rng.randint(11, 23)
    elif scenario.name == "double_run_clear":
        values, splits = make_double_run(rng)
        battery, signal = rng.randint(100, 225), rng.randint(10, 23)
    elif scenario.name == "double_run_late_boundary":
        values, splits = make_double_run(rng, late=True)
        battery, signal = rng.randint(100, 225), rng.randint(10, 23)
    elif scenario.name == "double_run_ambiguous_boundary":
        values, splits = make_double_run(rng, ambiguous=True)
        battery, signal = rng.randint(90, 215), rng.randint(8, 20)
    elif scenario.name == "single_run_deep_dip_false_positive_risk":
        values = make_deep_dip_single(rng)
        splits = []
        battery, signal = rng.randint(100, 220), rng.randint(10, 22)
    elif scenario.name == "startup_spike_extreme_sync":
        values = make_single_run(rng, rng.randint(60, 82), rng.randint(29700, 31500), rng.randint(39200, 42800), rng.uniform(450, 950), rng.uniform(0.35, 0.75))
        splits = []
        battery, signal = rng.randint(100, 230), rng.randint(10, 24)
    elif scenario.name == "truncated_payload":
        values = make_single_run(rng, rng.randint(18, 42), rng.randint(29400, 31500), rng.randint(34000, 39500), rng.uniform(450, 1100), rng.uniform(0.20, 0.70))
        splits = []
        battery, signal = rng.randint(75, 190), rng.randint(5, 18)
    elif scenario.name == "peak_saturation":
        saturation = rng.choice([40950, 41900, 42596, 43502])
        values = make_single_run(rng, rng.randint(62, 86), rng.randint(30400, 32600), rng.randint(44000, 48500), rng.uniform(550, 950), rng.uniform(0.70, 0.96), "heavy", saturation=saturation)
        splits = []
        battery, signal = rng.randint(100, 225), rng.randint(10, 23)
    elif scenario.name == "low_battery_weak_signal_noisy":
        values = make_single_run(rng, rng.randint(52, 84), rng.randint(29200, 32200), rng.randint(37500, 43500), rng.uniform(1100, 2600), rng.uniform(0.30, 0.85))
        splits = []
        battery, signal = rng.randint(5, 35), rng.randint(1, 7)
    elif scenario.name == "baseline_drift":
        base = rng.randint(29400, 30500) + drift_offset * rng.randint(75, 145)
        values = make_single_run(rng, rng.randint(61, 82), base, base + rng.randint(8500, 12600), rng.uniform(450, 950), min(0.96, 0.35 + drift_offset * 0.012 + rng.uniform(0.0, 0.28)))
        splits = []
        battery, signal = rng.randint(80, 220), rng.randint(8, 22)
    elif scenario.name == "dropout_missing_values":
        dense = make_single_run(rng, rng.randint(58, 84), rng.randint(29600, 31600), rng.randint(38500, 43000), rng.uniform(500, 1000), rng.uniform(0.35, 0.80))
        values = add_missing_slots(rng, dense)
        splits = []
        battery, signal = rng.randint(50, 160), rng.randint(3, 12)
    elif scenario.name == "triple_run_buffered":
        values, splits = make_double_run(rng, triple=True)
        battery, signal = rng.randint(70, 200), rng.randint(6, 19)
    else:
        raise ValueError(scenario.name)

    sync_artifact = real_sync
    if scenario.name == "startup_spike_extreme_sync":
        sync_artifact = rng.randint(56000, 65535)
    elif rng.random() < 0.12:
        sync_artifact = rng.randint(47000, 62000)

    run_start = base_time + timedelta(minutes=17 * index + rng.randint(-4, 4))
    raw_blob, b64 = encode_stream(run_start, sync_artifact, values, battery, signal)
    usable_values = [v for v in values if isinstance(v, int)]
    metric = stats(usable_values)
    record_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"caprock-mock-compaction-{scenario.name}-{index}"))
    received = run_start.astimezone(timezone.utc) + timedelta(seconds=rng.uniform(0.12, 2.75))
    logged = received.replace(microsecond=0)

    fullness_percentage = max(1, min(99, int(round((metric["power_average"] - 28500) / 165)))) if metric["power_average"] else None
    split_metrics = []
    if splits:
        boundaries = [0] + splits + [len(values)]
        for part_index, (start, end) in enumerate(zip(boundaries, boundaries[1:]), start=1):
            segment = [v for v in values[start:end] if isinstance(v, int)]
            split_metrics.append({"segment": part_index, "start": start, "end": end, **stats(segment)})

    normalized = {
        "schema_version": "mock_compactor_run.v1",
        "record_id": record_id,
        "source": {
            "kind": "synthetic",
            "derived_from": "CD2.2-006 case-study payload",
            "generator_seed": 424242,
            "scenario": scenario.name,
        },
        "device": {
            "device_id": 120177 + (index % 7),
            "device_name": "CD2.2-006-MOCK",
            "device_family": "CD2.2",
            "compaction_method": "hydraulic",
            "voltage": "220",
            "energy_threshold": 80,
            "expected_single_samples": 70,
            "material_type": "MSW (Compacted)",
            "capacity_cy": 32,
        },
        "site": {
            "site_id": 10,
            "site_name": "Mock Compaction Site",
            "timezone": "UTC",
            "location_type": "commercial_highrise",
        },
        "run": {
            "run_start": run_start.strftime("%Y-%m-%d %H:%M:%S"),
            "logged": logged.strftime("%Y-%m-%d %H:%M:%S"),
            "anomaly_label": scenario.label,
            "scenario_description": scenario.description,
            "split_indices": splits,
            "usable_sample_count": metric["samples"],
            "raw_token_count_including_sync": len(values) + 1,
            "has_missing_value_slots": any(v is None for v in values),
            "startup_sync_artifact": sync_artifact,
            "battery_percentage": battery,
            "signal_strength": signal,
            "fullness_percentage": fullness_percentage,
            "metrics": metric,
            "split_metrics": split_metrics,
        },
        "raw_stream": {
            "format": "base64_csv_v1",
            "decode_notes": "Decoded blob lines are timestamp, comma-delimited sensor readings with a blank leading token and sync artifact, battery percent, and signal strength.",
            "raw_blob": raw_blob,
            "base64_data": b64,
            "decoded_values": values,
        },
        "latest_message": {
            "id": 9000000 + index,
            "deviceid": 120177 + (index % 7),
            "type": "data",
            "record_id": record_id,
            "logged": logged.strftime("%Y-%m-%d %H:%M:%S"),
            "run_start": run_start.strftime("%Y-%m-%d %H:%M:%S"),
            "orgid": "7175",
            "data": json.dumps(
                {
                    "data": b64,
                    "tags": [
                        "_SIMPLESTRING_",
                        "_SOCKETAPI_",
                        "_DEVICE_120177_",
                        "_TAG_SYNTHETIC_",
                        "type:data",
                        f"scenario:{scenario.name}",
                    ],
                    "source": "synthetic-generator",
                    "authtype": "otp",
                    "received": received.isoformat(),
                    "device_id": 120177 + (index % 7),
                    "errorcode": 0,
                    "record_id": record_id,
                    "timestamp": str(int(run_start.timestamp())),
                    "device_name": "CD2.2-006-MOCK",
                    "device_metadata": {
                        "m_version": 1,
                        "dev_fw_string": "dash-SARA-U260-0.9.13",
                    },
                }
            ),
            "device_meta_data": json.dumps({"m_version": 1, "dev_fw_string": "dash-SARA-U260-0.9.13"}),
            "fullness": f"{(fullness_percentage or 0) * 328.99:.2f}",
            "power_low": metric["power_low"],
            "power_total": metric["power_total"],
            "power_peak": metric["power_peak"],
            "power_average": int(round(metric["power_average"])) if metric["power_average"] is not None else None,
            "battery_percentage": battery,
            "signal_strength": signal,
            "timestamp": run_start.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": logged.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": logged.strftime("%Y-%m-%d %H:%M:%S"),
        },
    }
    return normalized


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, separators=(",", ":"), ensure_ascii=False) + "\n")
            count += 1
    return count


def validation_summary(records: list[dict]) -> dict:
    by_scenario: dict[str, int] = {}
    labels: dict[str, int] = {}
    sample_counts = []
    peaks = []
    lows = []
    with_missing = 0
    with_splits = 0
    for rec in records:
        scenario = rec["source"]["scenario"]
        label = rec["run"]["anomaly_label"]
        by_scenario[scenario] = by_scenario.get(scenario, 0) + 1
        labels[label] = labels.get(label, 0) + 1
        sample_counts.append(rec["run"]["usable_sample_count"])
        if rec["run"]["metrics"]["power_peak"] is not None:
            peaks.append(rec["run"]["metrics"]["power_peak"])
        if rec["run"]["metrics"]["power_low"] is not None:
            lows.append(rec["run"]["metrics"]["power_low"])
        if rec["run"]["has_missing_value_slots"]:
            with_missing += 1
        if rec["run"]["split_indices"]:
            with_splits += 1
    return {
        "record_count": len(records),
        "scenario_counts": by_scenario,
        "label_counts": labels,
        "sample_count_min": min(sample_counts),
        "sample_count_max": max(sample_counts),
        "sample_count_mean": round(sum(sample_counts) / len(sample_counts), 2),
        "power_low_min": min(lows),
        "power_peak_max": max(peaks),
        "records_with_missing_value_slots": with_missing,
        "records_with_split_indices": with_splits,
    }


def make_readme(summary: dict) -> str:
    return f"""# Mock Compaction JSONL Run Data

This archive contains synthetic, standardized JSONL telemetry records modeled after the attached CD2.2-006 compaction-device case-study payload.

## Contents

- `all_runs.jsonl`: every generated record in one file.
- `scenarios/*.jsonl`: one JSONL file per scenario/edge-case family.
- `manifest.json`: generation settings, scenario descriptions, and validation summary.
- `schema.json`: informal JSON schema for the normalized record shape.
- `validation_summary.csv`: compact counts and metric ranges for quick inspection.

## Scale

- Total records: {summary["record_count"]}
- Usable sample count range: {summary["sample_count_min"]} to {summary["sample_count_max"]}
- Records with split labels: {summary["records_with_split_indices"]}
- Records with missing CSV value slots: {summary["records_with_missing_value_slots"]}

## Data shape

Each line is a full JSON object with these major blocks:

- `latest_message`: close analogue to the application payload, including `latest_message.data` as a JSON string that wraps the base64 CSV blob.
- `raw_stream`: decoded helper fields, including `raw_blob`, `base64_data`, and `decoded_values`.
- `run`: standardized labels, split indices, summary metrics, battery/signal readings, and anomaly scenario.
- `device` and `site`: stable mock metadata that resembles the real device family without using the full original customer/vendor record.

The encoded stream follows the real structure:

1. timestamp line such as `2018/04/02,16:10:58`
2. comma-delimited sensor readings with a blank first token and a sync artifact as the first numeric token
3. battery percentage line
4. signal-strength line

For experiments, calculate metrics from `raw_stream.decoded_values` after removing `None` gaps. To test production parsing, ignore the helper array and decode `latest_message.data` exactly as the original parser does.
"""


def main() -> None:
    rng = random.Random(424242)
    real_b64 = extract_reference_b64()
    _, real_sync, real_values, real_battery, real_signal = decode_blob(real_b64)
    base_time = datetime(2018, 4, 2, 16, 10, 58, tzinfo=timezone.utc)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    scenario_dir = OUT_DIR / "scenarios"
    scenario_dir.mkdir(exist_ok=True)
    for old_path in sorted(scenario_dir.glob("*.jsonl")):
        old_path.unlink()

    all_records: list[dict] = []
    global_index = 0
    for scenario in SCENARIOS:
        scenario_records = []
        for i in range(scenario.count):
            rec = make_record(rng, global_index, scenario, real_sync, base_time, drift_offset=i)
            scenario_records.append(rec)
            all_records.append(rec)
            global_index += 1
        write_jsonl(scenario_dir / scenario.file_name, scenario_records)

    # Include a known-real-reference line so downstream experiments can compare the synthetic set
    # to the original decoded series without treating the original customer payload as mock data.
    real_metric = stats(real_values)
    legacy_reference_obscured = {
        "schema_version": "mock_compactor_run.v1",
        "record_id": "legacy-reference-obscured-20180402",
        "source": {
            "kind": "legacy_reference_obscured",
            "derived_from": "private calibration sample (obscured)",
            "scenario": "legacy_double_run_reference",
        },
        "device": {
            "device_id": 120177,
            "device_name": "CD2.2-006 (66927)",
            "device_family": "CD2.2",
            "compaction_method": "hydraulic",
            "voltage": "220",
            "energy_threshold": 80,
            "expected_single_samples": 70,
            "material_type": "MSW (Compacted)",
            "capacity_cy": 32,
        },
        "site": {"site_id": 10, "site_name": "Reference Site - Obscured", "timezone": "UTC", "location_type": "commercial_highrise"},
        "run": {
            "run_start": "2018-04-02 16:10:58",
            "logged": "2018-04-02 20:10:59",
            "anomaly_label": "double_run",
            "scenario_description": "Legacy calibration run included as an obscured reference sample.",
            "split_indices": [41],
            "usable_sample_count": len(real_values),
            "raw_token_count_including_sync": len(real_values) + 1,
            "has_missing_value_slots": False,
            "startup_sync_artifact": real_sync,
            "battery_percentage": real_battery,
            "signal_strength": real_signal,
            "fullness_percentage": 38,
            "metrics": real_metric,
            "split_metrics": [
                {"segment": 1, "start": 0, "end": 41, **stats(real_values[:41])},
                {"segment": 2, "start": 41, "end": len(real_values), **stats(real_values[41:])},
            ],
        },
        "raw_stream": {
            "format": "base64_csv_v1",
            "decode_notes": "Reference stream from the attached case-study sample.",
            "raw_blob": base64.b64decode(real_b64).decode("utf-8", errors="replace"),
            "base64_data": real_b64,
            "decoded_values": real_values,
        },
        "latest_message": {
            "id": 9900000,
            "deviceid": 120177,
            "type": "data",
            "record_id": "legacy-obscured-record-id",
            "logged": "2018-04-02 20:10:59",
            "run_start": "2018-04-02 16:10:58",
            "orgid": "0000",
            "data": json.dumps({"data": real_b64, "tags": ["_SIMPLESTRING_", "_SOCKETAPI_", "_DEVICE_120177_", "_TAG_OBSCURED_", "type:data", "device:cd2.2-006-obscured"]}),
            "device_meta_data": json.dumps({"m_version": 1, "dev_fw_string": "dash-SARA-U260-0.9.13"}),
            "fullness": "13304.00",
            "power_low": real_metric["power_low"],
            "power_total": real_metric["power_total"],
            "power_peak": real_metric["power_peak"],
            "power_average": int(round(real_metric["power_average"])),
            "battery_percentage": real_battery,
            "signal_strength": real_signal,
            "timestamp": "2018-04-02 20:10:58",
            "created_at": "2018-04-02 20:10:59",
            "updated_at": "2018-04-02 20:10:59",
        },
    }
    # Deliberately not appended to generated datasets in this repository.
    # The published package is synthetic-only.

    write_jsonl(OUT_DIR / "all_runs.jsonl", all_records)

    summary = validation_summary(all_records)
    manifest = {
        "name": "mock_compaction_jsonl_runs",
        "schema_version": "mock_compactor_run.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_mock_compaction_data.py",
        "seed": 424242,
        "basis": {
            "calibration_sample_count": len(real_values),
            "calibration_reference_split_index": 41,
            "expected_single_samples": 70,
            "normal_operating_band_approx": [29000, 44000],
            "sync_artifact_example": real_sync,
        },
        "scenarios": [scenario.__dict__ for scenario in SCENARIOS],
        "validation_summary": summary,
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Mock Compactor Run Record",
        "type": "object",
        "required": ["schema_version", "record_id", "source", "device", "run", "raw_stream", "latest_message"],
        "properties": {
            "schema_version": {"const": "mock_compactor_run.v1"},
            "record_id": {"type": "string"},
            "source": {"type": "object"},
            "device": {"type": "object"},
            "site": {"type": "object"},
            "run": {"type": "object"},
            "raw_stream": {"type": "object"},
            "latest_message": {"type": "object"},
        },
    }
    (OUT_DIR / "schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (OUT_DIR / "README.md").write_text(make_readme(summary), encoding="utf-8")

    with (OUT_DIR / "validation_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, json.dumps(value) if isinstance(value, dict) else value])

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(OUT_DIR.rglob("*")):
            if path == ZIP_PATH:
                continue
            zf.write(path, path.relative_to(OUT_DIR.parent))

    print(f"Wrote {summary['record_count']} records to raw_payload_runs/all_runs.jsonl")
    print("Wrote scenario files to raw_payload_runs/scenarios/")
    print(f"Wrote manifest and summary files to {OUT_DIR}")
    print(f"Wrote archive to {ZIP_PATH}")


if __name__ == "__main__":
    main()
