#!/usr/bin/env bash
# Scratch: the bench (whole, then run-if2 and run-cosim alone) and the MAAP differential of one tree, one build at a time.
# usage: verilator-gates3.sh <tree> <log prefix>
set -u
tree=$1; pre=$2
export TMPDIR=$VALIDATION_STORAGE/697c-a583/round3/tmp VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
cd "$tree" || exit 2
for target in all run-if2 run-cosim; do
  log="$pre-mbx-$target.log"
  date -u +%FT%TZ > "$log"
  make -C tb/verilator/mbx VERILATOR="$VERILATOR" VBUILD_JOBS=4 "$target" >> "$log" 2>&1
  echo "rc=$?" >> "$log"; date -u +%FT%TZ >> "$log"
done
date -u +%FT%TZ > "$pre-maap-diff.log"
python3 -B sw/firmware/ctrl/test/maap_differential.py --self-test >> "$pre-maap-diff.log" 2>&1
echo "rc=$?" >> "$pre-maap-diff.log"; date -u +%FT%TZ >> "$pre-maap-diff.log"
