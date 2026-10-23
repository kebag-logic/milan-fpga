#!/usr/bin/env bash
# milan_dp_render: both clean legs, positive controls and leg defects, and the four #632 gateware mutants
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final
cd $LANES/632-phase/tb/verilator/milan_dp_render
git rev-parse HEAD > $L/d.head
make tdm8render-build tdm8render-multi-build > $L/tdm8_build.log 2>&1; echo $? > $L/tdm8_build.rc
python3 $VALIDATION_STORAGE/scratch/632-a659/r4/tools/tdm8_subset.py "the render out-lead one frame long" "the domain event's instant not back-dated" "the render out-lead one frame long, at every [LAW] phase" "the settle recentre never pulses" > $L/tdm8_subset.log 2>&1; echo $? > $L/tdm8_subset.rc
echo DONE > $L/d.done
