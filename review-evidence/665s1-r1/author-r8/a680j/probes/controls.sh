#!/bin/bash
# The harness's two 1x1 controls at the lane head: the slow ADP receive handler (group control) and the as-built CPU regions.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680j/probes
C=$LANES/665-s1-faces
"$O/leg.sh" "$C" C-slow 1x1 --mutation slow-adp-rx --groups control --jobs 4
"$O/leg.sh" "$C" C-asbuilt 1x1 --cpu-regions as-built --groups control --jobs 4
