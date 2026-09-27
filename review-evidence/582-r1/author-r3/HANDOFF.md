# Round 3 handoff

Executor: [A379]. Delta reviewer: [R354].
Issue: https://github.com/kebag-logic/milan-fpga/issues/582
PR: https://github.com/kebag-logic/milan-fpga/pull/596
Assignment: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5859065834
Takeover: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5859076610

Status: assigned implementation and committed-head validation complete;
ready for independent delta review. No review verdict is supplied here.
Branch: `582-baremetal-clock`.
Starting head: `77998f14b16bf7605956332d0f0ac8af0cecab5a`.
Final head: `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
One commit: `Clarify clock CI policy and complete product clock test controls`.
The commit has one subject line, no body and no trailers.

## Assigned items

| Item | Change and file:line | Mutant/probe and result |
|---|---|---|
| Required F1 / SG5 | `docs/testing/CI_WORKFLOWS.md:64,71` explicitly retains the relevant classification because the reader is outside `DOCS_JOB_PY`, and removes its row from the documentation-only table | R355 classification inputs replayed without pipelines: tap page `true`, plain-doc control `false`; explicit table audit passes; `ci_scope.py --selftest` rc 0 |
| Taken R354 SG1 | `sw/litex/milan_soc.py:3623` says the no-Milan option is a CLI smoke path that cannot finish a bare-metal image | R354 `soc_usage_probe.py`: seven documented invocations reach the pre-platform boundary with their stated options; 54 options have identical non-help keywords; rendered help states the limitation; all rc 0 |
| Taken R355 SG6 | `sw/builder/test_clock_contract.py:133` appends each configuration's `configs/generated/<stem>` entity directory to both accepted and divergent product argv cases | R355 mutant S9 KILLED, rc 1, owning `clock accepted before platform` assertion includes the entity path; identity control C1 rc 0 |
| Taken R355 SG7 | `sw/builder/test_clock_contract.py:94` retains the default control and skips only the system-clock control when the two configured clocks equal, with a named report | Unmodified R355 probe 39: builder accepts the equal-clock variant, test PASS and named SKIP; C4 distinct-clock control rc 0; R1 (system clock fed) and R2 (clock argument omitted) remain KILLED, rc 1 with owning ROM diagnostic |

`round3-probes.py` uses the exact mutation declarations from the read-only
round-2 reviewer script. Its copy loop is replaced with lane-local mutation
and restoration in `finally`; fresh temporary bytecode caches isolate runs.
The controls are C1, C4 and C5, all rc 0. The three assigned/regression
mutations fail by the expected owning assertion. The campaign itself returns 0.
Probe 39 reports assertion failures without changing its exit status, so the
wrapper also requires its PASS and SKIP text. Temporary variant files live
outside this packet. The usage probe runs unchanged.
`probe-results.json` records exact commands, exits, log hashes and sizes.
`review-input-identities.json` records the read-only inputs; all were rechecked.

The CLI probes stop before platform construction. They demonstrate the
argument checks, not a complete image or a hardware result. No default or
runtime guard changed. The full builder bank separately exercises elaboration.

## Five-configuration SHA-256 comparison

Base: `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
The base artifact manifest comes from the allowed previous author packet;
it was not regenerated with another checkout in this round. `identity.py`
regenerates all current outputs and compares every role and file hash with it.
All 61 artifact-role entries match. Each set digest hashes compact sorted
JSON mapping artifact roles to their file SHA-256 values.
`unchanged-configs.json` separately proves the five YAML files equal base bytes.
All five tracked configurations build; the STOP condition did not trigger.

| Configuration | Entries | Base SHA-256 = candidate SHA-256 |
|---|---:|---|
| `endstation_arty_4x4` | 12 | `f1a8ba03c1e639a0e6628d664efadc5d71f5ea45e7aa5398d44c93a8cf92b3f0` |
| `endstation_arty_8ch` | 12 | `e31a65d95263cc96f308d9b29d83e53c0425a25a110728120741fe41e671f7fc` |
| `endstation_arty_current` | 13 | `12f3fcedf8b24a32862d00e4a42e2107b8ad2b115606fcbfcf74c77a59b0427f` |
| `endstation_ax7101_1x1_tdm8` | 12 | `deeee0e1261257049a0e4b69349d86c6f6ff52cc63c097f9f77d388b4b1050c4` |
| `endstation_ax7101_8x8` | 12 | `6f8ce8711b3d995df08874ede226159efb4cd566cd7d47002896d1eb881e7732` |

## Gates at the committed head

All 48 commands below returned rc 0 at `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`.
They ran sequentially in the foreground, without pipelines, from the physical
`$LANES/582-baremetal-clock` directory. `gates.py` checks a clean
committed head before and after the sequence. `gate-results.json` records
the full argument arrays, cwd, head, elapsed time, return code, log hash and size.

`$PY` is `$WORKSPACE_HOME/litex-milan/venv/bin/python3`.
`$DOC_PY` is `/tmp/582-a370-docs/bin/python3`, the existing pinned renderer environment.
`$OUT` is this packet. No environment, package, SDK, tool prefix or tree export
is stored here. Logs over 200 KB stay outside the packet with hash/size receipts.

