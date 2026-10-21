#!/usr/bin/env bash
# Round-2 gate driver: every runnable step of .github/workflows/docs.yml and
# rtl-fast.yml, one log and one rc per command, no pipes.
# usage: gates.sh <tree> <logdir> <section>...
set -u
tree=$1; out=$2; shift 2
S=<scratch>
export TMPDIR=$S/r2/tmp
export PATH=$S/venv312/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$S/sdk/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out"
cd "$tree" || exit 2
tsv=$out/rc.tsv
g() {  # g <name> <command...>
  local name=$1; shift
  local t0; t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%ss\t%s\n' "$name" "$rc" "$(( $(date +%s) - t0 ))" "$*" >> "$tsv"
  echo "$name rc=$rc"
}
gm() {  # wavedrom and behave live in the second interpreter
  local name=$1; shift
  PATH=<tools>/md-venv-40cdefe08ebd/bin:$PATH g "$name" "$@"
}
for section in "$@"; do
case $section in
ident)
  { date -u +%FT%TZ; git rev-parse HEAD; git status --short; git submodule status;
    python3 --version; verilator --version; yosys -V; sv2v --version; } > "$out/identity.txt" 2>&1 ;;
docs0)
  g d0-04-gen_hdl_reference-selftest python3 scripts/gen_hdl_reference.py --selftest
  rm -rf "$S/r2/hdlref"
  g d0-04-gen_hdl_reference-build python3 scripts/gen_hdl_reference.py --output "$S/r2/hdlref"
  g d0-12-docs_check python3 scripts/docs_check.py
  g d0-13-check_em_dash python3 scripts/check_em_dash.py --base e26f1816e456dc8027924bc2e5d327a8aa6e46db
  g d0-14-check_doc_style python3 scripts/check_doc_style.py
  g d0-14-check_doc_style-selftest python3 scripts/check_doc_style.py --selftest
  g d0-14-check_gptp_docs python3 scripts/check_gptp_docs.py
  g d0-14-check_gptp_docs-selftest python3 scripts/check_gptp_docs.py --selftest
  g d0-15-doc_map-check python3 docs/DOC_MAP.gen.py --check
  g d0-15-doc_map-selftest python3 docs/DOC_MAP.gen.py --selftest
  g d0-15-timesync_chain-check python3 docs/diagrams/timesync_chain.gen.py --check
  g d0-15-timesync_chain-selftest python3 docs/diagrams/timesync_chain.gen.py --selftest
  g d0-16-check_solution_docs python3 scripts/check_solution_docs.py
  g d0-16-check_solution_docs-selftest python3 scripts/check_solution_docs.py --selftest
  g d0-17-submodule_boundaries-check python3 docs/diagrams/submodule_boundaries.gen.py --check
  g d0-17-submodule_boundaries-selftest python3 docs/diagrams/submodule_boundaries.gen.py --selftest
  g d0-17-check_submodule_docs python3 scripts/check_submodule_docs.py
  g d0-17-check_submodule_docs-selftest python3 scripts/check_submodule_docs.py --selftest
  gm d0-18-gen_wavedrom-selftest python3 scripts/gen_wavedrom.py --selftest
  gm d0-18-wd_axis_backpressure python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
  gm d0-18-wd_cdc_handshake python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
  gm d0-18-wd_gptp_pdelay python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
  g d0-19-check_diagram_pngs python3 scripts/check_diagram_pngs.py
  g d0-19-check_diagram_pngs-selftest python3 scripts/check_diagram_pngs.py --selftest
  g d0-20-check_feature_status-selftest python3 scripts/check_feature_status.py --self-test
  g d0-21-gen_module_matrix-check python3 docs/traceability/gen_module_matrix.py --check
  g d0-23-check_gptp_docs-with-submodule python3 scripts/check_gptp_docs.py --with-submodule
  g d0-23-gptp-processor-docs make -C gptp-processor docs
  g d0-24-measure_control_flow-selftest python3 scripts/measure_control_flow.py --selftest
  g d0-24-measure_cohesion-selftest python3 scripts/measure_cohesion.py --selftest
  g d0-27-check_baremetal_only python3 scripts/check_baremetal_only.py --check
  g d0-27-check_baremetal_only-selftest python3 scripts/check_baremetal_only.py --selftest
  g d0-29-ci_rv32_sdk-selftest python3 scripts/ci_rv32_sdk_selftest.py
  g d0-29-ci_rv32_sdk-verify python3 scripts/ci_rv32_sdk.py --destination "$S/sdk" --verify-only
  g d0-30-firmware_compiler-selftest python3 sw/builder/test_firmware_compiler.py --selftest
  g d0-30-firmware_compiler-absent python3 sw/builder/test_firmware_compiler.py --absent --audit "$S/r2/rv32-absent.jsonl"
  g d0-31-check_nvm_record_space python3 scripts/check_nvm_record_space.py
  g d0-31-check_nvm_record_space-selftest python3 scripts/check_nvm_record_space.py --self-test
  g d0-32-check_nvm_capture python3 scripts/check_nvm_capture.py
  g d0-33-nvm_firmware-selftest python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
  g d0-34-check_soc_sources python3 scripts/check_soc_sources.py
  g d0-34-check_soc_sources-selftest python3 scripts/check_soc_sources.py --selftest
  g d0-34-iob_pack-selftest python3 sw/litex/iob_pack_selftest.py
  g d0-35-check_rtl_source_lists python3 scripts/check_rtl_source_lists.py
  g d0-35-check_rtl_source_lists-selftest python3 scripts/check_rtl_source_lists.py --selftest
  g d0-36-measure_naming python3 scripts/measure_naming.py --check
  g d0-36-measure_naming-selftest python3 scripts/measure_naming.py --selftest
  g d0-37-check_port_contracts python3 scripts/check_port_contracts.py
  g d0-37-check_port_contracts-selftest python3 scripts/check_port_contracts.py --selftest
  g d0-38-measure_fail_fast python3 scripts/measure_fail_fast.py --check
  g d0-38-measure_fail_fast-selftest python3 scripts/measure_fail_fast.py --selftest
  g d0-39-check_todo_ownership python3 scripts/check_todo_ownership.py
  g d0-39-check_todo_ownership-selftest python3 scripts/check_todo_ownership.py --selftest
  g d0-40-measure_test_evidence python3 scripts/measure_test_evidence.py --check
  g d0-40-measure_test_evidence-selftest python3 scripts/measure_test_evidence.py --selftest
  g d0-41-check_hygiene python3 scripts/check_hygiene.py --check
  g d0-41-check_hygiene-selftest python3 scripts/check_hygiene.py --selftest
  g d0-42-check_sv_idiom python3 scripts/check_sv_idiom.py
  g d0-42-check_sv_idiom-selftest python3 scripts/check_sv_idiom.py --selftest
  g d0-43-check_cpp_idiom python3 scripts/check_cpp_idiom.py
  g d0-43-check_cpp_idiom-selftest python3 scripts/check_cpp_idiom.py --selftest
  g d0-44-check_py_idiom python3 scripts/check_py_idiom.py
  g d0-44-check_py_idiom-selftest python3 scripts/check_py_idiom.py --selftest
  g d0-45-check_sh_idiom python3 scripts/check_sh_idiom.py
  g d0-45-check_sh_idiom-selftest python3 scripts/check_sh_idiom.py --selftest
  g d0-46-check_doc_paths python3 scripts/check_doc_paths.py
  g d0-47-check_archive python3 scripts/check_archive.py
  g d0-47-check_archive-selftest python3 scripts/check_archive.py --selftest
  g d0-48-gen_toc-selftest python3 scripts/gen_toc.py --selftest
  g d0-48-gen_toc-verify-anchors python3 scripts/gen_toc.py --verify-anchors
  g d0-48-gen_toc-check python3 scripts/gen_toc.py --check
  g d0-49-gen_aem_store-selftest python3 avdecc/gen_aem_store.py --self-test
  g d0-50-check_sweep_shape-selftest python3 scripts/check_sweep_shape.py --self-test
  g d0-51-check_deploy_shape-selftest python3 scripts/check_deploy_shape.py --self-test
  g d0-52-check_entity_shape-selftest python3 scripts/check_entity_shape.py --self-test
  ;;
