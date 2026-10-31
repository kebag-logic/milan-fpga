#!/usr/bin/env bash
# #814 round 4: scripts/run_litex_sims.sh --selftest, then the full aggregate, at <rev> in a clean clone, on the
# bench LiteX interpreter, with the pinned Verilator on PATH (env.sh) so its comparison member runs.
# usage: litex_sims_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/814-a703d; C=$X/clone-litex-${rev:0:8}; O=$X/r/litex-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
source "$D/env.sh"
export MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
cd "$C" || exit 2
s=$(date +%s)
bash scripts/run_litex_sims.sh --selftest > "$O/selftest.log" 2>&1
echo "$? $(( $(date +%s) - s ))s run_litex_sims.sh --selftest" > "$O/selftest.rc"
s=$(date +%s)
bash scripts/run_litex_sims.sh "$O/aggregate" > "$O/aggregate.log" 2>&1
echo "$? $(( $(date +%s) - s ))s run_litex_sims.sh <out>" > "$O/aggregate.rc"
git status --short --ignored > "$O/clone-status-after.txt"
