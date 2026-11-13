#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-owned: link the size fixture's and the target platform's images at the four ledger points of TREE with
# the repository's own builders, on the runtime archives and split SoC exports this review's CPU budget harness
# builds made at the same head (BUILDS/vd-1x1, BUILDS/vd-8x8), then print each plan (size.json, the ledger's read).
# usage: images.sh TREE BUILDS OUT   (TREE a copy of the reviewed head; PATH carries the pinned RV32 SDK)
set -u
T=$1 B=$2 O=$3
mkdir -p "$O"
echo "tree $(git -C "$T" rev-parse HEAD) dirty $(git -C "$T" status --porcelain --untracked-files=no | wc -l) stack $(git -C "$T/third_party/tsn-c-stack" rev-parse HEAD)" > "$O/HEAD.txt"
for spec in "1x1 endstation_ax7101_1x1_tdm8 1" "1x1 endstation_ax7101_1x1_tdm8 2" "8x8 endstation_ax7101_8x8 1" "8x8 endstation_ax7101_8x8 2"; do
  set -- $spec; shape=$1 cfg=$2 n=$3
  R="$B/vd-$shape/split-soc"
  fx=""; pl=""
  if [ "$shape$n" = "8x82" ]; then fx="--ledgered-point 8x8-two-interfaces"; pl="--ledgered-point platform-8x8-two-interfaces"; fi
  ( cd "$T" && "${PY:-python3}" -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$cfg.yaml" --interfaces "$n" \
      --with-aecp --layout split $fx --output "$O/fixture-$shape-if$n" --flash-map "$R/flash-map" \
      --libc "$R/mapped/runtime/libc.a" --compiler-runtime "$R/mapped/runtime/libcompiler_rt.a" ) \
      > "$O/fixture-$shape-if$n.log" 2>&1
  echo $? > "$O/fixture-$shape-if$n.rc"
  ( cd "$T" && "${PY:-python3}" -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "configs/$cfg.yaml" --interfaces "$n" $pl \
      --csr-csv "$R/mapped/soc/csr.csv" --flash-map "$R/flash-map" --output "$O/platform-$shape-if$n" \
      --libc "$R/mapped/runtime/libc.a" --compiler-runtime "$R/mapped/runtime/libcompiler_rt.a" ) \
      > "$O/platform-$shape-if$n.log" 2>&1
  echo $? > "$O/platform-$shape-if$n.rc"
done
for d in "$O"/*-if*; do
  [ -d "$d" ] || continue
  name=$(basename "$d")
  rc=$(cat "$O/$name.rc")
  if [ -f "$d/size.json" ]; then
    python3 -I -c "
import json,sys
s=json.load(open(sys.argv[1]))['split']
print(f\"{sys.argv[2]} rc={sys.argv[3]} rom={s['rom']['bytes']} sram={s['sram']['bytes']} tiles={s['tiles']} rom_banks={sum(s['rom']['banks'])}\")
" "$d/size.json" "$name" "$rc"
  else
    echo "$name rc=$rc no size.json: $(tail -1 "$O/$name.log")"
  fi
  elf=$(ls "$d"/*.elf 2>/dev/null | head -1)
  [ -n "$elf" ] && riscv32-buildroot-linux-gnu-nm -S "$elf" | awk -v n="$name" '$4=="ctrl_plat"{printf "%s ctrl_plat=%d\n", n, strtonum("0x"$2)}'
done
