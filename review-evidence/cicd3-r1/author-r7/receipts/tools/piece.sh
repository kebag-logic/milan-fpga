#!/bin/bash
# piece.sh TREE CPUS SHARD...: in r7/wt/TREE, for each SHARD (L/T): `make clean`, then milan_dp's CI driver as a
# hosted worker runs a piece (ci_suite_pieces.py's command: ci_make_cases.py --suite milan_dp --shard L/T --jobs 2),
# pinned to CPUS, through the shared ccache. Log and receipt in r7/meas/piece-TREE/.
set -u
T=$1; C=$2; shift 2; R=/data-2/milan/tmp/cicd-a839/r7; O=$R/meas/piece-$T
. $R/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=ccache
mkdir -p "$O"; cd "$R/wt/$T" || exit 99
git rev-parse HEAD > "$O/head"
for s in "$@"; do
  g=${s/\//of}
  make -s -C tb/verilator/milan_dp clean > /dev/null 2>&1
  taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$g.time" \
    python3 scripts/ci_make_cases.py --suite milan_dp --shard "$s" --jobs 2 --receipt "$O/$g.json" > "$O/$g.log" 2>&1
  echo "rc=$?" >> "$O/$g.time"
  echo "$T piece $s cpus=$C: $(head -1 "$O/$g.time") $(tail -1 "$O/$g.time") | $(grep '^\[#207\]' "$O/$g.log" | tr '\n' ' ')" >> $R/meas/progress
done
