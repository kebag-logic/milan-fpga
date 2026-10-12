#!/usr/bin/env bash
# Scratch (M8a-1): the two long local gates CONTRIBUTING requires, unpiped, rc recorded.
set -u
L=$LANES/640-m8a
S=$VALIDATION_STORAGE/640m8a-a594/m81
G=$S/gates
export TMPDIR=$S/tmpdir PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH VERILATOR_JOBS=2 MAKEFLAGS=-j8
cd "$L" || exit 9
run() {
  local n=$1; shift
  "$@" > "$G/$n.log" 2>&1
  echo $? > "$G/$n.rc"
  printf '%s\t%s\trc=%s\n' "$(date -Is)" "$n" "$(cat "$G/$n.rc")" >> "$G/summary-long.tsv"
}
git rev-parse HEAD > "$G/long-head.txt"
case "${1:-}" in
  yosys) run yosys syn/yosys/run.sh ;;
  suites) mkdir -p "$G/suite-logs"; run run_all_suites scripts/run_all_suites.sh "$G/suite-logs" ;;
esac
git status --porcelain > "$G/long-status-${1:-none}.txt"
echo done > "$G/long-${1:-none}.done"
