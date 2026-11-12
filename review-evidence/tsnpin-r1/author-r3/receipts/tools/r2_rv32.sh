#!/usr/bin/env bash
# r2_rv32.sh: round 2's RV32 measurements on the pinned SDK: the fixture and platform images at both pins, and the size fixture.
set -u
export HOME=<scratch>/sdk/home
D=<scratch>; R=$D/ledger3/runtime
cd $D
echo "compiler: $($HOME/br-milan-rv32/host/bin/riscv32-linux-gcc --version | head -1)"
tools/snap.sh $D/snaps/base 1d6bf5556a >/dev/null || exit 4
for w in base head; do
  T=$D/snaps/base; [ $w = head ] && T=$D/snaps/sb2
  tools/ledger.sh $T $D/ledger3/$w $R
  for s in 1x1 8x8; do
    X=$D/s2/base-$s/split-soc; shape=endstation_ax7101_$s; [ $s = 1x1 ] && shape=endstation_ax7101_1x1_tdm8
    tools/plat_ledger.sh $T $D/plat3/$w $R $shape 1 $X/mapped/soc/csr.csv $X/flash-map
    led=; [ $s = 8x8 ] && led=platform-8x8-two-interfaces
    tools/plat_ledger.sh $T $D/plat3/$w $R $shape 2 $X/mapped/soc/csr.csv $X/flash-map $led
  done
done
cd $D/snaps/sb2 && python3 -B sw/firmware/ctrl/test/ctrl_image.py --base 1d6bf5556a > $D/logs/ctrl_image-r2.log 2>&1; echo "ctrl_image rc=$?"
