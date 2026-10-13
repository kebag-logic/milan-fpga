#!/usr/bin/env bash
# Scratch: R584-2's published probes (boundary, shape, pin) against a pristine clone of the head.
# usage: probes584.sh <pristine clone> <output directory>
set -u
pristine=$1; out=$2
S=$VALIDATION_STORAGE/697c-a583/round3
P=$S/packets/review-evidence/697c-r1/reviews/R584-2/scripts
RV=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
export TMPDIR=$S/tmp
mkdir -p "$out"
python3 -I "$P/boundary_probes.py" "$pristine" "$out/work" "$out/boundary_probes.json" --jobs 2 --rv32 "$RV" \
  > "$out/boundary_probes.log" 2>&1
echo "rc=$?" > "$out/boundary_probes.rc"
bash "$P/shape_probe.sh" "$pristine" "$out/shape-work" "$RV" > "$out/shape_probe.log" 2>&1
echo "rc=$?" > "$out/shape_probe.rc"
