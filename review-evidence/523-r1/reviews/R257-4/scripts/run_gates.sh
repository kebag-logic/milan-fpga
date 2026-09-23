#!/usr/bin/env bash
# Run the composition-relevant gates on a candidate checkout, one receipt per
# command. Usage: run_gates.sh <repo> <receipt-dir> <list-file>
# <list-file>: one "<name>|<command>" per line; the command runs in <repo>.
# Each receipt records the command, exit code, wall seconds and full output.
set -u
repo=$1
out=$2
list=$3
mkdir -p "$out"
summary="$out/SUMMARY.txt"
: > "$summary"
while IFS='|' read -r name cmd; do
  case "$name" in ''|'#'*) continue ;; esac
  log="$out/$name.log"
  start=$(date +%s.%N)
  ( cd "$repo" && bash -c "$cmd" ) > "$log.body" 2>&1 < /dev/null
  rc=$?
  end=$(date +%s.%N)
  secs=$(awk -v a="$start" -v b="$end" 'BEGIN{printf "%.1f", b-a}')
  { printf 'command: %s\nexit: %s\nseconds: %s\n----\n' "$cmd" "$rc" "$secs"; cat "$log.body"; } > "$log"
  rm -f "$log.body"
  printf '%-40s exit=%-3s %6ss  %s\n' "$name" "$rc" "$secs" "$cmd" | tee -a "$summary"
done < "$list"
