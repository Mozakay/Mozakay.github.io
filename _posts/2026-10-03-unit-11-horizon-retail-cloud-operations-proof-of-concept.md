---
layout: post
title: "Unit 11: Horizon Retail Group Cloud Operations Proof of Concept"
categories: ["Cloud Operations and Management"]
unit: 11
journey_group: "unit-11-part-2"
---

## Introduction

This practical activity demonstrates a cloud operations proof of concept (PoC) for Horizon Retail Group, a hypothetical multi-channel retailer with approximately 150 stores and a growing e-commerce channel. The practical implementation focused on a validated operational chain:

**Terraform → Azure Infrastructure → Ansible → Nginx → Azure Monitor**

The PoC was intentionally limited to technical validation rather than production deployment. The wider hybrid-cloud architecture shown below represents the recommended production direction and clearly separates implemented capabilities from proposed services.

![Figure 1. Horizon Retail hybrid cloud architecture](/assets/images/COM/unit12/part1/01-hybrid-architecture.png)

*Figure 1. Horizon Retail hybrid cloud architecture showing the validated PoC and proposed production design.*

## Terraform Infrastructure as Code

Terraform was used to provision and manage the Azure infrastructure declaratively. The configuration defined the Horizon Retail Linux virtual machine, network-interface association and SSH configuration, while the Terraform state confirmed management of the reused subnet, virtual machine, NIC, NSG association, public IP address and resource group.

![Figure 2. Terraform Infrastructure as Code](/assets/images/COM/unit11/part1/02-terraform-iac.png)

*Figure 2. Terraform Infrastructure as Code definition and managed Azure resources.*

This demonstrates repeatable infrastructure provisioning rather than reliance on manual portal configuration. However, the PoC also showed that Infrastructure as Code does not remove provider-side constraints such as regional capacity, quotas or service availability.

## Azure Infrastructure Validation

The deployed Azure environment included the Horizon Retail virtual machine, managed operating-system disk, network interface, public IP address and Network Security Group.

![Figure 3. Azure resources](/assets/images/COM/unit11/part1/03-azure-resources.png)

*Figure 3. Azure infrastructure visualiser showing the Horizon Retail VM and supporting resources.*

The PoC reused an existing subnet because of Azure for Students constraints. This was appropriate for technical validation, but a production environment should use dedicated networking, resource grouping and access boundaries.

## Automated Configuration with Ansible

Ansible was used after provisioning to configure the operating system and web service. The playbook updated the package cache, installed Nginx, confirmed that the service was running and deployed the Horizon Retail test page.

![Figure 4. Ansible configuration](/assets/images/COM/unit11/part1/04-ansible-config.png)

*Figure 4. Successful automated configuration of the Horizon Retail VM using Ansible.*

The final execution completed successfully with **ok=5**, **changed=3**, **unreachable=0** and **failed=0**, confirming that the configuration workflow operated successfully.

## Operational Verification

The deployed Nginx service was accessed through the Azure VM public IP address, confirming that the Terraform-provisioned infrastructure and Ansible configuration worked together correctly.

![Figure 5. Web service verification](/assets/images/COM/unit11/part1/05-web-verification.png)

*Figure 5. Operational verification of the Horizon Retail web service.*

The browser displayed **Not secure** because the PoC used HTTP for validation. This evidence confirms successful connectivity and deployment, but it should not be interpreted as production security readiness.

## Monitoring with Azure Monitor

Azure Monitor was used to validate operational telemetry for the virtual machine. The displayed 30-minute interval recorded approximately **2.93% average CPU utilisation**.

![Figure 6. Azure Monitor CPU utilisation](/assets/images/COM/unit11/part1/06-azure-monitor.png)

*Figure 6. Azure Monitor CPU utilisation for the Horizon Retail virtual machine.*

The result confirms that telemetry was collected successfully. It does not demonstrate production capacity because the PoC was not exposed to representative demand from approximately 150 stores or an active e-commerce platform.

## Reflection on Cloud Operations and Resilience

The practical work demonstrated that Terraform and Ansible perform complementary roles in cloud operations. Terraform provided repeatable infrastructure provisioning, while Ansible automated operating-system and application configuration. Together, they created a reproducible workflow from infrastructure creation to service deployment. This aligns with Infrastructure as Code research that emphasises repeatability, versioning and controlled infrastructure change (Rahman, Mahdavi-Hezaveh and Williams, 2019; Kumara et al., 2021).

A key lesson from the PoC was that successful automation does not remove operational constraints. Reusing an existing subnet allowed the practical work to continue, but it also demonstrated that quotas, regional capacity and provider limitations must be considered before automated production deployment. The Standard_B1s VM was suitable for validation only and should not be treated as evidence of enterprise-scale capacity.

The monitoring evidence also required careful interpretation. The low CPU result confirmed Azure Monitor telemetry collection, but it was not sufficient for production sizing or autoscaling decisions because the workload was not representative. Production assessment would need to consider CPU together with latency, memory, storage, availability and transaction volumes under realistic demand.

The PoC further highlighted the distinction between deployment success and production resilience. Public HTTP and administrative SSH were acceptable for controlled testing, but a production design would require stronger controls such as HTTPS/TLS, WAF protection, private endpoints, identity controls and restricted administrative access. Resilience would also require a scalable application tier, backup and recovery mechanisms, and workload-specific recovery objectives.

The wider architecture therefore adopts a hybrid-cloud strategy: selected store-level functions remain local to support continuity during WAN disruption, while Azure provides central applications, automation, monitoring, data services and analytics. The hybrid production architecture remains a recommendation rather than an implemented component of the PoC. This distinction is important because the practical evidence validates the operational mechanism, not complete enterprise readiness.

## Conclusion

The PoC successfully validated an automated cloud operations chain combining Infrastructure as Code, Azure infrastructure, configuration management, web-service deployment and operational monitoring. The main outcome was not the small virtual machine itself, but evidence that a repeatable operational workflow could be implemented and then critically extended into a more resilient hybrid-cloud production design.

## References

Kumara, I., Garriga, M., Romeu, A.U., Di Nucci, D., Palomba, F., Tamburri, D.A. and van den Heuvel, W.-J. (2021) ‘The do’s and don’ts of infrastructure code: A systematic gray literature review’, *Information and Software Technology*, 137, Article 106593. doi: 10.1016/j.infsof.2021.106593.

Rahman, A., Mahdavi-Hezaveh, R. and Williams, L. (2019) ‘A systematic mapping study of infrastructure as code research’, *Information and Software Technology*, 108, pp. 65–77. doi: 10.1016/j.infsof.2018.12.004.
