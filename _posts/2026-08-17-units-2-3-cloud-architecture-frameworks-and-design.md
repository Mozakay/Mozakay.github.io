---
layout: post
title: "Units 2–3: Cloud Architecture, Frameworks and Design"
categories: ["Cloud Operations and Management"]
journey_group: "units-2-3"
---

## Context and Purpose

Units 2 and 3 developed my understanding of cloud architecture, cloud adoption frameworks and Infrastructure as Code (IaC). The activities required more than description: they involved evaluating how organisations can structure cloud adoption and how infrastructure tools should be selected according to technical and organisational requirements.

In Unit 2, I examined the integration of the Roadmap for Cloud Computing Adoption (ROCCA) with TOGAF 9.2 in a government-agency context. In Unit 3, I evaluated Terraform as a cloud design and provisioning tool and compared its strengths and limitations with alternative Infrastructure as Code approaches. Peer discussion was important in both units because it exposed limitations and operational considerations that were not equally visible in my initial analysis.

## Unit 2: ROCCA and TOGAF Implementation in Government Agencies

Anggraini, Binariswanto and Legowo (2019) examine how the Roadmap for Cloud Computing Adoption (ROCCA) can be integrated with TOGAF 9.2 to guide cloud adoption in government agencies. This integration is significant because public-sector cloud migration is not only a technical decision; it must also reflect organisational objectives, regulatory obligations, stakeholder expectations and existing capabilities.

ROCCA provides a cloud-specific roadmap covering analysis, planning, adoption, migration and management, while TOGAF provides the enterprise architecture structure needed to align business, data, application and technology decisions. Their value therefore lies in complementarity: ROCCA addresses the cloud-adoption process, whereas TOGAF connects that process to wider enterprise architecture.

The article applies the combined approach to SKK Migas, an Indonesian government agency facing growing data volumes, limited data-centre capacity, budget pressures and operational constraints. Mapping ROCCA activities to the TOGAF Architecture Development Method enabled the agency to assess its current position, identify stakeholders, define target architectures and prepare an implementation roadmap.

The phased hybrid-cloud strategy is a notable strength because it begins with lower-risk supporting applications before considering more critical services. In a government context, this reduces the need to treat cloud migration as an all-or-nothing decision and allows security, procurement, compliance and service performance to be evaluated progressively.

However, the evidence remains stronger for planning than for long-term implementation. The study is based on one agency and limited managerial evaluation, which reduces the generalisability of the findings. The combined framework is therefore persuasive as a structured planning approach, but the case does not by itself demonstrate sustained operational, security and governance outcomes across different public-sector environments.

### Peer Feedback on Unit 2

Stelios Sotiriadis highlighted two aspects of my discussion: the relationship between ROCCA's cloud-specific stages and TOGAF's business, data, application and technology architecture stages, and the logic of beginning migration with lower-risk services.

More importantly, his feedback reinforced the limitation I had already identified. He noted that the case demonstrates planning and roadmap value more clearly than long-term migration, security and governance outcomes. This sharpened my interpretation of the evidence. I had initially treated limited generalisability mainly as a research limitation; the feedback helped me see its practical consequence: a coherent planning model should not be treated as proof of long-term operational success.

<img src="{{ '/assets/images/COM/unit23/unit-2-post-to-me.png' | relative_url }}" alt="Peer feedback on the Unit 2 ROCCA and TOGAF discussion" width="800">

*Figure 1. Peer feedback on the Unit 2 ROCCA and TOGAF discussion.*

## Unit 3: Terraform as a Cloud Design Tool

Terraform is a strong cloud design tool for organisations that require repeatable infrastructure provisioning across multiple cloud environments. Infrastructure as Code treats infrastructure definitions as software artefacts, allowing them to be versioned, reviewed and automated rather than configured manually (Quattrocchi and Tamburri, 2023). Terraform is particularly suitable for provisioning because it uses declarative configuration and maintains infrastructure state (Özdoğan, Ceran and Üstündağ, 2023).

