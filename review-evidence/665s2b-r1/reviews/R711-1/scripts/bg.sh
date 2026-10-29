#!/bin/bash
# usage: bg.sh NAME CMD...  run CMD detached from the checkout, log to receipts/NAME.log, rc to receipts/NAME.rc
P=${PACKET:?set PACKET to the packet directory}
N=$1; shift
. $P/scripts/env.sh
cd "${CHECKOUT:?set CHECKOUT to the reviewed checkout}"
start=$(date +%s)
"$@" > $P/receipts/$N.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $P/receipts/$N.log
echo $rc > $P/receipts/$N.rc
