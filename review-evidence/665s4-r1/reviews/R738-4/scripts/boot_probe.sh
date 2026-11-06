#!/bin/bash
# Runs the split boot at one point from the review clone: boot_probe.sh <clone> <outdir> <shape> <interfaces>
. "$(dirname "$0")/env.sh"
cd "$1" || exit 9
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$2" --shape "$3" --interfaces "$4"
