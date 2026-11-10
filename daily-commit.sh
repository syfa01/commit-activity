#!/usr/bin/env bash
# Commit harian buat jaga streak contribution graph.
# Pasang di cron: 0 9 * * * /path/ke/commit-activity/daily-commit.sh
set -euo pipefail

cd "$(dirname "$0")"

STAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "$STAMP | daily keep-alive" >> activity.log
git add activity.log
git commit -m "chore: daily activity $(date '+%Y-%m-%d')" >/dev/null
git push origin "$(git rev-parse --abbrev-ref HEAD)" >/dev/null 2>&1 || echo "push gagal (cek kredensial)"
