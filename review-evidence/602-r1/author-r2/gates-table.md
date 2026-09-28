| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |
|---|---|---:|---:|---:|
| `rtl-lint.json` | `python3 scripts/lint_rtl.py --check --jobs 8` | 1800 | 9.52 | 0 |
| `ci-scope.json` | `python3 scripts/ci_scope.py --selftest` | 600 | 2.03 | 0 |
| `baremetal-check.json` | `python3 scripts/check_baremetal_only.py --check` | 600 | 14.98 | 0 |
| `baremetal-selftest.json` | `python3 scripts/check_baremetal_only.py --selftest` | 600 | 5.6 | 0 |
| `docs.json` | `python3 scripts/docs_check.py` | 600 | 4.3 | 0 |
| `doc-style.json` | `python3 scripts/check_doc_style.py` | 600 | 0.07 | 0 |
| `doc-style-selftest.json` | `python3 scripts/check_doc_style.py --selftest` | 600 | 0.05 | 0 |
| `em-dash.json` | `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 600 | 3.43 | 0 |
| `doc-paths.json` | `python3 scripts/check_doc_paths.py` | 600 | 0.09 | 0 |
| `toc.json` | `python3 scripts/gen_toc.py --check` | 600 | 2.56 | 0 |
| `toc-selftest.json` | `python3 scripts/gen_toc.py --selftest` | 600 | 0.84 | 0 |
| `gptp-docs.json` | `python3 scripts/check_gptp_docs.py --with-submodule` | 600 | 0.18 | 0 |
| `feature-status.json` | `python3 scripts/check_feature_status.py --self-test` | 600 | 0.69 | 0 |
| `solution-docs.json` | `python3 scripts/check_solution_docs.py` | 600 | 0.13 | 0 |
| `submodule-docs.json` | `python3 scripts/check_submodule_docs.py` | 600 | 0.48 | 0 |
| `module-matrix.json` | `python3 docs/traceability/gen_module_matrix.py --check` | 600 | 0.99 | 0 |
| `diagram-pngs.json` | `python3 scripts/check_diagram_pngs.py` | 600 | 0.35 | 0 |
| `archive.json` | `python3 scripts/check_archive.py` | 600 | 0.28 | 0 |
| `source-lists.json` | `python3 scripts/check_rtl_source_lists.py` | 600 | 1.39 | 0 |
| `sv-idiom.json` | `python3 scripts/check_sv_idiom.py` | 600 | 0.45 | 0 |
| `cpp-idiom.json` | `python3 scripts/check_cpp_idiom.py` | 600 | 1.23 | 0 |
| `py-idiom.json` | `python3 scripts/check_py_idiom.py` | 600 | 3.46 | 0 |
| `hygiene.json` | `python3 scripts/check_hygiene.py --check` | 600 | 0.35 | 0 |
| `test-evidence.json` | `python3 scripts/measure_test_evidence.py --check` | 600 | 5.4 | 0 |
| `diff-check.json` | `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | 120 | 0.06 | 0 |
| `milan-dp.json` | `make -C $ROOT/tb/verilator/milan_dp run` | 10800 | 1425.01 | 0 |
| `tkdiag.json` | `make -C $ROOT/tb/verilator/tkdiag` | 1800 | 24.05 | 0 |
| `gmstep-mutants.json` | `make -C $ROOT/tb/verilator/milan_dp gmstep-mutants` | 7200 | 874.05 | 0 |
| `builder-rv32.json` | `python3 sw/builder/test_builder.py --require-rv32` | 10800 | 765.39 | 0 |
| `builder-absent.json` | `python3 $PACKET/builder_absent.py` | 10800 | 554.17 | 0 |
| `ooc-after.json` | `python3 $PACKET/ooc_measure.py after` | 14400 | 1088.44 | 0 |
| `artifact-identity.json` | `python3 $PACKET/check_artifact_identity.py` | 1200 | 0.53 | 0 |
| `stale-doc-rescan.json` | `python3 $PACKET/stale_doc_scan.py` | 180 | 1.36 | 0 |
| `candidate-audit.json` | `python3 $PACKET/audit_candidate.py` | 1200 | 0.69 | 0 |
