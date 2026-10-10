---
layout: post
title: "Unit 12: Cloud Operations and Management – Reflective e-Portfolio"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

## 1. Introduction

This e-Portfolio consolidates the Cloud Operations and Management module and traces a change in how I evaluate cloud computing. I initially understood the subject through service models: Infrastructure as a Service (IaaS) gives customers the greatest control, Platform as a Service (PaaS) transfers runtime management to the provider, and Software as a Service (SaaS) delivers a complete application (Nadeem, 2022). I understood deployment types through location and control, as public, private and hybrid clouds (Mell and Grance, 2011).

The module showed that these definitions are starting points rather than decisions. Selecting, automating, securing, migrating and recovering services required evidence about workload requirements, governance and operational constraints. The portfolio therefore reflects on five technical themes: strategy, automation, security and risk, recovery and continuity, and migration with production readiness. These draw on practical work in Azure, Docker, OpenVAS, Restic, MySQL, OpenFaaS and TensorFlow, and on the Horizon Retail Group scenario, with an additional reflection on ethical, social and professional responsibilities. A recurring principle is that successful deployment is not the same as production readiness; implemented work is therefore distinguished throughout from proposed design. Together, the themes address fundamental concepts (LO1), different cloud solutions (LO2), configuration and implementation (LO3) and the critical selection of methods for resilient solutions (LO4).

## 2. Weekly Reflections

### 2.1 From Cloud Service Selection to Cloud Strategy

In Unit 1, the comparison of AWS and Google Cloud concluded that neither provider is universally superior; suitability depends on control requirements, workload behaviour and total cost (Alkhatib, Shaheen and Albustanji, 2025). Units 2 and 3 moved the analysis towards architecture. The ROCCA and TOGAF study supported a phased hybrid strategy, yet tutor feedback (Figure 1a) confirmed that it evidenced planning value rather than long-term outcomes (Anggraini, Binariswanto and Legowo, 2019). Similarly, I had treated Terraform's declarative, state-aware design (Özdoğan, Ceran and Üstündağ, 2023) as a technical strength until peer feedback (Figure 1b) framed state as a governance issue of remote storage, locking and access control. The group Azure Resource Manager report extended this to hybrid governance through Azure Arc (Microsoft, 2025; 2026b). Consequently, the Horizon Retail strategy adopts hybrid placement rather than indiscriminate full-cloud migration, accepting added connectivity, identity and governance complexity (Ali et al., 2025). Cloud adoption therefore depends on architecture, governance and integration, not provider selection alone.

<figure>
  <img src="/assets/images/COM/unit23/unit-2-post-to-me.png" alt="Peer feedback on the Unit 2 ROCCA and TOGAF discussion" width="600">
  <figcaption><em>Figure 1a. Tutor feedback on the ROCCA and TOGAF discussion (Unit 2).</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit23/unit3post1.png" alt="Peer feedback on Terraform state management" width="600">
  <figcaption><em>Figure 1b. Peer feedback on Terraform state management (Unit 3).</em></figcaption>
</figure>

### 2.2 From Provisioning to Controlled and Verifiable Cloud Operations

Initially, I treated successful provisioning as the achievement. In Unit 5, Azure CLI created a resource group, a virtual network (10.0.0.0/16) and a subnet (10.0.1.0/24) in Qatar Central, and `az network vnet show` returned a Succeeded state (Figure 2). However, this proved only that Azure accepted the request, not that the design was secure or appropriate, because a repeatable command can repeat a poor decision at scale (Hashizume et al., 2013). The Horizon proof of concept applied this lesson: Terraform provisioned the virtual machine, Ansible configured Nginx (ok=5, changed=3, failed=0), and Azure Monitor recorded approximately 2.93% average CPU utilisation (Figure 3). Terraform thus handled provisioning and Ansible configuration management. Student-subscription constraints required an existing subnet to be reused, so automation did not remove provider limits, and the CPU figure demonstrated telemetry rather than enterprise capacity (Microsoft, 2023). My sequence became create, automate, verify, configure, observe and interpret. Automation replaces manual administration but increases the importance of version control, testing and review (Kumara et al., 2021).

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

