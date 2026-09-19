---
layout: post
title: "Units 2–3: Cloud Architecture, Frameworks and Design"
categories: ["Cloud Operations and Management"]
journey_group: "units-2-3"
---

## Context and Purpose

Units 2 and 3 developed my understanding of cloud architecture, cloud adoption frameworks and Infrastructure as Code (IaC). The two discussion activities required me to move beyond describing cloud technologies and instead evaluate how organisations can structure cloud adoption and select appropriate design tools.

In Unit 2, I examined the integration of the Roadmap for Cloud Computing Adoption (ROCCA) with TOGAF 9.2 in a government-agency context. In Unit 3, I evaluated Terraform as a cloud design and provisioning tool and compared its strengths and limitations with alternative Infrastructure as Code approaches.

The discussions were also important because peer feedback challenged and extended my original analysis. Rather than treating the discussion posts as finished answers, I used the comments from classmates to reconsider assumptions, identify additional limitations and develop a more balanced understanding of cloud architecture and IaC decision-making.

## Unit 2: ROCCA and TOGAF Implementation in Government Agencies

Anggraini, Binariswanto and Legowo (2019) examine how the Roadmap for Cloud Computing Adoption (ROCCA) can be integrated with TOGAF 9.2 to guide cloud adoption in government agencies. Their argument is significant because public-sector cloud migration is not only a technical decision; it must also reflect organisational objectives, regulatory obligations, stakeholder expectations and existing capabilities.

ROCCA supplies a cloud-specific roadmap covering analysis, planning, adoption, migration and management, whereas TOGAF provides the enterprise architecture structure needed to align business, data, application and technology decisions.

The article applies the combined approach to SKK Migas, an Indonesian government agency facing growing data volumes, limited data-centre capacity, budget pressures and operational constraints. Mapping ROCCA activities to the TOGAF Architecture Development Method enabled the agency to assess its current position, identify stakeholders, define target architectures and prepare an implementation roadmap.

The proposed strategy adopted a phased hybrid-cloud model, beginning with lower-risk supporting applications before considering more critical services. This is appropriate for government agencies because gradual migration allows security, procurement, compliance and service performance to be evaluated before wider implementation.

The integration provides several benefits. ROCCA ensures that cloud-specific issues are considered, while TOGAF links these decisions to enterprise strategy and produces documented architectural outputs. This can reduce fragmented technology decisions and strengthen business–IT alignment. Jager (2025) similarly explains that TOGAF should be adapted to organisational circumstances rather than treated as a rigid method.

However, the study provides stronger evidence for analysis and planning than for full migration and long-term cloud management. It is also based on one agency and limited managerial evaluation, reducing the generalisability of its findings. Overall, ROCCA and TOGAF offer a coherent approach to government cloud adoption, but further implementation across different public organisations is necessary to demonstrate sustained operational, security and governance outcomes under varied legal, institutional, financial and technological conditions.

### Peer Feedback on Unit 2

A classmate, Stelios Sotiriadis, responded positively to the balance of the analysis and specifically highlighted the relationship between ROCCA's cloud-specific stages and TOGAF's business, data, application and technology architecture stages. He also identified the phased hybrid-cloud approach for SKK Migas as a strong part of the discussion because it explained why lower-risk services can be a sensible starting point for public-sector migration.

More importantly, his feedback reinforced the limitation I had identified in the original discussion. He noted that the case demonstrates planning and roadmap value more clearly than long-term migration, security and governance outcomes, and that broader evidence would be needed before generalising the model.

This feedback developed my thinking because it made me distinguish more clearly between a framework that is logically well structured and one that has been fully validated through long-term implementation. My original discussion already identified the study's limited generalisability, but the peer response helped me recognise why this limitation matters in practical evaluation: a successful planning framework does not automatically demonstrate sustained operational success.

<img src="{{ '/assets/images/COM/unit23/unit-2-post-to-me.png' | relative_url }}" alt="Peer feedback on the Unit 2 ROCCA and TOGAF discussion" width="800">

