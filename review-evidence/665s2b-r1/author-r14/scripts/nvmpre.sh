#!/bin/bash
# The store's suite on a checkout, then the named plants. usage: nvmpre.sh CHECKOUT TAG NAMES
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683q
export TMPDIR=$T/tmp/nvm-$2; mkdir -p $TMPDIR; rm -rf $T/nvm-$2-work
cd "$1" && { python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4; echo "suite rc=$?"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/nvmplants.py "$1" $T/nvm-$2-work "$3"; echo "rc=$?"; } > $T/logs/nvmpre-$2.log 2>&1
