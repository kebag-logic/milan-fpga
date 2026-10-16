#!/usr/bin/env bash
# Lane B19: run OUT4 cycles FIRST..LAST in the foreground, one lock window each (lane B1's cycles.sh with
# the lane's runner and checks); stop on any failure. PAIRS (all|music) is passed through.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
for i in $(seq "$1" "$2"); do
  n=$(printf 'cycle%02d' "$i")
  B19_ENV=/tmp/a624/priv/env.sh "$P/tools/run_locked_b19.sh" "$n" 120 cycle 20 10 > "/tmp/a624/raw/$n.out" 2>&1
  grep -E "ACTION_RC|LOCK_RC|LOCK " "/tmp/a624/raw/$n.out"
  grep -q "ACTION_RC=0" "/tmp/a624/raw/$n.out" || { echo "STOP: action failed $n"; exit 2; }
  timeout 300 python3 -B "$P/tools/a624_analyze.py" "$n" > /dev/null 2>&1 || { echo "STOP: analysis failed $n"; exit 2; }
  timeout 200 python3 -B "$P/tools/cyc_check.py" "$n" > "$P/bench/$n/check.txt"; rc=$?
  cat "$P/bench/$n/check.txt"
  [ "$rc" = 0 ] || { echo "NOT RECOVERED at end of $n"; exit 3; }
done
