#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Focused donor gates whose inputs the change touches, on a fresh export of
# the head: the PHC contract, the uCPU and tsngen suites (their tracked
# images changed), engine and bench lint, and the documentation and diagram
# checks. Build parallelism is capped at 8 by scripts/bin/verilator.
set -eu
. "$(dirname "$0")/env.sh"
tree="$SCRATCH/gates_tree"
rm -rf "$tree"; mkdir -p "$tree"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$tree"
echo "# verilator: $(verilator --version); head $HEAD_SHA"
cd "$tree"
st=0
for step in "contract" "ucpu" "tsngen" "lint" "docs"; do
  echo "=== $step"
  rc=0
  case $step in
    contract) make contract || rc=$? ;;
    ucpu) { make -C tb/verilator/ucpu clean >/dev/null && make -C tb/verilator/ucpu; } > "$SCRATCH/ucpu.log" 2>&1 || rc=$?
          grep -E 'checks:|FAIL' "$SCRATCH/ucpu.log" || true ;;
    tsngen) { make -C tb/tsngen clean >/dev/null && make -C tb/tsngen all; } > "$SCRATCH/tsngen.log" 2>&1 || rc=$?
            grep -E 'checks:|FAIL|\[PASS\]|RESULT' "$SCRATCH/tsngen.log" | cut -c1-160 || true ;;
    lint) make lint > "$SCRATCH/lint.log" 2>&1 || rc=$?; tail -3 "$SCRATCH/lint.log" ;;
    docs) make docs > "$SCRATCH/docs.log" 2>&1 || rc=$?; tail -8 "$SCRATCH/docs.log" ;;
  esac
  echo "=== $step exit $rc"
  [ "$rc" = 0 ] || st=1
done
exit $st
