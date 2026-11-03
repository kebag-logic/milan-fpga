#!/bin/bash
# fw_coverage.py --write on a checkout (the ratchet's generator). usage: covwrite.sh CHECKOUT TAG
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683q
cd "$1" && { python3 sw/firmware/gtest/fw_coverage.py --write --lwsrp third_party/lwSRP --jobs 8; echo "rc=$?"; } > $T/logs/covwrite-$2.log 2>&1
