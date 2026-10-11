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

A cloud deployment can report **Succeeded** while remaining insecure, difficult to recover or unsuitable for its intended workload. This is not a paradox: provisioning verifies a resource state, whereas operational assurance requires evidence of security, resilience and business fitness. That distinction frames this portfolio.

Unit 1 compared AWS and Google Cloud through IaaS, PaaS and SaaS, showing how control and customer responsibility differ; public, private and hybrid models also change workload placement (Mell and Grance, 2011). Azure experiments exposed consequences of those choices, from VM hardening to managed databases and proposed hybrid integration. Six reflections trace the development from evaluating architectures to implementing, testing and questioning them. Each links an artefact to cloud fundamentals (LO1), solution selection (LO2), practical configuration (LO3) or resilient design judgement (LO4), without treating a proof of concept as a production system.

## 2. Critical Weekly Reflections

### 2.1 Architecture and IaC: Capability or Organisational Suitability? (Units 2–3; LO1, LO2, LO4)

*Critical question: Can a credible roadmap or powerful IaC tool justify adoption without operational evidence?*

The ROCCA–TOGAF analysis favoured phased government-cloud adoption because it aligned technology with enterprise needs. However, tutor feedback distinguished the case study's planning value from unproven long-term governance and resilience (Units 2–3 GitHub, original Figure 1). Anggraini, Binariswanto and Legowo (2019) investigated strategic planning, not sustained multi-agency outcomes. The judgement changed: architectural coherence was insufficient without later operational verification.

In Unit 3, Terraform's declarative reuse and multi-cloud reach initially dominated comparison. Payman's feedback exposed remote-state locking and access requirements; Joseph questioned specialist skills and maintenance overhead (Figure 1). Such governance concerns align with documented IaC practice limitations (Kumara *et al.*, 2021). Crucially, **this evaluation was revisited in Unit 11**, where Terraform and Ansible were implemented rather than merely compared. That later PoC confirmed a provisioning workflow, but still did not test secured team state or policy gates. Future selection must therefore weigh organisational capacity, validated deployment and enforceable controls, not portability alone.

<figure>
  <img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Payman's feedback about Terraform state management and locking" width="650">
  <img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Joseph's feedback about IaC operational overhead and skills" width="650">
  <figcaption><em>Figure 1. Feedback changed the selection criteria for Terraform from technical capability to governable operation. Source: Units 2–3 GitHub activity, original Figures 2–3 (LO1, LO2, LO4).</em></figcaption>
</figure>
### 2.2 Cloud-Native Services: Does Abstraction Remove Responsibility? (Units 5 and 10; LO2–LO4)

*Critical question: When does a functioning container or serverless deployment become an operable service?*

Early service-model comparisons explained reduced infrastructure management, but not how platform responsibility persists. In Unit 5, a Flask application was containerised with Docker, deployed on Minikube through Kubernetes Deployment and NodePort Service definitions, and increased from two to three replicas. This verified replica configuration, **not** faster responses or fault tolerance (Unit 5 discussion).

Unit 10 extended the work to OpenFaaS: Kubernetes components ran, a Python greeting function was deployed, and invocation produced the intended response (Figure 2). Payman's subsequent questions about registry credentials, CI/CD and function monitoring changed the success criterion. As Shafiei, Khonsari and Mousavi (2022) discuss, serverless reduces direct server administration without resolving all monitoring and security challenges. The new judgement separates *functional invocation* from *secure, observable operation*. A professional deployment would require image and secret controls, latency and error metrics, and concurrent-load tests before claiming elasticity.

<figure>
  <img src="{{ '/assets/images/COM/unit10/pic%205.png' | relative_url }}" alt="OpenFaaS function successfully deployed" width="600">
  <img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="OpenFaaS function invoked successfully" width="600">
  <figcaption><em>Figure 2. Deployment acceptance and successful function invocation establish functionality, not production security or elasticity. Source: Unit 10 OpenFaaS GitHub activity, original Figures 5–6 (LO2, LO3).</em></figcaption>
</figure>
### 2.3 Cloud Security: What Can a Low Scanner Score Actually Prove? (Unit 7; LO1, LO3, LO4)

*Critical question: Is a low vulnerability score meaningful when cloud configuration creates another exposure path?*

The initial emphasis was on vulnerability-scanner severity. Nginx and MongoDB containers ran on an Azure Ubuntu VM, assessed from a separate OpenVAS VM. The first scan failed to discover the host; changing the Alive Test enabled scanning and produced two low-severity findings, each scored **2.6** (Unit 7 GitHub, original Figures 7–10).