nogit)
  rm -rf "$S/r2/nogit"; mkdir -p "$S/r2/nogit"
  git archive HEAD | tar -x -C "$S/r2/nogit"
  for s in gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    (cd "$s" && git archive HEAD) | tar -x -C "$S/r2/nogit/$s"
  done
  (cd "$S/r2/nogit" && g nogit-docs_check python3 scripts/docs_check.py)
  (cd "$S/r2/nogit" && g nogit-check_feature_status python3 scripts/check_feature_status.py)
  ;;
wire)
  g wire-check_wire_accountability-selftest python3 scripts/check_wire_accountability.py --self-test ;;
docs2)
  g d2-ci_events-check python3 scripts/ci_events.py --check
  g d2-ci_events-selftest python3 scripts/ci_events.py --selftest
  g d2-act_ci-selftest python3 scripts/act_ci.py --selftest
  ;;
builder0)
  g d1-builder-leg0 python3 scripts/ci_builder_legs.py run 0 --receipt "$S/r2/builder-leg-0.json" -- python3 sw/builder/test_builder.py --require-rv32 ;;
builder1)
  g d2-builder-leg1 python3 scripts/ci_builder_legs.py run 1 --receipt "$S/r2/builder-leg-1.json" -- python3 sw/builder/test_builder.py --require-rv32 ;;
