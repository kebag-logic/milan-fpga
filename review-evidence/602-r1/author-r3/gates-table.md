| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |
|---|---|---:|---:|---:|
| `rtl-lint.json` | `python3 scripts/lint_rtl.py --check --jobs 8` | 1800 | 9.16 | 0 |
| `ci-scope.json` | `python3 scripts/ci_scope.py --selftest` | 600 | 2.04 | 0 |
| `baremetal-check.json` | `python3 scripts/check_baremetal_only.py --check` | 600 | 15.21 | 0 |
| `baremetal-selftest.json` | `python3 scripts/check_baremetal_only.py --selftest` | 600 | 5.73 | 0 |
| `docs.json` | `python3 scripts/docs_check.py` | 600 | 4.38 | 0 |
| `doc-style.json` | `python3 scripts/check_doc_style.py` | 600 | 0.07 | 0 |
| `doc-style-selftest.json` | `python3 scripts/check_doc_style.py --selftest` | 600 | 0.05 | 0 |
| `em-dash.json` | `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 600 | 3.31 | 0 |
| `doc-paths.json` | `python3 scripts/check_doc_paths.py` | 600 | 0.08 | 0 |
| `toc.json` | `python3 scripts/gen_toc.py --check` | 600 | 2.59 | 0 |
| `toc-selftest.json` | `python3 scripts/gen_toc.py --selftest` | 600 | 0.83 | 0 |
| `gptp-docs.json` | `python3 scripts/check_gptp_docs.py --with-submodule` | 600 | 0.16 | 0 |
| `feature-status.json` | `python3 scripts/check_feature_status.py --self-test` | 600 | 0.68 | 0 |
| `solution-docs.json` | `python3 scripts/check_solution_docs.py` | 600 | 0.12 | 0 |
| `submodule-docs.json` | `python3 scripts/check_submodule_docs.py` | 600 | 0.44 | 0 |
| `module-matrix.json` | `python3 docs/traceability/gen_module_matrix.py --check` | 600 | 0.98 | 0 |
| `diagram-pngs.json` | `python3 scripts/check_diagram_pngs.py` | 600 | 0.34 | 0 |
| `archive.json` | `python3 scripts/check_archive.py` | 600 | 0.29 | 0 |
| `source-lists.json` | `python3 scripts/check_rtl_source_lists.py` | 600 | 1.38 | 0 |
| `sv-idiom.json` | `python3 scripts/check_sv_idiom.py` | 600 | 0.45 | 0 |
| `cpp-idiom.json` | `python3 scripts/check_cpp_idiom.py` | 600 | 1.19 | 0 |
| `py-idiom.json` | `python3 scripts/check_py_idiom.py` | 600 | 3.42 | 0 |
| `hygiene.json` | `python3 scripts/check_hygiene.py --check` | 600 | 0.36 | 0 |
| `test-evidence.json` | `python3 scripts/measure_test_evidence.py --check` | 600 | 5.44 | 0 |
| `diff-check.json` | `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | 120 | 0.06 | 0 |
| `milan-dp.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp run` | 10800 | 1444.77 | 0 |
| `tkdiag.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/tkdiag` | 1800 | 21.26 | 0 |
| `gmstep-mutants.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp gmstep-mutants` | 7200 | 911.89 | 0 |
| `builder-rv32.json` | `python3 sw/builder/test_builder.py --require-rv32` | 10800 | 756.82 | 0 |
| `builder-absent.json` | `python3 $PACKET/builder_absent.py` | 10800 | 550.53 | 0 |
| `ooc-after.json` | `python3 $PACKET/ooc_measure.py after` | 14400 | 1021.27 | 0 |
| `artifact-identity.json` | `python3 $PACKET/check_artifact_identity.py` | 1200 | 0.54 | 0 |
| `stale-r366.json` | `python3 $PACKET/stale_scan_r366.py` | 180 | 1.31 | 0 |
| `stale-r367.json` | `python3 $REVIEWS/602-r367-2-packet/stale_scan_r367_2.py $LANES/602-phc-step-mr` | 180 | 1.49 | 0 |
| `probe-equivalence.json` | `python3 $PACKET/check_probe_equivalence.py` | 180 | 0.1 | 0 |
| `candidate-audit.json` | `python3 $PACKET/audit_candidate.py` | 1100 | 0.68 | 0 |
