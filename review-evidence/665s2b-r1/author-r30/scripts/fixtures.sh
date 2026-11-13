#!/bin/bash
# Link the size fixture's image at the four ledger points in a tree, on a plat_ledger.py build's runtime and flash maps.
# usage: fixtures.sh TREE PLAT_LEDGER_BUILD OUTDIR
set -u
T=$1 R=$2 O=$3
. /data-2/milan/tmp/665s2b-a683zo/scripts/env.sh
mkdir -p "$O"
echo "tree $(git -C $T rev-parse HEAD) dirty $(git -C $T status --porcelain | wc -l)" > $O/HEAD.txt
for spec in "1x1 endstation_ax7101_1x1_tdm8 1" "1x1 endstation_ax7101_1x1_tdm8 2" "8x8 endstation_ax7101_8x8 1" "8x8 endstation_ax7101_8x8 2"; do
  set -- $spec; shape=$1 cfg=$2 n=$3
  fx=(); [ "$shape$n" = "8x82" ] && fx=(--ledgered-point 8x8-two-interfaces)
  ( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $n --with-aecp --layout split "${fx[@]}" \
      --output $O/fixture-$shape-if$n --flash-map $R/$cfg/split-soc/flash-map --libc $R/runtime/libc.a --compiler-runtime $R/runtime/libcompiler_rt.a ) > $O/fixture-$shape-if$n.log 2>&1
  echo $? > $O/fixture-$shape-if$n.rc
  python3 -c "import json,sys; s=json.load(open('$O/fixture-$shape-if$n/size.json'))['split']; print('$shape-if$n', 'rc', open('$O/fixture-$shape-if$n.rc').read().strip(), 'rom', s['rom']['bytes'], 'in', sum(s['rom']['banks']), 'sram', s['sram']['bytes'], 'tiles', s['tiles'])" 2>/dev/null || echo "$shape-if$n rc $(cat $O/fixture-$shape-if$n.rc) $(tail -1 $O/fixture-$shape-if$n.log)"
done
