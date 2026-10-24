#!/usr/bin/env bash
# The Yosys gate (syn/yosys/run.sh, the full serial gate, every top) in its own
# clean clone at <rev>, sv2v v0.0.12 and CPython 3.12.3 first on PATH.
# usage: yosys_gate.sh <rev>
set -u
rev=$1; h=${rev:0:8}
here=$(cd "$(dirname "$0")" && pwd)
B=$VALIDATION_STORAGE/scratch/773-a664
C=$B/clone-yosys-$h
O=$B/yosys-$h
mkdir -p "$O"
[ -d "$C" ] || bash "$here/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
export PATH=$VALIDATION_TOOLS/sv2v-v0.0.12:$B/venv312/bin:$PATH
export TMPDIR=$B/tmp
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"; git status --short > "$O/status.txt"
{ yosys -V; sv2v --version; python3 --version; } > "$O/tools.txt" 2>&1
date -Is > "$O/start"
bash syn/yosys/run.sh > "$O/log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
