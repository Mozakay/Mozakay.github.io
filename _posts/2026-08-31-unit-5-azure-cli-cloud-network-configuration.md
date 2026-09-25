---
layout: post
title: "Unit 5: Azure CLI Cloud Network Configuration"
categories: ["Cloud Operations and Management"]
unit: 5
journey_group: "unit-5"
---

## Introduction

Cloud computing changes infrastructure from fixed physical assets into programmable resources that can be provisioned on demand. This model supports rapid resource allocation, elasticity and service-based consumption rather than requiring organisations to purchase and manually configure all underlying infrastructure. Buyya *et al.* (2009) describe this evolution through the concept of computing as a utility, while Armbrust *et al.* (2010) emphasise elasticity and the ability to obtain computing resources dynamically.

For this activity, Microsoft Azure CLI was used through Azure Cloud Shell to create and verify a small cloud network configuration. The implementation consisted of an Azure Resource Group, a Virtual Network (VNet) and a subnet deployed in the Qatar Central region. The exercise was designed to demonstrate fundamental cloud concepts, practical Infrastructure as a Service configuration and the use of command-line tooling for repeatable cloud deployment.

## Azure CLI Configuration

The following Azure CLI commands were used to create the resource group, virtual network and subnet, and then verify the deployed configuration:

```bash
az group create \
  --name unit5-rg \
  --location qatarcentral

az network vnet create \
  --resource-group unit5-rg \
  --name unit5-vnet \
  --location qatarcentral \
  --address-prefix 10.0.0.0/16 \
  --subnet-name unit5-subnet \
  --subnet-prefix 10.0.1.0/24

az network vnet show \
  --resource-group unit5-rg \
  --name unit5-vnet \
  --query "{VNet:name,Location:location,AddressSpace:addressSpace.addressPrefixes[0],ProvisioningState:provisioningState,Subnet:subnets[0].name,SubnetPrefix:subnets[0].addressPrefix}" \
  --output table
```

## Implementation and Evidence

The resource group `unit5-rg` was created in `qatarcentral`. Within it, `unit5-vnet` was configured with the private address space `10.0.0.0/16`, containing `unit5-subnet` with the more specific `10.0.1.0/24` prefix. Figure 1 provides evidence that the VNet provisioning command completed successfully.

<figure>
  <img src="{{ '/assets/images/COM/unit5/figure1-vnet-creation.png' | relative_url }}" alt="Figure 1. Successful creation of an Azure Virtual Network and subnet using Azure CLI." width="650">
  <figcaption><em>Figure 1. Successful creation of an Azure Virtual Network and subnet using Azure CLI.</em></figcaption>
</figure>

The exercise demonstrates a fundamental Infrastructure as a Service principle: networking infrastructure can be logically defined without directly configuring physical switches, routers or cabling. The VNet establishes a logical network boundary, while subnetting provides segmentation within the allocated address space. Cloud abstraction therefore simplifies infrastructure deployment but does not remove the requirement to understand conventional networking concepts such as CIDR addressing, segmentation and resource dependencies.

A significant advantage of the CLI approach was **repeatability**. Unlike manual portal configuration, command-based deployment can be reproduced, reviewed and incorporated into automation workflows. This improves consistency and reduces repetitive administrative activity. However, automation also introduces an important limitation: a command can be syntactically correct and successfully executed while still representing a poor architectural decision. An inappropriate CIDR range, region or subnet design could therefore be deployed consistently at scale. Successful provisioning should consequently not be interpreted as proof of secure or optimal design.

Validation was therefore treated as a separate step rather than relying only on the initial provisioning response. The `az network vnet show` command was used to interrogate the deployed resource. Figure 2 confirms that `unit5-vnet` was deployed in Qatar Central with the intended `10.0.0.0/16` address space, that `unit5-subnet` used `10.0.1.0/24`, and that the provisioning state was `Succeeded`.

<figure>
  <img src="{{ '/assets/images/COM/unit5/figure2-vnet-verification.png' | relative_url }}" alt="Figure 2. Verification of the Azure Virtual Network and subnet configuration using Azure CLI." width="650">
  <figcaption><em>Figure 2. Verification of the Azure Virtual Network and subnet configuration using Azure CLI.</em></figcaption>
</figure>

## Critical Evaluation and Challenges

The main challenge was not merely creating the resources, but ensuring parameter accuracy and verifying the resulting state. CLI deployment depends on precise resource names, regions and address prefixes; minor errors can cause failed commands or unintended configurations. This is particularly significant because cloud security problems can arise from configuration and management weaknesses even when the underlying cloud service operates correctly (Hashizume *et al.*, 2013).

The practical work also demonstrated that cloud automation transfers responsibility rather than eliminating it. Azure abstracts physical infrastructure and provides programmable interfaces, but the user remains responsible for logical design choices. In this case, the chosen address ranges were sufficient for a small isolated exercise, but a production network would require additional consideration of address-space overlap, routing, Network Security Groups, service endpoints, private connectivity and governance controls.

## Learning Outcomes

The activity addressed the Unit 5 learning outcomes by connecting cloud theory with a working Azure implementation. Fundamental cloud concepts were demonstrated through on-demand provisioning and infrastructure abstraction. Azure Virtual Network represented a practical cloud networking solution, while Azure CLI provided a management and configuration tool for implementing infrastructure programmatically. The exercise also demonstrated that successful cloud implementation requires both technical execution and validation rather than assuming that successful provisioning alone confirms architectural quality.

## Conclusion

Overall, the activity demonstrated how a small Azure network can be created and verified through command-line configuration. The use of Azure CLI provided a repeatable and auditable method of deployment, while the validation step confirmed that the intended network and subnet settings were actually applied. More importantly, the exercise showed that cloud abstraction and automation improve deployment efficiency but do not replace sound networking knowledge, security awareness or architectural judgement.

## References

Armbrust, M., Fox, A., Griffith, R., Joseph, A.D., Katz, R., Konwinski, A., Lee, G., Patterson, D., Rabkin, A., Stoica, I. and Zaharia, M. (2010) ‘A view of cloud computing’, *Communications of the ACM*, 53(4), pp. 50–58. doi: 10.1145/1721654.1721672.

Buyya, R., Yeo, C.S., Venugopal, S., Broberg, J. and Brandic, I. (2009) ‘Cloud computing and emerging IT platforms: Vision, hype, and reality for delivering computing as the 5th utility’, *Future Generation Computer Systems*, 25(6), pp. 599–616. doi: 10.1016/j.future.2008.12.001.

Hashizume, K., Rosado, D.G., Fernández-Medina, E. and Fernandez, E.B. (2013) ‘An analysis of security issues for cloud computing’, *Journal of Internet Services and Applications*, 4, Article 5. doi: 10.1186/1869-0238-4-5.

Microsoft (2026) *az network vnet*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/cli/azure/network/vnet (Accessed: 25 September 2026).
