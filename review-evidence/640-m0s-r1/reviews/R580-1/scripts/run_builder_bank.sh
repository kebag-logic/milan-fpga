#!/usr/bin/env bash
# Run the builder bank with the pinned SDK from the packet scratch home; writes log and rc.
REPO=$1; PACKET=$2; R=$PACKET/receipts/gates
export TMPDIR=$PACKET/scratch/tmp PYTHONDONTWRITEBYTECODE=1 HOME=$PACKET/scratch/home
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd "$REPO" || exit 9
start=$(date +%s)
python3 -u sw/builder/test_builder.py --require-rv32 > "$R/builder_bank.log" 2>&1
rc=$?
echo "builder_bank rc=$rc $(( $(date +%s) - start ))s" > "$R/builder_bank.time"
echo $rc > "$R/builder_bank.rc"
