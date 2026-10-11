---
layout: post
title: "From Cloud Deployment to Evidence-Based Operational Judgement"
categories: ["Cloud Operations and Management"]
unit: 12
journey_group: "unit-12"
---

<!-- Third-person academic revision. Reuses verified image paths from earlier GitHub posts; Figures 2 and 8 still require uploads. -->

# From Cloud Deployment to Evidence-Based Operational Judgement

*Cloud Operations and Management | Reflective e-Portfolio*

<!-- Editorial note from Word: Figure spaces are intentional. Replace each placeholder with the relevant cropped screenshot; keep the figure number and source caption. -->

## 1. Introduction

The student's foundational understanding began with IaaS, PaaS and SaaS, which distribute provider and customer responsibilities differently. Public, private and hybrid deployment models also involve distinct ownership and integration choices (Mell and Grance, 2011). The Unit 1 comparison of AWS and Google Cloud examined service features and costs, but did not establish workload suitability. Subsequent practical work shifted the evaluation from whether a cloud solution could be deployed to what evidence justified operating it securely and reliably.

This e-Portfolio critically traces cloud knowledge, practical skills and professional judgement across six learning episodes. Each connects activity or feedback to technical evidence, limitations, changed decisions and future professional application. The analysis addresses the four learning outcomes, from cloud fundamentals (LO1) and solution selection (LO2) to implementation (LO3) and critical evaluation of resilient solutions (LO4).

## 2. Weekly Reflections

### 2.1 Architecture and Governed IaC | Units 2–3 | LO2, LO4

Initially, the student valued ROCCA and TOGAF for connecting cloud-adoption stages with enterprise architecture. The Unit 2 analysis examined phased migration in a government agency; tutor feedback emphasised that the case demonstrated planning more convincingly than sustained operational outcomes (Figure 1). This mattered because a coherent roadmap does not prove that deployed systems remain secure or effective (Anggraini, Binariswanto and Legowo, 2019). The feedback made operational evidence necessary before judging adoption successful.

In Unit 3, the student initially favoured Terraform for declarative, multi-cloud provisioning. Payman Ghorbani raised state locking and access control, while Joseph Omondi Nyambok challenged its expertise and maintenance demands (Figure 1). Their feedback exposed a previously underweighted organisational dimension: repeatable IaC can also reproduce unsafe configuration (Kumara *et al.*, 2021). Professional selection criteria now include controlled state, peer review and team capability. Terraform's practical suitability therefore depends on whether a team can govern its dependencies and prevent unreviewed changes across environments.

<figure>
  <img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Peer comment on Terraform remote state, locking and access controls" width="700">
  <img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Peer comment on Terraform operational expertise and maintenance overhead" width="700">
  <figcaption><em>Figure 1. Peer feedback on Terraform governance and operational overhead. Source: Units 2–3 GitHub post, original Figures 2–3 (Payman and Joseph).</em></figcaption>
</figure>

### 2.2 Cloud-Native and Serverless Operations | Units 5, 10 | LO2–LO4

The earlier service-model comparisons did not establish how containerised applications were managed operationally. In a separate Unit 5 practical discussion, the student packaged a Flask application with Docker, deployed it to Minikube using Kubernetes Deployment and NodePort Service definitions, and tested increasing replicas from two to three (Figure 2). This demonstrated replica management, not improved latency, fault tolerance or full 12-Factor compliance. The replica change confirmed a controller instruction; without measuring responses during pod failure or concurrent demand, the experiment could not justify a claim of high availability.

The student subsequently deployed a Python greeting function through OpenFaaS, verified the Kubernetes components and obtained the expected invocation response (Unit 10 GitHub, Figures 2, 5–6). Peer feedback questioned registry credentials, image security and the monitoring complexity of multiple functions. As Shafiei, Khonsari and Mousavi (2022) identify, serverless reduces some infrastructure tasks without eliminating operational concerns. The resulting judgement distinguished a functioning endpoint from a securely managed service. Future application would require tests of concurrent requests, cold starts, errors and container provenance before operational approval.

