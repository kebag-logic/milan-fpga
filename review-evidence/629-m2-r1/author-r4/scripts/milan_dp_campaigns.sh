#!/bin/bash
# milan_dp's three explicit mutation campaigns, outside the sweep's deadline,
# under GNU make 4.3 with the pinned Verilator 5.050 first on PATH. Run after
# the sweep's milan_dp (shard 4): they rebuild the same obj_* legs.
set -u
R=$VALIDATION_STORAGE/629-a512
export PATH=$R/make43/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd $LANES/629-m2-impl || exit 2
echo "head $(git rev-parse HEAD); $(make --version | head -1); $(verilator --version)"
for t in crflic-mutants gsi-mutants gmstep-mutants; do
  echo "$t start $(date -Is)"
  make -C tb/verilator/milan_dp "$t" > "$R/logs/milan_dp_$t.log" 2>&1
  echo "$t rc=$? end $(date -Is)"
done