| Gate | Exact command | rc | Seconds | Evidence |
|---|---|---:|---:|---|
| builder-rv32 | `timeout 14400 $PY -u sw/builder/test_builder.py --require-rv32` | 0 | 773.64 | `gates/builder-rv32.log` |
| builder-absent | `timeout 14400 $PY -u $OUT/builder-absent.py` | 0 | 568.73 | `gates/builder-absent.log` |
| clock-contract | `timeout 1800 $PY sw/builder/test_clock_contract.py --soc` | 0 | 3.92 | `gates/clock-contract.log` |
| declarations | `timeout 1800 $PY sw/builder/test_declarations.py` | 0 | 3.12 | `gates/declarations.log` |
| capture | `timeout 1800 $PY scripts/check_nvm_capture.py` | 0 | 0.82 | `gates/capture.log` |
| pp-mem | `timeout 1800 $PY sw/litex/test_pp_mem_bridge.py` | 0 | 12.69 | `gates/pp-mem.log` |
| identity | `timeout 1800 $PY $OUT/identity.py` | 0 | 0.67 | `gates/identity.log` |
| round3-probes | `timeout 7200 $PY -u $OUT/round3-probes.py` | 0 | 11.29 | `gates/round3-probes.log` |
| docs-00-docs_check | `timeout 1800 $DOC_PY scripts/docs_check.py` | 0 | 4.22 | `gates/docs-00-docs_check.log` |
| docs-01-check_em_dash | `timeout 1800 $DOC_PY scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` | 0 | 3.27 | `gates/docs-01-check_em_dash.log` |
| docs-02-check_doc_style | `timeout 1800 $DOC_PY scripts/check_doc_style.py` | 0 | 0.06 | `gates/docs-02-check_doc_style.log` |
| docs-03-check_doc_paths | `timeout 1800 $DOC_PY scripts/check_doc_paths.py` | 0 | 0.11 | `gates/docs-03-check_doc_paths.log` |
| docs-04-check_archive | `timeout 1800 $DOC_PY scripts/check_archive.py` | 0 | 0.31 | `gates/docs-04-check_archive.log` |
| docs-05-check_archive | `timeout 1800 $DOC_PY scripts/check_archive.py --selftest` | 0 | 0.06 | `gates/docs-05-check_archive.log` |
| docs-06-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --selftest` | 0 | 0.87 | `gates/docs-06-gen_toc.log` |
| docs-07-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --verify-anchors` | 0 | 1.62 | `gates/docs-07-gen_toc.log` |
| docs-08-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --check` | 0 | 2.67 | `gates/docs-08-gen_toc.log` |
| docs-09-check_feature_status | `timeout 1800 $DOC_PY scripts/check_feature_status.py --self-test` | 0 | 0.67 | `gates/docs-09-check_feature_status.log` |
| docs-10-check_solution_docs | `timeout 1800 $DOC_PY scripts/check_solution_docs.py` | 0 | 0.11 | `gates/docs-10-check_solution_docs.log` |
| docs-11-check_solution_docs | `timeout 1800 $DOC_PY scripts/check_solution_docs.py --selftest` | 0 | 2.52 | `gates/docs-11-check_solution_docs.log` |
| docs-12-check_submodule_docs | `timeout 1800 $DOC_PY scripts/check_submodule_docs.py` | 0 | 0.41 | `gates/docs-12-check_submodule_docs.log` |
| docs-13-check_submodule_docs | `timeout 1800 $DOC_PY scripts/check_submodule_docs.py --selftest` | 0 | 0.06 | `gates/docs-13-check_submodule_docs.log` |
| docs-14-check_gptp_docs | `timeout 1800 $DOC_PY scripts/check_gptp_docs.py --with-submodule` | 0 | 0.16 | `gates/docs-14-check_gptp_docs.log` |
| docs-15-gen_module_matrix | `timeout 1800 $DOC_PY docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 | `gates/docs-15-gen_module_matrix.log` |
| docs-16-check_baremetal_only | `timeout 1800 $DOC_PY scripts/check_baremetal_only.py --check` | 0 | 14.69 | `gates/docs-16-check_baremetal_only.log` |
| docs-17-check_baremetal_only | `timeout 1800 $DOC_PY scripts/check_baremetal_only.py --selftest` | 0 | 5.68 | `gates/docs-17-check_baremetal_only.log` |
| docs-18-check_soc_sources | `timeout 1800 $DOC_PY scripts/check_soc_sources.py` | 0 | 0.11 | `gates/docs-18-check_soc_sources.log` |
| docs-19-check_soc_sources | `timeout 1800 $DOC_PY scripts/check_soc_sources.py --selftest` | 0 | 0.21 | `gates/docs-19-check_soc_sources.log` |
| docs-20-check_rtl_source_lists | `timeout 1800 $DOC_PY scripts/check_rtl_source_lists.py` | 0 | 1.42 | `gates/docs-20-check_rtl_source_lists.log` |
| docs-21-check_rtl_source_lists | `timeout 1800 $DOC_PY scripts/check_rtl_source_lists.py --selftest` | 0 | 2.62 | `gates/docs-21-check_rtl_source_lists.log` |
| docs-22-check_hygiene | `timeout 1800 $DOC_PY scripts/check_hygiene.py --check` | 0 | 0.36 | `gates/docs-22-check_hygiene.log` |
| docs-23-check_hygiene | `timeout 1800 $DOC_PY scripts/check_hygiene.py --selftest` | 0 | 0.36 | `gates/docs-23-check_hygiene.log` |
| docs-24-check_py_idiom | `timeout 1800 $DOC_PY scripts/check_py_idiom.py` | 0 | 3.47 | `gates/docs-24-check_py_idiom.log` |
| docs-25-check_py_idiom | `timeout 1800 $DOC_PY scripts/check_py_idiom.py --selftest` | 0 | 3.37 | `gates/docs-25-check_py_idiom.log` |
| docs-26-check_sh_idiom | `timeout 1800 $DOC_PY scripts/check_sh_idiom.py` | 0 | 0.26 | `gates/docs-26-check_sh_idiom.log` |
| docs-27-check_sh_idiom | `timeout 1800 $DOC_PY scripts/check_sh_idiom.py --selftest` | 0 | 0.26 | `gates/docs-27-check_sh_idiom.log` |
| docs-28-check_sweep_shape | `timeout 1800 $DOC_PY scripts/check_sweep_shape.py --self-test` | 0 | 12.3 | `gates/docs-28-check_sweep_shape.log` |
| docs-29-check_deploy_shape | `timeout 1800 $DOC_PY scripts/check_deploy_shape.py --self-test` | 0 | 0.46 | `gates/docs-29-check_deploy_shape.log` |
| docs-30-check_entity_shape | `timeout 1800 $DOC_PY scripts/check_entity_shape.py --self-test` | 0 | 41.21 | `gates/docs-30-check_entity_shape.log` |
| docs-31-ci_scope | `timeout 1800 $DOC_PY scripts/ci_scope.py --selftest` | 0 | 2.47 | `gates/docs-31-ci_scope.log` |
| docs-32-check_em_dash | `timeout 1800 $DOC_PY scripts/check_em_dash.py --selftest` | 0 | 3.32 | `gates/docs-32-check_em_dash.log` |
| docs-33-docs_check | `timeout 1800 $DOC_PY scripts/docs_check.py --selftest` | 0 | 0.16 | `gates/docs-33-docs_check.log` |
| docs-34-check_doc_style | `timeout 1800 $DOC_PY scripts/check_doc_style.py --selftest` | 0 | 0.06 | `gates/docs-34-check_doc_style.log` |
| docs-35-check_gptp_docs | `timeout 1800 $DOC_PY scripts/check_gptp_docs.py --selftest` | 0 | 0.16 | `gates/docs-35-check_gptp_docs.log` |
| docs-36-ci_events | `timeout 1800 $DOC_PY scripts/ci_events.py --check` | 0 | 0.21 | `gates/docs-36-ci_events.log` |
| docs-37-ci_events | `timeout 1800 $DOC_PY scripts/ci_events.py --selftest` | 0 | 14.85 | `gates/docs-37-ci_events.log` |
| diff-worktree | `timeout 600 git diff --check` | 0 | 0.03 | `gates/diff-worktree.log` |
| diff-base | `timeout 600 git diff --check 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD` | 0 | 0.03 | `gates/diff-base.log` |

