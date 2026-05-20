# Reference Image Classification

The attached images were classified into waveform/modeling concepts and mapped to generated synthetic dataset IDs. These classifications are treated as known labels for this benchmark, not as inferred unknowns.

| File | Classification | Mapped generated datasets | Notes |
|---|---|---|---|
| `200F3925-F99A-4DDA-B247-99D9D9896ACD.jpeg` | `empty_vs_full_temporal_shift_overlay` | `apartment_empty`, `apartment_full`, `office_empty`, `office_full` | Shows the primary supervised signal: full cycles reach peak resistance earlier than empty cycles while startup spikes are not fill indicators. |
| `1F409693-39CA-4CC5-83AF-374A4520E8CE.jpeg` | `site_class_signal_behavior_comparison` | `apartment_empty`, `office_empty`, `retail_partial`, `restaurant_partial`, `construction_partial` | Defines site-class prior behavior and expected confidence differences by material density and operating environment. |
| `8A36C567-DC28-4AE3-9F0F-234E0F75C827.jpeg` | `device_fingerprint_variability` | `device_a_empty`, `device_b_empty`, `device_c_empty`, `device_d_empty_multipulse` | Shows that identical operational states vary by compactor make, age, amplitude, duration, and peak timing. |
| `67AB489E-AAEF-4F16-AC98-9BB8FD439657.jpeg` | `compactor_cycle_phase_and_feature_map` | `apartment_empty`, `apartment_full`, `retail_full`, `restaurant_full` | Defines phase landmarks and engineered features: startup, ramp, compression, peak resistance, and release. |
| `F4B4E431-B6F4-4366-9EAB-43B304C20652.jpeg` | `patent_style_fullness_reading_traces` | `patent_style_compactor_a_partial`, `patent_style_compactor_b_empty`, `patent_style_compactor_b_partial` | Shows older fullness-reading style traces, including Compactor A partial spike and Compactor B empty/partial differences. |
| `F2E53358-B10F-4E8E-9300-47D67AF6E3BC.jpeg` | `patent_style_trace_figures_labeled` | `patent_style_compactor_a_partial`, `patent_style_compactor_b_empty`, `patent_style_compactor_b_partial` | Duplicate/variant of the patent-style trace set with figure labels preserved. |
| `IMG_1953.jpeg` | `stacked_site_class_and_fill_state_inference_architecture` | `all site-class scenarios`, `all full/empty/partial fill-state scenarios` | Defines the intended two-stage inference demonstration: site-class identification followed by site-calibrated full/not-full prediction. |

## Label taxonomy used in the generated JSON

- **Fill state**: `empty`, `partial`, `full`, and `anomaly_double_run`.
- **Site class**: `apartment_communities`, `office_campuses`, `retail_grocery`, `restaurant_hospitality`, `construction_sites`, plus lab/reference classes for device-fingerprint and patent-style traces.
- **Device fingerprint**: make/age or trace style, used to model amplitude, duration, startup structure, and peak timing variation.
- **Known outcomes**: every generated record includes labels under `labels`, and these are the ground truth used by the inference demo.