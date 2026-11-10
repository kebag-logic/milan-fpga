#!/bin/sh
# usage: rv32_text.sh NAME=TREE... -- text of src/acmp.c for RV32I at the default 16 sinks, -Os, -O2 and -O3.
# riscv64-elf-gcc, -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -std=c11 -DNDEBUG -DCTRL_REENTRY_ASSERT
W=${W:-$SCRATCH/rv32-text}; mkdir -p "$W"
riscv64-elf-gcc --version | head -1
for t in "$@"; do n=${t%%=*} d=${t#*=}
  for o in -Os -O2 -O3; do
    riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -isystem "$(riscv64-elf-gcc -print-file-name=include)" \
      -std=c11 -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT $o -I"$d/examples/rv32/include" -I"$d/include" \
      -c "$d/src/acmp.c" -o "$W/$n$o.o" || { echo "$n $o rc=$?"; continue; }
    printf '%-10s %-4s text=%s undefined=%s\n' "$n" "$o" "$(riscv64-elf-size "$W/$n$o.o" | awk 'NR==2{print $1}')" \
      "$(riscv64-elf-nm -u "$W/$n$o.o" | awk '{print $2}' | tr '\n' ',')"
  done
done
