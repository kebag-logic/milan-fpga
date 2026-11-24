#!/usr/bin/env bash
# docs_gates0.sh <clone> <base>: every run-step of .github/workflows/docs.yml job docs-gates-0, in workflow order, in
# <clone>; python3 is the pinned Markdown/pyslang venv (its bin dir first on PATH). Setup steps CI needs only on a fresh runner (checkout, caches,
# pip/apt installs, artifact upload, gate-receipt recording) are skipped; sv2v is the installed pinned v0.0.12.
# Prints one "STEP <rc> <name>" line per step and exits non-zero if any step failed.
set -u
cd "$1"; base=$2; T=/data-2/milan/tmp/opt-a837-r3b
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$WORKSPACE_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
export RUNNER_TEMP=$T/runner-temp; rm -rf "$RUNNER_TEMP"; mkdir -p "$RUNNER_TEMP"
fail=0
step() { local name=$1; shift; echo "=== $name"; ( set -eo pipefail; eval "$*" ); local rc=$?; echo "STEP $rc $name"; [ $rc -eq 0 ] || fail=1; }
step "Build the validated HDL reference" 'python3 scripts/gen_hdl_reference.py --selftest; python3 scripts/gen_hdl_reference.py --output "$RUNNER_TEMP/milan-hdl-reference"; test -f "$RUNNER_TEMP/milan-hdl-reference/index.html"'
step "Link health, wording, dead-reference and local-info gate" 'python3 scripts/docs_check.py'
step "Added-line em-dash gate" "git cat-file -e '$base^{commit}'; python3 scripts/check_em_dash.py --base $base"
step "Concise audience documentation gate" 'python3 scripts/check_doc_style.py; python3 scripts/check_doc_style.py --selftest; python3 scripts/check_gptp_docs.py; python3 scripts/check_gptp_docs.py --selftest'
step "Audience diagram no-drift gate" 'python3 docs/DOC_MAP.gen.py --check; python3 docs/DOC_MAP.gen.py --selftest; python3 docs/diagrams/timesync_chain.gen.py --check; python3 docs/diagrams/timesync_chain.gen.py --selftest'
step "Product solution source-fact gate" 'python3 scripts/check_solution_docs.py; python3 scripts/check_solution_docs.py --selftest'
step "Verified submodule documentation gate" 'python3 docs/diagrams/submodule_boundaries.gen.py --check; python3 docs/diagrams/submodule_boundaries.gen.py --selftest; python3 scripts/check_submodule_docs.py; python3 scripts/check_submodule_docs.py --selftest'
step "HDL timing diagram no-drift gate" 'python3 scripts/gen_wavedrom.py --selftest; for d in wd_axis_backpressure wd_cdc_handshake wd_gptp_pdelay; do python3 scripts/gen_wavedrom.py docs/diagrams/$d.json --background=white --check; done'
step "Published diagram PNG gate" 'python3 scripts/check_diagram_pngs.py; python3 scripts/check_diagram_pngs.py --selftest'
step "Milan feature-status consistency gate" 'python3 scripts/check_feature_status.py --self-test'
step "Traceability matrix no-drift gate" 'python3 docs/traceability/gen_module_matrix.py --check'
step "Imported gPTP documentation gate" 'python3 scripts/check_gptp_docs.py --with-submodule; make -C gptp-processor docs'
step "Code-quality measurement self-tests" 'python3 scripts/measure_control_flow.py --selftest; python3 scripts/measure_cohesion.py --selftest'
step "Install the pinned sv2v release (version check only)" 'test "$(sv2v --version)" = "sv2v v0.0.12"'
step "Bare-metal scope gate" 'python3 scripts/check_baremetal_only.py --check; python3 scripts/check_baremetal_only.py --selftest'
step "Install and verify the pinned RV32 SDK (installer self-test only)" 'python3 scripts/ci_rv32_sdk_selftest.py'
step "Compiler-absent firmware controls" 'python3 sw/builder/test_firmware_compiler.py --selftest; python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"'
step "NVM record-space gate" 'for s in check_nvm_record_space check_nvm_format_32x32 check_nvm_klj3; do python3 scripts/$s.py; python3 scripts/$s.py --self-test; done'
step "Capture measurement census and clock gate" 'python3 scripts/check_nvm_capture.py'
step "Saved-state writer gate" 'python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test'
step "SoC source-list gate" 'python3 scripts/check_soc_sources.py; python3 scripts/check_soc_sources.py --selftest; command -v tclsh >/dev/null; python3 sw/litex/iob_pack_selftest.py'
step "RTL source-list drift gate" 'python3 scripts/check_rtl_source_lists.py; python3 scripts/check_rtl_source_lists.py --selftest'
step "Boundary-unit naming ratchet" 'python3 scripts/measure_naming.py --check; python3 scripts/measure_naming.py --selftest'
step "Port contract gate" 'python3 scripts/check_port_contracts.py; python3 scripts/check_port_contracts.py --selftest'
step "Fail-fast ratchet" 'python3 scripts/measure_fail_fast.py --check; python3 scripts/measure_fail_fast.py --selftest'
step "TODO ownership gate" 'python3 scripts/check_todo_ownership.py; python3 scripts/check_todo_ownership.py --selftest'
step "Test-evidence ratchet" 'python3 scripts/measure_test_evidence.py --check; python3 scripts/measure_test_evidence.py --selftest'
step "Mechanical hygiene ratchet" 'python3 scripts/check_hygiene.py --check; python3 scripts/check_hygiene.py --selftest'
step "SystemVerilog idiom gate" 'python3 scripts/check_sv_idiom.py; python3 scripts/check_sv_idiom.py --selftest'
step "C and C++ idiom gate" 'python3 scripts/check_cpp_idiom.py; python3 scripts/check_cpp_idiom.py --selftest'
step "Python idiom gate" 'python3 scripts/check_py_idiom.py; python3 scripts/check_py_idiom.py --selftest'
step "Shell idiom gate" 'python3 scripts/check_sh_idiom.py; python3 scripts/check_sh_idiom.py --selftest'
step "Doc cited-path gate" 'python3 scripts/check_doc_paths.py'
step "Archive integrity gate" 'python3 scripts/check_archive.py; python3 scripts/check_archive.py --selftest'
step "Per-page contents gate" 'python3 scripts/gen_toc.py --selftest; python3 scripts/gen_toc.py --verify-anchors; python3 scripts/gen_toc.py --check'
step "Documentation inventory freshness gate" 'python3 scripts/docs_inventory.py --check; python3 scripts/docs_inventory.py --selftest'
step "AEM store generator self-test" 'python3 avdecc/gen_aem_store.py --self-test'
step "Sweep/build shape gate" 'python3 scripts/check_sweep_shape.py --self-test'
step "Deploy shape gate" 'python3 scripts/check_deploy_shape.py --self-test'
step "Entity shape gate" 'python3 scripts/check_entity_shape.py --self-test'
step "Register reference freshness gate" 'python3 scripts/gen_register_reference.py --check; python3 scripts/gen_register_reference.py --selftest; python3 docs/diagrams/memory_map.gen.py --check'
step "CI scheduling and evidence controls" 'python3 scripts/ci_gate_workflows.py --check; for s in ci_gate_workflows ci_case_receipts ci_make_cases ci_maap_cases ci_capture_cases ci_suite_pieces ci_suite_collect ci_fail_fast ci_runtime_evidence ci_install_cache; do python3 scripts/${s}_selftest.py; done; python3 scripts/generate_ci_evidence_pins.py --check; python3 scripts/ci_workflow_plan_selftest.py; python3 scripts/ci_manifest_selftest.py'
echo "porcelain-after $(git status --porcelain --untracked-files=all | wc -l)"
echo "ALL-STEPS rc=$fail"; exit $fail
