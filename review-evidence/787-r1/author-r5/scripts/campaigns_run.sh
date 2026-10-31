#!/usr/bin/env bash
# #787 round 5, the targeted re-measure: the campaigns whose inputs the merge of PR #826 (#814) changed, one at a time
# in a clean clone at <rev>. #814 changes sw/litex/milan_soc.py and adds sw/litex/test_soc_timing_cuts.py to the
# LiteX simulation inventory, so: the LiteX simulation aggregate (the new simulation among them), the new simulation
# run directly as its docstring says, the MAC transmit-chain model check at both levels (its generator reads the
# merged milan_soc.py, and pp_shadow [RB] grades against the committed model), and #70's service-budget suite (its
# capture SoC reads the merged milan_soc.py). The builder gate bites run in the builder bank.
# usage: campaigns_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/787-a700f; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export MILAN_LITEX_PYTHON=$LITEX_PYTHON VERILATOR_JOBS=4
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
git rev-parse HEAD > "$O/head.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run litex_sims bash scripts/run_litex_sims.sh "$O/litex-sims"
run soc_timing_cuts_direct bash -c 'cd sw/litex && "$LITEX_PYTHON" test_soc_timing_cuts.py'
run mac_tx_model_check_litex "$LITEX_PYTHON" sw/litex/gen_mac_tx_model.py --check
run mac_tx_model_check_plain python3 sw/litex/gen_mac_tx_model.py --check
# #70's service-budget record: its LiteX capture SoC reads the merged milan_soc.py; judged as the sweep judges it
run fw_service_budget timeout 1800 make -C tb/verilator/fw_service_budget
run fw_service_budget_verdict python3 scripts/suite_tally.py --verdict "$O/fw_service_budget.log"
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo CAMPAIGNS-DONE >> "$O/table.txt"
