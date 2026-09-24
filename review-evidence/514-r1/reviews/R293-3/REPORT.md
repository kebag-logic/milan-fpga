[R293] POSITIVE - exact head 177867daf3b35ba41b8c51f8c35c8509643dda22

# R293-3: composition review of issue #514 / PR #552 (merge-train candidate)

- **Candidate:** `177867daf3b35ba41b8c51f8c35c8509643dda22`, tree `384b3fe2060fb462ffb893a266ddf3b6cc7b6dc1`.
- **Parents:** `cf43b4716772582d0c77d40f1eeac5934a0cd9da` (the predecessor merge-train tip, "Validate issue 539 merge-train candidate") and `b0347a4fd668f8d40bdf40a142ac0ea70167acd1` (the PR source head).
- **Scope:** composition acceptance only. The source head already has two independent POSITIVE reviews: R292-2 (PR comment 5812395206) and R293-2 (PR comment 5812554984).
- **Verdict meaning:** POSITIVE means the composed tree introduces no defect beyond the reviewed sources.

I reconstructed this round in a cleared context from public material only. I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The #514 body and its manager decisions: DECISION 5789750055, ASSIGNMENT 5810682208 and ROUND-2 ASSIGNMENT 5812011094.
4. REQ-VER-04 and CONTRIBUTING 2.1 step 7.
5. The raw diff `cf43b471..177867da` and the history.

I read the prior public review rounds on PR #552 only after my own pass over the diff and gates was complete.

## Composition facts (receipts/blob_identity.txt)

- **The candidate is the plain mechanical merge.** `git merge-tree --write-tree cf43b471 b0347a4f` gives `384b3fe2…`, which is the candidate tree. No hand resolution is present.
- **Fork point:** the PR source forked from dev `3d2f3e3131c9db5898e1db9dd3e2a35149843109`, which is `merge-base(cf43b471, b0347a4f)`.
- **The PR changes 8 paths since the fork point:**
  - `AGENTS.md`, `CONTRIBUTING.md`, `docs/testing/CI_WORKFLOWS.md`, `docs/testing/RUNNING_TESTS.md`;
  - `scripts/check_merge_containment.py`, `scripts/merge_containment_replay.py`, `scripts/merge_containment_selftest.py`;
  - `scripts/merge_containment_selftest_linear.py` (added).
- **The predecessors change 52 paths since the fork point.** They merged #117, #387, #394/#510/#511, #536, #437, #542, #530 and #539.
- **Files changed on both sides:** exactly two, `CONTRIBUTING.md` and `docs/testing/RUNNING_TESTS.md`.
  - Their hunks do not overlap.
    - Predecessor text at the candidate: CONTRIBUTING.md:610-663 (the Contents/renderer rules) and RUNNING_TESTS.md:134-140 (installing the renderer lock).
    - PR text: CONTRIBUTING.md:207-273 (2.1 step 7) and RUNNING_TESTS.md:76-80.
  - The composed hunk bodies `cf43b471→177867da` are byte-identical to the PR's own hunk bodies `3d2f3e31→b0347a4f` (`SAME-HUNKS` for both files).
  - The first 300 lines of CONTRIBUTING.md and the first 110 of RUNNING_TESTS.md are byte-identical at source head and candidate, so every source-review line citation still holds (receipts/suggestion_lines.txt).
- **Blob identity.** The other 6 PR paths are blob-identical at source head and candidate. All 50 predecessor-only paths are identical at parent and candidate (one of them, `scripts/gen_toc_guards.py`, is absent in both). The candidate changes no path outside the PR set relative to its parent.
- **Gitlinks at the candidate equal the parent's:**
  - `external` efeb541a;
  - `gptp-processor` e5dcea6e;
  - `protocol-processor` 09f9bf38 (moved by a predecessor, not by this PR);
  - `third_party/verilog-axis` 48ff7a7e.

### Semantic interactions examined

- **Containment checker and self-test.** Every module in the import closure is blob-identical to the source head: `check_merge_containment.py`, `merge_containment_replay.py`, `merge_containment_git.py` and every `merge_containment_selftest*.py`. No predecessor touched one of them.
  - I ran `--selftest` on `git archive` extractions of both commits. Each gives 799 case lines, 799 `ok`, exit 0, and the case lines are identical (receipts/parity/).
  - Its callers are unchanged on both sides: `scripts/run_all_suites.sh:307` and `scripts/test_suite_cancellation.py:90,361`.
