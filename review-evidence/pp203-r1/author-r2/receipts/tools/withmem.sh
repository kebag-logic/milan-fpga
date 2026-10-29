#!/usr/bin/env bash
# run a command in the foreground while sampling this unit's memory.current every 5 s into $MEMLOG
set -u
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
( while true; do echo "$(date +%s) $(cat $CG/memory.current)" >> "$MEMLOG"; sleep 5; done ) &
S=$!
"$@"
rc=$?
kill $S 2>/dev/null
echo "rc=$rc"
exit $rc
