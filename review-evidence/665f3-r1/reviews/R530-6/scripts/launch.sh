#!/usr/bin/env bash
# Launch the independent R530-6 runs, each with its own log and rc file.
# Usage: launch.sh <clone> <packet>
set -u
C=$1; P=$2; R=$P/receipts; S=$P/scratch
export MILAN_RV32_CC=$S/sdk/host/bin/riscv32-linux-gcc
mkdir -p $R/campaign $R/probes $S/suite $S/cov $S/image $S/probes $S/campaign
bg() { local name=$1; shift; ( cd "$C" && "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) & }
bg suite python3 -I sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 2 --build-dir $S/suite
bg cov_check python3 -I sw/firmware/gtest/fw_coverage.py --check --jobs 2 --keep $S/cov
bg cov_selftest python3 -I sw/firmware/gtest/fw_coverage.py --selftest
bg image python3 sw/firmware/ctrl/test/ctrl_image.py --base 13e715136b0b7c8d9763e0b730d9709f2c9f5932 --out $S/image
( for n in app-maap-mac-per-interface app-own-mac-per-interface app-three-way-bound-drops-maap \
           app-three-way-bound-one-maap-poll rp-null rp-maap-mac-plus-one rp-maap-pass-event-7 \
           rp-share-rx-record-plus-one; do echo $n; done |
  xargs -P 3 -I{} sh -c "cd '$C' && python3 -I '$P/scripts/probe_mutant.py' '$C' '$S/probes' {} --jobs 1 > '$R/probes/{}.log' 2>&1; echo \$? > '$R/probes/{}.rc'" ) &
( seq 1 20 | xargs -P 8 -I{} sh -c "cd '$C' && python3 -I sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice {}/20 --jobs 1 --build-dir '$S/campaign/{}' > '$R/campaign/slice{}.log' 2>&1; echo \$? > '$R/campaign/slice{}.rc'" ) &
wait
