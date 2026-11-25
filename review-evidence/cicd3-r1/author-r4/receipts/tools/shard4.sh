#!/bin/bash
# shard4.sh TREE TAG CPUS ARGS...: scripts/run_all_suites.sh LOGS ARGS... from r4/wt/TREE as a hosted worker runs it
# (hosted job budgets and MAKEFLAGS, no ccache: the runner has none), pinned to CPUS. Records start/end, every log's
# birth and modification time (per-suite span), time and counters. Output: r4/shards/TAG/
set -u
T=$1; G=$2; C=$3; shift 3
W=/data-2/milan/tmp/cicd-a839/r4/wt/$T
O=/data-2/milan/tmp/cicd-a839/r4/shards/$G
. /data-2/milan/tmp/cicd-a839/r4/bin/env.sh
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
find "$O/logs" -maxdepth 1 -type f -name '*.log' -printf '%P\n' | while read -r f; do echo "$(stat -c '%W %Y' "$O/logs/$f") $f"; done | sort -n > "$O/spans"
echo "$G: $(head -1 "$O/time") $(tail -1 "$O/time")"
