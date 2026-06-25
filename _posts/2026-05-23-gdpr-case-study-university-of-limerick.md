---
layout: post
title: "GDPR Case Study: Inquiry concerning the University of Limerick"
subtitle: "Unit 5 e-Portfolio Activity – GDPR Case Studies"
categories: ["Security and Risk Management"]
tags: [unit5, e-portfolio, gdpr, data-protection, phishing, breach-notification]
---

GDPR Case Study: Inquiry concerning the University of Limerick

## Introduction

This case study examines the Data Protection Commission’s final decision concerning the University of Limerick. The inquiry arose after a series of personal data breaches involving unauthorised access to staff email accounts between November 2018 and January 2020. The case is relevant to information security management because it demonstrates how phishing attacks, weak email security controls and delayed breach handling can create significant GDPR compliance risks. The decision is particularly concerned with the security of processing, breach notification duties and the need for appropriate technical and organisational measures (Data Protection Commission, 2025). 

Table 1 summarises the main GDPR issues identified in the University of Limerick case and links them to relevant information security management actions.

| Area | Summary |
|---|---|
| Case study | Inquiry concerning the University of Limerick |
| Main issue | Unauthorised access to staff email accounts following phishing attacks and fake login pages |
| Type of data risk | Personal data breach involving possible exposure of identity, contact, financial and other personal information |
| Relevant GDPR aspects | Article 5(1)(f): integrity and confidentiality; Article 32(1): security of processing; Article 33(1): breach notification; Article 34(1): communication to affected individuals; Article 30(1): records of processing activities |
| Main weakness | Email security controls were not proportionate to the risk, particularly in relation to phishing protection, MFA and breach management |
| Resolution | The DPC issued a reprimand and administrative fines totalling €98,000, while also recognising that the university later introduced remedial security improvements |
| Information Security Manager response | Strengthen MFA, phishing protection, incident response, breach notification procedures, staff training, email monitoring, data retention and GDPR governance |

As shown in Table 1, the case was not limited to a technical phishing incident. It also raised wider governance concerns relating to breach notification, records of processing and the adequacy of organisational security controls. 


## Visual Summary of the GDPR Case

<img src="/assets/images/SRM/Unit5/gdpr_breach_flowchart.png" alt="Flowchart summarising the University of Limerick GDPR breach and security management response" width="800">

**Figure 1.** Summary of the University of Limerick GDPR breach, regulatory outcome and recommended Information Security Manager response.


### Specific aspect of GDPR addressed

The main GDPR aspect addressed in this case is the principle of integrity and confidentiality under Article 5(1)(f), together with the requirement for security of processing under Article 32(1). These provisions require organisations to protect personal data against unauthorised or unlawful processing, accidental loss, destruction or damage through appropriate technical and organisational measures (European Parliament and Council, 2016).

In the University of Limerick case, unauthorised third parties gained access to staff email accounts after phishing emails and fake login pages captured user credentials. The compromised accounts contained personal data and, in some cases, sensitive or high-risk information. The decision also shows that the affected data included identity details, contact information, financial data and other personal information held in staff mailboxes (Data Protection Commission, 2025). 

The case also addresses Articles 30(1), 33(1) and 34(1) GDPR. Article 30(1) concerns the obligation to maintain records of processing activities. Article 33(1) requires controllers to notify the supervisory authority of a personal data breach without undue delay and, where feasible, within 72 hours. Article 34(1) requires affected individuals to be informed where a breach is likely to result in a high risk to their rights and freedoms. As shown in the decision’s summary table of incidents, several breaches were reported to the DPC after unauthorised access had already occurred, demonstrating the importance of timely detection, escalation and notification. 

### How the issue was resolved

The issue was resolved through a regulatory inquiry by the Data Protection Commission. The DPC found that the University of Limerick had infringed Articles 5(1)(f), 32(1), 30(1), 33(1) and 34(1) GDPR. The decision concluded that the university had not implemented a level of security appropriate to the risks associated with its staff email system at the time of the breaches (Data Protection Commission, 2025). 

The DPC imposed a reprimand and administrative fines totalling €98,000. This included fines for failures relating to integrity and confidentiality, security of processing, records of processing, breach notification to the supervisory authority, and communication of high-risk breaches to affected data subjects. However, the DPC also acknowledged that the university had introduced remedial measures after the incidents. These included implementing multi-factor authentication, improving email security, moving towards more secure cloud-based services, strengthening incident response arrangements, updating policies and providing additional security awareness training.

Therefore, the resolution was not limited to financial penalties. It also involved recognising the need for improved governance, stronger technical controls and more effective organisational processes. This reflects a wider GDPR principle: compliance requires both security technology and accountable management practices.

### Steps an Information Security Manager should take

If a similar incident occurred in an organisation, the Information Security Manager should take a structured and risk-based response. First, the immediate priority should be containment. Compromised accounts should be disabled, passwords reset, active sessions revoked and suspicious forwarding rules removed. The organisation should also review the affected mailboxes to identify what personal data was accessed, altered or disclosed.

Second, the incident should be managed through a formal breach response process. The Information Security Manager should work with the Data Protection Officer, legal team and senior management to assess the severity of the breach. If the breach is likely to affect individuals’ rights and freedoms, the supervisory authority should be notified within the Article 33 timeframe. Where the breach creates a high risk to individuals, affected data subjects should also be informed clearly and without undue delay.

Third, technical controls should be strengthened. Multi-factor authentication should be mandatory for all users, especially staff with access to personal or sensitive data. Email authentication controls such as SPF, DKIM and DMARC should be implemented to reduce spoofing risks. In addition, phishing protection, malware filtering, suspicious login detection, mailbox rule monitoring and centralised security logging should be introduced. These controls would reduce both the likelihood and impact of account compromise.

Fourth, organisational controls should be improved. Staff should receive regular training on phishing, password security, data handling and breach reporting. Policies on email use, access control, retention and incident response should be reviewed and updated. The organisation should also maintain an accurate record of processing activities and ensure that responsibilities for breach escalation are clearly assigned.

Finally, the organisation should reduce reliance on email as a storage location for personal data. Sensitive information should be stored in controlled systems with appropriate permissions, retention rules and audit logging. Regular risk assessments and data protection impact assessments should be used to ensure that security measures remain proportionate to the nature and volume of personal data being processed. This would support GDPR compliance while also improving the organisation’s overall security maturity.

## Conclusion

The University of Limerick case demonstrates that GDPR compliance depends on effective technical controls, timely breach management and strong organisational governance. The central issue was the failure to maintain an appropriate level of security for staff email accounts, which led to unauthorised access to personal data. The DPC’s decision shows that organisations must not only respond to incidents after they occur, but also proactively assess risks, strengthen controls and maintain clear accountability for personal data protection.


## Reference:

Data Protection Commission (2025) Final Decision: Inquiry concerning the University of Limerick. Dublin: Data Protection Commission.

European Parliament and Council (2016) Regulation (EU) 2016/679: General Data Protection Regulation. Official Journal of the European Union.

