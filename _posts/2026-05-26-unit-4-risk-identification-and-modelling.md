---
layout: post
title: "Unit 4 Seminar: Risk Identification and Modelling"
subtitle: "Reviewing threat modelling for industrial cyber-physical systems in smart manufacturing"
categories: ["Security and Risk Management"]
tags: [unit4, seminar, risk-identification, threat-modelling, industrial-cyber-physical-systems, smart-manufacturing, digital-twin, reflection]
---

## Overview

This post presents evidence of my preparation for the **Unit 4 Seminar: Risk Identification and Modelling**. The seminar activity required students to review Jbair et al. (2022), which discusses threat modelling for Industrial Cyber-Physical Systems (ICPS) in the context of smart manufacturing.

The activity focused on how comprehensive threat modelling can support the identification of cyber-physical assets, attack entry points, system vulnerabilities, risk scenarios and suitable countermeasures. This is important because cyber incidents in ICPS environments may affect not only confidentiality, integrity and availability, but also physical safety, production continuity and operational reliability.

---

## Seminar Activity Summary

| Area | Summary |
|---|---|
| Seminar title | Risk Identification and Modelling |
| Unit | Unit 4 |
| Main reading | Jbair et al. (2022) |
| Main topic | Threat modelling for Industrial Cyber-Physical Systems |
| Context | Smart manufacturing and cyber-physical environments |
| Main methodology | Six-step threat modelling process |
| Main concepts | Asset identification, vulnerability analysis, attack modelling, risk evaluation, countermeasure design and digital twin deployment |
| Key conclusion | Effective ICPS threat modelling should connect risk identification with practical countermeasure deployment |

---

## My Response to the Workshop Activity

My response focused on three seminar questions. First, I identified the key elements and interdependencies that should be captured in a comprehensive cyber-physical system threat model. Second, I explained how threat modelling can help identify attack entry points and system vulnerabilities. Third, I discussed how scenario-specific metrics and risk assessment methodologies can support vulnerability prioritisation and targeted security countermeasures.

| Workshop question | My response focus | Purpose |
|---|---|---|
| Key elements and interdependencies | Assets, ICPS levels, CIA and safety impact, adversary profiles, attack vectors and digital twin representation. | To show that cyber-physical risk analysis must include both technical and operational dependencies. |
| Attack entry points and vulnerabilities | DoS, MITM, replay attacks, ransomware and zero-day attacks, mapped using STRIDE, CAPEC, ICS Cyber Kill Chain and MITRE ICS ATT&CK. | To explain how structured threat modelling helps identify possible attack paths. |
| Scenario-specific metrics and risk assessment | Risk evaluation using attack vector and attack likelihood to produce risk level, severity and treatment priority. | To show how risk modelling supports prioritisation and targeted countermeasures. |

---

## Visual Summary

<img src="/assets/images/SRM/Unit4/Six-Step.png" alt="Six-step threat modelling methodology for industrial cyber-physical systems" width="600">

**Figure 1.** Six-step threat modelling methodology for Industrial Cyber-Physical Systems.

---

## Key Seminar Points

The first key point is that Industrial Cyber-Physical Systems are more complex than traditional information systems. They combine physical industrial processes with digital control, communication and monitoring technologies. As a result, a cyber incident may affect safety, production and operational reliability, not only data security.

The second key point is that ICPS threat modelling should capture assets and interdependencies across different levels. These include sensors, actuators, PLCs, HMIs, industrial IoT devices, Safety Instrumented Systems, enterprise systems and cloud-connected services. A weakness in one component may create cascading effects across other layers.

The third key point is that threat modelling can identify attack entry points and vulnerable system paths. Frameworks such as STRIDE, CAPEC, ICS Cyber Kill Chain and MITRE ICS ATT&CK can support structured analysis of threats such as denial of service, man-in-the-middle attacks, replay attacks, ransomware and zero-day attacks.

The fourth key point is that scenario-specific metrics help prioritise vulnerabilities. Risk evaluation should consider attack vector, likelihood, asset criticality, severity and treatment priority. This supports the selection of technical, operational and management countermeasures.

---

## Six-Step ICPS Threat Modelling Methodology

