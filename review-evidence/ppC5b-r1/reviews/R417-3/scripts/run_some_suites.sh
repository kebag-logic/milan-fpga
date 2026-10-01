#!/usr/bin/env bash
# Reviewer copy of scripts/run_suites.sh's per-suite verdict, for a named subset of suites
# (so a sweep can be split into foreground chunks). usage: run_some_suites.sh <tree> <logdir> suite...
set -uo pipefail
T=$1; L=$2; shift 2; mkdir -p "$L"
for name in "$@"; do d=$T/tb/$name; [ -f "$d/Makefile" ] || { echo "NOSUITE $name"; continue; }
  s=$(date +%s); (cd "$d" && make) >"$L/$name.log" 2>&1; rc=$?; e=$(( $(date +%s) - s ))
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$L/$name.log" | tail -1) || tally=""
  if [ $rc -eq 0 ] && [ -n "$tally" ]; then echo "PASS $name ($tally) ${e}s"; elif [ $rc -eq 0 ]; then echo "UNREADABLE $name ${e}s"; else echo "FAIL $name rc=$rc ${e}s"; tail -5 "$L/$name.log" | sed 's/^/    /'; fi
done
