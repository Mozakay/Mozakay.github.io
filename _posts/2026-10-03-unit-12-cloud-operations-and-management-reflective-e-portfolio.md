---
layout: post
title: "From Cloud Deployment to Evidence-Based Operational Judgement"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

# From Cloud Deployment to Evidence-Based Operational Judgement

Cloud Operations and Management | Unit 12 Reflective e-Portfolio

## 1. Introduction

A cloud deployment can report Succeeded while remaining insecure, difficult to recover or unsuitable for its intended workload. This exposes a fundamental challenge in cloud engineering: successful provisioning does not establish operational readiness.
Initial comparisons of AWS and Google Cloud explored how IaaS, PaaS and SaaS distribute control and responsibility, while public, private and hybrid models influence workload placement (Mell and Grance, 2011). However, practical implementation, technical failures and peer feedback challenged the assumption that selecting appropriate technologies and deploying them successfully constituted sufficient evidence of their suitability. Security assessments exposed risks beyond automated scan results, recovery testing revealed data loss despite successful restoration, and infrastructure automation demonstrated functionality without establishing production readiness.
Across six interconnected reflections, these experiences reveal a progression from evaluating what cloud technologies can deliver to critically examining what their observed results actually demonstrate. This development establishes evidence-based professional judgement as essential to decisions concerning security, resilience, migration and operational suitability.


## 2. Critical Weekly Reflections

### 2.1 Architecture and IaC: Capability or Organisational Suitability? (Units 2–3, revisited in Unit 11)

*Critical question: Can a credible roadmap or powerful IaC tool justify adoption without operational evidence?*

The initial ROCCA–TOGAF analysis valued phased government-cloud adoption for aligning technical decisions with organisational needs. However, tutor feedback challenged whether a credible roadmap demonstrated long-term governance or operational resilience. The underlying Indonesian case examined strategic planning rather than sustained operational outcomes (Anggraini, Binariswanto and Legowo, 2019). This exposed an important distinction between architectural coherence and demonstrated effectiveness.
Terraform was initially favoured for declarative reuse and multi-cloud portability. Payman's feedback highlighted remote-state access and locking, while Joseph questioned specialist expertise and maintenance overhead (Figure 1). These concerns aligned with IaC maintainability challenges discussed by Kumara et al. (2021). Crucially, Unit 11 provided an opportunity to revisit this judgement: Terraform provisioned Azure resources, and Ansible configured Nginx successfully. Nevertheless, the PoC did not validate secure collaborative state management, policy enforcement or production readiness.
The resulting judgement shifted from whether an IaC tool could reproduce infrastructure to whether that infrastructure could be securely governed, independently verified and maintained. Consequently, production adoption would require protected state, reviewed deployment plans, enforceable policy checks and post-deployment validation, none of which was fully established by the PoC.

<img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Payman's feedback on Terraform remote state, access control and locking" width="650">

*Figure 1a. Payman's feedback highlighted remote-state access and locking as governance requirements for collaborative Terraform use. Source: Units 2–3 GitHub activity, original Figure 2.*

<img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Joseph's feedback on Terraform operational overhead and specialist expertise" width="650">

*Figure 1b. Joseph's feedback identified specialist expertise and maintenance overhead as organisational constraints on Terraform adoption. Source: Units 2–3 GitHub activity, original Figure 3.*


### 2.2 Cloud-Native Services: Does Abstraction Remove Responsibility? (Unit 5, extended in Unit 10)

*Critical question: When does a functioning container or serverless deployment become an operable service?*

Early service-model comparisons explained reduced infrastructure management, but not how platform responsibility persists. In Unit 5, a Flask application was containerised with Docker, deployed on Minikube through Kubernetes Deployment and NodePort Service definitions, and increased from two to three replicas. This verified replica configuration, not automatic scaling, faster responses or fault tolerance (Unit 5 discussion).
Unit 10 extended the work to OpenFaaS: Kubernetes components ran, a Python greeting function was deployed, and invocation produced the intended response (Figure 2). Payman’s subsequent questions about registry credentials, CI/CD and function monitoring changed the success criterion. As Shafiei, Khonsari and Mousavi (2022) discuss, serverless reduces direct server administration without resolving all monitoring and security challenges. The new judgement separates functional invocation from secure, observable operation. A professional deployment would require image and secret controls, latency and error metrics, and concurrent-load tests before claiming elasticity.


