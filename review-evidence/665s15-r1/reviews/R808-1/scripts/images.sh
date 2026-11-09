#!/bin/bash
# Link the split size fixture (ctrl_srp_image.py --with-aecp --layout split) at each shipped point
# and the 32x32 point in one clean clone, and print each ctrl_app.elf's SHA-256.
# usage: images.sh CLONE OUTDIR RUNTIME_DIR
set -u
C=$1 O=$2 RT=$3
mkdir -p "$O"
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l)" > "$O/head.txt"
for pt in "endstation_ax7101_1x1_tdm8 1 -" "endstation_ax7101_8x8 1 -" "endstation_ax7101_8x8 2 8x8-two-interfaces" "endstation_ax7101_32x32 2 -"; do
  set -- $pt
  led=(); [ "$3" != "-" ] && led=(--ledgered-point "$3")
  d="$O/$1-if$2"
  python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$1.yaml" --interfaces "$2" --with-aecp \
    --layout split --output "$d" "${led[@]}" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" \
    > "$d.log" 2>&1
  rc=$?
  h=$(sha256sum "$d/ctrl_app.elf" 2>/dev/null | cut -d' ' -f1)
  echo "$1 if$2 rc=$rc elf=${h:-none}" | tee -a "$O/elf.txt"
done
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O/head.txt"
