# Clean Waveform Benchmark

*Back to [repository root](../README.md) · Related: [case study](../case-study/README.md) · Compare with [raw payload runs](../raw_payload_runs/README.md)*

![Waveform timing shift overlay](graphs/overlay_fill_state_timing_shift.png)

## Purpose

This folder contains the clean synthetic waveform benchmark used for feature inspection, visual explanation, and known-label inference demonstrations.

It is the best place to start if you want a controlled view of the signal behavior discussed in the case study.

## What is included

| File / folder | Purpose |
|---|---|
| `clean_waveform_dataset.json` | Full benchmark dataset with metadata, labels, waveform arrays, and engineered features |
| `clean_waveform_dataset.jsonl` | JSONL export for batch processing and scripting |
| `graphs/` | Per-scenario images plus overlay comparisons used for explanation and documentation |
| `reference_image_classification.md` | Mapping of reference images to scenario families |
| `inference_demo.py` | Dependency-light Python inference demo using k-nearest-neighbor classification |

## Dataset profile

| Metric | Value |
|---|---|
| Scenarios | 18 |
| Records | 442 |
| Samples per waveform | 160 |
| Record style | One canonical clean curve plus noisy variants |

## What this benchmark is good for

- Demonstrating waveform feature engineering
- Showing how fill-state timing shifts emerge
- Comparing site-class behavior patterns
- Running known-label prediction examples
- Producing visual material for technical documentation

## Quick start

Run the example inference flow from the repository root:

```bash
python3 clean_waveform_benchmark/inference_demo.py
```

The script loads `clean_waveform_dataset.json`, trains simple **k-nearest-neighbor** models, and predicts:

- `site_class`
- `fill_state`

Because the dataset is synthetic, expected outcomes are already available in each record's `labels` block.

## Visual anchors

| Fill-state timing shift | Site-class behavior |
|---|---|
| ![Fill-state timing shift](graphs/overlay_fill_state_timing_shift.png) | ![Site-class behavior](graphs/overlay_site_class_behavior.png) |

## Recommended exploration flow

1. Open `reference_image_classification.md` to understand scenario mapping.
2. Browse the overlay graphs in `graphs/`.
3. Run `inference_demo.py`.
4. Compare this clean benchmark against the noisier payload-style data in [`../raw_payload_runs/`](../raw_payload_runs/).

## Related documentation

- [Repository root](../README.md)
- [Case study README](../case-study/README.md)
- [Raw payload runs README](../raw_payload_runs/README.md)