<figure>
  <img src="{{ '/assets/images/COM/unit10/pic%205.png' | relative_url }}" alt="OpenFaaS function successfully deployed" width="600">
  <figcaption><em>Figure 2a. OpenFaaS successfully accepted the Python function deployment, demonstrating deployment functionality rather than production readiness. Source: Unit 10 OpenFaaS GitHub activity, original Figure 5.</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="OpenFaaS function invoked successfully" width="600">
  <figcaption><em>Figure 2b. Successful invocation of the Python greeting function confirmed functional execution, not production security, performance or elasticity. Source: Unit 10 OpenFaaS GitHub activity, original Figure 6.</em></figcaption>
</figure>


### 2.3 Cloud Security: Can a Low Scanner Score Establish Security Assurance? (Unit 7)

*Critical question: What security risks remain undetected when vulnerability-scanner results are treated as evidence of safety?*

Initial security assessment emphasised vulnerability severity. In Unit 7, Nginx and MongoDB containers on an Azure Ubuntu VM were assessed using OpenVAS from a separate VM. The first scan failed to discover the target; adjusting the Alive Test enabled assessment, revealing two low-severity findings (2.6) involving SSH MAC algorithms and TCP timestamps (Unit 7 GitHub, original Figures 8–10). This demonstrated that scan results depend on correct discovery and adequate coverage.
More significantly, manual inspection revealed MongoDB bound to 0.0.0.0:27017, while Azure NSG rules permitted unrestricted inbound access; enforced database authentication was not demonstrated (Figure 3). These findings indicated potential exposure, not proven compromise. Scanner coverage, network reachability and authentication assess distinct security controls, consistent with the configuration and access-control concerns discussed by Ali, Khan and Vasilakos (2015).
The resulting judgement shifted from interpreting scanner severity to evaluating layered security assurance. The separate NIST-based healthcare risk assessment extended this understanding through likelihood-and-impact evaluation, although its recommended controls were not implemented. Production remediation would require restricting database and SSH access, verifying authentication, applying updates and rescanning.

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure8.png' | relative_url }}" alt="OpenVAS scan showing a low severity score of 2.6" width="650">
  <figcaption><em>Figure 3a. OpenVAS identified low-severity vulnerabilities (2.6), but the scan did not establish overall system security. Source: Unit 7 Docker Security Audit GitHub activity, original Figure 8.</em></figcaption>
</figure>

<figure>
  <img src="{{ '/assets/images/COM/unit7/Figure3.png' | relative_url }}" alt="Azure NSG inbound rules allowing unrestricted SSH and MongoDB traffic" width="650">
  <figcaption><em>Figure 3b. Azure NSG rules permitted unrestricted inbound access to SSH and MongoDB, revealing configuration risks beyond the scanner findings. Source: Unit 7 Docker Security Audit GitHub activity, original Figure 3.</em></figcaption>
</figure>


### 2.4 Disaster Recovery: Does Restore Success Demonstrate Continuity? (Unit 8)

*Critical question: Which recovery objectives were demonstrated, and which remained unverified?*

Initially, RTO and RPO were treated as planning targets. In Unit 8, three manually triggered Restic snapshots protected application files and a PostgreSQL dump in Azure Blob Storage. After 180 orders and six files were added without another backup, files and the orders table were deliberately deleted. Restoration recovered 252,700 orders in 3 minutes 49 seconds, meeting the 30-minute RTO, but the later records and files remained lost (Figure 4).
NIST guidance emphasises recovery testing (Swanson et al., 2010); however, this simulation demonstrated only one recovery scenario. The 69-second snapshot-to-incident interval was an observed gap, not proof of the proposed 60-minute RPO: hourly backups were never automated. Subsequent discussion clarified this distinction; the 24.416 MiB restore could not establish production performance.
The resulting judgement shifted from equating restoration with continuity to requiring repeatable evidence of acceptable downtime and data loss. Production assurance would need automated scheduling, missed-backup alerts and periodic recovery tests.

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="PostgreSQL orders restored to 252700 records" width="600">
  <figcaption><em>Figure 4. Restoration recovered the protected state, not post-snapshot changes. Source: Unit 8 GitHub activity, original Figure 6 and Table 1.</em></figcaption>
</figure>

### 2.5 Database Migration: Is a Successful Import a Successful Transition? (Unit 9)

*Critical question: What remains unresolved after a database is copied accurately?*

