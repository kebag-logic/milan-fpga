#!/usr/bin/env bash
# Usage: run_campaign.sh CLONE PACKET
# Starts the ctrl firmware arms and the full planted-defect campaign in three
# shards, plus the shared RV32 self-test, each detached with its own log and
# rc file under PACKET/receipts. Builds go under PACKET/scratch.
set -u
CLONE=$1 PACKET=$2
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$PACKET/scratch/tmp
mkdir -p "$TMPDIR" "$PACKET/receipts"
cd "$CLONE" || exit 2
start() {  # name, command...
    local name=$1; shift
    rm -f "$PACKET/receipts/$name.rc"
    nohup bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$PACKET/receipts/$name" "$@" >/dev/null 2>&1 &
}
for i in 0 1 2; do
    start "ctrl_selftest_shard${i}of3" python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 \
        --self-test --mutation-shard "$i" 3 --build-dir "$PACKET/scratch/ctrl_shard$i"
done
start fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
