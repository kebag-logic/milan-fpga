#!/usr/bin/env bash
# Run cycles FIRST..LAST in the foreground, one bench-lock window each.
# Stops on any action or analysis failure, and after ten consecutive #75 overruns (the PR #604 rule).
# usage: series.sh FIRST LAST; endpoints from B2_ENDPOINTS (private).
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
streak=0
for i in $(seq "$1" "$2"); do
  n=$(printf 'cycle-%03d' "$i")
  "$P/tools/run_action.sh" "$n" cycle > "/tmp/b2-a440/raw/$n.out" 2>&1
  cp "/tmp/b2-a440/raw/$n.out" "$P/cycles/$n/action.log" 2>/dev/null
  grep -q "ACTION_RC=0" "/tmp/b2-a440/raw/$n.out" || { echo "STOP: action failed $n"; grep -E "ACTION_RC|LOCK_RC|Error|assert" "/tmp/b2-a440/raw/$n.out"; exit 2; }
  line=$(timeout 60 python3 -B "$P/tools/b2_analyze.py" "cycles/$n") || { echo "STOP: analysis failed $n"; exit 2; }
  echo "$line"
  timeout 30 python3 -B "$P/tools/handoff_rows.py" > /dev/null
  if echo "$line" | grep -q " FAIL "; then streak=$((streak + 1)); else streak=0; fi
  if [ "$streak" -ge 10 ]; then echo "EARLY STOP: ten consecutive overruns"; exit 3; fi
done