<!-- FIGURE 2: Image not yet stored in the GitHub assets. Crop the Kubernetes/Minikube deployment and replica-scaling evidence from 'Discussion Unit 5.jpeg', upload the crop to your GitHub assets, and replace this comment with an <img> tag using its exact new path. -->

> **[Figure 2 image placeholder]** Practical Kubernetes deployment and replica-scaling evidence. Source: Unit 5 University discussion screenshot (24 August 2026). **Action:** upload a cropped screenshot and add its image path here.

*Figure 2. Practical Kubernetes deployment and replica-scaling evidence. Source: Unit 5 discussion.*

### 2.3 Security Findings versus Assurance | Unit 7 | LO3, LO4

Initially, the student treated vulnerability-scanner severity as an important indicator of security. To test a Docker application on Azure, Nginx and MongoDB were deployed on one Ubuntu VM and OpenVAS on another. The first scan detected no host; changing its Alive Test enabled discovery and a completed scan reporting two low-severity findings, each scored 2.6 (Unit 7 GitHub, Figures 8–10). These concerned weaker SSH message-authentication algorithms and TCP timestamp information disclosure, not demonstrated exploitation of MongoDB.

Manual inspection nevertheless showed unrestricted NSG rules and MongoDB published on TCP/27017; the inspected configuration did not adequately demonstrate enforced database authentication (Figure 3). These observations did not establish external compromise, but showed that scanning and configuration review addressed different risks. Cloud security therefore requires examination of access and deployment decisions, not just software findings (Ali, Khan and Vasilakos, 2015). The student's judgement changed from reliance on scan severity to a requirement for layered assurance. In professional practice, database exposure would be restricted, authentication and privileges verified, and the hardened environment rescanned.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%208%20OpenVAS%20Full%20and%20Fast%20scan%20completed%20successfully%20with%20a%20Low%20severity%20score%20of%202.6..png" alt="OpenVAS completed scan, low severity 2.6" width="650">
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%203%20Azure%20Network%20Security%20Group%20inbound%20rules%20allowing%20SSH%2C%20HTTP%20and%20MongoDB%20traffic..png" alt="Azure NSG unrestricted inbound rules for SSH, HTTP and MongoDB" width="650">
  <figcaption><em>Figure 3. OpenVAS low-severity result contrasted with unrestricted Azure NSG rules. Source: Unit 7 GitHub post, original Figures 8 and 3.</em></figcaption>
</figure>

### 2.4 Recovery Targets versus Tested Recovery | Unit 8 | LO3, LO4

RTO and RPO had initially been understood primarily as recovery-planning concepts; hands-on testing exposed their operational consequences. The student used Restic to back up Azure-hosted application files and a PostgreSQL dump into a separate Blob container. After deliberate deletion of the files and orders table, the latest snapshot was restored within 3 minutes 49 seconds, meeting a 30-minute RTO; 252,700 orders were recovered, but 180 later orders and six later files were lost (Figure 4). Restic verified the repository afterwards, although the protected dataset was only 24.416 MiB, limiting generalisation.

Discussion feedback prompted clarification that the observed 69-second snapshot-to-incident gap was not proof of compliance with the proposed 60-minute RPO policy. Snapshots were manually triggered, so hourly scheduling remained untested. NIST contingency guidance emphasises tested recovery arrangements (Swanson *et al.*, 2010). The student's revised judgement requires evidence of both restoration time and tolerable data loss, supported by automated schedules, missed-backup alerts and repeated recovery tests before production approval.

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="Restored PostgreSQL orders table with 252700 records" width="550">
  <figcaption><em>Figure 4. Restic restoration and recovery metrics. Source: Unit 8 GitHub post, original Figure 6 and Table 1.</em></figcaption>
</figure>

**Recovery measurements (Unit 8, original Table 1):**

| Test measure | Observed result |
|---|---|
| RTO target | 30 minutes |
| Measured recovery duration | 3 minutes 49 seconds |
| Snapshot-to-incident gap | 69 seconds (observed, not the scheduled RPO) |
| Proposed RPO target | 60 minutes (hourly scheduling not implemented) |
| Database restored | 252,700 orders |
| Post-backup data not recovered | 180 orders and 6 files |

### 2.5 Migration as Controlled Cutover | Unit 9 | LO2–LO4

