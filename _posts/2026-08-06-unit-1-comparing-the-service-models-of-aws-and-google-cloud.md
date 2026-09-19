---
layout: post
title: "Unit 1: Comparing the Service Models of AWS and Google Cloud"
categories: ["Cloud Operations and Management"]
unit: 1
journey_group: "unit-1"
---

## Context and Purpose

Cloud services are commonly classified as Infrastructure as a Service (IaaS), Platform as a Service (PaaS) and Software as a Service (SaaS). These models differ mainly in how responsibility is divided between provider and customer. IaaS gives customers the greatest control over computing resources, PaaS transfers more infrastructure and runtime management to the provider, and SaaS delivers a complete application with minimal technical administration for the user (Nadeem, 2022). Although AWS and Google Cloud offer services across these layers, their clearest differences appear in IaaS, managed platforms, serverless computing and data services.

## Technical Discussion and Comparison

### Infrastructure as a Service (IaaS)

At the IaaS level, Amazon EC2 and Google Compute Engine both provide virtual machines, storage and networking on demand. AWS offers a broad range of instance categories and supporting services, which can suit organisations operating heterogeneous workloads with different compute, memory, storage and accelerator requirements. Google Cloud also provides multiple machine families and connects its compute services with analytics, containers and machine-learning capabilities.

Alkhatib, Shaheen and Albustanji (2025) show that the providers differ across compute, storage, databases, networking and container services. This suggests that AWS flexibility is associated mainly with breadth of choice, whereas Google Cloud flexibility is associated with an integrated, data-oriented environment.

Performance also influences practical flexibility. Zboril and Svatá (2025) found that AWS achieved stronger results than GCP and Azure in their selected virtual-machine benchmarks. However, this finding applies only to the configurations tested and does not establish that AWS is always faster. Performance can vary according to machine type, region, software and workload; therefore, provider selection should be based on workload-specific requirements.

### PaaS and Serverless Computing

At the PaaS and serverless levels, both providers reduce the need to manage underlying infrastructure. This lowers operational effort but gives customers less direct control than IaaS (Nadeem, 2022).

Alkhatib, Shaheen and Albustanji (2025) identify application development, serverless computing and containers as important comparison areas. AWS may therefore suit teams needing to combine numerous specialised services within one architecture, while Google Cloud may suit teams prioritising cloud-native, containerised or data-intensive development. These are workload-based tendencies rather than exclusive strengths.

### Pricing

Both platforms use consumption-based pricing, but direct comparison is difficult because processing, storage, networking and additional services are billed differently. Ibrahimi (2017) identifies pricing structure as an important provider-selection factor and explains that AWS and Google Cloud apply different charging approaches.

A lower advertised compute price may therefore not produce the lowest total cost once storage, data transfer and dependent services are included. Cost evaluation should consider utilisation, workload duration and required performance rather than unit price alone.

### Data Warehousing

Data warehousing illustrates their different use cases. Borra (2024) describes Amazon Redshift as an enterprise data warehouse based on massively parallel processing, whereas BigQuery uses a serverless architecture that separates compute and storage.

BigQuery may suit organisations seeking large-scale SQL analytics without managing infrastructure, while Redshift may suit OLAP-focused workloads requiring integration with the AWS data environment.

## Comparison Summary

| Comparison Area | AWS | Google Cloud |
|---|---|---|
| IaaS | Amazon EC2 provides virtual machines, storage and networking on demand. AWS flexibility is associated mainly with breadth of instance categories and supporting services. | Google Compute Engine provides virtual machines, storage and networking on demand. Google Cloud flexibility is associated with an integrated, data-oriented environment. |
| PaaS and Serverless | May suit teams needing to combine numerous specialised services within one architecture. | May suit teams prioritising cloud-native, containerised or data-intensive development. |
| Pricing | Uses consumption-based pricing, with processing, storage, networking and additional services contributing to total cost. | Uses consumption-based pricing, with processing, storage, networking and additional services contributing to total cost. |
| Data Warehousing | Amazon Redshift is described as an enterprise data warehouse based on massively parallel processing and may suit OLAP-focused workloads requiring integration with the AWS data environment. | BigQuery uses a serverless architecture that separates compute and storage and may suit organisations seeking large-scale SQL analytics without managing infrastructure. |

## Key Learning

Overall, neither provider is universally superior. Selection should depend on control requirements, technical skills, workload behaviour, integration needs and total cost.

## References

Alkhatib, A., Shaheen, A. and Albustanji, R.N. (2025) ‘A comparative analysis of cloud computing services: AWS, Azure, and GCP’, *International Journal of Computing and Digital Systems*, 18(1), pp. 1–15. doi: 10.12785/ijcds/1571111846.

Borra, P. (2024) ‘An overview of cloud data warehouses: Amazon Redshift (AWS), Azure Synapse (Azure), and Google BigQuery (GCP)’, *International Journal of Advanced Research in Computer Science*, 15(3), pp. 23–27. doi: 10.26483/ijarcs.v15i3.7099.

Ibrahimi, A. (2017) ‘Cloud computing: Pricing model’, *International Journal of Advanced Computer Science and Applications*, 8(6), pp. 434–441. doi: 10.14569/IJACSA.2017.080658.

Nadeem, F. (2022) ‘Evaluating and ranking cloud IaaS, PaaS and SaaS models based on functional and non-functional key performance indicators’, *IEEE Access*, 10, pp. 63245–63257. doi: 10.1109/ACCESS.2022.3182688.

Zboril, M. and Svatá, V. (2025) ‘Performance comparison of cloud virtual machines’, *Journal of Systems and Information Technology*, 27(2), pp. 197–213. doi: 10.1108/JSIT-02-2022-0040.
