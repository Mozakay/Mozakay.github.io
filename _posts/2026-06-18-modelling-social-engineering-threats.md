---
layout: post
title: Modelling and Analysis of Social Engineering Threats
subtitle: Reviewing Aijaz and Nazir’s attack tree and Markov chain approach for quantitative social engineering risk modelling
categories: ["Security and Risk Management"]
tags: [unit8, seminar-preparation, quantitative-risk-modelling, social-engineering, attack-tree, markov-chain, aop, asp, risk-modelling]
---

## Overview

This post was prepared as part of **Unit 8: Implementing Quantitative Risk Models**. The unit focuses on the use of quantitative risk modelling techniques to support risk assessment and decision-making. The reviewed paper is relevant to this unit because it applies probabilistic modelling to Social Engineering Threats (SETs) by estimating **Attack Occurrence Probability (AOP)** and **Attack Success Probability (ASP)**.

This workshop activity reviews Aijaz and Nazir’s (2024) paper, *Modelling and analysis of social engineering threats using the attack tree and the Markov model*. The paper argues that Social Engineering Threats are a significant information security concern because they exploit human vulnerability rather than relying only on technical system weaknesses. While technical controls may protect systems, users can still be manipulated into disclosing sensitive information, sharing credentials or performing harmful actions.

The paper is useful for Security and Risk Management because it separates two important dimensions of risk: the probability that an attack occurs and the probability that it succeeds. The Attack Tree Model is used to estimate AOP, based on the frequency of communication modalities and persuasion principles. The Markov Chain Model is used to estimate ASP, based on the effectiveness of those modalities and persuasion principles.

---

## Question 1: Challenges in Modelling and Evaluating Social Engineering Threats

The main challenge in modelling Social Engineering Threats is that they depend heavily on human behaviour. Unlike purely technical attacks, SETs are influenced by trust, pressure, authority, communication style, awareness level and the victim’s response to manipulation. This makes their outcomes difficult to predict using traditional technical risk assessment methods.

A further challenge is that social engineering research is still developing in terms of rigorous modelling and quantitative evaluation. The paper notes that previous work has discussed detection, prevention, awareness and classification, but there is still a need to model persuasion principles and attacker steps more formally.

Aijaz and Nazir (2024) attempt to address this issue by breaking down SETs into structured components, including the attacker’s goal, communication modality, persuasion principle and affected asset. The Attack Tree Model is used to calculate AOP, while the Markov Chain Model is used to calculate ASP. This allows SETs to be assessed more systematically and supports risk ranking and policy decision-making.

### Key Challenges and Study Response

| Challenge | Why it is difficult | Study response |
|---|---|---|
| Human behaviour is unpredictable | Victims may respond differently depending on trust, pressure, workload and awareness | The study models persuasion principles and communication modalities as measurable factors |
| SETs can bypass technical controls | A secure system may still be compromised if the user is manipulated | The study focuses on human vulnerability as part of information security risk |
| Lack of formal modelling | SETs are often discussed qualitatively rather than quantitatively | The study calculates AOP and ASP using probabilistic models |
| Attacker steps are difficult to represent | Social engineering involves staged interaction between attacker and victim | The Markov Chain Model represents the attacker’s progress through defined states |
| Different channels have different risks | Email, voice call and face-to-face interaction vary in occurrence and effectiveness | The study compares modalities using occurrence and effectiveness probabilities |

---

## Question 2: Persuasion Principles and Modalities

Persuasion principles and modalities are central to the success of Social Engineering Threats because they explain how the attacker influences the victim and through which channel the attack is delivered. Persuasion principles such as authority, reciprocity and commitment increase the likelihood that the victim will comply with a malicious request. For example, an attacker may impersonate an IT support employee or a bank manager to create a sense of authority.

Modalities refer to the communication channels used in the attack, such as email, voice call or face-to-face interaction. These modalities differ in both frequency and effectiveness. Email may be more common because it is easy to send at scale, while face-to-face interaction may be less common but more persuasive because it involves direct human contact.

Analysing persuasion principles and modalities systematically is important because not all SETs carry the same level of risk. Some attacks may occur frequently but have a lower success rate, while others may occur less often but be more effective. This distinction helps organisations design targeted security awareness training, verification procedures and reporting policies.

### Persuasion Principles: Occurrence and Effectiveness

| Persuasion principle | Occurrence probability | Effectiveness probability | Interpretation |
|---|---:|---:|---|
| Authority | 0.63 | 0.63 | High occurrence and high effectiveness; victims may trust perceived authority figures |
| Commitment | 0.11 | 0.29 | Moderate occurrence and effectiveness; attackers may gradually build compliance |
| Reciprocity | 0.11 | 0.41 | Moderate occurrence but relatively strong effectiveness; victims may cooperate when the attacker appears helpful |
| Conformity | 0.01 | 0.45 | Low occurrence but potentially effective when victims believe others are complying |
| Scarcity | 0.006 | Not available | Low occurrence in the study’s dataset |
| Liking | 0.13 | Not available | Moderate occurrence, but effectiveness was not calculated in the study |

