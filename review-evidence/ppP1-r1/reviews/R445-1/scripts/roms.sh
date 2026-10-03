#!/bin/sh
# R445-1: regenerate every ROM from its generator in each extracted tree and
# print one sha256 per artefact and tree: the microcode, the listener ROM and
# both descriptor images (the generator's example and the minimal model).
# Usage: roms.sh TREE...
set -e
for t in "$@"; do
  o=$(mktemp -d)
  d="$t/hdl/aecp/desc"
  python3 -B "$t/hdl/aecp/ucode/gen_ucode.py" -o "$o/ucode.hex" >/dev/null
  python3 -B "$t/hdl/acmp/rom/gen_ltn_rom.py" -o "$o/ltn_rom.hex" >/dev/null
  python3 -B "$d/gen_desc_image.py" --no-lint -i "$d/example_milan_8.json" \
      -o "$o/desc_example_milan_8.bin" -m "$o/desc_example_milan_8.map" >/dev/null
  python3 -B "$d/gen_desc_image.py" -i "$d/milan_min.json" \
      -o "$o/desc_milan_min.bin" -m "$o/desc_milan_min.map" >/dev/null
  for f in ucode.hex ltn_rom.hex desc_example_milan_8.bin desc_example_milan_8.map \
           desc_milan_min.bin desc_milan_min.map; do
    printf '%s  %s  %s\n' "$(sha256sum "$o/$f" | cut -d' ' -f1)" "$f" "$(basename "$t")"
  done
  rm -rf "$o"
done
