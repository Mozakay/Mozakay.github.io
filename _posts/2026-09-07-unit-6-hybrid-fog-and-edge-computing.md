---
layout: post
title: "Microsoft Azure Resource Manager: An Evaluation of Cloud Deployment and Infrastructure Design"
categories: ["Cloud Operations and Management"]
unit: 6
journey_group: "unit-6"
---

# Unit 6: Hybrid, Fog and Edge Computing

*7th September 2026 | Critical reflection on Group Report A*

## From resource provisioning to operational governance

The Group Report A activity provided an opportunity to reconsider Microsoft Azure Resource Manager (ARM) beyond its apparent function as a tool for creating cloud resources. A provisioning-centred interpretation initially appears plausible because ARM deploys virtual machines, networks and databases. However, the report's examination of ARM's declarative, idempotent management model exposed a more consequential distinction: repeatable deployment defines an intended infrastructure state, whereas dependable operations also require enforceable access, resource organisation and lifecycle controls. Resource groups establish management boundaries; role-based access control (RBAC) limits management permissions; and tags and Azure Policy support classification and governance (Microsoft, 2026b). Rahman, Mahdavi-Hezaveh and Williams (2019) provide the broader Infrastructure as Code (IaC) research context for treating reproducible infrastructure definitions as managed artefacts rather than one-off configuration instructions.

This distinction changes how ARM should be evaluated. A successful template deployment would demonstrate that Azure accepted a specified resource configuration, not that permissions were appropriately scoped or that operational controls were effective. The stronger criterion is therefore whether the declared infrastructure can be reviewed, redeployed and governed consistently, while recognising that governance effectiveness still requires separate evidence.

## Service models: evaluating the distribution of responsibility

The IaaS–PaaS–SaaS comparison exposed an important design trade-off that a simple hierarchy of cloud services can conceal. ARM may provision infrastructure supporting IaaS workloads, but automating deployment does not transfer guest operating-system maintenance, patching or runtime security to Azure. In contrast, the report's proposed Azure App Service and Azure SQL Database reduce customer responsibility for underlying platform maintenance, while constraining operating-system-level control. ARM's direct provisioning and governance role also becomes more limited for SaaS applications (Younis et al., 2024; Microsoft, 2026b).

The resulting judgement is more precise than treating PaaS as universally preferable: PaaS is appropriate when managed operations and faster application delivery outweigh the need for extensive host-level configuration. For the report's secure web application, App Service and Azure SQL form a coherent PaaS-oriented choice; nevertheless, their selection alone does not establish that the application, network or data-access configuration is secure. The provider–customer responsibility boundary must be evaluated at the level of the *specific service and workload*, not merely its service-model label.

## Why hybrid deployment was selected, and what it complicates

The report considered public, private and hybrid cloud deployment against a scenario in which a secure web application must communicate with sensitive or legacy systems. A wholly public-cloud deployment offers centralised Azure management, whereas keeping all components within dedicated private infrastructure preserves organisational control but does not deliver the same Azure-hosted application model. The proposed hybrid arrangement therefore places the web application in Azure while retaining selected systems on-premises (Mell and Grance, 2011). This is a conditional architectural judgement, not evidence that hybrid infrastructure is inherently more secure or economical.

Azure Arc adds an important qualification. It can project *supported* external resources into Azure's management environment, but it does not make ARM a universal deployment engine for private infrastructure (Microsoft, 2025; Muniyandi, Nair and Natva, 2025). Furthermore, retaining data or services on-premises does not remove the need to protect cross-environment communication. Opara-Martins, Sahandi and Tian (2016) identify provider dependence as a cloud migration concern, while Ullah et al. (2024) examine how distributed processing across hybrid environments involves performance and resource-allocation considerations. Applied to the group scenario, these sources challenge an overly optimistic reading of flexibility: Azure-specific management can improve consistency, yet also increases dependency on integration mechanisms and demands evidence about network performance and ongoing operational cost.

## Critically examining the proposed ARM architecture

