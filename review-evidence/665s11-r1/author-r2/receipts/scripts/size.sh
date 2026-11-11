#!/bin/bash
# size.sh <tree> <label>: the platform image (ctrl_plat_image.py) at the four ledger points, its sections and
# sizeof(struct ctrl_plat) (the ctrl_plat symbol); the 8x8 two-interface image planned at its ledgered point
set -u
S=<scratch>; R1=<round1-scratch>
tree=$1; label=$2; D=$S/size/$label; rm -rf $D; mkdir -p $D
CSR=$S/reboot-dev1/soc-provisional/csr.csv; RT=$S/reboot-dev1/runtime
for p in "1x1_tdm8 1 $S/reboot-dev1/split-soc/flash-map" "1x1_tdm8 2 $S/reboot-dev1/split-soc/flash-map" \
         "8x8 1 $R1/size/map-8x8/flash-map" "8x8 2 $R1/size/map-8x8/flash-map"; do
  set -- $p; cfg=$1; n=$2; map=$3; name=$cfg-$n
  extra=(); [ "$cfg-$n" = 8x8-2 ] && extra=(--ledgered-point platform-8x8-two-interfaces)
  python3 -B $tree/sw/firmware/ctrl/test/ctrl_plat_image.py --config $tree/configs/endstation_ax7101_$cfg.yaml \
    --interfaces $n --csr-csv $CSR --flash-map $map --output $D/$name --libc $RT/libc.a \
    --compiler-runtime $RT/libcompiler_rt.a "${extra[@]}" > $D/$name.log 2>&1
  echo "$name rc=$?" >> $D/rc.txt
  riscv32-buildroot-linux-gnu-nm -S $D/$name/ctrl_app.elf 2>/dev/null | grep " ctrl_plat$" > $D/$name.ctrl_plat.txt
  riscv32-buildroot-linux-gnu-size -A $D/$name/ctrl_app.elf > $D/$name.size.txt 2>&1
done
cat $D/rc.txt
