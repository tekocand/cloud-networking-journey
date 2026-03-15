# Trading Playbook Skeleton

Use this file to define your real setups over time.
The trading advisor should rely on these definitions instead of improvising.

## Suggested Setup Template
For each setup, record:
- setup name
- market conditions
- timeframe
- trigger condition
- invalidation logic
- target logic
- expected R range
- common failure mode
- example chart notes

## Example Setup Definition
### 1. Trend Pullback
- Market conditions: higher timeframe trend intact
- Timeframe: define explicitly
- Trigger: pullback into key area + reclaim / confirmation
- Invalidation: below structural low / above structural high for shorts
- Target logic: trend continuation target, liquidity target, or prior impulse extension
- Expected R range: 2R to 4R
- Failure mode: late entry after extension, weak pullback structure, event risk against thesis

### 2. Range Rejection
- Market conditions: clear range boundaries, no major breakout context
- Trigger: rejection from edge with confirmation
- Invalidation: clean break beyond range boundary
- Target logic: mid-range first, opposite side second
- Expected R range: 1.5R to 3R
- Failure mode: breakout environment mistaken for range environment

### 3. Breakout Continuation
- Market conditions: compression + clear breakout catalyst
- Trigger: breakout and hold / retest hold
- Invalidation: failed hold back inside range
- Target logic: measured move, liquidity sweep target, prior volatility expansion target
- Expected R range: 2R+
- Failure mode: false breakout in low participation

## Use Rule
If a trade does not fit a defined setup, the advisor should say so explicitly.
