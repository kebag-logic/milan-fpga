#!/bin/bash
# piece_smoke.sh ARM CPUS PIECE...: run each piece as the sweep's --ci-pieces arm does, in r5/wt/m<ARM>,
# hosted budgets, no compiler cache, pinned to CPUS; logs and receipts in r5/smoke/<ARM>/, times in progress
set -u
A=$1; C=$2; shift 2
W=/data-2/milan/tmp/cicd-a839/r5/wt/m$A; O=/data-2/milan/tmp/cicd-a839/r5/smoke/$A
. /data-2/milan/tmp/cicd-a839/r5/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE= CCACHE_DISABLE=1
mkdir -p "$O/cases"; cd "$W" || exit 99
for p in "$@"; do
  make -s -C "tb/verilator/${p%__*}" clean > /dev/null 2>&1
  s=$(date +%s.%N)
  taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$p.time" \
    python3 scripts/ci_suite_pieces.py run "$p" --receipts "$O/cases" > "$O/$p.log" 2>&1
  echo "rc=$?" >> "$O/$p.time"
  echo "$A $p: $(head -1 "$O/$p.time") $(tail -1 "$O/$p.time")" >> "$O/progress"
done
