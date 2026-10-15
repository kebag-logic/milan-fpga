#!/bin/sh
# Usage: launch_runs.sh <scratch dir> <tree with tb/verilator/follow_ring>
# Starts the R634-1 falsification runs detached; each writes <name>.log and <name>.rc in <scratch>/runs.
S=$1; FR=$2/tb/verilator/follow_ring; R=$S/runs; mkdir -p $R
export PATH=$S/bin:$PATH
go() { n=$1; shift; ( cd "$FR" && env -u MAKEFLAGS "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
go head_bind  $S/obj_head/Vfollow_ring --case bind --b17-cycles 5,4,9 --bind-phase 0.125 --jitter-us 5 --dwell-s 0.5 --follow-binds 1
go base_bind  $S/obj_base/Vfollow_ring --case bind --b17-cycles 5,4,9 --bind-phase 0.125 --jitter-us 5 --dwell-s 0.5
go settle_control python3 settle_control.py --sim verilator --out $S/sc --jobs 4
go mutants    python3 mutants.py --jobs 3
go sweep_bind python3 sweep.py bind --exe $S/obj_head/Vfollow_ring --out $S/sweep_head --jobs 3 --jitter-us 0 5 --extra --dwell-s 0.5
go sweep_bind32 python3 sweep.py bind --exe $S/obj_head/Vfollow_ring --out $S/sweep_head32 --jobs 3 --phases 32 --jitter-us 5 --extra --dwell-s 0.5
