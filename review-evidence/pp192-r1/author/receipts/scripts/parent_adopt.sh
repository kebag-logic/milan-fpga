#!/usr/bin/env bash
# usage: parent_adopt.sh   the head pass again with the #192 milan_dp adoption commit (57465d43)
# between the three patches and the gitlink, every gate but g17; then g17, which waits on the
# host-wide Vivado lock, at the adopted head, at the prescribed head (9d1dcf14) and at base
S=<scratch>; P="$S/parent"; sha=21855f6cce6d8771f5b1e84de3d875d7683e23f1
G="$S/scripts/gate.sh"; A="$S/rec/parent-head-adopt"; H="$S/rec/parent-head"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir" VERILATOR_JOBS=2
g17() { "$G" "$1" g17_xvlog "$P" flock <vivado-lock> python3 scripts/xvlog_gate.py --check; }
set -e
git -C "$P" checkout -q -B pp192-a660-head-adopt 57465d43cd886b4711deb45616d01d21b95c9feb
git -C "$P" clean -fdXq -- tb/verilator
git -C "$P/protocol-processor" checkout -q --detach "$sha"
git -C "$P/protocol-processor" clean -fdXq
git -C "$P" add protocol-processor
git -C "$P" commit -q -m "Scratch: protocol-processor at ${sha:0:8} (head pass with the #192 milan_dp adoption)"
set +e
SKIP_G17=1 "$S/scripts/parent_gates2.sh" "$A"
g17 "$A"
git -C "$P" status --short > "$A/parent-status-after-g17.txt"
git -C "$P" checkout -q pp192-a660-head-21855f6c
git -C "$P" clean -fdXq -- tb/verilator
git -C "$P" rev-parse HEAD > "$H/parent-HEAD-g17.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$H/submodule-HEAD-g17.txt"
g17 "$H"
git -C "$P" status --short > "$H/parent-status-after.txt"
git -C "$P/protocol-processor" status --short --ignored > "$H/submodule-status-after.txt"
echo ALL-DONE > "$H/parent.done"
"$S/scripts/parent_base_g17.sh"
