#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Focused suites at the exact head, in a disposable git-archive extraction.
# Usage: run_focused.sh <repo-clone> <verilator-binary> <out-dir> <work-dir>
set -uo pipefail
REPO=$1; VL=$2; OUT=$3; WORK=$4
HEAD=73a5478784bd861f8c8d33c0d1619594390b9529
rm -rf "$WORK"; mkdir -p "$WORK" "$OUT"
git -C "$REPO" archive "$HEAD" | tar -x -C "$WORK"
"$VL" --version | tee "$OUT/verilator-version.txt"
rc_all=0
run() { # name dir make-args...
  local name=$1 dir=$2; shift 2
  (cd "$WORK/$dir" && make VERILATOR="$VL" "$@") >"$OUT/$name.log" 2>&1
  local rc=$?
  local tally
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$OUT/$name.log" | tail -1)
  echo "$name rc=$rc ${tally:-NO-TALLY}" | tee -a "$OUT/summary.txt"
  [ $rc -eq 0 ] || rc_all=1
}
: >"$OUT/summary.txt"
for n in 1 2 3 5 8; do run srp_admission_N$n tb/srp_admission run N=$n; done
run srp_top tb/srp_top
run srp_stream_fsms tb/srp_stream_fsms
run pp_top tb/pp_top
exit $rc_all
