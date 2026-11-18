#!/bin/bash
# Run a command detached in a directory, writing <log> and <log>.rc when it ends.
# usage: bg.sh <dir> <log> <command...>
dir=$1; log=$2; shift 2
rm -f "$log" "$log.rc"
(
  cd "$dir" || exit 99
  echo "HEAD $(git rev-parse HEAD) start $(date +%T) cmd: $*"
  "$@"
  rc=$?
  echo "END rc=$rc $(date +%T)"
  echo $rc > "$log.rc"
) > "$log" 2>&1 < /dev/null &
disown
echo "started $log pid $!"
