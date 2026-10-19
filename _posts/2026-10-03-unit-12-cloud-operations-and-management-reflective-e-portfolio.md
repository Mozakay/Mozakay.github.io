---
layout: post
title: "From Cloud Deployment to Evidence-Based Operational Judgement"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

## 1. Introduction

A cloud deployment can report *Succeeded* while remaining insecure, difficult to recover or unsuitable for its intended workload. This exposes a fundamental challenge in cloud engineering: successful provisioning does not establish operational readiness.

Initial comparisons of AWS and Google Cloud explored how IaaS, PaaS and SaaS distribute control and responsibility, while public, private and hybrid models influence workload placement (Zhang et al., 2010). However, practical implementation, technical failures and peer feedback challenged the assumption that selecting appropriate technologies and deploying them successfully constituted sufficient evidence of their suitability. Security assessments exposed risks beyond automated scan results, recovery testing revealed data loss despite successful restoration, and infrastructure automation demonstrated functionality without establishing production readiness.

Across six interconnected reflections, these experiences reveal a progression from evaluating the capabilities of cloud technologies to critically assessing the extent to which practical outcomes substantiate their claimed benefits. This development establishes evidence-based professional judgement as essential to decisions concerning security, resilience, migration and operational suitability.


## 2. Critical Weekly Reflections

### 2.1 Architecture and IaC: Capability or Organisational Suitability?

*Critical question: Can a credible roadmap or powerful IaC tool justify adoption without operational evidence?*

The initial ROCCA–TOGAF analysis valued phased government-cloud adoption for aligning technical decisions with organisational needs. However, tutor feedback challenged whether a credible roadmap demonstrated long-term governance or operational resilience. The underlying Indonesian case examined strategic planning rather than sustained operational outcomes (Anggraini, Binariswanto and Legowo, 2019). This exposed an important distinction between architectural coherence and demonstrated effectiveness.

Terraform was initially favoured for declarative reuse and multi-cloud portability (Özdoğan, Ceran and Üstündağ, 2023). However, this emphasis on technical benefits required closer scrutiny, particularly given research gaps concerning IaC code defects and security (Rahman, Mahdavi-Hezaveh and Williams, 2019). Payman subsequently highlighted remote-state access and locking (Figure 1a), while Joseph questioned specialist expertise and maintenance overhead (Figure 1b), reinforcing broader IaC maintainability concerns (Kumara et al., 2021). Building on Unit 6's ARM analysis, Table 1 compares Azure-native IaC and Terraform across integration, state management, governance and tooling costs, drawing on official documentation (HashiCorp, no date; Microsoft, 2026).

Unit 11 demonstrated Terraform provisioning and Ansible configuration, but the PoC did not establish secure collaborative state management, policy enforcement or production readiness. The judgement therefore shifted from technical reproducibility to governance, independent verification and maintainability. Terraform may be justified where multi-cloud needs outweigh management overhead; ARM-native IaC may suit Azure-only environments prioritising native integration. However, neither option warrants production adoption without comparative evaluation, reviewed deployment plans, enforceable policy checks and post-deployment validation.

*Table 1: Comparison of ARM-Native IaC and Terraform*

| Evaluation criterion | ARM templates / Bicep | Terraform |
| --- | --- | --- |
| Cloud support | Azure-specific | Multi-cloud through providers |
| Cost | No separate Bicep licence; Azure resource charges apply | Terraform CLI can be self-managed; managed HCP services may incur additional charges |
| Integration | Native ARM and Azure Portal integration | AzureRM/AzAPI providers; broader third-party integration |
| State management | No separate state file | Requires state storage and governance |
| Security and governance | Native ARM validation, RBAC and Azure Policy | Azure RBAC/Policy apply; provider credentials and state require management |
| Change management | ARM what-if previews deployment changes | terraform plan previews infrastructure changes |
| Maintenance | Azure-specific tooling and updates | Provider versions, state and configuration maintenance |
| Operational suitability | Azure-only environments prioritising native integration | Multi-cloud environments requiring cross-provider provisioning |

<img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Figure 1a evidence from the submitted Word report" width="700">

*Figure 1a: Payman’s feedback highlighted remote-state access and locking as governance requirements for collaborative Terraform use.*

