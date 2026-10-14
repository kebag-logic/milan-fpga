. /jobs/lib.sh
step "HDL reference (selftest+build)" 'python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py --output "$RUNNER_TEMP/milan-hdl-reference"'
step "pyyaml/markdown/diagram deps present" 'python3 -c "import yaml, wavedrom"; rsvg-convert --version'
step "Link health docs_check" 'python3 scripts/docs_check.py'
step "Added-line em-dash gate (base=merge-base with live dev)" 'base="$(git merge-base HEAD refs/remotes/origin/dev)"; echo base=$base; git cat-file -e "$base^{commit}"; python3 scripts/check_em_dash.py --base "$base"'
step "Concise audience doc gate" 'python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest'
step "Audience diagram no-drift" 'python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest'
step "Product solution source-fact" 'python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest'
step "Verified submodule documentation" 'python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest'
step "HDL timing diagram no-drift" 'python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check'
step "Published diagram PNG" 'python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest'
step "Milan feature-status" 'python3 scripts/check_feature_status.py --self-test'
step "Traceability matrix" 'python3 docs/traceability/gen_module_matrix.py --check'
step "Imported gPTP documentation" 'python3 scripts/check_gptp_docs.py --with-submodule
make -C gptp-processor docs'
step "Code-quality self-tests" 'python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest'
step "sv2v version" 'sv2v --version'
step "Bare-metal scope gate" 'python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest'
rv32
step "Compiler-absent firmware controls" 'python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"'
step "NVM record-space" 'python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test'
step "Capture census/clock" 'python3 scripts/check_nvm_capture.py'
step "Saved-state writer" 'python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test'
step "SoC source-list" 'python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh
python3 sw/litex/iob_pack_selftest.py'
step "RTL source-list drift" 'python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest'
step "Naming ratchet" 'python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest'
step "Port contract" 'python3 scripts/check_port_contracts.py
python3 scripts/check_port_contracts.py --selftest'
step "Fail-fast ratchet" 'python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_fail_fast.py --selftest'
step "TODO ownership" 'python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest'
step "Test-evidence ratchet" 'python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest'
step "Hygiene ratchet" 'python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest'
step "SV idiom" 'python3 scripts/check_sv_idiom.py
python3 scripts/check_sv_idiom.py --selftest'
step "C/C++ idiom" 'python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest'
step "Python idiom" 'python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest'
step "Shell idiom" 'python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest'
step "CI event/SHA contract" 'python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest'
step "Local act runner contract (inside disposable container)" 'python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
trap '"'"'rm -rf "$install_dir"'"'"' EXIT
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$GITHUB_WORKSPACE"'
step "Doc cited-path" 'python3 scripts/check_doc_paths.py'
step "Archive integrity" 'python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest'
step "Per-page contents" 'python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check'
step "AEM store generator" 'python3 avdecc/gen_aem_store.py --self-test'
step "Sweep/build shape" 'python3 scripts/check_sweep_shape.py --self-test'
step "Deploy shape" 'python3 scripts/check_deploy_shape.py --self-test'
step "Entity shape gate" 'python3 scripts/check_entity_shape.py --self-test'
