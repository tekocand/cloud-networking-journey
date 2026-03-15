# Trading System Overview

## Structure
This trading system has four layers:

### 1. Base Layer
General Yue behavior lives in `SOUL.md`.
This keeps the main assistant usable for normal chat, coding, admin work, and life stuff.

### 2. Specialist Layer
Core trading behavior lives in:
- `agent-spec.md`
- `risk-rules.md`
- `playbook.md`

### 3. Workflow Layer
Reusable workflows live in:
- `modes.md`
- `usage.md`
- `routines.md`
- `output-formats.md`
- `prompts/`

### 4. Market Intelligence Layer
Context-first analysis lives in:
- `market-intelligence.md`
- `screening-framework.md`

## Philosophy
This system is built to:
- improve process
- improve market context
- improve decision quality
- reduce weak trades
- improve review quality

It is not built to:
- act like an execution bot
- pretend certainty
- generate random trade ideas without context

## Golden Rule
Context first.
Then screening.
Then setup quality.
Then execution readiness.
Never reverse that order.
