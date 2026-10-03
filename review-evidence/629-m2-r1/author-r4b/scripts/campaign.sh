#!/bin/bash
# campaign.sh <make-target> [VAR=value ...]: one of milan_dp's explicit
# mutation campaigns, its documented command (make -C tb/verilator/milan_dp
# <target>), under GNU make 4.3 with the pinned Verilator 5.050 first on PATH.
# Run after the replayed shard 4: they rebuild the same clean obj_* legs.
set -u
R=$VALIDATION_STORAGE/629-a517
t=$1; shift
export PATH=$R/make43/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd $LANES/629-m2-impl || exit 2
mkdir -p "$R/campaigns"
log=$R/campaigns/milan_dp_$t.log
{
  echo "head $(git rev-parse HEAD); $(make --version | head -1); $(verilator --version); env: $*"
  echo "$t start $(date -Is)"
} > "$log"
env "$@" make -C tb/verilator/milan_dp "$t" >> "$log" 2>&1
rc=$?
echo "$t rc=$rc end $(date -Is)" >> "$log"
echo "$rc" > "$R/campaigns/milan_dp_$t.rc"
exit $rc
