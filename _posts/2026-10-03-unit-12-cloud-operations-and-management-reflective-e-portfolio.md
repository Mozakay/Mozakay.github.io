---
layout: post
title: "From Cloud Deployment to Evidence-Based Operational Judgement"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

# From Cloud Deployment to Evidence-Based Operational Judgement

*Cloud Operations and Management | Unit 12 Reflective e-Portfolio*

## 1. Introduction

The Unit 1 comparison of AWS and Google Cloud addressed Infrastructure, Platform and Software as a Service (IaaS, PaaS and SaaS) mainly through responsibility, control and pricing. NIST also identifies public, private, community and hybrid deployment models, selected according to workload and organisational conditions (Mell and Grance, 2011). Later activities shifted the central question from **whether a cloud resource could be deployed** to **what operational evidence justified relying on it**.

This portfolio evaluates six connected learning episodes against cloud fundamentals (LO1), solution selection (LO2), implementation (LO3) and critical design of resilient solutions (LO4). Artefacts, feedback and research trace changing knowledge, skills and judgement. Successful tests are distinguished throughout from untested assumptions and proposed production architectures.

## 2. Critical Weekly Reflections

### 2.1 Architectural Frameworks and Governed Infrastructure as Code (Units 2–3 | LO2, LO4)

**Previous understanding and task.** The Unit 2 work initially valued ROCCA and TOGAF because staged cloud adoption could align technical decisions with organisational architecture. Analysing an Indonesian government-agency case supported a phased roadmap, but the tutor's feedback questioned whether evidence of planning also established long-term governance and operational performance (Units 2–3 GitHub, original Figure 1). The underlying study evaluated strategic planning, not sustained resilience across multiple agencies (Anggraini, Binariswanto and Legowo, 2019).

**Evidence and changed judgement.** In Unit 3, Terraform was initially preferred for declarative reuse and multi-cloud provisioning. Payman's comments introduced remote-state access and locking; Joseph questioned specialist expertise and maintenance overhead (Figure 1). These comments exposed how IaC can repeat unsafe configurations. Research on IaC documents the importance of maintainability and disciplined practices (Kumara *et al.*, 2021). The student's judgement consequently shifted towards assessing governance maturity and demonstrated outcomes, not merely architectural coherence. A professional rollout would require protected state, reviewed plans, change approval and post-deployment validation.

<figure>
  <img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Payman's feedback about Terraform state management and locking" width="650">
  <img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Joseph's feedback about IaC operational overhead and skills" width="650">
  <figcaption><em>Figure 1. Feedback changed the selection criteria for Terraform from technical capability to governable operation. Source: Units 2–3 GitHub activity, original Figures 2–3.</em></figcaption>
</figure>

### 2.2 Container Orchestration and Serverless Responsibility (Units 5 and 10 | LO2–LO4)

**Previous understanding and task.** Earlier comparisons explained why managed services reduce some infrastructure responsibilities, but did not demonstrate orchestration. In the Unit 5 discussion, the student created a Flask application, containerised it with Docker and deployed it through Minikube using Kubernetes Deployment and NodePort Service definitions. A change from two to three replicas demonstrated controller-managed scaling, **not** measured fault tolerance or improved response times (Unit 5 discussion, 24 August 2026).

**Evidence and changed judgement.** In Unit 10, Kubernetes nodes and OpenFaaS components were checked, a Python function was deployed, and invocation returned the intended greeting (Figure 2). Initially, successful invocation was the main criterion. Payman's feedback then raised image-registry permissions, credentials, CI/CD and monitoring complexity. Consistent with serverless research, abstraction reduces direct server administration without eliminating platform, security or performance responsibilities (Shafiei, Khonsari and Mousavi, 2022). This changed the operational judgement from *function works* to *function is controlled and measurable*. Future approval would require secured images and secrets, plus latency, error-rate and cold-start tests under concurrent requests.

<figure>
  <img src="{{ '/assets/images/COM/unit10/pic%205.png' | relative_url }}" alt="OpenFaaS function successfully deployed" width="600">
  <img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="OpenFaaS function invoked successfully" width="600">
  <figcaption><em>Figure 2. Deployment acceptance and successful function invocation establish functionality, not production security or elasticity. Source: Unit 10 OpenFaaS GitHub activity, original Figures 5–6.</em></figcaption>
</figure>

### 2.3 Security Scanning versus Configuration Assurance (Unit 7 | LO3, LO4)

