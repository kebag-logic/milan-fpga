#!/usr/bin/env bash
# Regenerate the AX7101 1x1 TDM8 AEM image from dev ede8d48e source and
# print its length, CRC32 and SHA-256 (compare with the on-board AEM CRC).
# usage: scripts/aem_regen.sh <repo-clone> <scratch dir>
set -euo pipefail
repo=$1
work=$2
rm -rf "$work"
git clone -q --shared --no-checkout "$repo" "$work/src"
git -C "$work/src" checkout -q --detach ede8d48ecd7c7f589a14b957951f040d92c99c70
git -C "$work/src" submodule update -q --init protocol-processor gptp-processor
cd "$work/src"
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml -o "$work/out" > "$work/builder.log"
python3 avdecc/gen_aemi_image.py -o "$work/aem_desc.bin" \
  --overlay "$work/out/endstation_ax7101_1x1_tdm8/aem_overlay.json" > "$work/pack.log"
python3 -c "
import hashlib, sys, zlib
b = open(sys.argv[1], 'rb').read()
print('aem_desc.bin len', len(b), 'crc32 %08x' % (zlib.crc32(b) & 0xffffffff), 'sha256', hashlib.sha256(b).hexdigest())
" "$work/aem_desc.bin"
