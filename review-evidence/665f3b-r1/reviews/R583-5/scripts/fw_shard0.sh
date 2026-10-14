#!/bin/sh
# R583-5: firmware-unit shard 0 exactly as the hosted job runs it. Usage: fw_shard0.sh <clone> <packet>
CLONE=$1; PKT=$2; R=$PKT/receipts/campaign
export TMPDIR=$PKT/scratch/tmp PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
cd "$CLONE" || exit 2
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 --build-dir "$PKT/scratch/fw0" >"$R/fw_shard0.log" 2>&1
echo $? >"$R/fw_shard0.rc"
