#!/usr/bin/env bash
# Link every RV32 measurement image at every shipped shape with the tree's OWN builders, and hash each ELF.
# ctrl_image.py at every configs/endstation_*.yaml shape; ctrl_srp_image.py at every shape, one and two
# interfaces, with SRP, without SRP, and with AECP. Same runtime archives on both sides.
# usage: images.sh <tree> <output directory> <runtime directory holding libc.a and libcompiler_rt.a>
# needs MILAN_RV32_CC (the pinned SDK compiler).
set -uo pipefail
tree=$1; out=$2; rt=$3
: "${MILAN_RV32_CC:?}"
rm -rf "$out"; mkdir -p "$out/srp_image"
shapes=()
for config in "$tree"/configs/endstation_*.yaml; do shapes+=(--shape "$(basename "$config" .yaml)"); done
(cd "$tree" && python3 sw/firmware/ctrl/test/ctrl_image.py "${shapes[@]}" --out "$out/ctrl_image") > "$out/ctrl_image.log" 2>&1
echo "ctrl_image rc=$?" > "$out/rcs.txt"
for config in "$tree"/configs/endstation_*.yaml; do
  name=$(basename "$config" .yaml)
  for interfaces in 1 2; do
    for comp in srp nosrp aecp; do
      extra=()
      [ "$comp" = nosrp ] && extra=(--without-srp)
      [ "$comp" = aecp ] && extra=(--with-aecp)
      dest="$out/srp_image/$name-if$interfaces-$comp"
      (cd "$tree" && python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "$config" --interfaces "$interfaces" \
        --output "$dest" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" "${extra[@]}") > "$dest.log" 2>&1
      echo "$name-if$interfaces-$comp rc=$?" >> "$out/rcs.txt"
    done
  done
done
cd "$out" && find . -name ctrl_app.elf | sort | xargs -r sha256sum > elf.sha256
wc -l < elf.sha256
