#!/bin/bash
# usage: run_boot.sh <tree> <build-dir> <log> [run.py args...]; writes <log>.rc
tree=$1 out=$2 log=$3
shift 3
cd "$tree" && python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$out" "$@" > "$log" 2>&1
echo $? > "$log.rc"
