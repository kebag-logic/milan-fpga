#!/bin/bash
# bg.sh NAME CMD... : run CMD in the clone, log to receipts/NAME.log, rc to receipts/NAME.rc, pid to scratch/NAME.pid
P=$REVIEWS/697c-r585-6-packet; N=$1; shift
. $P/scripts/env.sh
cd $REVIEWS/r585-6-697c
rm -f $P/receipts/$N.rc
( start=$(date +%s); "$@" > $P/receipts/$N.log 2>&1; rc=$?; end=$(date +%s); echo "rc=$rc seconds=$((end-start))" > $P/receipts/$N.rc ) &
echo $! > $P/scratch/$N.pid
