#!/bin/bash
# fbrun.sh TAG CPUS CLONE ARGS...: run ctrl_boundary.py ARGS in CLONE, pinned to CPUS, with the hosted job's
# budgets; output in r6/meas/TAG/{out,time,head}
set -u
T=$1; C=$2; W=$3; shift 3
. /data-2/milan/tmp/cicd-a839/r6/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE= CCACHE_DISABLE=1
O=/data-2/milan/tmp/cicd-a839/r6/meas/$T; mkdir -p "$O"
cd "$W" || exit 99
git rev-parse HEAD > "$O/head"
date +%s.%N > "$O/start"
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" python3 sw/firmware/ctrl/test/ctrl_boundary.py "$@" > "$O/out" 2>&1
echo "rc=$?" >> "$O/time"
date +%s.%N > "$O/end"
echo "$T: $(head -1 "$O/time") $(tail -1 "$O/time")" >> /data-2/milan/tmp/cicd-a839/r6/meas/progress