<img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Figure 1b evidence from the submitted Word report" width="700">

*Figure 1b: Joseph’s feedback identified specialist expertise and maintenance overhead as organisational constraints on Terraform adoption.*

### 2.2 Cloud-Native Services: Does Abstraction Remove Responsibility?

*Critical question: When does a functioning container or serverless deployment become an operable service?*

Early service-model comparisons explained reduced infrastructure management, but not how platform responsibility persists. In the Unit 5 discussion, a Flask application was containerised with Docker, deployed on Minikube using Kubernetes Deployment and NodePort Service definitions, and scaled from two to three replicas. This demonstrated replica configuration rather than automatic scaling, improved response times or fault tolerance.

Unit 10 extended the work to OpenFaaS: Kubernetes components ran, a Python greeting function was deployed (Figure 2a), and invocation produced the intended response (Figure 2b). Payman’s subsequent questions about registry credentials, CI/CD and function monitoring changed the success criterion. As Shafiei, Khonsari and Mousavi (2022) discuss, serverless reduces direct server administration without resolving all monitoring and security challenges. The new judgement separates *functional invocation* from *secure, observable operation*. A professional deployment would require image and secret controls, latency and error metrics, and concurrent-load tests before claiming elasticity.

<img src="{{ '/assets/images/COM/unit10/pic%205.png' | relative_url }}" alt="Figure 2a evidence from the submitted Word report" width="700">

*Figure 2a: OpenFaaS successfully accepted the Python function deployment, demonstrating deployment functionality rather than production readiness.*

<img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="Figure 2b evidence from the submitted Word report" width="700">

*Figure 2b: Successful invocation of the Python greeting function confirmed functional execution, not production security, performance or elasticity.*

### 2.3 Cloud Security: Can a Low Scanner Score Establish Security Assurance?

*Critical question: What security risks remain undetected when vulnerability-scanner results are treated as evidence of safety?*

Initial security assessment emphasised vulnerability severity. In Unit 7, Nginx and MongoDB containers on an Azure Ubuntu VM were assessed using OpenVAS from a separate VM. The first scan failed to discover the target; adjusting the Alive Test enabled assessment, revealing two low-severity findings (2.6) involving SSH MAC algorithms and TCP timestamps (Figure 3a). This demonstrated that scan results depend on correct discovery and adequate coverage.

More significantly, manual inspection showed Docker published MongoDB on 0.0.0.0:27017, while Azure NSG rules permitted unrestricted inbound access (Figure 3b); enforced database authentication was not demonstrated. These findings indicated potential exposure, not proven compromise. Scanner coverage, network reachability and authentication assess distinct security controls, consistent with the configuration and access-control concerns discussed by Ali, Khan and Vasilakos (2015).

The resulting judgement shifted from interpreting scanner severity to evaluating layered security assurance. The separate NIST-based healthcare risk assessment extended this understanding through likelihood-and-impact evaluation (Joint Task Force Transformation Initiative, 2012), although its recommended controls were not implemented. Production remediation would require restricting database and SSH access, verifying authentication, applying updates and rescanning.

<img src="{{ '/assets/images/COM/unit7/Figure8.png' | relative_url }}" alt="Figure 3a evidence from the submitted Word report" width="700">

*Figure 3a: OpenVAS identified low-severity vulnerabilities (2.6), but the scan did not establish overall system security.*

<img src="{{ '/assets/images/COM/unit7/Figure3.png' | relative_url }}" alt="Figure 3b evidence from the submitted Word report" width="700">

*Figure 3b: Azure NSG rules permitted unrestricted inbound access to SSH and MongoDB, revealing configuration risks beyond the scanner findings.*

### 2.4 Disaster Recovery: Does Restore Success Demonstrate Continuity?

*Critical question: Which recovery objectives were demonstrated, and which remained unverified?*

Initially, RTO and RPO were treated as planning targets. In Unit 8, three manually triggered Restic snapshots protected application files and a PostgreSQL dump in Azure Blob Storage. After 180 orders and six files were added without another backup, files and the orders table were deliberately deleted. Following the simulated deletion, recovery restored 252,700 orders within 3 minutes 49 seconds of the incident, meeting the test’s 30-minute RTO, while data added after the final backup remained unrecovered (Figure 4).