Migration was initially evaluated through completed transfer. Unit 9 used mysqldump --single-transaction to move MySQL 8.0.46 into Azure MySQL 8.4; all four table counts matched. However, later transactions increased customers 8→9, orders 8→10 and order items 11→14. An INSERT-only delta and record-level checks reconciled the cloud database (Figure 5).
The key lesson was that initial consistency does not guarantee ongoing data consistency. Jamshidi, Ahmad and Pahl (2013) distinguish planning, execution and evaluation; the practical results showed why transferring data alone addresses only part of that process. The delta excluded UPDATE/DELETE changes, while application cutover and rollback remained untested. Consequently, judgement shifted from verifying copied records to planning change capture, acceptable downtime and recovery from a failed cutover. This insight subsequently informed the proposed Horizon Retail migration strategy.


<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Final Azure MySQL table and record validation following delta synchronisation" width="680">
  <figcaption><em>Figure 5. Final reconciliation confirms test-level data consistency, not application cutover. Source: Unit 9 GitHub, original Figure 4.</em></figcaption>
</figure>

### 2.6 Integrated Operations: Does a Working PoC Establish Production Readiness? (Unit 11, revisiting Units 3 and 9)

*Critical question: What evidence separates deployment success from production readiness?*

Unit 11 revisited the Unit 3 Terraform evaluation through implementation: Terraform provisioned Azure resources, Ansible configured Nginx (ok=5, changed=3, failed=0), and Azure Monitor recorded 2.93% average CPU over 30 minutes (Figure 6). This proved a functioning workflow and telemetry, not capacity or resilience for 150 stores. The Standard_B1s VM, reused subnet and HTTP endpoint limited generalisation.

Linking this PoC to Unit 9's INSERT-only delta and untested cutover exposed a further gap: deployable architecture does not establish a safe transition for existing applications and data. Rahman, Mahdavi-Hezaveh and Williams (2019) examine IaC research, but provisioning cannot establish migration readiness. Judgement shifted towards evaluating dependencies, synchronisation, cutover and rollback alongside security, load and failure testing. The broader hybrid architecture remained proposed, not implemented.


<figure>
  <img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Successful Ansible configuration results" width="650">
  <figcaption><em>Figure 6a. Ansible successfully configured Nginx (ok=5, changed=3, failed=0), demonstrating automated configuration, not production readiness. Source: Unit 11 Horizon Retail GitHub activity, original Figure 4.</em></figcaption>
</figure>

<figure>
  <img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Azure Monitor CPU telemetry for small proof of concept" width="650">
  <figcaption><em>Figure 6b. Azure Monitor recorded approximately 2.93% average CPU utilisation over 30 minutes, demonstrating telemetry collection, not production capacity or resilience. Source: Unit 11 Horizon Retail GitHub activity, original Figure 6.</em></figcaption>
</figure>


## 3. Skills Development, Independent Work and Collaboration

Skills advanced from command-based Azure CLI verification towards declarative Terraform provisioning, Ansible configuration and evidence-led operational evaluation. Table 1 synthesises tested competencies without repeating the six reflections.

**Table 1. Skills development linked to evidence and judgement**

| Capability | Practical evidence | Professional judgement |
| --- | --- | --- |
| **Provisioning and configuration** | Azure CLI VNet/subnet; Terraform/Ansible (`ok=5`, `changed=3`); Azure Monitor | Successful commands and CPU telemetry do not establish capacity or governance (LO3–LO4). |
| **Containers and AI** | Flask/Minikube; OpenFaaS invocation; CNN **75.89%** accuracy; Buildx fixed Azure image rejection | Deployment is distinct from measured performance and model reliability (LO2–LO4). |
| **Security** | OpenVAS **2.6** versus exposed NSG/MongoDB settings | Security requires configuration and identity assurance beyond scanning (LO3–LO4). |
| **Recovery and migration** | Restic **3:49**; lost post-snapshot orders; MySQL delta validation | Restore success and data transfer demand separate continuity/cutover tests (LO3–LO4). |

Independent troubleshooting included fixing host discovery, rebuilding an incompatible container image for Azure Container Apps (Figure 7), and adapting to subscription restrictions. TensorFlow supported the Unit 11 CNN workflow (Abadi *et al.*, 2016), but **75.89% test accuracy** did not establish real-world model reliability.

Group Report A assessed a **proposed Azure Resource Manager architecture**. The student's self-evaluation documents forming the team, coordinating work, consolidating sections and identifying inconsistencies in Benjamin's infrastructure design; the design itself was his contribution. Comparing sections with the shared scenario exposed a collaboration weakness: late cross-review. Earlier architecture assumptions, named reviewers and intermediate integration checks would be necessary in future team deployments.

