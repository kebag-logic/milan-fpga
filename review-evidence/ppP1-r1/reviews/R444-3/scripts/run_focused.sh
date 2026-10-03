#!/usr/bin/env bash
# Launch the focused head checks concurrently (detached), each with its own log and rc file.
# usage: run_focused.sh <repo> <commit> <packet>
set -u
repo=$1 rev=$2 P=$3
T=$P/scratch/head; rm -rf "$T"; mkdir -p "$T"
git -C "$repo" archive "$rev" | tar -x -C "$T"
export PATH=$P/scratch/bin:$PATH VERILATOR=$P/scratch/bin/verilator
L=$P/logs
launch() { name=$1; shift; setsid nohup bash -c "cd '$T' && ( $* ) > '$L/$name.log' 2>&1; echo \$? > '$L/$name.rc'" >/dev/null 2>&1 & }
rm -f $L/*.rc
launch pp_top      "CAPJ=8 make -C tb/pp_top run"
launch nvm_port    "CAPJ=6 make -C tb/nvm_port run && make -C tb/nvm_port clean >/dev/null && CAPJ=6 make -C tb/nvm_port figures"
launch lint_docs   "CAPJ=2 ./scripts/lint_hdl.sh && make check && python3 scripts/gen_matrix.py --check"
