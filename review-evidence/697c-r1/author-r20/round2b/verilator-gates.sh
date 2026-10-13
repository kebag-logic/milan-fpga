#!/usr/bin/env bash
# Scratch: the two local Verilator gates of one tree, one after the other (at most two Verilator builds at once).
# usage: verilator-gates.sh <tree> <log prefix>
set -u
tree=$1; pre=$2
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
cd "$tree" || exit 2
date -u +%FT%TZ > "$pre-maap-diff.log"
python3 -B sw/firmware/ctrl/test/maap_differential.py --self-test >> "$pre-maap-diff.log" 2>&1
echo "rc=$?" >> "$pre-maap-diff.log"; date -u +%FT%TZ >> "$pre-maap-diff.log"
date -u +%FT%TZ > "$pre-mbx.log"
make -C tb/verilator/mbx VERILATOR="$VERILATOR" VBUILD_JOBS=4 >> "$pre-mbx.log" 2>&1
echo "rc=$?" >> "$pre-mbx.log"; date -u +%FT%TZ >> "$pre-mbx.log"
