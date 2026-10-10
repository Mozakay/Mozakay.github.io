---
layout: post
title: "Unit 12: Cloud Operations and Management – Reflective e-Portfolio"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

## 1. Introduction

This e-Portfolio traces a change in how I evaluate cloud computing. Infrastructure as a Service (IaaS) gives customers the greatest infrastructure control; Platform as a Service (PaaS) transfers runtime management to the provider; Software as a Service (SaaS) delivers an application (Nadeem, 2022). Public, private and hybrid deployment models frame decisions about hosting and control (Mell and Grance, 2011).

Five technical themes connect Azure, Docker, OpenVAS, Restic, MySQL, OpenFaaS, TensorFlow and Horizon Retail activities, alongside ethical, social and professional reflection. They address fundamental concepts (LO1), different cloud solutions (LO2), configuration and implementation (LO3), and critical selection of methods for resilience (LO4). The evidence list links artefacts to these outcomes.

## 2. Weekly Reflections

### 2.1 From Cloud Service Selection to Cloud Strategy

In Unit 1, comparing AWS and Google Cloud showed that suitability depends on control, workload behaviour and total cost (Alkhatib, Shaheen and Albustanji, 2025). Units 2–3 moved my analysis towards architecture. The ROCCA and TOGAF study supported phased hybrid adoption, but tutor feedback clarified that planning value did not establish long-term outcomes (Figure 1a; Anggraini, Binariswanto and Legowo, 2019). Terraform's declarative, state-aware design initially appeared mainly a technical strength (Özdoğan, Ceran and Üstündağ, 2023); peer feedback highlighted remote storage, locking and access control as governance responsibilities (Figure 1b). The group ARM report extended this reasoning to Azure Arc (Microsoft, 2025; 2026b). Consequently, my Horizon strategy accepts hybrid connectivity and identity complexity rather than assuming cloud migration is universally beneficial (Ali et al., 2025).

<figure>
  <img src="/assets/images/COM/unit23/unit-2-post-to-me.png" alt="Peer feedback on the Unit 2 ROCCA and TOGAF discussion" width="600">
  <figcaption><em>Figure 1a. Tutor feedback on the ROCCA and TOGAF discussion (Unit 2).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit23/unit3post1.png" alt="Peer feedback on Terraform state management" width="600">
  <figcaption><em>Figure 1b. Peer feedback on Terraform state management (Unit 3).</em></figcaption>
</figure>

### 2.2 From Provisioning to Controlled and Verifiable Cloud Operations

Initially, successful provisioning appeared to be the achievement. Unit 5 created and verified a Qatar Central VNet (10.0.0.0/16) and subnet (10.0.1.0/24) using Azure CLI (Figure 2). A Succeeded state confirmed deployment, not secure design (Hashizume et al., 2013). Horizon extended this lesson: Terraform provisioned infrastructure, Ansible configured Nginx (ok=5, changed=3, failed=0), and Azure Monitor recorded approximately 2.93% average CPU utilisation (Figure 3). Subscription constraints required subnet reuse; automation did not remove provider limits. The CPU result demonstrated telemetry, not enterprise capacity (Microsoft, 2023). My operational sequence became create, automate, verify, configure, observe and interpret, with version control and review needed to prevent repeated configuration errors (Kumara et al., 2021).

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit5/figure2-vnet-verification.png" alt="Verification of the Azure Virtual Network and subnet configuration using Azure CLI" width="600">
  <figcaption><em>Figure 2. Azure CLI verification of the virtual network and subnet (Unit 5).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit11/part2/02-terraform-iac.png" alt="Terraform Infrastructure as Code" width="550">
  <figcaption><em>Figure 3a. Terraform definition and managed Azure resources (Unit 11, Part 2).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Ansible configuration" width="550">
  <figcaption><em>Figure 3b. Automated configuration of the Horizon Retail VM using Ansible (Unit 11, Part 2).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Azure Monitor CPU utilisation" width="650">
  <figcaption><em>Figure 3c. Azure Monitor CPU utilisation for the Horizon Retail virtual machine (Unit 11, Part 2).</em></figcaption>
