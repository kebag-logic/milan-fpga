#!/usr/bin/env bash
# Time syn/yosys/run.sh end to end in extracted trees, one run at a time.
# usage: time_gate.sh <out-dir> <label>=<tree>[:<YOSYS_MALLOC>] ...
# Each run's stdout+stderr goes to <out-dir>/<label>.log; one TSV line per run
# (label, rc, wall seconds, peak RSS KiB of the largest child) to <out-dir>/times.tsv.
set -uo pipefail
out=$1; shift
mkdir -p "$out"
for spec in "$@"; do
  label=${spec%%=*}; rest=${spec#*=}
  tree=${rest%%:*}; mal=""
  [ "$rest" != "$tree" ] && mal=${rest#*:}
  t0=$(date +%s.%N)
  if [ -n "$mal" ]; then
    YOSYS_MALLOC=$mal /usr/bin/time -f '%M' -o "$out/$label.rss" "$tree/syn/yosys/run.sh" >"$out/$label.log" 2>&1; rc=$?
  else
    (unset YOSYS_MALLOC; /usr/bin/time -f '%M' -o "$out/$label.rss" "$tree/syn/yosys/run.sh") >"$out/$label.log" 2>&1; rc=$?
  fi
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$label" "$rc" "$(echo "$t1 - $t0" | bc)" "$(tail -1 "$out/$label.rss")" | tee -a "$out/times.tsv"
done
