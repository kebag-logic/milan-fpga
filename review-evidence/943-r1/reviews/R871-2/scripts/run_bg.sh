#!/usr/bin/env bash
# run_bg.sh NAME CMD...: run CMD from the clone with this review's env, its log and rc under receipts/NAME.{log,rc}
P=$REVIEWS/943-r871-2-packet
C=$REVIEWS/r871-2-943
N=$1; shift
. "$P/scripts/env.sh"
cd "$C" || exit 3
{
  echo "# $* (clone HEAD $(git rev-parse HEAD), dirty $(git status --porcelain --untracked-files=all | wc -l), start $(date -u +%FT%TZ))"
  start=$(date +%s)
  "$@"
  rc=$?
  echo "# rc=$rc elapsed=$(( $(date +%s) - start ))s dirty-after $(git status --porcelain --untracked-files=all | wc -l)"
  echo $rc > "$P/receipts/$N.rc"
} > "$P/receipts/$N.log" 2>&1