</figure>

### 2.3 From Security Assessment to Risk-Based Cloud Governance

Docker initially appeared primarily a portability mechanism; the audit exposed runtime and network responsibilities (Martin et al., 2018). When OpenVAS failed to identify the host, I changed the Alive Test setting and repeated the scan, obtaining two low-severity findings (score 2.6). Manual review identified MongoDB listening on 0.0.0.0:27017 with an unrestricted NSG rule, no authenticated identity in the connection status, HTTP without TLS and pending updates (Figure 4). These indicated exposure and authentication-assurance concerns, not proven compromise. Scanner scope limits a “no findings” result (Kritikos et al., 2019). The healthcare NIST assessment and Horizon analysis then shifted my decisions towards likelihood, impact, treatment and residual risk (NIST, 2012). I learned to combine scanning with configuration review and continuous governance (Torkura et al., 2021).

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure 8 OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6..png' | relative_url }}" alt="Figure 8. OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6." width="700">
  <figcaption><em>Figure 4a. OpenVAS scan completed with a low-severity score of 2.6 (Unit 7).</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure%2012%20MongoDB%20configuration%20and%20connection%20status%20showing%20successful%20access%20with%20no%20authenticated%20users%20or%20roles..png' | relative_url }}" alt="Figure 12. MongoDB configuration and connection status showing successful access with no authenticated users or roles." width="700">
  <figcaption><em>Figure 4b. MongoDB connection status showing no authenticated users or roles (Unit 7).</em></figcaption>
</figure>

### 2.4 From Backup to Disaster Recovery and Business Continuity

I initially associated resilience with possessing backups. Unit 8 used encrypted Restic snapshots in Azure Blob Storage to protect PostgreSQL and application files. After simulated deletion, restoration recovered 252,700 orders and the application files; the integrity check reported no errors (Figure 5). Recovery took 3 minutes 49 seconds against a 30-minute target, but 180 orders and six files created after the snapshot were lost. The 69-second snapshot-to-incident interval was an observed recovery-point gap, not target RPO. The proposed 60-minute production RPO requires automated, monitored hourly backups; the exercise used manual snapshots. Timing also excluded realistic incident detection. I therefore distinguish backups, disaster recovery and business continuity through defined objectives and tested recovery, rather than treating restoration success as complete resilience (Swanson et al., 2010; Mendonça, Lima and Andrade, 2020).

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic5.png' | relative_url }}" alt="Recovery from latest Restic snapshot" width="500">
  <figcaption><em>Figure 5a. Recovery from the latest Restic snapshot (Unit 8).</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="Database restored to 252,700 records" width="500">
  <figcaption><em>Figure 5b. Orders table restored to 252,700 records (Unit 8).</em></figcaption>
</figure>

### 2.5 From Migration Strategy to Production Readiness

Migration initially appeared to be data copying. Unit 9 moved MySQL 8.0.46 to Azure MySQL Flexible Server using mysqldump with `--single-transaction` and TLS. After bulk restoration, new transactions created a gap; maintenance, delta synchronisation and record-level checks established cutover readiness (Figure 6). The insert-only delta excluded updates and deletions, requiring replication or equivalent change capture for production (Oracle, 2026). Migration became a controlled service transition in my understanding (Jamshidi, Ahmad and Pahl, 2013).

Unit 10 deployed and invoked a Python function through OpenFaaS on Kubernetes (Figure 7). Serverless abstracted execution infrastructure, but self-hosted platform operation remained; cold starts were unmeasured (Baldini et al., 2017; Shafiei, Khonsari and Mousavi, 2022).