- **Markdown renderer.** The predecessors (#437/#516) made `gen_toc.py` and `check_em_dash.py` read Markdown through the hash-locked cmark-gfm and html5lib pair. So the PR's Markdown, including a fenced block and a table inside CONTRIBUTING 2.1 step 7, is judged here for the first time by the new renderer.
  - All TOC, anchor and em-dash gates pass under the pinned lock.
  - The renderer finds no heading inside step 7, lines 210-273 (receipts/anchor_probe.txt).
  - The two new cross-page links `../../CONTRIBUTING.md#21-the-issue-to-merge-lane` resolve (the anchor is derived by `gen_toc.headings`).
- **CI workflow and record pins.** The predecessors changed `.github/workflows/docs.yml` (renderer install steps) and `scripts/ci_events.py` (docs-check step count 47→49). The PR changed `docs/testing/CI_WORKFLOWS.md`, which `ci_events.py --check` reads.
  - `ci_events.py --check` passes: 1647 contract items across 4 workflows and CI_WORKFLOWS.md.
  - `--selftest` passes: 2188 arms.
  - No workflow, record or pin names a containment script.
- **Test-evidence inventory.** The predecessors changed `measure_test_evidence.py` (a new disposition). The PR adds `merge_containment_selftest_linear.py`. `measure_test_evidence.py --check` passes on the composed tree.
- **Checker on the composed history.** In a disposable clone, the default checker gives `contained … [historical inclusion by ancestry; current retention not implied]`, exit 0 (receipts/smoke_candidate_containment.txt).
  - With `--current-retention` it adds `UNKNOWN … unsupported: needs a nonempty whitespace-exact linear replay`, exit 1.
  - This is the documented exclusion of ancestry-only proofs (CONTRIBUTING.md:226-228), not a regression. The default post-merge gate does not pass the option.

## Gates run on the candidate (receipts/gates/, all exit 0)

The Python used is 3.14.7 with the tools/markdown lock installed `--require-hashes` (cmarkgfm 2025.10.22, html5lib 1.1) plus PyYAML 6.0.3. Git is 2.55.0.

| Gate | Result |
|---|---|
| `docs_check.py` / `GIT_DIR=/dev/null docs_check.py` | 0 findings, 165 md files (both discovery modes) |
| `check_em_dash.py --base cf43b471` (parent) | 0 findings over 52 added lines in 4 pages, 339/339 arms |
| `check_em_dash.py --base 3d2f3e31` (PR fork point) | 0 findings over 432 added lines in 19 pages |
| `check_em_dash.py --selftest` | PASS, 339 arms |
| `check_doc_style.py` and `--selftest` | OK (22 current documents); selftest OK |
| `gen_toc.py --check` / `--verify-anchors` / `--selftest` | OK (107 pages); 165 cross-page fragments reproduced; 1501/1501 |
| `check_doc_paths.py` | OK, 841 cited paths resolve |
| `check_py_idiom.py` and `--selftest` | 0 across all counters; 54/54 |
| `check_hygiene.py --check`, `check_todo_ownership.py` | PASS; OK |
| `measure_test_evidence.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check` | PASS; PASS; PASS |
| `check_feature_status.py` | 0 findings |
| `ci_events.py --check` / `--selftest` | OK (1647 items); PASS (2188 arms) |
| `check_merge_containment.py --selftest` | PASS, 799/799 `ok` |
| `git diff --check cf43b471 HEAD` | clean |

In a first run, the two `ci_events.py` commands exited 2 with `pyyaml is not importable`. That was a missing dependency in my environment, not a defect: the docs workflow installs pyyaml before them. Both pass once it is installed. The first run's logs were replaced by the final run.

## Findings

This round raises no BLOCKER, MAJOR, MINOR or SUGGESTION finding. The composition introduces nothing beyond the reviewed source.

## Per-lens results at 177867da

- **[R293] PASS Conformance.** Artifacts: CONTRIBUTING.md:207-273 at the candidate; receipts/blob_identity.txt (SAME-HUNKS); receipts/parity/SUMMARY.txt; receipts/smoke_candidate_containment.txt.
  - Checked against the #514 DECISION (5789750055) and acceptance items 1-5 as the source reviews verified them.
  - The contract text of 2.1 step 7 composes without alteration.
  - The checker's code and every expectation are byte-identical to the source head, and its verdict wording on the composed history matches the documented claims.
  - The composition touches this lens's scope through the two shared documents. I applied the lens and found nothing.
- **[R293] PASS RTL.** Artifacts: receipts/blob_identity.txt (the `cf43b471..177867da` path set and the gitlink list); `scripts/run_all_suites.sh:307`.
  - The candidate differs from its parent only in the PR's 8 paths. None is HDL, a constraint, tcl or a gitlink, and all four gitlinks equal the parent's.
  - The composition does not touch this lens's scope. For the PR's own artifacts it is covered by the source reviews R292-2 and R293-2 at `b0347a4f`.
  - The predecessor RTL present at the parent belongs to those predecessors' lanes.
- **[R293] PASS Robustness.** Artifacts: receipts/smoke_candidate_containment.txt; receipts/parity/; `scripts/check_merge_containment.py` (blob `141baec9…`, identical at source head and candidate).
  - The option fails closed on the composed merge-shaped history (`UNKNOWN`, exit 1) and leaves the default verdict and exit unchanged.
  - The failure paths are unchanged: without the renderer lock the docs gates refuse with rc 2 (predecessor behaviour), and `ci_events` refuses by name without pyyaml.
  - The composition adds no input or state path to the checker. The source rounds' probe matrices therefore still apply.
- **[R293] PASS Tests.** Artifacts: receipts/parity/cases-*.txt (799 identical case lines); receipts/gates/containment_selftest.log; receipts/gates/test_evidence_check.log; `scripts/test_suite_cancellation.py:90,361`.
  - The self-test modules are blob-identical to the source head, the case output is identical, and the runner and cancellation wiring are unchanged on both sides.
  - The test-evidence inventory accepts the new self-test file on the composed tree.
  - The composition does not change what any test proves. Mutation coverage is the source rounds' (R292-2, R293-2), and I did not repeat it.
- **[R293] PASS Docs.** Artifacts:
  - CONTRIBUTING.md:207-273 and :610-663;
  - docs/testing/RUNNING_TESTS.md:70-80 and :134-140;
  - docs/testing/CI_WORKFLOWS.md:1754-1760;
  - AGENTS.md:416;
  - receipts/gates/ (docs_check both modes, em-dash vs parent and fork point, doc style, TOC check/anchors/selftest, doc paths, ci_events);
  - receipts/anchor_probe.txt.

  The two shared pages carry both sides' text, and each block reads correctly in its composed context. The new cross-page anchors resolve under the pinned renderer, and no heading or Contents entry changed. The composition touches this lens's scope, and I applied the lens.

## Reviewer-owned completion ledger

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | CONTRIBUTING.md:207-273; SAME-HUNKS composition proof; 799-case parity; checker run on the composed history | R293-3 (composition). Source coverage: R292-2, R293-2 at b0347a4f | 177867daf3b35ba41b8c51f8c35c8509643dda22 |
| RTL | CLEAN | parent..candidate path set (no HDL, constraint, tcl or gitlink change); gitlinks equal parent; run_all_suites.sh:307 | Composition does not touch it (verified by R293-3). Covered by source reviews R292-2 and R293-2 at b0347a4f | 177867daf3b35ba41b8c51f8c35c8509643dda22 (R293-3 inapplicability); b0347a4fd668f8d40bdf40a142ac0ea70167acd1 (source) |
| Robustness | CLEAN | Composed-history checker run (default and option); unchanged checker blob; gate refusal paths | R293-3. Source coverage: R292-2, R293-2 at b0347a4f | 177867daf3b35ba41b8c51f8c35c8509643dda22 |
| Tests | CLEAN | Self-test parity (799 = 799, identical lines); test-evidence inventory; runner and cancellation wiring | R293-3. Mutation coverage: R292-2, R293-2 at b0347a4f | 177867daf3b35ba41b8c51f8c35c8509643dda22 |
| Docs | CLEAN | Both shared pages composed; the docs, TOC, anchor, em-dash, style, path and ci_events gates in receipts/gates (all exit 0); anchor probe | R293-3 | 177867daf3b35ba41b8c51f8c35c8509643dda22 |

Open at this head: SUGGESTION only (the retained prior S1-S4 below). None affects coverage.

## Prior public findings on PR #552 (read after the pass above)

| Prior finding | Disposition at 177867da |
|---|---|
| R292-1 F1 / R293-1 F1 MINOR `Tests` | Resolved at b0347a4f by R292-2 and R293-2. The resolving cases (`linear-empty-delta`, `linear-H-measurement-failure`, `linear-H-failure-diagnostic`) run and pass at the candidate (receipts/gates/containment_selftest.log). **Resolved.** |
| R292-1 F2 / R293-1 F2 MINOR `Tests` | Resolved at b0347a4f. The pinning cases are present and pass at the candidate. **Resolved.** |
| R292-1 S1 / R293-1 S2 SUGGESTION `Robustness` (`check_merge_containment.py:948-949`, `--base --current-retention` parsing) | The blob is identical and the line numbers unchanged. **Retained, optional.** |
| R292-1 S2 / R293-1 S1 SUGGESTION `Docs` (CONTRIBUTING.md:219 and :222-231, sweep `UNKNOWN` for merge-shaped landings) | The text and line numbers are unchanged. The composed-history run above is a live instance of that expected `UNKNOWN`. **Retained, optional.** |
| R292-1 S3 / R293-1 S3 SUGGESTION `Docs` (RUNNING_TESTS.md:76, "It" antecedent) | The text and line are unchanged. **Retained, optional.** |
| R292-2 S4 / R293-2 S4 SUGGESTION `Tests` (`check_merge_containment.py:884-887`, pre-error branch unpinned under the option) | The blob is identical. **Retained, optional.** |

## Real limits

- **No hosted evidence for the candidate.** The candidate is not on the remote (the API answers "No commit found"), so it has no hosted run.
  - Hosted runs exist for the source head `b0347a4f` only (receipts/hosted-check-runs-source-head.tsv): 21 completed `success`, including rtl-fast, docs-check, docs-check-no-git, full-ci-gate, verilator-suites (shards 0-4/5), yosys-portability (shards 0-3/4) and bdd-conformance.
  - "Physical gPTP (nightly and manual)" was `skipped`. A skip is not hardware evidence.
  - I inspected these runs; I did not accept them.
- **Live dev is not in this candidate.** Live dev `eaf0e6c4` is not an ancestor of the candidate parent `cf43b471`, so this is not the final current-dev candidate.
  - For information only (receipts/live_dev_informational.txt), in a disposable clone: live dev also changed `CONTRIBUTING.md` and `docs/testing/RUNNING_TESTS.md` since the fork point, and `git merge-tree eaf0e6c4 b0347a4f` merges without conflict.
  - I did not gate that tree.
- **Manager bank evidence was not found.** I did not locate receipts for the manager's source static, builder and native banks under `review-evidence/514-r1` at `7a00fd14` (it holds author and reviewer packets), nor in issue or PR comments. This round does not rely on them.
- **Not run:**
  - full parent, protocol-processor, gPTP, Yosys or builder banks;
  - Docker/act, host act_ci or its self-test;
  - hardware. Physical calibration is NOT RUN.
  - I did not repeat the mutation campaigns; the source rounds own them.
- **Scoped Verilator not used.** The scoped Verilator binary was not needed, so I did not identity-check it.
- **Environment.** The renderer lock and PyYAML were installed only into a private virtual environment under this packet's `scratch/`. PyYAML is unpinned, as in the docs workflow.
- **Clone restored and verified** (receipts/clone-integrity.txt, all OK):
  - HEAD and HEAD tree are exact;
  - index modes and OIDs equal the HEAD tree, and tracked bytes equal the index;
  - porcelain status, including ignored files, is empty. The gates' `scripts/__pycache__` was removed.
  - All four gitlinks equal HEAD: `external` efeb541a, `gptp-processor` e5dcea6e, `protocol-processor` 09f9bf38, `third_party/verilog-axis` 48ff7a7e.

  Every probe that runs code ran on `git archive` extractions or a disposable clone under `scratch/`.

## Pending manager duties

- Publish this report.
- Build and gate the final current-dev candidate: source base `3d2f3e31` (the source head's fork point), live dev `eaf0e6c4`, plus the queued predecessors. That includes the two shared documents against live dev's own edits to them.
- Hosted and act acceptance at the exact merge head.
- Maintainer merge authorization, post-merge containment, and closing #514 and moving it to Done.
- Optional: dispose of S1-S4.

## Reproduction (scripts in this packet)

- `bash blob_identity.sh <clone>` → receipts/blob_identity.txt
- `bash run_composition_gates.sh <clone> <python-with-lock-and-pyyaml> receipts/gates`
- `python anchor_probe.py <clone>` (with the lock installed) → receipts/anchor_probe.txt
- `bash selftest_parity.sh <clone> <python> <scratch> receipts/parity`
- `bash smoke_containment.sh <clone> <python> <scratch>` → receipts/smoke_candidate_containment.txt
- `bash clone_integrity.sh <clone>` → receipts/clone-integrity.txt
- Install the lock with `python -m pip install --require-hashes -r tools/markdown/requirements.txt`, then `python -m pip install pyyaml`, into a private virtual environment.

R293-3 FINISHED
