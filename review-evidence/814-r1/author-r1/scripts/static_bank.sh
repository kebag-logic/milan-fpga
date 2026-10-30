#!/usr/bin/env bash
# #814: the static and pin-record gates, one at a time in a clean clone at <rev> (the #780 and #799 pin checks, the
# lint, xvlog, the four idiom, source-list, port, measurement and builder gates the consumer banks ran). xvlog is a
# Vivado tool, so it alone runs under the exclusive Vivado lock.
# usage: static_bank.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/814-a703; C=$X/clone-static-${rev:0:8}; O=$X/r/static-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH
git rev-parse HEAD > "$O/head.txt"; git submodule status > "$O/submodules.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run rom_digests_record bash syn/yosys/ooc.sh --record-rom-digests
run rom_digests_diff git diff --exit-code syn/yosys/rom_digests.tsv
run boundaries_check python3 docs/diagrams/submodule_boundaries.gen.py --check
run timesync_check python3 docs/diagrams/timesync_chain.gen.py --check
run submodule_docs python3 scripts/check_submodule_docs.py
run gptp_docs python3 scripts/check_gptp_docs.py --with-submodule
run port_contracts python3 scripts/check_port_contracts.py
run naming python3 scripts/measure_naming.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run integrator_params python3 protocol-processor/scripts/check-integrator-params.py
run lint python3 scripts/lint_rtl.py --check
run lint_selftest python3 scripts/lint_rtl.py --check --self-test
run xvlog flock -x $VIVADO_LOCK python3 scripts/xvlog_gate.py --check
run sv_idiom python3 scripts/check_sv_idiom.py
run sh_idiom python3 scripts/check_sh_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run cpp_idiom_selftest python3 scripts/check_cpp_idiom.py --selftest
run py_idiom python3 scripts/check_py_idiom.py
run py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
run rtl_source_lists python3 scripts/check_rtl_source_lists.py
run rtl_source_lists_selftest python3 scripts/check_rtl_source_lists.py --selftest
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run builder_bank python3 sw/builder/test_builder.py
run hygiene python3 scripts/check_hygiene.py --check
run fail_fast python3 scripts/measure_fail_fast.py --check
run todo_ownership python3 scripts/check_todo_ownership.py
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
run soc_sources python3 scripts/check_soc_sources.py
run nvm_capture python3 scripts/check_nvm_capture.py
run gptp_docs_plain python3 scripts/check_gptp_docs.py
run feature_status python3 scripts/check_feature_status.py
run docs_check python3 scripts/docs_check.py
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo STATIC-DONE >> "$O/table.txt"
