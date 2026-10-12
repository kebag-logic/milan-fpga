#!/usr/bin/env bash
# Scratch: link every RV32 measurement image at every shipped shape and hash each ELF:
# ctrl_image.py at every shape; ctrl_srp_image.py at every shape, one and two interfaces, with and
# without SRP, and with AECP (F5, which needs the SRP composition).
# usage: images2b.sh <repository tree> <output directory>
set -euo pipefail
tree=$1
out=$2
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
runtime=$VALIDATION_STORAGE/697c-a583/runtime
# The AECP composition links __umoddi3, which the pinned SDK compiles with its default stack protector
# unless told not to: the AECP images use the freestanding archives (-fno-stack-protector) F5 measured with.
freestanding=$VALIDATION_STORAGE/697c-a583/runtime-freestanding
rm -rf "$out"
mkdir -p "$out/srp_image"
shapes=()
for config in "$tree"/configs/endstation_*.yaml; do
  shapes+=(--shape "$(basename "$config" .yaml)")
done
python3 "$tree/sw/firmware/ctrl/test/ctrl_image.py" "${shapes[@]}" --out "$out/ctrl_image" > "$out/ctrl_image.log" 2>&1
for config in "$tree"/configs/endstation_*.yaml; do
  name=$(basename "$config" .yaml)
  for interfaces in 1 2; do
    for comp in srp nosrp aecp; do
      extra=()
      if [ "$comp" = nosrp ]; then extra=(--without-srp); fi
      rt=$runtime
      if [ "$comp" = aecp ]; then extra=(--with-aecp); rt=$freestanding; fi
      dest="$out/srp_image/$name-if$interfaces-$comp"
      python3 "$tree/sw/firmware/ctrl/test/ctrl_srp_image.py" --config "$config" --interfaces "$interfaces" \
        --output "$dest" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" \
        "${extra[@]}" > "$dest.log" 2>&1
    done
  done
done
cd "$out"
find . -name ctrl_app.elf | sort | xargs sha256sum > elf.sha256
wc -l < elf.sha256
