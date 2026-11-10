#!/usr/bin/env bash
# ticker.sh: every 60 s, ci_replay.py tick <head> 3 (ready instances as their own units on free 0-95 ranges), until
# every instance has a result
T=$MANAGEMENT/2026-09-23/665s7-a757c/tools; H=2128daad26b932feeed1ef2bde8f2774e8a51a31
cd /data-2/milan/tmp/665s7-a757c
while true; do
  echo "$(date +%T) $(python3 $T/ci_replay.py tick $H 3 | tr '\n' ' ')"
  python3 $T/ci_replay.py tick $H 0 > /dev/null 2>&1 && break
  python3 -c "import time; time.sleep(60)"
done