Although NIST emphasises recovery testing (Swanson et al., 2010), feedback exposed limits of this trial. The tutor’s feedback prompted recognition that the observed 69-second gap did not establish consistent compliance with the proposed 60-minute RPO without automated backups. Donald’s comparison of data restoration on an existing VM with a complete VM rebuild highlighted how reprovisioning could extend overall recovery time.

The resulting judgement shifted from equating restoration with continuity to requiring repeatable evidence of acceptable downtime and data loss. Production assurance would need automated scheduling, missed-backup alerts and periodic recovery tests.

<img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="Figure 4 evidence from the submitted Word report" width="700">

*Figure 4: Restoration recovered the protected state, not post-snapshot changes.*

### 2.5 Database Migration: Is a Successful Import a Successful Transition?

*Critical question: What remains unresolved after a database is copied accurately?*

Migration was initially evaluated through completed transfer. Unit 9 used mysqldump --single-transaction to move MySQL 8.0.46 into Azure MySQL 8.4; all four table counts matched. However, later transactions increased customers 8→9, orders 8→10 and order items 11→14. An INSERT-only delta and record-level checks reconciled the cloud database (Figure 5).

The key lesson was that initial consistency does not guarantee ongoing data consistency. Jamshidi, Ahmad and Pahl (2013) distinguish planning, execution and evaluation; the practical results showed why transferring data alone addresses only part of that process. The delta excluded UPDATE/DELETE changes, while application cutover and rollback remained untested. Consequently, judgement shifted from verifying copied records to planning change capture, acceptable downtime and recovery from a failed cutover. This insight subsequently informed the proposed Horizon Retail migration strategy.

<img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Figure 5 evidence from the submitted Word report" width="700">

*Figure 5: Final reconciliation confirms test-level data consistency, not application cutover.*

### 2.6 Integrated Operations: Does a Working PoC Establish Production Readiness?

*Critical question: What evidence separates deployment success from production readiness?*

Unit 11 revisited the Unit 3 Terraform evaluation through implementation: Terraform provisioned Azure resources, Ansible configured Nginx (ok=5, changed=3, failed=0; Figure 6a), and Azure Monitor recorded 2.93% average CPU over 30 minutes (Figure 6b). This proved a functioning workflow and telemetry, not capacity or resilience for 150 stores. The Standard_B1s VM, reused subnet and HTTP endpoint limited generalisation.

Linking this PoC to Unit 9's INSERT-only delta and untested cutover exposed a further gap: deployable architecture does not establish a safe transition for existing applications and data. Judgement shifted towards evaluating dependencies, synchronisation, cutover and rollback alongside security, load and failure testing. The broader hybrid architecture remained proposed, not implemented.

<img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Figure 6a evidence from the submitted Word report" width="700">

*Figure 6a: Ansible successfully configured Nginx (ok=5, changed=3, failed=0), demonstrating automated configuration, not production readiness.*

<img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Figure 6b evidence from the submitted Word report" width="700">

*Figure 6b: Azure Monitor recorded approximately 2.93% average CPU utilisation over 30 minutes, demonstrating telemetry collection, not production capacity or resilience.*

## 3. Skills Development, Independent Work and Collaboration

Skills advanced from command-based Azure CLI verification towards declarative Terraform provisioning, Ansible configuration and evidence-led operational evaluation. Table 2 synthesises tested competencies without repeating the six reflections.

*Table 2: Skills development linked to evidence and Learning Outcomes*

| Capability | Practical evidence | Professional judgement | Learning Outcome Demonstrated |
| --- | --- | --- | --- |
| Provisioning and configuration | Azure CLI VNet/subnet; Terraform/Ansible (ok=5, changed=3); Azure Monitor | Successful commands and CPU telemetry do not establish capacity or governance. | Ability to configure cloud infrastructure and critically assess operational suitability. |
| Containers and AI | Flask/Minikube; OpenFaaS invocation; CNN 75.89% accuracy; Buildx resolved container image compatibility. | Deployment is distinct from measured performance and model reliability. | Understanding of cloud-native solutions and practical application of cloud tools. |
| Security | OpenVAS 2.6 versus exposed NSG/MongoDB settings | Security requires configuration and identity assurance beyond scanning. | Ability to evaluate security risks and determine appropriate controls for resilient cloud solutions. |
| Recovery and migration | Restic recovery in 3:49; 180 post-backup orders lost; INSERT-only MySQL delta validation. | Restore success and data transfer demand separate continuity/cutover tests. | Ability to assess recovery and migration methods against operational requirements. |

