#!/usr/bin/env bash
# Usage: run_receipt.sh <name> <workdir> <cmd...>
# Runs cmd in workdir in the foreground, writes receipts/<name>.log and
# receipts/<name>.rc (exit status, UTC start/end, exact argv, head).
set -u
PKT="$(cd "$(dirname "$0")/.." && pwd)"
name="$1"; wd="$2"; shift 2
log="$PKT/receipts/$name.log"; meta="$PKT/receipts/$name.rc"
start="$(date -u +%FT%TZ)"
( cd "$wd" && "$@" ) >"$log" 2>&1
rc=$?
{ echo "name=$name"; echo "cwd=$wd"; printf 'argv='; printf '%q ' "$@"; echo
  echo "head=$(git -C "$wd" rev-parse HEAD 2>/dev/null)"; echo "start=$start"
  echo "end=$(date -u +%FT%TZ)"; echo "rc=$rc"; } >"$meta"
echo "$name rc=$rc"
exit 0
