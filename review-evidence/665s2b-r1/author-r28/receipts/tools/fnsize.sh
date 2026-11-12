#!/bin/bash
# Size of the named functions of one firmware source built for RV32I -Os: fnsize.sh SRC FN...
S=$1; shift
D=<lane>/sw/firmware/ctrl
CC=<home>/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-gcc
NM=<home>/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-nm
$CC -march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -DNDEBUG -std=c11 -Wall -Wextra -Werror -pedantic \
  -ffunction-sections -DCTRL_MBX_BASE=0x80000000u -DCTRL_MBX_DMA_BASE=0x90000000u -I$D/mbx -I$D/port -I$D/loop -I$D/aecp -I$D/srp \
  -I<lane>/third_party/tsn-c-stack/include -c "$S" -o /tmp/a683zm_fn.o || exit 1
for f in "$@"; do $NM -S /tmp/a683zm_fn.o | awk -v f=$f '$4==f {printf "%s %d  ", f, strtonum("0x"$2)}'; done; echo