### Communication Modalities

| Modality | Occurrence probability | Effectiveness probability | Interpretation |
|---|---:|---:|---|
| Email | 0.50 | 0.20 | High occurrence but lower effectiveness; useful for scalable phishing attacks |
| Voice call | 0.40 | 0.30 | Moderate occurrence and effectiveness; allows direct interaction with the victim |
| Face-to-face | 0.10 | 0.40 | Low occurrence but higher effectiveness; direct human contact may increase trust |

---

## Question 3: Role of the Attack Tree Model and Markov Chain Model

The Attack Tree Model and Markov Chain Model play complementary roles in the study. The Attack Tree Model is used to estimate the **Attack Occurrence Probability (AOP)**. It decomposes a social engineering attack into smaller elements, such as communication modality and persuasion principle. These elements are treated as leaf nodes and combined through AND and OR relationships. This makes it possible to calculate how likely a particular SET pattern is to occur.

The Markov Chain Model is used to estimate the **Attack Success Probability (ASP)**. Instead of focusing on frequency, it represents the attacker’s progression through different states: Disconnect, Connect, Persuade and Success. The transition probabilities between these states depend on the effectiveness of the selected modality and persuasion principle. This helps estimate whether an attack is likely to move from initial contact to successful compromise.

The value of using both models is that the study separates occurrence from success. A social engineering attack may occur frequently but have a lower chance of success. In contrast, a less frequent attack may be more persuasive and therefore more likely to succeed.

### Comparison Between Attack Tree and Markov Chain Models

| Comparison point | Attack Tree Model | Markov Chain Model |
|---|---|---|
| Main purpose | Estimates Attack Occurrence Probability (AOP) | Estimates Attack Success Probability (ASP) |
| Main question | How likely is the attack to occur? | If the attack starts, how likely is it to succeed? |
| Focus | Frequency of attack components | Effectiveness of attack progression |
| Inputs | Modality frequency and persuasion principle frequency | Modality effectiveness and persuasion principle effectiveness |
| Structure | Root node, child nodes, leaf nodes and AND/OR gates | States and transition probabilities |
| Example elements | Email, voice call, authority and reciprocity | Disconnect, Connect, Persuade and Success |
| Output | AOP percentage | ASP percentage |
| Risk value | Identifies common SET patterns | Identifies successful SET patterns |
| Practical use | Helps prioritise likely attacks | Helps prioritise effective attacks |

### Methodology Flow

<img src="/assets/images/SRM/Unit8/Proposed%20methodology%20to%20compute%20attack%20occurrence%20and%20success%20probability.png" alt="Figure 1 - Methodology flow for modelling social engineering threats" width="800">

**Figure 1.** Methodology flow for modelling Social Engineering Threats using Attack Tree and Markov Chain models.

The methodology begins with knowledge identification, including modality, persuasion principle, frequency and affected asset. The Attack Tree Model is then used to compute AOP, while the Markov Chain Model is used to compute ASP. Together, these outputs can support risk ranking and policy decisions.

### Markov Chain Attack Progression

<img src="/assets/images/SRM/Unit8/Proposed%20Markov%20chain.png" alt="Figure 2 - Proposed Markov chain model" width="500">

**Figure 2.** Markov Chain attack progression from Disconnect to Connect, Persuade and Success.

The Markov Chain Model represents the attacker’s movement through four states. The model starts with Disconnect, moves to Connect when contact is established, progresses to Persuade when the attacker attempts manipulation, and reaches Success if the victim complies.

### AOP and ASP Results from the Ten Case Scenarios

<img src="/assets/images/SRM/Unit8/aop_asp_results.png" alt="Figure 3 - AOP and ASP results from ten social engineering case scenarios" width="800">

**Figure 3.** AOP and ASP results from ten Social Engineering Threat case scenarios.

| Case scenario | Attack pattern | AOP % | ASP % | Interpretation |
|---|---|---:|---:|---|
| CS1 | Email + Authority | 31.5 | 12.0 | Highest occurrence because both email and authority are frequent |
| CS2 | Email + Reciprocity | 5.5 | 7.7 | Lower occurrence and lower success compared with authority |
| CS3 | Email + Commitment | 5.5 | 8.4 | Similar occurrence to reciprocity, with slightly higher success |
| CS4 | Voice call + Authority | 25.2 | 11.4 | High occurrence due to authority and voice call use |
| CS5 | Voice call + Reciprocity | 4.4 | 10.0 | Lower occurrence but moderate success |
| CS6 | Voice call + Commitment | 4.4 | 10.9 | Lower occurrence but slightly higher success than CS5 |
| CS7 | Face-to-face + Authority | 6.3 | 16.0 | Lower occurrence but high success due to direct interaction |
| CS8 | Voice call/email + Authority/Reciprocity | 1.7 | 15.0 | Low occurrence but high success due to combined persuasion principles |
| CS9 | Voice call + Authority/Commitment | 1.1 | 18.0 | Highest success despite low occurrence |
| CS10 | Email + Commitment/Reciprocity | 0.3 | 15.0 | Very low occurrence but strong success probability |

