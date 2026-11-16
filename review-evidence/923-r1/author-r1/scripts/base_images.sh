#!/usr/bin/env bash
# base_images.sh <base clone>: both split platform images at the base commit at the recipe's directive, for the area
# delta, one Vivado build at a time through vivado-slot.sh.
set -u
L=$1; T=/data-2/milan/tmp/923-a789; S=$MANAGEMENT/2026-09-23/923-a789/round1/scripts
mkdir -p $T/logs
for STEM in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  case $STEM in *1x1*) E=$T/standin-1x1.elf; R=$T/build/b1x1/runtime;; *) E=$T/standin-8x8.elf; R=$T/build/b8x8/runtime;; esac
  $MANAGEMENT/2026-09-23/vivado-slot.sh $S/base_image.sh "$L" $STEM ExtraPostPlacementOpt "$E" "$R" > $T/logs/baseimage-$STEM.log 2>&1
  echo "$STEM base rc=$? $(date -Iseconds)" >> $T/logs/baseimages.rc
done
