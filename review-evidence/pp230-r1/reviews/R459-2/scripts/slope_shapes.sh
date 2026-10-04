#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# slope_shapes.sh JOBS: each committed slope patch (tb/srp_top/mutations)
# applied to a fresh `git archive` of the head, the committed srp_admission
# suite run ONE shape at a time (N = 1, 2, 3, 5, 8), so every shape's
# failing-check count is measured (the suite's own `shapes` target stops at
# the first failing shape).
set -u
J=${1:-3}
P=${P:-$(cd "$(dirname "$0")/.." && pwd)}
. "$P/scripts/env.sh"
CLONE=${CLONE:?set CLONE to a clone that holds the exact head}
T=$S/slope; rm -rf "$T"; mkdir -p "$T"
jobs=$T/jobs.txt; : > "$jobs"
for m in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  for n in 1 2 3 5 8; do
    d=$T/$m-N$n; mkdir -p "$d"
    git -C "$CLONE" archive "$HEAD" hdl tb/common tb/srp_admission tb/srp_top/mutations | tar -x -C "$d"
    (cd "$d" && git apply --check "tb/srp_top/mutations/$m.patch" && git apply "tb/srp_top/mutations/$m.patch") || { echo "apply failed $m"; exit 1; }
    echo "$d $n" >> "$jobs"
  done
done
xargs -P "$J" -L 1 bash -c 'make -C "$0/tb/srp_admission" run N=$1 > "$0/run.log" 2>&1; echo $? > "$0/run.rc"' < "$jobs"
for d in $(cut -d" " -f1 "$jobs"); do
  printf '%s rc=%s fails=%s %s\n' "$(basename "$d")" "$(cat "$d/run.rc")" \
    "$(grep -c '^FAIL' "$d/run.log")" "$(grep 'checks:' "$d/run.log" | tail -1)"
done
