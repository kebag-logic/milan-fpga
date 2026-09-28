[A397] REVIEW READY

Commit: `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` on `602-phc-step-mr` (local; not pushed).

Changed: the option-off adjtime observation now spans the settle interval up to the settime baseline; the two delayed-cause controls are retained; the firmware gate contract and accepted coincidence/measurement labels are corrected. No RTL, builder, firmware, configuration or submodule change was made in this round.

Acceptance criteria: met at this committed head.

- R367-2 F1: the firmware contract names two `media_rebase_p_w` references and the CRF-only restart initializer, with #602 citations. Both stale-document scans were rerun and every hit classified: zero stale claims outside `docs/history/**`. The full builder bank passes in both compiler modes.
- R366-2 F1: the 16-cycle and 256-cycle controls each fail only adjtime. The original failure sets remain settime-only = settime `mr` plus MEDIA_RESET; adjtime-only = adjtime alone; both-causes = all three. Clean option-off remains 234/0.
- Accepted suggestions: coincidence is named as suppression coverage with the pending-merge bound; the README cites the round-2 reviewers' 42/42 phase measurement at `471892a9`; the Makefile labels #602 PHC-only exclusions.
- All 50 generated artifacts across five configurations match the base-derived manifest. Both AX OOC shapes pass. The area question remains closed by the round-2 assignment; no new area claim is made.

Validation: all commands below returned 0 at `6b2ebd1c435136966f84ffc16d28a80c7d6b9387`. Full `milan_dp` passes, including gmstep 103/0, option-off 234/0, render campaign 6/6 and default gmstep campaign 6/6. The full gmstep campaign passes 22/22 (two clean baselines, twenty caught controls). `tkdiag` passes 96/0 and catches all four mutants.

`$PACKET` denotes the supplied `602-a397` evidence directory. Commands ran from the physical `$LANES/602-phc-step-mr` worktree in the foreground with explicit timeouts; none was piped. Per-gate receipts record the head, command, elapsed time, rc, full-log size and SHA-256. `HANDOFF.md` supplies file:line mapping, controls, scan classification and gate tables; `PR-BODY.md` is updated locally.

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


Open risks/questions: no unresolved implementation question. The compiler-absent bank explicitly omits compiled instruments; both builder modes omit the unavailable historical placed-calibration report. The gmstep harness uses compressed clocks and the streaming escape, and does not prove physical clock continuity or an lwSRP reservation. Coincidence grades suppression; isolated checks grade an added PHC-only cause. The final audit confirms a clean worktree, unchanged protected bytes and submodule pins, unchanged read-only inputs, bounded packet files and one commit with a one-line subject and no body or trailers. Independent re-review remains required. No push or PR edit was performed.
