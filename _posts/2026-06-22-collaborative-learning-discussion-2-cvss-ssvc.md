---
layout: post
title: "Collaborative Learning Discussion 2: CVSS and SSVC"
subtitle: "Reflecting on CVSS scoring inconsistencies and stakeholder-specific vulnerability prioritisation"
categories: ["Security and Risk Management"]
tags: [unit7, collaborative-learning, cvss, ssvc, vulnerability-management, peer-feedback, reflection]
---

## Overview

This post presents evidence of my participation in **Collaborative Learning Discussion 2**. The discussion focused on Wunder et al. (2024) and their critique of the Common Vulnerability Scoring System (CVSS). The activity required students to evaluate the limitations of CVSS and consider whether an alternative approach, such as Stakeholder-Specific Vulnerability Categorization (SSVC), could provide a better basis for vulnerability prioritisation.

This activity was relevant to Security and Risk Management because vulnerability scoring is often used to support remediation decisions. However, if scoring is inconsistent or used without organisational context, security teams may prioritise vulnerabilities inefficiently.

---

## Initial Post Summary

My initial post argued that CVSS is useful for communicating technical severity, but it has limitations when used as the main basis for vulnerability prioritisation. Wunder et al. (2024) criticise CVSS because different evaluators may assign different values to the same vulnerability. The study identifies several problematic characteristics, including reliance on human interpretation, ambiguity in metric definitions and inconsistent use of metrics such as Attack Vector, User Interaction and Scope.

The post also argued that CVSS should not be treated as a complete risk assessment method. It provides a severity score, but it does not fully capture exploit status, exposure, asset criticality, business impact or stakeholder-specific priorities. As an alternative, SSVC was proposed because it is more decision-oriented than score-oriented. SSVC uses stakeholder-specific decision trees to guide practical response decisions, such as whether to defer, track, schedule or act.

---

## Peer Responses Received

| Peer response | Main point raised | How it developed the discussion |
|---|---|---|
| Sèba Daher | The response supported the separation between CVSS for severity communication and SSVC for prioritisation, but also noted that SSVC still requires empirical validation and clear decision points. | This helped strengthen the argument by recognising that SSVC is useful but not perfect. It still requires careful implementation and validation. |
| Payman Ghorbani | The response agreed that CVSS can be inconsistent, but questioned whether replacing CVSS entirely could create communication challenges between vendors, security teams and regulators. | This helped refine the conclusion toward a combined approach rather than fully dismissing CVSS. |
| Sopheaktra Chea | The response supported the use of SSVC to reduce wasted remediation effort and highlighted the need for contextual risk mapping and clear internal communication procedures. | This reinforced the practical value of SSVC when supported by organisational context, asset inventories and clear processes. |

---

## My Peer Responses

| My response | Main argument | Learning value |
|---|---|---|
| Response to Payman Ghorbani | I agreed that CVSS should not be used as a standalone prioritisation method and argued that SSVC can support prioritisation while CVSS remains useful for severity communication. | This response helped me explain a balanced position that combines standardised severity communication with contextual decision-making. |
| Response to Sèba Daher | I discussed the need to avoid relying on CVSS Base Scores alone and suggested clearer scoring guidance, calibration sessions and SSVC decision trees. | This helped me focus on practical preventive measures that could reduce inconsistent vulnerability assessment. |
| Response to Sopheaktra Chea | I highlighted that CVSS inconsistency could be reduced through better guidance, official documentation, and using SSVC as part of a structured vulnerability management process. | This response helped me connect academic critique with operational improvements. |

---

## Key Themes from the Discussion

The discussion highlighted four important themes. First, CVSS remains useful as a shared technical language for communicating vulnerability severity. Second, CVSS should not be used alone for remediation prioritisation because it does not fully reflect organisational risk. Third, SSVC provides a more practical decision-making structure, but it still depends on analyst judgement and clear decision criteria. Finally, a combined approach may be more realistic, where CVSS supports severity communication and SSVC supports prioritisation decisions.

---

## Summary Post

The discussion on CVSS highlighted the importance of distinguishing between technical severity, risk and vulnerability prioritisation. The initial post argued that Wunder et al. (2024) criticise CVSS because it does not always produce consistent scores across evaluators. The study identifies Attack Vector, User Interaction and Scope as problematic metrics, as their interpretation may vary between analysts. This matters because vulnerability management decisions often rely on scoring outputs, and inconsistent scores may lead to inefficient remediation priorities.