Unit 11's CIFAR-10 model achieved training 80.47%, validation 76.78% and test 75.89% accuracy. Deployment through ACR to Container Apps required rebuilding the rejected image with Docker Buildx and OCI-compatible media types (Figure 8). Working /health and /predict endpoints and sample confidence of 79.62% demonstrated functional inference, not measured latency, concurrency, security or class-level reliability. These exercises shifted my focus from deployment completion to operational readiness.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Final validation of the Azure MySQL database after final synchronisation" width="700">
  <figcaption><em>Figure 6. Final validation of the Azure MySQL database after synchronisation (Unit 9).</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="Successful invocation of the greeting function" width="700">
  <figcaption><em>Figure 7. Successful invocation of the OpenFaaS function (Unit 10).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png" alt="Successful image prediction using the deployed CIFAR-10 model on Azure Container Apps" width="700">
  <figcaption><em>Figure 8. Prediction from the model deployed on Azure Container Apps (Unit 11, Part 1).</em></figcaption>
</figure>

### 2.6 Ethical, Social and Professional Reflection

My Reflective Report connected technical learning to responsibility. **Ethically**, configuration review showed why access checks should precede release. Terraform security-policy research and cloud privacy risks reinforce this responsibility (Verdet et al., 2025; Khalil, Khreishah and Azeem, 2014). Al-Qahtani and Abu-Shanab (2021) link security, privacy and trust to cloud-user satisfaction in Qatar; satisfaction nevertheless cannot verify technical security.

**Socially**, restoration left some transactions lost (Figure 5), highlighting consequences beyond service availability. Outages and data lock-in constrain cloud adoption (Armbrust et al., 2010); limited connectivity or digital skills can also exclude users. A small VM and resource destruction encouraged proportionate provisioning, but did not establish environmental sustainability.

**Professionally**, I would combine user feedback, access verification, recovery testing and application monitoring. Hybrid control adds complexity, while managed services reduce maintenance without removing accountability (Mell and Grance, 2011). My decisions should balance sensitivity, continuity, cost and organisational capability.

## 3. Skills Development

**Table 1. Skills development by capability group**

| Capability | Application and evidence | Learning and professional significance |
|---|---|---|
| Infrastructure automation | CLI verification; Terraform VM; Ansible Nginx (Figures 2–3). | Separate provisioning from configuration; review reproducible changes. |
| Networking | CIDR design, NSG rules, SSH tunnel; MySQL in UAE North. | Subscription policy constrained region selection; location and exposure require governance. |
| Security and risk | OpenVAS, Docker inspection and ISO/IEC 27001:2022 mapping; NIST healthcare assessment (Figure 4). | Combine scanner findings with manual checks and risk prioritisation. |
| Recovery and migration | Restic restoration; consistent MySQL export, synchronisation and validation (Figures 5–6). | Measure recovery and data loss; recognise incomplete change capture. |
| Cloud-native and AI operations | Kubernetes/OpenFaaS function; TensorFlow/Keras, ACR and Container Apps (Figures 7–8). | Resolve image compatibility; distinguish functional success from performance assurance. |

### 3.1 Individual Contribution to Unit 6 Group Report A

My self-evaluation records that I initiated the group, helped coordinate meetings and task allocation, completed my work on time and consolidated contributions. I reviewed section consistency and identified infrastructure-design changes needed to align the report with our scenario. Group Report A documents the shared ARM analysis; the Team Contract records participation, while Peer Evaluation Group1 Moza records my reported contribution. I learned that task allocation alone does not ensure cohesion: shared assumptions and cross-review matter. In future cloud projects, I will introduce earlier section-review checkpoints before final integration.

## 4. Application to Industry: Horizon Retail Group

Horizon Retail Group, a hypothetical retailer with approximately 150 stores and growing e-commerce, integrates the module's learning around demand peaks, secure integration, trading continuity and data-informed decisions.

Selected point-of-sale and inventory functions remain local to reduce WAN dependence; Azure would host central applications, automation, monitoring and analytics (Figure 9). This proposed hybrid design accepts additional identity and connectivity complexity (Ali et al., 2025). Following Unit 9, I would progress through PoC, limited pilot and staged rollout with synchronisation and cutover validation; continuous transactions require more complete change capture than my insert-only delta. One Standard_B1s VM validates a mechanism, not enterprise readiness (Microsoft, 2023).