Docker initially appeared primarily as a portability mechanism, but the security audit demonstrated that containerisation introduces runtime, network and configuration responsibilities that must be assessed independently of the host (Martin et al., 2018). The first OpenVAS scan did not identify the target host; instead of accepting that result, I changed the Alive Test setting and repeated the scan, which reported two low-severity findings (score 2.6). Manual review then identified more significant exposures: MongoDB listening on 0.0.0.0:27017 with an unrestricted network security group rule, no authenticated identity in the connection status, HTTP without TLS and pending updates (Figure 4). These indicate exposure and authentication-assurance concerns rather than compromise, as no external access test was performed. A “no findings” result is therefore not evidence of security, because scanner scope and configuration limit it (Kritikos et al., 2019). The NIST SP 800-30 healthcare assessment and Horizon risk analysis then shifted my focus to likelihood, impact, treatment and residual risk (NIST, 2012). Cloud security requires continuous governance, identity management, secure configuration and risk-based prioritisation (Torkura et al., 2021).

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure 8 OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6..png' | relative_url }}" alt="Figure 8. OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6." width="700">
  <figcaption><em>Figure 4a. OpenVAS scan completed with a low-severity score of 2.6 (Unit 7).</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure%2012%20MongoDB%20configuration%20and%20connection%20status%20showing%20successful%20access%20with%20no%20authenticated%20users%20or%20roles..png' | relative_url }}" alt="Figure 12. MongoDB configuration and connection status showing successful access with no authenticated users or roles." width="700">
  <figcaption><em>Figure 4b. MongoDB connection status showing no authenticated users or roles (Unit 7).</em></figcaption>
</figure>


### 2.4 From Backup to Disaster Recovery and Business Continuity

I initially associated resilience with possessing backups. In Unit 8, Restic stored encrypted snapshots in Azure Blob Storage, separate from the virtual machine, protecting application files and a PostgreSQL database. A simulated incident deleted the files and dropped the orders table. Restoring the latest valid snapshot recovered 252,700 orders and the application files, and the integrity check reported no errors (Figure 5). Recovery took 3 minutes 49 seconds against a 30-minute target, but 180 orders and six files created after the final snapshot were lost. The 69-second interval between snapshot and incident was an observed recovery-point gap, not the recovery point objective; the proposed production objective is 60 minutes, requiring automated, monitored hourly backups, whereas these snapshots were manual. The operator also knew of the failure, so the timing excludes realistic detection. Backup is therefore not disaster recovery, and disaster recovery is not business continuity; each requires defined objectives and tested recovery (Swanson et al., 2010; Mendonça, Lima and Andrade, 2020). Modern cloud resilience is judged by measured, repeatable recovery.

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic5.png' | relative_url }}" alt="Recovery from latest Restic snapshot" width="500">
  <figcaption><em>Figure 5a. Recovery from the latest Restic snapshot (Unit 8).</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="Database restored to 252,700 records" width="500">
  <figcaption><em>Figure 5b. Orders table restored to 252,700 records (Unit 8).</em></figcaption>
</figure>

### 2.5 From Migration Strategy to Production Readiness

Migration initially appeared to be data copying. In Unit 9, a local MySQL 8.0.46 database was migrated to Azure Database for MySQL Flexible Server using mysqldump with `--single-transaction` and TLS. After the bulk restore matched baseline row counts, new source transactions created a deliberate gap; a maintenance window, delta synchronisation and record-level checks then established cutover readiness (Figure 6). The delta covered inserts only, so it was not production change-data-capture; continuous updates and deletions would require binary-log replication or an equivalent (Oracle, 2026). Migration is therefore a controlled service transition (Jamshidi, Ahmad and Pahl, 2013). In Unit 10, OpenFaaS on Kubernetes deployed and invoked a Python function (Figure 7), showing that serverless abstracts infrastructure management without eliminating it; cold starts and monitoring were not measured (Baldini et al., 2017; Shafiei, Khonsari and Mousavi, 2022). In Unit 11, a CIFAR-10 neural network (training 80.47%, validation 76.78%, test 75.89%) reached Azure Container Apps through Azure Container Registry only after Azure rejected the original image and it was rebuilt with Docker Buildx using OCI-compatible media types (Figure 8). The /health and /predict endpoints worked (sample confidence 79.62%), yet latency, concurrency, security and class-level reliability remained untested. Deployment is therefore one component of operational readiness; modern cloud operations integrate automation, containers, serverless, AI, monitoring and governance.

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

