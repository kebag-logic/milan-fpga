#!/bin/sh
# bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
# (the packet is this script's parent directory; scratch/vbin holds the pinned verilator link)
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
( cd "$dir" && export TMPDIR=$P/scratch/tmp && PATH=$P/scratch/vbin:$PATH && export PATH && \
  { date -u +%FT%TZ; echo "+ $*"; } > "$P/receipts/$name.log" && \
  start=$(date +%s) && "$@" >> "$P/receipts/$name.log" 2>&1; rc=$?; \
  echo "elapsed_s $(( $(date +%s) - start ))" >> "$P/receipts/$name.log"; echo $rc > "$P/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
echo started $name
