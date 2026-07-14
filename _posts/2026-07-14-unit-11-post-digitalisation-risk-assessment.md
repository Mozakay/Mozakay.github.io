---
layout: post
title: "Unit 11 Individual Assignment: Post-Digitalisation Risk Assessment and Disaster Recovery Strategy"
subtitle: "Applying quantitative risk modelling to digital supply-chain risks and designing an AWS multi-region disaster recovery solution"
categories: ["Security and Risk Management"]
tags: [unit11, individual-assignment, digitalisation, supply-chain-risk, monte-carlo, quantitative-risk-modelling, disaster-recovery, aws, gdpr, vendor-lock-in, reflection]
---

## Overview

This post presents evidence from the author's **Unit 11 Individual Assignment** for the Security and Risk Management module. The task required an assessment of how the proposed digitalisation of Pampered Pets could affect product quality, product availability and supply-chain security.

The assignment was approached by first defining the new operating environment created by the digital transformation. This included the online shop, international suppliers, automated warehouses, the warehouse management system (WMS), customer relationship management (CRM), logistics partners and cloud services. The author then identified the risks created by these dependencies, developed a quantitative model to estimate their probabilities and used the results to prioritise practical recommendations.

The assignment also required a disaster recovery solution capable of supporting 24/7/365 availability, with both the Recovery Time Objective (RTO) and Recovery Point Objective (RPO) below one minute. The author therefore designed an AWS active-active multi-region solution and considered the associated vendor lock-in risks.

---

## How the Assessment Scope Was Defined

The assessment began by examining the business as a connected digital supply-chain system rather than treating digitalisation as a general technology change. This helped the author identify where failures could occur and how one failure could affect several business outcomes.

The system was divided into three flows:

| Supply-chain flow | Application in the assessment |
|---|---|
| Product flow | The assessment considered how products move from international suppliers through logistics and automated warehouses to customers. |
| Information flow | The assessment examined online orders, inventory records, WMS data, CRM information, supplier communication and fulfilment status. |
| Financial flow | The assessment included online payments, supplier invoices, transaction records and shipping costs. |

Particular emphasis was placed on **information-flow risks** because the digital supply chain depends on accurate, secure and integrated data. During this stage, the author learned that product availability and quality are not determined only by physical stock. They can also be affected by incorrect inventory records, failed system interfaces, inaccurate warehouse data or disrupted supplier communication.

### Post-digitalisation assessment process

<img src="/assets/images/SRM/Unit11/Post-Digitalisation-Supply-Chain-Risk.png" alt="Post-digitalisation supply-chain risk and disaster recovery assessment process" width="600">

**Figure 1.** The process followed to move from the digitalisation scenario to risk modelling, prioritisation and disaster recovery recommendations.

---

## How the Risks Were Identified

Five risks were selected because they directly reflected the changes proposed in the scenario. The aim was to avoid creating a general list of digital risks and instead focus on risks that could realistically arise from international supply-chain expansion, warehouse automation and online operations.

| Risk | Reason for selection | Main business effect |
|---|---|---|
| R1: Inventory data inaccuracy | This risk was included because incorrect stock records could cause the online shop to accept orders for unavailable products. | Availability |
| R2: System integration failure | This risk was included because the e-commerce platform, CRM, inventory system, WMS and logistics systems must exchange data accurately. | Availability and quality |
| R3: Cybersecurity breach or ransomware | This risk was included because connected systems and third parties increase the potential attack surface. | Availability and security |
| R4: International supplier or logistics disruption and quality variation | This risk was included because international expansion introduces supplier, customs, transport and storage uncertainty. | Quality and availability |
| R5: Automated warehouse system failure | This risk was included because the new operating model depends on WMS, scanners, sensors, warehouse networks and automated equipment. | Availability and quality |

This stage improved the author's understanding of the difference between identifying a threat and describing its business consequence. For example, system integration failure is a technical risk, but its business effect may be an incorrect order, a delayed dispatch or a product-quality problem.

---

## How the Quantitative Model Was Developed

After identifying the risks, their probabilities needed to be estimated. Pampered Pets did not have historical data for the proposed international digital supply chain, so the use of precise single values as if they were measured frequencies could not be justified.

Each risk was therefore assigned:

- a minimum probability;
- a most likely probability;
- a maximum probability;
- an impact score from 1 to 5.

Triangular distributions were used because they allowed uncertainty to be represented while still distinguishing the most plausible value from the lower and upper estimates. The probability ranges were informed by the scenario, academic literature, professional sources and judgement.

The author then developed a Monte Carlo simulation in Python using **10,000 iterations**. In each iteration, the model sampled a probability for every risk and calculated the probability of at least one relevant quality, availability or security issue.

The model also calculated exposure using:

```text
Exposure = Probability × Impact
```

The most likely probability was used for the risk-priority ranking, while the sampled probability ranges were used for the aggregate Monte Carlo outcomes.

### Documented assumptions

To make the model transparent, the following assumptions were recorded:

