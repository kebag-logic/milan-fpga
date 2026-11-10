#!/bin/bash
# usage: rv32_identity.sh <clone> <scratch work dir> -- RV32I object code of src/acmp.c at main (ea4af6f1), round 1
# (c6013804) and the head, default 16 sinks, at -Os/-O2/-O3 with the PR's stated flags; text size and a hash of the
# disassembly with file names stripped, so equal hashes mean identical instructions.
C=$1 W=$2; rm -rf "$W"; mkdir -p "$W"
for r in ea4af6f1 c6013804 97414fe6518cda2bf7c4ea136fdd8bd25c860d83; do mkdir -p "$W/$r"; git -C "$C" archive $r src include examples/rv32 | tar -x -C "$W/$r"; done
I="-isystem $(riscv64-elf-gcc -print-file-name=include)"
for o in Os O2 O3; do
  for r in ea4af6f1 c6013804 97414fe6518cda2bf7c4ea136fdd8bd25c860d83; do
    T=$W/$r
    riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc $I -I"$T/examples/rv32/include" -std=c11 \
      -Wall -Wextra -Werror -$o -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$T/include" -c "$T/src/acmp.c" -o "$W/$r-$o.o" || echo "build fail $r $o"
    txt=$(riscv64-elf-size "$W/$r-$o.o" | awk 'NR==2{print $1"/"$2"/"$3}')
    dis=$(riscv64-elf-objdump -d -j .text "$W/$r-$o.o" | tail -n +4 | sha256sum | cut -c1-16)
    sec=$(riscv64-elf-objcopy -O binary -j .text "$W/$r-$o.o" /dev/stdout | sha256sum | cut -c1-16)
    echo "-$o ${r:0:8} text/data/bss=$txt disasm=$dis text-bytes=$sec"
  done
done
riscv64-elf-gcc --version | head -1