**Previous understanding and task.** The student initially regarded vulnerability severity as an important security indicator. Nginx and MongoDB containers were configured on an Azure Ubuntu VM and examined using OpenVAS from another VM. The initial scan failed to detect its target; setting the Alive Test to 'Consider Hosts as Alive' enabled assessment. Two low-severity findings (2.6) concerned SSH algorithms and TCP timestamps (Unit 7 GitHub, original Figures 8–10).

**Interpretation and changed judgement.** The stronger finding came from manual configuration inspection: MongoDB was published on TCP/27017 and NSG rules permitted unrestricted inbound connections; enforced database authentication was not established by the inspected evidence (Figure 3). This does **not** establish unauthorised access, nor does the low scanner score certify safety. Scanner coverage, firewall reachability and application authentication answer different questions. Security research similarly identifies access-control and configuration risks (Ali, Khan and Vasilakos, 2015). Judgement therefore shifted from severity scores to layered assurance. Professional remediation would close public database access, restrict SSH, verify authentication and privileges, apply updates and rescan; the separate healthcare risk assessment supplied a structured NIST-based way to prioritise such treatments, not evidence that they were implemented.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%208%20OpenVAS%20Full%20and%20Fast%20scan%20completed%20successfully%20with%20a%20Low%20severity%20score%20of%202.6..png" alt="Completed OpenVAS scan displaying severity 2.6" width="650">
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%203%20Azure%20Network%20Security%20Group%20inbound%20rules%20allowing%20SSH%2C%20HTTP%20and%20MongoDB%20traffic..png" alt="Azure network security rules permitting broad inbound access" width="650">
  <figcaption><em>Figure 3. A low vulnerability score did not establish safe network exposure. Source: Unit 7 Docker Security Audit GitHub activity, original Figures 8 and 3.</em></figcaption>
</figure>

### 2.4 Disaster Recovery: Recovery Targets versus Measured Loss (Unit 8 | LO3, LO4)

**Previous understanding and task.** Initially, RTO and RPO were understood as planning targets. The Restic exercise made them testable: an Ubuntu VM in Austria East backed up application files and a PostgreSQL dump to Azure Blob Storage in Qatar Central. After three manually triggered snapshots, six files and 180 orders were added without another backup. Files were then deleted and the database orders table dropped to simulate destructive failure (Unit 8 GitHub, original Figures 3–4).

**Evidence, limitation and changed judgement.** Restoration recovered 252,700 orders and protected files in **3 minutes 49 seconds**, within the **30-minute RTO** (Figure 4). The later 180 orders and six files were correctly unrecoverable. The **69-second** snapshot-to-incident interval was an *observed gap*, while **60 minutes** was the proposed operational RPO; an hourly schedule was never automated. Subsequent discussion clarified this difference. NIST contingency guidance stresses planning and testing recovery arrangements (Swanson *et al.*, 2010). Professional judgement therefore changed from accepting a successful restore to requiring measurable downtime, tolerable lost transactions, monitored scheduling and repeated recovery tests under representative load. The small 24.416 MiB backup cannot establish enterprise recovery performance.

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="PostgreSQL orders restored to 252700 records" width="600">
  <figcaption><em>Figure 4. Database restoration confirms the latest protected state, not recovery of post-snapshot records. Source: Unit 8 Disaster Recovery GitHub activity, original Figure 6 and Table 1.</em></figcaption>
</figure>

### 2.5 Database Migration as a Controlled Transition (Unit 9 | LO2–LO4)

**Previous understanding and task.** Migration was initially judged by data transfer. A local MySQL 8.0.46 retail database was exported using `mysqldump --single-transaction` and restored to Azure Database for MySQL 8.4. Counts initially matched for customers, products, orders and order items. The snapshot-based export supported consistent InnoDB data without a prolonged write freeze, but subsequent source changes were not carried into the initial target.

**Evidence, limitation and changed judgement.** New transactions increased customers **8→9**, orders **8→10** and order items **11→14**. A controlled pause, INSERT-only delta transfer and record-level checks reconciled the Azure target (Figure 5). This exceeded basic import validation but excluded application redirection and UPDATE/DELETE capture. Subscription restrictions also required UAE North instead of the preferred Qatar Central region. Migration research recognises technical, organisational and dependency challenges (Gholami *et al.*, 2017). The student's judgement shifted from *database copied* to *transition controlled*: future migration strategies would define compatibility checks, change-data capture, cutover, rollback, acceptable downtime and post-cutover verification before retiring the source.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Final Azure MySQL table and record validation following delta synchronisation" width="680">
  <figcaption><em>Figure 5. Final reconciliation demonstrates data consistency in the limited migration test, not full application cutover. Source: Unit 9 MySQL Migration GitHub activity, original Figure 4.</em></figcaption>