Proposed HTTPS/TLS, WAF, Entra ID, RBAC, private endpoints, Key Vault and logging address the testing environment's exposure. Azure Backup and Site Recovery remain proposals requiring workload-specific recovery objectives and tests (Microsoft, 2026a; 2026c). AI forecasting should follow data quality, ownership and human oversight (Fildes, Ma and Kolassa, 2022). Autoscaling and right-sizing require measured demand and cost evaluation (Gill and Chana, 2016). Pilot acceptance should assess availability, latency, incident rates, recovery, cost and supportability.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail hybrid cloud architecture" width="750">
  <figcaption><em>Figure 9. Horizon Retail hybrid architecture showing the validated proof of concept and proposed production design (Unit 11, Part 2).</em></figcaption>
</figure>

## 5. Future Learning Goals

These goals address practical limitations and Weeks 10–12 trends; their criteria are proposed learning targets.

**Goal 1: infrastructure as code and DevOps.** Within three months, I will deliver modular Terraform with remote state, locking and a policy-checking pipeline (Kumara et al., 2021). Success means reproducible deployment, rejection of a deliberately unsafe configuration and a documented recovery procedure.

**Goal 2: observability and reliability.** Within two months, I will produce an OpenFaaS/Container Apps load-test report and monitoring dashboard covering latency, cold starts and errors (Microsoft, 2023). Success means documented SLIs/SLOs and tested alerts for a service breach and missed backup.

**Goal 3: AI-assisted operations.** Within four months, I will compare predictive scaling or anomaly detection with a reactive baseline (Lorido-Botran, Miguel-Alonso and Lozano, 2014). The deliverable is a reproducible experiment measuring cost, response time and false alerts. Success means explaining whether AI improves the baseline, including drift and human oversight; a negative result remains informative.

**Goal 4: edge and emerging technologies.** Within six months, I will prototype one store workload (Shi et al., 2016). Success means demonstrated offline operation, reconnection synchronisation and measured patching/monitoring overhead. I will also produce a feasibility note comparing blockchain traceability with a conventional database and quantum optimisation with classical approaches (Golec et al., 2024). Success means an evidence-based adoption or deferral decision, not presumed technological advantage.

The module has connected strategy, automation, security, recovery and emerging technologies into an operational lifecycle judged by evidence.

## 6. References

Al-Qahtani, F. and Abu-Shanab, E.A. (2021) 'End user satisfaction with cloud computing: The case of Hamad Medical Corporation in Qatar', *International Journal of Healthcare Information Systems and Informatics*, 16(4), pp. 1–23. doi: 10.4018/IJHISI.295821.

Ali, S., Talpur, D.B., Abro, A., Alshudukhi, K.S., Alwakid, G.N., Humayun, M., Bashir, F., Wadho, S.A. and Shah, A. (2025) 'Security and privacy in multi-cloud and hybrid cloud environments: Challenges, strategies, and future directions', *Computers & Security*, 157, Article 104599. doi: 10.1016/j.cose.2025.104599.

Alkhatib, A., Shaheen, A. and Albustanji, R.N. (2025) 'A comparative analysis of cloud computing services: AWS, Azure, and GCP', *International Journal of Computing and Digital Systems*, 18(1), pp. 1–15. doi: 10.12785/ijcds/1571111846.

Anggraini, N., Binariswanto and Legowo, N. (2019) 'Cloud computing adoption strategic planning using ROCCA and TOGAF 9.2: A study in government agency', *Procedia Computer Science*, 161, pp. 1316–1324.

Armbrust, M. et al. (2010) 'A view of cloud computing', *Communications of the ACM*, 53(4), pp. 50–58. doi: 10.1145/1721654.1721672.

Baldini, I., Castro, P., Chang, K., Cheng, P., Fink, S., Ishakian, V., Mitchell, N., Muthusamy, V., Rabbah, R., Slominski, A. and Suter, P. (2017) 'Serverless computing: Current trends and open problems', in *Research Advances in Cloud Computing*. Singapore: Springer, pp. 1–20. doi: 10.1007/978-981-10-5026-8_1.

Fildes, R., Ma, S. and Kolassa, S. (2022) 'Retail forecasting: Research and practice', *International Journal of Forecasting*, 38(4), pp. 1283–1318. doi: 10.1016/j.ijforecast.2019.06.004.