Yet manual inspection revealed MongoDB published on TCP/27017 and an NSG rule admitting unrestricted inbound sources; enforced authentication was not demonstrated (Figure 3). The findings are not contradictory: scanner signatures, network reachability and application identity test different controls. Nor do these screenshots prove external compromise. Cloud-security research identifies configuration and access control as distinct risks (Ali, Khan and Vasilakos, 2015). This shifted judgement from accepting scanner severity to combining vulnerability results with network and authentication assurance. The complementary NIST-based healthcare risk assessment helped structure likelihood and impact, but its recommended controls were **not** implemented. In production, database exposure would be removed, identity verified and remedial changes rescanned.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%208%20OpenVAS%20Full%20and%20Fast%20scan%20completed%20successfully%20with%20a%20Low%20severity%20score%20of%202.6..png" alt="Completed OpenVAS scan displaying severity 2.6" width="650">
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%203%20Azure%20Network%20Security%20Group%20inbound%20rules%20allowing%20SSH%2C%20HTTP%20and%20MongoDB%20traffic..png" alt="Azure network security rules permitting broad inbound access" width="650">
  <figcaption><em>Figure 3. A low vulnerability score did not establish safe network exposure. Source: Unit 7 Docker Security Audit GitHub activity, original Figures 8 and 3 (LO3, LO4).</em></figcaption>
</figure>
### 2.4 Disaster Recovery: Does Restore Success Demonstrate Continuity? (Unit 8; LO3, LO4)

*Critical question: Which recovery objectives were measured, and which remained untested promises?*

Initially, RTO and RPO served as planning targets. The Restic exercise made the distinction concrete: application files and a PostgreSQL dump were backed up from an Azure VM to Blob Storage, then files and the orders table were deliberately deleted. The latest snapshot restored **252,700 orders in 3 minutes 49 seconds**, meeting the **30-minute RTO**. However, **180 later orders and six files** remained lost (Figure 4).

NIST contingency guidance treats recovery testing as necessary evidence (Swanson *et al.*, 2010), yet this single simulation validated only one restoration path. The **69-second** gap between snapshot and incident was observed, while the **60-minute RPO** was a target for a schedule never automated; the subsequent discussion clarified that distinction. Detection delay and performance under representative production load were also untested. The judgement therefore moved from *a backup exists* to *acceptable downtime and data loss must be demonstrated repeatedly*. Future operations require scheduled backups, failure alerts and measured recovery exercises, not confidence inferred from one successful command.

<figure>
  <img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="PostgreSQL orders restored to 252700 records" width="600">
  <figcaption><em>Figure 4. Database restoration confirms the latest protected state, not recovery of post-snapshot records. Source: Unit 8 Disaster Recovery GitHub activity, original Figure 6 and Table 1 (LO3, LO4).</em></figcaption>
</figure>
### 2.5 Database Migration: Is a Successful Import a Successful Transition? (Unit 9; LO2–LO4)

*Critical question: What remains unresolved after a database is copied accurately?*

Migration was initially evaluated through completed transfer. Unit 9 used `mysqldump --single-transaction` to move local MySQL **8.0.46** into Azure MySQL **8.4**; all four table counts matched the original snapshot. But the live source then acquired new transactions, increasing customers **8→9**, orders **8→10** and order items **11→14**. A controlled INSERT-only delta and record checks reconciled the cloud database (Figure 5).

Jamshidi, Ahmad and Pahl (2013) distinguish migration planning, execution and evaluation. The practical result supports that distinction: initial consistency did not preserve ongoing consistency. Moreover, an INSERT-only delta does not capture UPDATE/DELETE changes, and no application connection cutover or rollback was executed. Qatar Central subscription restrictions also led to UAE North, demonstrating deployment constraints without implying a legal residency rule. The revised judgement makes **dependency mapping, change capture, cutover, rollback and acceptable downtime** prerequisites for migration approval. This insight becomes central again when assessing the Horizon Retail architecture in Reflection 6.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit9/part1/Figure%204%20Final%20validation%20of%20the%20Azure%20MySQL%20database%20after%20final%20synchronisation..png" alt="Final Azure MySQL table and record validation following delta synchronisation" width="680">
  <figcaption><em>Figure 5. Final reconciliation demonstrates data consistency in the limited migration test, not full application cutover. Source: Unit 9 MySQL Migration GitHub activity, original Figure 4 (LO2, LO3, LO4).</em></figcaption>
</figure>
### 2.6 Integrated Operations: When Does a PoC Justify Production Adoption? (Unit 11; LO2–LO4)

*Critical question: What evidence is missing between automated deployment and a safe 150-store transition?*

Unit 11 put the earlier Unit 3 IaC evaluation into practice: Terraform provisioned Azure resources, Ansible configured Nginx and browser verification established service reachability. Ansible reported `ok=5`, `changed=3`, `failed=0`; Azure Monitor recorded around **2.93% average CPU** over 30 minutes (Figure 6). This supported operational integration, **not** production capacity or high availability. The single Standard_B1s VM, reused subnet and HTTP test endpoint limited any broader claim.

