#!/bin/bash
# image_identity.sh TREE OUT: the size fixture's and the platform's split images at 1x1/1if and 8x8/1if (one interface),
# linked from TREE against one flash map, csr.csv and runtime per shape (round 5's ledger run), each image's ELF and its
# loadable binary hashed (sha256), so two heads' images can be compared byte for byte.
set -u
T=$1 O=$2 L=<scratch>/r5/ledger3
. <scratch>/tools/env.sh
mkdir -p $O
rc=0
for cfg in 1x1_tdm8 8x8; do
  M=$L/endstation_ax7101_$cfg/split-soc
  python3 -B $T/sw/firmware/ctrl/test/ctrl_srp_image.py --config $T/configs/endstation_ax7101_$cfg.yaml --interfaces 1 \
    --with-aecp --layout split --flash-map $M/flash-map --output $O/fixture-$cfg --libc $L/runtime/libc.a \
    --compiler-runtime $L/runtime/libcompiler_rt.a > $O/fixture-$cfg.log 2>&1 || rc=1
  python3 -B $T/sw/firmware/ctrl/test/ctrl_plat_image.py --config $T/configs/endstation_ax7101_$cfg.yaml --interfaces 1 \
    --csr-csv $M/mapped/soc/csr.csv --flash-map $M/flash-map --output $O/platform-$cfg --libc $L/runtime/libc.a \
    --compiler-runtime $L/runtime/libcompiler_rt.a > $O/platform-$cfg.log 2>&1 || rc=1
done
for d in $O/fixture-* $O/platform-*; do
  [ -d $d ] || continue
  riscv32-buildroot-linux-gnu-objcopy -O binary $d/ctrl_app.elf $d/ctrl_app.loadable.bin
  echo "$(sha256sum < $d/ctrl_app.elf | cut -c1-64) $(basename $d)/ctrl_app.elf"
  echo "$(sha256sum < $d/ctrl_app.loadable.bin | cut -c1-64) $(basename $d)/ctrl_app.loadable.bin"
done > $O/sha256.txt
exit $rc
