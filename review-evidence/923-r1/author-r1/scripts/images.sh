#!/usr/bin/env bash
# images.sh <clone>: both split platform images (1x1/1if, 8x8/1if) through S9's recipe, each directive in turn, one
# Vivado build at a time through vivado-slot.sh: the recipe's ExtraPostPlacementOpt for both, then ExtraTimingOpt,
# then AltSpreadLogic_high.
set -u
L=$1; T=/data-2/milan/tmp/923-a789; S=$MANAGEMENT/2026-09-23/923-a789/round1/scripts
mkdir -p $T/logs
for D in ExtraPostPlacementOpt ExtraTimingOpt AltSpreadLogic_high; do
  for STEM in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    case $STEM in *1x1*) E=$T/standin-1x1.elf; R=$T/build/b1x1/runtime;; *) E=$T/standin-8x8.elf; R=$T/build/b8x8/runtime;; esac
    $MANAGEMENT/2026-09-23/vivado-slot.sh $S/image.sh "$L" $STEM $D "$E" "$R" > $T/logs/image-$STEM-$D.log 2>&1
    echo "$STEM $D rc=$? $(date -Iseconds)" >> $T/logs/images.rc
  done
done