- the model covers the first 12 months after implementation;
- a material event includes a failed customer order, quality deviation, online-service outage or security incident requiring formal response;
- the probability values are scenario-based estimates rather than measured Pampered Pets frequencies;
- the cited sources support the relevance of the risks and controls;
- the aggregate calculations assume approximate independence;
- shared causes may cause the combined exposure to be understated or overstated;
- impact is scored from 1 to 5 according to operational and commercial harm.

One of the main lessons from this stage was that a quantitative model is not made reliable simply because it produces numerical results. The author recognised that the assumptions, data limitations and calculation method must also be explained so that the reader can understand how the results were produced.

---

## Python Model and Reproducibility Evidence

The model was developed and tested in Python, and the code was then saved in the repository so that the results could be reproduced.

[View the Monte Carlo simulation code](/assets/code/SRM/monte_carlo_simulation.py)

### Successful execution and reproducibility settings

<img src="/assets/images/SRM/Unit11/Successful-Execution-and-Reproducibility-Settings.png" alt="Python execution showing the random seed and 10000 Monte Carlo iterations" width="700">

**Figure 2.** Evidence that the model ran with a documented random seed and 10,000 iterations.

### Risk assumptions and expected exposure

<img src="/assets/images/SRM/Unit11/Python-Output-for-Risk-Assumptions-and-Exposure.png" alt="Python output showing the risk assumptions, mean probabilities, impacts and expected exposure scores" width="700">

**Figure 3.** Python output showing the assumptions and calculated exposure values.

Creating the code helped the author move beyond describing risks qualitatively. It enabled the effect of uncertainty across several risks on wider business outcomes to be tested.

---

## Quantitative Results

The individual risk ranking showed that inventory data inaccuracy was the highest priority.

| Priority | Risk | Most likely probability | Impact | Exposure score |
|---:|---|---:|---:|---:|
| 1 | R1: Inventory data inaccuracy | 55% | 4 | 2.20 |
| 2 | R4: Supplier or logistics disruption and quality variation | 35% | 5 | 1.75 |
| 3 | R2: System integration failure | 35% | 4 | 1.40 |
| 4 | R3: Cybersecurity breach or ransomware | 20% | 5 | 1.00 |
| 5 | R5: Automated warehouse system failure | 20% | 4 | 0.80 |

### Probability and impact ranking

<img src="/assets/images/SRM/Unit11/Probability × impact results.png" alt="Probability multiplied by impact ranking for the five digital supply-chain risks" width="700">

**Figure 4.** The probability and impact ranking used to prioritise the five risks.

The aggregate Monte Carlo results were:

| Outcome | Monte Carlo mean | 5th percentile | 95th percentile |
|---|---:|---:|---:|
| At least one quality issue | 66.9% | 58.5% | 74.5% |
| At least one availability issue | 87.9% | 83.6% | 91.5% |
| At least one security issue | 21.7% | 13.5% | 30.6% |

### Monte Carlo simulation results

<img src="/assets/images/SRM/Unit11/Monte Carlo simulation results.png" alt="Monte Carlo simulation output showing quality, availability and security probabilities" width="700">

**Figure 5.** Monte Carlo results from 10,000 iterations.

A deterministic cross-check was also completed using the most likely probability for each risk.

| Outcome | Deterministic result | Monte Carlo mean |
|---|---:|---:|
| At least one quality issue | 66.2% | 66.9% |
| At least one availability issue | 87.8% | 87.9% |
| At least one security issue | 20.0% | 21.7% |

### Deterministic cross-check

<img src="/assets/images/SRM/Unit11/Python Output for the Deterministic Cross-Check.png" alt="Python output showing the deterministic cross-check of quality, availability and security probabilities" width="700">

**Figure 6.** The deterministic cross-check using the most likely probability values.

The cross-check did not provide independent validation, but it helped the author confirm that the simulation results were consistent with the underlying assumptions. This demonstrated that model outputs should be checked for reasonableness rather than accepted automatically.

---

## Interpretation of the Results

The most important result was the **87.9% probability of at least one availability issue**. This was interpreted as evidence that the online business would be highly dependent on several connected controls, including inventory accuracy, system integration, supplier continuity and warehouse availability.

The estimated probability of at least one **quality issue was 66.9%**. This result was linked mainly to supplier or logistics variation, system integration problems and warehouse control weaknesses. It was significant because Pampered Pets depends on product reputation and expects to serve high-profile customers.

The estimated probability of at least one **security issue was 21.7%**. Although this was lower than the other outcome probabilities, it was not treated as unimportant. The ransomware scenario had an impact score of 5 and could interrupt the online shop, WMS, order processing and access to operational data.

This part of the activity helped the author understand that probability alone should not determine business priority. A lower-probability risk may still require strong controls when its potential impact is critical.

---

## How the Recommendations Were Developed

The model results, exposure scores and commercial importance of each outcome were used to prioritise the recommendations. The recommendations were then mapped to the Transfer, Accept, Reduce and Avoid (TARA) framework.

