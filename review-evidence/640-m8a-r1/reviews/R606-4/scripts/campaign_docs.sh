#!/bin/bash
# docs.yml's docs-check, wire-accountability and docs-check-no-git commands at the reviewed head,
# in a CPython 3.12.3 interpreter holding only that job's installs. Not run: the apt and pip
# install steps (done once beforehand), `act_ci.py --selftest` (outside this review's remit),
# and the SDK install (a fresh verified install is already at $HOME/br-milan-rv32/host).
# usage: campaign_docs.sh <em-dash base>  (PACKET and CLONE exported)
set -u
. "$PACKET/scripts/env.sh"
export PATH=$S/docs-venv/bin:$PATH
base=$1
R=$PACKET/receipts/docs
mkdir -p "$R"
cd "$CLONE" || exit 9
n=0
step() { n=$((n+1)); name=$(printf '%02d' $n)_$1; shift; "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
step hdlref_selftest python3 scripts/gen_hdl_reference.py --selftest
step hdlref python3 scripts/gen_hdl_reference.py --output "$S/hdl-reference"
step docs_check python3 scripts/docs_check.py
step em_dash python3 scripts/check_em_dash.py --base "$base"
step em_dash_selftest python3 scripts/check_em_dash.py --selftest
step doc_style python3 scripts/check_doc_style.py
step doc_style_selftest python3 scripts/check_doc_style.py --selftest
step gptp_docs python3 scripts/check_gptp_docs.py
step gptp_docs_selftest python3 scripts/check_gptp_docs.py --selftest
step doc_map python3 docs/DOC_MAP.gen.py --check
step doc_map_selftest python3 docs/DOC_MAP.gen.py --selftest
step timesync python3 docs/diagrams/timesync_chain.gen.py --check
step timesync_selftest python3 docs/diagrams/timesync_chain.gen.py --selftest
step solution_docs python3 scripts/check_solution_docs.py
step solution_docs_selftest python3 scripts/check_solution_docs.py --selftest
step submodule_boundaries python3 docs/diagrams/submodule_boundaries.gen.py --check
step submodule_boundaries_selftest python3 docs/diagrams/submodule_boundaries.gen.py --selftest
step submodule_docs python3 scripts/check_submodule_docs.py
step submodule_docs_selftest python3 scripts/check_submodule_docs.py --selftest
step wavedrom_selftest python3 scripts/gen_wavedrom.py --selftest
step wd_axis python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
step wd_cdc python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
step wd_pdelay python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
step diagram_pngs python3 scripts/check_diagram_pngs.py
step diagram_pngs_selftest python3 scripts/check_diagram_pngs.py --selftest
step feature_status_selftest python3 scripts/check_feature_status.py --self-test
step module_matrix python3 docs/traceability/gen_module_matrix.py --check
step gptp_docs_submodule python3 scripts/check_gptp_docs.py --with-submodule
step gptp_make_docs make -C gptp-processor docs
step control_flow_selftest python3 scripts/measure_control_flow.py --selftest
step cohesion_selftest python3 scripts/measure_cohesion.py --selftest
step baremetal_only python3 scripts/check_baremetal_only.py --check
step baremetal_only_selftest python3 scripts/check_baremetal_only.py --selftest
step rv32_sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
step rv32_sdk_verify python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host" --verify-only
step fw_compiler_selftest python3 sw/builder/test_firmware_compiler.py --selftest
step fw_compiler_absent python3 sw/builder/test_firmware_compiler.py --absent --audit "$S/rv32-absent.jsonl"
step test_builder_rv32 python3 sw/builder/test_builder.py --require-rv32
step nvm_record_space python3 scripts/check_nvm_record_space.py
step nvm_record_space_selftest python3 scripts/check_nvm_record_space.py --self-test
step nvm_capture python3 scripts/check_nvm_capture.py
step nvm_firmware_selftest python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
step soc_sources python3 scripts/check_soc_sources.py
step soc_sources_selftest python3 scripts/check_soc_sources.py --selftest
step iob_pack_selftest python3 sw/litex/iob_pack_selftest.py
step rtl_source_lists python3 scripts/check_rtl_source_lists.py
step rtl_source_lists_selftest python3 scripts/check_rtl_source_lists.py --selftest
step naming python3 scripts/measure_naming.py --check
step naming_selftest python3 scripts/measure_naming.py --selftest
step port_contracts python3 scripts/check_port_contracts.py
step port_contracts_selftest python3 scripts/check_port_contracts.py --selftest
step fail_fast python3 scripts/measure_fail_fast.py --check
step fail_fast_selftest python3 scripts/measure_fail_fast.py --selftest
step todo python3 scripts/check_todo_ownership.py
step todo_selftest python3 scripts/check_todo_ownership.py --selftest
step test_evidence python3 scripts/measure_test_evidence.py --check
step test_evidence_selftest python3 scripts/measure_test_evidence.py --selftest
step hygiene python3 scripts/check_hygiene.py --check
step hygiene_selftest python3 scripts/check_hygiene.py --selftest
step sv_idiom python3 scripts/check_sv_idiom.py
step sv_idiom_selftest python3 scripts/check_sv_idiom.py --selftest
step cpp_idiom python3 scripts/check_cpp_idiom.py
step cpp_idiom_selftest python3 scripts/check_cpp_idiom.py --selftest
step py_idiom python3 scripts/check_py_idiom.py
step py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
step sh_idiom python3 scripts/check_sh_idiom.py
step sh_idiom_selftest python3 scripts/check_sh_idiom.py --selftest
step ci_events python3 scripts/ci_events.py --check
step ci_events_selftest python3 scripts/ci_events.py --selftest
step doc_paths python3 scripts/check_doc_paths.py
step archive python3 scripts/check_archive.py
step archive_selftest python3 scripts/check_archive.py --selftest
step toc_selftest python3 scripts/gen_toc.py --selftest
step toc_anchors python3 scripts/gen_toc.py --verify-anchors
step toc_check python3 scripts/gen_toc.py --check
step aem_store_selftest python3 avdecc/gen_aem_store.py --self-test
step sweep_shape_selftest python3 scripts/check_sweep_shape.py --self-test
step deploy_shape_selftest python3 scripts/check_deploy_shape.py --self-test
step entity_shape_selftest python3 scripts/check_entity_shape.py --self-test
step wire_accountability_selftest python3 scripts/check_wire_accountability.py --self-test
step ci_scope_selftest python3 scripts/ci_scope.py --selftest
step ci_scope_split_page sh -c 'echo docs/design/SPLIT_CONTROL_MEMORY.md | python3 scripts/ci_scope.py'
step resource_gate_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
step diff_check git -c core.quotepath=off diff --check "$base" HEAD
# docs-check-no-git: the head's tree without .git (submodule checkouts copied in at their pins)
nogit=$S/nogit
rm -rf "$nogit" && mkdir -p "$nogit"
git archive HEAD | tar -x -C "$nogit"
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  git -C "$sm" archive HEAD | tar -x -C "$nogit/$sm"
done
cd "$nogit" || exit 9
step nogit_docs_check python3 scripts/docs_check.py
step nogit_feature_status python3 scripts/check_feature_status.py
echo done > "$R/DONE"
