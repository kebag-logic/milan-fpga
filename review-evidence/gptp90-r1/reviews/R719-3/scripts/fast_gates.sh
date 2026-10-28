#!/bin/bash
# usage: fast_gates.sh <src-tree> <receipt-dir> <bin-dir-with-pinned-verilator>
# Runs independent cheap gates concurrently, one log and rc per gate.
S=$1; R=$2; export PATH=$3:$PATH
cd "$S" || exit 2
verilator --version > "$R/verilator-version.txt"
run() { name=$1; shift; ( "$@" > "$R/gate-$name.log" 2>&1; echo $? > "$R/gate-$name.rc" ) & }
run contract make contract
run docs make docs
run lint make lint
run ucpu make -C tb/verilator/ucpu
run tsngen make -C tb/tsngen
run gaskets make -C tb/verilator/gaskets
run bench-test make -C bench/arty test
run ooc-selftest python3 syn/ooc/check_ooc_clock.py --selftest
wait
for f in "$R"/gate-*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
