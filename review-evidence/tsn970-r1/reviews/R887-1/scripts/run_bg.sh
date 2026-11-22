#!/bin/bash
# run_bg.sh NAME DIR CMD... : run CMD in DIR detached; log to receipts/NAME.log and the exit status to receipts/NAME.rc
# (the packet is this script's parent directory; TOOLS must be set for env.sh).
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
nohup setsid bash -c "source $P/scripts/env.sh; cd $dir && $*; echo \$? > $P/receipts/$name.rc" > "$P/receipts/$name.log" 2>&1 < /dev/null &
echo "started $name"