*Figure 1. Peer feedback on the Unit 2 ROCCA and TOGAF discussion.*

## Unit 3: Terraform as a Cloud Design Tool

Terraform is a strong cloud design tool for organisations that require repeatable infrastructure provisioning across multiple cloud environments. Infrastructure as Code (IaC) treats infrastructure definitions as software artefacts, allowing them to be versioned, reviewed and automated rather than configured manually (Quattrocchi and Tamburri, 2023). Within this approach, Terraform is particularly suitable for provisioning because it uses declarative configuration and maintains infrastructure state (Özdoğan, Ceran and Üstündağ, 2023).

Its principal advantage is multi-cloud flexibility. Özdoğan, Ceran and Üstündağ (2023) identify Terraform as supporting AWS, Microsoft Azure and Google Cloud, whereas CloudFormation is specific to AWS. Their systematic analysis also recommends both Terraform and CloudFormation for provisioning, but highlights differences in cloud integration, architecture and data representation. Consequently, Terraform is more appropriate where an organisation requires one provisioning approach across heterogeneous cloud environments rather than a provider-specific solution.

Terraform also offers reusable modules and state-aware infrastructure management, supporting reuse and the tracking of infrastructure changes (Özdoğan, Ceran and Üstündağ, 2023). Empirical evidence further strengthens the comparison. Regvart, Vlahović and Balković (2026) conducted 30 controlled deployment repetitions using Terraform, Pulumi and CloudFormation in an AWS environment. Terraform and Pulumi achieved comparable deployment performance, whereas CloudFormation required more than twice the average provisioning time under the specific experimental conditions.

However, the authors also emphasise trade-offs between modular design, programmatic flexibility and native cloud integration, indicating that no tool is universally superior.

Cost considerations also remain relevant. Feitosa et al. (2024) demonstrate that cost awareness is reflected in Terraform-based IaC artefacts and deployment decisions. Nevertheless, Ansible may be more suitable where configuration management or orchestration is the primary objective, while CloudFormation may remain more appropriate in AWS-centred environments because it is specifically designed for the AWS ecosystem (Özdoğan, Ceran and Üstündağ, 2023).

Overall, Terraform is most convincingly superior for multi-cloud provisioning because it combines provider flexibility, declarative infrastructure management, reusable configuration and state awareness, while retaining clear contextual limitations across deployment environments.

## Peer Discussion and Development of My Thinking

The peer discussion around Terraform developed my understanding beyond the original comparison of provisioning capability, flexibility and deployment performance. Three classmates raised different issues, and each comment added a different perspective to the analysis.

### Payman Ghorbani: State Management and Collaboration

Payman agreed that Terraform's multi-cloud capability is one of its strongest advantages, particularly for organisations that do not want their infrastructure approach tied closely to one cloud provider. He also agreed with the importance of presenting Terraform's limitations rather than treating it as the best option in every situation.

His main contribution was to focus on Terraform state in collaborative environments. He highlighted the need for careful management when several people work on the same infrastructure, including remote state, access control and state locking.

This expanded my thinking because my original discussion treated state awareness mainly as a technical strength that supports infrastructure tracking. The feedback showed me that the same feature also creates management responsibilities. I therefore developed a more balanced understanding: state awareness supports consistency and repeatability, but in team environments it also requires disciplined controls and shared management practices.

<img src="{{ '/assets/images/COM/unit23/unit3post1.png' | relative_url }}" alt="Peer feedback from Payman Ghorbani on Terraform state management" width="800">

*Figure 2. Peer feedback from Payman Ghorbani on Terraform state management.*

### Joseph Omondi Nyambok: Operational Overhead and Organisational Constraints

Joseph agreed with Terraform's role in multi-cloud provisioning and standardised IaC deployment, but he introduced several drawbacks that are particularly relevant to small-to-medium enterprises and resource-constrained organisations.