<figure>
  <img src="/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png" alt="CNN inference successfully served by Azure Container Apps" width="700">
  <figcaption><em>Figure 7. Azure inference demonstrates deployment troubleshooting and basic functional testing. Source: Unit 11 TensorFlow and Keras GitHub activity, original Figure 4 (LO2, LO3).</em></figcaption>
</figure>

## 4. Critical Application to Retail: Horizon Retail Group

Horizon Retail's hypothetical **150 stores and e-commerce channel** face fluctuating demand, transaction consistency and WAN-dependent operations. Fully public hosting could simplify central management but interrupt local trading during connectivity failure; fully on-premises infrastructure preserves local processing at the cost of elastic peak capacity and maintenance. A **selective hybrid design** is defensible for keeping continuity-critical work near stores while placing central applications and analytics on Azure (Figure 8). Edge principles support locality for latency-sensitive processing (Shi *et al.*, 2016), although 150 distributed endpoints increase patching, monitoring and connectivity costs.

The choice also depends on service models. A VM permits OS-level control but retains patching and security responsibilities; managed PaaS reduces platform administration while limiting customisation. Neither is automatically cheaper: network links, synchronisation, cloud consumption and local support need a workload-level cost comparison, not extrapolation from the **2.93% CPU** PoC.

Practical evidence qualifies the proposal. The MySQL test demonstrates why changing retail orders require controlled migration and reliable replication; the OpenVAS audit challenges permissive database access; Restic shows that later transactions can remain unrecovered. Empirical migration research highlights the dependencies and organisational risks of moving legacy systems (Gholami et al., 2017); the retail plan therefore requires reconciled cutover, rollback, recovery targets and business acceptance tests. The CIFAR-10 deployment proves AI inference mechanics, not demand-forecast accuracy; any forecasting pilot needs actual retail data and benchmark results. Ethical, social and professional reflection further challenged cloud adoption criteria: user satisfaction cannot verify privacy controls (Al-Qahtani and Abu-Shanab, 2021), service availability does not guarantee equitable access, and a small VM experiment cannot establish environmental sustainability. Outages, vendor lock-in and operational costs also require evaluation (Armbrust et al., 2010).
Consequently, adoption should proceed through a staged pilot with measured latency, failure recovery, security, cost and accessibility, rather than assuming a working hybrid diagram is a production-ready solution.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail proposed hybrid cloud solution with PoC distinguished from future components" width="750">
  <figcaption><em>Figure 8. Horizon Retail architecture distinguishes the implemented technical PoC from the proposed hybrid production services. Source: Unit 11 Horizon Retail GitHub activity, original Figure 1 (LO2, LO4).</em></figcaption>
</figure>

## 5. Future Learning Goals

Goal 1: Governed IaC (months 0–3). Unit 3 feedback, Unit 7 exposure and the Horizon PoC revealed untested state and policy governance. HashiCorp tutorials will guide remote state locking, reviews and policy checks. Success requires rejecting an unsafe NSG change (Kumara et al., 2021).
Goal 2: Operational reliability (months 3–6). OpenFaaS invocation, CPU readings and manual Restic backups did not establish reliability. Azure Monitor training will support latency, error-rate and concurrent-load tests, plus backup alerts and repeated restores against proposed 30-minute RTO and 60-minute RPO targets (Swanson et al., 2010).
Goal 3: Controlled migration (months 6–9). Unit 9’s INSERT-only delta excluded UPDATE/DELETE changes and application cutover. A staged MySQL lab will test replication, cutover, rollback and record verification. Findings will guide Horizon Retail migration planning (Gholami et al., 2017).
Goal 4: Evidence-led innovation (months 9–12). CNN inference did not establish AI-assisted operations; proposed edge architecture remained untested. The student will compare anomaly monitoring with fixed thresholds and pilot offline store operation against cloud-only processing. Cost and human oversight will guide decisions; blockchain and quantum remain research topics until practical value is demonstrated (Notaro, Cardoso and Gerndt, 2021; Shi et al., 2016).

**Table 2. Proposed Training and Practical Development Plan**

