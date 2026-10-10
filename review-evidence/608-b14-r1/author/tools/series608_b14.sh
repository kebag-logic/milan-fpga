#!/usr/bin/env bash
# Lane B14 item 3: run cycles FIRST..LAST in the foreground, one bench-lock window each (lane B2's series.sh).
# Stops on any action or analysis failure. usage: series608_b14.sh FIRST LAST; endpoints from B14_ENV (private).
set -u
set -a; . "${B14_ENV:?}"; set +a
T=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$T")
mkdir -p /tmp/608-b14/raw/item3
for i in $(seq "$1" "$2"); do
  n=$(printf 'cycle-%03d' "$i")
  "$T/run_locked_b14.sh" 130 python3 -B "$T/cyc608_b14.py" "$n" cycle "$DUT_CONSOLE" "$CTL_HOST" "$CTL_IFACE" "$TAP_HOST" "$TAP_IFACE" > "/tmp/608-b14/raw/item3/$n.out" 2>&1
  cp "/tmp/608-b14/raw/item3/$n.out" "$P/item3/cycles/$n/action.log" 2>/dev/null
  grep -q "ACTION_RC=0" "/tmp/608-b14/raw/item3/$n.out" || { echo "STOP: action failed $n"; grep -E "ACTION_RC|LOCK_RC|Error|assert" "/tmp/608-b14/raw/item3/$n.out"; exit 2; }
  line=$(cd "$P" && timeout 60 python3 -B "$T/an608_b14.py" "item3/cycles/$n") || { echo "STOP: analysis failed $n"; exit 2; }
  echo "$line $(grep -E '^LOCK |^UNLOCK ' /tmp/608-b14/raw/item3/$n.out | awk '{print $2}' | tr '\n' ' ')"
done
