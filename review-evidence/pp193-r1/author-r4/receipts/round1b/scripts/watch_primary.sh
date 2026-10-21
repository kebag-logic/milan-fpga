#!/usr/bin/env bash
# usage: watch_primary.sh <primary pgid> <primary out> <helper out>
# Stops the primary runner's group when it starts a campaign the helper
# claimed, and removes that partial start; ends when the helper ends.
pg=$1; prim=$2; help=$3
while [ ! -f "$help/HELPER.done" ] || pgrep -g "$pg" >/dev/null; do
  for l in "$prim"/*.log; do
    c=$(basename "$l" .log)
    if [ ! -f "$prim/$c.rc" ] && [ -d "$help/claims/$c" ]; then
      kill -TERM -- -"$pg"; sleep 5; kill -KILL -- -"$pg" 2>/dev/null
      rm -rf "$prim/$c.log" "$prim/work/$c"
      echo "primary stopped before $c at $(date -Is)" > "$prim/MET.txt"
      exit 0
    fi
  done
  pgrep -g "$pg" >/dev/null || exit 0
  sleep 10
done
