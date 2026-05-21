# Appendix C

##### [**Undermind**](https://undermind.ai)

---


## Table of Contents

- [Appendix C: Research Comparison Sources and Provenance](#appendix-c-research-comparison-sources-and-provenance)
  - [Purpose and Use](#purpose-and-use)
  - [Pull Provenance for the Augmented Case Study](#pull-provenance-for-the-augmented-case-study)
  - [Academic Comparison Source Register](#academic-comparison-source-register)
  - [Research Integration Map](#research-integration-map)
  - [Reading Guide](#reading-guide)
  - [References](#references)

# Appendix C: Research Comparison Sources and Provenance

## Purpose and Use

This appendix captures the academic comparison sources used to position the case study, along with provenance for the augmented chapters.

Use this appendix when the question is:

- which papers informed the research framing,
- what each paper contributed,
- and where those additions were used in the file set.

For public company and operating evidence, use \[Appendix A\] and \[Appendix B\].

## Pull Provenance for the Augmented Case Study

The case study now draws from four distinct evidence pools:

| Evidence pool | What was pulled | Pull basis | Main use in file set |
|:---|:---|:---|:---|
| Existing public evidence register A1 to A54 | operating scale, product capability, transaction history, public case examples, market context | prior appendix collection pass | \[00 Executive Summary\], \[11 Nationwide Scale\], \[12 Business Outcome\], \[13 Strategic Significance\], \[Appendix A\], \[Appendix B\] |
| Deep search summary for Recent AI comparisons for industrial telemetry work | literature framing, ranked relevance, and initial positioning of the work as industrial soft sensing rather than ordinary smart bin monitoring | project deep search summary | \[14 Research Positioning\], \[03 Technical Architecture\], \[09 Signal Drift\], \[11 Nationwide Scale\], \[13 Strategic Significance\] |
| Full PDF reads of comparison papers | sensing modality, labels, deployment details, operational use, reliability lessons, and reported metrics | direct PDF extraction from \[Rut20\], \[Sob23b\], \[Hei21\], \[Mel20\], \[Fer18\], \[Hen19\], \[Bro23\], \[Pol24\], \[Har21\], \[Jou21\] | \[14 Research Positioning\] and targeted augmentations to \[00 Executive Summary\], \[03 Technical Architecture\], \[09 Signal Drift\], \[11 Nationwide Scale\], \[13 Strategic Significance\] |
| Metadata and abstracts for framing papers | soft sensor definition, fleet knowledge framing, and survey-level context | paper metadata for \[Jia21\] and \[Yan25\] | \[14 Research Positioning\], \[03 Technical Architecture\], \[11 Nationwide Scale\], \[13 Strategic Significance\] |

## Academic Comparison Source Register

| Cite key | Source type | Data pulled into the case study | Pulled from | Main use |
|:---|:---|:---|:---|:---|
| \[Jia21\] | Soft sensor review | definition of soft sensing and the broader industrial framing for inferring unmeasured state from routine telemetry | abstract and metadata | anchors the overall research frame |
| \[Mel20\] | Commercial waste collection case | ultrasonic sensing stack, GPS and ERP data, 47 sensor deployment, anomaly detection and 48 hour fill prediction | full PDF read | establishes that recent waste work usually depends on direct sensing |
| \[Rut20\] | Smart waste ML system | ultrasonic plus accelerometer sensing, emptying detection task, label construction from service records, Random Forest results, and forecast support | full PDF read | shows a strong waste AI comparator that still relies on direct sensing |
| \[Fer18\] | Waste fill prediction and routing | 217 container dataset, fill prediction thresholds, and route optimization results | full PDF read | supports the routing and operational decision comparison |
| \[Bro23\] | Monitoring approach comparison | direct ultrasonic sensing versus driver observation, Gaussian process forecasting, and collection versus overflow trade-off | full PDF read | supports the low-cost monitoring comparison |
| \[Pol24\] | Predicted fill levels for robotic service | manually gathered training labels, XGBoost prediction, and route and energy optimization gains | full PDF read | shows decision integration without permanent sensors at deployment |
| \[Sob23b\] | Industrial soft sensor | current, torque, and speed inputs, virtual sensor rationale, PLC deployment, and production accounting results | full PDF read | strongest industrial comparator for telemetry-based hidden-state inference |
| \[Hei21\] | Indirect industrial measurement | motor power input, idle power estimation, state-dependent indirect mass estimation, and hardware replacement rationale | full PDF read | supports the claim that indirect telemetry can replace costly instrumentation |
| \[Hen19\] | Fleet anomaly monitoring | online fleet comparison, no large historical dataset required, electrical and vibration signatures, and interpretability | full PDF read | supports fleet-scale comparison and heterogeneity handling |
| \[Har21\] | Distributed digital twin deployment | embedded execution limits, data prioritization, uncertainty-based novelty detection, and model synchronization loop | full PDF read | supports edge-to-fleet architecture and retraining discussion |
| \[Jou21\] | Industrial ML reliability | sensor drift, concept drift, calibration decay, and the need for online monitoring and uncertainty-aware maintenance | full PDF read | supports the signal drift chapter |
| \[Yan25\] | Fleet methods overview | data scarcity and heterogeneity framing and stepwise fleet method guidance for industrial deployments | abstract and metadata | supports the nationwide fleet framing |

## Research Integration Map

| File | Research addition |
|:---|:---|
| \[00 Executive Summary\] | positions the work against smart waste sensing and industrial soft sensing |
| \[03 Technical Architecture\] | compares the stack to virtual sensor and fleet architecture literature |
| \[09 Signal Drift\] | ties drift handling to industrial reliability research |
| \[11 Nationwide Scale\] | ties distributed deployment to fleet monitoring and heterogeneous asset literature |
| \[13 Strategic Significance\] | frames the project as an early applied industrial AI and soft sensor case |
| \[14 Research Positioning\] | provides the dedicated literature comparison chapter |

## Reading Guide

A simple way to read the research layer is:

1.  Start with \[14 Research Positioning\] for the full comparison argument.
2.  Use the source register above to see which papers support each comparison move.
3.  Use the integration map to trace where the literature was folded into the broader case-study set.

---

## References

\[Rut20\] D. Rutqvist, D. Kleyko, and F. Blomstedt, “An Automated Machine Learning Approach for Smart Waste Management Systems,” *IEEE Transactions on Industrial Informatics*, vol. 16, pp. 384–392, Jan. 2020, doi: [10.1109/TII.2019.2915572](https://doi.org/10.1109/TII.2019.2915572).

\[Sob23b\] S. G. A. Sobreira, P. Gomes, G. P. R. Filho, and G. Pessin, “A Data-Driven Soft Sensor for Mass Flow Estimation,” *IEEE Transactions on Instrumentation and Measurement*, vol. 72, pp. 1–9, 2023, doi: [10.1109/TIM.2023.3273658](https://doi.org/10.1109/TIM.2023.3273658).

\[Hei21\] B. Heinzl, J. Martinez-Gil, J. Himmelbauer, M. Rossbory, C. Hinterdorfer, and C. Hinterreiter, “Indirect Mass Flow Estimation based on Power Measurements of Conveyor Belts in Mineral Processing Applications,” *2021 IEEE 19th International Conference on Industrial Informatics (INDIN)*, pp. 1–6, Jul. 2021, doi: [10.1109/INDIN45523.2021.9557482](https://doi.org/10.1109/INDIN45523.2021.9557482).

\[Mel20\] F. Melakessou, P. Kugener, N. AlNaffakh, S. Faye, and D. Khadraoui, “Heterogeneous Sensing Data Analysis for Commercial Waste Collection,” *Sensors (Basel, Switzerland)*, vol. 20, Feb. 2020, doi: [10.3390/s20040978](https://doi.org/10.3390/s20040978).

\[Fer18\] J. Ferrer and E. Alba, “BIN-CT: Urban Waste Collection based in Predicting the Container Fill Level,” *Bio Systems*, Jul. 2018, doi: [10.1016/j.biosystems.2019.04.006](https://doi.org/10.1016/j.biosystems.2019.04.006).

\[Hen19\] K. Hendrickx *et al.*, “A general anomaly detection framework for fleet-based condition monitoring of machines,” *ArXiv*, vol. abs/1912.12941, Dec. 2019, doi: [10.1016/j.ymssp.2019.106585](https://doi.org/10.1016/j.ymssp.2019.106585).

\[Bro23\] Y. Brouwer, A. Barbosa‐Póvoa, A. Antunes, and T. R. P. Ramos, “Comparison of different waste bin monitoring approaches: An exploratory study,” *Waste Management & Research*, vol. 41, pp. 1570–1583, May 2023, doi: [10.1177/0734242X231160691](https://doi.org/10.1177/0734242X231160691).

\[Pol24\] A. Pollak, A. Gupta, and D. Göhlich, “Optimized Operation Management With Predicted Filling Levels of the Litter Bins for a Fleet of Autonomous Urban Service Robots,” *IEEE Access*, vol. 12, pp. 7689–7703, 2024, doi: [10.1109/ACCESS.2024.3352436](https://doi.org/10.1109/ACCESS.2024.3352436).

\[Har21\] A. Hartwell, F. J. Montana, W. R. Jacobs, V. Kadirkamanathan, A. Mills, and T. Clark, “Distributed digital twins for health monitoring: resource constrained aero-engine fleet management,” *The Aeronautical Journal*, vol. 128, pp. 1556–1575, Dec. 2021, doi: [10.1017/aer.2024.23](https://doi.org/10.1017/aer.2024.23).

\[Jou21\] N. Jourdan, S. Sen, E. J. Husom, E. Garcia-Ceja, T. Biegel, and J. Metternich, “On The Reliability Of Machine Learning Applications In Manufacturing Environments,” *ArXiv*, vol. abs/2112.06986, Dec. 2021.

\[Jia21\] Y. Jiang, S. Yin, J. Dong, and O. Kaynak, “A Review on Soft Sensors for Monitoring, Control, and Optimization of Industrial Processes,” *IEEE Sensors Journal*, vol. 21, pp. 12868–12881, Jun. 2021, doi: [10.1109/JSEN.2020.3033153](https://doi.org/10.1109/JSEN.2020.3033153).

\[Yan25\] X. Yan, J. Woelke, B. Bensmann, C. Eckert, R. Hanke‐Rauschenbach, and A. Niesse, “Cross-Method Overview of Fleet-Based Machine Health Estimation and Prediction: A Practical Guide for Industrial Applications,” *IEEE Access*, vol. 13, pp. 60131–60147, 2025, doi: [10.1109/ACCESS.2025.3556251](https://doi.org/10.1109/ACCESS.2025.3556251).
