#!/usr/bin/env bash
# usage: parent_base_g17.sh   the parent base pass's last gate, g17 (xvlog), which waited on
# the host-wide Vivado lock: the scratch parent back on its base commit (625c0e5c, the
# protocol-processor gitlink at 24c7f853), then g17 into the base record directory
S=<scratch>; P="$S/parent"; rec="$S/rec/parent-base"
G="$S/scripts/gate.sh"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir" VERILATOR_JOBS=2
set -e
git -C "$P" checkout -q pp192-a660-scratch
git -C "$P" clean -fdXq -- tb/verilator
git -C "$P/protocol-processor" checkout -q --detach 24c7f85340437c7c5b9321c1f76e45c955324e2d
git -C "$P/protocol-processor" clean -fdXq
set +e
git -C "$P" rev-parse HEAD > "$rec/parent-HEAD-g17.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$rec/submodule-HEAD-g17.txt"
git -C "$P" status --short > "$rec/parent-status-before-g17.txt"
"$G" "$rec" g17_xvlog "$P" flock <vivado-lock> python3 scripts/xvlog_gate.py --check
git -C "$P" status --short > "$rec/parent-status-after.txt"
git -C "$P/protocol-processor" status --short --ignored > "$rec/submodule-status-after.txt"
echo ALL-DONE > "$rec/parent.done"