Independent troubleshooting included fixing host discovery, rebuilding an incompatible container image for Azure Container Apps (Figure 7), and adapting to subscription restrictions. TensorFlow supported the Unit 11 CNN workflow (Abadi *et al.*, 2016), but 75.89% test accuracy did not establish real-world model reliability.

Group Report A assessed a proposed Azure Resource Manager architecture. The self-evaluation documents individual contributions to forming the team, coordinating work, consolidating sections and identifying inconsistencies in Benjamin’s infrastructure design, while recognising his ownership of that design. Comparing sections with the shared scenario exposed a collaboration weakness: late cross-review. Earlier architecture assumptions, named reviewers and intermediate integration checks would be necessary in future team deployments.

<img src="/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png" alt="Figure 7 evidence from the submitted Word report" width="700">

*Figure 7: Azure inference demonstrates deployment troubleshooting and basic functional testing.*

## 4. Critical Application to Retail: Horizon Retail Group

Horizon Retail’s hypothetical 150 stores and e-commerce channel face fluctuating demand, transaction consistency and WAN-dependent operations. Fully public hosting could simplify central management but interrupt local trading during connectivity failure; fully on-premises infrastructure preserves local processing at the cost of elastic peak capacity and maintenance. A selective hybrid design is defensible for keeping continuity-critical work near stores while placing central applications and analytics on Azure (Figure 8). Edge principles support locality for latency-sensitive processing (Shi *et al.*, 2016), although 150 distributed endpoints increase patching, monitoring and connectivity costs.

The choice also depends on service models. A VM permits OS-level control but retains patching and security responsibilities; managed PaaS reduces platform administration while limiting customisation. Neither is automatically cheaper: network links, synchronisation, cloud consumption and local support need a workload-level cost comparison, not extrapolation from the 2.93% CPU PoC.

The practical exercises challenged whether technical success justified the proposed retail architecture. Although MySQL achieved data consistency in a controlled test, INSERT-only synchronisation highlighted the need to manage subsequent changes before cutover. Despite a low OpenVAS score, manual inspection identified permissive MongoDB network exposure, while Restic showed that successful recovery could leave post-backup transactions unrecovered. Together, these findings shifted the evaluation from isolated technical success towards data integrity, security and operational continuity. This judgement also reflects the technical and organisational challenges of legacy cloud migration identified by Gholami et al. (2017). Consequently, Horizon Retail requires reconciled cutover, rollback planning, recovery targets and business acceptance tests. Similarly, CIFAR-10 demonstrated functional inference, not demand-forecast accuracy, which requires representative retail data and benchmark results.

Earlier ethical, social and professional reflection extended the evaluation beyond technical deployment towards organisational suitability. Al-Qahtani and Abu-Shanab (2021) linked cloud-user satisfaction at Hamad Medical Corporation to trust, security and privacy, highlighting the importance of user acceptance. However, satisfaction does not independently verify privacy controls or equitable access, while a small VM experiment cannot establish environmental sustainability. Vendor lock-in also warrants consideration (Armbrust et al., 2010).

Consequently, adoption should proceed through a staged pilot with measured latency, failure recovery, security, cost and accessibility, rather than assuming a working hybrid diagram is a production-ready solution.

<img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Figure 8 evidence from the submitted Word report" width="700">

*Figure 8: Horizon Retail architecture distinguishes the implemented technical PoC from the proposed hybrid production services.*

## 5. Future Learning Goals

**Goal 1: Governed IaC (months 0–3):** Unit 3 feedback, Unit 7 exposure and the Horizon PoC revealed untested state and policy governance. HashiCorp tutorials will guide remote state locking, reviews and policy checks. Success requires rejecting an unsafe NSG change (Kumara et al., 2021), as outlined in Table 3.

