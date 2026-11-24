#!/bin/bash
# shard.sh TREE SHARD CPUS: run the hosted shard SHARD/19 exactly as rtl.yml does (run_all_suites.sh
# --ci-pieces, the hosted job budgets and MAKEFLAGS), pinned to CPUS, from worktree wt/TREE.
# Output: runs/shards/TREE-SHARD/{logs/,out,time,perf}
set -u
T=$1; S=$2; C=$3
W=/data-2/milan/tmp/cicd-a839/wt/$T
O=/data-2/milan/tmp/cicd-a839/runs/shards/$T-$S
. /data-2/milan/tmp/cicd-a839/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory'
export CCACHE_DIR=/data-2/milan/tmp/cicd-a839/ccache-$T-$S; case "$T" in *n) export OBJCACHE= ;; b*) export OBJCACHE= ;; esac
rm -rf "$O" "$CCACHE_DIR"; mkdir -p "$O"
cd "$W" || exit 99
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" \
  perf stat -x, -o "$O/perf" -e task-clock,cycles:u,instructions:u -- \
  scripts/run_all_suites.sh "$O/logs" --ci-pieces --shard "$S/19" > "$O/out" 2>&1
echo "rc=$?" >> "$O/time"
command -v ccache > /dev/null && ccache -s > "$O/ccache-stats" 2>&1
echo "$T shard $S: $(head -1 "$O/time") $(tail -1 "$O/time")"
