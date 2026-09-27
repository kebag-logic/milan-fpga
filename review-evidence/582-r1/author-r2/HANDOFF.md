# Round 2 handoff

Author: [A374]. Reviewers: [R354] and [R355].
Issue #582; PR #596; branch `582-baremetal-clock`.
Starting head: `3baff4411fd70aaccb066662628ff0b0a7d7c05d`.
Base: `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Status: required items 1-6 and assigned local validation complete; ready for independent re-review.

## Required items

| Item | Change and file:line | Mutant/probe and result |
|---|---|---|
| 1: R354 F1 / R355 F1 / bank failure | `scripts/ci_scope.py:55,265` registers the tap page and an independent classifier case. `docs/testing/CI_WORKFLOWS.md:56,62,74` records four relevant pages and the clock-test reader. | `ci_scope.py --selftest`: rc 0, including rejection when the tap page is removed from the table. |
| 2: R354 F2 / R355 F3 | `sw/builder/test_clock_contract.py:75` compares each builder ROM with a direct generator run at its configured Milan clock. Default-clock and system-clock generator runs must produce different bytes. `sw/builder/test_builder.py:27559,27567` adds this check to both full bank modes. | R354 M21 (dropped `--clk-hz`) and R355 probe 36 (`sys_clk_hz` forwarded): KILLED, rc 1 with the owning ROM diagnostic. Restored control: rc 0 for all five configurations. |
| 3: R355 F2 | `sw/builder/test_clock_contract.py:47,60` accepts `flashboot: none` at the contract clock and refuses all five invalid-clock variants. `:123,129,143` covers every configured product argv plus explicit and implicit no-Milan clocks. | R355 B3 and S1-S4: KILLED, rc 1 with owning refusal-test diagnostics. C0-C3: CONTROL-PASS, rc 0. Reviewer probe 31: 75 cases, zero unexpected. |
| 4: R355 F4 | `sw/builder/README-parameters.md:58` and `docs/ENDSTATION_BUILDER.md:967,1014` state the fixed Milan clock using `recipe.py` `CPU_HZ`; no number is restated. | `usage-probe.py`: both reference rows and product-profile entry pass. All documentation gates return rc 0 at the committed head. |
| 5: R355 F5 / R354 S2 | `scripts/check_solution_docs.py:794` preserves the default-change mutation despite added help. `sw/litex/milan_soc.py:7,3391,3401,3494` names required clock and generated entity options, removes the tracked-entity fallback claim, and clarifies the no-Milan CLI boundary. | `usage-probe.py`: seven header invocations plus stated required options reach the pre-platform boundary; both clock help entries cite `recipe.py`; executable AST equals round 1 after removing help text, proving unchanged defaults. Reviewer probe 31 confirms the required clock addition. |
| 6: R354 S1 | `sw/litex/test_pp_mem_bridge.py:389` and `sw/builder/test_clock_contract.py:161` read normalized `load_config` results. `sw/litex/test_pp_mem_bridge.py:400` and `sw/builder/test_clock_contract.py:185` cover omitted system clocks. | R354 bypass probe now returns the expected AX system/Milan pair for the omitted key. Real normalization passes for all five fixture shapes. M16/M17/M18 pair mutations: KILLED; normalized independent fixture control passes. |

The read-only reviewer scripts supply their exact substitution strings and commands.
`reviewer-probes.py` replaces their checkout/copy loops with byte restoration in
`finally`, in this lane only. No additional checkout or tree export is used.
For M21 and probe 36, the assigned new bank test replaces the old assertion replay.
Fresh temporary bytecode caches prevent stale imports. All edited bytes are restored.
`probe-results.json` records each command, return code, log hash and size.

The CLI probes stop before platform construction. They prove argument acceptance,
not hardware elaboration. The no-Milan path still cannot complete a bare-metal
firmware image because the existing code requires the Milan entity; the usage
comment now states that limitation. No default or runtime behavior changed.

## Five-configuration artifact identities

The baseline manifest is the previous author's recorded base result for
`9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`, supplied in the allowed packet.
`identity.py` regenerates the candidate outputs in a temporary directory and
compares every artifact role and per-file SHA-256 with that manifest.
Each set digest hashes compact, sorted JSON of artifact role to file SHA-256.
The 61 artifact-role entries match. Five tracked configuration files, the
clock recipe and capture receipt also equal the base bytes (`unchanged-inputs.json`).
No tracked configuration was refused; the STOP condition did not trigger.

| Configuration | Entries | Base SHA-256 = candidate SHA-256 | Result |
|---|---:|---|---|
| `endstation_arty_4x4` | 12 | `f1a8ba03c1e639a0e6628d664efadc5d71f5ea45e7aa5398d44c93a8cf92b3f0` | identical |
| `endstation_arty_8ch` | 12 | `e31a65d95263cc96f308d9b29d83e53c0425a25a110728120741fe41e671f7fc` | identical |
| `endstation_arty_current` | 13 | `12f3fcedf8b24a32862d00e4a42e2107b8ad2b115606fcbfcf74c77a59b0427f` | identical |
| `endstation_ax7101_1x1_tdm8` | 12 | `deeee0e1261257049a0e4b69349d86c6f6ff52cc63c097f9f77d388b4b1050c4` | identical |
| `endstation_ax7101_8x8` | 12 | `6f8ce8711b3d995df08874ede226159efb4cd566cd7d47002896d1eb881e7732` | identical |

## Gate results at committed head

All 51 commands below returned rc 0 at the committed head
`77998f14b16bf7605956332d0f0ac8af0cecab5a`.
Commands ran sequentially, in the foreground, without pipelines, from the
physical `$LANES/582-baremetal-clock` directory.
`gate-results.json` retains exact argument arrays, working directory, head,
return code, elapsed time, full-log location, SHA-256 and size.
`gates.py` reproduces the sequence. It verifies a clean committed head before
starting and verifies the same clean head after finishing.

For compact commands below, `$PY` is the existing SoC environment's
`$WORKSPACE_HOME/litex-milan/venv/bin/python3`; `$DOC_PY` is the existing pinned
Markdown environment's `/tmp/582-a370-docs/bin/python3`; `$OUT` is this packet.
No environment, installed package, SDK, prefix or tree export is stored here.
Logs over 200 KB remain outside this packet and are represented by hash and size.

| Gate | Command | rc | Seconds | Packet evidence |
|---|---|---:|---:|---|
| builder-rv32 | `timeout 14400 $PY -u sw/builder/test_builder.py --require-rv32` | 0 | 768.81 | gates/builder-rv32.log |
| builder-absent | `timeout 14400 $PY -u $OUT/builder-absent.py` | 0 | 566.26 | gates/builder-absent.log |
| clock-contract | `timeout 1800 $PY sw/builder/test_clock_contract.py --soc` | 0 | 3.82 | gates/clock-contract.log |
| declarations | `timeout 1800 $PY sw/builder/test_declarations.py` | 0 | 3.17 | gates/declarations.log |
| capture | `timeout 1800 $PY scripts/check_nvm_capture.py` | 0 | 0.82 | gates/capture.log |
| pp-mem | `timeout 1800 $PY sw/litex/test_pp_mem_bridge.py` | 0 | 11.94 | gates/pp-mem.log |
| identity | `timeout 1800 $PY $OUT/identity.py` | 0 | 0.67 | gates/identity.log |
| reviewer-mutants | `timeout 7200 $PY -u $OUT/reviewer-probes.py` | 0 | 26.11 | gates/reviewer-mutants.log |
| R354-bypass | `timeout 1800 $PY $REVIEWS/582-r354-1-packet/scripts/bypass_probe.py $LANES/582-baremetal-clock` | 0 | 0.57 | gates/R354-bypass.log |
| R355-soc | `timeout 1800 $PY $REVIEWS/582-r355-1-packet/scripts/31_soc_behaviour.py $LANES/582-baremetal-clock round2` | 0 | 0.36 | gates/R355-soc.log |
| usage | `timeout 1800 $PY $OUT/usage-probe.py` | 0 | 0.31 | gates/usage.log |
| docs-00-docs_check | `timeout 1800 $DOC_PY scripts/docs_check.py` | 0 | 4.22 | gates/docs-00-docs_check.log |
| docs-01-check_em_dash | `timeout 1800 $DOC_PY scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` | 0 | 3.12 | gates/docs-01-check_em_dash.log |
| docs-02-check_doc_style | `timeout 1800 $DOC_PY scripts/check_doc_style.py` | 0 | 0.06 | gates/docs-02-check_doc_style.log |
| docs-03-check_doc_paths | `timeout 1800 $DOC_PY scripts/check_doc_paths.py` | 0 | 0.06 | gates/docs-03-check_doc_paths.log |
| docs-04-check_archive | `timeout 1800 $DOC_PY scripts/check_archive.py` | 0 | 0.31 | gates/docs-04-check_archive.log |
| docs-05-check_archive | `timeout 1800 $DOC_PY scripts/check_archive.py --selftest` | 0 | 0.06 | gates/docs-05-check_archive.log |
| docs-06-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --selftest` | 0 | 0.87 | gates/docs-06-gen_toc.log |
| docs-07-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --verify-anchors` | 0 | 1.62 | gates/docs-07-gen_toc.log |
| docs-08-gen_toc | `timeout 1800 $DOC_PY scripts/gen_toc.py --check` | 0 | 2.57 | gates/docs-08-gen_toc.log |
| docs-09-check_feature_status | `timeout 1800 $DOC_PY scripts/check_feature_status.py --self-test` | 0 | 0.67 | gates/docs-09-check_feature_status.log |
| docs-10-check_solution_docs | `timeout 1800 $DOC_PY scripts/check_solution_docs.py` | 0 | 0.11 | gates/docs-10-check_solution_docs.log |
| docs-11-check_solution_docs | `timeout 1800 $DOC_PY scripts/check_solution_docs.py --selftest` | 0 | 2.37 | gates/docs-11-check_solution_docs.log |
| docs-12-check_submodule_docs | `timeout 1800 $DOC_PY scripts/check_submodule_docs.py` | 0 | 0.52 | gates/docs-12-check_submodule_docs.log |
| docs-13-check_submodule_docs | `timeout 1800 $DOC_PY scripts/check_submodule_docs.py --selftest` | 0 | 0.06 | gates/docs-13-check_submodule_docs.log |
| docs-14-check_gptp_docs | `timeout 1800 $DOC_PY scripts/check_gptp_docs.py --with-submodule` | 0 | 0.16 | gates/docs-14-check_gptp_docs.log |
| docs-15-gen_module_matrix | `timeout 1800 $DOC_PY docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 | gates/docs-15-gen_module_matrix.log |
| docs-16-check_baremetal_only | `timeout 1800 $DOC_PY scripts/check_baremetal_only.py --check` | 0 | 14.69 | gates/docs-16-check_baremetal_only.log |
| docs-17-check_baremetal_only | `timeout 1800 $DOC_PY scripts/check_baremetal_only.py --selftest` | 0 | 5.33 | gates/docs-17-check_baremetal_only.log |
| docs-18-check_soc_sources | `timeout 1800 $DOC_PY scripts/check_soc_sources.py` | 0 | 0.11 | gates/docs-18-check_soc_sources.log |
| docs-19-check_soc_sources | `timeout 1800 $DOC_PY scripts/check_soc_sources.py --selftest` | 0 | 0.21 | gates/docs-19-check_soc_sources.log |
| docs-20-check_rtl_source_lists | `timeout 1800 $DOC_PY scripts/check_rtl_source_lists.py` | 0 | 1.37 | gates/docs-20-check_rtl_source_lists.log |
| docs-21-check_rtl_source_lists | `timeout 1800 $DOC_PY scripts/check_rtl_source_lists.py --selftest` | 0 | 2.62 | gates/docs-21-check_rtl_source_lists.log |
| docs-22-check_hygiene | `timeout 1800 $DOC_PY scripts/check_hygiene.py --check` | 0 | 0.36 | gates/docs-22-check_hygiene.log |
| docs-23-check_hygiene | `timeout 1800 $DOC_PY scripts/check_hygiene.py --selftest` | 0 | 0.31 | gates/docs-23-check_hygiene.log |
| docs-24-check_py_idiom | `timeout 1800 $DOC_PY scripts/check_py_idiom.py` | 0 | 3.37 | gates/docs-24-check_py_idiom.log |
| docs-25-check_py_idiom | `timeout 1800 $DOC_PY scripts/check_py_idiom.py --selftest` | 0 | 3.37 | gates/docs-25-check_py_idiom.log |
| docs-26-check_sh_idiom | `timeout 1800 $DOC_PY scripts/check_sh_idiom.py` | 0 | 0.26 | gates/docs-26-check_sh_idiom.log |
| docs-27-check_sh_idiom | `timeout 1800 $DOC_PY scripts/check_sh_idiom.py --selftest` | 0 | 0.27 | gates/docs-27-check_sh_idiom.log |
| docs-28-check_sweep_shape | `timeout 1800 $DOC_PY scripts/check_sweep_shape.py --self-test` | 0 | 11.95 | gates/docs-28-check_sweep_shape.log |
| docs-29-check_deploy_shape | `timeout 1800 $DOC_PY scripts/check_deploy_shape.py --self-test` | 0 | 0.42 | gates/docs-29-check_deploy_shape.log |
| docs-30-check_entity_shape | `timeout 1800 $DOC_PY scripts/check_entity_shape.py --self-test` | 0 | 41.35 | gates/docs-30-check_entity_shape.log |
| docs-31-ci_scope | `timeout 1800 $DOC_PY scripts/ci_scope.py --selftest` | 0 | 2.47 | gates/docs-31-ci_scope.log |
| docs-32-check_em_dash | `timeout 1800 $DOC_PY scripts/check_em_dash.py --selftest` | 0 | 3.12 | gates/docs-32-check_em_dash.log |
| docs-33-docs_check | `timeout 1800 $DOC_PY scripts/docs_check.py --selftest` | 0 | 0.16 | gates/docs-33-docs_check.log |
| docs-34-check_doc_style | `timeout 1800 $DOC_PY scripts/check_doc_style.py --selftest` | 0 | 0.06 | gates/docs-34-check_doc_style.log |
| docs-35-check_gptp_docs | `timeout 1800 $DOC_PY scripts/check_gptp_docs.py --selftest` | 0 | 0.16 | gates/docs-35-check_gptp_docs.log |
| docs-36-ci_events | `timeout 1800 $DOC_PY scripts/ci_events.py --check` | 0 | 0.21 | gates/docs-36-ci_events.log |
| docs-37-ci_events | `timeout 1800 $DOC_PY scripts/ci_events.py --selftest` | 0 | 14.94 | gates/docs-37-ci_events.log |
| diff-worktree | `timeout 600 git diff --check` | 0 | 0.03 | gates/diff-worktree.log |
| diff-base | `timeout 600 git diff --check 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD` | 0 | 0.06 | gates/diff-base.log |

