# Mock Compaction JSONL Run Data

This archive contains synthetic, standardized JSONL telemetry records modeled after the attached CD2.2-006 compaction-device case-study payload.

## Contents

- `all_runs.jsonl`: every generated record in one file.
- `scenarios/*.jsonl`: one JSONL file per scenario/edge-case family.
- `manifest.json`: generation settings, scenario descriptions, and validation summary.
- `schema.json`: informal JSON schema for the normalized record shape.
- `validation_summary.csv`: compact counts and metric ranges for quick inspection.

## Scale

- Total records: 725
- Usable sample count range: 18 to 214
- Records with split labels: 200
- Records with missing CSV value slots: 30

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