Rahman, Mahdavi-Hezaveh and Williams (2019) describe IaC practice, but repeatability alone cannot validate resilience or organisational suitability. Connecting this PoC to Unit 9 prompted a further change in judgement: **deployment architecture needs a migration strategy**, because existing applications, data and processes must reach the new environment safely. The future decision therefore requires governed state, HTTPS, load and failure tests, integration dependencies, synchronisation, verified cutover and rollback. The illustrated hybrid services remain **proposed**, not deployed. This completes the progression from selecting a tool in Unit 3 to evaluating an operational transition in Unit 11.

<figure>
  <img src="/assets/images/COM/unit11/part2/04-ansible-config.png" alt="Successful Ansible configuration results" width="650">
  <img src="/assets/images/COM/unit11/part2/06-azure-monitor.png" alt="Azure Monitor CPU telemetry for small proof of concept" width="650">
  <figcaption><em>Figure 6. Automated configuration and CPU telemetry demonstrate a working PoC, not production-scale resilience. Source: Unit 11 Horizon Retail GitHub activity, original Figures 4 and 6 (LO3, LO4).</em></figcaption>
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

Practical evidence qualifies the proposal. The MySQL test demonstrates why changing retail orders require controlled migration and reliable replication; the OpenVAS audit challenges permissive database access; Restic shows that later transactions can remain unrecovered. Empirical migration research highlights the dependencies and organisational risks of moving legacy systems (Gholami *et al.*, 2017); the retail plan therefore requires reconciled cutover, rollback, recovery targets and business acceptance tests. The CIFAR-10 deployment proves AI inference mechanics, **not** demand-forecast accuracy; any forecasting pilot needs actual retail data and benchmark results. The Reflective Report also distinguishes uptime from equitable access under weak connectivity. Consequently, adoption should proceed through a staged pilot with measured latency, failure recovery, security, cost and accessibility, rather than assuming a working hybrid diagram is a production-ready solution.

<figure>
  <img src="/assets/images/COM/unit11/part2/01-hybrid-architecture.png" alt="Horizon Retail proposed hybrid cloud solution with PoC distinguished from future components" width="750">
  <figcaption><em>Figure 8. Horizon Retail architecture distinguishes the implemented technical PoC from the proposed hybrid production services. Source: Unit 11 Horizon Retail GitHub activity, original Figure 1 (LO2, LO4).</em></figcaption>
</figure>
## 5. Future Learning Goals

The roadmap below derives each goal from a limitation exposed in practice and from serverless, AI and emerging technologies covered in Weeks 10–12.

**Goal 1: Governed IaC and DevOps (months 0–3).** The Terraform–Ansible PoC did not test remote-state governance or team approval, precisely the gaps raised in Unit 3. Development will cover Terraform modules, encrypted remote state, locking and CI/CD policy checks (Kumara *et al.*, 2021). Success means reproducing the environment and rejecting a deliberately unsafe NSG change.

**Goal 2: Observability and recovery assurance (months 3–6).** CPU telemetry, working OpenFaaS invocation and manual Restic snapshots did not establish service-level reliability. The next lab will set availability, latency and error objectives, test concurrent requests, alert on missed backups and repeat restores. Results must show whether **30-minute RTO** and **60-minute RPO** targets hold across trials (Swanson *et al.*, 2010).

**Goal 3: AI-assisted operations (months 6–9).** The CNN established model deployment, not resource optimisation. A controlled experiment will compare predictive scaling and anomaly detection with threshold-based alternatives, evaluating latency, false alerts, cost and drift; human approval remains necessary for consequential actions (Notaro, Cardoso and Gerndt, 2021).

**Goal 4: Edge and emerging technologies (months 9–12).** One store-level edge pilot will test local transaction continuity and management overhead during degraded connectivity (Shi *et al.*, 2016). Blockchain will be assessed only for a justified multi-party traceability requirement; quantum cloud remains exploratory specialised optimisation, not an immediate retail dependency (Preskill, 2018). Each study must end with evidence supporting adoption **or deferral**, not novelty alone.

## 6. Conclusion

Across the module, judgement progressed from comparing services to verifying what their results actually establish. State-governance feedback informed later Terraform practice; insecure exposure challenged scanner scores; recovered snapshots revealed lost transactions; and successful automation exposed the missing migration strategy. The professional outcome is a conditional, evidence-based standard for **secure, resilient and business-appropriate cloud operation**.

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

Table 1 summarises verified skills and their limitations; Section 5 explains the evidence-based learning roadmap in analytical prose.

The following are student-authored or course discussion artefacts, not peer-reviewed scientific publications. Their inclusion supports practical reflection. Formal self-/peer-referencing should follow the tutor's instructions under the University of Essex Online referencing guide.

| Portfolio evidence | Original uploaded Markdown or document | Demonstration and limitation |
| --- | --- | --- |
| Unit 1 baseline | `2026-08-06-unit-1-comparing-the-service-models-of-aws-and-google-cloud (1).md` | Service-model comparison, not provider benchmark |
| Figure 1 | `2026-08-17-units-2-3-cloud-architecture-frameworks-and-design(1).md`, original Figures 2–3; original Figure 1 discussed in prose | Terraform and tutor feedback on adoption evidence |
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
