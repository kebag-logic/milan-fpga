#!/usr/bin/env bash
# usage: helper_camps.sh <tree> <primary out> <helper out> <jobs> <campaign ...>
# Takes the primary runner's remaining campaigns from the other end: before
# each one it stops if the primary has started it, else claims it (mkdir).
S=<scratch>
tree=$1; prim=$2; out=$3; jobs=$4; shift 4
mkdir -p "$out/claims"
for c in "$@"; do
  [ -e "$prim/$c.log" ] && break
  mkdir "$out/claims/$c" 2>/dev/null || break
  bash $S/scripts/run_camps.sh "$tree" "$out" "$jobs" "$c"
  rm -f "$out/ALL.done"
done
echo done > "$out/HELPER.done"
