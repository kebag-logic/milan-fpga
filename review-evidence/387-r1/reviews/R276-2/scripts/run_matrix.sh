#!/bin/sh
# Run "<name> <mdir> <delay>" jobs from stdin, at most 8 at once, one log
# per job under <logdir>, then summarise each job's tally and failing checks.
# Usage: run_matrix.sh <clone> <logdir> < jobs
set -u
repo=$1; logs=$2
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$logs"
jobs=$(cat)
printf '%s\n' "$jobs" | xargs -P 8 -L 1 sh -c "\"$here/run_gmstep.sh\" \"$repo\" \"\$1\" \"\$2\" > \"$logs/\$0-delay-\$2.log\" 2>&1"
printf '%s\n' "$jobs" | while read -r name mdir delay; do
  f="$logs/$name-delay-$delay.log"
  tally=$(grep -E '^== gmstep: checks' "$f" | sed 's/== gmstep: //; s/ ==//')
  fails=$(grep -E '^\s*\[FAIL\]' "$f" | sed -E 's/^\s*\[FAIL\] //; s/ +got=/ got=/' | tr '\n' ';')
  echo "$name delay=$delay | $tally | $(grep -E '^EXIT=' "$f") | fails: ${fails:-none}"
done
