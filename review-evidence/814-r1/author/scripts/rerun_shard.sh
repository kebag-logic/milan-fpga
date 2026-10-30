#!/usr/bin/env bash
# rerun_shard.sh <k> <cpus>: start shard <k> of the 814-a703c sweep again exactly as native-shards.py starts it (same
# clone, spec, unit name and properties), after keeping the previous attempt's results under shard-<k>/attempt-<n>.
set -euo pipefail
k=$1; cpus=$2
out=$VALIDATION_STORAGE/scratch/814-a703c/sweep/shard-$k; clone=$LANES/814-a703c-shard$k
unit=milan-814-a703c-shard$k
! systemctl --user is-active -q "$unit"
n=1; while [ -e "$out/attempt-$n" ]; do n=$((n + 1)); done
mkdir "$out/attempt-$n"; mv "$out/spec" "$out/logs" "$out/attempt-$n/"
head=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['head'])" "$out/spec.json")
[ "$(git -C "$clone" rev-parse HEAD)" = "$head" ]
git -C "$clone" clean -q -fdx -e gptp-processor -e protocol-processor -e third_party/lwSRP -e third_party/tsn-c-stack -e third_party/verilog-axis
[ -z "$(git -C "$clone" status --porcelain --untracked-files=no)" ]
systemd-run --user --unit="$unit" --collect --property=MemoryMax=10G --setenv=HOME=$WORKSPACE_HOME --setenv=MAKEFLAGS=-j4 \
  --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$cpus" /usr/bin/python3 $MANAGEMENT/2026-09-21/run-recorded-gates.py "$out/spec.json"
echo "shard $k attempt $((n + 1)) started on $cpus, previous kept in attempt-$n"
