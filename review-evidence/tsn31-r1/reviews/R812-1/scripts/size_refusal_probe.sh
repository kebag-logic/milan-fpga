#!/bin/bash
# Refusal bound, owed-entry size and RV32 text size of src/acmp.c at main and the head.
# usage: size_refusal_probe.sh <head tree> <main tree> <scratch work dir>
H=$1 M=$2 W=$3
rm -rf "$W"; mkdir -p "$W"
echo "== 1. build-time refusal: head as committed (host gcc, -std=c11 -Wall -Wextra -Werror)"
for n in 1 16 31 32 33 63 64 65 254 4294967295; do
  gcc -std=c11 -Wall -Wextra -Werror -DACMP_MAX_SINKS=${n}u -I"$H/include" -c "$H/src/acmp.c" -o /dev/null 2> "$W/c$n.err"; rc=$?
  echo "N=$n rc=$rc $(grep -o 'static assertion failed: "[^"]*"' "$W/c$n.err" | head -1) $(grep -c 'error' "$W/c$n.err") error-lines"
done
echo "== 2. build-time refusal: head with the one-word mask planted back (uint32_t release[1])"
D=$W/oneword; mkdir -p "$D"; cp -r "$H/src" "$H/include" "$D/"
sed -i 's/\tuint32_t release\[ACMP_RELEASE_WORDS\];/\tuint32_t release[1];/' "$D/include/acmp.h"
grep -n 'uint32_t release\[' "$D/include/acmp.h"
for n in 16 32 33 64; do
  gcc -std=c11 -Wall -Wextra -Werror -DACMP_MAX_SINKS=${n}u -I"$D/include" -c "$D/src/acmp.c" -o /dev/null 2> "$W/o$n.err"; rc=$?
  echo "N=$n rc=$rc $(grep -o 'static assertion failed: "[^"]*"' "$W/o$n.err" | head -1)"
done
echo "== 3. sizeof(struct acmp_owed) and sizeof(struct acmp), x86-64 gcc and RV32I"
cat > "$W/sz.c" <<'EOF'
#include "acmp.h"
unsigned owed_size = sizeof(struct acmp_owed);
unsigned owed_set = sizeof(((struct acmp *)0)->owed);
unsigned acmp_size = sizeof(struct acmp);
EOF
for t in main head; do
  T=$M; [ $t = head ] && T=$H
  for n in 16 32 33 64 65; do
    [ $t = main ] && [ $n -gt 32 ] && continue
    for arch in x86 rv32; do
      if [ $arch = x86 ]; then
        gcc -std=c11 -O0 -DACMP_MAX_SINKS=${n}u -I"$T/include" -S "$W/sz.c" -o "$W/sz.s"
      else
        riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -nostdinc -isystem "$(riscv64-elf-gcc -print-file-name=include)" -I"$T/examples/rv32/include" -std=c11 -O0 \
          -DACMP_MAX_SINKS=${n}u -I"$T/include" -S "$W/sz.c" -o "$W/sz.s"
      fi
      v=$(awk '/^owed_size:|^owed_set:|^acmp_size:/{n=$1} /\.(long|word)/{if(n){printf "%s%s ",n,$2;n=""}}' "$W/sz.s")
      echo "$t N=$n $arch $v"
    done
  done
done
echo "== 4. RV32I text of src/acmp.c at the default 16 sinks (riscv64-elf-gcc, -ffreestanding -fno-builtin -nostdinc -DNDEBUG -DCTRL_REENTRY_ASSERT)"
for o in Os O2 O3; do
  for t in main head; do
    T=$M; [ $t = head ] && T=$H
    riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -isystem "$(riscv64-elf-gcc -print-file-name=include)" -I"$T/examples/rv32/include" -std=c11 \
      -Wall -Wextra -Werror -$o -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$T/include" -c "$T/src/acmp.c" -o "$W/$t-$o.o"
  done
  a=$(riscv64-elf-size "$W/main-$o.o" | awk 'NR==2{print $1}'); b=$(riscv64-elf-size "$W/head-$o.o" | awk 'NR==2{print $1}')
  echo "-$o main=$a head=$b delta=$((b-a))"
done
echo "== 5. RV32I at 33 sinks (head, -Os and -O3): undefined symbols (no new libcalls), text"
for o in Os O3; do
  riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -isystem "$(riscv64-elf-gcc -print-file-name=include)" -I"$H/examples/rv32/include" -std=c11 \
    -Wall -Wextra -Werror -$o -DNDEBUG -DCTRL_REENTRY_ASSERT -DACMP_MAX_SINKS=33u -I"$H/include" -c "$H/src/acmp.c" -o "$W/h33-$o.o"
  echo "-$o text=$(riscv64-elf-size "$W/h33-$o.o" | awk 'NR==2{print $1}') undefined: $(riscv64-elf-nm -u "$W/h33-$o.o" | awk '{print $2}' | tr '\n' ' ')"
done
echo "== 6. main at 16 sinks, -Os, undefined symbols (for comparison)"
echo "$(riscv64-elf-nm -u "$W/main-Os.o" | awk '{print $2}' | tr '\n' ' ') | head: $(riscv64-elf-nm -u "$W/head-Os.o" | awk '{print $2}' | tr '\n' ' ')"
riscv64-elf-gcc --version | head -1
