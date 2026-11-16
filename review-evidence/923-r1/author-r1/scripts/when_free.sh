#!/bin/bash
# when_free.sh NAME MEM DIR -- CMD...: wait (in the foreground, at most WAIT_S seconds, default 540) for a free CPU
# range from cpu_ranges.py pick, then start CMD as unit NAME on it (unit.sh). Exit 1 if none freed in time.
set -u
NAME=$1 MEM=$2 DIR=$3; shift 3
[ "$1" = "--" ] && shift
end=$(( $(date +%s) + ${WAIT_S:-540} ))
while [ "$(date +%s)" -lt "$end" ]; do
    R=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick 2>/dev/null)
    if [ -n "$R" ]; then
        echo "$(date +%T) $NAME on $R"
        exec $MANAGEMENT/2026-09-23/923-a789/round1/scripts/unit.sh "$NAME" "$R" "$MEM" "$DIR" -- "$@"
    fi
    sleep 20
done
echo "$(date +%T) no free range for $NAME"; exit 1
