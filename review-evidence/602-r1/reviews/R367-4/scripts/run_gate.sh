#!/usr/bin/env bash
# Usage: run_gate.sh <receipt-dir> <name> <timeout-seconds> <command...>
# Runs one gate from the candidate root ($REPO) and writes <name>.log with a
# header (command, head, tree, start/end, rc) plus <name>.rc.
set -u
out=$1; name=$2; limit=$3; shift 3
repo=${REPO:?set REPO to the candidate clone}
mkdir -p "$out"
log="$out/$name.log"
{
  printf 'command: %s\n' "$*"
  printf 'head: %s\n' "$(git -C "$repo" rev-parse HEAD)"
  printf 'tree: %s\n' "$(git -C "$repo" rev-parse 'HEAD^{tree}')"
  printf 'start: %s\n' "$(date -u +%FT%TZ)"
  printf -- '----\n'
} > "$log"
start=$(date +%s)
( cd "$repo" && timeout --kill-after=60 "$limit" "$@" ) >> "$log" 2>&1
rc=$?
end=$(date +%s)
printf -- '----\nend: %s\nseconds: %s\nrc: %s\n' "$(date -u +%FT%TZ)" "$((end-start))" "$rc" >> "$log"
printf '%s\n' "$rc" > "$out/$name.rc"
printf '%-40s rc=%s %ss\n' "$name" "$rc" "$((end-start))"
