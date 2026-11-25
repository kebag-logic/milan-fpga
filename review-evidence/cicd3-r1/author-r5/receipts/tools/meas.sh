#!/bin/bash
# meas.sh ARM CPUS JOB...: run each JOB in r5/wt/m<ARM>, as a hosted worker runs a piece (hosted budgets and
# MAKEFLAGS, no compiler cache: the hosted runner has none), pinned to CPUS, one after another.
# JOB forms: mdp:L/T  mclk:L/T  cc:L/T  make:SUITE:TARGET (after `make clean` when TARGET is `clean+X`)
# Output per job: r5/meas/<ARM>-<job tag>/{time,out,start,end}
set -u
A=$1; C=$2; shift 2
W=/data-2/milan/tmp/cicd-a839/r5/wt/m$A
. /data-2/milan/tmp/cicd-a839/r5/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE= CCACHE_DISABLE=1
cd "$W" || exit 99
for job in "$@"; do
  tag=$(printf '%s' "$job" | tr ':/+' '___')
  O=/data-2/milan/tmp/cicd-a839/r5/meas/$A-$tag
  rm -rf "$O"; mkdir -p "$O"
  case "$job" in
    mdp:*) cmd=(python3 scripts/ci_make_cases.py --suite milan_dp --shard "${job#mdp:}" --jobs 2 --receipt "$O/r.json") ;;
    mclk:*) cmd=(bash -c "make -C tb/verilator/milan_dp_mclk mclk-build && exec python3 tb/verilator/milan_dp_mclk/mclk_mutants.py --shard ${job#mclk:} --receipt $O/r.json") ;;
    cc:*) cmd=(env VERILATOR_JOBS=1 python3 tb/verilator/capture_coherence/mutants.py --whole-suite --jobs 4 --shard "${job#cc:}" --receipt "$O/r.json") ;;
    make:*) s=${job#make:}; t=${s#*:}; s=${s%%:*}
            if [ "${t#clean+}" != "$t" ]; then make -s -C "tb/verilator/$s" clean > /dev/null 2>&1; t=${t#clean+}; fi
            cmd=(make -C "tb/verilator/$s" $t) ;;
  esac
  case "$job" in
    mdp:*) make -s -C tb/verilator/milan_dp clean > /dev/null 2>&1 ;;
    mclk:*) make -s -C tb/verilator/milan_dp_mclk clean > /dev/null 2>&1 ;;
  esac
  git rev-parse HEAD > "$O/head"
  date +%s.%N > "$O/start"
  taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" "${cmd[@]}" > "$O/out" 2>&1
  echo "rc=$?" >> "$O/time"
  date +%s.%N > "$O/end"
  echo "$A $job: $(head -1 "$O/time") $(tail -1 "$O/time")" >> /data-2/milan/tmp/cicd-a839/r5/meas/progress
done
