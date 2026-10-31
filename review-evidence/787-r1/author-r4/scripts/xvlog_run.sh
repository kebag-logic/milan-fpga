#!/usr/bin/env bash
# #787 round 4: scripts/xvlog_gate.py --check in the clean clone (every tracked hdl/ and processor source,
# the merged RTL files among them), run by the slot wrapper. Writes <out>/xvlog.log and xvlog.rc.
# usage: xvlog_run.sh <repo> <out>
set -u
repo=$1; out=$2
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH
export TMPDIR=$VALIDATION_STORAGE/787-a700e/tmp
mkdir -p "$out"; cd "$repo" || exit 2
s=$(date +%s)
python3 -B scripts/xvlog_gate.py --check > "$out/xvlog.log" 2>&1
rc=$?
echo "$rc $(( $(date +%s) - s ))s" > "$out/xvlog.rc"
exit $rc