The student's earlier focus in migration was on transferring data successfully. In Unit 9, `mysqldump --single-transaction` transferred a local MySQL 8.0.46 retail database into Azure MySQL 8.4. All four table counts initially matched. However, new source transactions increased customers from eight to nine, orders from eight to ten and order items from eleven to fourteen, leaving the target stale until an INSERT-only delta and record-level validation restored agreement (Figure 5). The initial dump used a transactionally consistent InnoDB snapshot, reducing the need to stop writes during bulk export, while the final maintenance window was designed to be brief.

This demonstrated consistent copying and a simulated maintenance window, not a live application cutover. The delta excluded UPDATE and DELETE operations. Migration research stresses evaluation and organisational dependencies alongside execution (Jamshidi, Ahmad and Pahl, 2013). Azure for Students restrictions additionally required UAE North rather than the preferred Qatar Central. This experience changed the student's judgement: migration must be assessed through synchronisation, compatibility, downtime, rollback and region constraints, not an error-free import alone. Matching counts could conceal inconsistent values; checking new records strengthened, but did not complete, validation. A busy production database would warrant assessment of change-data capture.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Azure MySQL final synchronisation validation with matching source records" width="700">
  <figcaption><em>Figure 5. Post-synchronisation validation of Azure MySQL. Source: Unit 9 GitHub post, original Figure 4.</em></figcaption>
</figure>

### 2.6 Automation, Monitoring and Migration Strategy | Unit 11 | LO2–LO4

Earlier activities tested individual tools; the Horizon Retail proof of concept connected Terraform provisioning, Azure infrastructure, Ansible configuration, Nginx service verification and Azure Monitor. Ansible completed with `ok=5`, `changed=3` and `failed=0`; Azure Monitor showed approximately 2.93% average CPU over 30 minutes (Figure 6). Yet a single Standard_B1s VM, reused subnet and HTTP endpoint could not establish security, resilience or capacity for approximately 150 stores. Reproducibility does not replace operational testing (Rahman, Mahdavi-Hezaveh and Williams, 2019). Whereas successful deployment had previously appeared the primary technical milestone, the integrated exercise recast it as only the first stage of operational acceptance.

The exercise also changed the student's judgement about migration strategy. Provisioning a cloud environment did not explain how existing applications, databases or store processes would transition to it. Connecting the PoC with the Unit 9 data-consistency problem established migration strategy as an architectural and operational planning requirement rather than a later implementation detail. A production recommendation would therefore need dependency mapping, data synchronisation, controlled cutover, rollback, acceptable downtime, HTTPS and workload-based monitoring. The wider hybrid architecture remained proposed, not implemented.

<figure>
  <img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Ansible configuration run with successful result and no failed tasks" width="700">
  <img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Azure Monitor CPU utilisation for Horizon Retail virtual machine" width="700">
  <figcaption><em>Figure 6. Automated configuration and operational CPU telemetry. Source: Unit 11 Horizon Retail PoC GitHub post, original Figures 4 and 6.</em></figcaption>
</figure>

## 3. Skills Development and Collaborative Working | LO1–LO4

Technical skills developed through a sequence of verifiable tasks. Azure CLI provisioned and verified a VNet and subnet in Qatar Central (Unit 5 GitHub, Figures 1–2); Terraform later formalised infrastructure definitions, while Ansible automated operating-system configuration. Docker, Kubernetes and OpenFaaS extended these skills to packaging, orchestration and function deployment. OpenVAS, Restic and MySQL exercises progressively shifted the student's focus from successful commands to validation of exposure, recoverability and data consistency.

In Unit 11, a CIFAR-10 CNN achieved 75.89% test accuracy. Its Azure Container Apps deployment initially failed because the image-layer format was unsupported; rebuilding with Docker Buildx enabled remote inference matching the local result (Figure 7). This established container compatibility, not model robustness, latency or production security (Abadi *et al.*, 2016).

