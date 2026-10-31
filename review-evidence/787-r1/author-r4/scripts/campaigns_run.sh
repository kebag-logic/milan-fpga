#!/usr/bin/env bash
# #787 round 4, the targeted re-measure: the campaigns whose inputs the merge of dev 02ca829a changed, one at a time
# in a clean clone at <rev>. This lane's pp_shadow [RB] and its six reboot arms (dev changed milan_datapath.sv,
# KL_gptp_shadow.sv and the gPTP pin), the LiteX simulation aggregate and the MAC transmit-chain model check at both
# levels (dev changed milan_soc.py), and #70's dynmap-mutants campaign (its three arms copy the processor, now this
# lane's pin, and every arm plants into the merged milan_datapath.sv), and #70's service-budget suite (its capture
# SoC reads the merged milan_soc.py). The builder gate bites and #817's constraint tests run in the builder bank.
# usage: campaigns_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/787-a700e; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export MILAN_LITEX_PYTHON=$LITEX_PYTHON VERILATOR_JOBS=4
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
git rev-parse HEAD > "$O/head.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run pp_shadow_rb make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--reboot-only BUILD_DIR=$X/obj-camp-rb
run pp_shadow_reboot_mutant make -C tb/verilator/pp_shadow reboot-mutant
run litex_sims bash scripts/run_litex_sims.sh "$O/litex-sims"
run mac_tx_model_check_litex "$LITEX_PYTHON" sw/litex/gen_mac_tx_model.py --check
run mac_tx_model_check_plain python3 sw/litex/gen_mac_tx_model.py --check
run dynmap_mutants make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4
# #70's service-budget record: its LiteX capture SoC reads the merged milan_soc.py; judged as the sweep judges it
run fw_service_budget timeout 1800 make -C tb/verilator/fw_service_budget
run fw_service_budget_verdict python3 scripts/suite_tally.py --verdict "$O/fw_service_budget.log"
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo CAMPAIGNS-DONE >> "$O/table.txt"
