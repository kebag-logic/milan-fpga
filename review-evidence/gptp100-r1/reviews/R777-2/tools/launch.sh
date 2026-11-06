#!/bin/sh
# usage: launch.sh <packet dir> <probe clone>
# Runs the parser suite (with its mutation arm), the engine suite and an
# engine mutation-arm subset concurrently with the pinned Verilator first on
# PATH; each writes runs/<name>.log and runs/<name>.rc.
P=$1; H=$2
export PATH="$P/scratch/bin:$PATH" VERILATOR="$P/scratch/bin/verilator"
verilator --version > "$P/runs/verilator-version.log" 2>&1
( cd "$H" && make -C tb/verilator/parser VERILATOR="$VERILATOR" > "$P/runs/parser.log" 2>&1; echo $? > "$P/runs/parser.rc" ) &
( cd "$H" && make -C tb/verilator/engine run VERILATOR="$VERILATOR" > "$P/runs/engine-run.log" 2>&1; echo $? > "$P/runs/engine-run.rc" ) &
( python3 "$P/tools/arm_subset.py" "$H" "$P/scratch/arm-work" 6 0 148 149 150 \
    112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 \
    > "$P/runs/engine-arm-subset.log" 2>&1; echo $? > "$P/runs/engine-arm-subset.rc" ) &
wait
