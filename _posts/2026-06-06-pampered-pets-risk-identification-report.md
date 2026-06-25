---
layout: post
title: "Security Risk Identification Report: Pampered Pets"
subtitle: "Pampered Pets current state and digitalisation risks using NIST CSF 2.0"
categories: ["Security and Risk Management"]
tags: [unit6, team-project, risk-identification, pampered-pets, nist-csf, digitalisation, cybersecurity, qualitative-risk-assessment]
---

# Security Risk Identification Report: Pampered Pets Current State and Digitalization Risks

## Introduction

Pampered Pets is a small bricks-and-mortar pet food retailer that operates mainly through face-to-face sales while using limited digital tools such as e-mail orders, spreadsheets, staff smartphones and a shared wireless network. This report evaluates the cybersecurity, operational, data protection and supply chain risks in the current operating model and the proposed digitalisation programme. The report uses NIST CSF 2.0 as the guiding framework for structuring the assessment and provides phased recommendations on whether digitalisation should proceed.

## Risk Assessment Methodology

A qualitative asset-based risk assessment methodology is structured using NIST CSF 2.0 functions: Govern, Identify, Protect, Detect, Respond and Recover (National Institute of Standards and Technology, 2024). The framework is applied through qualitative asset-based tables that connect each business asset with relevant threats, vulnerabilities, likelihood, impact, risk rating, NIST function and mitigation. Risks are rated as Low, Medium or High by considering both likelihood and impact, reflecting standard practices in enterprise risk management (AIRMIC, 2010). This approach is suitable for Pampered Pets because SMEs often face limited security awareness, informal governance and weaker technical controls (Bada and Nurse, 2019). “Threat modelling principles were applied to identify cyber and operational threats affecting key business assets.”

## Current Business Risk Assessment

As shown in Table 1, the current operating model presents several cybersecurity and operational risks. The highest risks relate to Harry’s old warehouse computer, the shared Wi-Fi gateway, the front-desk sales computer and customer and sales records.

The old warehouse computer is a significant vulnerability because it is an ageing networked device with no stated endpoint protection, patching process or backup control. This creates exposure to malware, system failure and stock data loss. Chidukwani and Koutsakis (2022) identify unpatched and weakly controlled SME systems as important cybersecurity concerns.

The shared wireless gateway is also a material risk because business computers and staff smartphones use the same unsegmented network. This increases the likelihood of unauthorized access or malware movement between devices. Harris and Patten (2014) note that unmanaged mobile devices can increase security exposure for smaller organisations. In addition, the front-desk sales computer stores sales, VAT and tax records without a documented backup or recovery process. Customer and sales records also create potential UK GDPR compliance exposure if accessed, lost or retained without appropriate controls.

### Table 1: Current Business Risk Assessment for Pampered Pets

| Asset | NIST CSF Function | Threat | Vulnerability | Likelihood | Impact | Risk Level | Mitigation |
|---|---|---|---|---|---|---|---|
| Old warehouse computer | Protect / Recover | Malware or system failure | Old networked device; no stated patching or protection | High | High | High | Update or replace device; endpoint protection; patching; backups |
| Warehouse spreadsheet | Identify / Protect | Stock data loss or error | Manual spreadsheet tracking with limited access control or backup | Medium | Medium | Medium | Controlled inventory system; restricted editing; regular backups |
| Front-desk computer | Protect / Recover | Loss of sales and tax records | Key records stored on one system | Medium | High | High | Access control; backups; recovery procedures |
| Wireless gateway | Protect | Unauthorised access or malware spread | Shared and unsegmented network | High | High | High | Secure router; strong passwords; network segmentation |
| Staff smartphones | Protect | Malware or unsafe application use | Personal devices use business Wi-Fi | Medium | Medium | Medium | BYOD rules; staff guidance; network segmentation |
| E-mail orders | Detect / Protect | Phishing or spoofed orders | Manual e-mail orders with weak verification | Medium | Medium | Medium | E-mail filtering; staff training; order verification checks |
| Customer records | Govern / Protect | Data loss or unauthorised access | Weak access, backup and retention controls | Medium | High | High | RBAC; secure passwords; backups; data protection procedures |
| Local suppliers | Identify / Recover | Supply disruption | Reliance on limited local suppliers | Medium | Medium | Medium | Backup suppliers; supplier continuity plan |

