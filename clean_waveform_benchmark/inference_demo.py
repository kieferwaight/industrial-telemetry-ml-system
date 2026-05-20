#!/usr/bin/env python3
"""
Simple known-outcome inference demo for clean_waveform_dataset.json.

This intentionally avoids external ML dependencies. It trains two k-nearest-neighbor
classifiers from the generated feature vectors:
1. site_class prediction
2. fill_state prediction

Because the dataset is synthetic, the expected outcome is known in each record's
labels block. The point is to demonstrate the end-to-end mechanics of feature
extraction, training, prediction, and validation against known labels.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


FEATURES = [
    "duration_s",
    "peak_current_a",
    "mean_current_a",
    "area_under_curve_a_s",
    "peak_timing_s",
    "peak_timing_ratio",
    "ramp_slope_a_per_s",
    "release_slope_a_per_s",
    "early_energy_ratio",
    "compression_variability",
]


def load_rows(path: str | Path):
    data = json.loads(Path(path).read_text())
    return data["records"]


def vector(row):
    return [float(row["features"][name]) for name in FEATURES]


def standardize(train_vectors, vectors):
    means = [sum(col) / len(col) for col in zip(*train_vectors)]
    stds = []
    for j, mean in enumerate(means):
        variance = sum((v[j] - mean) ** 2 for v in train_vectors) / max(1, len(train_vectors) - 1)
        stds.append(math.sqrt(variance) or 1.0)
    return [[(x - means[j]) / stds[j] for j, x in enumerate(v)] for v in vectors], means, stds


class KNearestNeighbors:
    def __init__(self, label_key, k=5):
        self.label_key = label_key
        self.k = k
        self.means = []
        self.stds = []
        self.train_rows = []
        self.train_vectors = []

    def fit(self, rows):
        raw_vectors = [vector(r) for r in rows]
        self.train_vectors, self.means, self.stds = standardize(raw_vectors, raw_vectors)
        self.train_rows = rows
        return self

    def _scale_one(self, row):
        return [(x - self.means[j]) / self.stds[j] for j, x in enumerate(vector(row))]

    def predict_one(self, row):
        vec = self._scale_one(row)
        scored = []
        for train_row, train_vec in zip(self.train_rows, self.train_vectors):
            distance = math.sqrt(sum((vec[j] - train_vec[j]) ** 2 for j in range(len(vec))))
            scored.append((distance, train_row["labels"][self.label_key]))
        neighbors = sorted(scored, key=lambda x: x[0])[: self.k]
        vote_weight = Counter()
        for distance, label in neighbors:
            vote_weight[label] += 1.0 / (distance + 1e-9)
        prediction = vote_weight.most_common(1)[0][0]
        confidence = vote_weight[prediction] / sum(vote_weight.values())
        return prediction, confidence, neighbors

    def score(self, rows):
        correct = 0
        confusion = Counter()
        examples = []
        for row in rows:
            pred, conf, _ = self.predict_one(row)
            actual = row["labels"][self.label_key]
            correct += int(pred == actual)
            confusion[(actual, pred)] += 1
            if len(examples) < 10:
                examples.append((row["record_id"], actual, pred, round(conf, 3)))
        return {
            "target": self.label_key,
            "accuracy": correct / len(rows),
            "correct": correct,
            "total": len(rows),
            "confusion": dict(confusion),
            "examples": examples,
        }


def main():
    rows = load_rows(Path(__file__).with_name("clean_waveform_dataset.json"))
    # Use noisy variants for train/test. Canonicals are reserved as clean references.
    rows = [r for r in rows if r["variant_role"] == "noisy_variant" and r["labels"]["fill_state"] != "anomaly_double_run"]
    random.Random(7).shuffle(rows)
    split = int(len(rows) * 0.7)
    train, test = rows[:split], rows[split:]

    site_model = KNearestNeighbors("site_class", k=5).fit(train)
    fill_model = KNearestNeighbors("fill_state", k=5).fit(train)

    print("Training rows:", len(train))
    print("Test rows:", len(test))
    for result in [site_model.score(test), fill_model.score(test)]:
        print("\nTarget:", result["target"])
        print(f"Accuracy: {result['accuracy']:.3f} ({result['correct']}/{result['total']})")
        print("Example predictions:")
        for record_id, actual, pred, conf in result["examples"]:
            print(f"  {record_id}: actual={actual} predicted={pred} confidence={conf}")

    print("\nSingle-row inference example:")
    row = test[0]
    site_pred, site_conf, _ = site_model.predict_one(row)
    fill_pred, fill_conf, _ = fill_model.predict_one(row)
    print(json.dumps({
        "record_id": row["record_id"],
        "known_site_class": row["labels"]["site_class"],
        "predicted_site_class": site_pred,
        "site_confidence": round(site_conf, 3),
        "known_fill_state": row["labels"]["fill_state"],
        "predicted_fill_state": fill_pred,
        "fill_confidence": round(fill_conf, 3),
    }, indent=2))


if __name__ == "__main__":
    main()
