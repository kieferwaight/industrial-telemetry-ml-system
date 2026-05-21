# Updates & Verfications for Executive Summary

I have manually pulled content from the PDF case study for 01 Executive Summary.  I need to make sure our (git-repositories/industrial-telemetry-ml-system/case-study/01_Executive_Summary.md) matches or is updated based on the todo items in this document.

- [ ] Remove the dash in the header of all documents not just Executive Summary

```before
# 01 — Executive Summary
```

```after
# 01 Executive Summary
```


- [ ] Ensure the content of git-repositories/industrial-telemetry-ml-system/case-study/01_Executive_Summary.md (executive summary) matches and represents the below text, images, bullets, and tables listed further down this page

- [ ] Link all sources (Mel20, Rut20, ...) to the correct sources. The sources can be found in this file git-repositories/industrial-telemetry-ml-system/case-study/Undermind_Edit_Appendix_C.md under section ## Resources

- [ ] In the sources table in section 1.3 also link the title column (| Rut20 | {LINK THIS: An Automated Machine Learning Approach for Smart Waste Management Systems} |) Sources can be found in appendix c

- [ ] Rename all images that I have linked to match alt text format. I have imported all the images from the PDF manually. They are being dropped into the todo folder as "image-*.png".  I went ahead and renamed 2 images for example. (git-repositories/industrial-telemetry-ml-system/todo/figure_1.1_deployed_compactors_had_a_lack_of_real-time_visibility.png), and (git-repositories/industrial-telemetry-ml-system/todo/figure_1.2_ransportation_costs_are_incurred_per_pickup.png). For the other images, this needs to be repeated.  Simply use the alt label where I have linked the images. Make sure to follow the naming convention.

- [ ] Once images have been properly named, move them to assets and ensure they are properly linked.


```markdown
# Executive Summary

> The Compactor Became the Sensor

## 1.1 The Business Problem

Commercial waste operations had a persistent visibility problem: Dispatch decisions were often made without a reliable real-time view of actual compactor utilization.

![Figure 1.1 Deployed compactors had a lack of real-time-visibility](figure_1.1_deployed_compactors_had_a_lack_of_real-time_visibility.png)

In practice, hauling schedules usually depended on a limited set of unreliable operating methods:

| Method                 | Failure Mode                      |
| ---------------------- | --------------------------------- |
| Fixed schedules        | Ignores real utilization patterns |
| Manual inspection      | Non-scalable and inconsistent     |
| Overflow response      | Reactive, service-disruptive      |
| Vendor heuristics      | Subjective and non-repeatable     |
| Conservative servicing | Systematically over-dispatches    |

This created operational inefficiency in both directions.

Trucks were either dispatched before compactors were meaningfully full, or service was delayed until overflow, contamination, emergency pickups, and customer disruption forced action.

![Figure 1.2 Transportation costs are incurred per pickup](figure_1.2_ransportation_costs_are_incurred_per_pickup.png)

This was not a narrow routing problem. It was a recurring operational decision failure that affected cost, service quality, and fleet efficiency across distributed commercial environments.

## 1.2 Technical Strategy

This project approached the problem differently. Instead of installing invasive internal fill-level sensors inside industrial compactors, the system treated the compactor itself as the sensing mechanism.

> The compactor Became The Sensor 

By analyzing the electrical behavior generated during compaction cycles, including:

- startup load
- current draw
- crush-cycle duration
- compression resistance
- repeated-cycle behavior
- waveform drift

The platform inferred compactor fullness using machine learning and industrial telemetry.

![Figure 1.3a non-invasive electromagnetic sensor clamped around the primary cable](image.png)

This was the central conceptual move of the entire platform.
It reframed the task from direct measurement to state inference: not adding more hardware inside the waste stream, but extracting hidden operational meaning from signals already produced by the equipment.


![Figure 1.3b non-invasive electromagnetic sensor clamped around the primary cable](image-1.png)

## 1.3 Research Context and Technical Legitimacy

Placed against recent literature, the closest frame for this work is industrial soft sensing rather than ordinary smart waste sensing.

![Figure 1.4 Common approaches in waste monitoring literature](image-2.png)


Recent waste-monitoring papers usually begin with direct fill measurement through ultrasonic sensors, event sensors, or manual observation. [Mel20, Rut20, Bro23, Fer18, Pol24] The closer technical analogues are virtual sensor and soft sensor papers that recover hidden physical state from current, torque, speed, or power traces without adding dedicated measurement hardware. [Jia21, Sob23b, Hei21]

That makes this case unusual in a useful way. It applied a soft-sensor pattern to commercial waste operations, then connected the result directly to dispatch decisions across a distributed fleet. In that sense, the project sits between industrial inference research and real-world fleet operations rather than within a narrow smart-bin prototype category. [Hen19, Har21, Jou21, Yan25]

| Source | Title                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Rut20  | An Automated Machine Learning Approach for Smart Waste Management Systems                                                      |
| Bro23  | Comparison of different waste bin monitoring approaches: An exploratory study                                                  |
| Fer18  | BIN-CT: Urban Waste Collection based in Predicting the Container Fill Level                                                    |
| Pol24  | Optimized Operation Management With Predicted Filling Levels of the Litter Bins for a Fleet of Autonomous Urban Service Robots |
| Jia21  | A Review on Soft Sensors for Monitoring, Control, and Optimization of Industrial Processes                                     |
| Sob23b | A Data-Driven Soft Sensor for Mass Flow Estimation                                                                             |
| Hei21  | Indirect Mass Flow Estimation based on Power Measurements of Conveyor Belts in Mineral Processing Applications                 |
| Hen19  | A general anomaly detection framework for fleet-based condition monitoring of machines                                         |
| Har21  | Distributed digital twins for health monitoring: resource constrained aero-engine fleet management                             |
| Jou21  | On The Reliability Of Machine Learning Applications In Manufacturing Environments                                              |
| Yan25  | Cross-Method Overview of Fleet-Based Machine Health Estimation and Prediction: A Practical Guide for Industrial Applications   |

## 1.4 Strategic Significance

The broader significance of the project extended beyond waste operations. The platform demonstrated a larger industrial AI principle:

>  Operational intelligence can often be  extracted
>  from infrastructure that already exists.

Rather than deploying increasingly complex sensor hardware, the system used telemetry, software, and machine learning to interpret hidden signals already embedded within industrial systems.

The commercial outcome validated that approach. The machine-learning codebase and compactor-monitoring logic later became part of a broader waste-technology ecosystem associated with [Quest Resource Holding Corporation](https://investors.qrhc.com/overview/default.aspx), whose public materials emphasize data-driven waste programs, AI-assisted operations, IoT-enabled infrastructure, equipment intelligence, and centralized operational reporting.

Public-facing product evolution aligned closely with the original operational thesis:

- predictive hauling
- real-time fullness intelligence
- cellular telemetry
- automated scheduling
- machine-learning-assisted waste operations

This case demonstrates applied machine learning in a physical industrial system before “industrial AI” became a mainstream framing.

Its enduring value came from four linked sources:

| Source of Value                | Why It Mattered                                                         |
| ------------------------------ | ----------------------------------------------------------------------- |
| Existing infrastructure        | Avoided invasive retrofits by leveraging equipment already in the field |
| Real-world signal modeling     | Extracted useful state from noisy industrial behavior                   |
| Workflow integration           | Made predictions operationally meaningful rather than merely analytical |
| Operational telemetry at scale | Turned distributed equipment data into automated decision support       |

```