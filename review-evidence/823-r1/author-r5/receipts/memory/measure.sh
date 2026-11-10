#!/usr/bin/env bash
# measure.sh <label> <nvm-source>: link the split size fixture at the four points and plan each.
set -u
L=$1; SRC=$2; R=<scratch>/mem/runtime; O=<scratch>/mem/$L
mkdir -p $O
for p in "1x1_tdm8 1" "1x1_tdm8 2" "8x8 1" "8x8 2"; do
  set -- $p
  cfg=configs/endstation_ax7101_$1.yaml; n=$2; out=$O/$1-if$n
  extra=""; [ "$1" = 8x8 ] && [ "$n" = 2 ] && extra="--ledgered-point 8x8-two-interfaces"
  python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config $cfg --interfaces $n --with-aecp --layout split \
    --nvm-source "$SRC" $extra --output $out --libc $R/libc.a --compiler-runtime $R/libcompiler_rt.a \
    > $out.log 2>&1
  echo "$L $1 if$n rc=$?"
done
