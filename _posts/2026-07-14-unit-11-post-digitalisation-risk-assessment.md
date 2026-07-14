---
layout: post
title: "Unit 11 Individual Assignment: Post-Digitalisation Risk Assessment and Disaster Recovery Strategy"
subtitle: "Using Monte Carlo simulation to evaluate digital supply-chain risks and design an AWS multi-region disaster recovery solution"
categories: ["Security and Risk Management"]
tags: [unit11, individual-assignment, digitalisation, supply-chain-risk, monte-carlo, quantitative-risk-modelling, disaster-recovery, aws, gdpr, vendor-lock-in, reflection]
---

## Overview

This post presents evidence from my **Unit 11 Individual Assignment** for the Security and Risk Management module. The assessment required an executive summary evaluating how the digitalisation of Pampered Pets could affect product quality, product availability and supply-chain security.

The scenario introduced an international supply chain, automated warehouses, an online shop, a warehouse management system (WMS), customer relationship management (CRM), logistics partners and cloud-based services. The assessment therefore treated the organisation as a digital supply-chain system whose performance depends on reliable product, information and financial flows.

The work combined risk identification, probability ranges, impact scoring, Monte Carlo simulation, a deterministic cross-check and TARA-based recommendations. It also proposed an AWS active-active multi-region disaster recovery solution designed to support 24/7/365 service availability, with a Recovery Time Objective (RTO) and Recovery Point Objective (RPO) of less than one minute.

---

## Assignment Activity Summary

| Area | Summary |
|---|---|
| Assessment | Individual Executive Summary |
| Unit | Unit 11 |
| Business scenario | Pampered Pets post-digitalisation |
| Main changes assessed | International suppliers, automated warehouses, online operations, WMS, CRM and cloud services |
| Main outcomes assessed | Product quality, product availability and digital supply-chain security |
| Quantitative method | Monte Carlo simulation with 10,000 iterations |
| Supporting methods | Probability-impact scoring, deterministic cross-check and heat-map presentation |
| Risk response framework | Transfer, Accept, Reduce and Avoid (TARA) |
| DR requirement | 24/7/365 availability with RTO and RPO below one minute |
| Recommended platform | Amazon Web Services with Amazon Aurora Global Database |
| Main learning evidence | Risk model, Python outputs, quantitative results, DR architecture and final recommendations |

---

## Assessment Scope

The assessment examined the post-digitalisation supply chain through three connected flows.

| Supply-chain flow | Application in the scenario |
|---|---|
| Product flow | Pet food products moving from international suppliers through logistics and automated warehouses to customers |
| Information flow | Online orders, inventory records, WMS data, CRM data, supplier communication and fulfilment status |
| Financial flow | Online payments, supplier invoices, transaction records and shipping costs |

The main focus was placed on **information-flow risks** because product availability, product quality and operational continuity depend on accurate, secure and integrated data across the digital supply chain.

### Post-digitalisation assessment process

<img src="/assets/images/SRM/Unit11/Post-Digitalisation-Supply-Chain-Risk.png" alt="Post-digitalisation supply-chain risk and disaster recovery assessment process" width="800">

**Figure 1.** Post-digitalisation supply-chain risk and disaster recovery assessment activities.

---

## Risks Identified

Five risk scenarios were selected because they directly reflected the proposed digital transformation.

| Risk | Description | Main business effect |
|---|---|---|
| R1: Inventory data inaccuracy | Incorrect stock records may show unavailable products as available and cause failed orders or dispatches. | Availability |
| R2: System integration failure | E-commerce, CRM, inventory, WMS and logistics systems may fail to exchange data correctly. | Availability and quality |
| R3: Cybersecurity breach or ransomware | A cyberattack may interrupt online operations, warehouse execution and data integrity. | Availability and security |
| R4: International supplier or logistics disruption and quality variation | Supplier, customs, logistics or storage variation may affect supply continuity and product quality. | Quality and availability |
| R5: Automated warehouse system failure | WMS, automated guided vehicles, scanners, sensors or warehouse networks may fail. | Availability and quality |

---

## Quantitative Risk Modelling Approach

Monte Carlo simulation was selected because the organisation did not have historical data for the proposed international digital supply chain. Instead of relying on unsupported single-point estimates, each risk was assigned a minimum, most likely and maximum probability.

The model used a triangular distribution for each risk and completed **10,000 iterations**. For every iteration, the code sampled a probability for each risk and calculated the probability of at least one relevant quality, availability or security issue.

The model also calculated individual risk exposure using:

```text
Exposure = Probability × Impact
```