| Timeline | Official Learning Resource | Practical Evidence of Development | Official Learning Link |
|---|---|---|---|
| **0–3 months** | HashiCorp: Terraform Remote State Tutorials | Secure state configuration and policy-checking demonstration | [HashiCorp Training](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/azure-remote) |
| **3–6 months** | Microsoft Learn: Deploy and Configure Azure Monitor | Service monitoring, backup alerts and repeated recovery tests | [Microsoft Learn](https://learn.microsoft.com/en-us/training/paths/deploy-configure-azure-monitor/) |
| **6–9 months** | Microsoft Learn: Choose a Tool to Migrate Data to Azure Database for MySQL | Documented replication, cutover and rollback rehearsal | [Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/choose-tool-to-migrate-data-to-azure-database-for-mysql/) |
| **9–12 months** | Microsoft Learn: Monitor AI Workloads on Azure; Azure Container Apps observability documentation | Comparative AI monitoring evaluation and edge feasibility assessment | [AI Monitoring](https://learn.microsoft.com/en-us/training/paths/monitor-ai-workloads-on-azure/) / [Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/observability) |


## 6. Conclusion

Across six reflections, professional judgement moved from choosing and deploying services to interrogating their evidence. Feedback exposed Terraform governance needs; Kubernetes and OpenFaaS proved functionality, not performance; OpenVAS severity did not capture network exposure; Restic recovered a snapshot but lost 180 post-backup orders; and MySQL synchronisation did not establish cutover.

These limitations converge in Horizon Retail: Ansible success and 2.93% CPU cannot justify deployment across 150 stores without tested security, capacity, recovery, migration and lifecycle cost (Swanson et al., 2010; Gholami et al., 2017). Independent troubleshooting and group cross-review underscored accountable verification. The ethical, social and professional reflection added requirements for privacy verification, equitable access and substantiated environmental claims.

Future learning targets governed IaC, reliability, controlled migration and justified innovation. Cloud adoption is appropriate only when verified organisational benefits outweigh operational risks and constraints.

---


## References

Abadi, M. *et al.* (2016) ‘TensorFlow: A system for large-scale machine learning’, *Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)*. Savannah, GA: USENIX Association, pp. 265–283. Available at: https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi (Accessed: 11 October 2026).

Al-Qahtani, F. and Abu-Shanab, E.A. (2021) ‘End user satisfaction with cloud computing: The case of Hamad Medical Corporation in Qatar’, *International Journal of Healthcare Information Systems and Informatics*, 16(4), pp. 1–23. Available at: https://doi.org/10.4018/IJHISI.295821.

Ali, M., Khan, S.U. and Vasilakos, A.V. (2015) ‘Security in cloud computing: Opportunities and challenges’, *Information Sciences*, 305, pp. 357–383. Available at: https://doi.org/10.1016/j.ins.2015.01.025.

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud computing adoption strategic planning using ROCCA and TOGAF 9.2: A study in government agency’, *Procedia Computer Science*, 161, pp. 1316–1324. Available at: https://doi.org/10.1016/j.procs.2019.11.247.

Armbrust, M. *et al.* (2010) ‘A view of cloud computing’, *Communications of the ACM*, 53(4), pp. 50–58. Available at: https://doi.org/10.1145/1721654.1721672.

Gholami, M.F. *et al.* (2017) ‘Challenges in migrating legacy software systems to the cloud: An empirical study’, *Information Systems*, 67, pp. 100–113. Available at: https://doi.org/10.1016/j.is.2017.03.008.

Jamshidi, P., Ahmad, A. and Pahl, C. (2013) ‘Cloud migration research: A systematic review’, *IEEE Transactions on Cloud Computing*, 1(2), pp. 142–157. Available at: https://doi.org/10.1109/TCC.2013.10.

Kumara, I. *et al.* (2021) ‘The do’s and don’ts of infrastructure code: A systematic gray literature review’, *Information and Software Technology*, 137, Article 106593. Available at: https://doi.org/10.1016/j.infsof.2021.106593.

Mell, P. and Grance, T. (2011) *The NIST Definition of Cloud Computing*. NIST Special Publication 800-145. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-145.

Notaro, P., Cardoso, J. and Gerndt, M. (2021) ‘A survey of AIOps methods for failure management’, *ACM Transactions on Intelligent Systems and Technology*, 12(6), Article 81. Available at: https://doi.org/10.1145/3483424.

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. Available at: https://doi.org/10.1016/j.infsof.2018.12.004.

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) ‘Serverless computing: A survey of opportunities, challenges, and applications’, *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. Available at: https://doi.org/10.1145/3510611.

Shi, W. *et al.* (2016) ‘Edge computing: Vision and challenges’, *IEEE Internet of Things Journal*, 3(5), pp. 637–646. Available at: https://doi.org/10.1109/JIOT.2016.2579198.

Swanson, M. *et al.* (2010) *Contingency Planning Guide for Federal Information Systems*. NIST Special Publication 800-34, Revision 1. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-34r1.


