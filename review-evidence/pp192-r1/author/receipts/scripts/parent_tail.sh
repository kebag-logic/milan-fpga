#!/usr/bin/env bash
# usage: parent_tail.sh <record-dir>   the parent gates the host reset cut (g15 from a clean
# milan_dp, then g10 and g17), unpiped, into the same record directory as the earlier ones
S=<scratch>; P="$S/parent"; rec="$1"; mkdir -p "$rec"
G="$S/scripts/gate.sh"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir" VERILATOR_JOBS=2
test "$(git -C "$P" rev-parse --show-toplevel)" = "$P" || exit 3
git -C "$P" rev-parse HEAD > "$rec/parent-HEAD-tail.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$rec/submodule-HEAD-tail.txt"
mkdir -p "$rec/cut-by-reset" && mv "$rec/g15_milan_dp.log" "$rec/cut-by-reset/" 2>/dev/null
git -C "$P" clean -fdXq tb/verilator/milan_dp
"$G" "$rec" g15_milan_dp "$P" make -j8 -O -C tb/verilator/milan_dp SIM_JOBS=2
"$G" "$rec" g10_test_builder "$P" python3 sw/builder/test_builder.py
"$G" "$rec" g17_xvlog "$P" flock <vivado-lock> python3 scripts/xvlog_gate.py --check
git -C "$P" status --short > "$rec/parent-status-after.txt"
git -C "$P/protocol-processor" status --short --ignored > "$rec/submodule-status-after.txt"
echo ALL-DONE > "$rec/parent.done"