</figure>

### 2.6 IaC, Observability and the Missing Migration Strategy (Unit 11 | LO3, LO4)

**Previous understanding and task.** The Horizon Retail proof of concept initially concentrated on proving that a cloud deployment workflow could function. Terraform provisioned and managed Azure resources, Ansible configured Nginx and a public page was verified; Azure Monitor then collected VM telemetry. Ansible reported `ok=5`, `changed=3` and `failed=0`, while average CPU utilisation was approximately **2.93%** over 30 minutes (Figure 6).

**Interpretation and changed judgement.** These outputs validated deployment and telemetry, not 150-store capacity or availability. The reused subnet, Standard_B1s VM and HTTP endpoint made the production limitations tangible. This also prompted a further change in judgement: **a deployable target architecture is incomplete without a migration strategy for existing applications, data and operational processes**. The Unit 9 experience showed why dependencies, reconciliation, cutover and rollback must enter architecture decisions early, rather than after infrastructure deployment. IaC scholarship supports repeatability but acknowledges potential defects in infrastructure code (Rahman, Mahdavi-Hezaveh and Williams, 2019). Future approval would require governed state, HTTPS, representative load and failure testing, an integration plan and measurable migration acceptance criteria. The wider hybrid diagram remains a **proposal**, not a deployed or validated enterprise environment.

<figure>
  <img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Successful Ansible configuration results" width="650">
  <img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Azure Monitor CPU telemetry for small proof of concept" width="650">
  <figcaption><em>Figure 6. Automated configuration and CPU telemetry demonstrate a working PoC, not production-scale resilience. Source: Unit 11 Horizon Retail GitHub activity, original Figures 4 and 6.</em></figcaption>
</figure>

## 3. Skills Development, Independent Work and Collaboration

Technical development progressed from Azure CLI configuration to Terraform provisioning, Ansible configuration and evidence-based operational testing. Table 1 summarises what each skill demonstrated and where judgement changed.

**Table 1. Skills developed and evidence of professional judgement**

| Capability | Verified practical evidence | Professional judgement |
| --- | --- | --- |
| **IaC and monitoring** | Azure CLI VNet/subnet; Terraform and Ansible (`ok=5`, `changed=3`); Azure Monitor CPU **2.93%** | Deployment and CPU telemetry do not establish secure configuration or capacity (LO3–LO4). |
| **Containers, serverless and AI** | Flask on Minikube; OpenFaaS invoked; CNN accuracy **75.89%**; Buildx resolved image rejection | Functionality does not demonstrate safe delivery, workload scaling or model reliability (LO2–LO4). |
| **Security and risk** | OpenVAS **2.6**; NSG/MongoDB configuration inspection | Low scanner severity does not establish low overall risk (LO3–LO4). |
| **Recovery and migration** | Restic recovery **3:49**, with 180 later orders lost; MySQL delta synchronisation validated | RTO, data loss and cutover readiness require different tests (LO3–LO4). |

Independent troubleshooting involved correcting OpenVAS host discovery, rebuilding the incompatible Azure container image and adapting to subscription constraints (Figure 7). Group Report A assessed a **proposed**, not deployed, ARM architecture. The student's self-evaluation records organising work, consolidating contributions and identifying inconsistencies in a teammate's infrastructure design, without claiming authorship of that design. Late cross-review prompted a specific improvement: assign reviewers and integration checkpoints earlier. This connected technical accountability with collaborative architectural governance.

<figure>
  <img src="/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png" alt="CNN inference successfully served by Azure Container Apps" width="700">
  <figcaption><em>Figure 7. Azure inference demonstrates deployment troubleshooting and basic functional testing. Source: Unit 11 TensorFlow and Keras GitHub activity, original Figure 4.</em></figcaption>
</figure>

## 4. Critical Application to Retail: Horizon Retail Group

The hypothetical retailer's **150 stores and e-commerce channel** require continuous checkout, consistent stock and order data, peak-demand capacity and recoverability. A public-cloud-only placement could make store transactions overly dependent on WAN availability, whereas an entirely local estate would retain infrastructure management and limit elastic capacity. A **selective hybrid** approach therefore appears proportionate: continuity-critical processing stays near stores, while Azure supports central applications, data integration and analytics. However, dual-environment identity, connectivity, data synchronisation and cost create additional risks requiring explicit ownership (Figure 8).

