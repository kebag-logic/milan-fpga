#!/bin/bash
# mutrun2.sh TAG CACHE CPUS RUN... : for each driver of DRIVERS in turn, every RUN (TREE:LABEL) in order, through
# ccache with CCACHE_DIR=CACHE (emptied once, at the start), pinned to CPUS, under the hosted job budgets.
# Output: r3/mut2/TAG/<TREE>-<LABEL>/<suite>-<driver>.{log,time,stats}, one summary line each in r3/mut2/TAG/summary
set -u
G=$1; CACHE=$2; C=$3; shift 3
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=ccache CCACHE_DIR=$CACHE CCACHE_MAXSIZE=20G
DRIVERS=(
  "rx_filter binding_mutant.py"
  "tcam mutants.py"
  "mmcm_servo slew_mutants.py"
  "avtp_rxmon depkt_mutants.py"
  "crf_rx mutants.py"
)
RUNS=("$@")
rm -rf "$CACHE"; mkdir -p "$CACHE"
for d in "${DRIVERS[@]}"; do
  for tr in "${RUNS[@]}"; do
    T=${tr%%:*}; R=${tr#*:}
    O=/data-2/milan/tmp/cicd-a839/r3/mut2/$G/$T-$R; mkdir -p "$O"
    read -r -a A <<< "$d"; S=${A[0]}; CMD=("${A[@]:1}"); N="$S-${CMD[0]%.py}"
    ccache -z > /dev/null
    ( cd /data-2/milan/tmp/cicd-a839/r3/wt/$T/tb/verilator/$S && \
      taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$N.time" python3 "${CMD[@]}" > "$O/$N.log" 2>&1
      echo "rc=$?" >> "$O/$N.time" )
    ccache --print-stats > "$O/$N.stats" 2>&1
    echo "$T-$R $N $(head -1 "$O/$N.time") $(tail -1 "$O/$N.time") hit=$(awk '$1~/_cache_hit$/{s+=$2} END{print s+0}' "$O/$N.stats") miss=$(awk '$1=="cache_miss"{print $2}' "$O/$N.stats")" >> /data-2/milan/tmp/cicd-a839/r3/mut2/$G/summary
  done
done
