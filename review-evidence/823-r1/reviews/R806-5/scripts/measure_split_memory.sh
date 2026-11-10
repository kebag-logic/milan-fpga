#!/usr/bin/env bash
# measure_split_memory.sh <tree at 7c97e99f> <runtime dir with libc.a, libcompiler_rt.a> <base ctrl_nvm tree at 30ca4b21> <out>
# Links the split size fixture at the four points with this head's store and
# with 30ca4b21's, and plans each; 8x8 two interfaces against its ledger.
set -u
T=$1; R=$2; BASE=$3; O=$4
cd "$T" || exit 2
for L in head base; do
  SRC=sw/firmware/ctrl_nvm; [ "$L" = base ] && SRC=$BASE
  for p in "1x1_tdm8 1" "1x1_tdm8 2" "8x8 1" "8x8 2"; do
    set -- $p; n=$2; extra=""; [ "$1" = 8x8 ] && [ "$n" = 2 ] && extra="--ledgered-point 8x8-two-interfaces"
    mkdir -p "$O/$L"
    PYTHONDONTWRITEBYTECODE=1 python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_$1.yaml \
      --interfaces $n --with-aecp --layout split --nvm-source "$SRC" $extra --output "$O/build/$L/$1-if$n" \
      --libc "$R/libc.a" --compiler-runtime "$R/libcompiler_rt.a" > "$O/$L/$1-if$n.log" 2>&1
    echo "$L $1 if$n rc=$?"
  done
done
