#!/bin/bash
# One exclusive lock acquisition for every Vivado run, then the Vivado-free resource-gate checks.
root=$SCRATCH
export PATH=$LITEX_ENV/venv/bin:$PATH TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1
log=$root/vendor/driver.log
echo "$(date -Is) waiting for the exclusive lock" >> $log
flock $VIVADO_LOCK $root/scripts/vivado_runs.sh
echo "$(date -Is) lock released, rc $?" >> $log
for side in cand base; do
  for verb in check record; do
    (cd $root/exp-$side && python3 syn/ooc/pp_resource_gate.py $verb $root/res/$side/ax7101/gateware --endpoint route-1x1) > $root/vendor/$verb-route-1x1-$side.log 2>&1
    echo "$?" > $root/vendor/$verb-route-1x1-$side.rc
    echo "$(date -Is) $verb route-1x1 $side rc $(cat $root/vendor/$verb-route-1x1-$side.rc)" >> $log
  done
done
echo "$(date -Is) vendor done" >> $log
