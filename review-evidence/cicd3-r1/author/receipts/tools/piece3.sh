#!/bin/bash
# piece3.sh TREE TAG CPUS SHARD: one milan_dp CI piece through its driver exactly as ci_suite_pieces.py runs it
# (ci_make_cases.py --shard SHARD --jobs 2 --receipt), from r3/wt/TREE with its cases prebuilt, pinned to CPUS (two
# physical cores, a hosted runner's shape), hosted budgets, no ccache. Output: r3/piece/TAG/{log,time,perf,*.json}
set -u
T=$1; G=$2; C=$3; S=$4
O=/data-2/milan/tmp/cicd-a839/r3/piece/$G
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=
rm -rf "$O"; mkdir -p "$O"; cd /data-2/milan/tmp/cicd-a839/r3/wt/$T || exit 99
git rev-parse HEAD > "$O/head"; date +%s.%N > "$O/start"
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" perf stat -x, -o "$O/perf" -e task-clock,cycles:u,instructions:u -- \
  python3 scripts/ci_make_cases.py --suite milan_dp --shard "$S" --jobs 2 --receipt "$O/milan_dp__${S%/*}.json" > "$O/log" 2>&1
echo "rc=$?" >> "$O/time"; date +%s.%N > "$O/end"; echo "$G $(head -1 "$O/time") $(tail -1 "$O/time")"