| Step | Methodology stage | Summary |
|---|---|---|
| Step 1 | ICPS asset identification and classification | Identify and classify assets such as PLCs, HMIs, industrial IoT devices and Safety Instrumented Systems according to criticality. |
| Step 2 | Vulnerability and threat analysis | Analyse vulnerabilities and threats using structured approaches such as STRIDE, CAPEC and adversary profiles. |
| Step 3 | Attack modelling | Model attack paths using ICS Cyber Kill Chain and MITRE ICS ATT&CK. |
| Step 4 | Risk evaluation and risk matrix | Evaluate risk using attack vector and attack likelihood to determine severity and treatment priority. |
| Step 5 | Countermeasure design | Select suitable technical, operational and management controls based on risk level. |
| Step 6 | Automatic deployment via digital twin | Use digital twin metadata to support countermeasure deployment and reduce the gap between analysis and implementation. |

---

## ICPS Threat Modelling Challenges

| Challenge | Why it matters | Possible response |
|---|---|---|
| OT and IT convergence | Increased connectivity expands the attack surface. | Model dependencies between operational technology, enterprise systems and cloud services. |
| Legacy industrial systems | Older systems may lack strong authentication, encryption or monitoring. | Apply compensating controls, segmentation and monitoring. |
| Physical safety impact | Cyber compromise may affect equipment behaviour or worker safety. | Include safety impact alongside confidentiality, integrity and availability. |
| Cascading interdependencies | A weakness in one layer may affect other ICPS components. | Use asset classification and digital twin modelling to represent dependencies. |
| Limited threat intelligence | Likelihood values may be uncertain or incomplete. | Use scenario-based analysis and update the model as evidence improves. |
| Deployment gap | Some threat models identify risks but do not support implementation. | Link risk assessment to countermeasure design and deployment planning. |

---

## Critical Reflection

Jbair et al. (2022) provide a useful and structured approach for analysing threats in Industrial Cyber-Physical Systems. A key strength of the methodology is that it does not stop at identifying risks. Instead, it connects asset identification, attack modelling, risk evaluation, countermeasure design and deployment through a digital twin.

However, the approach also has limitations. Modelling interdependencies across all ICPS levels may be resource-intensive, especially in complex industrial environments. The method also depends on accurate asset information, reliable system metadata and realistic likelihood assessment. If the input data is incomplete, the resulting risk evaluation may be less reliable.

Another limitation is that automated deployment of countermeasures may not always be straightforward in operational technology environments. Industrial systems often have safety, availability and real-time constraints, so any change must be carefully tested before deployment. Therefore, the methodology is valuable, but it should be supported by governance, validation and human oversight.

---

## Reflection

This seminar activity developed my understanding of risk identification and threat modelling in cyber-physical environments. Before completing the activity, I mainly associated threat modelling with identifying technical vulnerabilities in information systems. However, the reading helped me recognise that Industrial Cyber-Physical Systems require a wider form of analysis because cyber incidents can affect physical safety, production continuity, operational reliability and system interdependencies.

A key learning point was that risk identification in ICPS should not focus on individual assets in isolation. Components such as sensors, actuators, PLCs, HMIs, industrial IoT devices and cloud-connected services are interdependent. A weakness in one component may therefore create cascading effects across other parts of the system. This changed my understanding of threat modelling from a mainly technical process to a more integrated activity that must consider operational context, asset criticality and physical consequences.

The activity also showed that effective risk modelling should connect analysis with practical mitigation. The six-step methodology demonstrates that identifying assets, threats and vulnerabilities is only the starting point. A useful threat model should also support risk evaluation, prioritisation and the design of targeted countermeasures. The use of a digital twin was particularly important because it showed how threat modelling can be linked to the system design lifecycle and, where appropriate, to the deployment of countermeasures.

Overall, this activity strengthened my ability to think about risk in a more structured and practical way. In future work, I would approach cyber-physical risk assessment by considering not only individual vulnerabilities, but also system dependencies, safety impact, operational priorities and the feasibility of implementing countermeasures in live industrial environments.
---

## References

Jbair, M., Ahmad, B., Maple, C. and Harrison, R. (2022) 'Threat modelling for industrial cyber physical systems in the era of smart manufacturing', *Computers in Industry*, 137, p. 103611. Available at: https://doi.org/10.1016/j.compind.2022.103611.
