#!/bin/bash
# One shard of the firmware self-test on a clean clone at a commit, its log and rc kept. usage: fwshard.sh HEAD K
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
H=$1 K=$2
T=$VALIDATION_STORAGE/665s2b-a683q
C=$T/fw/$H-$K
mkdir -p "$T/fw"
[ -d "$C" ] || $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/clone.sh "$C" "$H" > "$T/logs/fwshard-$K.clone.log" 2>&1
cd "$C" || exit 3
export TMPDIR=$T/tmp-fw$K; mkdir -p "$TMPDIR"
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard "$K/4"; echo "rc=$?"; } > "$T/logs/fwshard-$K.log" 2>&1
