#!/usr/bin/env bash
# usage: parent_all.sh <head-sha>   the parent base gates the second host reset cut (g10, g17)
# into the base record directory, then the head pass (parent_head.sh) into rec/parent-head
S=<scratch>; P="$S/parent"; rec="$S/rec/parent-base"
G="$S/scripts/gate.sh"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir" VERILATOR_JOBS=2
test "$(git -C "$P" rev-parse --show-toplevel)" = "$P" || exit 3
git -C "$P" rev-parse HEAD > "$rec/parent-HEAD-tail2.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$rec/submodule-HEAD-tail2.txt"
"$G" "$rec" g10_test_builder "$P" python3 sw/builder/test_builder.py
"$G" "$rec" g17_xvlog "$P" flock <vivado-lock> python3 scripts/xvlog_gate.py --check
git -C "$P" status --short > "$rec/parent-status-after.txt"
git -C "$P/protocol-processor" status --short --ignored > "$rec/submodule-status-after.txt"
echo ALL-DONE > "$rec/parent.done"
"$S/scripts/parent_head.sh" "$1" "$S/rec/parent-head"
