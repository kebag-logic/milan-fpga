#!/bin/bash
# Usage: bg.sh NAME DIR CMD...  -- run CMD detached in DIR; log receipts/runs/NAME.log, rc+seconds receipts/runs/NAME.rc
P=$PACKET; S=$P/scratch
name=$1; dir=$2; shift 2
export PYTHONDONTWRITEBYTECODE=1 MILAN_RV32_CC=$S/sdk/bin/riscv32-linux-gcc TMPDIR=$S/tmp
rm -f $P/receipts/runs/$name.rc
setsid nohup bash -c 'cd "$0"; start=$(date +%s); "${@}" > '"$P/receipts/runs/$name.log"' 2>&1; rc=$?; echo "$rc $(( $(date +%s)-start ))s" > '"$P/receipts/runs/$name.rc" "$dir" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name pid $!"
