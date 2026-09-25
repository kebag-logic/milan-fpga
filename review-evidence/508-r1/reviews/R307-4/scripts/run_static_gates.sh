#!/bin/bash
# Run the repository's static gates that read files the composition touches,
# against a candidate clone, one log per command plus a summary table.
# Usage: run_static_gates.sh <clone> <receipt-dir> <python-venv-bin-dir> <verilator-dir>
# Excluded on purpose (manager duties or outside the review's allowance):
# the builder (test_builder.py), the RV32 SDK install and compiler controls,
# the local act runner self-test, the gPTP donor docs make target.
set -u
CLONE=$1; OUT=$2; VENV=$3; VDIR=$4
mkdir -p "$OUT"
export PATH="$VENV:$VDIR:$PATH"
cd "$CLONE" || exit 2
SUMMARY="$OUT/SUMMARY.tsv"
printf 'n\trc\tseconds\tcommand\n' > "$SUMMARY"
n=0
run() {
  n=$((n+1))
  local log; log=$(printf '%s/%02d.log' "$OUT" "$n")
  local t0; t0=$(date +%s)
  { echo "\$ $*"; echo "cwd: $PWD"; } > "$log"
  "$@" >> "$log" 2>&1
  local rc=$?
  local dt=$(( $(date +%s) - t0 ))
  echo "rc=$rc" >> "$log"
  printf '%02d\t%s\t%s\t%s\n' "$n" "$rc" "$dt" "$*" >> "$SUMMARY"
}
PY=python3
run $PY scripts/docs_check.py
run $PY scripts/check_em_dash.py --base b74fb11162fba8f019110d9f2c21492300857da2
run $PY scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
run $PY scripts/check_doc_style.py
run $PY scripts/check_doc_style.py --selftest
run $PY scripts/check_gptp_docs.py
run $PY scripts/check_gptp_docs.py --selftest
run $PY docs/DOC_MAP.gen.py --check
run $PY docs/DOC_MAP.gen.py --selftest
run $PY docs/diagrams/timesync_chain.gen.py --check
run $PY docs/diagrams/timesync_chain.gen.py --selftest
run $PY scripts/check_solution_docs.py
run $PY scripts/check_solution_docs.py --selftest
run $PY docs/diagrams/submodule_boundaries.gen.py --check
run $PY docs/diagrams/submodule_boundaries.gen.py --selftest
run $PY scripts/check_submodule_docs.py
run $PY scripts/check_submodule_docs.py --selftest
run $PY scripts/gen_wavedrom.py --selftest
run $PY scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
run $PY scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
run $PY scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
run $PY scripts/check_diagram_pngs.py
run $PY scripts/check_diagram_pngs.py --selftest
run $PY scripts/check_feature_status.py --self-test
run $PY docs/traceability/gen_module_matrix.py --check
run $PY scripts/check_gptp_docs.py --with-submodule
run $PY scripts/measure_control_flow.py --selftest
run $PY scripts/measure_cohesion.py --selftest
run $PY scripts/check_baremetal_only.py --check
run $PY scripts/check_baremetal_only.py --selftest
run $PY scripts/check_nvm_record_space.py
run $PY scripts/check_nvm_record_space.py --self-test
run $PY sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run $PY scripts/check_soc_sources.py
run $PY scripts/check_soc_sources.py --selftest
run $PY sw/litex/iob_pack_selftest.py
run $PY scripts/check_rtl_source_lists.py
run $PY scripts/check_rtl_source_lists.py --selftest
run $PY scripts/measure_naming.py --check
run $PY scripts/measure_naming.py --selftest
run $PY scripts/check_port_contracts.py
run $PY scripts/check_port_contracts.py --selftest
run $PY scripts/measure_fail_fast.py --check
run $PY scripts/measure_fail_fast.py --selftest
run $PY scripts/check_todo_ownership.py
run $PY scripts/check_todo_ownership.py --selftest
run $PY scripts/measure_test_evidence.py --check
run $PY scripts/measure_test_evidence.py --selftest
run $PY scripts/check_hygiene.py --check
run $PY scripts/check_hygiene.py --selftest
run $PY scripts/check_sv_idiom.py
run $PY scripts/check_sv_idiom.py --selftest
run $PY scripts/check_cpp_idiom.py
run $PY scripts/check_cpp_idiom.py --selftest
run $PY scripts/check_py_idiom.py
run $PY scripts/check_py_idiom.py --selftest
run $PY scripts/check_sh_idiom.py
run $PY scripts/check_sh_idiom.py --selftest
run $PY scripts/ci_events.py --check
run $PY scripts/ci_events.py --selftest
run $PY scripts/check_doc_paths.py
run $PY scripts/check_archive.py
run $PY scripts/check_archive.py --selftest
run $PY scripts/gen_toc.py --selftest
run $PY scripts/gen_toc.py --verify-anchors
run $PY scripts/gen_toc.py --check
run $PY avdecc/gen_aem_store.py --self-test
run $PY scripts/check_sweep_shape.py --self-test
run $PY scripts/check_deploy_shape.py --self-test
run $PY scripts/check_entity_shape.py --self-test
run $PY scripts/check_wire_accountability.py --self-test
run $PY scripts/ci_scope.py --selftest
run $PY scripts/pp_srcs.py --check --selftest
run $PY scripts/lint_rtl.py --check --self-test
run $PY scripts/suite_shards.py --selftest
run $PY scripts/gen_hdl_reference.py --selftest
run $PY scripts/gen_hdl_reference.py --output "$OUT/../../scratch/hdl-reference"
run $PY syn/ooc/dp_srcs.py --selftest
run $PY syn/ooc/dp_srcs.py --top milan_datapath
run $PY syn/ooc/dp_srcs.py --top KL_pp_shadow
run git diff --check b74fb11162fba8f019110d9f2c21492300857da2 HEAD
run git diff --check 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38 HEAD
echo "done: $n commands; failures: $(awk -F'\t' 'NR>1 && $2!=0' "$SUMMARY" | wc -l)"
