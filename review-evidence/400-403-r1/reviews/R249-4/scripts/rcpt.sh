#!/usr/bin/env bash
# Usage: rcpt.sh <receipt-name> <command...>
# Runs the command in the candidate clone ($R249_CLONE, default: the current directory),
# writing combined output and the exit code to receipts/<name>.log and receipts/<name>.exit.
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
name="$1"; shift
clone="${R249_CLONE:-$PWD}"
log="$here/receipts/$name.log"
{
  echo "# cwd: $clone"
  echo "# head: $(git -C "$clone" rev-parse HEAD) tree: $(git -C "$clone" rev-parse 'HEAD^{tree}')"
  echo "# cmd: $*"
  echo "# start: $(date -u +%FT%TZ)"
} > "$log"
( cd "$clone" && "$@" ) >> "$log" 2>&1
rc=$?
echo "# end: $(date -u +%FT%TZ) exit=$rc" >> "$log"
echo "$rc" > "$here/receipts/$name.exit"
echo "$name exit=$rc"
exit 0
