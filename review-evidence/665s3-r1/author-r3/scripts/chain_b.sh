#!/bin/bash
# Chain B at one head: the memory test, the linked images, the firmware self-test's four shards, the firmware
# coverage, the split boot simulation (both points, their regrades, its native controls and self-test), the CPU
# budget harness at 8x8; each step its own unit and clone.
# usage: chain_b.sh COMMIT CPUS
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697d/scripts
C=$1 CPUS=$2 W=$VALIDATION_STORAGE/665s3-a697d/$1 R=$MANAGEMENT/2026-09-23/665s3-a697d/receipts/gates-at-$1
mkdir -p "$W" "$R"
for d in mem img f0 f1 f2 f3 cov boot s2b; do [ -e "$W/$d" ] || bash $S/clone.sh "$W/$d" "$C" > "$R/clone-$d.txt" 2>&1; done
bash $S/unitw.sh mem-$C "$CPUS" "$W/mem" "$R/test_ctrl_memory.log" . python3 sw/litex/test_ctrl_memory.py
bash $S/unitw.sh img-$C "$CPUS" "$W/img" "$R/images.log" . /bin/bash $S/images.sh "$W/img" "$W/img-out" "$R/images"
for k in 0 1 2 3; do
    bash $S/unitw.sh f$k-$C "$CPUS" "$W/f$k" "$R/selftest-shard$k.log" . python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard $k/4 --jobs 8
done
bash $S/unitw.sh cov-$C "$CPUS" "$W/cov" "$R/fw_coverage.log" . /bin/bash -c "python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8"
mkdir -p "$R/boot"
bash $S/unitw.sh boot-$C "$CPUS" "$W/boot" "$R/boot/runner.log" . /bin/bash $S/boot.sh "$W/boot" "$W/boot-build" "$R/boot"
bash $S/unitw.sh s2b-$C "$CPUS" "$W/s2b" "$R/s2_harness-8x8.log" . python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$W/s2build/budget-8x8" --record-budget-findings --jobs 4
echo "chain B done $(date)" > "$R/chain_b.done"
