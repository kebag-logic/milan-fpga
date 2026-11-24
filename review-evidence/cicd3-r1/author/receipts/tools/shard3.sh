#!/bin/bash
# shard3.sh TREE TAG CPUS ARGS...: run scripts/run_all_suites.sh LOGS ARGS... from r3/wt/TREE exactly as a hosted worker
# does (hosted job budgets and MAKEFLAGS, no ccache: the runner has none), pinned to CPUS. Records the start time, the
# end time, every log's birth time (time to first suite), time and counters.
# Output: r3/shards/TAG/{logs/,out,time,perf,start,end,births}
set -u
T=$1; G=$2; C=$3; shift 3
W=/data-2/milan/tmp/cicd-a839/r3/wt/$T
O=/data-2/milan/tmp/cicd-a839/r3/shards/$G
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=
rm -rf "$O"; mkdir -p "$O"; cd "$W" || exit 99
git rev-parse HEAD > "$O/head"
date +%s.%N > "$O/start"
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" \
  perf stat -x, -o "$O/perf" -e task-clock,cycles:u,instructions:u -- \
  scripts/run_all_suites.sh "$O/logs" "$@" > "$O/out" 2>&1
echo "rc=$?" >> "$O/time"
date +%s.%N > "$O/end"
find "$O/logs" -type f -printf '%P\n' | while read -r f; do echo "$(stat -c %W "$O/logs/$f") $f"; done | sort -n > "$O/births"
echo "$G: $(head -1 "$O/time") $(tail -1 "$O/time")"
