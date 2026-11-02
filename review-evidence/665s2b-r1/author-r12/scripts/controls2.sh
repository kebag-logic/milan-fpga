#!/bin/bash
# The cached window and the whole-page read together, the state before the fixes, for the figures the docs quote.
S=$MANAGEMENT/2026-09-23/665s2b-a683o/scripts
T=$VALIDATION_STORAGE/665s2b-a683o
$S/leg.sh $T/CC CC-A1 1x1 acmp-disc &
$S/leg.sh $T/CC CC-A8 8x8 acmp-disc &
wait
