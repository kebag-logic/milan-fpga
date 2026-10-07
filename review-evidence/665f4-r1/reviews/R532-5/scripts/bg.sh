#!/bin/bash
# Usage: bg.sh NAME DIR CMD...  -- run CMD detached in DIR; log to receipts/runs/NAME.log, rc to NAME.rc
P=$REVIEWS/665f4-r532-5-packet; S=$P/scratch
name=$1; dir=$2; shift 2
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$PATH PYTHONDONTWRITEBYTECODE=1 MILAN_RV32_CC=$S/sdk/bin/riscv32-buildroot-linux-gnu-gcc TMPDIR=$S/tmp
rm -f $P/receipts/runs/$name.rc
setsid nohup bash -c 'cd "$0"; start=$(date +%s); "${@}" > '"$P/receipts/runs/$name.log"' 2>&1; rc=$?; echo "$rc $(( $(date +%s)-start ))s" > '"$P/receipts/runs/$name.rc" "$dir" "$@" < /dev/null > /dev/null 2>&1 &