fast)
  g rf-ci_scope-selftest python3 scripts/ci_scope.py --selftest
  g rf-lint_rtl python3 scripts/lint_rtl.py --check --self-test --jobs 4
  g rf-pp_srcs python3 scripts/pp_srcs.py --check --selftest
  ;;
hdlref)
  rm -rf "$S/r2/hdlref"
  g d0-04-gen_hdl_reference-build python3 scripts/gen_hdl_reference.py --output "$S/r2/hdlref"
  ;;
bdd)
  (cd tests && gm rf-bdd-behave behave --no-capture -f plain)
  ;;
yosys)
  g rf-yosys-elaborate syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
  g rf-dp_srcs-selftest python3 syn/ooc/dp_srcs.py --selftest
  g rf-ooc_tcl-selftest python3 syn/ooc/ooc_tcl_selftest.py
  g rf-pp_baseline-selftest python3 syn/ooc/pp_baseline.py --selftest
  g rf-pp_baseline_mutants python3 syn/ooc/pp_baseline_mutants.py
  g rf-pp_baseline_reports-selftest python3 syn/ooc/pp_baseline_reports_selftest.py
  g rf-pp_resource_gate-selftest python3 syn/ooc/pp_resource_gate.py --selftest
  g rf-pp_resource_gate_mutants python3 syn/ooc/pp_resource_gate_mutants.py
  g rf-pp_resource_gate-check-baseline python3 syn/ooc/pp_resource_gate.py check-baseline
  g rf-dp_srcs-milan_datapath python3 syn/ooc/dp_srcs.py --top milan_datapath
  g rf-dp_srcs-KL_pp_shadow python3 syn/ooc/dp_srcs.py --top KL_pp_shadow
  g rf-yosys-ooc-selftest python3 syn/yosys/ooc_selftest.py
  g rf-yosys-guard-selftest python3 syn/yosys/guard_selftest.py
  g rf-yosys-cache-selftest python3 syn/yosys/cache_selftest.py
  ;;
census)
  g rf-publication_census python3 sw/mailbox/publication_census.py --check --selftest --jobs 2 ;;
firmware)
  g fw-tally-selftest python3 sw/firmware/gtest/tally_selftest.py
  g fw-rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
  g fw-ctrl-shard0 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
  g fw-ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
  g fw-coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
  g fw-coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
  ;;
fwmut)
  g fw-ctrl-shard1 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
  g fw-ctrl-shard2 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
  g fw-ctrl-shard3 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
  g fw-boundary-without-verilator python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
  g fw-boundary-verilator python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
  ;;
*) echo "unknown section $section"; exit 2 ;;
esac
done
