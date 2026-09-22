[A172] Executed commands and exits

Final candidate `b5e6c23e1b9802b5cacbc62db212064d7e429862`, tree `2fd42873a06123f87f539c116e4969c87f5e33d8`. Each JSON receipt records exact argv, cwd, timestamp and source hashes.

| Receipt | Exact command | Exit |
|---|---|---|
| archive-selftest | `rtk proxy python3 -B scripts/check_archive.py --selftest` | 0 |
| archive | `rtk proxy python3 -B scripts/check_archive.py` | 0 |
| baremetal-selftest | `rtk proxy python3 -B scripts/check_baremetal_only.py --selftest` | 0 |
| baremetal | `rtk proxy python3 -B scripts/check_baremetal_only.py --check` | 0 |
| consumers-baseline | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/consumers.py --scripts $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/snapshots/baseline/scripts --label baseline` | 0 |
| consumers-marker-mutant | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/consumers.py --scripts $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/mutants/block-marker-only --label marker-mutant` | 0 |
| consumers-starting | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/consumers.py --scripts $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/snapshots/starting/scripts --label starting` | 0 |
| consumers | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/consumers.py --assert-correct` | 0 |
| doc-paths | `rtk proxy python3 -B scripts/check_doc_paths.py` | 0 |
| doc-style-selftest | `rtk proxy python3 -B scripts/check_doc_style.py --selftest` | 0 |
| doc-style | `rtk proxy python3 -B scripts/check_doc_style.py` | 0 |
| docs | `rtk proxy python3 -B scripts/docs_check.py` | 0 |
| emdash-base | `rtk proxy python3 -B scripts/check_em_dash.py --base 52711029f374650dc93830d5ea28e81cb5c8f410` | 0 |
| emdash-selftest | `rtk proxy python3 -B scripts/check_em_dash.py --selftest` | 0 |
| feature-status | `rtk proxy python3 -B scripts/check_feature_status.py --self-test` | 0 |
| gptp-docs | `rtk proxy python3 -B scripts/check_gptp_docs.py` | 0 |
| hygiene-selftest | `rtk proxy python3 -B scripts/check_hygiene.py --selftest` | 0 |
| hygiene | `rtk proxy python3 -B scripts/check_hygiene.py --check` | 0 |
| mutations | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/mutate.py` | 0 |
| pp-sources-selftest | `rtk proxy python3 -B scripts/pp_srcs.py --selftest` | 0 |
| pp-sources | `rtk proxy python3 -B scripts/pp_srcs.py --check` | 0 |
| preservation | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/preserve.py` | 0 |
| probes-three-revisions | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/compare_probes.py` | 0 |
| py-idiom-selftest | `rtk proxy python3 -B scripts/check_py_idiom.py --selftest` | 0 |
| py-idiom | `rtk proxy python3 -B scripts/check_py_idiom.py` | 0 |
| renderer-consumers | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/render_consumers.py` | 0 |
| renderer | `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/render.py` | 0 |
| rtl-source-lists-selftest | `rtk proxy python3 -B scripts/check_rtl_source_lists.py --selftest` | 0 |
| rtl-source-lists | `rtk proxy python3 -B scripts/check_rtl_source_lists.py` | 0 |
| solution-docs | `rtk proxy python3 -B scripts/check_solution_docs.py` | 0 |
| submodule-docs | `rtk proxy python3 -B scripts/check_submodule_docs.py` | 0 |
| toc-anchors | `rtk proxy python3 -B scripts/gen_toc.py --verify-anchors` | 0 |
| toc-check | `rtk proxy python3 -B scripts/gen_toc.py --check` | 0 |
| toc-selftest | `rtk proxy python3 -B scripts/gen_toc.py --selftest` | 0 |
| traceability | `rtk proxy python3 -B docs/traceability/gen_module_matrix.py --check` | 0 |

Baseline/starting/marker-mutant consumer commands are measurement runs: exit 0 means the receipt was produced, not that the old or mutated semantics pass. Their `failed` rows are expected before/after evidence. `mutate.py` separately asserts nonzero exits at named arms.

Do not execute any candidate act_ci host orchestrator. This packet invokes no such runner. `reproduce.py` is a bounded sequence of the commands above and cache-backed synthetic renders; it has not been separately rerun as a whole.

Exploratory failures were retained and corrected transparently: an unsupported check_py_idiom.py --check invocation exited 2 (the valid command takes no --check); early new real-Git fixtures caused added-heading diff findings until an extra blank before the sentinel was removed, with the original 42 base bytes preserved; initial empty-item and unclosed-comment expected results were contradicted by GitHub and remain documented mismatches outside the named correction. No shipped prior test expectation was weakened. An initial comparison assumed all unclosed-comment shapes were also unchanged from the original base; executable comparison rejected that assumption, and the report now explicitly records six resumed regressions at the starting PR head.
