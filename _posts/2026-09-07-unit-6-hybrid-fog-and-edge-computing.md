---
layout: post
title: "Microsoft Azure Resource Manager: An Evaluation of Cloud Deployment and Infrastructure Design"
categories: ["Cloud Operations and Management"]
unit: 6
journey_group: "unit-6"
---

## Reflection on the Group Activity

The Unit 6 group activity examined Microsoft Azure Resource Manager (ARM) in the context of cloud service models, deployment approaches and infrastructure design. Initially, ARM could be understood principally as a way of provisioning Azure resources. The report developed a wider understanding of its operational role: declarative templates help standardise infrastructure, while resource groups, role-based access control (RBAC), tags and Azure Policy support repeatability and governance (Microsoft, 2026b; Rahman, Mahdavi-Hezaveh and Williams, 2019). This distinction matters because successfully creating resources is not equivalent to managing their security, lifecycle or consistency.

## Reconsidering Cloud Service and Deployment Models

Comparing IaaS, PaaS and SaaS made the division of responsibilities more explicit. IaaS retains operating-system and patching responsibilities for the customer, whereas PaaS transfers more platform maintenance to the provider. ARM can provision Azure IaaS and PaaS resources, but its direct role in managing SaaS applications is limited (Younis et al., 2024; Microsoft, 2026b). The important learning was therefore not that one service model is inherently superior, but that reduced operational effort is accompanied by reduced configuration control.

The public, private and hybrid cloud comparison further challenged the assumption that all workloads should be moved to a public cloud. The group recommended a **hybrid approach** for its secure web application scenario: Azure would host the web application, while sensitive or legacy systems could remain on-premises. Although Azure Arc can bring supported non-Azure resources into Azure management, this does not make ARM a universal manager for private infrastructure (Microsoft, 2025). The trade-off is significant: hybrid deployment accommodates organisational constraints, yet introduces connectivity, coordination and provider-dependence risks (Opara-Martins, Sahandi and Tian, 2016; Ullah et al., 2024).

## Reflecting on the Proposed Architecture

![Figure 1: Proposed Azure Infrastructure Design Using Azure Resource Manager](https://mozakay.github.io/assets/images/COM/unit6/Figure1.png)

*Figure 1. Proposed Azure Infrastructure Design Using Azure Resource Manager (Group Report A).*

Figure 1 captures the group's **proposed** hybrid architecture. Azure Front Door was selected as the public entry point; Azure App Service and Azure SQL Database represented managed application and data services. Managed identity with Microsoft Entra authentication was proposed to avoid embedding database credentials in application code (Microsoft, 2026a). The design also included a Site-to-Site VPN, Azure VPN Gateway and App Service VNet Integration to connect the Azure application with on-premises systems (Savill, 2019).

The strongest insight from designing these connections was that hybrid architecture is an **operational integration problem**, not just a choice of where applications run. An ARM JSON template, with parameters and deployment through PowerShell or CI/CD, could improve consistency between environments. Nevertheless, a reproducible template does not itself demonstrate secure connectivity, acceptable latency, effective monitoring or successful recovery. Those claims would require deployment and testing evidence, which the group report did not provide. This limitation changed the evaluation from asking whether the diagram was technically plausible to asking **what evidence would be needed before production adoption**.

## Industry Evidence and Its Limits

The Jotun case study offered a useful comparison with an organisation that had actually modernised applications using Azure App Service, Azure SQL Database and on-premises integration. Microsoft (2021) reported that Jotun used ARM templates to switch test environments off between releases and restore them when required. Reported release frequency increased from two or three times a year to every two or three weeks, while upgrade downtime decreased to approximately 5–10 minutes. The case helped link infrastructure automation to operational efficiency, but those results belong to Jotun's wider modernisation initiative. They cannot establish that the group's unimplemented architecture would deliver the same outcomes.

## Collaboration, Critical Judgement and Future Application

The Group 1 Team Contract established shared expectations for meetings, communication, task ownership and peer review, using WhatsApp for coordination and SharePoint for document sharing. This provided a collaborative framework for bringing together service-model analysis, architecture choices and research. However, the contract describes planned responsibilities rather than proving any particular member's individual contribution; a reflective account of individual work should be supported by peer-assessment or version-history evidence.

The activity strengthened the ability to evaluate **trade-offs rather than products in isolation**. In future cloud-design work, the proposed architecture would need explicit tests for connectivity, identity, resource governance, deployment repeatability, cost and operational resilience before its suitability could be concluded. Although the unit also addressed fog and edge computing, this particular group report concentrated on ARM and hybrid deployment and did not demonstrate a separate fog or edge implementation. Recognising that boundary is part of an evidence-based reflection.


## References

Mell, P. and Grance, T. (2011) *The NIST Definition of Cloud Computing*. NIST Special Publication 800-145. https://doi.org/10.6028/NIST.SP.800-145

Microsoft (2021) ‘Jotun modernizes key business apps to run on Azure’, *Microsoft Customer Stories*, 27 December.

Microsoft (2025) ‘Azure Arc overview’, *Microsoft Learn*.

Microsoft (2026a) ‘Microsoft Entra authentication for Azure SQL’, *Microsoft Learn*, 15 May.

Microsoft (2026b) ‘What is Azure Resource Manager?’, *Microsoft Learn*, 4 August.

Opara-Martins, J., Sahandi, R. and Tian, F. (2016) ‘Critical analysis of vendor lock-in and its impact on cloud computing migration: a business perspective’, *Journal of Cloud Computing*, 5, article 4. https://doi.org/10.1186/s13677-016-0054-z

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. https://doi.org/10.1016/j.infsof.2018.12.004

Savill, J. (2019) *Microsoft Azure Infrastructure Services for Architects: Designing Cloud Solutions*. 1st edn. Newark: John Wiley & Sons.

Ullah, F., Dhingra, S., Xia, X. and Babar, M.A. (2024) ‘Evaluation of distributed data processing frameworks in hybrid clouds’, *Journal of Network and Computer Applications*, 224, article 103837. https://doi.org/10.1016/j.jnca.2024.103837

Younis, R. et al. (2024) ‘A comprehensive analysis of cloud service models: IaaS, PaaS, and SaaS in the context of emerging technologies and trend’, in *2024 International Conference on Electrical, Communication and Computer Engineering (ICECCE)*, pp. 1–6. https://doi.org/10.1109/ICECCE63537.2024.10823401