![Figure 1: Proposed Azure Infrastructure Design Using Azure Resource Manager](https://mozakay.github.io/assets/images/COM/unit6/Figure1.png)

*Figure 1. Proposed Azure Infrastructure Design Using Azure Resource Manager (Group Report A; original figure unchanged).*

The architecture in Figure 1 combines an on-premises system, a Site-to-Site VPN and Azure VPN Gateway, Azure Front Door, Azure App Service and Azure SQL Database. It also depicts ARM template deployment using JSON and a CI/CD or PowerShell workflow. The diagram is valuable because it connects workload placement to identity, networking and deployment automation, rather than considering those elements independently. It is, however, a **proposed design**: the group report contains no deployment results, measured network behaviour or security-test outcomes.

Three dependencies sharpen the reflection. **First, application and data access:** managed identity with Microsoft Entra authentication was proposed to avoid embedding database credentials in application code (Microsoft, 2026a). This addresses a credential-management risk, but does not itself demonstrate suitable database authorisations or network restrictions. **Second, hybrid communication:** the proposed Site-to-Site VPN terminates at Azure VPN Gateway, with App Service VNet Integration enabling the application to reach resources through the connected virtual network (Savill, 2019, pp. 181–182, 194–196). Such a topology requires more than drawing a connection; effective routing, access controls, availability and latency would need verification. **Third, repeatable deployment:** the report proposed a parameterised ARM JSON template under version control, deployable through PowerShell or CI/CD. Parameters for region and environment could reduce manual differences between development, test and production configurations. Deployment automation research supports attention to the relationship between models and execution tools (Wurster et al., 2020), but version control cannot, by itself, validate network security or application behaviour.

These dependencies lead to a narrower, defensible conclusion: the figure demonstrates *design reasoning and proposed component integration*, not production readiness. Before adoption, a prototype would need to test ARM deployment consistency, least-privilege access, database authentication, end-to-end hybrid connectivity, error handling and recoverability. These are **recommended verification activities**, not activities reported as completed by Group 1.

## Evaluating the Jotun evidence rather than transferring its results

The Jotun case study adds operational evidence absent from the group's proposed architecture. Microsoft (2021) describes modernisation of nine business applications using Azure App Service, Azure SQL Database and integration with on-premises applications. Jotun used ARM templates to switch QA and test environments off between releases and restore them when needed, illustrating how environment lifecycle management can contribute to resource and cost control. Its reported release cadence changed from two or three releases per year to every two or three weeks, while upgrade downtime fell to approximately 5–10 minutes.

The significance lies in distinguishing **plausible mechanisms from demonstrated outcomes**. Jotun supports the argument that automation and managed Azure services can contribute to operational improvements in a real organisation. It does not isolate ARM templates as the sole cause: the case also describes DevSecOps practices and App Service deployment slots (Microsoft, 2021). Nor does a Microsoft-published customer story establish that the group's unimplemented design would reproduce Jotun's benefits. The reflection therefore shifts from citing Jotun as proof of architecture success to using it as a bounded comparison and a reason to define measurable operational success criteria.

## Group learning, evidence boundaries and future practice

The Group 1 Team Contract established expectations for shared responsibility, weekly meetings, WhatsApp communication, SharePoint document sharing and collective review. Such arrangements provide a process for integrating service-model analysis, architecture reasoning and references into one report. However, the contract records agreed ways of working rather than the specific work performed by each member; individual contribution must be evidenced separately through peer assessment or document history. Consequently, this account does not attribute particular architecture or writing tasks to an individual without that evidence.

The central development in judgement is the distinction between **an architecturally coherent proposal and a validated operational solution**. Future use of this approach would connect design decisions to testable criteria: controlled deployments across environments, verifiable Azure-to-on-premises connectivity, appropriate identity permissions, and monitored reliability and cost. The unit's wider theme includes fog and edge computing, and the report references hybrid cloud-to-edge orchestration research (Ullah et al., 2021). Nevertheless, Group Report A did **not** design or implement a distinct fog or edge component. Treating that as a boundary of the submitted evidence, rather than retrospectively claiming experience, preserves the reflection's academic integrity.

## References

Mell, P. and Grance, T. (2011) *The NIST Definition of Cloud Computing*. NIST Special Publication 800-145. Gaithersburg, MD: National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-145

Microsoft (2021) ‘Jotun modernizes key business apps to run on Azure’, *Microsoft Customer Stories*, 27 December. (Accessed: 15 August 2026).

Microsoft (2025) ‘Azure Arc overview’, *Microsoft Learn*. (Accessed: 15 August 2026).

Microsoft (2026a) ‘Microsoft Entra authentication for Azure SQL’, *Microsoft Learn*, 15 May. (Accessed: 23 August 2026).

Microsoft (2026b) ‘What is Azure Resource Manager?’, *Microsoft Learn*, 4 August. (Accessed: 24 August 2026).

Muniyandi, V., Nair, S.S. and Natva, A.K. (2025) ‘Leveraging Azure Arc for unified hybrid cloud and multi-cloud management’, in *2025 International Conference on Computing Technologies & Data Communication (ICCTDC)*. IEEE. https://doi.org/10.1109/ICCTDC64446.2025.11159047

Opara-Martins, J., Sahandi, R. and Tian, F. (2016) ‘Critical analysis of vendor lock-in and its impact on cloud computing migration: a business perspective’, *Journal of Cloud Computing*, 5, article 4. https://doi.org/10.1186/s13677-016-0054-z

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. https://doi.org/10.1016/j.infsof.2018.12.004

Savill, J. (2019) *Microsoft Azure Infrastructure Services for Architects: Designing Cloud Solutions*. 1st edn. Newark: John Wiley & Sons, Incorporated.

Ullah, A., Dagdeviren, H., Ariyattu, R.C., DesLauriers, J., Kiss, T. and Bowden, J. (2021) ‘MiCADO-Edge: Towards an application-level orchestrator for the cloud-to-edge computing continuum’, *Journal of Grid Computing*, 19, article 47. https://doi.org/10.1007/s10723-021-09589-5

Ullah, F., Dhingra, S., Xia, X. and Babar, M.A. (2024) ‘Evaluation of distributed data processing frameworks in hybrid clouds’, *Journal of Network and Computer Applications*, 224, article 103837. https://doi.org/10.1016/j.jnca.2024.103837

Wurster, M., Breitenbücher, U., Falkenthal, M., Krieger, C., Leymann, F., Saatkamp, K. and Soldani, J. (2020) ‘The essential deployment metamodel: a systematic review of deployment automation technologies’, *SICS Software-Intensive Cyber-Physical Systems*, 35, pp. 63–75. https://doi.org/10.1007/s00450-019-00412-x

Younis, R., Iqbal, M., Munir, K., Javed, M.A., Haris, M. and Alahmari, S. (2024) ‘A comprehensive analysis of cloud service models: IaaS, PaaS, and SaaS in the context of emerging technologies and trend’, in *2024 International Conference on Electrical, Communication and Computer Engineering (ICECCE)*, pp. 1–6. IEEE. https://doi.org/10.1109/ICECCE63537.2024.10823401
