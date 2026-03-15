# Pre-Trade Checklist Prompt

Use this prompt when reviewing a possible trade before entry.

## Prompt
Analyze this setup using the trading advisor framework.

Required fields:
- Market / symbol:
- Timeframe:
- Thesis:
- Entry zone:
- Invalidation / stop:
- Target(s):
- Risk per trade:
- News / event context:
- Screenshot / chart notes:

Output exactly in this structure:
1. Bias
2. Market context
3. Setup quality
4. Trigger quality
5. Invalidation quality
6. Target quality
7. Estimated R multiple
8. Event risk
9. Missing information
10. Verdict: trade / wait / no trade
11. Why

Rules:
- If invalidation is weak, verdict cannot be trade.
- If reward is unclear, verdict cannot be trade.
- If context is missing, say incomplete instead of guessing.
- Prefer no trade over forcing a setup.
