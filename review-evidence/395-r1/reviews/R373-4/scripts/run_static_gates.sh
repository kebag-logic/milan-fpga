#!/usr/bin/env bash
# Usage: run_static_gates.sh <repository> <receipts dir> <markdown python> [jobs]
# Runs every line of static_gates.txt ("name|command") through run_logged.sh,
# at most <jobs> at a time, then writes a summary table of exit codes.
set -u
here=$(cd "$(dirname "$0")" && pwd)
repo=$1; out=$2; mdpy=$3; jobs=${4:-4}
sed "s#MDPY#$mdpy#" "$here/static_gates.txt" |
  xargs -P "$jobs" -I{} bash -c 'line="$1"; name=${line%%|*}; cmd=${line#*|};
    "$0" "$2/$name.log" "$3" bash -c "$cmd"' "$here/run_logged.sh" {} "$out" "$repo"
for f in "$out"/[2-5][0-9]_*.log; do
  printf '%s rc=%s wall=%s\n' "$(basename "$f" .log)" \
    "$(sed -n 's/^# rc: //p' "$f")" "$(sed -n 's/^# wall_seconds: //p' "$f")"
done > "$out/static_gates_summary.txt"
cat "$out/static_gates_summary.txt"
