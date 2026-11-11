#!/bin/bash
# Text, data and bss of the RV32 smoke image and of acmp.c's object in libtsn.a, per build, and the hash of each
# image with its debug sections stripped. usage: rv32_sizes.sh LABEL=BUILD_RV32_DIR...
set -u
for spec in "$@"; do
  label=${spec%%=*} dir=${spec#*=}
  for cfg in debug release; do
    elf=$dir/$cfg/rv32_smoke.elf
    t=$(mktemp -d <scratch>/tmp/sz.XXXX)
    (cd "$t" && riscv64-elf-ar x "$dir/$cfg/libtsn.a")
    obj=$t/acmp.c.obj
    riscv64-elf-objcopy --strip-debug "$elf" "$t/stripped.elf"
    printf '%-8s %-7s image %s | acmp.c.obj %s | image without debug sha256 %s\n' "$label" "$cfg" \
      "$(riscv64-elf-size -A "$elf" >/dev/null; riscv64-elf-size "$elf" | tail -1 | awk '{print "text "$1" data "$2" bss "$3}')" \
      "$(riscv64-elf-size "$obj" | tail -1 | awk '{print "text "$1" data "$2" bss "$3}')" \
      "$(sha256sum "$t/stripped.elf" | cut -c1-16)"
    rm -rf "$t"
  done
done
