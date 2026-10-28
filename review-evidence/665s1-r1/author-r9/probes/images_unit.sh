#!/bin/bash
# The four linked image points at the lane head (image_points.sh ... ledgered), with the -fno-stack-protector
# runtime and compiler wrapper (link and plan only), into receipts/images/, then the ELF digests.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680l
W=$VALIDATION_STORAGE/scratch/665s1-a680l-work
export TMPDIR=$W/tmp MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/a680b-work/rv32-nossp/riscv32-linux-gcc
mkdir -p "$O/receipts/images"
bash "$O/probes/image_points.sh" $LANES/665-s1-faces head "$W" $VALIDATION_STORAGE/scratch/a680b-work/runtime-nossp ledgered \
  > "$O/receipts/images/image-points.txt" 2>&1
rc=$?
echo "rc=$rc" >> "$O/receipts/images/image-points.txt"
cp "$W"/images/head-*.txt "$O/receipts/images/"
(cd "$W/images" && sha256sum head-*/ctrl_app.elf) > "$O/receipts/images/elf-sha256.txt"
exit $rc