His feedback identified three areas: operational and cognitive overhead, licensing uncertainty and platform risk, and blast-radius and maintenance overhead. He explained that Terraform can require dedicated expertise for state locking, remote backends, module sprawl and dependency resolution. He also raised the effect of licensing changes and the possibility that organisations may need to evaluate alternatives such as OpenTofu. Finally, he highlighted how large state files or poorly optimised configurations can increase deployment and maintenance complexity.

This feedback widened my analysis because it moved the discussion beyond whether Terraform is technically capable of multi-cloud provisioning. It made me consider whether an organisation has the skills, resources and operational maturity needed to manage the tool effectively. The comment therefore helped me see that tool selection must consider organisational capacity as well as technical capability.

<img src="{{ '/assets/images/COM/unit23/unit3post2.png' | relative_url }}" alt="Peer feedback from Joseph Omondi Nyambok on Terraform limitations" width="800">

*Figure 3. Peer feedback from Joseph Omondi Nyambok on Terraform limitations.*

### Stelios Sotiriadis: Context-Specific Tool Selection

Stelios highlighted that the original Terraform discussion combined the conceptual IaC argument with empirical comparison across Terraform, Pulumi and CloudFormation. He particularly noted that the discussion did not present Terraform as universally superior. Instead, it identified multi-cloud provisioning, reusable modules and state awareness as strengths while recognising that AWS-native or configuration-management cases may be better served by other tools.

He also reinforced the discussion around state files, noting that Terraform's effectiveness in team environments depends on disciplined remote state, locking and access control.

This feedback strengthened the conclusion of my original analysis. It confirmed that the most useful evaluation is not to identify one tool as the best in every case, but to understand the conditions under which each tool is appropriate. It also connected Payman's state-management point with the wider issue of governance and disciplined team practice.

<img src="{{ '/assets/images/COM/unit23/unit3post3.png' | relative_url }}" alt="Peer feedback from Stelios Sotiriadis on Terraform and context-specific tool selection" width="800">

*Figure 4. Peer feedback from Stelios Sotiriadis on Terraform and context-specific tool selection.*

## How the Peer Discussion Changed My Approach

The discussion with classmates changed the way I evaluated both cloud architecture frameworks and IaC tools. In Unit 2, the peer feedback encouraged me to separate evidence of good planning from evidence of successful long-term implementation. In Unit 3, the comments encouraged me to separate Terraform's technical strengths from the organisational responsibilities required to use those strengths effectively.

| Discussion | What I Initially Focused On | What Peer Feedback Added | How My Thinking Developed |
|---|---|---|---|
| Unit 2 – ROCCA and TOGAF | Integration of cloud-specific planning with enterprise architecture, phased hybrid-cloud adoption and limitations of the SKK Migas case | The distinction between planning and roadmap value and evidence of long-term migration, security and governance outcomes | I became more careful about distinguishing a strong framework design from proven long-term implementation |
| Unit 3 – Payman | Terraform state awareness as a strength for tracking infrastructure | Remote state, access control and state locking in collaborative environments | I recognised that state management is both a technical capability and a governance responsibility |
| Unit 3 – Joseph | Multi-cloud flexibility, reuse, provisioning and performance | Operational and cognitive overhead, licensing uncertainty, platform risk and maintenance overhead | I broadened the evaluation from technical features to organisational resources and operational capability |
| Unit 3 – Stelios | Contextual comparison between Terraform, Pulumi, CloudFormation and Ansible | Reinforcement of context-specific tool selection and disciplined state management | I strengthened the view that tool selection should depend on workload, environment and management requirements rather than a universal ranking |

The peer discussion therefore became part of the learning process rather than simply feedback on a completed post. Reading the responses required me to revisit my own arguments, compare them with the additional concerns raised by classmates and identify where my original evaluation could become more precise.

## Connection to Module Learning

