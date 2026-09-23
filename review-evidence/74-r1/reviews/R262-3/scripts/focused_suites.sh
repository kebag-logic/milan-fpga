#!/usr/bin/env bash
# Run the two suites whose inputs this PR changes, at the candidate, the way
# the candidate's own sweep runs one suite: under scripts/owned_process.py,
# `timeout <suite budget> make -C tb/verilator/<suite>`, then the sweep's
# masked-verdict recogniser `suite_tally.py --verdict` on the log.
# Parallelism: pinned to 8 CPUs (Verilator's -j 0 follows the affinity mask).
# usage: focused_suites.sh <clone> <out-dir> <verilator>
set -u
clone=$1; out=$2; vl=$3
mkdir -p "$out"; cd "$clone" || exit 2
"$vl" --version > "$out/verilator-version.txt" 2>&1
: > "$out/suites.tsv"
for suite in media_grid_align chmap_capture; do
  make -C "tb/verilator/$suite" clean > /dev/null 2>&1
  start=$(date +%s)
  taskset -c 0-7 python3 scripts/owned_process.py -- \
    timeout 1800 make -C "tb/verilator/$suite" VERILATOR="$vl" > "$out/$suite.log" 2>&1
  rc=$?
  secs=$(( $(date +%s) - start ))
  python3 scripts/suite_tally.py --verdict "$out/$suite.log" > "$out/$suite.verdict" 2>&1
  vrc=$?
  printf '%s\tmake_rc=%s\tverdict_rc=%s\twall_s=%s\n' "$suite" "$rc" "$vrc" "$secs" >> "$out/suites.tsv"
done
python3 scripts/suite_tally.py "$out" > "$out/tally.txt" 2>&1; echo "tally_rc=$?" >> "$out/tally.txt"
