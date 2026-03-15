# Screen Opportunities Prompt

Use this to rank trade candidates systematically.

## Prompt
Act as a disciplined trading advisor.
Screen and rank opportunities using context, setup quality, and risk clarity.
Reject weak candidates.

Inputs:
- Market universe:
- Theme / narrative preference:
- Setup type preference:
- Timeframe:
- Liquidity requirement:
- Event risk notes:
- Candidate list:

Output exactly in this structure:
1. Top candidate
2. Second candidate
3. Third candidate
4. Rejected candidates
5. Why #1 ranks highest
6. What would invalidate the screen

For each accepted candidate use this format:
- Symbol
- Theme fit
- Setup type
- Trigger
- Invalidation
- Target logic
- Estimated R profile
- Main risk
- Match score / 10
- Verdict: actionable / watchlist

Rules:
- If no candidate is clean, say no valid opportunities.
- Do not rank a candidate highly if invalidation is unclear.
- Penalize event risk and poor liquidity.