The results show that single-principle attacks may have higher occurrence probability, especially where authority is involved. For example, email combined with authority has the highest AOP at 31.5%. However, attacks that combine more than one persuasion principle may have a higher ASP. For instance, the voice call attack using authority and commitment has a low AOP of 1.1%, but the highest ASP at 18.0%. This suggests that multi-principle attacks may be less common but more effective once the attacker engages with the victim.

---

## Question 4: Policy Framework Implications

The findings of the study can support the development of effective policy frameworks by helping organisations understand which social engineering patterns are more likely to occur and which are more likely to succeed. Instead of treating SETs as a general awareness problem, organisations can use AOP and ASP to prioritise security controls.

For example, if authority-based email or voice call attacks show high occurrence or success probability, organisations can introduce stricter identity verification procedures before employees respond to requests for sensitive information. This may include callback procedures, approval workflows and escalation channels. Similarly, if multi-principle attacks show higher success probability, awareness training should include realistic scenarios where attackers combine authority, reciprocity and commitment.

The distinction between AOP and ASP is also important for policy design. High-AOP attacks require broad preventive measures because they are likely to occur frequently. High-ASP attacks require targeted controls because they may be especially effective even if they occur less often.

### Policy Framework Applications

| Study finding | Policy implication |
|---|---|
| SETs exploit human vulnerability | Policies should include human-centred security controls, not only technical controls |
| Authority is a high-risk persuasion principle | Employees should verify requests from managers, IT teams, banks or external officials |
| Email has high occurrence | Email security awareness and phishing reporting should remain core controls |
| Face-to-face interaction has high effectiveness | Physical security and staff identification procedures should be included |
| AOP and ASP are different | Organisations should distinguish between frequent attacks and successful attacks |
| Multi-principle attacks can be highly effective | Training should include complex scenarios involving more than one persuasion technique |
| SETs can be ranked systematically | Security resources can be prioritised based on risk ranking |

### AOP and ASP Policy Implications

| Scenario type | Meaning | Policy priority |
|---|---|---|
| High AOP / Low ASP | The attack is common but less likely to succeed | Broad awareness and prevention |
| Low AOP / High ASP | The attack is less common but more effective | Targeted controls and specialist training |
| High AOP / High ASP | The attack is both common and effective | Immediate priority and layered controls |
| Low AOP / Low ASP | The attack is less common and less effective | Monitor and review periodically |

---

## Group Discussion Notes

This section will be completed after the group discussion.

### Main points discussed by the group

- 
- 
- 

### Points of agreement

- 
- 
- 

### Points of disagreement or critique

- 
- 
- 

### Questions raised during the discussion

- 
- 
- 

### Actions or learning points to carry forward

- 
- 
- 

---

## Critical Reflection

The study provides a useful and structured way to analyse Social Engineering Threats, but it also has limitations. The model focuses mainly on communication modalities and persuasion principles. However, real-world social engineering attacks may also depend on victim profile, organisational culture, workload, attacker capability and the specific context of the interaction.

Another limitation is that the study estimates occurrence and success probabilities, but it does not fully calculate impact or overall organisational risk. Therefore, the model is valuable as a starting point for understanding and ranking SETs, but it should be combined with stronger empirical evidence and organisational risk assessment before being used as the sole basis for policy decisions.

This limitation is important because an effective policy framework should consider not only the likelihood and success of an attack, but also the potential impact on confidentiality, integrity, availability, financial loss and organisational reputation.

---

## Reflection

This workshop activity strengthened my understanding of how social engineering threats can be modelled using probability-based methods. The key learning point was the distinction between attack occurrence and attack success. AOP shows how likely a social engineering attack pattern is to occur, while ASP shows how likely the attack is to succeed once it begins.

The activity also demonstrated the importance of analysing human factors in cybersecurity. Technical controls are important, but SETs show that attackers can exploit trust, authority and communication channels to bypass those controls. The use of Attack Tree and Markov Chain models provides a structured way to examine these human vulnerabilities and translate them into risk-informed policy decisions.

However, the activity also showed that probabilistic models depend heavily on the quality of their assumptions and input data. Therefore, such models should be used carefully and supported by organisational evidence, incident data and contextual risk assessment.

---

## References

Aijaz, M. and Nazir, M. (2024) ‘Modelling and analysis of social engineering threats using the attack tree and the Markov model’, *International Journal of Information Technology*, 16(2), pp. 1231–1238.