These two units developed my ability to connect cloud architecture with practical implementation decisions. Unit 2 showed how cloud adoption can be structured through architecture and planning frameworks, while Unit 3 showed how IaC tools can translate infrastructure decisions into repeatable and automated provisioning.

The peer discussion also strengthened my critical evaluation. Rather than focusing only on the advantages of a framework or tool, I became more attentive to limitations, organisational context, governance responsibilities and the strength of the evidence supporting a conclusion.

## Critical Reflection

### What?

I analysed two different aspects of cloud design. The first focused on ROCCA and TOGAF as a structured approach to government cloud adoption. The second evaluated Terraform as an Infrastructure as Code tool for multi-cloud provisioning.

I also participated in peer discussion by presenting my analysis and then reviewing feedback from classmates who challenged or extended different parts of my argument. This required me to compare different technical perspectives, evaluate the strengths and limitations of the approaches discussed, and reconsider some of my original assumptions.

### So What?

The most important development was learning that a technically strong solution still needs to be evaluated within its organisational and operational context. This strengthened my ability to critically evaluate cloud adoption frameworks and Infrastructure as Code tools rather than focusing only on their technical advantages.

The Unit 2 feedback made me more aware that planning success and long-term implementation success are not the same thing. This improved my ability to compare cloud technologies within specific organisational contexts and to evaluate the strength of the evidence supporting a conclusion.

The Unit 3 feedback made me more aware that Terraform's strengths, particularly state awareness and multi-cloud provisioning, also introduce responsibilities around collaboration, management and operational capability. The different peer comments were useful because they did not simply repeat the same point. Payman focused on collaborative state management, Joseph introduced operational, licensing and maintenance concerns, and Stelios reinforced context-specific tool selection.

Engaging with these different perspectives developed my academic discussion skills and helped me understand the value of peer feedback in technical decision-making. Rather than treating alternative views as separate comments, I used them to refine my own analysis and develop a more balanced evaluation of cloud technologies.

### Now What?

In future cloud evaluations, I will make a clearer distinction between technical capability, organisational suitability and evidence of long-term effectiveness. I will also continue to evaluate both strengths and limitations rather than relying on a single technical advantage when comparing cloud technologies.

I will use peer discussion more deliberately as a way of testing my assumptions, identifying issues that I may not have considered initially, and improving the quality of my technical judgement. This experience showed me that reflection on alternative perspectives can strengthen both critical analysis and professional decision-making.

## References

Anggraini, N., Binariswanto and Legowo, N. (2019) ‘Cloud Computing Adoption Strategic Planning Using ROCCA and TOGAF 9.2: A Study in Government Agency’, *Procedia Computer Science*, 161, pp. 1316–1324.

Feitosa, D., Penca, M.T., Berardi, M., Boza, R.-D. and Andrikopoulos, V. (2024) ‘Mining for cost awareness in the infrastructure as code artifacts of cloud-based applications: An exploratory study’, *Journal of Systems and Software*, 215, 112112. https://doi.org/10.1016/j.jss.2024.112112.

Jager, E. (2025) *Mastering the TOGAF® Standard: A Practical Translation of the World’s Leading Architecture Framework*. 1st edn. Berkeley, CA: Apress.

Özdoğan, E., Ceran, O. and Üstündağ, M.T. (2023) ‘Systematic analysis of Infrastructure as Code technologies’, *Gazi University Journal of Science Part A: Engineering and Innovation*, 10(4), pp. 452–471. https://doi.org/10.54287/gujsa.1373305.

Quattrocchi, G. and Tamburri, D.A. (2023) ‘Infrastructure as Code’, *IEEE Software*, 40(1), pp. 37–40. https://doi.org/10.1109/MS.2022.3212034.

Regvart, D., Vlahović, I. and Balković, M. (2026) ‘A controlled comparative evaluation of Infrastructure as Code tools: Deployment performance and maintainability across Terraform, Pulumi, and AWS CloudFormation’, *Applied Sciences*, 16(6), 2971. https://doi.org/10.3390/app16062971.