| Priority | Recommendation | Basis | TARA response |
|---:|---|---|---|
| 1 | Inventory accuracy programme | R1: 55% probability, impact 4, exposure 2.20 | Reduce |
| 2 | Supplier quality assurance process | R4: 35% probability, impact 5, exposure 1.75 | Reduce |
| 3 | System integration governance | R2: 35% probability, impact 4, exposure 1.40 | Reduce |
| 4 | Cybersecurity resilience baseline | R3: 20% probability, impact 5, exposure 1.00 | Reduce and Transfer |
| 5 | Warehouse continuity process | R5: 20% probability, impact 4, exposure 0.80 | Reduce and Transfer |
| 6 | AWS active-active multi-region DR | RTO and RPO below one minute | Reduce |
| 7 | GDPR and data governance process | Linked to R2 and R3 data and security risks | Reduce and Avoid |
| 8 | Vendor lock-in reduction process | Linked to cloud and DR platform dependency | Reduce |

The recommended controls included:

- barcode scanning;
- WMS validation;
- stock reconciliation;
- approved supplier lists;
- supplier scorecards;
- integration testing;
- API monitoring;
- multi-factor authentication;
- role-based access control;
- immutable backups;
- preventive maintenance;
- manual fallback procedures;
- data minimisation;
- supplier data-processing agreements.

This stage helped the author understand how quantitative results can support decisions without replacing professional judgement. The model helped establish the priority order, but the final recommendations also had to consider reputation, customer trust, legal obligations and operational resilience.

---

## How the Disaster Recovery Solution Was Designed

The assignment specified that the online shop must remain available 24/7/365, with both RTO and RPO below one minute. Cold standby, periodic restoration and manual recovery were therefore ruled out because they would not reliably achieve the required recovery window.

An **AWS active-active multi-region application architecture** was designed with:

- two active application regions;
- live traffic distribution;
- continuous health checks;
- automated traffic redirection;
- Amazon Aurora Global Database;
- cross-region replication;
- automated database failover;
- regular disaster recovery testing.

### Disaster recovery architecture

<img src="/assets/images/SRM/Unit11/disaster_recovery_architecture.png" alt="AWS active-active multi-region disaster recovery architecture designed for sub-one-minute RTO and RPO" width="600">

**Figure 7.** The proposed AWS active-active multi-region disaster recovery solution for sub-one-minute RTO and RPO.

AWS was recommended for the online shop and critical supporting data services because the platform can support multi-region deployment, automated failover and near-real-time replication. Amazon Aurora Global Database was selected for the critical order and transaction database.

Designing this solution helped the author understand that RTO and RPO are not only policy targets. They directly affect architecture, replication, monitoring, failover readiness, capacity planning and testing.

---

## How Vendor Lock-In and GDPR Were Addressed

The choice of AWS was not treated as risk-free. The author recognised that reliance on one cloud provider could increase migration difficulty and switching cost.

The following controls were therefore recommended:

- portable backups;
- contractual data-export rights;
- open API design;
- infrastructure-as-code;
- containerised deployment where practical;
- documented migration procedures;
- a tested exit plan.

GDPR and security controls were also linked to the digital supply-chain risks. The recommended controls included data minimisation, role-based access control and supplier data-processing agreements.

This part of the assignment improved the author's understanding that cloud adoption creates both resilience benefits and dependency risks. A strong solution should use the platform’s capabilities while preserving the organisation’s ability to retrieve, move and govern its data.

---

## Reflection

This assignment changed the author's understanding of quantitative risk assessment. Before completing the activity, the author mainly associated risk assessment with qualitative likelihood and impact categories. Developing the Monte Carlo model demonstrated how probability ranges can represent uncertainty more realistically than unsupported single-point estimates.

The author also learned the importance of distinguishing between an individual risk and an aggregate business outcome. Each of the five risks had its own probability and impact score, but several risks contributed to the same outcome. The availability result demonstrated how inventory errors, integration failures, supplier disruption and warehouse failures could collectively create a much higher overall exposure.

Another important learning point was the need to be transparent about limitations. The model used scenario-based probabilities because historical data were unavailable. The assumptions were therefore documented, the role of the sources was explained and the approximate independence assumption was acknowledged. This helped the author recognise that a useful model does not need to claim perfect precision, but it must explain what the results mean and what they do not mean.

The deterministic cross-check also strengthened the author's approach to reviewing model outputs. Although it was not an independent validation method, it provided a practical way to confirm that the simulation followed the expected pattern. In future work, this approach could be extended by testing dependencies between risks and updating the probability ranges using operational data collected after implementation.

The disaster recovery section helped the author connect business requirements with technical architecture. The sub-one-minute RTO and RPO targets required more than backups. They required multi-region deployment, continuous monitoring, replication, automated failover and regular testing. This demonstrated how continuity objectives should influence system design from the beginning rather than being added after implementation.

Overall, the assignment improved the author's ability to connect risk modelling, technical controls and business priorities. The author learned that inventory accuracy, supplier assurance, cybersecurity, GDPR, disaster recovery and vendor portability are not separate concerns. They collectively protect product reputation, customer trust, online availability and long-term resilience.

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
