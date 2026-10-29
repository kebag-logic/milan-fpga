#!/bin/bash
# Chain B at one head: the memory test, the linked images, the firmware self-test's four shards; each step its
# own unit and clone.
# usage: chain_b.sh COMMIT CPUS
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697c/scripts
C=$1 CPUS=$2 W=$VALIDATION_STORAGE/665s3-a697c/$1 R=$MANAGEMENT/2026-09-23/665s3-a697c/receipts/gates-at-$1
mkdir -p "$W" "$R"
for d in mem img f0 f1 f2 f3; do [ -e "$W/$d" ] || bash $S/clone.sh "$W/$d" "$C" > "$R/clone-$d.txt" 2>&1; done
bash $S/unitw.sh mem-$C "$CPUS" "$W/mem" "$R/test_ctrl_memory.log" . python3 sw/litex/test_ctrl_memory.py
bash $S/unitw.sh img-$C "$CPUS" "$W/img" "$R/images.log" . /bin/bash $S/images.sh "$W/img" "$W/img-out" "$R/images"
for k in 0 1 2 3; do
    bash $S/unitw.sh f$k-$C "$CPUS" "$W/f$k" "$R/selftest-shard$k.log" . python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard $k/4 --jobs 8
done
echo "chain B done $(date)" > "$R/chain_b.done"
