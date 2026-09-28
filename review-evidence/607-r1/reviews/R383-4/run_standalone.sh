#!/usr/bin/env bash
# Standalone #607/#395/#595 builder tests on a candidate tree, in a named interpreter environment.
# Usage: run_standalone.sh <tree> <packet> <label> <python> [pins-home]
set -u
T=$1; PKT=$2; LBL=$3; PY=$4; PH=${5:-}
export PATH="$PKT/scratch/bin:$PATH" PYTHONHASHSEED=0
if [ -n "$PH" ]; then export HOME=$PH; export PATH="$(dirname "$PY"):$PKT/scratch/bin:/usr/bin:/bin"; unset MILAN_LITEX_PYTHON; fi
cd "$T"
OUT=$PKT/receipts/40_standalone_$LBL.tsv; : > "$OUT"
run() { local n=$1; shift; local t0=$(date +%s); "$@" > "$PKT/receipts/40_${LBL}_$n.log" 2>&1; local rc=$?
  printf '%s\t%s\t%ss\t%s\n' "$n" "$rc" "$(( $(date +%s)-t0 ))" "$(git rev-parse HEAD)" >> "$OUT"; }
run test_declarations            "$PY" -B sw/builder/test_declarations.py
run test_timing_grade            "$PY" -B sw/builder/test_timing_grade.py "$PY"
run test_shipping_clock_constraints "$PY" -B sw/builder/test_shipping_clock_constraints.py
run test_clock_constraints       "$PY" -B sw/builder/test_clock_constraints.py
cat "$OUT"