Reflecting on these activities also changed how I judge responsible cloud operation. **Ethically**, reviewing the Horizon NSG configuration showed why infrastructure deployment must be accompanied by access-control verification (Figures 3–4). Verdet et al. (2025) examine security-policy adoption in Terraform projects, while Khalil, Khreishah and Azeem (2014) identify privacy and security concerns in shared cloud environments. I would therefore review permissions and deployment constraints before release. Al-Qahtani and Abu-Shanab (2021) link security, privacy and trust to cloud-user satisfaction at Hamad Medical Corporation in Qatar; however, satisfaction does not verify technical security. I would combine user feedback with technical checks.

**Socially**, the recovery exercise demonstrated that restoring a service does not recover every lost transaction (Figure 5). Armbrust et al. (2010) identify availability and data lock-in as cloud-adoption challenges. My reflection extended this concern to users with limited connectivity or digital skills: technical availability alone does not ensure equitable access. Using a small VM and destroying temporary resources encouraged proportionate provisioning, but this cannot demonstrate environmental sustainability; future decisions require measured demand and resource use.

**Professionally**, the CPU screenshot evidenced telemetry, not service availability (Figure 3c). I would require recovery testing and application monitoring before recommending production use. Comparing service and deployment models also showed that hybrid control introduces complexity, while managed services reduce maintenance without removing accountability (Mell and Grance, 2011). My future decisions should therefore balance workload sensitivity, continuity, cost and organisational capability.

## 3. Skills Development

Skills are presented as capabilities, each linking application, evidence, challenge and professional significance (Table 1).

**Table 1. Skills development by capability group**

| Capability | Practical application and evidence | Challenge and learning | Professional significance |
|---|---|---|---|
| Infrastructure automation | Azure CLI created and verified a resource group, VNet and subnet; Terraform provisioned the Horizon virtual machine (Standard_B1s); Ansible configured Nginx (Figures 2–3). | Student-subscription limits forced reuse of a subnet. I learned to treat verification, not command success, as evidence, and to separate provisioning from configuration. | Repeatable, auditable delivery. |
| Networking and cloud infrastructure | Defined 10.0.0.0/16 and 10.0.1.0/24 address spaces; applied NSG rules; reached the scanner interface through an SSH tunnel; deployed MySQL in UAE North. | Qatar Central was unavailable for the MySQL deployment under the subscription. Region and network design proved to be architectural decisions constrained by provider policy. | Network exposure and data location are governance matters. |
| Security and risk | Ran OpenVAS; inspected Docker settings (privileged=false, no explicit user); mapped findings to ISO/IEC 27001:2022 controls; assessed a healthcare deployment using NIST SP 800-30 (Figure 4). | The first scan failed to identify the host, and manual review exposed risks the scan missed. | Interpreting scanner output and prioritising risk. |
| Resilience and migration | Restic with Azure Blob recovered PostgreSQL and files in 3 minutes 49 seconds; mysqldump migration used a consistent snapshot, delta synchronisation and validation (Figures 5–6). | Backup frequency determined data loss (180 orders); the delta method excluded updates and deletions. | Setting recovery objectives and cutover evidence. |
| Cloud-native and intelligent operations | Docker, Kubernetes and OpenFaaS delivered a Python function; TensorFlow/Keras trained a CNN deployed through Azure Container Registry to Azure Container Apps; Azure Monitor collected telemetry (Figures 3, 7–8). | Azure rejected the original image format until it was rebuilt with OCI-compatible media types; latency and concurrency were not measured. | Questioning workloads beyond functional success. |

The most important skill developed was evidence-based operational judgement rather than mastery of one tool. Independent practical tasks were complemented by the co-authored group report on Azure Resource Manager, which applied similar reasoning to hybrid design.