Table 1 shows that the highest current risks affect business continuity, financial record integrity, stock visibility, and data protection. These risks should be treated as immediate priorities because they would be inherited and amplified by new digital infrastructure if left unresolved.

## Digitalisation Risk Assessment

The proposed digitalisation program should be treated as a controlled risk transition, rather than as an automatic improvement. Metin et al. (2024) argue that digitalisation introduces additional cybersecurity exposure that requires structured governance before implementation. This is relevant because Pampered Pets currently lacks formalised security controls.

The scenario figures should be treated cautiously. A possible 50 per cent online revenue increase is a planning assumption rather than a confirmed forecast, as outcomes would depend on demand, fulfilment capacity, marketing effectiveness and customer trust. Similarly, the projected 24 per cent cost reduction through international sourcing requires validation through supplier due diligence and cost modelling. Yudhiyati et al. (2021) caution that SMEs may underestimate the operational complexity and security risks of digital supply chain transitions. The 33 per cent customer-loss figure should also be treated as a competitive risk scenario rather than a proven outcome.

As shown in Table 2, the e-commerce website, online payment system, CRM/customer accounts and international suppliers each carry a high risk rating. These risks do not prevent digitalisation, but they require governance, access controls, monitoring, supplier assessment, incident response and recovery planning. Nazareth et al. (2024) support hosted and security-managed e-commerce solutions for SMEs, particularly where payment and customer data risks exist. A full move to international sourcing is not recommended for core pet food products unless due diligence confirms equivalent quality, reliability and resilience. Local suppliers should therefore remain central to core product lines, while international suppliers should be trialed only for non-core products (Sun et al., 2025).

### Table 2: Digitalisation Risk Assessment for Pampered Pets

| Digitalisation Change | NIST CSF Function | Threat | Vulnerability | Likelihood | Impact | Risk Level | Mitigation |
|---|---|---|---|---|---|---|---|
| E-commerce website | Protect / Detect | Website attack, denial-of-service attack, downtime or defacement | Public-facing system increases exposure | Medium | High | High | Hosted platform; HTTPS; patching; regular vulnerability scanning; monitoring; DDoS protection |
| Online payment system | Govern / Protect | Payment fraud, credential theft or payment data exposure | Financial and compliance risk | Medium | High | High | PCI DSS-compliant payment gateway; tokenisation; no card storage; MFA for admin access. |
| Cloud inventory system | Protect / Recover | Service outage or misconfiguration | Third-party cloud dependency | Medium | Medium | Medium | Trusted vendor; RBAC; backups; export plan; service-level review. |
| Customer accounts / CRM | Govern / Protect | Customer data breach, staff account compromise or unauthorised access | Increased personal data storage | Medium | High | High | MFA; RBAC; least-privilege access; data minimisation; UK GDPR-aligned privacy and retention policy |
| Digital marketing channels | Detect / Respond | Social media impersonation, reputational damage or misleading communication | Public messaging and customer reviews | Medium | Medium | Medium | Account protection; content approval; feedback monitoring; complaint and response plan |
| International suppliers | Identify / Recover | Quality issues, delivery delays or supplier failure | Reduced control over supplier quality | Medium | High | High | Supplier verification; contractual security and quality requirements; phased testing; retain local core suppliers |

Table 2 demonstrates that digitalisation would introduce High risks in e-commerce, online payments, CRM/customer accounts and international sourcing. However, proportionate controls, phased implementation and documented governance would reduce cyber risk and improve operational resilience.

## Recommendation

Digitalisation is recommended, provided it is implemented through a controlled, phased approach that is aligned with the NIST CSF functions. The current-to-digital risk transition is summarised in Appendix A (see Appendix A). Phase 1 should secure the current environment within 0–30 days. This includes updating or replacing the warehouse computer, installing endpoint protection and firewall controls, applying patches, implementing tested backups, segmenting the wireless network, securing the front-desk POS system, documenting recovery procedures and applying role-based and least-privilege access controls to customer data.

Phase 2 should introduce a low-risk digital presence within months 1–3 through a hosted website or product catalogue selected through vendor due diligence, with HTTPS, security patching, regular vulnerability scanning, website monitoring, DDoS protection and an incident response plan.

