#!/bin/bash
# The split boot simulation at both shapes from a checkout, one log and rc each. usage: boot.sh CHECKOUT OUT TAG
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
C=$1 B=$2 TAG=$3
L=$VALIDATION_STORAGE/665s2b-a683u/logs
cd "$C"
go() { n=$1; shift; { echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)"; echo "\$ $*"; nice -n 10 "$@"; echo "rc=$?"; } > "$L/boot-$TAG-$n.log" 2>&1; }
go 1x1 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/1x1"
go 8x8 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/8x8" --shape endstation_ax7101_8x8