## 4. Application to Industry: Horizon Retail Group

Horizon Retail Group, a hypothetical retailer with approximately 150 stores and a growing e-commerce channel, provided the principal context for integrating the module. Its business problem is to absorb variable demand, integrate stores and suppliers securely, maintain trading during disruption and use data for decisions. From a cloud engineering and project management perspective, the central questions are which workloads should move, in what sequence and on what evidence.

Selected point-of-sale, inventory and operational functions should remain local, because a fully centralised model would increase store dependence on continuous network connectivity. Azure would host central applications, automation, monitoring, data and analytics (Figure 9). Azure elasticity suits e-commerce demand peaks, whereas local capability supports continuity during network disruption. This hybrid design is proposed rather than implemented, and it adds connectivity, identity and governance complexity (Ali et al., 2025).

A big-bang migration is inappropriate. Following Unit 9, a proof of concept should precede a limited pilot, measurement and staged rollout, with bulk transfer, synchronisation, validation and cutover planning; continuous retail transactions would require change-data-capture rather than the simplified delta used in the exercise. The validated chain (Terraform, Azure, Ansible, Nginx and Azure Monitor) demonstrates technical feasibility only, and one Standard_B1s virtual machine does not establish readiness for approximately 150 stores (Microsoft, 2023).

Proposed controls include HTTPS/TLS, a web application firewall, Microsoft Entra ID, role-based access control, private endpoints, Key Vault and central logging, because the public HTTP and SSH used in the proof of concept suited testing only. Azure Backup and Site Recovery are likewise proposals; workload-specific recovery objectives, validated through recovery testing as in Unit 8, should justify their cost (Microsoft, 2026a; 2026c). AI forecasting using Azure SQL Database and Blob Storage should follow data ownership, quality and governance, and should initially augment human planning (Fildes, Ma and Kolassa, 2022). Autoscaling and right-sizing should follow measured demand because capacity also carries cost (Gill and Chana, 2016).

Pilot success should be judged by availability, response time, incident rates, recovery performance, cost per workload and operational supportability. Production readiness therefore means demonstrated, supportable performance against agreed criteria, not completed deployment.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail hybrid cloud architecture" width="750">
  <figcaption><em>Figure 9. Horizon Retail hybrid architecture showing the validated proof of concept and proposed production design (Unit 11, Part 2).</em></figcaption>
</figure>

## 5. Future Learning Goals

The following goals arise from limitations identified in the practical work and from the Weeks 10–12 topics of serverless computing, AI and cloud computing, and emerging technologies.

**Goal 1: production-grade infrastructure as code and DevOps.** The Horizon proof of concept demonstrated repeatability but not state governance, testing or rollback. Within three months, I will refactor the Terraform configuration into modules with remote state and locking, then add a pipeline with policy checks, testing and rollback (Kumara et al., 2021).

**Goal 2: observability and site reliability engineering.** Azure Monitor validated telemetry, not capacity, and the OpenFaaS and Container Apps deployments lacked latency, cold-start and concurrency measurements. I will define service level indicators and objectives for both, then run load and failure tests with alerting, including missed-backup alerts, to support capacity planning (Microsoft, 2023).

**Goal 3: AI-assisted cloud operations.** Building on Unit 11, I will compare predictive scaling and anomaly detection with reactive autoscaling on one workload (Lorido-Botran, Miguel-Alonso and Lozano, 2014), assessing reliability, model drift, bias, transparency and human oversight, because AI should augment deterministic controls rather than replace them.

**Goal 4: edge and emerging technologies.** Edge computing could support offline store operation and lower latency but would enlarge the patching, monitoring and security surface across approximately 150 locations (Shi et al., 2016); I will test one store-level workload to measure that overhead. Blockchain remains conceptual, as I implemented nothing, and merits consideration only where a genuine distributed-trust requirement exists, such as supply-chain traceability. Quantum cloud is long-term research for logistics and inventory optimisation, not a production dependency (Golec et al., 2024).

Overall, the module moved my practice from comparing services towards evaluating strategy, automation, migration, security, resilience and emerging technologies as one operational lifecycle, judged by evidence rather than successful deployment.

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

