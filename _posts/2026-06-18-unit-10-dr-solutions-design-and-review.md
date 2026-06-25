---
layout: post
title: "Unit 10 Seminar: DR Solutions Design and Review"
subtitle: "Reviewing cloud vendor lock-in, modern cloud security concerns and disaster recovery design"
categories: ["Security and Risk Management"]
tags: [unit10, seminar, disaster-recovery, cloud-security, vendor-lock-in, rto, rpo, mission-thread-analysis, reflection]
---

## Overview

This post presents evidence of my preparation for the **Unit 10 Seminar: DR Solutions Design and Review**. The seminar activity required students to review papers on cloud vendor lock-in and modern cloud security concerns, then answer questions about the main vendor lock-in issues, possible mitigation strategies, cloud security concerns and appropriate responses.

The activity focused on the relationship between **cloud vendor lock-in**, **modern cloud security risks** and **disaster recovery design**. The main learning point was that cloud-based disaster recovery should not only focus on storing backups or replicating systems. It should also consider portability, vendor dependency, secure configuration, tested recovery procedures, Recovery Time Objective (RTO), Recovery Point Objective (RPO), and operational priorities.

---

## My Response to the Workshop Activity

My response focused on two main questions. First, I examined the cloud vendor lock-in issues identified by Kumar (2024) and considered how they could affect disaster recovery. Second, I reviewed modern cloud security concerns using the operational defence perspective presented by Corbari et al. (2024).

| Workshop question | My response focus | Purpose |
|---|---|---|
| What are the main vendor lock-in issues and how can they be mitigated? | I discussed technical, data, service, contractual, economic and network lock-in. | To show how dependency on one provider can reduce portability and affect disaster recovery. |
| What are the main security concerns with the modern cloud and how can they be mitigated? | I discussed misconfiguration, weak IAM, insecure APIs, monitoring gaps, third-party dependency and service availability risk. | To show how cloud security weaknesses can affect response, recovery and business continuity. |
| How does this relate to disaster recovery? | I linked vendor lock-in and cloud security to RTO, RPO and DR tier selection. | To show that DR design should include both recovery objectives and cloud risk controls. |

---

## Visual Summary

<img src="/assets/images/SRM/Unit10/dr_cloud_security_flowchart.png" alt="Flowchart summarising cloud vendor lock-in, cloud security risks and disaster recovery design" width="600">

**Figure 1.** Disaster recovery framing of cloud vendor lock-in and modern cloud security risks.

---

## Key Seminar Points

The first key point is that vendor lock-in can reduce organisational flexibility. Kumar (2024) identifies several forms of lock-in, including technical lock-in, data lock-in, service lock-in, contractual lock-in, economic lock-in and network lock-in. These issues may make migration complex, costly and time-consuming.

The second key point is that vendor lock-in is directly relevant to disaster recovery. If systems, data or backups cannot be moved or restored outside one provider’s ecosystem, the organisation may struggle to meet its RTO and RPO. Therefore, vendor lock-in should be treated as a strategic disaster recovery risk, not only as a procurement or technical issue.

The third key point is that modern cloud security concerns can affect recovery outcomes. Misconfiguration, weak Identity and Access Management, insecure APIs, insufficient logging, monitoring gaps and third-party dependency may delay detection, response and restoration.

The fourth key point is that cloud disaster recovery requires both technical and organisational planning. Technical controls such as MFA, least-privilege access, secure API management, logging, monitoring and tested backups are important. However, disaster recovery also requires governance, mission-based prioritisation and clear understanding between operational teams and security teams.

---

## Vendor Lock-in Issues and Mitigation

| Vendor lock-in issue | Risk to disaster recovery | Mitigation |
|---|---|---|
| Technical lock-in | Dependency on proprietary APIs and technologies may make migration difficult. | Use open standards, API gateways and decoupled architecture. |
| Data lock-in | Proprietary formats may limit data portability. | Use data mobility planning, export testing and portable storage formats. |
| Service lock-in | Deep integration with vendor-specific services may reduce flexibility. | Use containerisation and modular design where appropriate. |
| Contractual and economic lock-in | Exit penalties and investment in one provider may increase switching cost. | Include exit planning and cost review in vendor selection. |
| Network lock-in | Dependency on one provider’s network infrastructure may affect recovery options. | Plan alternative connectivity and test recovery paths. |

