---
layout: post
title: Monte Carlo Simulation for Risk Modelling
subtitle: Using Python to model uncertainty through repeated dice game simulations
categories:
  - Security and Risk Management
tags: [unit7, risk-modelling, monte-carlo-simulation, python, probability, uncertainty]
---

## Overview

This post reflects on the formative activity based on Fizell’s (2022) Python-based Monte Carlo simulation exercise. The purpose of the activity was to examine how repeated random trials can be used to estimate uncertain outcomes and support risk modelling. Monte Carlo simulation is relevant to risk analysis because it produces a range of possible outcomes rather than a single fixed prediction. This is useful in contexts where probability, uncertainty and variability affect decision-making (Metropolis and Ulam, 1949).

## Summary of the Activity

The activity used a dice game to demonstrate the practical application of simulation. The Python code imported the required packages and defined a function to simulate rolling two dice. The function checked whether both dice produced the same number and returned either `True` or `False`. This provided the basic random event used throughout the simulation.

<img src="/assets/images/SRM/ImportingPackagesandDefiningtheDiceRollFunction.png" alt="Figure 1 - Importing packages and defining the dice roll function" width="800">

**Figure 1.** Importing packages and defining the dice roll function.

The model then set the number of simulations to 10,000, with each simulation containing 1,000 dice rolls. The tracking variables recorded the win probability and the ending balance after each simulation. Each run started with a balance of $1,000. If the dice matched, the balance increased by four times the bet. If the dice did not match, the balance decreased by the bet amount.

<img src="/assets/images/SRM/RunningtheMonteCarloSimulation.png" alt="Figure 2 - Running the Monte Carlo simulation" width="800">

**Figure 2.** Running the Monte Carlo simulation.

## Results and Interpretation

The simulation produced an average win probability of approximately 0.1666. This result is consistent with the probability of rolling matching numbers using two six-sided dice. The average ending balance was approximately $833.08 from an initial balance of $1,000. This indicates that, although some individual simulations produced higher balances, the overall trend showed a decline in the player’s balance over repeated rolls.

<img src="/assets/images/SRM/SimulatedBalanceAcross10,000Runs.png" alt="Figure 3 - Simulated balance across 10000 runs" width="800">

**Figure 3.** Simulated balance across 10,000 runs.

<img src="/assets/images/SRM/SummaryofAverageSimulationOutcomes.png" alt="Figure 4 - Summary of average simulation outcomes" width="800">

**Figure 4.** Summary of average simulation outcomes.

## Reflection

The activity demonstrates that Monte Carlo simulation can support risk modelling by showing how repeated random trials reveal expected patterns and possible losses. Instead of assuming one fixed result, the simulation shows a distribution of outcomes across many trials. However, the results depend on the assumptions used in the model, including the rules of the dice game, the initial balance, the bet value and the number of simulations. Therefore, Monte Carlo simulation should be treated as a decision-support method rather than a precise prediction tool. Overall, the activity strengthened understanding of how probability-based modelling can be applied to uncertainty and risk evaluation.

## References

Fizell, Z. (2022) ‘How to Create a Monte Carlo Simulation using Python’, *Towards Data Science*. Available at: https://towardsdatascience.com/how-to-create-a-monte-carlo-simulation-using-python-c24634a0978a/ (Accessed: 13 June 2026).

Metropolis, N. and Ulam, S. (1949) ‘The Monte Carlo method’, *Journal of the American Statistical Association*, 44(247), pp. 335–341.

