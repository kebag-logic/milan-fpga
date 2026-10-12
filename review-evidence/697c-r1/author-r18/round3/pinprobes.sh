#!/usr/bin/env bash
# Scratch: both reviewers' published pin probes, each on its own clone of the head (they edit its submodule
# in place and restore it).
# usage: pinprobes.sh <clone for R584-2> <clone for R585-2> <output directory>
set -u
c584=$1; c585=$2; out=$3
S=$VALIDATION_STORAGE/697c-a583/round3
R=$S/packets/review-evidence/697c-r1/reviews
RV=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
export TMPDIR=$S/tmp MILAN_RV32_CC=$RV
mkdir -p "$out"
bash "$R/R584-2/scripts/pin_probes.sh" "$c584" "$out/r584-work" "$RV" > "$out/r584-pin_probes.log" 2>&1
echo "rc=$?" > "$out/r584-pin_probes.rc"
bash "$R/R585-2/scripts/pin_probes.sh" "$c585" "$out/r585-work" > "$out/r585-pin_probes.log" 2>&1
echo "rc=$?" > "$out/r585-pin_probes.rc"
