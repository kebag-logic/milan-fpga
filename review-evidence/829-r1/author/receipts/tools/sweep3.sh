#!/usr/bin/env bash
set -u
O=$MANAGEMENT/2026-09-23/829-a725b/receipts
T=$VALIDATION_STORAGE/829-a725b/tools
pr() { python3 -c "
import json,sys
r=json.loads(sys.stdin.read())
print({k:r[k] for k in ('dir','n_arty','arty','arty_sd','zero','zero_sd','residual','sum','pdelay_mean','pdelay_min','pdelay_max','predicted_pdelay','gptp_lat','ascapable','sync','tu','gm')})
print(r['wire'])"; }
d=$O/f-05-pair-from-math; mkdir -p $d
flock -w 200 /tmp/milan-bench.lock python3 $T/setpair.py $O/f-01-pair-0-0/row.json true $d/write.txt | tee $d/write.stdout
sleep 3; POLL_PERIOD=5 $T/measure.sh $d 70 2>&1 | tail -1 | pr
d=$O/f-06-true-pair-reset-value; mkdir -p $d
flock -w 200 /tmp/milan-bench.lock python3 $T/lat.py $d/write.txt write 1409 100 | tee $d/write.stdout
sleep 3; POLL_PERIOD=5 $T/measure.sh $d 90 2>&1 | tail -1 | pr
d=$O/f-07-tap-comp; mkdir -p $d
flock -w 200 /tmp/milan-bench.lock python3 $T/setpair.py $O/f-06-true-pair-reset-value/row.json tap $d/write.txt | tee $d/write.stdout
sleep 8; POLL_PERIOD=5 $T/measure.sh $d 70 2>&1 | tail -1 | pr
date
