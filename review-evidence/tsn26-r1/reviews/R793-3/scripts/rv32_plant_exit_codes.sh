#!/bin/sh
# Usage: rv32_plant_exit_codes.sh <dir holding one rv32_plant_smoke.sh output tree per plant> <plant>...
# Runs each plant's Debug and Release smoke ELF under QEMU and prints the exit code (the failing check number).
set -u
D=$1; shift
for n in "$@"; do
  line=$n
  for k in debug release; do
    e=$D/$n/build-rv32/$k/rv32_smoke.elf
    if [ -f "$e" ]; then timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -kernel "$e" -no-reboot >/dev/null 2>&1; line="$line $k qemu_rc=$?"; else line="$line $k missing"; fi
  done
  echo "$line"
done