A deterministic cross-check using the most likely probabilities was completed to confirm that the Monte Carlo results followed the same broad pattern.

### Model assumptions

The main assumptions were:

- the model covers the first 12 months after implementation;
- a material event includes a failed customer order, quality deviation, online-service outage or security incident requiring formal response;
- the probability values are scenario-based estimates informed by literature, professional sources and business judgement;
- the sources support the relevance of the risks rather than exact event frequencies for Pampered Pets;
- aggregate calculations assume approximate independence between the selected risks;
- shared causes could cause the combined exposure to be understated or overstated;
- impact was scored from 1 to 5, with higher values representing greater operational or commercial harm.

---

## Python Model and Reproducibility Evidence

The quantitative model was developed in Python and saved in the repository.

[View the Monte Carlo simulation code](/assets/code/SRM/monte_carlo_simulation.py)

### Successful execution and reproducibility settings

<img src="/assets/images/SRM/Unit11/Successful-Execution-and-Reproducibility-Settings.png" alt="Python execution showing the random seed and 10000 Monte Carlo iterations" width="800">

**Figure 2.** Successful execution showing the random seed and 10,000 simulation iterations.

### Risk assumptions and expected exposure

<img src="/assets/images/SRM/Unit11/Python-Output-for-Risk-Assumptions-and-Exposure.png" alt="Python output showing the risk assumptions, mean probabilities, impacts and expected exposure scores" width="800">

**Figure 3.** Python output for risk assumptions and expected exposure.

---

## Quantitative Results

The model showed that inventory data inaccuracy was the highest individual priority, followed by international supplier or logistics disruption, system integration failure, cybersecurity breach or ransomware, and automated warehouse failure.

| Priority | Risk | Most likely probability | Impact | Exposure score |
|---:|---|---:|---:|---:|
| 1 | R1: Inventory data inaccuracy | 55% | 4 | 2.20 |
| 2 | R4: Supplier or logistics disruption and quality variation | 35% | 5 | 1.75 |
| 3 | R2: System integration failure | 35% | 4 | 1.40 |
| 4 | R3: Cybersecurity breach or ransomware | 20% | 5 | 1.00 |
| 5 | R5: Automated warehouse system failure | 20% | 4 | 0.80 |

### Probability and impact ranking

<img src="/assets/images/SRM/Unit11/Probability × impact results.png" alt="Probability multiplied by impact ranking for the five digital supply-chain risks" width="800">

**Figure 4.** Probability and impact results used to prioritise the five risks.

The aggregate Monte Carlo results were:

| Outcome | Monte Carlo mean | 5th percentile | 95th percentile |
|---|---:|---:|---:|
| At least one quality issue | 66.9% | 58.5% | 74.5% |
| At least one availability issue | 87.9% | 83.6% | 91.5% |
| At least one security issue | 21.7% | 13.5% | 30.6% |

### Monte Carlo simulation results

<img src="/assets/images/SRM/Unit11/Monte Carlo simulation results.png" alt="Monte Carlo simulation output showing quality, availability and security probabilities" width="800">

**Figure 5.** Monte Carlo simulation results from 10,000 iterations.

The deterministic cross-check produced similar results:

| Outcome | Deterministic result | Monte Carlo mean |
|---|---:|---:|
| At least one quality issue | 66.2% | 66.9% |
| At least one availability issue | 87.8% | 87.9% |
| At least one security issue | 20.0% | 21.7% |

### Deterministic cross-check

<img src="/assets/images/SRM/Unit11/Python Output for the Deterministic Cross-Check.png" alt="Python output showing the deterministic cross-check of quality, availability and security probabilities" width="800">

**Figure 6.** Deterministic cross-check using the most likely probability values.

---

## Interpretation of the Results

The model identified **availability** as the most exposed outcome, with an estimated probability of 87.9%. This result reflects the organisation’s dependency on accurate inventory data, reliable system integration, supplier continuity and warehouse availability.

The estimated probability of at least one **quality issue** was 66.9%. The main contributors were supplier or logistics variation, system integration failure and warehouse control weaknesses. This was commercially important because Pampered Pets depends on maintaining its product reputation while serving high-profile customers.

The estimated probability of at least one **security issue** was lower at 21.7%. However, this result was not treated as a low business priority because the ransomware scenario had a critical impact score of 5 and could interrupt the online shop, WMS, order processing and access to operational data.

---

## TARA-Based Recommendations

The recommendations were prioritised using the modelled probabilities, exposure scores and the commercial importance of each outcome.

