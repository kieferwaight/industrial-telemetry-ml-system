# The Compactor Became The Sensor
### From Electrical Signal To Dispatch Intelligence

[![Applied AI](https://img.shields.io/badge/Applied%20AI-Real%20Operations-0b7a75?style=for-the-badge)](../README.md)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Production%20Inference-005f73?style=for-the-badge)](03_Technical_Architecture.md#38-machine-learning-inference)
[![Scale](https://img.shields.io/badge/Scale-1000%2B%20Locations%20%7C%2046%20States-9b2226?style=for-the-badge)](#deployment-scale)
[![Latest](https://img.shields.io/badge/Latest%20Version-May%202026-ee9b00?style=for-the-badge)](#latest-version)

*Back to [repository root](../README.md) · Related: [clean waveform benchmark](../clean_waveform_benchmark/README.md) · Related: [raw payload runs](../raw_payload_runs/README.md)*


---

This technical case study details how electromagnetic telemetry, signal processing, and machine learning were deployed across a nationally distributed waste environment to transform ordinary compactors into operational intelligence systems.

The markdown chapter set in this directory is the canonical repository version of the case study.

## Latest Version

- Status: current canonical case study release
- Updated: May 2026
- Landing page entry point: [root README](../README.md)

## High-Impact Visual Entry Points

- System narrative map: [assets/figure-diagram-end-to-end-model-evolution-workflow.png](assets/figure-diagram-end-to-end-model-evolution-workflow.png)
- Device operations context: [assets/figure-diagram-iot-device-operational-workflow.png](assets/figure-diagram-iot-device-operational-workflow.png)
- Non-invasive sensing innovation: [assets/figure_1.3a_non-invasive_electromagnetic_sensor_clamped_around_the_primary_cable.png](assets/figure_1.3a_non-invasive_electromagnetic_sensor_clamped_around_the_primary_cable.png)
- AI/ML inference flow: [assets/figure-diagram-fullness-inference-workflow.png](assets/figure-diagram-fullness-inference-workflow.png)

## Contact

For research and educational collaboration:

- kiefer.waight@uta.edu

---

## Repository Navigation

| Need                                   | Go here                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| Read the full repository overview      | [Root README](../README.md)                                                                 |
| Inspect clean benchmark data           | [clean_waveform_benchmark/](../clean_waveform_benchmark/)                                   |
| Inspect payload-style parser test data | [raw_payload_runs/](../raw_payload_runs/)                                                   |
| Run the example inference demo         | [clean_waveform_benchmark/inference_demo.py](../clean_waveform_benchmark/inference_demo.py) |

---

## Deployment Scale

| Metric             | Value                      |
| ------------------ | -------------------------- |
| Customer Locations | 1,000+                     |
| States             | 46                         |
| Telemetry          | 24/7 industrial monitoring |
| Signal Events      | Millions analyzed          |

---

## Table of Contents

### Part I — Foundation

| Chapter                       | Title                 | Description                                                                       |
| ----------------------------- | --------------------- | --------------------------------------------------------------------------------- |
| [01](01_Executive_Summary.md) | **Executive Summary** | Business problem, technical strategy, research context, strategic significance    |
| [02](02_Core_Insight.md)      | **Core Insight**      | The compactor already contained the signal — crush cycles as behavioral telemetry |

**Chapter 01 Sections:**
- [1.1 The Business Problem](01_Executive_Summary.md#11-the-business-problem)
- [1.2 Technical Strategy](01_Executive_Summary.md#12-technical-strategy)
- [1.3 Research Context and Technical Legitimacy](01_Executive_Summary.md#13-research-context-and-technical-legitimacy)
- [1.4 Strategic Significance](01_Executive_Summary.md#14-strategic-significance)

**Chapter 02 Sections:**
- [2.1 The Compactor Already Contained the Signal](02_Core_Insight.md#21-the-compactor-already-contained-the-signal)
- [2.2 A Crush Cycle Became a Signal](02_Core_Insight.md#22-a-crush-cycle-became-a-signal)
- [2.3 Behavior Had to Be Learned, Not Defined](02_Core_Insight.md#23-behavior-had-to-be-learned-not-defined)
- [2.4 The System Learned More Than Fullness](02_Core_Insight.md#24-the-system-learned-more-than-fullness)
- [2.5 The Insight Extended Beyond Waste Operations](02_Core_Insight.md#25-the-insight-extended-beyond-waste-operations)

---

### Part II — Technical System

| Chapter                            | Title                      | Description                                                                          |
| ---------------------------------- | -------------------------- | ------------------------------------------------------------------------------------ |
| [03](03_Technical_Architecture.md) | **Technical Architecture** | Full-stack industrial intelligence pipeline — telemetry, processing, ML, dispatch    |
| [04](04_Signal_Modeling.md)        | **Signal Modeling**        | Reading industrial behavior as a time-series system — waveforms, baselines, features |

**Chapter 03 Sections:**
- [3.1 System Overview](03_Technical_Architecture.md#31-system-overview)
- [3.2 Telemetry Collection](03_Technical_Architecture.md#32-telemetry-collection)
- [3.3 Cellular Transport and Ingestion](03_Technical_Architecture.md#33-cellular-transport-and-ingestion)
- [3.4 Raw Event Storage](03_Technical_Architecture.md#34-raw-event-storage)
- [3.5 Signal Processing](03_Technical_Architecture.md#35-signal-processing)
- [3.6 Feature Engineering](03_Technical_Architecture.md#36-feature-engineering)
- [3.7 Device Fingerprint Normalization](03_Technical_Architecture.md#37-device-fingerprint-normalization)
- [3.8 Machine Learning Inference](03_Technical_Architecture.md#38-machine-learning-inference)
- [3.9 Dispatch and Workflow Automation](03_Technical_Architecture.md#39-dispatch-and-workflow-automation)
- [3.10 Administrative Interface](03_Technical_Architecture.md#310-administrative-interface)
- [3.11 Ground-Truth Feedback Loop](03_Technical_Architecture.md#311-ground-truth-feedback-loop)
- [3.12 Architecture Summary](03_Technical_Architecture.md#312-architecture-summary)

**Chapter 04 Sections:**
- [4.1 Understanding the Crush Cycle](04_Signal_Modeling.md#41-understanding-the-crush-cycle)
- [4.2 The Startup Spike Problem](04_Signal_Modeling.md#42-the-startup-spike-problem)
- [4.3 Empty-State Baselines](04_Signal_Modeling.md#43-empty-state-baselines)
- [4.4 Resistance Curves Became Predictive](04_Signal_Modeling.md#44-resistance-curves-became-predictive)
- [4.5 Cycle Duration Was a Strong Behavioral Signal](04_Signal_Modeling.md#45-cycle-duration-was-a-strong-behavioral-signal)
- [4.6 Repeated Crush Attempts](04_Signal_Modeling.md#46-repeated-crush-attempts)
- [4.7 Feature Engineering Beyond Raw Current](04_Signal_Modeling.md#47-feature-engineering-beyond-raw-current)
- [4.8 Device Fingerprinting](04_Signal_Modeling.md#48-device-fingerprinting)
- [4.9 Site-Type Segmentation](04_Signal_Modeling.md#49-site-type-segmentation)
- [4.10 Signal Drift](04_Signal_Modeling.md#410-signal-drift)
- [4.11 Ground Truth Was the Hardest Part](04_Signal_Modeling.md#411-ground-truth-was-the-hardest-part)
- [4.12 Confidence Scoring](04_Signal_Modeling.md#412-confidence-scoring)
- [4.13 The Modeling Shift](04_Signal_Modeling.md#413-the-modeling-shift)

---

### Part III — The Hard Problems

| Chapter                               | Title                       | Description                                                                      |
| ------------------------------------- | --------------------------- | -------------------------------------------------------------------------------- |
| [05](05_Why_This_Was_Hard.md)         | **Why This Was Hard**       | No ground truth sensor, drifting environments, noisy labels, physical complexity |
| [06](06_Ground_Truth_and_Labeling.md) | **Ground Truth & Labeling** | How operational workflows became the training dataset                            |
| [07](07_Model_Evolution.md)           | **Model Evolution**         | Six phases from raw observation to confidence-weighted automation                |
| [08](08_Failure_Cases.md)             | **Failure Cases**           | Construction false positives, dense material misclassification, operator noise   |
| [09](09_Signal_Drift.md)              | **Signal Drift**            | Equipment wear, maintenance resets, occupancy changes, continuous recalibration  |

**Chapter 05 Sections:**
- [5.1 There Was No Ground Truth Sensor](05_Why_This_Was_Hard.md#51-there-was-no-ground-truth-sensor)
- [5.2 Every Compactor Behaved Differently](05_Why_This_Was_Hard.md#52-every-compactor-behaved-differently)
- [5.3 Waste Is Not a Stable Material](05_Why_This_Was_Hard.md#53-waste-is-not-a-stable-material)
- [5.4 Human Behavior Introduced Noise](05_Why_This_Was_Hard.md#54-human-behavior-introduced-noise)
- [5.5 Labels Were Delayed and Imperfect](05_Why_This_Was_Hard.md#55-labels-were-delayed-and-imperfect)
- [5.6 The Environment Drifted Continuously](05_Why_This_Was_Hard.md#56-the-environment-drifted-continuously)
- [5.7 The System Had to Be Trusted Operationally](05_Why_This_Was_Hard.md#57-the-system-had-to-be-trusted-operationally)
- [5.8 Physical Systems Do Not Behave Like Software Systems](05_Why_This_Was_Hard.md#58-physical-systems-do-not-behave-like-software-systems)
- [5.9 The Real Problem Was Interpretation](05_Why_This_Was_Hard.md#59-the-real-problem-was-interpretation)
- [5.10 Why This Matters](05_Why_This_Was_Hard.md#510-why-this-matters)

**Chapter 06 Sections:**
- [6.1 The Operational World Became the Labeling System](06_Ground_Truth_and_Labeling.md#61-the-operational-world-became-the-labeling-system)
- [6.2 Pickup Events Became Ground Truth Anchors](06_Ground_Truth_and_Labeling.md#62-pickup-events-became-ground-truth-anchors)
- [6.3 The Dashboard Became a Labeling Tool](06_Ground_Truth_and_Labeling.md#63-the-dashboard-became-a-labeling-tool)
- [6.4 Labels Were Delayed](06_Ground_Truth_and_Labeling.md#64-labels-were-delayed)
- [6.5 Labels Were Noisy](06_Ground_Truth_and_Labeling.md#65-labels-were-noisy)
- [6.6 Confidence Weighting Became Necessary](06_Ground_Truth_and_Labeling.md#66-confidence-weighting-became-necessary)
- [6.7 Site History Became Part of the Label](06_Ground_Truth_and_Labeling.md#67-site-history-became-part-of-the-label)
- [6.8 Failed Predictions Were Extremely Valuable](06_Ground_Truth_and_Labeling.md#68-failed-predictions-were-extremely-valuable)
- [6.9 Operational Intelligence Was the Dataset](06_Ground_Truth_and_Labeling.md#69-operational-intelligence-was-the-dataset)
- [6.10 Why This Matters](06_Ground_Truth_and_Labeling.md#610-why-this-matters)

**Chapter 07 Sections:**
- [7.1 Raw Telemetry Observation](07_Model_Evolution.md#71-raw-telemetry-observation)
- [7.2 Rule-Based Thresholds](07_Model_Evolution.md#72-rule-based-thresholds)
- [7.3 Cycle Segmentation and Signal Processing](07_Model_Evolution.md#73-cycle-segmentation-and-signal-processing)
- [7.4 Device Fingerprinting](07_Model_Evolution.md#74-device-fingerprinting)
- [7.5 Site-Type Segmentation](07_Model_Evolution.md#75-site-type-segmentation)
- [7.6 Behavioral Trend Modeling](07_Model_Evolution.md#76-behavioral-trend-modeling)
- [7.7 Confidence Scoring](07_Model_Evolution.md#77-confidence-scoring)
- [7.8 Operational Feedback Integration](07_Model_Evolution.md#78-operational-feedback-integration)
- [7.9 Automation Readiness](07_Model_Evolution.md#79-automation-readiness)
- [7.10 The Most Important Evolution](07_Model_Evolution.md#710-the-most-important-evolution)
- [7.11 Why This Matters](07_Model_Evolution.md#711-why-this-matters)

**Chapter 08 Sections:**
- [8.1 Construction Site False Positives](08_Failure_Cases.md#81-construction-site-false-positives)
- [8.2 Dense Material Misclassification](08_Failure_Cases.md#82-dense-material-misclassification)
- [8.3 Operator-Induced Noise](08_Failure_Cases.md#83-operator-induced-noise)
- [8.4 Mechanical Drift](08_Failure_Cases.md#84-mechanical-drift)
- [8.5 Sparse Data Environments](08_Failure_Cases.md#85-sparse-data-environments)
- [8.6 Delayed Operational Labels](08_Failure_Cases.md#86-delayed-operational-labels)
- [8.7 Connectivity and Missing Telemetry](08_Failure_Cases.md#87-connectivity-and-missing-telemetry)
- [8.8 False Negatives](08_Failure_Cases.md#88-false-negatives)
- [8.9 Overconfidence](08_Failure_Cases.md#89-overconfidence)
- [8.10 Failure Analysis Improved the System](08_Failure_Cases.md#810-failure-analysis-improved-the-system)
- [8.11 The Most Important Lesson](08_Failure_Cases.md#811-the-most-important-lesson)

**Chapter 09 Sections:**
- [9.1 Drift Emerged From Multiple Sources](09_Signal_Drift.md#91-drift-emerged-from-multiple-sources)
- [9.2 Equipment Wear Changed the Signal](09_Signal_Drift.md#92-equipment-wear-changed-the-signal)
- [9.3 Maintenance Events Could Reset Behavioral Patterns](09_Signal_Drift.md#93-maintenance-events-could-reset-behavioral-patterns)
- [9.4 Occupancy Changes Altered Usage Patterns](09_Signal_Drift.md#94-occupancy-changes-altered-usage-patterns)
- [9.5 Seasonal Waste Behavior Was Significant](09_Signal_Drift.md#95-seasonal-waste-behavior-was-significant)
- [9.6 Waste Composition Drifted Over Time](09_Signal_Drift.md#96-waste-composition-drifted-over-time)
- [9.7 Operator Behavior Drifted Too](09_Signal_Drift.md#97-operator-behavior-drifted-too)
- [9.8 Drift Detection Became a Core System Capability](09_Signal_Drift.md#98-drift-detection-became-a-core-system-capability)
- [9.9 Drift Was Not an Edge Case](09_Signal_Drift.md#99-drift-was-not-an-edge-case)
- [9.10 Why This Matters](09_Signal_Drift.md#910-why-this-matters)

---

### Part IV — Operational Reality

| Chapter                             | Title                       | Description                                                                    |
| ----------------------------------- | --------------------------- | ------------------------------------------------------------------------------ |
| [10](10_Operational_Integration.md) | **Operational Integration** | Dispatch loop, condition-based hauling, invoice auditing, automation path      |
| [11](11_Nationwide_Scale.md)        | **Nationwide Scale**        | 1,000+ locations, cellular deployment, heterogeneous equipment, generalization |
| [12](12_Business_Outcome.md)        | **Business Outcome**        | Haul reduction, overflow avoidance, operational visibility, strategic value    |

**Chapter 10 Sections:**
- [10.1 The Dispatch Workflow](10_Operational_Integration.md#101-the-dispatch-workflow)
- [10.2 Condition-Based Hauling](10_Operational_Integration.md#102-condition-based-hauling)
- [10.3 Dispatch Recommendations](10_Operational_Integration.md#103-dispatch-recommendations)
- [10.4 Human Review and Account Management](10_Operational_Integration.md#104-human-review-and-account-management)
- [10.5 Exception Handling](10_Operational_Integration.md#105-exception-handling)
- [10.6 Haul Confirmation Closed the Loop](10_Operational_Integration.md#106-haul-confirmation-closed-the-loop)
- [10.7 Invoice Auditing and Service Validation](10_Operational_Integration.md#107-invoice-auditing-and-service-validation)
- [10.8 Reporting and Operational Visibility](10_Operational_Integration.md#108-reporting-and-operational-visibility)
- [10.9 Operational Segmentation](10_Operational_Integration.md#109-operational-segmentation)
- [10.10 The Dashboard Was an Operational Tool](10_Operational_Integration.md#1010-the-dashboard-was-an-operational-tool)
- [10.11 Automation Was Introduced Gradually](10_Operational_Integration.md#1011-automation-was-introduced-gradually)
- [10.12 The Most Important Operational Shift](10_Operational_Integration.md#1012-the-most-important-operational-shift)
- [10.13 Why This Matters](10_Operational_Integration.md#1013-why-this-matters)

**Chapter 11 Sections:**
- [11.1 Distributed Physical Infrastructure](11_Nationwide_Scale.md#111-distributed-physical-infrastructure)
- [11.2 Cellular Connectivity Made National Deployment Possible](11_Nationwide_Scale.md#112-cellular-connectivity-made-national-deployment-possible)
- [11.3 Heterogeneous Equipment Increased Complexity](11_Nationwide_Scale.md#113-heterogeneous-equipment-increased-complexity)
- [11.4 Site-Type Diversity Was Operationally Important](11_Nationwide_Scale.md#114-site-type-diversity-was-operationally-important)
- [11.5 Nationwide Vendor Coordination](11_Nationwide_Scale.md#115-nationwide-vendor-coordination)
- [11.6 Connectivity Realities at Scale](11_Nationwide_Scale.md#116-connectivity-realities-at-scale)
- [11.7 Scale Increased the Value of the System](11_Nationwide_Scale.md#117-scale-increased-the-value-of-the-system)
- [11.8 Generalization Was the Real Achievement](11_Nationwide_Scale.md#118-generalization-was-the-real-achievement)
- [11.9 Operational Credibility Came From Deployment Reality](11_Nationwide_Scale.md#119-operational-credibility-came-from-deployment-reality)
- [11.10 The Nationwide Layer Changed the Nature of the Project](11_Nationwide_Scale.md#1110-the-nationwide-layer-changed-the-nature-of-the-project)
- [11.11 Why This Matters](11_Nationwide_Scale.md#1111-why-this-matters)

**Chapter 12 Sections:**
- [12.1 The Core Operational Shift](12_Business_Outcome.md#121-the-core-operational-shift)
- [12.2 Haul Reduction and Utilization Improvement](12_Business_Outcome.md#122-haul-reduction-and-utilization-improvement)
- [12.3 Avoided Overflow Events](12_Business_Outcome.md#123-avoided-overflow-events)
- [12.4 Operational Visibility Became a Major Outcome](12_Business_Outcome.md#124-operational-visibility-became-a-major-outcome)
- [12.5 Reduced Manual Oversight](12_Business_Outcome.md#125-reduced-manual-oversight)
- [12.6 Invoice Auditing and Vendor Accountability](12_Business_Outcome.md#126-invoice-auditing-and-vendor-accountability)
- [12.7 Route and Fleet Efficiency](12_Business_Outcome.md#127-route-and-fleet-efficiency)
- [12.8 Environmental and ESG Implications](12_Business_Outcome.md#128-environmental-and-esg-implications)
- [12.9 The Most Important Outcome Was Trustworthy Operational Intelligence](12_Business_Outcome.md#129-the-most-important-outcome-was-trustworthy-operational-intelligence)
- [12.10 The System Improved Decision Quality](12_Business_Outcome.md#1210-the-system-improved-decision-quality)
- [12.11 Business Outcomes Were Incremental but Compounding](12_Business_Outcome.md#1211-business-outcomes-were-incremental-but-compounding)
- [12.12 Strategic Outcome](12_Business_Outcome.md#1212-strategic-outcome)
- [12.13 Why This Matters](12_Business_Outcome.md#1213-why-this-matters)

---

### Part V — Strategic Framing

| Chapter                            | Title                           | Description                                                         |
| ---------------------------------- | ------------------------------- | ------------------------------------------------------------------- |
| [13](13_Strategic_Significance.md) | **Strategic Significance**      | The compactor as instrument, industrial AI thesis, closed-loop moat |
| [14](14_Appendix_A.md)             | **Appendix A: Public Evidence** | Source register, citation matrix, validated claims                  |

**Chapter 13 Sections:**
- [13.1 The Compactor Became an Instrument](13_Strategic_Significance.md#131-the-compactor-became-an-instrument)
- [13.2 The Broader Industrial AI Thesis](13_Strategic_Significance.md#132-the-broader-industrial-ai-thesis)
- [13.3 The System Modeled Behavior, Not Just Data](13_Strategic_Significance.md#133-the-system-modeled-behavior-not-just-data)
- [13.4 Operational Intelligence Became the Product](13_Strategic_Significance.md#134-operational-intelligence-became-the-product)
- [13.5 The Platform Demonstrated Commercial Viability](13_Strategic_Significance.md#135-the-platform-demonstrated-commercial-viability)
- [13.6 This Was an Early Applied ML Infrastructure System](13_Strategic_Significance.md#136-this-was-an-early-applied-ml-infrastructure-system)
- [13.7 The Most Important Insight](13_Strategic_Significance.md#137-the-most-important-insight)
- [13.8 The Closed-Loop Learning System Was the Moat](13_Strategic_Significance.md#138-the-closed-loop-learning-system-was-the-moat)
- [13.9 Why This Matters Beyond Waste](13_Strategic_Significance.md#139-why-this-matters-beyond-waste)
- [13.10 Closing Synthesis](13_Strategic_Significance.md#1310-closing-synthesis)

---

## Image Assets

All extracted images are available in the [`assets/`](assets/) directory.

**Key named assets:**

| File                                                                    | Description                         |
| ----------------------------------------------------------------------- | ----------------------------------- |
| `assets/style-style-element-blueprint-compactor-cover.png`              | Cover photograph                    |
| `assets/figure-illustration-compactor-hardware-city-scene.png`          | Compactor hardware in field         |
| `assets/figure-illustration-waste-collection-architecture-overview.png` | System architecture overview        |
| `assets/figure-diagram-electromagnetic-sensor-telemetry-flow.png`       | Telemetry data flow                 |
| `assets/figure-diagram-traditional-vs-sensor-comparison.png`            | Full pipeline architecture          |
| `assets/figure-waveform-empty-compactor-crush-cycle.png`                | Empty-state crush cycle waveform    |
| `assets/figure-waveform-full-compactor-crush-cycle.png`                 | Full-state crush cycle waveform     |
| `assets/figure-diagram-empty-vs-full-waveform-overlay.png`              | Signal progression over fill states |
| `assets/figure-diagram-compactor-feature-engineering.png`               | Feature engineering structure       |
| `assets/figure-diagram-device-fingerprint-comparison.png`               | Device fingerprint normalization    |
| `assets/figure-diagram-site-type-waveform-overlay.png`                  | Site-type segmentation model        |
| `assets/figure-diagram-fullness-inference-workflow.png`                 | Signal analysis full view           |
| `assets/figure-diagram-end-to-end-model-evolution-workflow.png`         | Model evolution phases              |
| `assets/figure-diagram-iot-device-operational-workflow.png`             | Operational workflow context        |
| `assets/figure-diagram-nationwide-deployment-workflow.png`              | Nationwide deployment context       |
| `assets/figure-diagram-signal-processing-normalization-workflow.png`    | Scale operations photo              |
| `assets/figure-mockup-business-outcome-dashboard.png`                   | Business outcome context            |
| `assets/figure-diagram-human-feedback-loop.png`                         | Strategic significance diagram      |
| `assets/planning-mockup-executive-summary-pdf-draft.png`                | Closing synthesis image             |

---

## Image Layout Utilities

Use a single wrapper plus utility classes for consistent image placement in Markdown preview.

### Base Pattern

```html
<div class="img w-60 center">
	<img src="assets/figure.png" alt="Figure" />
</div>
```

### Available Utility Classes

- Wrapper: `.img`
- Widths: `.w-full`, `.w-75`, `.w-60`, `.w-50`, `.w-40`
- Alignment: `.center`, `.left`, `.right`
- Optional float: `.float-right`, `.float-left`
- Float reset: `.clear`
- Optional caption: `.img-caption`

### Usage Patterns

Centered image:

```html
<div class="img w-60 center">
	<img src="assets/image.png" alt="Centered example" />
</div>
```

Left aligned:

```html
<div class="img w-60 left">
	<img src="assets/image.png" alt="Left example" />
</div>
```

Right aligned:

```html
<div class="img w-40 right">
	<img src="assets/image.png" alt="Right example" />
</div>
```

Float right with wrapping text:

```html
<div class="img w-40 float-right">
	<img src="assets/image.png" alt="Float example" />
</div>

This paragraph will wrap around the image in Markdown preview.

<div class="clear"></div>
```

Optional caption:

```html
<div class="img w-60 center">
	<img src="assets/image.png" alt="Caption example" />
	<div class="img-caption">Optional caption text</div>
</div>
```

Recommended defaults for this case study:

- Use `.img w-60 center` for most figures.
- Use `.img w-40 right` for tighter callout graphics.
- Use `.float-right` only when text wrapping is intentional.
- Add `.clear` after any floated image block.

---

*This case study documents a real production system. Proprietary operational details have been abstracted while preserving technical accuracy.*

*Back to [repository root](../README.md)*
