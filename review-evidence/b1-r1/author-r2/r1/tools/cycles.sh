#!/usr/bin/env bash
# Run cycles FIRST..LAST in the foreground, one lock window each; stop on any failure.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
for i in $(seq "$1" "$2"); do
  n=$(printf 'cycle%02d' "$i")
  B1_ENDPOINTS=/tmp/b1-a438/endpoints.sh "$P/tools/run_locked.sh" "$n" 110 cycle 20 10 > "/tmp/b1-a438/raw/$n.out" 2>&1
  grep -E "ACTION_RC|LOCK_RC" "/tmp/b1-a438/raw/$n.out"
  grep -q "ACTION_RC=0" "/tmp/b1-a438/raw/$n.out" || { echo "STOP: action failed $n"; exit 2; }
  timeout 300 python3 -B "$P/tools/b1_analyze.py" "$n" > /dev/null 2>&1 || { echo "STOP: analysis failed $n"; exit 2; }
  python3 -B "$P/tools/b1_check.py" "$n" | tee "$P/bench/$n/check.txt"
  if [ "${PIPESTATUS[0]}" != 0 ]; then echo "NOT RECOVERED at end of $n: extend"; exit 3; fi
done