---

## Modern Cloud Security Concerns and Mitigation

| Cloud security concern | DR impact | Mitigation |
|---|---|---|
| Misconfiguration | Exposed services or storage may cause data loss or breach risk. | Use cloud security posture management and configuration review. |
| Weak IAM | Excessive privileges may allow unauthorised access or lateral movement. | Apply least privilege, MFA and role-based access control. |
| Insecure APIs | Integration points may create vulnerabilities. | Use secure API management and regular testing. |
| Monitoring gaps | Delayed detection may increase incident impact. | Use centralised logging and continuous monitoring. |
| Third-party dependency | External service failure may affect recovery. | Assess suppliers and test recovery dependencies. |
| Service availability risk | Downtime may prevent timely restoration. | Align cold, warm or hot standby with RTO and RPO needs. |

---

## Comparison Between the Readings

| Comparison area | Kumar (2024) | Corbari et al. (2024) |
|---|---|---|
| Main focus | Cloud vendor lock-in and dependency on one provider. | Mission Thread Analysis and operational alignment. |
| Core problem | Proprietary APIs, data formats, contracts, costs and technical dependencies reduce flexibility. | Cybersecurity teams and operational teams may define risks differently. |
| Type of risk | Strategic, technical, economic, contractual and compliance risk. | Operational, governance, communication and mission-prioritisation risk. |
| Relevance to cloud DR | Lock-in can make recovery difficult if systems or backups cannot be moved. | Mission Thread Analysis helps identify critical systems, data flows and dependencies. |
| Proposed mitigation | Exit planning, multi-cloud, containerisation, Infrastructure as Code and open standards. | Mission Thread Analysis to create shared understanding between mission owners and cyber defenders. |
| Limitation | Portability strategies may increase cost and complexity. | MTA requires collaboration, documentation and organisational maturity. |

The comparison shows that the two readings address different but complementary dimensions of cloud disaster recovery. Kumar (2024) focuses on strategic and technical dependency, while Corbari et al. (2024) focus on operational alignment and mission-based prioritisation.

---

## Key Learning Points

This activity showed that cloud disaster recovery should not be designed only around backup availability. It should also consider vendor dependency, data portability, cloud security posture, mission-critical systems, RTO and RPO.

Vendor lock-in can prevent an organisation from restoring systems quickly or moving workloads during disruption. At the same time, cloud security weaknesses such as misconfiguration, weak IAM or monitoring gaps can delay detection and recovery. Therefore, effective DR design requires both technical controls and governance controls.

A robust cloud disaster recovery approach should combine exit planning, portable architecture, tested recovery procedures, secure cloud configuration and mission-based prioritisation.

---

## Reflection

This seminar activity improved my understanding of cloud disaster recovery as a wider security and risk management issue. Before completing the activity, I mainly associated disaster recovery with backups and system restoration. However, reviewing the readings helped me understand that cloud DR also depends on vendor portability, secure configuration, cost planning, RTO, RPO and operational priorities.

The activity also showed that cloud risk is not only technical. Vendor lock-in can create legal, contractual, economic and operational constraints. Similarly, modern cloud security concerns require coordination between mission owners, cyber defenders and technical teams. This helped me understand why disaster recovery planning should include both technical architecture and organisational decision-making.

Overall, this activity strengthened my ability to connect cloud security concerns with practical recovery planning. In future work, I would assess cloud DR solutions by considering not only whether systems can be backed up, but also whether they can be restored securely, quickly and independently enough to meet business requirements.

---

## References

Alhazmi, O. and Malaiya, Y. (2013) ‘Evaluating Disaster Recovery Plans using the Cloud’, *2013 Proceedings Annual Reliability and Maintainability Symposium*, 1(1), pp. 1–6.

Corbari, G.I., Khatod, N., Popiak, J.F. and Sinclair, P. (2024) ‘Mission Thread Analysis: Establishing a Common Framework in a Multi-discipline Domain to Enhance Defensive Cyberspace Operations’, *The Cyber Defense Review*, 9(1), pp. 37–54.

Kumar, A. (2024) *Cloud Vendor Lock-In: Identify, Strategies and Mitigate*. Module reading.
