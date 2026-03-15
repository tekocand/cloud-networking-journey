#!/usr/bin/env bash
set -euo pipefail

REPO="/home/openclaw/.openclaw/workspace/backtest-dashboard"
BRANCH="backup/dashboard-weekly"
LOGFILE="$REPO/.backup-dashboard-weekly.log"

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

# Sync branch from origin when present.
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  git pull --ff-only origin "$BRANCH" >/dev/null 2>&1 || true
fi

# Stage everything, then unstage runtime noise files.
git add -A
git restore --staged .watcher.pid 2>/dev/null || true
git restore --staged .watcher.heartbeat 2>/dev/null || true

if ! git diff --cached --quiet; then
  commit_status="skipped"
  if git commit -m "Weekly dashboard backup $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1; then
    commit_status="committed"
  fi

  origin_status="fail"
  if git push -u origin "$BRANCH" >/dev/null 2>&1; then
    origin_status="ok"
  fi

  personal_status="n/a"
  if git remote get-url personal >/dev/null 2>&1; then
    if git push -u personal "$BRANCH" >/dev/null 2>&1; then
      personal_status="ok"
    else
      personal_status="fail"
    fi
  fi

  echo "$(date): branch=$BRANCH commit=$commit_status origin=$origin_status personal=$personal_status" >> "$LOGFILE"
else
  echo "$(date): no changes to back up" >> "$LOGFILE"
fi
