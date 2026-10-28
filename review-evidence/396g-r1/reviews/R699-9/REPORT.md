[R699] POSITIVE - exact head 70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2

# R699-9: internal cleared-context delta review, issue #396 part A, PR #786

- **Head:** `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2`, tree `49ecd37721ae83d0a84cd8bc22bff550836b85e0`.
- **Source base:** `e76a755a`. **Live dev at review time:** `97aab1d0f28bd753a3e11df6278d5cac54f964dd` (`live_dev_tip.txt`).
- **Previously reviewed head:** `a7a514fb` (R699-8, POSITIVE).
- **Delta:** one merge commit, `70b351a5`. Its parents are `a7a514fb` (the branch) and `97aab1d0` (dev). Its message is one line, "Merge dev 97aab1d0 into 396-release-gate-plan", with no body and no trailers. The merge was made because the branch predated the `ubuntu-24.04` workflow pin (#784), and the local replay refuses `ubuntu-latest`.

## Scope reconstructed

- **Acceptance.** Issue #396 acceptance 1, 2 and 5, plus the desk half of 4. This is part A. Items 3 and 4 need the bench (part B) and stay open, so the PR correctly says "Relates to #396".
- **This round's question.** Did the merge bring in only dev's own content? Did it keep both sides of the one file that auto-merged? Is the head tree the validated candidate tree? Did it alter anything in the round-8 grader, its claims or its gate?
- **Authorities for a merge.** CONTRIBUTING step 7 says "a merge is a change nobody wrote and nobody reviewed" and the merged tree must be gated. It also says that if the reviewed head directly descends from the unchanged base, the head tree is the candidate tree. Since `70b351a5` descends from live dev `97aab1d0`, its tree is the candidate tree for as long as dev stays at `97aab1d0`.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open.

- There is one new RESIDUE (R1, PR-body wording).
- One RESIDUE from R699-8 is retained (R699-8 R1).
- Two SUGGESTIONs from R699-8 are retained and stay optional.
- R699-8's POSITIVE stands for the content it reviewed: every one of the branch's eleven changed files is byte-identical between `a7a514fb` and this head, except `docs/testing/TESTING.md`, which gained exactly dev's two-line change.

### (1) The merge brings only dev's content

- **Name and status.** `git diff --name-status a7a514fb 70b351a5` is identical to `git diff --name-status e76a755a 97aab1d0`: the same 22 entries (`delta_head_vs_branch.namestatus`, `dev_since_base.namestatus`).
- **Every path classified by provenance** (mode and blob, across head, branch, dev and base; `check_tree_provenance.sh`, `tree_provenance.txt`, `tree_provenance.counts`):

  | Class | Paths | Meaning |
  |---|---|---|
  | same | 1419 | identical in all three |
  | dev-only change | 21 | head equals dev, and branch equals base |
  | branch-only change | 10 | head equals branch, and dev equals base |
  | OTHER | 1 | `docs/testing/TESTING.md`, the only file both sides changed (`overlap.names`) |

  No path holds content that is neither side's.
- **The dev content** is the ten commits `e76a755a..97aab1d0` (`dev_commits_since_base.txt`): #784 (PRs #785 and #788, the `ubuntu-24.04` pin and the act runner's label refusal) and #789 (PR #794, the cached pinned Yosys job).
- **Only the expected workflow jobs change.** Every job body in the four generated workflows was compared with `runs-on` removed (`compare_workflow_jobs.py`, `workflow_job_compare.txt`). Every job changes `runs-on` from `ubuntu-latest` to `ubuntu-24.04`. The only body changes are in rtl-fast:
  - the new `yosys-tool` job;
  - `yosys-elaboration`;
  - the `rtl-fast` summary job and `ci-manifest`, which now include `yosys-tool`;
  - `ci-fail-fast`, whose `EXPECTED_JOBS` now includes "Prepare pinned Yosys".

  `bdd-conformance`, the job that runs the plan feature, keeps its body unchanged.
- **Gitlinks.** All six submodule gitlinks are identical at the branch, at dev and at the head. They fall in the "same" class of `tree_provenance.txt`, and the head's are listed in `restore_verify.txt`.

### TESTING.md keeps both sides

- **Dev's side.** The `+/-` lines of `git diff e76a755a 97aab1d0` are byte-identical to those of `git diff a7a514fb 70b351a5` (4 lines). These are `docs/testing/TESTING.md:174` "Both target a four-core `ubuntu-24.04` hosted worker." and `:331` "…which resolved to the `ubuntu-24.04` image…".
- **The branch's side.** The `+/-` lines of `git diff e76a755a a7a514fb` are byte-identical to those of `git diff 97aab1d0 70b351a5` (454 lines, the round 1-8 section 6d work).
- Receipts: `testing_md_merge/RESULT.txt` and the four `.diff` and `.lines` pairs.
- **No semantic conflict.** The branch's 454 lines never mention a runner label. At the head, every remaining `ubuntu-latest` is either historical (run 37892515345, in TESTING `:331` and two Makefile comments) or names the refused label (`CI_WORKFLOWS.md:8-11`, `:2148-2156`, `scripts/act_ci.py`).

### (2) The head tree is the candidate tree

- `git merge-tree --write-tree 97aab1d0 a7a514fb` returns `49ecd37721ae83d0a84cd8bc22bff550836b85e0` with rc 0 and no conflict. That equals `70b351a5^{tree}` (`merge_tree_recompute.txt`).
- The head's second parent is live dev, so this tree is the current-dev candidate tree.

### (3) The round-8 grader, its claims and its gate are unaltered

- **Unchanged files.** The grader and its claims are in the ten branch-only files: `tb/tools/torture_campaign.py`, `tb/tools/torture_release_audio_mutants.py`, `tb/tools/torture_release_mutants.py`, `tests/steps/torture_audio_model.py`, `tests/steps/torture_release_steps.py`, `tests/features/torture_campaign_plan.feature`, `REQUIREMENTS.md`, `CONTRIBUTING.md`, `README.md` and `docs/design/SAVED_STATE_MATERIALIZATION.md`. Each holds the same blob at the head as at `a7a514fb`. The eleventh, TESTING.md, gained only the two runner-label lines above, both outside section 6d.
- **No dependency on the dev-changed scripts.** No module under `tests/` or `tb/tools/` imports or calls any dev-changed script: `act_ci`, `ci_events`, `ci_fast_tool_selftest`, `ci_gate_workflows`, `ci_gate_workflows_selftest`, `ci_runtime_workflows`, `ci_suite_workflows`, `ci_workflow_plan_selftest` or `yosys_shards`. The `git grep` found no match.
- **Spot-check at this head.** `behave --no-capture -f plain tests/features/torture_campaign_plan.feature` gives rc 0: 176 scenarios and 665 steps passed (`gates/behave_torture_campaign_plan.log`). That matches the 176 recorded at `a7a514fb` in the author's round-8 receipts.

## Findings

### R1 RESIDUE: Docs. The PR body's Status still names the pre-merge head and commit count

- **Where:** the PR body, `## Status`, line 23 "Green at the desk, head `a7a514fbf5572ce08394cd727c9cc9085745c79f`:" and line 30 "`396-release-gate-plan` -> `dev`: fourteen commits on dev `e76a755a`."
- **Evidence:**
  - The PR head is `70b351a5`, and `git rev-list --count --first-parent e76a755a..70b351a5` gives 15.
  - The branch now contains dev `97aab1d0` through the merge commit.
  - The desk-green statement remains true of `a7a514fb`, and the grader bytes it covered are unchanged, so no figure or claim is wrong.
- **Impact:** wording only. A cold reader is not told that the head is a merge of dev, or which dev it carries.
- **Exact fix:**
  - Change "fourteen commits on dev `e76a755a`." to "fourteen commits on dev `e76a755a`, plus a merge of dev `97aab1d0` (#784, #789) at head `70b351a5`."
  - Add after that line: "The merge changes none of this lane's files except two runner-label lines that dev brings into TESTING.md, so the desk results above, at `a7a514fb`, cover this lane's content."

### Comment-rule check

The merge adds no source comment of this lane's own. A scan of every added line in `e76a755a..97aab1d0` for bench-lane labels, `A`/`R` session IDs, `issuecomment` and "round N" found none. There is no new comment RESIDUE.

## Prior findings at this head

R699-8's findings were read in full only after this round's own pass was finished and its verdict and ledger were recorded.

| Prior finding | Status at `70b351a5` | Evidence |
|---|---|---|
| R699-8 R1 (RESIDUE): a Round 7 history sentence reads as a current bound | **Retained**, unchanged. The fix stands as written: replace "The ruling's bound, outside the scope, is that" with "The round-7 assignment's bound, outside the scope, was that". | PR body line 165 still reads "The ruling's bound, outside the scope, is that each listing falls at or after the event's first word…" |
| R699-8 S1 (SUGGESTION): pin the coverage rule's text | **Retained**, optional. The grader is byte-unchanged. | `tb/tools/torture_campaign.py:7606-7617`: the `(name, phrase)` list still carries no coverage phrase. The phrase itself is at `:3343` and `:3754-3757`. |
| R699-8 S2 (SUGGESTION): the gate test's name predates the coverage wording | **Retained**, optional. | `tb/tools/torture_campaign.py:9507` `test_audio_compositions_never_pass_and_list_every_event` |
| Earlier rounds (R699-3 to R699-7) | Resolved at `a7a514fb`, per R699-8. Their artifacts are byte-unchanged here, so they stay resolved. | `tree_provenance.txt`: every grader file is branch-only |

## Probes and gates at this head

All were run in the foreground against the exact head, and all return rc 0 (`gates/*.rc`, `gates/*.log`). The concurrent gates were driven by `run_focused_gates.sh`.

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings across 210 md files and 1421 scrubbed text files |
| `scripts/gen_toc.py --verify-anchors` | 538 cross-page fragment links reproduced |
| `scripts/gen_toc.py --check` | OK |
| `scripts/check_doc_paths.py` | rc 0 |
| `scripts/check_doc_style.py` | rc 0 |
| `scripts/check_em_dash.py --base 97aab1d0` | 0 findings over 525 added lines |
| `scripts/check_em_dash.py --base e76a755a` | 0 findings over 683 added lines |
| `scripts/ci_gate_workflows.py --check` | rc 0 (generated workflows match the templates on the merged tree) |
| `scripts/ci_events.py --check` | rc 0 |
| `scripts/check_hygiene.py --check` | rc 0 |
| `scripts/check_py_idiom.py` | rc 0 |
| behave, plan feature | 176/176 |

- **Renderer.** `gen_toc` and `check_em_dash` need the pinned Markdown renderer. It was installed from `tools/markdown/requirements.txt` with `--require-hashes` into a disposable venv under `scratch/`. The first runs under the system interpreter refused by name, as designed, and were discarded.
- **Published evidence.** The evidence tree at `9bae445a` (`review-evidence/396g-r1`) has 1684 files. All 1684 match their `published_sha256` in `MANIFEST.json`, none is missing and none is unlisted. The 82 under `author-r8/` were checked separately (`verify_evidence_manifest.py`, `evidence_all_verify.txt`, `evidence_author_r8_verify.txt`).
- **What the author receipts cover.** The author's round-8 receipts bind `a7a514fb` (`receipts/gates/head.txt`), and all 20 of their gate rc files are 0. They are source-head evidence for the lane's content, not for this merge head.
- **Signature.** The evidence commit itself carries no signature (`verification.reason=unsigned`). Integrity rests on the manifest hashes and on the commit ID named in the assignment.
- **Hosted contexts at this exact head, at the time read** (`hosted_check_runs_70b351a5.tsv`): 18 success, 13 in progress, 18 queued, and 1 skipped ("Physical gPTP (nightly and manual)", which is not run on a PR). Among the 18 that succeeded:
  - docs-check, docs-gates-0/1/2, docs-check-no-git, wire-accountability;
  - bdd-conformance, verilator-lint, Prepare pinned Yosys;
  - elaborate and its two gate legs, full-ci-gate;
  - firmware-aecp-mutants, firmware-boundary;
  - Verilator shards 8 and 11 of 17.

  Hosted and act acceptance is the manager's.
- **Restore** (`verify_restore.sh`, `restore_verify.txt`):
  - HEAD is `70b351a5`;
  - porcelain is empty, including untracked files;
  - the index equals the head tree in mode, blob and path, and the worktree equals HEAD;
  - the three initialised submodules are checked out at their gitlinks and clean;
  - the other three are not initialised, as before;
  - the `__pycache__` directories created by the probes were removed.

## Lens coverage

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The issue's part-A acceptance against the delta. `tree_provenance.txt`: no acceptance-bearing file changed (`REQUIREMENTS.md`, TESTING 6d, `AUDIO_COUNTER_LIMITS`, the assertion texts are branch-only and byte-equal to `a7a514fb`). CONTRIBUTING step 7 candidate rule: `merge_tree_recompute.txt` | R699-9 | `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2` |
| RTL | CLEAN | `tree_provenance.txt`: no `.sv`/`.v`/HDL path and no gitlink differs from either parent's corresponding side. The dev-only paths are workflows, CI scripts and READMEs. The gitlinks are equal across head, branch and dev | R699-9 | `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2` |
| Robustness | CLEAN | Semantic-merge risks in the combined tree: the `ubuntu-latest` residue scan; `workflow_job_compare.txt` (`bdd-conformance` body unchanged, only the expected `yosys-tool` wiring); `ci_gate_workflows --check` and `ci_events --check` rc 0 on the merged tree; no grader import of dev-changed scripts | R699-9 | `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2` |
| Tests | CLEAN | Grader and gate files byte-unchanged (`tree_provenance.txt`); `gates/behave_torture_campaign_plan.log` 176/176 at this head; the author's round-8 receipts hash-verified (`evidence_author_r8_verify.txt`); R699-8 S1 retained as optional | R699-9 | `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2` |
| Docs | CLEAN (R1 and R699-8 R1 are RESIDUE; S2 is optional) | `testing_md_merge/RESULT.txt` (both sides kept, `TESTING.md:174`, `:331`); `gates/docs_check.log`, `gen_toc_*.log`, `doc_paths.log`, `doc_style.log`, `em_dash_base_*.log`; the PR body Status lines 23 and 30, and line 165 | R699-9 | `70b351a5b40db3fac5e0cc18fe31d3fd96bf65b2` |

## Real limits

- **No full local bank at this head.** No full Verilator sweep, Yosys, builder, parent, PP or gPTP bank was run, and none is claimed. The release-mutation driver (298 controls) was not rerun: its inputs are byte-unchanged from `a7a514fb`, where the author's receipts record 298/298 killed.
- **No manager source bank exists at this head**, and none is inferred.
- **Physical calibration was not run.** The bench items (3 and 4, part B) are untouched, and field skips are not hardware proof.
- **Hosted contexts were partly still running** when read. Only the 18 listed as success executed to completion at that time.
- **The evidence commit is unsigned.** Integrity was checked through its manifest hashes only.
- **Reading order.** While locating manager evidence comments by searching for this head's IDs, the search printed the opening sections of the R699-6, R699-7 and R699-8 reports. That happened after this round's own delta pass and all its merge probes were complete, and the verdict and ledger were then recorded before the R699-8 findings were read in full.

## Pending manager duties

- Build and validate the current-dev candidate at the merge turn. If dev is still `97aab1d0`, that is this tree, `49ecd377`. Run the builder and native banks, and link their receipts on the PR.
- Own hosted and act acceptance at this exact head, including the contexts still queued or in progress here.
- Carry R1 and R699-8 R1 to the residue checklist.
- Obtain the external positive review, and confirm the full CONTRIBUTING bar before any authorized merge.
- Run post-merge containment and the integrity checks.

## Receipts

Listed in `MANIFEST.sha256`, with paths relative to the packet root. They are the scripts (`check_tree_provenance.sh`, `compare_workflow_jobs.py`, `run_focused_gates.sh`, `verify_evidence_manifest.py`, `verify_restore.sh`), the provenance and comparison outputs, `testing_md_merge/`, `gates/`, the hosted snapshot, the live dev tip, the evidence verification and the restore check.

R699-9 FINISHED