Group Report A assessed an ARM-based proposal incorporating App Service, Azure SQL, managed identity, Front Door and hybrid connectivity. The student's self-evaluation documents initiating coordination, consolidating sections and identifying inconsistencies in a teammate's infrastructure design, not independently implementing that design (Figure 8). The Team Contract established shared review responsibilities, but cross-review occurred too late. Reviewing a peer's proposed architecture required checking whether App Service, Azure SQL, identity and VPN integration fitted the same scenario; this was architectural quality assurance, not evidence of deploying those services. Future collaboration requires earlier cross-reviews, shared assumptions and integration checkpoints.

<figure>
  <img src="/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png" alt="Azure Container Apps deployed CNN service returned prediction" width="700">
  <figcaption><em>Figure 7. Successful live inference from the containerised CNN model on Azure. Source: Unit 11 TensorFlow and Keras GitHub post, original Figure 4.</em></figcaption>
</figure>

<!-- FIGURE 8: Peer evaluation is not yet in GitHub assets. Before publishing, crop only your own contribution/reflection paragraphs from page 5 of Peer Evaluation Group1 Moza(1).docx and redact other people's names if appropriate. Upload that crop to your assets and replace this comment with the verified path. -->

> **[Figure 8 image placeholder]** Individual contribution and collaborative review. Source: Peer Evaluation Group 1 (2026), p. 5. **Action:** upload a cropped/redacted extract and add its image path here.

*Figure 8. Individual contribution and collaborative review lessons. Source: Peer Evaluation Group 1 (2026), p. 5.*

## 4. Critical Application to Retail | LO2, LO4

Horizon Retail Group's hypothetical 150-store and e-commerce environment requires reliable local trading, consistent orders and inventory, scalable central services and recoverable data. A public-cloud-only architecture could increase dependence on WAN connectivity; an entirely local design would retain greater infrastructure management overhead. The resulting professional recommendation is to retain selected continuity-critical store functions locally while hosting central services and analytics on Azure (Figure 9). Hybrid placement may reduce some interruption risks, but adds identity, synchronisation, network and cost complexity. The decision requires comparing local capacity, connectivity and dual-environment costs against the value of checkout continuity during WAN outages.

Practical evidence constrains that recommendation. The MySQL test exposed stale records after bulk transfer, so production integration would need reliable change capture, reconciled cutover and rollback. The security audit demonstrated why database reachability and a low scan score do not prove safe access. The Restic test recovered data but demonstrated loss after the last snapshot, requiring business-defined RPO and RTO. Terraform and Ansible support consistency, yet the PoC's 2.93% CPU value cannot size a multi-store workload; transaction rates, latency, error rates, failover and total costs need measurement. Likewise, an Azure public endpoint that works in a browser is not proof that payment or inventory services can remain operational during loss of connectivity.

AI forecasting could support inventory decisions, but the CIFAR-10 experiment proved image-model deployment, not retail forecasting accuracy. A pilot would require representative sales data and comparison with a non-AI baseline. Likewise, subscription restrictions encountered during testing are not themselves evidence of legal data-residency obligations. The student's professional recommendation is a staged migration with operational acceptance testing, considering security, cost and accessibility together rather than assuming technical availability guarantees user access.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail hybrid architecture showing implemented PoC and proposed components" width="750">
  <figcaption><em>Figure 9. Proposed hybrid-cloud architecture for Horizon Retail Group, distinguishing the validated PoC from the proposed production components. Source: Unit 11 Horizon Retail PoC GitHub post, original Figure 1.</em></figcaption>
</figure>

## 5. Future Learning Goals

The first eight-week learning objective is to build a governed Terraform pipeline with encrypted remote state, locking, review approval and policy checks. Completion would be evidenced by reproducing the environment and demonstrating rejection of an intentionally insecure NSG rule, directly addressing the IaC governance gap.

The next twelve-week objective is to test Kubernetes and OpenFaaS under controlled concurrency, recording cold starts, latency, error rates and scaling. It also includes automating Restic backups, configuring failure alerts and conducting repeated restores against explicit 30-minute RTO and 60-minute RPO targets. These results would address the untested assumptions in Units 5, 8 and 10. Baselines and failed recovery attempts would be documented alongside successful runs.

