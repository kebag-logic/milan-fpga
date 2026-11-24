#!/bin/bash
# absuite.sh VARIANT SUITE CPUS: run one suite (or one CI piece NAME__K) in tree/VARIANT pinned to CPUS,
# with the hosted runner's 4-CPU job budgets, under perf stat (cache/branch events) and /usr/bin/time.
# VARIANT base = tree as committed; o2/o3 = OPT_FAST/OPT_GLOBAL forced through MAKEFLAGS; other = tree as edited.
set -u
V=$1; S=$2; C=$3
T=/data-2/milan/tmp/cicd-a839/tree/$V; [ -d /data-2/milan/tmp/cicd-a839/wt/$V ] && [ "${USE_WT:-0}" = 1 ] && T=/data-2/milan/tmp/cicd-a839/wt/$V
O=/data-2/milan/tmp/cicd-a839/runs/ab/$V/$S
. /data-2/milan/tmp/cicd-a839/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
case "$V" in
  o2) export MAKEFLAGS='-j1 --no-print-directory -- OPT_FAST=-O2 OPT_GLOBAL=-O2' ;;
  o3) export MAKEFLAGS='-j1 --no-print-directory -- OPT_FAST=-O3 OPT_GLOBAL=-O3' ;;
  *)  export MAKEFLAGS='-j1 --no-print-directory' ;;
esac
rm -rf "$O"; mkdir -p "$O"
cd "$T" || exit 99
if [[ "$S" == *__* ]]; then
  cmd=(python3 scripts/ci_suite_pieces.py run "$S" --receipts "$O/cases")
else
  cmd=(make -C "tb/verilator/$S")
fi
echo "${cmd[*]}  MAKEFLAGS=$MAKEFLAGS cpus=$C" > "$O/cmd"
EV=task-clock,cycles:u,instructions:u,cache-references:u,cache-misses:u,L1-dcache-loads:u,L1-dcache-load-misses:u,branches:u,branch-misses:u,L1-icache-load-misses:u
start=$(date +%s.%N)
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys %M maxrssKB" -o "$O/time" \
  perf stat -x, -o "$O/perf" -e "$EV" -- "${cmd[@]}" > "$O/log" 2>&1
rc=$?
echo "rc=$rc wall=$(echo "$(date +%s.%N) - $start" | bc)" >> "$O/time"
python3 scripts/suite_tally.py --verdict "$O/log" > "$O/verdict" 2>&1; echo "verdict_rc=$?" >> "$O/verdict"
echo "$V $S rc=$rc $(head -1 "$O/time")"