Gill, S.S. and Chana, I. (2016) 'Cloud resource provisioning: Survey, status and future research directions', *Knowledge and Information Systems*, 49(3), pp. 1005–1069. doi: 10.1007/s10115-016-0922-3.

Golec, M., Hatay, E.S., Golec, M., Uyar, M., Golec, M. and Gill, S.S. (2024) 'Quantum cloud computing: Trends and challenges', *Journal of Economy and Technology*, 2, pp. 190–199. doi: 10.1016/j.ject.2024.05.001.

Hashizume, K., Rosado, D.G., Fernández-Medina, E. and Fernandez, E.B. (2013) 'An analysis of security issues for cloud computing', *Journal of Internet Services and Applications*, 4, Article 5. doi: 10.1186/1869-0238-4-5.

Jamshidi, P., Ahmad, A. and Pahl, C. (2013) 'Cloud migration research: A systematic review', *IEEE Transactions on Cloud Computing*, 1(2), pp. 142–157. doi: 10.1109/TCC.2013.10.

Khalil, I.M., Khreishah, A. and Azeem, M. (2014) 'Cloud computing security: A survey', *Computers*, 3(1), pp. 1–35. doi: 10.3390/computers3010001.

Kritikos, K., Magoutis, K., Papoutsakis, M. and Ioannidis, S. (2019) 'A survey on vulnerability assessment tools and databases for cloud-based web applications', *Array*, 3–4, Article 100011.

Kumara, I., Garriga, M., Romeu, A.U., Di Nucci, D., Palomba, F., Tamburri, D.A. and van den Heuvel, W.-J. (2021) 'The do's and don'ts of infrastructure code: A systematic gray literature review', *Information and Software Technology*, 137, Article 106593. doi: 10.1016/j.infsof.2021.106593.

Lorido-Botran, T., Miguel-Alonso, J. and Lozano, J.A. (2014) 'A review of auto-scaling techniques for elastic applications in cloud environments', *Journal of Grid Computing*, 12(4), pp. 559–592. doi: 10.1007/s10723-014-9314-7.

Martin, A., Raponi, S., Combe, T. and Di Pietro, R. (2018) 'Docker ecosystem – Vulnerability analysis', *Computer Communications*, 122, pp. 30–43.

Mell, P. and Grance, T. (2011) *The NIST definition of cloud computing*. NIST Special Publication 800-145. Gaithersburg, MD: National Institute of Standards and Technology. doi: 10.6028/NIST.SP.800-145.

Mendonça, J., Lima, R. and Andrade, E. (2020) 'Evaluating and modelling solutions for disaster recovery', *International Journal of Grid and Utility Computing*, 11(5), pp. 683–704. doi: 10.1504/IJGUC.2020.110055.

Microsoft (2023) 'Deployment and testing for mission-critical workloads on Azure', *Microsoft Learn*, last updated 1 February 2023. Available at: https://learn.microsoft.com/en-us/azure/well-architected/mission-critical/mission-critical-deployment-testing (Accessed: 2 October 2026).

Microsoft (2025) 'Azure Arc overview', *Microsoft Learn*. Available at: https://learn.microsoft.com/en-us/azure/azure-arc/overview (Accessed: 15 August 2026).

Microsoft (2026a) 'About Site Recovery', *Microsoft Learn*, last updated 23 September 2026. Available at: https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview (Accessed: 2 October 2026).

Microsoft (2026b) 'What is Azure Resource Manager?', *Microsoft Learn*, 4 August. Available at: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview (Accessed: 24 August 2026).

Microsoft (2026c) 'What is the Azure Backup service?', *Microsoft Learn*, last updated 16 September 2026. Available at: https://learn.microsoft.com/en-us/azure/backup/backup-overview (Accessed: 2 October 2026).

Nadeem, F. (2022) 'Evaluating and ranking cloud IaaS, PaaS and SaaS models based on functional and non-functional key performance indicators', *IEEE Access*, 10, pp. 63245–63257. doi: 10.1109/ACCESS.2022.3182688.

