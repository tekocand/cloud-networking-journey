# Trading Risk Rules

## Purpose
These are deterministic guardrails for trading decisions.
The LLM may analyze and explain, but these rules should control execution decisions if automation is ever added.

## Base Risk Framework
- Define max risk per trade before entry.
- Define max daily loss before session starts.
- Define max open exposure across positions.
- Define allowed number of simultaneous trades.
- Define invalidation before entry.
- Define target logic before entry.

## Non-Negotiables
1. No trade without invalidation.
2. No trade without predefined risk.
3. No averaging down unless explicitly part of a tested playbook.
4. No revenge trade after loss.
5. No size increase after emotional disruption.
6. No trade if news/event risk invalidates technical read.
7. No trade if setup cannot be explained in one clean thesis.

## Checklist Rules
Before any trade is considered valid:
- higher timeframe context checked
- event/news risk checked
- trigger defined
- stop/invalidation defined
- target defined
- R multiple estimated
- position size computed from rule-based risk

## Risk Questions To Answer
- What is the maximum loss on this idea?
- Is the stop structural or arbitrary?
- Is the expected reward enough for the stop distance?
- Does this trade fit a known playbook?
- Is the trader calm enough to execute the plan?

## Execution Separation
The advisor may suggest:
- setup quality
- better invalidation
- better target logic
- whether to wait

The advisor must not replace deterministic code for:
- sizing
- risk caps
- execution filters
- stop placement engine
- order submission