Practical results constrain this recommendation. Unit 9 demonstrates that an initial database import can leave stock and order data stale, so a retail migration must use suitable change capture, reconciled cutover and rollback. Unit 7 demonstrates that exposed ports and unverified authentication cannot be excused by a low vulnerability score. Unit 8 demonstrates that an available backup does not guarantee preservation of transactions since the last snapshot. The Unit 11 CPU result cannot justify capacity sizing without throughput, latency, error-rate, failover and total-cost measurements.

An AI demand-forecasting pilot remains plausible, but CIFAR-10 test accuracy supplies **no** evidence of forecast quality on sales data. Baseline forecasting, data quality and monitoring would need independent evaluation. Similarly, subscription-based regional restrictions encountered in Azure testing cannot by themselves establish legal data-residency requirements. The student's ethical reflection identified another constraint: operational uptime does not guarantee equitable access during connectivity disruption. Consequently, the professionally defensible recommendation is a staged **architecture-and-migration programme** with explicit security, resilience, cost, accessibility and business acceptance gates, rather than immediate wholesale adoption.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail proposed hybrid cloud solution with PoC distinguished from future components" width="750">
  <figcaption><em>Figure 8. Horizon Retail architecture distinguishes the implemented technical PoC from the proposed hybrid production services. Source: Unit 11 Horizon Retail GitHub activity, original Figure 1.</em></figcaption>
</figure>

## 5. Future Learning Goals

Four goals translate the limitations revealed in practical work into measurable development, while addressing serverless, AI and emerging technologies from Weeks 10–12.

**Goal 1: Governed Infrastructure as Code and DevOps (months 0–3).** The Horizon Retail PoC established provisioning, not safe team-based changes; Unit 3 feedback exposed state-management responsibilities. The next development stage will introduce reusable Terraform modules, protected remote state, locking and a CI/CD pipeline with policy checks (Kumara *et al.*, 2021). Success requires reproducing the deployment and demonstrating rejection of an unsafe NSG rule, rather than merely completing a pipeline.

**Goal 2: Observability and resilience engineering (months 3–6).** Azure Monitor recorded CPU but not service quality; OpenFaaS lacked latency and concurrency tests, while Restic backups were manual. The student will define latency, error-rate and availability indicators, test increasing loads, automate backup alerts and repeat restoration. Evidence must establish whether the proposed 30-minute RTO and 60-minute RPO are achieved across trials (Shafiei, Khonsari and Mousavi, 2022; Swanson *et al.*, 2010).

**Goal 3: AI-assisted operations (months 6–9).** The CNN deployment proved inference, not predictive resource management. The student will compare anomaly detection and predictive scaling against threshold-based controls on one workload. Cost, latency, false alerts and model drift will determine whether AI adds operational value; human review will remain necessary for high-impact actions (Notaro, Cardoso and Gerndt, 2021).

**Goal 4: Edge and emerging technologies (months 9–12).** A store-level edge pilot will measure checkout continuity, latency and management overhead during degraded connectivity (Shi *et al.*, 2016). Blockchain will be considered only if multi-party traceability outperforms a conventional auditable database. Quantum cloud remains a research option for specialised optimisation, not an immediate retail dependency given current technical limitations (Preskill, 2018). Each assessment will end in a justified adoption or deferral decision.

## 6. Conclusion

Across the module, operational judgement developed from explaining and deploying cloud services to asking what evidence justifies trusting them. Peer criticism, incomplete security assurance, recoverable but lost transactions, migration drift and an unscaled PoC each exposed a different limit. The resulting professional standard is not deployment success alone, but **governed, measurable and business-appropriate operation**.

---

## References

Abadi, M. *et al.* (2016) ‘TensorFlow: A system for large-scale machine learning’, *Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)*. Savannah, GA: USENIX Association, pp. 265–283. Available at: https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi (Accessed: 11 October 2026).

Ali, M., Khan, S.U. and Vasilakos, A.V. (2015) ‘Security in cloud computing: Opportunities and challenges’, *Information Sciences*, 305, pp. 357–383. Available at: https://doi.org/10.1016/j.ins.2015.01.025.

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud computing adoption strategic planning using ROCCA and TOGAF 9.2: A study in government agency’, *Procedia Computer Science*, 161, pp. 1316–1324. Available at: https://doi.org/10.1016/j.procs.2019.11.247.

