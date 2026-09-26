#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Rebuild every image the processor repository generates, from an exported tree,
# into OUT, and print "sha256  name" for each. Usage: image_digests.sh TREE OUT
set -euo pipefail
tree=$(cd "$1" && pwd); out=$2; mkdir -p "$out"; out=$(cd "$out" && pwd)
cd "$tree"
# the worked example, exactly as tb/desc_store/Makefile builds image.bin/image.map
python3 -B hdl/aecp/desc/gen_desc_image.py -i hdl/aecp/desc/example_milan_8.json \
  -o "$out/desc_store_image.bin" -m "$out/desc_store_image.map" >/dev/null
# the ROM/microcode images the other suites and the Yosys gate build
python3 -B hdl/acmp/rom/gen_ltn_rom.py -o "$out/ltn_rom.hex" >/dev/null
for g in hdl/aecp/ucode/gen_ucode.py hdl/ucode/gen_ucode.py; do
  if [ -f "$g" ]; then
    python3 -B "$g" -o "$out/ucode__$(echo "$g" | tr / _).hex" >/dev/null
  else
    echo "absent: $g" >&2
  fi
done
cd "$out" && sha256sum -- * | sort -k2
