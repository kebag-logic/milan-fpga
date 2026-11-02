#!/bin/bash
# The coverage ratchet written by its generator on the lane's tree.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/covw; mkdir -p "$TMPDIR"
cd $LANES/665-s2b-cycles
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B sw/firmware/gtest/fw_coverage.py --write --lwsrp third_party/lwSRP --jobs 4; echo "rc=$?"; } > "$T/logs/covwrite.log" 2>&1