Both builder modes run the complete bank. The absent-mode wrapper hides exactly
the three RV32 compiler selectors; `absent-audit.json` records the selectors and
the expected stand-downs. Host compiler probes remain real. The required-RV32
run covers those compiler-dependent instruments. The existing gate 11 physical
resource-calibration arm is NOT RUN because its historical report is absent.
The bank returns rc 0 with that explicitly reported limit. No hardware claim is made.

The assignment names `check_baremetal_only.py` without a mode. Its bare
invocation returns rc 2 with a usage error. The gate requires `--check` or
`--selftest`; both documented modes are explicitly run above and pass. No
CLI default was changed to accommodate that invocation.

The first committed-head sequence stopped at a stale system-clock mutation
fixture in `check_solution_docs.py --selftest`. The fixture now targets the
default-value prefix, retaining the same mutated value and expected refusal.
All 43 controls pass. The initial result is retained in
`initial-gate-results.json`; the complete sequence above was rerun after
committing the repair. `docs-preflight-results.json` also retains the bare-mode
usage error; it is not a gate verdict.

## Final state and review boundary

Commit: `77998f14b16bf7605956332d0f0ac8af0cecab5a`.
Subjects: `Close clock contract review gaps in CI, ROM checks, refusals and documentation`; `Preserve the system clock mutation after adding CLI help`.
Both round-2 commits have one-line subjects, with no body or trailers. Worktree clean.

The round changes nine files, limited to tests, CI scope registration and
documentation/help. The SoC executable AST is unchanged except help keywords.
No firmware, RTL, configuration, submodule pin, capture recipe or receipt changed.
The out-of-scope simulation clock mirrors and group-5 prose remain unchanged.
No push, PR edit, merge, additional checkout or hardware operation occurred.
The local `PR-BODY.md` keeps its original label and `Closes #582` and adds Round 2.

The assigned local work is complete. Independent re-review, publication of the
branch/PR update, hosted checks and the separate merge process remain with the
assigned reviewers and maintainer. This author supplies evidence, not a review
verdict or lens ledger. `REVIEW-READY.md` is the exact final issue comment.
The final action is to append that comment to issue #582 and stop.
