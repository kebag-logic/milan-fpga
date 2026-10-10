#!/bin/sh
# Regenerate the two parent AEM images per the head README recipe: parent
# milan-fpga 5603c353 (tarball), gptp-processor at its gitlink, the head's
# processor tree in the protocol-processor slot (gen_desc_image.py blob is
# identical at the parent's gitlink 2ad2f845 and at the head), the builder's
# overlay, then avdecc/gen_aemi_image.py --overlay.
set -u; . "$(dirname "$0")/env.sh"
P=5603c353137e90c1fa95429f6d00ef7a2298d9ee G=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
d="$SCRATCH/parent"; rm -rf "$d" "$SCRATCH/images"; mkdir -p "$d/gptp-processor" "$SCRATCH/parent-dl" "$SCRATCH/images"
gh api repos/kebag-logic/milan-fpga/tarball/$P > "$SCRATCH/parent-dl/parent.tgz"
tar -xzf "$SCRATCH/parent-dl/parent.tgz" -C "$d" --strip-components=1
rm -rf "$d/protocol-processor" "$d/gptp-processor"; mkdir -p "$d/protocol-processor" "$d/gptp-processor"
git -C "$SRC" archive "$HEAD_SHA" | tar -x -C "$d/protocol-processor"
gh api repos/Mister-M-alt/FPGA-gPTP/tarball/$G > "$SCRATCH/parent-dl/gptp.tgz"
tar -xzf "$SCRATCH/parent-dl/gptp.tgz" -C "$d/gptp-processor" --strip-components=1
for c in 1x1_tdm8:1x1 8x8:8x8; do cfg=${c%%:*}; n=${c##*:}
  ( cd "$d" && python3 sw/builder/endstation_builder.py configs/endstation_ax7101_$cfg.yaml -o "$SCRATCH/gen-$cfg" \
    && python3 avdecc/gen_aemi_image.py --overlay "$SCRATCH/gen-$cfg/endstation_ax7101_$cfg/aem_overlay.json" -o "$SCRATCH/images/$n.img.bin" ) > "$SCRATCH/gen-$cfg.log" 2>&1
  echo "$n rc=$?"
done > "$RCPT/regen-images.log"
( cd "$SCRATCH/images" && stat -c '%s %n' *.img.bin && sha256sum *.img.bin ) >> "$RCPT/regen-images.log"
