#!/bin/bash
# usage: bgdir.sh NAME DIR CMD...  as bg.sh, from checkout DIR
P=${PACKET:?set PACKET to the packet directory}
N=$1; D=$2; shift 2
. $P/scripts/env.sh
cd "$D"
start=$(date +%s)
"$@" > $P/receipts/$N.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $P/receipts/$N.log
echo $rc > $P/receipts/$N.rc
