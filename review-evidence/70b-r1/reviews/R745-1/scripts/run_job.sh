#!/usr/bin/env bash
# run_job.sh NAME DIR CMD... : run CMD in DIR, log to receipts/NAME.log, rc to receipts/NAME.rc
set -u
P="$(cd "$(dirname "$0")/.." && pwd)"
name=$1; dir=$2; shift 2
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH"
cd "$dir" || exit 2
{ echo "# job $name  dir=$dir  start=$(date -u +%FT%TZ)"; echo "# cmd: $*"; } > "$P/receipts/$name.log"
"$@" >> "$P/receipts/$name.log" 2>&1
rc=$?
echo "# end=$(date -u +%FT%TZ) rc=$rc" >> "$P/receipts/$name.log"
echo $rc > "$P/receipts/$name.rc"
