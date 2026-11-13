#!/bin/sh
# Run one jobs_probe.py variant in the probe environment.
# usage: run_jobs_probe.sh <variant>
. $REVIEWS/gptp104-r840-1-packet/scripts/env.sh
cd $S || exit 9
python3 -I $P/scripts/jobs_probe.py $S/trees/head $S $P/receipts/jobs-probe "$1" > $S/jobs-$1.out 2>&1
echo "rc=$?" > $S/jobs-$1.done
