#!/usr/bin/env bash
set -u
cd $LANES/671-read-fault || exit 2
export PATH="$VALIDATION_STORAGE/671-a592/venv312/bin:$PATH" TMPDIR=$VALIDATION_STORAGE/671-a592/r7/tmp
echo "START $(date -Is) $(git rev-parse HEAD) $(python3 --version)"
start=$(date +%s.%N)
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4
rc=$?
echo "END rc=$rc elapsed=$(python3 -c "print(round($(date +%s.%N) - $start, 2))") $(date -Is)"
