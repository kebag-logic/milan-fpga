#!/usr/bin/env bash
# Link every RV32 measurement image at every shape of one tree and hash each ELF.
# usage: images.sh <tree> <output directory> <runtime directory holding libc.a and libcompiler_rt.a>
# MILAN_RV32_CC must name the pinned SDK compiler. The runtime archives are a differential stand-in
# (the same archives for both trees compared), built by runtime.sh from the repository's own
# rv32_image/image_rt.c and image_arith.c.
set -uo pipefail
tree=$1 out=$2 rt=$3
: "${MILAN_RV32_CC:?}"
rm -rf "$out"; mkdir -p "$out/srp_image"
shapes=()
for config in "$tree"/configs/endstation_*.yaml; do shapes+=(--shape "$(basename "$config" .yaml)"); done
python3 "$tree/sw/firmware/ctrl/test/ctrl_image.py" "${shapes[@]}" --out "$out/ctrl_image" > "$out/ctrl_image.log" 2>&1
echo "ctrl_image rc=$?" >> "$out/rc.txt"
pids=()
for config in "$tree"/configs/endstation_*.yaml; do
  name=$(basename "$config" .yaml)
  for interfaces in 1 2; do
    for comp in srp nosrp aecp; do
      extra=()
      [ "$comp" = nosrp ] && extra=(--without-srp)
      [ "$comp" = aecp ] && extra=(--with-aecp)
      dest="$out/srp_image/$name-if$interfaces-$comp"
      ( python3 "$tree/sw/firmware/ctrl/test/ctrl_srp_image.py" --config "$config" --interfaces "$interfaces" \
          --output "$dest" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" "${extra[@]}" \
          > "$dest.log" 2>&1; echo "$name-if$interfaces-$comp rc=$?" >> "$out/rc.txt" ) &
      pids+=($!)
      if [ ${#pids[@]} -ge 6 ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi
    done
  done
done
wait
cd "$out" && find . -name ctrl_app.elf | sort | xargs sha256sum > elf.sha256
wc -l < elf.sha256
