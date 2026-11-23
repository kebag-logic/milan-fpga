#!/bin/bash
# plat_images.sh CLONE OUT: the target platform's split image at every ledger point by the tree's own plat_ledger.py
# (each shape's split export, flash map and runtime built under OUT), then the size fixture's images at the four points
# on that runtime and map (ctrl_srp_image.py, the ledgered point named at 8x8/2if). Read-only on CLONE apart from the
# builder's ignored outputs.
set -u
T=$1 O=$2
mkdir -p "$O"; cd "$T" || exit 3
echo "tree $(git rev-parse HEAD) dirty $(git status --porcelain | wc -l) start $(date +%T)" > "$O/HEAD.txt"
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$O/plat" > "$O/plat_ledger.log" 2>&1
echo $? > "$O/plat_ledger.rc"
RT=$O/plat/runtime
for spec in "1x1 endstation_ax7101_1x1_tdm8 1" "1x1 endstation_ax7101_1x1_tdm8 2" "8x8 endstation_ax7101_8x8 1" \
            "8x8 endstation_ax7101_8x8 2"; do
  set -- $spec; shape=$1 cfg=$2 n=$3
  fx=(); [ "$shape$n" = "8x82" ] && fx=(--ledgered-point 8x8-two-interfaces)
  python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $n --with-aecp \
    --layout split "${fx[@]}" --output "$O/fixture-$shape-if$n" --flash-map "$O/plat/$cfg/split-soc/flash-map" \
    --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" > "$O/fixture-$shape-if$n.log" 2>&1
  echo $? > "$O/fixture-$shape-if$n.rc"
done
echo "end $(date +%T) dirty-after $(git status --porcelain | wc -l)" >> "$O/HEAD.txt"