Over six months, the development plan calls for comparing AI-based workload forecasting against threshold-based scaling in terms of cost, responsiveness and under-provisioning, and testing whether edge processing benefits an appropriately chosen retail event. Unit 12 discussions of blockchain and quantum computing support feasibility assessments rather than automatic adoption: multi-party trust or specialised computation must justify added governance and cost. Each investigation would document unsuccessful tests alongside successful outcomes.

## 6. Conclusion

Across the module, the student's judgement developed from selecting and deploying services towards asking what evidence justifies their operation. The most consequential lessons arose when results were incomplete: low scanner severity, successful but lossy recovery, a stale migrated database and a functioning yet unscaled PoC. These distinctions now support more defensible architectural, security and migration decisions.

## References

Abadi, M. *et al.* (2016) ‘TensorFlow: A system for large-scale machine learning’, *Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)*. Savannah, GA: USENIX Association, pp. 265–283. Available at: https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi (Accessed: 11 October 2026).

Ali, M., Khan, S.U. and Vasilakos, A.V. (2015) ‘Security in cloud computing: Opportunities and challenges’, *Information Sciences*, 305, pp. 357–383. Available at: https://doi.org/10.1016/j.ins.2015.01.025.

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud computing adoption strategic planning using ROCCA and TOGAF 9.2: A study in government agency’, *Procedia Computer Science*, 161, pp. 1316–1324. Available at: https://doi.org/10.1016/j.procs.2019.11.247.

Jamshidi, P., Ahmad, A. and Pahl, C. (2013) ‘Cloud migration research: A systematic review’, *IEEE Transactions on Cloud Computing*, 1(2), pp. 142–157. Available at: https://doi.org/10.1109/TCC.2013.10.

Kumara, I. *et al.* (2021) ‘The do’s and don’ts of infrastructure code: A systematic gray literature review’, *Information and Software Technology*, 137, Article 106593. Available at: https://doi.org/10.1016/j.infsof.2021.106593.

Mell, P. and Grance, T. (2011) *The NIST Definition of Cloud Computing*. NIST Special Publication 800-145. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-145.

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. Available at: https://doi.org/10.1016/j.infsof.2018.12.004.

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) ‘Serverless computing: A survey of opportunities, challenges, and applications’, *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. Available at: https://doi.org/10.1145/3510611.

Swanson, M. *et al.* (2010) *Contingency Planning Guide for Federal Information Systems*. NIST Special Publication 800-34, Revision 1. Gaithersburg, MD: National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-34r1.

## Evidence Index (supporting artefacts)

<!-- Editorial note from Word: The entries below identify original artefacts and figures for the editor. For formal self-/peer-referencing, follow University of Essex Online guidance and confirm the accepted approach with the tutor. -->

| Unit | Original source | Evidence |
| --- | --- | --- |
| Units 2–3 | 2026-08-17-units-2-3-cloud-architecture-frameworks-and-design(1).md | Figures 1–3: tutor and peer feedback |
| Unit 5 Kubernetes | Discussion Unit 5.jpeg | Flask, Docker, Minikube and replica scaling |
| Unit 7 | 2026-09-08-unit-7-security-audit-of-a-docker-based-cloud-application.md | Figures 3, 8–12: OpenVAS and NSG |
| Unit 8 | 2026-09-14-unit-8-disaster-recovery-and-business-continuity.md | Figure 6 and Table 1: recovery measurements |
| Unit 9 | 2026-09-18-unit-9-cloud-database-migration-for-a-retail-order-management-system.md | Figure 4: synchronisation validation |
| Unit 10 | 2026-09-21-unit-10-implementing-a-serverless-function-using-openfaas.md | Figures 2, 5–6: function deployment/invocation |
| Unit 11 AI | 2026-09-25-unit-11-part-1-formative-activity-tensorflow-and-keras (2).md | Figure 4: Azure prediction |
| Unit 11 PoC | 2026-10-03-unit-11-horizon-retail-cloud-operations-proof-of-concept (2).md | Figures 1, 4 and 6: architecture, Ansible, Monitor |
| Group work | Peer Evaluation Group1 Moza(1).docx | Page 5: self-evaluation of contribution |
| Unit 5 Azure CLI | Unit 5: Azure CLI Cloud Network Configuration (GitHub Markdown) | Figures 1–2: VNet setup and verification |
