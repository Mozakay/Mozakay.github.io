---
layout: post
title: Think Bayes 2 Probability and Bayesian Updating
subtitle: Completing Chapter 1 and Chapter 2 exercises using conditional probability and Bayesian tables
categories: ["Security and Risk Management"]
tags: [unit7, think-bayes, probability, bayesian-updating, conditional-probability, risk-modelling, python]
---

## Overview

This post reflects on the formative activity based on Downey’s (2022) *Think Bayes 2*. The activity required the completion of the exercises labelled Chapter 1 and Chapter 2. The purpose of the work was to develop an applied understanding of probability, conditional probability and Bayesian updating. These concepts are relevant to risk modelling because risk assessment often requires the interpretation of uncertain evidence and the revision of probability estimates when new information becomes available.

## Chapter 1: Probability and Conditional Probability

Chapter 1 introduced probability using practical examples based on survey data. The exercises required the use of `prob` and `conditional` to calculate single probabilities, combined probabilities and conditional probabilities. A key learning point was that the order of arguments in conditional probability changes the meaning of the result. For example, the probability that a respondent is liberal given that they are a Democrat is not the same as the probability that a respondent is a Democrat given that they are liberal.

<img src="/assets/images/SRM/Downey/Conditional%20Probability%20between%20Political%20Identity%20and%20Liberal%20Views.png" alt="Figure 1 - Conditional probability between political identity and liberal views" width="800">

**Figure 1.** Conditional probability between political identity and liberal views.

The exercises also included a variation of the Linda problem. The results showed that the probability of Linda being a banker, given that she is female, was higher than the probability of Linda being a banker and a liberal Democrat. This demonstrates the conjunction rule, where a combined event cannot be more probable than one of its individual components.

<img src="/assets/images/SRM/Downey/Linda%20Problem%20and%20the%20Conjunction%20Rule.png" alt="Figure 2 - Linda problem and the conjunction rule" width="800">

**Figure 2.** Linda problem and the conjunction rule.

The final Chapter 1 exercises examined relationships between age groups and political views. The notebook defined young respondents as those under 30 and old respondents as those aged 65 or above. It also defined conservative respondents based on selected political view categories.

<img src="/assets/images/SRM/Downey/Defining%20Age%20and%20Political%20View%20Categories.png" alt="Figure 3 - Defining age and political view categories" width="800">

**Figure 3.** Defining age and political view categories.

The results showed that approximately 0.0658 of respondents were both young and liberal, while the probability that a young respondent was liberal was approximately 0.3385. The results also showed that approximately 0.0670 of respondents were old conservatives, while approximately 0.1959 of conservatives were old. These results demonstrate the difference between a conjunction and a conditional probability.

<img src="/assets/images/SRM/Downey/Probability%20and%20Conditional%20Probability%20Exercises%20for%20Age%20and%20Political%20Views.png" alt="Figure 4 - Probability and conditional probability exercises for age and political views" width="800">

**Figure 4.** Probability and conditional probability exercises for age and political views.

## Chapter 2: Bayes’s Theorem and Bayesian Tables

Chapter 2 introduced Bayesian updating through table-based examples. Bayesian reasoning is useful because it allows prior probabilities to be revised after new evidence is observed. In the first exercise, the table compared a normal coin with a trick coin. After observing heads, the posterior probability of having chosen the trick coin was updated to 2/3. This shows how evidence can change the probability assigned to each hypothesis.

<img src="/assets/images/SRM/Downey/Bayesian%20Updating%20for%20the%20Trick%20Coin%20Problem.png" alt="Figure 5 - Bayesian updating for the trick coin problem" width="800">

**Figure 5.** Bayesian updating for the trick coin problem.

The second exercise considered the two children problem. Starting with four equally likely hypotheses, the evidence that at least one child is a girl removed the boy-boy possibility. The posterior probability that both children are girls was therefore 1/3.

<img src="/assets/images/SRM/Downey/Bayesian%20Table%20for%20the%20Two%20Children%20Problem.png" alt="Figure 6 - Bayesian table for the two children problem" width="800">

**Figure 6.** Bayesian table for the two children problem.

The Monty Hall exercise demonstrated how the probability depends on the host’s decision rule. When Door 2 was opened, the probability that the car was behind Door 3 became 1/2. When Door 3 was opened, the probability that the car was behind Door 2 became 1. This illustrates that Bayesian reasoning depends not only on the observed evidence, but also on the process that generated the evidence.

<img src="/assets/images/SRM/Downey/Monty%20Hall%20Problem%20with%20Conditional%20Door%20Selection.png" alt="Figure 7 - Monty Hall problem with conditional door selection" width="800">

**Figure 7.** Monty Hall problem with conditional door selection.

The final Chapter 2 exercise used the M&M colour problem to compare two hypotheses about which bag came from 1994 and which came from 1996. After observing one yellow and one green M&M, the posterior probability that the yellow M&M came from the 1994 bag was approximately 0.7407.

<img src="/assets/images/SRM/Downey/Bayesian%20Updating%20for%20the%20M%26M%20Colour%20Problem.png" alt="Figure 8 - Bayesian updating for the M&M colour problem" width="800">

**Figure 8.** Bayesian updating for the M&M colour problem.

## Reflection

The Think Bayes 2 exercises strengthened understanding of how probability can be used to reason under uncertainty. Chapter 1 demonstrated the importance of distinguishing between ordinary probability, conjunctions and conditional probability. Chapter 2 extended this understanding by showing how prior probabilities can be updated when evidence is introduced. This is directly relevant to risk modelling because risk decisions often require the evaluation of incomplete or changing information. However, the exercises also show that probability estimates depend on how hypotheses, data and likelihoods are defined. Therefore, Bayesian analysis should be applied carefully, with attention to assumptions and the interpretation of evidence.

## References

Downey, A. (2022) *Think Bayes: Bayesian Statistics in Python*. 2nd edn. Available at: https://allendowney.github.io/ThinkBayes2/ (Accessed: 13 June 2026).
