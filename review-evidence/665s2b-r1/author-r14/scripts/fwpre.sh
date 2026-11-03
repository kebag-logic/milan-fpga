#!/bin/bash
# The firmware suite on a checkout (no plants). usage: fwpre.sh CHECKOUT TAG
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683q
export TMPDIR=$T/tmp/fw-$2; mkdir -p $TMPDIR; rm -rf $T/fw-$2
cd "$1" && { python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir $T/fw-$2; echo "rc=$?"; } > $T/logs/fwpre-$2.log 2>&1
