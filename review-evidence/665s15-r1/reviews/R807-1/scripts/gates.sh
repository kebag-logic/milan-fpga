#!/bin/bash
# The focused gates at a clean clone, each with its own log and rc; writes ALL.done last.
# usage: gates.sh CLONE OUTDIR BASE_SHA
set -u
C=$1 O=$2 BASE=$3
. "$(dirname "$0")/env.sh"
mkdir -p "$O"; cd "$C" || exit 2
g() { local n=$1; shift; "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc"; }
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l)" > "$O/head.txt"
g builder32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/shape32"
g tree_after_builder32 git status --porcelain --untracked-files=all
g builder32_write_rtl python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/shape32b" --write-rtl
g test_builder_subset python3 sw/builder/test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged
g py_idiom python3 scripts/check_py_idiom.py
g soc_options python3 sw/builder/test_soc_options.py
g gen_mailbox_check python3 sw/mailbox/gen_mailbox.py --check --crosscheck
g gen_mailbox_selftest python3 sw/mailbox/gen_mailbox.py --selftest
g gen_mailbox_shape python3 sw/mailbox/gen_mailbox.py --variant-interfaces 2 --variant-shape configs/endstation_ax7101_32x32.yaml --out "$O/mbx32"
g ctrl_memory python3 sw/litex/test_ctrl_memory.py
g harness_selftest python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
g nvm_target_32 python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir "$O/nvm-target-32x32"
g docs_check python3 scripts/docs_check.py
g record_space python3 scripts/check_nvm_record_space.py
g baremetal python3 scripts/check_baremetal_only.py --check
g diff_check git diff --check "$BASE" HEAD
g tree_after git status --porcelain --untracked-files=all
touch "$O/ALL.done"
