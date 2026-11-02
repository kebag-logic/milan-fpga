#!/bin/bash
# The saved-state store's gate with its planted defects, on a clean clone. usage: nvmself.sh HEAD
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/env.sh
H=$1
T=$VALIDATION_STORAGE/665s2b-a683o
C=$T/fw/$H-nvm
[ -d "$C" ] || $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/clone.sh "$C" "$H" > /dev/null 2>&1
cd "$C" || exit 3
{ echo "HEAD $(git rev-parse HEAD)"; python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4; echo "rc=$?"; } > "$T/logs/nvmself.log" 2>&1