| Priority | Recommendation | Quantitative basis | TARA response |
|---:|---|---|---|
| 1 | Inventory accuracy programme | R1: 55% probability, impact 4, exposure 2.20 | Reduce |
| 2 | Supplier quality assurance process | R4: 35% probability, impact 5, exposure 1.75 | Reduce |
| 3 | System integration governance | R2: 35% probability, impact 4, exposure 1.40 | Reduce |
| 4 | Cybersecurity resilience baseline | R3: 20% probability, impact 5, exposure 1.00 | Reduce and Transfer |
| 5 | Warehouse continuity process | R5: 20% probability, impact 4, exposure 0.80 | Reduce and Transfer |
| 6 | AWS active-active multi-region DR | RTO and RPO below one minute | Reduce |
| 7 | GDPR and data governance process | Linked to R2 and R3 data and security risks | Reduce and Avoid |
| 8 | Vendor lock-in reduction process | Linked to cloud and DR platform dependency | Reduce |

The recommended controls included barcode scanning, WMS validation, stock reconciliation, approved supplier lists, supplier scorecards, integration testing, API monitoring, multi-factor authentication, role-based access control, immutable backups, preventive maintenance, manual fallback procedures, data minimisation and supplier data-processing agreements.

---

## Disaster Recovery Solution

The online shop was required to remain available 24/7/365, with an RTO and RPO of less than one minute. Cold standby, periodic restoration and manual recovery were therefore unsuitable.

The proposed design used an **AWS active-active multi-region application architecture** supported by:

- two active application regions;
- live traffic distribution;
- continuous health checks;
- automated traffic redirection;
- Amazon Aurora Global Database;
- cross-region replication;
- automated database failover;
- regular disaster recovery testing.

### Disaster recovery architecture

<img src="/assets/images/SRM/Unit11/disaster_recovery_architecture.png" alt="AWS active-active multi-region disaster recovery architecture designed for sub-one-minute RTO and RPO" width="800">

**Figure 7.** AWS active-active multi-region disaster recovery architecture for sub-one-minute RTO and RPO.

AWS was selected for the online shop and critical supporting data services because the platform supports multi-region deployment, automated failover and near-real-time replication. Amazon Aurora Global Database was recommended for the critical order and transaction database.

Vendor lock-in was addressed through portable backups, contractual data-export rights, open API design, infrastructure-as-code, containerised deployment where practical and a documented exit plan.

---

## Reflection

This assignment developed my understanding of how quantitative methods can be applied to a business scenario where complete historical data is unavailable. At the beginning of the activity, I viewed risk assessment mainly as the identification and ranking of threats using qualitative likelihood and impact categories. Developing the Monte Carlo model helped me understand how probability ranges can represent uncertainty more effectively than unsupported single-point estimates.

The most important learning point was the distinction between identifying a risk and estimating its effect on a wider business outcome. The five risks had separate probabilities and impact scores, but the model also calculated the probability of at least one quality, availability or security issue. This showed me that several moderate risks can combine to create a high overall level of exposure. The 87.9% availability result was particularly important because it demonstrated how inventory errors, integration failures, supplier disruption and warehouse failures collectively affect the reliability of the online business.

The deterministic cross-check also improved my understanding of model validation. It was not an independent validation method, but it provided a useful consistency check by confirming that the most likely probability values produced results close to the Monte Carlo means. This helped me recognise the importance of checking whether model outputs are reasonable rather than accepting simulation results without review.

The assignment also strengthened my understanding of the relationship between risk assessment and business continuity. The disaster recovery requirement could not be addressed through ordinary backup procedures because the specified RTO and RPO were below one minute. Designing the AWS multi-region solution showed me that recovery objectives directly influence architecture, replication, monitoring, failover and testing requirements.

Finally, the activity improved my ability to connect technical controls with business priorities. Inventory validation, supplier assurance, cybersecurity, GDPR and vendor portability were not treated as isolated technical concerns. They were linked to product reputation, customer trust, online availability and long-term operational resilience. In future work, I would improve the model further by using operational data collected after implementation, reviewing dependencies between risks and updating the probability ranges as evidence becomes available.

---

## References

Amazon Web Services (n.d.) *Amazon Aurora Global Database*. Available at: https://aws.amazon.com/rds/aurora/global-database/ (Accessed: 3 July 2026).

Boyens, J., Smith, A., Bartol, N., Winkler, K., Holbrook, A. and Fallon, M. (2024) *Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations*. NIST Special Publication 800-161 Rev. 1 Update 1. Gaithersburg, MD: National Institute of Standards and Technology. doi:10.6028/NIST.SP.800-161r1-upd1.

