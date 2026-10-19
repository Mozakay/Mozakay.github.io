---
layout: post
title: "Formative Activity: Bash Automation for Azure Cloud Operations"
categories: ["Cloud Operations and Management"]
unit: 4
journey_group: "unit-4"
---



## Bash Scripting for Automated Cloud Operations in Microsoft Azure

Bash scripting supports cloud infrastructure provisioning, system configuration and routine operational checks, reflecting the flexibility of virtualised resource allocation discussed by Buyya et al. (2009). This activity demonstrates Bash and Azure Command-Line Interface (CLI) operations on an Ubuntu virtual machine. The deployment uses resource group `unit4-rg-india`, virtual machine `unit4-vm`, the India South Central region and the `Standard_B1s` instance size. Figure 1 records successful virtual machine provisioning, while Figure 2 demonstrates an active Nginx service and a successful local HTTP response.

The Bash workflow checks Azure CLI availability and account authentication. Configuration variables identify the deployment region, resource group, machine name, operating system image and administrator. The provisioning commands create a resource group and virtual machine, while existence checks in the published script prevent unintended duplication. However, avoiding duplicate resources is not equivalent to full idempotency: existing configurations are not automatically reconciled against an intended state.

Azure Run Command subsequently executes shell commands within the virtual machine without requiring an interactive SSH connection (Microsoft, 2025). Commands update package information, install Nginx, enable its service and write a simple HTML page. Further commands retrieve the hostname, kernel version, disk usage and memory statistics. Service-status and HTTP checks then establish whether Nginx is active and returns the expected content. The positive response in Figure 2 demonstrates local application functionality, not external availability or sustained performance.

Automation offers operational benefits, but these require qualification. First, scripted commands improve procedural consistency compared with individually configured servers. Morris (2016) identifies repeatability and configuration drift as central infrastructure management concerns. Nevertheless, using unpinned operating system images or software repositories may produce different results over time. Second, automated deployment and configuration reduce repeated manual steps and provide a basis for pipeline integration. No execution-time comparison was measured here, so a quantified efficiency improvement cannot be claimed.

Third, explicit service checks help identify functional failures after infrastructure provisioning. Yet successful checks at one point cannot replace continuous monitoring, alerting, log retention, backup and recovery testing. Fourth, resource-group organisation facilitates management and cleanup, although stopping a virtual machine does not necessarily eliminate storage or networking charges. Financial control therefore requires regular review of resource consumption rather than assuming automation guarantees savings.

The evidence also distinguishes infrastructure state from application state: a running Azure VM alone would not confirm a functioning web server. Combining platform-level and application-level checks therefore provides stronger, though still necessarily limited, evidence of successful automation outcomes.

Security also constrains automation. The local HTTP test does not require a publicly exposed web endpoint, but it cannot establish that all network access rules are appropriately restricted. Cloud security literature emphasises risks involving access controls, service availability and shared responsibilities (Hashizume et al., 2013). Consequently, least-privilege permissions, protected credentials and network-rule reviews remain necessary. Bash is suitable for procedural automation, whereas Terraform and Azure Bicep support declarative provisioning and Ansible focuses on configuration management. Overall, the activity demonstrates a verifiable connection between Azure provisioning, system configuration and basic validation, while identifying the additional controls required for reliable, secure production operations.

## Bash script

The Bash source is available in the repository: [unit4-azure-vm.sh](/assets/code/COM/unit4/unit4-azure-vm.sh).

The published file defines the provisioning and configuration workflow, including checks for an existing VM and its power state, Azure Run Command configuration, and local HTTP validation.

## Execution evidence

**Figure 1. Successful automated provisioning of an Azure virtual machine using Bash and Azure CLI.**

![Azure CLI terminal showing execution of unit4-azure-vm.sh and VM running in India South Central](/assets/images/COM/unit4/Figure1.png)

**Figure 2. Successful Nginx service configuration and local HTTP verification on the Azure virtual machine.**

![Azure Cloud Shell output showing Nginx active and successful local HTTP response](/assets/images/COM/unit4/Figure2.png)

## References

Buyya, R., Yeo, C.S., Venugopal, S., Broberg, J. and Brandic, I. (2009) ‘Cloud computing and emerging IT platforms: Vision, hype, and reality for delivering computing as the 5th utility’, *Future Generation Computer Systems*, 25(6), pp. 599–616. https://doi.org/10.1016/j.future.2008.12.001

Hashizume, K., Rosado, D.G., Fernández-Medina, E. and Fernandez, E.B. (2013) ‘An analysis of security issues for cloud computing’, *Journal of Internet Services and Applications*, 4, Article 5. https://doi.org/10.1186/1869-0238-4-5

Microsoft (2025) *Run scripts in your Linux VM by using action Run Commands*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command (Accessed: 19 October 2026).

Morris, K. (2016) *Infrastructure as Code: Managing Servers in the Cloud*. Sebastopol, CA: O’Reilly Media.
