#!/bin/bash
# fw_coverage.py --check on a checkout. usage: cov.sh CHECKOUT TAG
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
cd "$1" && { python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8; echo "rc=$?"; } > $T/logs/cov-$2.log 2>&1
