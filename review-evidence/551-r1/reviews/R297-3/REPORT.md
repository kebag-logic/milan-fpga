[R297] POSITIVE - exact head 6e4a3b420e055ef7529ceb16bb2ab5be93c34487

# R297-3: external independent review of PR #553 (issue #551), round 4

- **Head:** `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`, tree `f4e0bc482e7ee734f9ff50c627cedfbc89beacad`. This is the PR head (`receipts/hosted_checks_6e4a3b42.txt`).
- **Delta judged:** `f219a5ed..6e4a3b42`, one commit. Round R297-2 covered `f219a5ed` in full.
- **Authorities:** AGENTS.md and CONTRIBUTING.md. Issue #551: the body, the decision at 5813147847, the R296-1/R297-1 decision at 5816014072, the round-3 assignment at 5831903033 and the round-4 assignment at 5833406989.
- **Upstream sources:** processor PR #114 (`a8f8ce81`, "keep an SRP admission grant low until the source's current TSpec has been evaluated"). Issue #508, which PR #560 closed when it adopted processor pin `990f9652` at dev `864b36f5`.

## Verdict

**POSITIVE.** No finding is open at this head. The commit changes exactly two text files, and each change does what the round-4 assignment asked:

- R297-2 F1 = R296-2 N1 is closed.
- R296-2 S2 is closed.

All five lenses were applied at this head and are clean.

## What the delta is

`receipts/delta_diff.txt`:

- **Commit and files:** the commit has one subject line and no body or trailers. It changes two files, both mode 100644:
  - `tests/features/milan_streaming_licence.feature`
  - `tb/verilator/milan_dp/README.md`
- **`milan_streaming_licence.feature:92-94`:** three comment lines replace the three "Residual ... previous slope ... pending fix" lines. The scenario title (`:87`), the `When` step (`:95`) and the `Then` step (`:96`) are unchanged. Every changed line in the feature is a `#` comment.
- **`README.md:468`:** the pre-#112 control row now reads "34 failures total: 28 `[I]` assertions and 6 `[J]` admitted-case timing checks". The rest of the row is unchanged.

## Assigned verification items

