#!/bin/bash
# frpiece.sh CPUS TREE...: in r8/wt/TREE, follow_ring's two CI pieces (ci_make_cases.py --suite follow_ring
# --shard L/2 --jobs 2, as ci_suite_pieces.py runs them), one after the other on CPUS, after `make clean`.
# Shared ccache. Logs, receipts and times in r8/meas/fr-TREE/.
set -u
C=$1; shift; R=/data-2/milan/tmp/cicd-a839/r8
. $R/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=ccache
for T in "$@"; do
  O=$R/meas/fr-$T; mkdir -p "$O"; cd "$R/wt/$T" || exit 99
  git rev-parse HEAD > "$O/head"
  make -s -C tb/verilator/follow_ring clean > /dev/null 2>&1
  # the two pieces share obj_dir: build each piece's model in turn, as each hosted worker does on its own runner
  for s in 0 1; do
    ( taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$s.time" \
        python3 scripts/ci_make_cases.py --suite follow_ring --shard "$s/2" --jobs 2 --receipt "$O/$s.json" > "$O/$s.log" 2>&1
      echo "rc=$?" >> "$O/$s.time" ) 
  done
  echo "$T $(cat $O/head): leg0 $(tr '\n' ' ' < $O/0.time) leg1 $(tr '\n' ' ' < $O/1.time)" >> $R/meas/progress
done
echo finished >> $R/meas/progress
