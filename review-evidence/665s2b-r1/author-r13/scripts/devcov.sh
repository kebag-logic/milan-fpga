#!/bin/bash
# The coverage gate on the working tree, its log and rc kept. usage: devcov.sh NAME
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/cov-$1; mkdir -p "$TMPDIR"
cd $LANES/665-s2b-cycles
{ python3 -B sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 4; echo "rc=$?"; } > "$T/logs/$1.log" 2>&1
