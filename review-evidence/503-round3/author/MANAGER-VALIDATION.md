# Manager pre-publication validation

Candidate `ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4`, live base `2d8fd62fd986ea2d6a87d284e144f023034c0944`. All 38 manager commands and the full builder command exited 0. The candidate descends directly from the base; its tree is the candidate merge tree. Both validation checkouts were clean before publication.

The builder explicitly did not run gate 11's existing physical utilization-report arm because its report was absent. All executable builder arms passed. The xvlog ratchet passed with 0 first-party findings and its existing 4 pinned-processor findings.

The complete native suite bar, local workflow replicas and required hosted contexts remain pending. This record is evidence, not review or merge approval.

| Command | Exit |
|---|---|
| `python3 scripts/pp_srcs.py --check --selftest` | 0 |
| `python3 scripts/lint_rtl.py --check --self-test` | 0 |
| `python3 scripts/suite_shards.py --selftest` | 0 |
| `python3 scripts/ci_events.py --check` | 0 |
| `python3 scripts/ci_scope.py --selftest` | 0 |
| `python3 scripts/ci_events.py --selftest` | 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| `python3 scripts/check_feature_status.py` | 0 |
| `python3 scripts/check_submodule_docs.py` | 0 |
| `python3 scripts/check_cpp_idiom.py` | 0 |
| `python3 scripts/check_py_idiom.py` | 0 |
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 scripts/check_doc_style.py --selftest` | 0 |
| `python3 scripts/check_solution_docs.py` | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/check_archive.py` | 0 |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| `python3 scripts/gen_toc.py --check` | 0 |
| `python3 scripts/check_hygiene.py --check` | 0 |
| `python3 scripts/check_todo_ownership.py` | 0 |
| `python3 scripts/check_sv_idiom.py` | 0 |
| `python3 scripts/check_sh_idiom.py` | 0 |
| `python3 scripts/check_rtl_source_lists.py` | 0 |
| `python3 scripts/check_soc_sources.py` | 0 |
| `python3 scripts/check_port_contracts.py` | 0 |
| `python3 scripts/check_nvm_record_space.py` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 0 |
| `python3 scripts/check_baremetal_only.py --selftest` | 0 |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 |
| `python3 scripts/check_sweep_shape.py --self-test` | 0 |
| `python3 scripts/xvlog_gate.py --check` | 0 |
| `python3 scripts/measure_control_flow.py --selftest` | 0 |
| `python3 scripts/measure_cohesion.py --selftest` | 0 |
| `python3 scripts/check_em_dash.py --base 2d8fd62fd986ea2d6a87d284e144f023034c0944` | 0 |
| `python3 scripts/measure_fail_fast.py --check` | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 0 |
| `python3 scripts/measure_naming.py --check` | 0 |
| `python3 sw/builder/test_builder.py` | 0 |
