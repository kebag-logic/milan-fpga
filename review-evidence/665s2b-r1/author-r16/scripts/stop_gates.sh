#!/bin/bash
# The gates run at the STOP head, one log and one rc each, on a clean clone (F), never piped.
set -u
H=$1
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
W=$T/F G=$T/stop-logs
mkdir -p "$G"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-stop MAKEFLAGS="-j8 --no-print-directory"
mkdir -p "$TMPDIR"
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc" >> "$G/summary.txt"; }
run diffcheck_round "git diff --check 65251a2ff505396f30c2544d1db58f5f3eda2cf5 HEAD"
run diffcheck_merge "git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run fw_coverage "python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8"
run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
git status --short > "$G/tree-after.txt"
echo done >> "$G/summary.txt"
