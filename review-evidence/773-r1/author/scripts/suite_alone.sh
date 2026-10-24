#!/usr/bin/env bash
# One sweep suite run alone at <rev>, in its own clean clone, the way
# scripts/run_all_suites.sh runs it (timeout <its wall clock> make -C
# tb/verilator/<suite>, then scripts/suite_tally.py's verdict), with the
# sweep's environment.
# usage: suite_alone.sh <suite> <rev> <timeout-s>
set -u
suite=$1; rev=$2; tmo=$3; h=${rev:0:8}
here=$(cd "$(dirname "$0")" && pwd)
B=$VALIDATION_STORAGE/scratch/773-a664
C=$B/clone-suite-$suite-$h
O=$B/suite-$suite-$h
mkdir -p "$O"
[ -d "$C" ] || bash "$here/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$B/venv31213/bin:$PATH
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$VALIDATION_STORAGE/773-a664
export TSN_GEN_ROOT=$B/tools/tsn-gen
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"; git status --short > "$O/status.txt"
date -Is > "$O/start"
timeout "$tmo" make -C "tb/verilator/$suite" > "$O/$suite.log" 2>&1
echo $? > "$O/rc"
python3 scripts/suite_tally.py --verdict "$O/$suite.log" > "$O/tally.txt" 2>&1; echo $? >> "$O/tally.txt"
date -Is > "$O/end"
