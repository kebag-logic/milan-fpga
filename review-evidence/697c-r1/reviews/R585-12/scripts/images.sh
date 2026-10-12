#!/usr/bin/env bash
# Link every RV32 measurement image at every shipped shape in one tree and hash each ELF.
# ctrl_image.py at all shapes; ctrl_srp_image.py at each shape, 1 and 2 interfaces,
# with SRP, without SRP, and with AECP (AECP uses -fno-stack-protector runtime archives).
# usage: images.sh <tree> <out> <runtime dir> <freestanding runtime dir>
# needs MILAN_RV32_CC naming the pinned SDK compiler.
set -euo pipefail
tree=$1 out=$2 runtime=$3 freestanding=$4
: "${MILAN_RV32_CC:?}"
rm -rf "$out"; mkdir -p "$out/srp_image"
shapes=()
for config in "$tree"/configs/endstation_*.yaml; do shapes+=(--shape "$(basename "$config" .yaml)"); done
python3 "$tree/sw/firmware/ctrl/test/ctrl_image.py" "${shapes[@]}" --out "$out/ctrl_image" > "$out/ctrl_image.log" 2>&1
pids=()
for config in "$tree"/configs/endstation_*.yaml; do
  name=$(basename "$config" .yaml)
  for interfaces in 1 2; do
    for comp in srp nosrp aecp; do
      extra=(); rt=$runtime
      [ "$comp" = nosrp ] && extra=(--without-srp)
      if [ "$comp" = aecp ]; then extra=(--with-aecp); rt=$freestanding; fi
      dest="$out/srp_image/$name-if$interfaces-$comp"
      ( python3 "$tree/sw/firmware/ctrl/test/ctrl_srp_image.py" --config "$config" --interfaces "$interfaces" \
          --output "$dest" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" "${extra[@]}" \
          > "$dest.log" 2>&1; echo $? > "$dest.rc" ) &
      pids+=($!)
      if [ ${#pids[@]} -ge 8 ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi
    done
  done
done
wait
cat "$out"/srp_image/*.rc | sort | uniq -c
cd "$out"
find . -name ctrl_app.elf | sort | xargs sha256sum > elf.sha256
wc -l < elf.sha256
