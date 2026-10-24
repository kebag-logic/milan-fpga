#!/usr/bin/env bash
# CONTRIBUTING's Vivado front-end gate (scripts/xvlog_gate.py --check) in a clean
# clone at <rev>, under the exclusive Vivado lock.
# usage: xvlog_gate.sh <rev>
set -u
rev=$1; h=${rev:0:8}
here=$(cd "$(dirname "$0")" && pwd)
B=$VALIDATION_STORAGE/scratch/773-a664
C=$B/clone-xvlog-$h
O=$B/xvlog-$h
mkdir -p "$O"
[ -d "$C" ] || bash "$here/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$B/venv31213/bin:$PATH
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"; git status --short > "$O/status.txt"
date -Is > "$O/start"
flock -x $VIVADO_LOCK python3 scripts/xvlog_gate.py --check > "$O/log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
