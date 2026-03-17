# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## X Helpers

- `openclaw-x-follow-audit <username>` — navigates to `x.com/<username>` (skips navigation if already there) and samples the profile with a single JS call. Appends a JSONL entry to `logs/x-follow-audit.jsonl`. Returns one JSON line: `{"ts":…,"user":…,"following":"12 Following","followers":"3 Followers"}`.
- `openclaw-x-scope-handles [max_count]` — extracts visible candidate handles from the current X page. Use for "current X scope" work instead of reading scratch files like `x_scope_handles.txt`.
- `openclaw-x-profile-score <handle>` — opens `x.com/<handle>`, extracts bio plus recent post text, scores the account for finance-alpha usefulness, closes the opened tab, and returns JSON with `decision=follow|review|skip`, `score`, `matched_groups`, `reasons`, and `tab_closed`.
- `openclaw-x-follow-one <handle>` — navigates to `x.com/<handle>` and clicks the Follow button. Returns JSON: `{"handle":"…","result":"clicked|already_following|no_button|error","ts":"…","tab_closed":true|false}`. **This is the only follow command.** Never call `openclaw-x-follow` (does not exist).

## X Curation Procedure

### Tool usage critical rules
- Always use the **`exec` tool** for these helpers — never `process`. The `process` tool returns `(no output yet)` which loses the output.
- If `exec` returns "Command still running (session `<name>`, ...)", immediately call `process log <name>` to retrieve the output. The session name is the exact word from the current exec result — copy it verbatim, never reuse a session name from an earlier call.
- **Chat-originated curation requests must call the script**: When a user asks for curation from chat (`go for N accounts`, `continue`, `follow more`), respond with a single `exec: openclaw-yue-curation-run linnitless [max_accounts]` call. Default is 10; pass the user's requested count as the second arg (e.g. `openclaw-yue-curation-run linnitless 20` for 20 accounts). Do NOT manually loop through scope→score→follow steps in the chat session. The script is reliable; manual in-chat looping is not.
- If execution did not actually begin, say `not started` and give the exact blocker.
- Use `openclaw-yue-status` to verify whether Yue is `busy`, `idle`, or likely `stuck` before claiming batch progress.

### Per-batch steps (SERIAL: loop through ALL candidates one by one)
1. **Before snapshot** — if the caller script already ran the audit before this turn, use the shortcut: `exec tail -1 /home/openclaw/.openclaw/workspace/logs/x-follow-audit.jsonl`. Otherwise: `exec openclaw-x-follow-audit <username>`.
2. **Get candidates** — `exec openclaw-x-scope-handles 10` (get all available candidates).
3. **Loop serially** — for each candidate in order:
   - `exec openclaw-x-profile-score <candidate>` first.
   - Follow only if the score result is `decision=follow`, or `decision=review` with clear finance-alpha reasons.
   - `exec openclaw-x-follow-one <candidate>` only for approved candidates. This helper must close the tab it opened and return `tab_closed=true` on success.
   - Sleep 2 seconds before next
   - Do NOT use process loop or parallel execution; execute sequentially one by one
4. **After snapshot** — `exec openclaw-x-follow-audit <username>`.
5. **Report once** — after all candidates are processed, output final line with cumulative stats. Do not ask for approval per candidate; just complete all and report final results.

### Alpha selection rubric
- Prefer accounts with direct evidence of market research: macro, rates, liquidity, FX, on-chain, derivatives, order flow, earnings, valuation, sector/fundamental analysis.
- Prefer accounts with recent substantive posts, not just reposts or memes.
- Prefer cross-asset or specialist expertise over generic influencer vibes.
- Skip hard on spam/promo patterns: giveaway, airdrop, VIP, paid group, referral, copy-trade, pump language.
- Usually skip memecoin-only, NFT-only, gaming/lifestyle, and generic motivational accounts unless they clearly publish serious market research.
- If uncertain, bias to skip instead of polluting the feed with low-signal follows.

### Audit rules
- The audited `<username>` must be the logged-in posting account — **never** a candidate being visited (not `@self`, `@glassnode`, or any other inspected handle).
- Parse `before`/`after` from the numeric part of `"12 Following"`. A `null` title does not invalidate the snapshot.
- `follow_delta = after - before` (exact arithmetic, never inferred from attempted/succeeded).

### Final line format (required for every curation batch)
```
attempted=<n> succeeded=<n> failed=<n> before=<n|unknown> after=<n|unknown> follow_delta=<n|unknown>
```
- Use `follow_delta=`, never `delta=`.
- If audits are unavailable, use `unknown` and state the exact failure — do not guess.

### Batch size (SERIAL auto-loop until all done)
- Get ALL candidates with `openclaw-x-scope-handles` (no limit).
- Loop through every candidate serially, one by one, closing tabs between each follow.
- No approval per candidate; Yue processes all candidates and reports cumulative results once.
- One user confirmation = do all available candidates (not just one). User only confirms once at the start.

### Scope errors
- If `openclaw-x-scope-handles` returns no candidates: report `no visible handles in current X scope` and stop.
- Never read scratch files like `x_scope_handles.txt` or `following_audit_before.txt` unless Candra explicitly asked you to use that file in the current run.
