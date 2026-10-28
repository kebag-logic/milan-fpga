#!/bin/bash
# At the final head: the two 1x1 controls from the lane checkout, then the acknowledgement plants in the scratch worktree.
set -u
P=$MANAGEMENT/2026-09-23/665s1-a680j/probes
"$P/controls.sh"
"$P/plants.sh"