Its main advantage is multi-cloud flexibility. Özdoğan, Ceran and Üstündağ (2023) identify Terraform as supporting AWS, Microsoft Azure and Google Cloud, whereas CloudFormation is specific to AWS. This makes Terraform attractive where one provisioning approach is required across heterogeneous cloud environments. However, this advantage is contextual rather than universal because provider-specific tools may offer stronger native integration in environments centred on a single platform.

Terraform also provides reusable modules and state-aware infrastructure management, supporting reuse and the tracking of infrastructure changes (Özdoğan, Ceran and Üstündağ, 2023). Regvart, Vlahović and Balković (2026) add empirical evidence by comparing Terraform, Pulumi and CloudFormation across 30 controlled AWS deployment repetitions. Terraform and Pulumi achieved comparable deployment performance, while CloudFormation required more than twice the average provisioning time under the tested conditions.

This result strengthens the case for Terraform in the specific experiment, but it should not be treated as a universal performance conclusion. The same study emphasises trade-offs between modular design, programmatic flexibility and native cloud integration. Tool selection therefore depends on the deployment context rather than a single performance result.

Cost and operational purpose also affect suitability. Feitosa et al. (2024) show that cost awareness is reflected in Terraform-based IaC artefacts and deployment decisions. Nevertheless, Ansible may be more suitable where configuration management or orchestration is the primary objective, while CloudFormation may remain more appropriate in AWS-centred environments because it is designed specifically for the AWS ecosystem (Özdoğan, Ceran and Üstündağ, 2023).

Overall, Terraform is strongest in this discussion when the requirement is multi-cloud provisioning combined with declarative management, reusable configuration and state awareness. Its suitability becomes less clear when native cloud integration, configuration management or organisational capacity is the dominant concern.

## Peer Discussion and Development of My Thinking

The peer responses to the Terraform discussion added three distinct perspectives that extended the original comparison.

### Payman Ghorbani: State Management and Collaboration

Payman agreed that multi-cloud capability is a major Terraform advantage, but he focused on the management implications of Terraform state in collaborative environments. He highlighted remote state, access control and state locking when several people work on the same infrastructure.

This changed how I interpreted state awareness. My original discussion treated it mainly as a technical strength for tracking infrastructure. The feedback showed that state is also a governance issue: the same mechanism that supports consistency and repeatability requires disciplined controls when infrastructure is managed collaboratively.

<img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Peer feedback from Payman Ghorbani on Terraform state management" width="800">

*Figure 2. Peer feedback from Payman Ghorbani on Terraform state management.*

### Joseph Omondi Nyambok: Operational Overhead and Organisational Constraints

Joseph shifted the discussion from technical capability to organisational capacity. He identified operational and cognitive overhead, licensing uncertainty and platform risk, and blast-radius and maintenance overhead. He also noted that state locking, remote backends, module sprawl and dependency resolution can require dedicated expertise, particularly in resource-constrained organisations.

This widened my evaluation because multi-cloud capability alone does not establish suitability. A tool may be technically capable yet still impose management demands that an organisation is not prepared to support. The feedback therefore added operational maturity and available expertise as factors that should be considered alongside technical features.

<img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Peer feedback from Joseph Omondi Nyambok on Terraform limitations" width="800">

*Figure 3. Peer feedback from Joseph Omondi Nyambok on Terraform limitations.*

### Stelios Sotiriadis: Context-Specific Tool Selection

Stelios highlighted that the discussion did not present Terraform as universally superior. He noted that multi-cloud provisioning, reusable modules and state awareness are strengths, while AWS-native or configuration-management scenarios may justify different tools. He also reinforced the importance of disciplined remote state, locking and access control.

His feedback strengthened the contextual conclusion of my analysis. The key question is not which tool is best in isolation, but which tool is most appropriate for a particular environment, workload and management model.

<img src="{{ '/assets/images/COM/unit23/unit3post3.png' | relative_url }}" alt="Peer feedback from Stelios Sotiriadis on Terraform and context-specific tool selection" width="800">

*Figure 4. Peer feedback from Stelios Sotiriadis on Terraform and context-specific tool selection.*

## Synthesis of Peer Learning

