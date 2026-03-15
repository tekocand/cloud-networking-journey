# Trading Modes

This file defines the clean entry points for the trading specialization.

## Use These Modes

### 1. trading:narrative
Use when you want market context first.

Best for:
- dominant market theme
- sentiment regime
- sector rotation
- crypto narrative shifts
- macro context
- what the market is rewarding or punishing

Example asks:
- "Yue, use trading:narrative for crypto today"
- "Yue, trading:narrative on US equities this week"

Expected output:
- dominant narrative
- sentiment
- sector/theme rotation
- event risk
- best-fit trading style

---

### 2. trading:screen
Use when you want ranked opportunities.

Best for:
- screening crypto or stocks
- breakout candidates
- momentum names
- pullback candidates
- theme-aligned opportunities

Example asks:
- "Yue, use trading:screen for crypto breakout setups"
- "Yue, trading:screen for AI-related names"

Expected output:
- ranked candidates
- trigger
- invalidation
- target logic
- risk
- score / 10
- verdict

---

### 3. trading:pretrade
Use before entering a trade.

Best for:
- setup validation
- invalidation check
- R profile check
- event-risk filter
- execution-readiness check

Example asks:
- "Yue, use trading:pretrade on this BTC setup"
- "Yue, pretrade-check this chart"

Expected output:
- bias
- setup quality
- trigger quality
- invalidation quality
- R estimate
- verdict: trade / wait / no trade

---

### 4. trading:analysis
Use for one deep setup breakdown.

Best for:
- one symbol
- one chart
- one thesis
- detailed structured view

Example asks:
- "Yue, use trading:analysis on ETH 4H"
- "Yue, analyze this setup with the trading framework"

Expected output:
- higher timeframe context
- trading timeframe context
- key levels
- entry plan
- invalidation plan
- target plan
- main risk
- confidence
- verdict

---

### 5. trading:review
Use after a trade is finished.

Best for:
- post-trade review
- process grading
- execution review
- emotional review

Example asks:
- "Yue, use trading:review on this closed trade"
- "Yue, review my execution on this setup"

Expected output:
- thesis quality
- entry quality
- stop quality
- exit quality
- discipline review
- repeat / remove
- final grade

---

### 6. trading:weekly
Use for end-of-week reflection.

Best for:
- weekly trading review
- narrative recap
- setup-class review
- discipline review
- next-week focus

Example asks:
- "Yue, use trading:weekly for this week"

Expected output:
- best narrative
- failed narrative
- best setup class
- weakest setup class
- edge quality
- lesson
- next-week focus

---

## Default Rule
If the request is trading-related but mode is unclear:
- use trading:narrative if context is missing
- use trading:pretrade if user is close to entry
- use trading:review if trade is already closed
- use trading:screen if user asks for opportunities

## Hard Rule
If a user asks for a trade idea without enough context, start with:
1. trading:narrative
2. then trading:screen or trading:analysis

Do not skip straight to entry suggestions when market context is missing.
