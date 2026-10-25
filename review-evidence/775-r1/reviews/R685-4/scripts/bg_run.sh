#!/bin/sh
# usage: bg_run.sh NAME DIR CMD...  -> receipts/NAME.log, receipts/NAME.rc
# Runs CMD in DIR with the pinned Verilator 5.050 first on PATH.
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH TMPDIR=$P/scratch/tmp
cd "$dir" || exit 2
{ echo "# cmd: $*"; echo "# dir: $dir"; echo "# verilator: $(verilator --version)"; date -u +"# start %FT%TZ"; } > $P/receipts/$name.log
"$@" >> $P/receipts/$name.log 2>&1; rc=$?
date -u +"# end %FT%TZ rc=$rc" >> $P/receipts/$name.log
echo $rc > $P/receipts/$name.rc
