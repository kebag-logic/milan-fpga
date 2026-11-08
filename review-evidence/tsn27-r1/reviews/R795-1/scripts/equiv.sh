#!/bin/bash
# Bit-exactness of the head wire_put_be against the old byte form: hosted gcc/clang with UBSan,
# and RV32 under qemu-system-riscv32 at -O0/-O2/-O3/-Os for rv32i and rv32im.
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/equiv; W=$SCR/equiv; mkdir -p "$O" "$W"; : > "$O/summary.txt"
H=$(dirname "$0")/equiv.c
for cc in gcc clang; do for opt in -O0 -O2 -Os -O3; do
  t=$W/host-$cc$opt
  $cc -std=c11 -Wall -Wextra -Werror $opt -DHOSTED -fsanitize=undefined -fno-sanitize-recover=all -I"$REPO/include" "$H" -o "$t" >"$t.log" 2>&1 \
    && UBSAN_OPTIONS=halt_on_error=1 "$t" >>"$t.log" 2>&1; echo "host $cc $opt rc $?" >> "$O/summary.txt"
done; done
RV=riscv64-elf-gcc
for march in rv32i rv32im; do for opt in -O0 -O2 -O3 -Os; do
  e=$W/rv32-$march$opt.elf
  $RV -march=$march -mabi=ilp32 -ffreestanding -fno-builtin -nostdlib -nostartfiles $opt -std=c11 -Wall -Wextra -Werror \
      -I"$REPO/include" -T"$REPO/examples/rv32/link.ld" "$REPO/examples/rv32/start.S" "$REPO/examples/rv32/runtime.c" "$H" -lgcc -o "$e" >"$e.log" 2>&1
  b=$?
  timeout 300 qemu-system-riscv32 -machine virt -nographic -bios none -kernel "$e" -no-reboot >>"$e.log" 2>&1; q=$?
  echo "rv32 $march $opt build $b qemu $q" >> "$O/summary.txt"
done; done
cat "$O/summary.txt"
