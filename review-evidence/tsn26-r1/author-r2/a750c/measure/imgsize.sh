#!/bin/bash
# usage: imgsize.sh WORK  -> ELF bytes, .text/.rodata/.bss, acmp.c object text per configuration
for c in debug release; do
  d=$1/$c
  elf=$(find $d -name rv32_smoke.elf | head -1)
  obj=$(find $d -name 'acmp.c.obj' -path '*tsn.dir*' | head -1)
  sec=$(riscv64-elf-size -A $elf | awk '$1==".text"{t=$2} $1==".rodata"{r=$2} $1==".bss"{b=$2} END{print ".text "t" .rodata "r" .bss "b}')
  echo "$c elf $(stat -c %s $elf) $sec acmp.o-text $(riscv64-elf-size $obj | tail -1 | awk '{print $1}') ($obj)"
done
