#!/bin/sh
# One split boot: run_boot.sh TREE OUTDIR [run.py args]. Set PACKET and the tool variables first.
. "$PACKET/scripts/env.sh"
tree=$1; out=$2; shift 2
cd "$tree" || exit 2
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$out" "$@" > "$out.log" 2>&1
echo $? > "$out.rc"
