#!/bin/bash
# fixture_sizes.sh TREE LEDGER OUT: the size fixture's image (ctrl_srp_image.py --with-aecp --layout split) at the four
# ledger points, against the ledger run's flash maps and runtime, the 8x8 two-interface one at its ledgered point; each
# image's size.json, and the plan line its log prints
set -u
T=$1 L=$2 O=$3
mkdir -p $O
rc=0
for p in "1x1_tdm8 1" "1x1_tdm8 2" "8x8 1" "8x8 2"; do
  set -- $p; cfg=$1 n=$2 name=${cfg%_tdm8}-if$n
  extra=(); [ "$cfg-$n" = 8x8-2 ] && extra=(--ledgered-point 8x8-two-interfaces)
  python3 -B $T/sw/firmware/ctrl/test/ctrl_srp_image.py --config $T/configs/endstation_ax7101_$cfg.yaml \
    --interfaces $n --with-aecp --layout split --flash-map $L/endstation_ax7101_$cfg/split-soc/flash-map \
    --output $O/$name --libc $L/runtime/libc.a --compiler-runtime $L/runtime/libcompiler_rt.a "${extra[@]}" \
    > $O/$name.log 2>&1 || rc=1
  echo "$name rc=$?"
done
exit $rc