Chopra, S. and Meindl, P. (2016) *Supply Chain Management: Strategy, Planning, and Operation*. 6th edn. Boston, MA: Pearson.

Cox, L.A. (2008) ‘What’s wrong with risk matrices?’, *Risk Analysis*, 28(2), pp. 497–512. doi:10.1111/j.1539-6924.2008.01030.x.

DeHoratius, N. and Raman, A. (2008) ‘Inventory record inaccuracy: An empirical analysis’, *Management Science*, 54(4), pp. 627–641. doi:10.1287/mnsc.1070.0789.

Duijm, N.J. (2015) ‘Recommendations on the use and design of risk matrices’, *Safety Science*, 76, pp. 21–31. doi:10.1016/j.ssci.2015.02.014.

Granata, D., Mastroianni, M., Rak, M., Cantiello, P. and Salzillo, G. (2024) ‘GDPR compliance through standard security controls: An automated approach’, *Journal of High Speed Networks*, 30(2), pp. 147–174. doi:10.3233/JHS-230080.

Hasani, A., Haseli, G. and Deveci, M. (2025) ‘Analyzing operational risks of digital supply chain transformation using hybrid ISM-MICMAC method’, *OPSEARCH*, 62, pp. 583–607. doi:10.1007/s12597-024-00792-y.

Hosseini, S., Ivanov, D. and Dolgui, A. (2020) ‘Ripple effect modelling of supplier disruption: Integrated Markov chain and dynamic Bayesian network approach’, *International Journal of Production Research*, 58(11), pp. 3284–3303. doi:10.1080/00207543.2019.1661538.

Hubbard, D.W. and Seiersen, R. (2016) *How to Measure Anything in Cybersecurity Risk*. Hoboken, NJ: Wiley. doi:10.1002/9781119162315.

Lewczuk, K. (2021) ‘The study on the automated storage and retrieval system dependability’, *Eksploatacja i Niezawodnosc – Maintenance and Reliability*, 23(4), pp. 709–718. doi:10.17531/ein.2021.4.13.

Li, J., He, Z. and Wang, S. (2022) ‘A survey of supply chain operation and finance with Fintech: Research framework and managerial insights’, *International Journal of Production Economics*, 247, 108431. doi:10.1016/j.ijpe.2022.108431.

Moran, A. (2014) *Agile Risk Management*. Cham: Springer International Publishing. doi:10.1007/978-3-319-05008-9.

Moravcik, M., Segec, P., Kontsek, M. and Zidekova, L. (2024) ‘Model-driven approach to cloud-portability issue’, *Applied Sciences*, 14(20), Article 9298. doi:10.3390/app14209298.

Pennekamp, J., Matzutt, R., Klinkmüller, C., Bader, L., Serror, M., Wagner, E., Malik, S., Spiß, M., Rahn, J., Gürpinar, T., Vlad, E., Leemans, S.J.J., Kanhere, S.S., Stich, V. and Wehrle, K. (2024) ‘An interdisciplinary survey on information flows in supply chains’, *ACM Computing Surveys*, 56(2), Article 32, pp. 1–38. doi:10.1145/3606693.

Polyviou, M., Ramos, G. and Schneller, E. (2022) ‘Supply chain risk management: An enterprise view and a survey of methods’, in Khojasteh, Y., Xu, H. and Zolfaghari, S. (eds.) *Supply Chain Risk Mitigation: Strategies, Methods and Applications*. Cham: Springer International Publishing, pp. 27–58. doi:10.1007/978-3-031-09183-4_2.

Schmitt, A.J. and Singh, M. (2009) ‘Quantifying supply chain disruption risk using Monte Carlo and discrete-event simulation’, in *Proceedings of the 2009 Winter Simulation Conference*, Austin, TX, 13–16 December. Piscataway, NJ: IEEE, pp. 1237–1248. doi:10.1109/WSC.2009.5429561.

Sobb, T., Turnbull, B. and Moustafa, N. (2020) ‘Supply Chain 4.0: A survey of cyber security challenges, solutions and future directions’, *Electronics*, 9(11), Article 1864. doi:10.3390/electronics9111864.

Stoneburner, G., Goguen, A. and Feringa, A. (2002) *Risk Management Guide for Information Technology Systems*. NIST Special Publication 800-30. Gaithersburg, MD: National Institute of Standards and Technology. doi:10.6028/NIST.SP.800-30.

Yadav, G. (2023) ‘Architectural approaches to disaster recovery and high availability in SAP HANA Cloud’, *International Journal of Scientific Research and Modern Technology*, 2(8), pp. 81–91. doi:10.38124/ijsrmt.v2i8.854.