The peer discussion changed my approach in two main ways. First, it made me more cautious about the strength of evidence. In Unit 2, a well-structured adoption roadmap did not automatically demonstrate long-term implementation success. Second, it made me more attentive to operational context. In Unit 3, technical strengths such as state awareness and multi-cloud provisioning also introduced governance, expertise and maintenance requirements.

| Discussion | Initial Focus | Peer Contribution | Development in My Thinking |
|---|---|---|---|
| Unit 2 – ROCCA and TOGAF | Framework integration, phased migration and case-study limitations | Stronger distinction between planning value and evidence of long-term outcomes | I became more careful about separating a coherent design from validated operational success |
| Unit 3 – Payman | State awareness as a technical strength | Remote state, access control and locking | I recognised state management as both a technical and governance responsibility |
| Unit 3 – Joseph | Multi-cloud flexibility, reuse and provisioning | Operational overhead, licensing risk and maintenance complexity | I added organisational capacity and operational maturity to the evaluation |
| Unit 3 – Stelios | Contextual comparison of IaC tools | Reinforcement of context-specific selection | I strengthened the conclusion that suitability depends on environment and management requirements |

## Connection to Module Learning

Together, the two units connected cloud architecture with implementation decisions. Unit 2 showed how adoption can be structured through architecture and planning frameworks, while Unit 3 showed how IaC tools can translate infrastructure decisions into repeatable provisioning. The peer discussion strengthened this connection by showing that both frameworks and tools must be evaluated in relation to evidence, organisational context and operational responsibilities.

## Critical Reflection

### What?

I evaluated two related areas of cloud design: structured cloud adoption through ROCCA and TOGAF, and infrastructure provisioning through Terraform. I also engaged with peer feedback that questioned or extended parts of my original reasoning.

### So What?

The main development in my thinking was moving from feature-based comparison towards contextual evaluation. In Unit 2, I learned to distinguish between evidence that a framework supports planning and evidence that it produces successful long-term outcomes. In Unit 3, I learned that technical strengths such as multi-cloud support and state awareness cannot be separated from governance, expertise and maintenance requirements.

This process strengthened my critical evaluation because I became less likely to treat a framework or tool as effective solely because its design is logical or its technical capabilities are strong. I also developed my academic discussion skills by using peer comments as evidence to test my assumptions rather than treating them as simple agreement or disagreement.

### Now What?

In future cloud evaluations, I will structure my analysis around three questions: what the technology or framework can do, what evidence supports its effectiveness, and what organisational conditions are required for it to work successfully. I will also use peer discussion more deliberately to identify limitations and alternative interpretations before reaching a conclusion.

## References

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud Computing Adoption Strategic Planning Using ROCCA and TOGAF 9.2: A Study in Government Agency’, *Procedia Computer Science*, 161, pp. 1316–1324.

Feitosa, D., Penca, M.T., Berardi, M., Boza, R.-D. and Andrikopoulos, V. (2024) ‘Mining for cost awareness in the infrastructure as code artifacts of cloud-based applications: An exploratory study’, *Journal of Systems and Software*, 215, 112112. https://doi.org/10.1016/j.jss.2024.112112.

Jager, E. (2025) *Mastering the TOGAF® Standard: A Practical Translation of the World’s Leading Architecture Framework*. 1st edn. Berkeley, CA: Apress.

Özdoğan, E., Ceran, O. and Üstündağ, M.T. (2023) ‘Systematic analysis of Infrastructure as Code technologies’, *Gazi University Journal of Science Part A: Engineering and Innovation*, 10(4), pp. 452–471. https://doi.org/10.54287/gujsa.1373305.

Quattrocchi, G. and Tamburri, D.A. (2023) ‘Infrastructure as Code’, *IEEE Software*, 40(1), pp. 37–40. https://doi.org/10.1109/MS.2022.3212034.

Regvart, D., Vlahović, I. and Balković, M. (2026) ‘A controlled comparative evaluation of Infrastructure as Code tools: Deployment performance and maintainability across Terraform, Pulumi, and AWS CloudFormation’, *Applied Sciences*, 16(6), 2971. https://doi.org/10.3390/app16062971.