The peer feedback helped develop a more balanced view of the issue. One response supported the argument that SSVC offers a more decision-focused approach than CVSS, but also noted that SSVC may still depend on analyst judgement at decision points. This is an important limitation because a decision-tree approach does not automatically remove subjectivity. Another peer response suggested that CVSS may remain useful for communicating technical severity, while SSVC could be used internally to support prioritisation. This feedback strengthened the conclusion that CVSS should not be dismissed entirely. Instead, its role should be limited to severity communication, while other methods should support risk-informed response decisions.

The academic literature supports this balanced position. Spring et al. (2021) argue that CVSS has limitations when it is used beyond severity assessment, particularly because it does not sufficiently account for context, consequences or stakeholder-specific priorities. SSVC addresses this weakness by using stakeholder-specific decision trees to guide vulnerability response decisions (Spring et al., 2020). Therefore, the key learning from the discussion is that effective vulnerability management should not rely on a single numerical score. A more balanced approach would combine CVSS for severity communication, SSVC for prioritisation, and organisational context for risk-informed decision-making.

---

## Evidence of Discussion

### Initial post and summary post

<img src="/assets/images/SRM/Unit7/Initial%20Post.png" alt="Screenshot of the initial post for Collaborative Learning Discussion 2" width="800">

**Figure 1.** Initial post for Collaborative Learning Discussion 2.

<img src="/assets/images/SRM/Unit7/Summary%20Post.png" alt="Screenshot of the summary post for Collaborative Learning Discussion 2" width="800">

**Figure 2.** Summary post for Collaborative Learning Discussion 2.

### Peer responses received

<img src="/assets/images/SRM/Unit7/Peer%20Response%20by%20seba%20daher.png" alt="Peer response by Sèba Daher" width="800">

**Figure 3.** Peer response received from Sèba Daher.

<img src="/assets/images/SRM/Unit7/Peer%20Response%20by%20%20Payman%20Ghorbani.png" alt="Peer response by Payman Ghorbani" width="800">

**Figure 4.** Peer response received from Payman Ghorbani.

<img src="/assets/images/SRM/Unit7/Peer%20Response%20by%20Sopheaktra%20Chea.png" alt="Peer response by Sopheaktra Chea" width="800">

**Figure 5.** Peer response received from Sopheaktra Chea.

### My peer responses

<img src="/assets/images/SRM/Unit7/My%20Peer%20Response%20to%20Payman%20Ghorbani.png" alt="My peer response to Payman Ghorbani" width="800">

**Figure 6.** My peer response to Payman Ghorbani.

<img src="/assets/images/SRM/Unit7/My%20Peer%20Response%20to%20seba%20daher.png" alt="My peer response to Sèba Daher" width="800">

**Figure 7.** My peer response to Sèba Daher.

<img src="/assets/images/SRM/Unit7/My%20Peer%20Response%20to%20Sopheaktra%20Chea.png" alt="My peer response to Sopheaktra Chea" width="800">

**Figure 8.** My peer response to Sopheaktra Chea.

---

## Reflection

This activity improved my understanding of the difference between vulnerability severity and vulnerability prioritisation. Before the discussion, my argument focused mainly on the limitations of CVSS and the benefits of SSVC. However, the peer responses helped me develop a more balanced view. CVSS still has value as a common language for communicating technical severity, but it should not be used alone to decide remediation priorities.

The discussion also showed that alternative models such as SSVC are not free from limitations. Although SSVC is more decision-focused, it still requires clear definitions, consistent judgement and organisational context. This helped me understand that effective vulnerability management should combine technical scoring, exploit likelihood, asset importance, stakeholder impact and business context.

Overall, the discussion strengthened my ability to evaluate security frameworks critically rather than accepting or rejecting them completely. It also demonstrated the value of peer feedback in improving academic reasoning and developing more practical security recommendations.

---

## References

Spring, J.M., Hatleback, E., Householder, A., Manion, A. and Shick, D. (2020) ‘Prioritizing vulnerability response: A stakeholder-specific vulnerability categorization (Version 1.1)’, *Workshop on the Economics of Information Security*.

Spring, J.M., Hatleback, E., Householder, A., Manion, A. and Shick, D. (2021) ‘Time to change the CVSS?’, *IEEE Security & Privacy*, 19(2), pp. 74–78. doi: 10.1109/MSEC.2020.3044475.

Wunder, J., Kurtz, A., Eichenmüller, C., Gassmann, F. and Benenson, Z. (2024) ‘Shedding light on CVSS scoring inconsistencies: A user-centric study on evaluating widespread security vulnerabilities’, *2024 IEEE Symposium on Security and Privacy (SP)*, pp. 1102–1121. doi: 10.1109/SP54263.2024.00058.
