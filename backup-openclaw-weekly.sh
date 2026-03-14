#!/usr/bin/env bash
set -euo pipefail

REPO="/home/openclaw/.openclaw/workspace"
BRANCH="backup/openclaw-weekly"
LOGFILE="/home/openclaw/.openclaw/workspace/.backup-openclaw-weekly.log"

cd "$REPO"

# Keep backup automation on a dedicated branch.
current_branch="$(git branch --show-current || true)"
if [ "$current_branch" != "$BRANCH" ]; then
  if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git checkout "$BRANCH" >/dev/null 2>&1
  else
    git checkout -b "$BRANCH" >/dev/null 2>&1
  fi
fi

# Sync with remote branch when available.
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  git pull --ff-only origin "$BRANCH" >/dev/null 2>&1 || true
fi

# Stage everything, then drop runtime/noise artifacts from the snapshot.
git add -A
git restore --staged backtest-dashboard/.watcher.pid 2>/dev/null || true
git restore --staged backtest-dashboard/.watcher.heartbeat 2>/dev/null || true
git restore --staged backtest-dashboard.pre-recovery-20260314-025044 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "Weekly OpenClaw backup $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1 || true
  git push -u origin "$BRANCH" >/dev/null 2>&1 || true
  echo "$(date): backup pushed to $BRANCH" >> "$LOGFILE"
else
  echo "$(date): no changes to back up" >> "$LOGFILE"
fi
