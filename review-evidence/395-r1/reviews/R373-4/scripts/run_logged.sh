#!/usr/bin/env bash
# Usage: run_logged.sh <log> <workdir> <command...>
# Runs one command, recording start/end UTC, wall seconds and exit code in the log.
set -u
log=$1; shift
dir=$1; shift
cd "$dir" || exit 97
start=$(date +%s.%N)
{
  echo "# cwd: $dir"
  echo "# head: $(git rev-parse HEAD 2>/dev/null)"
  echo "# command: $*"
  echo "# start: $(date -u +%FT%TZ)"
} > "$log"
"$@" >> "$log" 2>&1
rc=$?
end=$(date +%s.%N)
{
  echo "# end: $(date -u +%FT%TZ)"
  echo "# wall_seconds: $(echo "$end - $start" | bc)"
  echo "# rc: $rc"
} >> "$log"
exit "$rc"
