#!/bin/sh
# rerun_fixture.sh WORK LOGNAME VAR=VALUE... : re-run an already built
# stream_counters fixture binary under WORK with extra environment, writing
# WORK/LOGNAME, and print rc, failure groups, RESULT and the GAPS start column.
WORK=$1; NAME=$2; shift 2
( cd "$WORK/tb/verilator/milan_dp" && env -u COUNTERS_OMIT_CHECK -u COUNTERS_WINDOW_SHIFT "$@" "$WORK/obj/stream_counters" ) > "$WORK/$NAME" 2>&1
rc=$?
groups=$(grep -h "\[FAIL\]" "$WORK/$NAME" | sed -E 's/.*\[726 ([A-Z_]+)\].*/\1/; s/^ *\[FAIL\].*/other/' | sort | uniq -c | tr -s ' ' | tr '\n' ' ')
res=$(grep -h "RESULT:" "$WORK/$NAME" | tail -1)
starts=$(grep -h "^GAPS," "$WORK/$NAME" | cut -d, -f6 | sort -u | tr '\n' ' ')
echo "$(basename "$WORK") $NAME $* rc=$rc fails=[${groups}] $res gaps_start=[$starts]"
