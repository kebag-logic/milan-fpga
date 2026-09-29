#!/usr/bin/env bash
# [R398-1] Portable mutation/probe runner for PR #133 at the exact head.
# Usage: run_arms.sh <head-tree> <arms-file> <out-dir> [jobs<=8]
#   head-tree : `git archive 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b` extracted
#   arms-file : lines "id|patch1,patch2|suite|group|expected-FAIL-substring|KILL or PASS"
#               patch paths are absolute or relative to the arms file's directory
#   VERILATOR : environment variable naming a Verilator 5.050 executable
# Every arm gets a fresh copy of hdl/ and tb/<suite>/, so arms never share state.
set -u
HEAD_TREE=$(readlink -f "$1"); ARMS=$(readlink -f "$2"); OUT=$(readlink -f "$3"); JOBS=${4:-8}
[ "$JOBS" -le 8 ] || JOBS=8
: "${VERILATOR:?set VERILATOR to a Verilator 5.050 executable}"
BASE=$(dirname "$ARMS"); WORK=${WORK:-$OUT/work}
mkdir -p "$OUT/logs" "$WORK"
one() {
  IFS='|' read -r id patches suite group expect mode <<<"$1"
  t="$WORK/$id"; rm -rf "$t"; mkdir -p "$t/tb"
  cp -r "$HEAD_TREE/hdl" "$t/hdl"; cp -r "$HEAD_TREE/tb/common" "$t/tb/common"; cp -r "$HEAD_TREE/tb/$suite" "$t/tb/$suite"; rm -rf "$t/tb/$suite/obj_dir"
  log="$OUT/logs/$id.log"; : > "$log"
  if [ -n "$patches" ]; then
    for p in ${patches//,/ }; do
      case "$p" in /*) pp=$p;; *) pp="$BASE/$p";; esac
      if ! (cd "$t" && patch -p1 --no-backup-if-mismatch < "$pp") >> "$log" 2>&1; then
        echo "$id: PATCH-FAILED"; return; fi
    done
  fi
  make -C "$t/tb/$suite" run VERILATOR="$VERILATOR" RUN_ARGS="$group" >> "$log" 2>&1; rc=$?
  tally=$(grep -E '^[0-9]+ checks:' "$log" | tail -1)
  nfail=$(grep -c '^FAIL:' "$log")
  hit=$(grep '^FAIL:' "$log" | grep -cF -- "$expect")
  if [ "$mode" = KILL ]; then
    if [ $rc -ne 0 ] && [ -n "$tally" ] && ! grep -q CYCLE_BUDGET "$log" && [ "$hit" -gt 0 ]; then v=KILLED; else v=SURVIVED-OR-UNPROVEN; fi
  else
    if [ $rc -eq 0 ] && [ -n "$tally" ] && [ "$nfail" -eq 0 ]; then v=PASS; else v=FAIL; fi
  fi
  tags=$(grep '^FAIL:' "$log" | sed -E 's/^FAIL: *([A-Za-z0-9 =]+[:]).*/\1/' | sort -u | tr '\n' ' ')
  echo "$id: mode=$mode rc=$rc fails=$nfail expected_hits=$hit verdict=$v tally=[$tally] tags=[$tags]"
}
export -f one; export HEAD_TREE OUT BASE WORK VERILATOR
grep -vE '^\s*(#|$)' "$ARMS" | xargs -d '\n' -P "$JOBS" -I{} bash -c 'one "$@"' _ {} | sort > "$OUT/summary.txt"
cat "$OUT/summary.txt"
