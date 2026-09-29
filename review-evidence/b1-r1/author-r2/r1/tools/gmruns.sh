#!/usr/bin/env bash
# Run software-GM runs FIRST..LAST in the foreground, one lock window each; stop on failure.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
for i in $(seq "$1" "$2"); do
  n=$(printf 'gm%02d' "$i")
  B1_ENDPOINTS=/tmp/b1-a438/endpoints.sh "$P/tools/run_locked.sh" "$n" 120 gm 50 10 > "/tmp/b1-a438/raw/$n.out" 2>&1
  grep -E "gm-prep-converged|gm-prep-offset|gm-start|gm-end|ACTION_RC|LOCK_RC" "/tmp/b1-a438/raw/$n.out" | cut -c1-220
  grep -q "ACTION_RC=0" "/tmp/b1-a438/raw/$n.out" || { echo "STOP: action failed $n"; exit 2; }
  timeout 300 python3 -B "$P/tools/b1_analyze.py" "$n" > /dev/null 2>&1 || { echo "STOP: analysis failed $n"; exit 2; }
  python3 -B "$P/tools/b1_gmcheck.py" "$n" | tee "$P/bench/$n/check.txt"
  if [ "${PIPESTATUS[0]}" != 0 ]; then echo "NOT RESTORED at end of $n"; exit 3; fi
done