**Goal 2: Operational reliability (months 3–6):** OpenFaaS invocation, CPU readings and manual Restic backups did not establish reliability. Azure Monitor training will support latency, error-rate and concurrent-load tests, plus backup alerts and repeated restores against proposed 30-minute RTO and 60-minute RPO targets (Swanson et al., 2010).

**Goal 3: Controlled migration (months 6–9):** Unit 9’s INSERT-only delta excluded UPDATE/DELETE changes and application cutover. A staged MySQL lab will test replication, cutover, rollback and record verification. Findings will guide Horizon Retail migration planning (Gholami et al., 2017).

**Goal 4: Evidence-led innovation (months 9–12):** As part of the learning plan in Table 3, CNN inference did not establish AI-assisted operations, while the proposed edge architecture remained untested. Future work will compare anomaly detection with fixed thresholds using false-positive rates (Notaro, Cardoso and Gerndt, 2021) and test offline store operation against cloud-only processing using latency and continuity measures (Shi et al., 2016). Cost and human oversight will guide decisions; blockchain and quantum require practical evaluation before adoption (Marchese and Tomarchio, 2022; Preskill, 2018).

*Table 3: Future Learning and Success Criteria*

| Timeline | Practical development activity | Success criterion |
| --- | --- | --- |
| 0–3 months | Configure Terraform remote state and policy checks | Unsafe NSG change rejected |
| 3–6 months | Test monitoring, backup alerts and recovery | Latency/errors recorded; recovery tested against RTO/RPO targets |
| 6–9 months | Test MySQL replication, cutover and rollback | Records reconciled; rollback demonstrated |
| 9–12 months | Compare AI anomaly detection and offline edge processing | False-positive rates, latency and continuity evaluated |

## 6. Conclusion

Across six reflections, professional judgement moved from choosing and deploying services to interrogating their evidence. Feedback exposed Terraform governance needs; Kubernetes and OpenFaaS proved functionality, not performance; OpenVAS severity did not capture network exposure; Restic recovered a snapshot but lost 180 post-backup orders; and MySQL synchronisation did not establish cutover.

These limitations converge in Horizon Retail: Ansible success and 2.93% CPU cannot justify deployment across 150 stores without tested security, capacity, recovery, migration and lifecycle cost (Swanson *et al*., 2010; Gholami *et al*., 2017). Independent troubleshooting and group cross-review underscored accountable verification. The ethical, social and professional reflection added requirements for privacy verification, equitable access and substantiated environmental claims.

Future learning targets governed IaC, reliability, controlled migration and justified innovation. Cloud adoption is appropriate only when verified organisational benefits outweigh operational risks and constraints.

## References

Abadi, M. *et al.* (2016) ‘TensorFlow: A system for large-scale machine learning’, *Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)*, Savannah, GA, 2–4 November. Berkeley, CA: USENIX Association, pp. 265–283. Available at: [https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi) (Accessed: 11 October 2026).

