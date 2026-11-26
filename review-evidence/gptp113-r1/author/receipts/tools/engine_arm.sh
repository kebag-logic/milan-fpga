#!/bin/bash
# usage: engine_arm.sh WORKTREE LOGDIR NAME  -- one clean `make -j4 -C tb/verilator/engine run`
wt=$1; out=$2/$3; mkdir -p "$out"
export PATH=<verilator-5.050>/bin:$PATH CCACHE_DIR=<ccache> MAKEFLAGS='-j4 --no-print-directory'
ulimit -c 0
cd "$wt" || exit 9
git rev-parse HEAD > "$out/head"; git status --porcelain > "$out/dirty"
make -C tb/verilator/engine clean >/dev/null 2>&1
start=$(date +%s.%N)
make -C tb/verilator/engine run > "$out/log" 2>&1; rc=$?
end=$(date +%s.%N)
echo "rc=$rc wall=$(echo "$end - $start" | bc) s verilator=$(verilator --version)" > "$out/result"
