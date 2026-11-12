#!/bin/sh
# Compile the three sources the portable-C change touches (aecp/aecp.c and port/ctrl_pool.c; srp_mbx.c needs generated headers and is not compiled here) for RV32IM
# at -Os from two trees (git archives of a base and of the change) with the pinned SDK, and compare each object's
# allocated sections byte for byte. usage: item5_objects.sh <cc> <base-tree> <change-tree> <out>
set -eu
CC=$1; A=$2; B=$3; OUT=$4
OBJCOPY=${CC%gcc}objcopy
mkdir -p "$OUT"
for t in A B; do
  eval T=\$$t
  for s in aecp/aecp.c port/ctrl_pool.c ; do
    o="$OUT/$t-$(echo $s | tr / _).o"
    inc=""; for d in mbx host port loop adp maap acmp app test aecp srp plat; do inc="$inc -I$T/sw/firmware/ctrl/$d"; done
    "$CC" -march=rv32im -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -DNDEBUG -std=c11 -ffunction-sections \
      -fdata-sections -fno-pic -DCTRL_MBX_BASE=0x80000000u -DCTRL_MBX_DMA_BASE=0x8000ff00u $inc \
      -I"$T/third_party/tsn-c-stack/include" -I"$T/third_party/lwSRP/src" -I"$T/third_party/lwSRP/include" \
      -I"$T/sw/firmware/ctrl_nvm" -I"$T/sw/firmware/gtest" -c "$T/sw/firmware/ctrl/$s" -o "$o"
    "$OBJCOPY" -O binary --only-section='.text*' --only-section='.rodata*' --only-section='.data*' \
      --only-section='.bss*' --only-section='.sdata*' --only-section='.sbss*' "$o" "$o.bin"
  done
done
for s in aecp_aecp.c port_ctrl_pool.c; do
  a=$(sha256sum < "$OUT/A-$s.o.bin" | cut -c1-64); b=$(sha256sum < "$OUT/B-$s.o.bin" | cut -c1-64)
  sa=$(${CC%gcc}size -A "$OUT/A-$s.o" | awk '$1 ~ /^\.(text|rodata|data|bss|sdata|sbss)/ {print $1, $2}' | sort | sha256sum | cut -c1-16)
  sb=$(${CC%gcc}size -A "$OUT/B-$s.o" | awk '$1 ~ /^\.(text|rodata|data|bss|sdata|sbss)/ {print $1, $2}' | sort | sha256sum | cut -c1-16)
  [ "$a" = "$b" ] && [ "$sa" = "$sb" ] && r=identical || r=DIFFER
  echo "$s: sections $r (base $a, change $b; section table $sa / $sb)"
done
