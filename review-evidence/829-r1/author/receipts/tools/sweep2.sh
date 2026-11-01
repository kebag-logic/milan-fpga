#!/usr/bin/env bash
# sweep2.sh: the before-and-after rows on the final image: reset value, 0/0, three written sums, the pair from math, the reset pair, the compensation. Each step takes the bench lock and releases it.
set -u
O=$MANAGEMENT/2026-09-23/829-a725b/receipts
T=$VALIDATION_STORAGE/829-a725b/tools
one() { # dir seconds ing egr
  d=$O/$1; mkdir -p "$d"
  if [ -n "${3:-}" ]; then flock -w 200 /tmp/milan-bench.lock python3 $T/lat.py "$d/write.txt" write "$3" "$4" | tee "$d/write.stdout"; sleep 3; fi
  POLL_PERIOD=5 $T/measure.sh "$d" "$2" 2>&1 | tail -1 | python3 -c "
import json,sys
r=json.loads(sys.stdin.read())
print({k:r[k] for k in ('dir','n_arty','arty','arty_sd','zero','zero_sd','residual','sum','pdelay_mean','pdelay_min','pdelay_max','predicted_pdelay','gptp_lat','ascapable','sync','tu')})"
}
one f-00-after-flash-reset-pair 50
one f-01-pair-0-0 130 0 0
one f-02-pair-400-0 70 400 0
one f-03-pair-0-400 70 0 400
one f-04-pair-800-400 70 800 400
date
