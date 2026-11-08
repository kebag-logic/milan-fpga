#!/bin/bash
# Compile the three core sources against each wire.h variant with the stack's and the parent's RV32 flags;
# report .text bytes and __lshrdi3 references per object set.
# usage: variants.sh REPO WORK VARIANT_DIR...   (each VARIANT_DIR holds a wire.h)
set -eu
REPO=$1 W=$2; shift 2
BR=$HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-
mkdir -p "$W"
for v in "$@"; do
  name=$(basename "$v")
  inc=$W/$name/include; mkdir -p "$inc"
  cp "$REPO"/include/*.h "$inc"/; cp "$v/wire.h" "$inc/wire.h"
  for set in "stack-O0:riscv64-elf-gcc:-march=rv32i -mabi=ilp32 -O0" \
             "stack-O3:riscv64-elf-gcc:-march=rv32i -mabi=ilp32 -O3 -DNDEBUG" \
             "parent-Os-rv32im:${BR}gcc:-march=rv32im -mabi=ilp32 -Os -DNDEBUG -ffunction-sections" \
             "parent-Os-rv32i:${BR}gcc:-march=rv32i -mabi=ilp32 -Os -DNDEBUG -ffunction-sections"; do
    tag=${set%%:*}; rest=${set#*:}; cc=${rest%%:*}; flags=${rest#*:}
    text=0; calls=0
    for m in adp acmp maap; do
      o=$W/$name/$tag-$m.o
      $cc $flags -std=c11 -ffreestanding -DCTRL_REENTRY_ASSERT -I"$inc" -c "$REPO/src/$m.c" -o "$o"
      t=$(${BR}size -A "$o" | awk '$1 ~ /^\.text/ {s += $2} END {print s + 0}')
      c=$(${BR}objdump -dr "$o" | grep -c "__lshrdi3" || true)
      text=$((text + t)); calls=$((calls + c))
    done
    echo "$name $tag text=$text lshrdi3_refs=$calls"
  done
done
