#!/usr/bin/env bash
# Scratch: run every firmware arm once from the instrumented clones, dumping SRP-channel TX frames.
export TMPDIR=$SCRATCH/tmp PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc
for side in cand base; do
  out=$SCRATCH/dump/$side
  rm -rf "$out"; mkdir -p "$out/frames"
  cd $SCRATCH/dump-$side || exit 2
  SRP_TX_DUMP="$out/frames" python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$out/build" > "$out/arms.log" 2>&1
  echo "$side rc=$?" >> $SCRATCH/dump/summary.txt
done
echo done >> $SCRATCH/dump/summary.txt
