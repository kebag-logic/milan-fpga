#!/usr/bin/env bash
# Regenerate every processor ROM/image at one revision, in a private export,
# and print sha256 of each output.
# usage: rom_regen.sh <repo> <rev> <scratch>
set -euo pipefail
repo=$1 rev=$2 scr=$3
t="$scr/rom-$rev"; rm -rf "$t"; mkdir -p "$t/src" "$t/out"
git -C "$repo" archive "$rev" | tar -x -C "$t/src"
cd "$t/src"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$t/out/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$t/out/ltn_rom.hex" >/dev/null )
python3 -B hdl/aecp/desc/gen_desc_image.py --no-lint -i hdl/aecp/desc/example_milan_8.json \
  -o "$t/out/example_milan_8.bin" -m "$t/out/example_milan_8.map" >/dev/null
python3 -B hdl/aecp/desc/gen_desc_image.py -i hdl/aecp/desc/milan_min.json \
  -o "$t/out/milan_min.bin" -m "$t/out/milan_min.map" >/dev/null
( cd "$t/out" && sha256sum ucode.hex ltn_rom.hex example_milan_8.bin example_milan_8.map milan_min.bin milan_min.map ) \
  | sed "s|\$| @$rev|"
rm -rf "$t"