National Institute of Standards and Technology (NIST) (2012) *Guide for conducting risk assessments*. NIST Special Publication 800-30 Rev. 1. Gaithersburg, MD: NIST. doi: 10.6028/NIST.SP.800-30r1.

Oracle (2026) *MySQL 8.0 reference manual: mysqldump — A database backup program*. Available at: https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html (Accessed: 21 September 2026).

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) 'Serverless computing: A survey of opportunities, challenges, and applications', *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. doi: 10.1145/3510611.

Shi, W., Cao, J., Zhang, Q., Li, Y. and Xu, L. (2016) 'Edge computing: Vision and challenges', *IEEE Internet of Things Journal*, 3(5), pp. 637–646. doi: 10.1109/JIOT.2016.2579198.

Swanson, M., Bowen, P., Phillips, A.W., Gallup, D. and Lynes, D. (2010) *Contingency planning guide for federal information systems*. NIST Special Publication 800-34 Rev. 1. Gaithersburg, MD: National Institute of Standards and Technology.

Torkura, K.A., Sukmana, M.I.H., Cheng, F. and Meinel, C. (2021) 'Continuous auditing and threat detection in multi-cloud infrastructure', *Computers & Security*, 102, Article 102124.

Verdet, A. et al. (2025) 'Assessing the adoption of security policies by developers in terraform across different cloud providers', *Empirical Software Engineering*, 30, Article 74. doi: 10.1007/s10664-024-10610-0.

Özdoğan, E., Ceran, O. and Üstündağ, M.T. (2023) 'Systematic analysis of Infrastructure as Code technologies', *Gazi University Journal of Science Part A: Engineering and Innovation*, 10(4), pp. 452–471. doi: 10.54287/gujsa.1373305.

## Attachment List: Evidence and Learning Outcomes

Original posts retain the fuller technical evidence. Group documents are supplied separately.

| Artefact | Learning demonstrated | Outcomes |
|---|---|---|
| [Unit 1 comparison][u1] | Service responsibilities and workload selection. | LO1–2 |
| [Units 2–3; Figure 1][u23] | Architecture, adoption and feedback-informed IaC selection. | LO2, LO4 |
| [Unit 5; Figure 2][u5] | Verified CLI networking. | LO1, LO3 |
| Unit 6: Group Report A, Team Contract, Peer Evaluation | ARM analysis and individual responsibility (§3.1). | LO1–2 |
| [Unit 7; Figure 4][u7] | Scanning and configuration-risk interpretation. | LO3–4 |
| [Unit 8; Figure 5][u8] | Tested restoration and recovery limitations. | LO3–4 |
| [Unit 9; Figure 6][u9] | Migration, synchronisation and validation. | LO3–4 |
| [Unit 10; Figure 7][u10] | Kubernetes-supported function deployment. | LO2–3 |
| [Unit 11 AI; Figure 8][ai] | Model evaluation and containerised inference. | LO3–4 |
| [Horizon PoC; Figures 3, 9][poc] | Automation, telemetry and proposed hybrid resilience. | LO2–4 |
| Reflective Report; §2.6 | Ethical, social and professional judgement. | LO1–2, LO4 |
| Table 1 | Practical capability development. | LO3–4 |

[u1]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/08/06/unit-1-comparing-the-service-models-of-aws-and-google-cloud.html
[u23]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/08/17/units-2-3-cloud-architecture-frameworks-and-design.html
[u5]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/08/31/unit-5-azure-cli-cloud-network-configuration.html
[u7]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/09/08/unit-7-security-audit-of-a-docker-based-cloud-application.html
[u8]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/09/14/unit-8-disaster-recovery-and-business-continuity.html
[u9]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/09/18/unit-9-cloud-database-migration-for-a-retail-order-management-system.html
[u10]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/09/21/unit-10-implementing-a-serverless-function-using-openfaas.html
[ai]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/09/25/unit-11-part-1-formative-activity-tensorflow-and-keras.html
[poc]: https://mozakay.github.io/cloud%20operations%20and%20management/2026/10/03/unit-11-horizon-retail-cloud-operations-proof-of-concept.html
