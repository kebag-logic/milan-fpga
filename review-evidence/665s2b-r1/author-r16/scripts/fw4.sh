#!/bin/bash
# The firmware self-test's four shards side by side, each on its own clean clone of a commit, logs tagged.
# usage: fw4.sh HEAD TAG
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
H=$1 TAG=$2
T=$VALIDATION_STORAGE/665s2b-a683u
mkdir -p $T/fw
for K in 0 1 2 3; do
  (
    C=$T/fw/$TAG-$K
    [ -d "$C" ] || $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/clone.sh "$C" "$H" > "$T/logs/fwshard-$TAG-$K.clone.log" 2>&1
    cd "$C" || exit 3
    export TMPDIR=$T/tmp-fw-$TAG-$K; mkdir -p "$TMPDIR"
    { echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard "$K/4"; echo "rc=$?"; } > "$T/logs/fwshard-$TAG-$K.log" 2>&1
  ) &
done
wait
