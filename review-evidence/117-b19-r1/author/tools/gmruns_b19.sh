#!/usr/bin/env bash
# Lane B19: software-GM runs FIRST..LAST in the foreground, one lock window each (lane B1's gmruns.sh with
# the lane's runner and checks); stop on any failure. Each run: 40 s alignment as a never-grandmaster port,
# +GM_OFFSET on the controller host's PHC, then the measurement with the software grandmaster held for 50 s.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
for i in $(seq "$1" "$2"); do
  n=$(printf 'gm%02d' "$i")
  GM_OFFSET=0.010 PAIRS=all B19_ENV=/tmp/a624/priv/env.sh "$P/tools/run_locked_b19.sh" "$n" 120 gm 50 10 > "/tmp/a624/raw/$n.out" 2>&1
  grep -E "gm-prep-converged|gm-prep-offset|gm-start|gm-end|ACTION_RC|LOCK_RC|LOCK " "/tmp/a624/raw/$n.out" | cut -c1-220
  grep -q "ACTION_RC=0" "/tmp/a624/raw/$n.out" || { echo "STOP: action failed $n"; exit 2; }
  timeout 300 python3 -B "$P/tools/a624_analyze.py" "$n" > /dev/null 2>&1 || { echo "STOP: analysis failed $n"; exit 2; }
  timeout 200 python3 -B "$P/tools/cyc_check.py" "$n" > "$P/bench/$n/check.txt"; rc=$?
  cat "$P/bench/$n/check.txt"
  [ "$rc" = 0 ] || { echo "NOT RESTORED at end of $n"; exit 3; }
done
