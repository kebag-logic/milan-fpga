#!/bin/bash
# sizeof(struct acmp) at main and the head, for host x86-64 GCC and RV32 (ilp32) GCC, at several ACMP_MAX_SINKS.
# usage: struct_size.sh REPO MAIN HEAD WORKDIR
set -eu
R=$1 M=$2 H=$3 W=$4; mkdir -p "$W"
for rev in $M $H; do
  mkdir -p "$W/$rev/include"; for f in acmp.h wire.h; do git -C "$R" show "$rev:include/$f" > "$W/$rev/include/$f"; done
  printf '#include "acmp.h"\nchar acmp_size[sizeof(struct acmp)];\n' > "$W/$rev/s.c"
  for n in 16 32 33 64; do
    for cc in "gcc" "riscv64-elf-gcc -march=rv32imac_zicsr -mabi=ilp32"; do
      $cc -std=c11 -DACMP_MAX_SINKS=${n}u -I"$W/$rev/include" -c "$W/$rev/s.c" -o "$W/s.o"
      nmt=nm; [ "${cc%% *}" = riscv64-elf-gcc ] && nmt=riscv64-elf-nm
      printf '%s sinks=%s %-16s %d\n' "${rev:0:8}" "$n" "${cc%% *}" $((16#$($nmt -S "$W/s.o" | awk '/acmp_size/{print $2}')))
    done
  done
done
