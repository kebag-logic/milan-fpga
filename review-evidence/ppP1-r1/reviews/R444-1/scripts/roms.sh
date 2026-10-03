#!/usr/bin/env bash
# R444-1: regenerate every ROM from its generator at the base, both merge
# parents and the head, and compare bytes. Usage: roms.sh REPO OUTDIR
set -u
REPO=$1; OUT=$2
mkdir -p "$OUT"
for rev in ddb3119dbbce59f81bf7a536a1ad90a20546edb2 53e1474b633ee31de2ce1c1436b6b61920c9c8b2 \
           f4167536d358c996f4e1b70b875879c1651f85d3 c066dd83a2004f9b3640a933860c4d9e677d017e; do
  d="$OUT/${rev:0:8}"; rm -rf "$d"; mkdir -p "$d/src" "$d/rom"
  git -C "$REPO" archive "$rev" hdl | tar -x -C "$d/src"
  (cd "$d/src" &&
   python3 -B hdl/aecp/ucode/gen_ucode.py -o "$d/rom/ucode.hex" >/dev/null &&
   python3 -B hdl/acmp/rom/gen_ltn_rom.py -o "$d/rom/ltn_rom.hex" >/dev/null &&
   python3 -B hdl/aecp/desc/gen_desc_image.py -i hdl/aecp/desc/milan_min.json \
       -o "$d/rom/milan_min.bin" >/dev/null &&
   python3 -B hdl/aecp/desc/gen_desc_image.py --no-lint -i hdl/aecp/desc/example_milan_8.json \
       -o "$d/rom/example_milan_8.bin" >/dev/null) || echo "GEN FAIL at $rev"
  (cd "$d/rom" && sha256sum *) | sed "s|^|${rev:0:8} |"
done
