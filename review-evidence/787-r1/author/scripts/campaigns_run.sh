#!/usr/bin/env bash
# #787 round 2: every mutant driver and self-test this lane owns, one at a time in a clean clone at <rev>: the
# reboot_ctrl suite (both legs and its 30 mutants), pp_shadow's [RB] alone and its six arms, the #396 planner
# self-test and its behave feature, the UART smoke self-test, the LiteX simulation aggregate (MilanMAC is built by
# two of its members) and the MAC transmit-chain model check at both levels.
# Then the cheap gates that read Python, for a head that differs from the long banks' head in a driver only.
# usage: campaigns_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/787-a700c; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export MILAN_LITEX_PYTHON=$LITEX_PYTHON VERILATOR_JOBS=4
git rev-parse HEAD > "$O/head.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run reboot_ctrl make -C tb/verilator/reboot_ctrl
run pp_shadow_rb make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--reboot-only BUILD_DIR=$X/obj-camp-rb
run pp_shadow_reboot_mutant make -C tb/verilator/pp_shadow reboot-mutant
run torture_selftest python3 -B tb/tools/torture_campaign.py --self-test
run torture_behave python3 -B -m behave tests/features/torture_campaign_plan.feature
run uart_smoke_selftest python3 scripts/baremetal_uart_smoke.py --self-test
run litex_sims bash scripts/run_litex_sims.sh "$O/litex-sims"
run mac_tx_model_check_litex "$LITEX_PYTHON" sw/litex/gen_mac_tx_model.py --check
run mac_tx_model_check_plain python3 sw/litex/gen_mac_tx_model.py --check
# the gates that read the one file the head changed after the long banks' head (reboot_mutant.py)
run py_idiom python3 scripts/check_py_idiom.py
run py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
run hygiene python3 scripts/check_hygiene.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run todo_ownership python3 scripts/check_todo_ownership.py
run docs_check python3 scripts/docs_check.py
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo CAMPAIGNS-DONE >> "$O/table.txt"
