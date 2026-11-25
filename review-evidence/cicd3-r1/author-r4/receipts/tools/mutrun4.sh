#!/bin/bash
# mutrun4.sh TAG CPUS RUN... : each driver of DRIVERS in turn, every RUN (TREE:LABEL) in order, through the SHARED
# ccache (CCACHE_DIR untouched); each run's own compile results come from its CCACHE_STATSLOG. Pinned to CPUS,
# hosted job budgets. Output: r4/mut/TAG/<TREE>-<LABEL>/<suite>-<driver>.{log,time,statslog}, a summary line each.
set -u
G=$1; C=$2; shift 2
. /data-2/milan/tmp/cicd-a839/r4/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=ccache
DRIVERS=(
  "tcam mutants.py"
  "rx_filter binding_mutant.py"
  "avtp_rxmon depkt_mutants.py"
  "crf_rx mutants.py"
  "milan_dp split_mutants.py"
)
mkdir -p /data-2/milan/tmp/cicd-a839/r4/mut/$G
for d in "${DRIVERS[@]}"; do
  for tr in "$@"; do
    T=${tr%%:*}; R=${tr#*:}
    O=/data-2/milan/tmp/cicd-a839/r4/mut/$G/$T-$R; mkdir -p "$O"
    read -r -a A <<< "$d"; S=${A[0]}; CMD=("${A[@]:1}"); N="$S-${CMD[0]%.py}"
    rm -f "$O/$N.statslog"
    ( cd /data-2/milan/tmp/cicd-a839/r4/wt/$T/tb/verilator/$S && \
      CCACHE_STATSLOG="$O/$N.statslog" taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$N.time" \
        python3 "${CMD[@]}" > "$O/$N.log" 2>&1
      echo "rc=$?" >> "$O/$N.time" )
    hit=$(grep -cE '^(direct|preprocessed)_cache_hit$' "$O/$N.statslog" 2>/dev/null); miss=$(grep -c '^cache_miss$' "$O/$N.statslog" 2>/dev/null)
    echo "$T-$R $N $(head -1 "$O/$N.time") $(tail -1 "$O/$N.time") hit=$hit miss=$miss" >> /data-2/milan/tmp/cicd-a839/r4/mut/$G/summary
  done
done
echo done >> /data-2/milan/tmp/cicd-a839/r4/mut/$G/summary
