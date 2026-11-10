#!/bin/sh
# SPDX-License-Identifier: MIT
# usage: rv32_compare.sh MAIN_TREE R1_TREE HEAD_TREE WORK -- round 1's rv32_size.sh (main vs round 1, then main vs head) at
# 16 and 33 sinks, and a disassembly comparison of round 1 and the head at each level (addresses and symbols included).
M=$1 A=$2 H=$3 W=$4; D=$(cd "$(dirname "$0")" && pwd)
echo "== round 1 script: main vs round 1"; sh "$D/r1/scripts/rv32_size.sh" "$M" "$A" "$W/r1"
echo "== round 1 script: main vs head"; sh "$D/r1/scripts/rv32_size.sh" "$M" "$H" "$W/head"
for n in default 33; do for o in -Os -O2 -O3; do
  riscv64-elf-objdump -d -r "$W/r1/head$o$n.o" | tail -n +3 > "$W/r1$o$n.dis"; riscv64-elf-objdump -d -r "$W/head/head$o$n.o" | tail -n +3 > "$W/head$o$n.dis"
  if cmp -s "$W/r1$o$n.dis" "$W/head$o$n.dis"; then r=identical; else r="DIFFERS $(diff "$W/r1$o$n.dis" "$W/head$o$n.dis" | grep -c '^[<>]') lines"; fi
  echo "disassembly round 1 vs head sinks=$n $o: $r; text sha256 $(riscv64-elf-objcopy -O binary -j .text "$W/head/head$o$n.o" /dev/stdout | sha256sum | cut -c1-16) vs $(riscv64-elf-objcopy -O binary -j .text "$W/r1/head$o$n.o" /dev/stdout | sha256sum | cut -c1-16)"
done; done
