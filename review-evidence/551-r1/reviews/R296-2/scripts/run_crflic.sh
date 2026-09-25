#!/bin/sh
# R296-2: build and run the obj_crflic leg in a disposable parent clone with
# the pinned simulator. Prints the leg's own verdict; exit status is make's.
# Usage: run_crflic.sh <disposable-parent-clone> <pinned-tool-bin-dir> [mdir]
set -u
root=$1
tools=$2
mdir=${3:-obj_crflic}
PATH=$tools:$PATH
export PATH
verilator --version
cd "$root/tb/verilator/milan_dp" || exit 2
make crflic VERILATOR_JOBS=8 CRFLIC_MDIR="$mdir"
