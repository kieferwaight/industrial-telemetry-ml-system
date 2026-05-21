#!/usr/bin/env python3
"""
Export the trained KNN model to a JSON file.
"""

import json
from pathlib import Path
import sys

# Add benchmark dir to path
sys.path.append(str(Path(__file__).parent.parent / "clean_waveform_benchmark"))

from inference_demo import KNearestNeighbors, load_rows

def export_model():
    data_path = Path(__file__).parent.parent / "clean_waveform_benchmark" / "clean_waveform_dataset.json"
    rows = load_rows(data_path)
    # Use noisy variants for training
    train_rows = [r for r in rows if r["variant_role"] == "noisy_variant"]
    
    # We'll just export the site_class model as an example
    model = KNearestNeighbors("site_class", k=5).fit(train_rows)
    
    model_data = {
        "model_type": "KNearestNeighbors",
        "target": "site_class",
        "k": model.k,
        "means": model.means,
        "stds": model.stds,
        "train_vectors": model.train_vectors,
        "train_labels": [r["labels"]["site_class"] for r in model.train_rows],
        "feature_names": [
            "duration_s", "peak_current_a", "mean_current_a", "area_under_curve_a_s",
            "peak_timing_s", "peak_timing_ratio", "ramp_slope_a_per_s",
            "release_slope_a_per_s", "early_energy_ratio", "compression_variability"
        ]
    }
    
    output_path = Path(__file__).parent / "baseline_knn_site_class.json"
    output_path.write_text(json.dumps(model_data, indent=2))
    print(f"Exported model to {output_path}")

if __name__ == "__main__":
    export_model()