Phase 3 should introduce transactional digitalisation within months 3–6. Online payments should use a secure PCI DSS-compliant gateway, encrypted customer and payment data, and no direct card storage. CRM should use MFA, least-privilege access and a UK GDPR-aligned privacy and retention policy. Cloud inventory should require vendor due diligence, RBAC, tested backups, disaster recovery planning and service-level review.

Phase 4 should involve a controlled supplier trial within months 6–12. International suppliers should be formally verified, subject to contractual security and quality requirements, and tested only for non-core product lines, while local suppliers remain central to core pet food products.

Overall, the benefits are likely to outweigh the risks if appropriate safeguards are implemented.


## Collaboration and Meeting Evidence

As part of the group work for this report, a meeting was arranged with Payman Ghorbani to clarify the project requirements and divide the work before submission. The discussion focused on understanding the main purpose of the assignment, including whether Pampered Pets should proceed with digitalisation or maintain the current situation. The meeting also helped clarify how the report would answer the required questions through risk analysis, recommendations and final formatting.

The second purpose of the meeting was to agree on work division and the submission timeline. The tasks were divided between group members, including research, current business risk assessment, digitalisation risk assessment, recommendations and final review. This helped ensure that the report was completed in a structured way and that the group had an internal deadline before the official submission date.

### Meeting confirmation

<img src="/assets/images/SRM/Unit6/meetingconfirmation.png" alt="Screenshot showing meeting confirmation with Payman Ghorbani" width="800">

**Figure 3.** Meeting confirmation with Payman Ghorbani.

### Meeting discussion points

<img src="/assets/images/SRM/Unit6/minutesofmeeting.png" alt="Screenshot showing discussion points for the group meeting" width="800">

**Figure 4.** Meeting discussion points covering project requirements, work division and submission timeline.

The meeting evidence demonstrates collaboration, planning and task coordination. It also shows that the group discussed the project requirements before completing the report, which helped align the risk assessment, recommendations and final submission.


## Conclusion

Maintaining the status quo would leave Pampered Pets exposed to operational, cybersecurity and data protection risks. However, rapid digitalisation would introduce additional payment, privacy, platform and supplier risks. A phased approach is therefore the most proportionate option, as it supports customer access and operational efficiency while protecting product quality, business continuity and customer trust.

## References

AIRMIC (2010) *A structured approach to enterprise risk management (ERM) and the requirements of ISO 31000*. London: AIRMIC.

Bada, M. and Nurse, J.R.C. (2019) ‘Developing cybersecurity education and awareness programmes for small- and medium-sized enterprises’, *Information and Computer Security*, 27(3), pp. 393–410.

Chidukwani, Z., Zander, S. and Koutsakis, P. (2022) ‘A survey on the cyber security of small-to-medium businesses: challenges, research focus and recommendations’, *IEEE Access*, 10, pp. 85701–85719.

Harris, M.A. and Patten, K.P. (2014) ‘Mobile device security considerations for small- and medium-sized enterprise business mobility’, *Information Management & Computer Security*, 22(1), pp. 97–114.

Metin, B., Özhan, F.G. and Wynn, M. (2024) ‘Digitalisation and cybersecurity: towards an operational framework’, *Electronics*, 13(21), p. 4226.

National Institute of Standards and Technology (2024) *Cybersecurity Framework (CSF) 2.0*. Gaithersburg, MD: NIST.

Nazareth, D.L. et al. (2024) ‘Investing in security-as-a-service for e-commerce infrastructure by small and medium enterprises: a Monte Carlo approach’, *Journal of Systems and Information Technology*, 26(2), pp. 257–275.

Sun, K., Ooi, K.B., Hwang, G.W., Lee, V.H. and Tan, K.H. (2025) ‘Small and medium-sized enterprises’ path to sustainable supply chains: exploring the role of supply chain finance and risk management’, *Supply Chain Management*, 30(1), pp. 1–18.

Yudhiyati, R., Putritama, A. and Rahmawati, D. (2021) ‘What small businesses in developing country think of cybersecurity risks in the digital age: Indonesian case’, *Journal of Information, Communication and Ethics in Society*, 19(4), pp. 446–462.

## Appendices

### Appendix A: Current VS. Digitalised Risk Situation

<img src="/assets/images/SRM/Unit6/Current-VS-Digitalised-Risk-Situation.png" alt="Current versus digitalised risk situation for Pampered Pets" width="800">

**Figure A1.** Current VS. Digitalised Risk Situation.
