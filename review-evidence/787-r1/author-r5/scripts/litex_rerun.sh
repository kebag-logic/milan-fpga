#!/usr/bin/env bash
# #787 round 5: the LiteX simulation aggregate again, unchanged (default LITEX_SIM_TIMEOUT 900 s a member), in the
# campaigns clone at <rev>, after the first run's test_soc_timing_cuts reached the 900 s wall limit on this unit's
# 16 oversubscribed CPUs. Only scheduling differs: the lane's other jobs run reniced to +10 (renice_others.sh).
# usage: litex_rerun.sh <rev> <name>
set -u
rev=$1; name=$2; X=$VALIDATION_STORAGE/787-a700f; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$rev^{commit}")" ] || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export MILAN_LITEX_PYTHON=$LITEX_PYTHON
s=$(date +%s); bash scripts/run_litex_sims.sh "$O/$name" > "$O/$name.log" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s $name: bash scripts/run_litex_sims.sh <out>/$name (nice $(nice))" >> "$O/table-litex-rerun.txt"
git status --porcelain --untracked-files=no > "$O/clone-status-after-$name.txt"
