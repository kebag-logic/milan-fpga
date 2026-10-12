#!/usr/bin/env bash
# Compile the ADP, ACMP and MAAP cores of dev's ctrl tree and of the pinned stack to RV32 objects and compare.
# Each side's .c and headers are copied flat into one directory and compiled there by bare file name, so
# __FILE__ (assert's text under -UNDEBUG) is the same on both sides.
# usage: core_objects.sh <dev tree> <head tree> <work>; MILAN_RV32_CC names the pinned SDK compiler.
set -uo pipefail
dev=$1 head=$2 work=$3
: "${MILAN_RV32_CC:?}"
rm -rf "$work"; mkdir -p "$work/dev" "$work/head"
for x in adp acmp maap; do cp "$dev/sw/firmware/ctrl/$x/$x.c" "$dev/sw/firmware/ctrl/$x/$x.h" "$work/dev/"; done
cp "$dev/sw/firmware/ctrl/wire/wire.h" "$work/dev/"
cp "$head"/third_party/tsn-c-stack/src/{adp,acmp,maap}.c "$head"/third_party/tsn-c-stack/include/{adp,acmp,maap,wire}.h "$work/head/"
gccinc=$(dirname "$MILAN_RV32_CC")/../lib/gcc/riscv32-buildroot-linux-gnu/14.3.0/include
rv32inc=$head/sw/firmware/gtest/rv32_include
base=(-march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -std=c11 -Wall -Wextra -Werror -pedantic
      -DCTRL_MBX_BASE=0x80000000u -ffunction-sections -fdata-sections -fno-pic -fno-pie
      -nostdinc -isystem "$gccinc" -I "$rv32inc" -I .)
bad=0
for nd in -DNDEBUG -UNDEBUG; do
  for x in adp acmp maap; do
    for side in dev head; do
      (cd "$work/$side" && "$MILAN_RV32_CC" "${base[@]}" "$nd" -c "$x.c" -o "$x$nd.o") || { echo "COMPILE FAILED $side $x $nd"; bad=1; }
    done
    a=$(sha256sum < "$work/dev/$x$nd.o" | cut -c1-16); b=$(sha256sum < "$work/head/$x$nd.o" | cut -c1-16)
    if cmp -s "$work/dev/$x$nd.o" "$work/head/$x$nd.o"; then
      echo "BYTE-EQUAL $x.c $nd sha256 $a... $(stat -c %s "$work/head/$x$nd.o") bytes"
    else
      echo "DIFFERENT $x.c $nd dev $a head $b"; bad=1
    fi
  done
done
exit $bad