| item | result | evidence |
|---|---|---|
| The comment says the grant waits for the current TSpec (processor #112, adopted through #508), with no residual window or pending fix | Met | `feature:92-94`. The wording matches processor PR #114's title. `a8f8ce81` lies between `7a47f578` and pin `990f9652` (`receipts/crflic/control_identity.txt`: both ancestor checks say yes). #508 is the issue that PR #560 closed when it moved the gitlink `09f9bf38 -> 990f9652` at dev `864b36f5`. `sim_crf_licence.cpp:59` and `:1081,1090` confirm that `[I]` is the changed-TSpec refused case, as the comment says. |
| Step text and assertions unchanged | Met | `receipts/delta_diff.txt`: no line outside a comment changed. `tests/steps/` is untouched. |
| `grep -rnE "Residual\|pending fix\|previous slope" tests/` is empty | Met | `receipts/gates/absence_grep.log`: grep rc 1. The wider case-insensitive search in `receipts/remnant_search.txt` also finds no residual-window claim. It returns two unrelated hits: a history document, and `sim_crf_licence.cpp:1087`, which correctly says neither previous slope may decide. |
| behave passes all scenarios | Met | `receipts/gates/behave_full.log`: 14 features, 344 scenarios and 1739 steps passed; 0 failed, 0 skipped. |
| All four BDD mutants are caught | Met | `scripts/bdd_mutants.py`, which I wrote for this round, runs on `git archive HEAD` copies in scratch. Clean before and after: 5/5, rc 0. ACTIVE-only, grant-only, ACTIVE OR grant, and AND with an extra term: each rc 1, and each fails exactly the scenario at `feature:87` on the "nothing else" assertion (`receipts/bdd/`). |
| README states 28 `[I]` + 6 `[J]` = 34, matching a rerun | Met | `scripts/prefix_control.sh` builds the unchanged head leg against the processor `hdl/` at `7a47f578`, extracted by `git archive`. The dependency file shows that build compiled the old `KL_srp_admission.sv`. Result: `checks: 415 failures: 34`, with `fail_section_I=28` and `fail_section_J=6`. Each of the four `[I]` cases fails 7 checks: grant, licence, START, STOP and three counter resets. `[J]` fails 2 checks, the ACTIVE-rise count and the three-round rise bound, in three of its four cases (`receipts/crflic/prefix_control.rc`, `.run.log`). The same leg at pin `990f9652` gives 415/0, rc 0 (`receipts/crflic/head_pin.rc`). |
| docs_check in both modes, check_em_dash, gen_toc `--verify-anchors` | Met | See `receipts/gates_venv/` for the full results, including gen_toc `--check`. docs_check has 0 findings in git mode (scrub 23/23) and in filesystem mode (22/22, with only inventory parity skipped). check_em_dash `--base 864b36f5` has 0 findings and 339/339 arms. gen_toc `--check` is OK, and `--verify-anchors` reproduces 174 links. These gates ran under a private venv with the pinned `tools/markdown/requirements.txt`. The host interpreter lacks that renderer, so the same three commands return rc 2 "cannot judge" there (`receipts/gates/`). That is an environment limit, not a result. |
| Nothing but the two text files changed | Met | `receipts/delta_diff.txt` (`--raw`). |

Other gates that returned rc 0 at this head (`receipts/gates/summary.txt`):

- `check_doc_style`
- `check_doc_paths`: 847 paths
- `measure_test_evidence --check`
- `gen_module_matrix --check`: 69 modules
- `git diff --check f219a5ed 6e4a3b42`

## Findings

None open at this head.

## Prior public findings on this PR, resolved or retained at this head

| finding | status | evidence at `6e4a3b42` |
|---|---|---|
| R297-2 F1 (MINOR: Docs, Conformance), the same defect as R296-2 N1 (MINOR: Conformance, Tests, Docs). The residual-window comment in the licence scenario. | **CLOSED** | `feature:92-94` states the current contract. R297-2's verification search (`residual\|pending fix\|first-round grant`, case-insensitive, on the feature) is empty (`receipts/remnant_search.txt`). The feature passes 5/5, and all wrong-composition arms fail (`receipts/bdd/`). |
| R296-2 S2 (SUGGESTION: Docs). The README control row gave only the 28 `[I]` failures. | **CLOSED** | `README.md:468` gives 28 + 6 = 34, and my rerun reproduces it exactly. |
| R297-2 S1 (SUGGESTION: Tests). The no-PDU refused check has no demonstrated failing arm. | Retained as a SUGGESTION, and it does not affect coverage | Unchanged. The pre-fix control again fails the licence, counter-pair and reset checks but not the PDU check. The manager moved this to #495, which is open. |
| R297-2 S2 (SUGGESTION: Tests, Robustness). No shipped case refuses a declaration made over a standing admitted one. | Retained as a SUGGESTION | Unchanged, and moved to #495. |
| R296-2 S1 (SUGGESTION: Tests). The grant-falls-under-ACTIVE closing edge is not exercised. | Retained as a SUGGESTION | Unchanged, and moved to #495. |
| R296-1 F1-F4, R297-1 F1-F4 | CLOSED at `f219a5ed` by both round-2 reviews | Nothing in their scope changed in this delta: no RTL, bench, step, generator or contract document. |

## Per-lens results

[R297] PASS Conformance - `tests/features/milan_streaming_licence.feature:92-94`, `tb/verilator/milan_dp/README.md:468`; issue 551 comments 5831903033 (item 3) and 5833406989 (items 1-2) - Checked against the round-4 assignment and the round-3 "remove the residual-window text" acceptance:
- The comment now states the current-TSpec grant guarantee. That matches processor PR #114's title and pin lineage (`control_identity.txt`) and issue #508 / PR #560.
- The step and assertion are unchanged, so the pinned contract is still ACTIVE AND the real grant.
- The README count equals the rerun.

[R297] PASS RTL - `git diff --raw f219a5ed 6e4a3b42` (`receipts/delta_diff.txt`) - No RTL, bench or processor file is in the delta, so the lens's scope is untouched since R297-2 covered `f219a5ed`. To confirm this at this head:
- the gate assignment the mutation runner requires still reads `milan_datapath.sv:6623-6624` exactly once;
- the unchanged `obj_crflic` leg at pin `990f9652` builds with Verilator 5.050 and passes 415/0 (`receipts/crflic/head_pin.*`, `receipts/tool_identity.txt`).

[R297] PASS Robustness - `receipts/crflic/head_pin.run.log`, `receipts/crflic/prefix_control.run.log` - No behaviour changed. At this head the refused/admitted re-declaration cases pass for both sources and both phases, and so do the unwarmed cases `[G]`-`[J]`. The pre-#112 processor still fails exactly the documented refused-case signature: grant and licence pulse, a START/STOP pair and three counter resets in each `[I]` case.

[R297] PASS Tests - `tests/features/milan_streaming_licence.feature:87-96`, `receipts/bdd/bdd_mutants_summary.txt`, `receipts/gates/behave_full.log` - The only feature change is comment text. The full suite passes 344/0. The four composition mutants (ACTIVE-only, grant-only, OR, extra term) each fail the pinned scenario, and the clean copy passes before and after, so the scenario still detects the defects it claims to.

[R297] PASS Docs - `tb/verilator/milan_dp/README.md:468`, `tests/features/milan_streaming_licence.feature:92-94`, `receipts/gates_venv/`, `receipts/gates/summary.txt`, `receipts/remnant_search.txt` - Both texts are true against the executable evidence. The whole tree has no residual-window or pending-fix remnant, and the documentation gates pass as listed above.

Note on wording: the README's "6 `[J]` admitted-case timing checks" are the ACTIVE-rise count and the three-round rise bound (`sim_crf_licence.cpp:1126-1128`). Both judge the optimistic window's rise, so the wording is accurate enough for a re-runner to match, and I do not raise it as a finding.

## Reviewer-owned completion ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `feature:87-96`, `README.md:468`, issue 551 decisions and assignments, processor PR #114 / `a8f8ce81` lineage, issue #508 / PR #560 | R297-3 | `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` |
| RTL | CLEAN | delta `--raw` (no RTL in scope); `milan_datapath.sv:6623-6624`; `obj_crflic` build and run at pin `990f9652` | R297-3 | `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` |
| Robustness | CLEAN | `obj_crflic` `[G]`-`[J]` at the head, 415/0; pre-#112 control 34 failures, 28 `[I]` + 6 `[J]` | R297-3 | `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` |
| Tests | CLEAN | full behave 344/0; four BDD mutants caught with clean controls; step file unchanged | R297-3 | `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` |
| Docs | CLEAN | `README.md:468`, `feature:92-94`, remnant search, docs_check (both modes), check_em_dash, gen_toc `--check` / `--verify-anchors`, doc_style, doc_paths, module matrix, test-evidence ratchet | R297-3 | `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` |

This round's ledger is based on a delta review. For the content under each lens that the delta does not touch, it relies on R297-2's full coverage of the ancestor `f219a5ed`. Since then, nothing in the RTL, Robustness or Tests-executable scope has changed. The Conformance and Docs artifacts that did change were re-covered here.

## Real limits

- **Delta review only:** I judged `f219a5ed..6e4a3b42`. I did not re-derive the content under R297-2 beyond the head leg rerun, the BDD arms, and the searches and gates listed above.
- **How the control was built:** it compiled an extracted processor `hdl/` tree via `PP_DIR`, not a temporary repin of the submodule as the README row describes. The build inputs are equivalent: the dependency file names the old admission source, and the processor `hdl/` tree ids are recorded. The clone's gitlink and submodule checkout were never touched.
- **Banks not run:** I did not run the full parent, processor, gPTP, Yosys or builder banks, the default `milan_dp` sweep, `crflic-mutants`, or act. The manager's public evidence covers these, and I did not re-execute them.
- **Hosted checks:** my capture at this head was mid-run (`receipts/hosted_checks_6e4a3b42.txt`).
  - Succeeded: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability and Yosys shards 0-3.
  - Still in progress: docs-check, elaborate, Verilator shards 0-4 and yosys-elaboration.
  - Skipped context: "Physical gPTP (nightly and manual)". This is not an executed job.
- **Not run:** physical calibration and all hardware. Field skips are not hardware proof.
- **Clone restored:** after the probes the clone is at the exact head. The index matches the head tree, the tracked blobs and modes match, the status is clean including ignored files (the generated artifacts were removed), and the submodule gitlinks are unchanged (`receipts/restore_verification.txt`).

## Pending manager duties

- Hosted exact-head acceptance, when the in-progress jobs finish, and the act replay.
- The final candidate merge against the live dev `fd9e0ebf2bbaa38330e99d1c489f01a820f1c363`, from source base `864b36f5`, and its validation.
- Explicit maintainer merge authorization, post-merge containment, and closing #551.
- Tracking the retained suggestions in #495.

## Receipts

Every published receipt and script is listed in `MANIFEST.sha256`.

R297-3 FINISHED