Both compiler modes run the complete builder bank. The absent wrapper hides
exactly the three RV32 compiler selectors and leaves host probes real;
`absent-audit.json` records the expected compiler-dependent stand-downs.
The required-RV32 run covers those instruments. Both banks report the existing
gate-11 physical-resource calibration as NOT RUN because its historical
placement report is absent. Their command return codes are 0. These are
reported limitations, not hardware or timing-closure evidence.

`check_baremetal_only.py` requires a mode; both supported `--check` and
`--selftest` invocations pass. No CLI default was changed.
Pre-commit style checking found one overlong help line. It was wrapped and
the idiom gate passed before the commit; no assertion or acceptance criterion
was weakened. Every final gate above ran after that commit.

## Final boundary

Only the three assigned documentation/help/test files changed this round.
The worktree is clean. No firmware, RTL, configuration, gitlink, capture
recipe or capture receipt changed. The out-of-scope sweep entity-path omission,
clock-shadowing issue, simulation mirrors and group-5 prose remain unchanged.
No push, PR mutation, merge, additional checkout or hardware action occurred.

`PR-BODY.md` preserves its original `[A370]` label and `Closes #582`, and adds
Round 3 with this head and the validation results. It contains no absolute
home paths or attribution footer.

Independent delta review, publication of the branch/PR update, hosted checks
and the separate merge process remain with the reviewer and maintainer.
`REVIEW-READY.md` is the final issue comment. The only remaining action in
this assignment is to append it to issue #582, then stop.