Al-Qahtani, F. and Abu-Shanab, E.A. (2021) ‘End user satisfaction with cloud computing: The case of Hamad Medical Corporation in Qatar’, *International Journal of Healthcare Information Systems and Informatics*, 16(4), pp. 1–23. Available at: [https://doi.org/10.4018/IJHISI.295821](https://doi.org/10.4018/IJHISI.295821).

Ali, M., Khan, S.U. and Vasilakos, A.V. (2015) ‘Security in cloud computing: Opportunities and challenges’, *Information Sciences*, 305, pp. 357–383. Available at: [https://doi.org/10.1016/j.ins.2015.01.025](https://doi.org/10.1016/j.ins.2015.01.025).

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud computing adoption strategic planning using ROCCA and TOGAF 9.2: A study in government agency’, *Procedia Computer Science*, 161, pp. 1316–1324. Available at: [https://doi.org/10.1016/j.procs.2019.11.247](https://doi.org/10.1016/j.procs.2019.11.247).

Armbrust, M. *et al.* (2010) ‘A view of cloud computing’, *Communications of the ACM*, 53(4), pp. 50–58. Available at: [https://doi.org/10.1145/1721654.1721672](https://doi.org/10.1145/1721654.1721672).

Gholami, M.F. *et al.* (2017) ‘Challenges in migrating legacy software systems to the cloud: An empirical study’, *Information Systems*, 67, pp. 100–113. Available at: [https://doi.org/10.1016/j.is.2017.03.008](https://doi.org/10.1016/j.is.2017.03.008).

HashiCorp (no date) *HCP Terraform subscription plans*. HashiCorp Developer. Available at: [https://developer.hashicorp.com/terraform/cloud-docs/overview](https://developer.hashicorp.com/terraform/cloud-docs/overview) (Accessed: 17 October 2026).

Jamshidi, P., Ahmad, A. and Pahl, C. (2013) ‘Cloud migration research: A systematic review’, *IEEE Transactions on Cloud Computing*, 1(2), pp. 142–157. Available at: [https://doi.org/10.1109/TCC.2013.10](https://doi.org/10.1109/TCC.2013.10).

Joint Task Force Transformation Initiative (2012) *Guide for Conducting Risk Assessments*. NIST Special Publication 800-30, Revision 1. Gaithersburg, MD: National Institute of Standards and Technology. Available at: [https://doi.org/10.6028/NIST.SP.800-30r1](https://doi.org/10.6028/NIST.SP.800-30r1).

Kumara, I. *et al.* (2021) ‘The do’s and don’ts of infrastructure code: A systematic gray literature review’, *Information and Software Technology*, 137, Article 106593. Available at: [https://doi.org/10.1016/j.infsof.2021.106593](https://doi.org/10.1016/j.infsof.2021.106593).

Marchese, A. and Tomarchio, O. (2022) ‘A blockchain-based system for agri-food supply chain traceability management’, *SN Computer Science*, 3, Article 279. Available at: [https://doi.org/10.1007/s42979-022-01148-3](https://doi.org/10.1007/s42979-022-01148-3).

Microsoft (2026) *Comparing Terraform and Bicep*. Microsoft Learn. Available at: [https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/comparing-terraform-and-bicep](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/comparing-terraform-and-bicep) (Accessed: 17 October 2026).

Notaro, P., Cardoso, J. and Gerndt, M. (2021) ‘A survey of AIOps methods for failure management’, *ACM Transactions on Intelligent Systems and Technology*, 12(6), Article 81. Available at: [https://doi.org/10.1145/3483424](https://doi.org/10.1145/3483424).

Özdoğan, E., Ceran, O. and Üstündağ, M.T. (2023) ‘Systematic analysis of infrastructure as code technologies’, *Gazi University Journal of Science Part A: Engineering and Innovation*, 10(4), pp. 452–471. Available at: [https://doi.org/10.54287/gujsa.1373305](https://doi.org/10.54287/gujsa.1373305).

Preskill, J. (2018) ‘Quantum computing in the NISQ era and beyond’, *Quantum*, 2, Article 79. Available at: [https://doi.org/10.22331/q-2018-08-06-79](https://doi.org/10.22331/q-2018-08-06-79).

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. Available at: [https://doi.org/10.1016/j.infsof.2018.12.004](https://doi.org/10.1016/j.infsof.2018.12.004).

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) ‘Serverless computing: A survey of opportunities, challenges, and applications’, *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. Available at: [https://doi.org/10.1145/3510611](https://doi.org/10.1145/3510611).

Shi, W. *et al.* (2016) ‘Edge computing: Vision and challenges’, *IEEE Internet of Things Journal*, 3(5), pp. 637–646. Available at: [https://doi.org/10.1109/JIOT.2016.2579198](https://doi.org/10.1109/JIOT.2016.2579198).

Swanson, M. *et al.* (2010) *Contingency Planning Guide for Federal Information Systems*. NIST Special Publication 800-34, Revision 1. Gaithersburg, MD: National Institute of Standards and Technology. Available at: [https://doi.org/10.6028/NIST.SP.800-34r1](https://doi.org/10.6028/NIST.SP.800-34r1).

Zhang, Q., Cheng, L. and Boutaba, R. (2010) ‘Cloud computing: State-of-the-art and research challenges’, *Journal of Internet Services and Applications*, 1(1), pp. 7–18. Available at: [https://doi.org/10.1007/s13174-010-0007-6](https://doi.org/10.1007/s13174-010-0007-6).
