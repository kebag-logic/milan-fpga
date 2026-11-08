#!/bin/bash
# Run named jobs concurrently, each with its own log and rc file, and wait for all of them.
# usage: wave.sh NAME "command" [NAME "command"]...
set -u; . "$(dirname "$0")/env.sh"
L=$RCP/wave-logs; mkdir -p "$L"; pids=()
while [ $# -ge 2 ]; do n=$1 c=$2; shift 2
  ( bash -c "$c" > "$L/$n.log" 2>&1; echo $? > "$L/$n.rc" ) & pids+=($!)
done
wait "${pids[@]}"
for f in "$L"/*.rc; do echo "$(basename "$f" .rc): rc $(cat "$f")"; done
