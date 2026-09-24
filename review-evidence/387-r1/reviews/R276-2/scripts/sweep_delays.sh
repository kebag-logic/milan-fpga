#!/bin/sh
# Run one built gmstep binary at a list of feed delays, at most 8 at once,
# one log per delay, then summarise each: checks, failures, failing check
# names and the printed render fills.
# Usage: sweep_delays.sh <clone> <mdir> <logdir> <delay>...
set -u
repo=$1; mdir=$2; logs=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$logs"
printf '%s\n' "$@" | xargs -P 8 -I{} sh -c "\"$here/run_gmstep.sh\" \"$repo\" \"$mdir\" {} > \"$logs/delay-{}.log\" 2>&1"
for d in "$@"; do
  f="$logs/delay-$d.log"
  tally=$(grep -E '^== gmstep: checks' "$f" | sed 's/== gmstep: //; s/ ==//')
  fills=$(grep -E '^RENDER: fill after each push' "$f" | sed -E 's/.*push ([0-9.]+) events.*accept ([0-9.]+) .*/push=\1 accept=\2/')
  fails=$(grep -E '^\s*\[FAIL\]' "$f" | sed -E 's/^\s*\[FAIL\] //; s/ +got=.*//' | tr '\n' ';')
  echo "delay=$d | $tally | $fills | $(grep -E '^EXIT=' "$f") | fails: ${fails:-none}"
done