Gholami, M.F. *et al.* (2017) ‘Challenges in migrating legacy software systems to the cloud: An empirical study’, *Information Systems*, 67, pp. 100–113. Available at: https://doi.org/10.1016/j.is.2017.03.008.

Kumara, I. *et al.* (2021) ‘The do’s and don’ts of infrastructure code: A systematic gray literature review’, *Information and Software Technology*, 137, Article 106593. Available at: https://doi.org/10.1016/j.infsof.2021.106593.

Mell, P. and Grance, T. (2011) *The NIST Definition of Cloud Computing*. NIST Special Publication 800-145. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-145.

Notaro, P., Cardoso, J. and Gerndt, M. (2021) ‘A survey of AIOps methods for failure management’, *ACM Transactions on Intelligent Systems and Technology*, 12(6), Article 81. Available at: https://doi.org/10.1145/3483424.

Preskill, J. (2018) ‘Quantum computing in the NISQ era and beyond’, *Quantum*, 2, Article 79. Available at: https://doi.org/10.22331/q-2018-08-06-79.

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. Available at: https://doi.org/10.1016/j.infsof.2018.12.004.

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) ‘Serverless computing: A survey of opportunities, challenges, and applications’, *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. Available at: https://doi.org/10.1145/3510611.

Shi, W. *et al.* (2016) ‘Edge computing: Vision and challenges’, *IEEE Internet of Things Journal*, 3(5), pp. 637–646. Available at: https://doi.org/10.1109/JIOT.2016.2579198.

Swanson, M. *et al.* (2010) *Contingency Planning Guide for Federal Information Systems*. NIST Special Publication 800-34, Revision 1. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-34r1.

## Evidence and Figure Register

**Table:** Table 1 summarises verified skills and their limitations; Section 5 explains the evidence-based learning roadmap in analytical prose.

The following are student-authored or course discussion artefacts, not peer-reviewed scientific publications. Their inclusion supports practical reflection. Formal self-/peer-referencing should follow the tutor's instructions under the University of Essex Online referencing guide.

| Portfolio evidence | Original uploaded Markdown or document | Demonstration and limitation |
| --- | --- | --- |
| Unit 1 baseline | `2026-08-06-unit-1-comparing-the-service-models-of-aws-and-google-cloud (1).md` | Service-model comparison, not provider benchmark |
| Figure 1 | `2026-08-17-units-2-3-cloud-architecture-frameworks-and-design(1).md`, original Figures 2–3 | Terraform feedback and governance requirements |
| Unit 5 Kubernetes discussion | `Discussion Unit 5.jpeg`, 24 August 2026 | Flask/Docker/Minikube and replica configuration, not load testing |
| Unit 5 command provisioning | `2026-08-31-unit-5-azure-cli-cloud-network-configuration.md`, original Figures 1–2 | Azure CLI VNet and subnet creation/verification |
| Figure 2 | `2026-09-21-unit-10-implementing-a-serverless-function-using-openfaas.md`, original Figures 5–6 | Deployment and invocation, not secure scaling |
| Figure 3 | `2026-09-08-unit-7-security-audit-of-a-docker-based-cloud-application.md`, original Figures 8 and 3 | OpenVAS versus exposed NSG configuration |
| Figure 4 | `2026-09-14-unit-8-disaster-recovery-and-business-continuity.md`, original Figure 6 and Table 1 | Measured recovery; manual scheduling limitation |
| Figure 5 | `2026-09-18-unit-9-cloud-database-migration-for-a-retail-order-management-system.md`, original Figure 4 | Data validation, not live application cutover |
| Figure 6 and 8 | `2026-10-03-unit-11-horizon-retail-cloud-operations-proof-of-concept (2).md`, original Figures 4, 6 and 1 | PoC versus proposed production design |
| Figure 7 | `2026-09-25-unit-11-part-1-formative-activity-tensorflow-and-keras (2).md`, original Figure 4 | AI inference, not retail forecasting validation |
| Group collaboration | `Peer Evaluation Group1 Moza(1).docx`, p. 5; `Team Contract.docx`; `Development Team Project - Azure (1).docx` | Individual self-reported contribution versus proposed group design |
| Reflective context | `Reflective Report(1).docx` | Ethical, social and operational judgements |
