# Manager pre-publication validation

Candidate `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3`, live base `2d8fd62fd986ea2d6a87d284e144f023034c0944`. All 38 manager commands exited 0. The candidate descends directly from the base; its tree `1fc6e7edcfc5a3e1f055ed1f73ba70614996977e` is the candidate merge tree.

The xvlog ratchet passed with zero first-party findings and its existing four pinned-processor findings. The full builder is running separately. Its result will be posted in the PR thread; no builder pass is claimed in this archive.

The complete native bar remains pending until positive contract reviews. Local workflow replicas and hosted checks will start with publication. This record is evidence, not review or merge approval.

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
