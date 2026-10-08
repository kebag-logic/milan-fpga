#!/usr/bin/env bash
# Full ctrl+SRP mutation campaign at the candidate, as the composed rtl-fast firmware-unit step runs it.
# Usage: run_campaign.sh <clone> <packet>
set -u
CLONE=$1; PKT=$2; R=$PKT/receipts
export TMPDIR=$PKT/scratch/tmp MILAN_RV32_CC=riscv64-elf-gcc
cd "$CLONE" || exit 2
( echo '$ python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4'
  timeout 7000 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 ) > "$R/ctrl_campaign.log" 2>&1
echo $? > "$R/ctrl_campaign.rc"
