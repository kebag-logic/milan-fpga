#!/bin/bash
# The firmware gate on the working tree (no plants), its log and rc kept. usage: devfw.sh NAME
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/fw-$1; mkdir -p "$TMPDIR"
cd $LANES/665-s2b-cycles
{ python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --lwsrp third_party/lwSRP --jobs 4; echo "rc=$?"; } > "$T/logs/$1.log" 2>&1
