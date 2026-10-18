#!/bin/sh
# Reviewer gate launcher: run each repository gate of TREE concurrently, one
# log and one rc file per gate under OUT. Pinned simulator dir first on PATH.
# usage: run_gates.sh TREE OUT BINDIR
TREE=$1; OUT=$2; BIN=$3
mkdir -p "$OUT"
export PATH="$BIN:$PATH"
g() { name=$1; shift; ( cd "$TREE" && "$@" ) >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc"; }
g contract make contract &
g lint make lint &
g docs make docs &
g ucpu make -C tb/verilator/ucpu &
g parser make -C tb/verilator/parser &
g gaskets make -C tb/verilator/gaskets &
g tsngen make -C tb/tsngen &
g bench make -C bench/arty test &
g engine-run make -C tb/verilator/engine run &
wait
echo done >"$OUT/ALL.done"
