[R725] POSITIVE - exact head 0a9f398b699da726e1d9244e3a4d9c44478889f8

# R725-6: composition review of the merge-train candidate for PR #802 (issues #799, #790)

Candidate `0a9f398b699da726e1d9244e3a4d9c44478889f8`, tree `5795b6769b96c1e99e4bce47c83d5fdb11dc2e57`. This round reviews composition acceptance only. The PR source head `865c2f9d82f2394b3453f36ccf92c49317a7fddd` was reviewed at source level (see "Source reviews relied on").

**Verdict: POSITIVE.** The composed tree introduces no defect beyond the reviewed sources.

- The candidate is a two-parent merge: live dev `5fcec84b` and PR head `865c2f9d`. `git merge-tree --write-tree` of those two parents reproduces tree `5795b676` exactly, with no conflicts, and the merge commit adds no edits of its own.
- The only predecessor in the candidate is dev's move from the PR's source base `97aab1d0` to `5fcec84b`, which is PR #786 (#396 release gate plan). Three files are changed on both sides, and in every one the hunks are disjoint and far apart.
- Every gate that reads those files returns rc 0 on the candidate (reviewer-run). This includes the whole behave suite, which runs both sides' feature and step changes together.
- The signed local-CI packet verifies: the key fingerprint is right, the signature is good, the subject names this candidate and head, and all 47 coverage entries are `ok`.
- No new finding. Of the prior items: RES-A and RES-B are closed in the PR body. RES-C, RES-D and R3/RES-1 are retained as residue. S5 is a closed suggestion, with no gate row added. One new optional SUGGESTION (S6).

## Composition scope (`receipts/composition.txt`, `receipts/pr_files.txt`, `receipts/dev_files.txt`)

- Parents: `5fcec84b1aa72c43048eff28bb63a982add830dd` (dev) and `865c2f9d82f2394b3453f36ccf92c49317a7fddd` (PR head). Their merge-base is `97aab1d0`, the PR's source base.
- Predecessor delta `97aab1d0..5fcec84b` (PR #786, 16 commits) changes 11 files. The PR changes 61.
- **Files changed on both sides.** Line numbers below are in the candidate.

| File | Dev (#786) hunks | PR hunks | Interaction |
|---|---|---|---|
| `docs/testing/TESTING.md` | from `:1022` on (release soak, audio and power plan) | `:275`, `:405-417`, `:544-557` (gsi-mutants row, milan_dp command list, sidmove scratch, 19-worker paragraph) | Disjoint sections. The TOC and anchors regenerate clean, and docs_check, doc style and em dash pass |
| `tb/tools/torture_campaign.py` | release settings, asserts, oracles, plan_soak/power/audio and their self-tests (base lines 135-3915) | `:2649-2682` (`_torture_maap_steps` clause text and one added AssertSpec) | Disjoint. Dev does not touch the MAAP entry, and the PR does not touch release code. All 377 release and audio mutant anchors occur the same number of times in dev's copy and in the candidate's copy. The planner self-test passes |
| `tests/features/torture_campaign_plan.feature` | from `:304` on (release scenarios, first at `:311`) | `:241-250` (MAAP conflict scenario) | Disjoint. The PR's two new steps live in `tests/steps/torture_plan_steps.py` and dev's in `tests/steps/torture_release_steps.py`. The full behave run has no ambiguous or undefined step |

- `git diff --stat 865c2f9d HEAD` over the PR's files shows only those three files. Their line counts (454, 4419, 262) equal dev's own diffstat for them, so the candidate carries the PR's hunks unchanged.
- **Semantic interactions checked:**
  - Dev changed `CONTRIBUTING.md`, `README.md`, `REQUIREMENTS.md` (REQ-VER-05, REQ-VER-06 wording) and `docs/design/SAVED_STATE_MATERIALIZATION.md`. No file the PR changes cites the old soak figures. A grep for "seven continuous days", "604800" and "160 idle" over the PR's files finds only dev's own self-test row in `torture_campaign.py` (and, outside the PR's files, dev's mutants).
  - Dev touched no workflow, generator, suite inventory, shard planner, budget file or registry. So the PR's 19-worker workflow, `ci_events` contract, planner figures and `rtl.yml` hash do not depend on the predecessor.
  - The workflow definitions in the signed manifest (`definitions.candidate` and `definitions.head`) are byte-identical, and equal `sha256sum .github/workflows/*.yml` in this clone.
  - Repository-wide ratchets (Python idiom, naming, fail-fast, test evidence, hygiene, TODO ownership) measure both sides together and all pass.
- **Comment rule:** the merge adds no line of its own, so the composition delta has no new instance. The PR-side comment lines were scanned by the source rounds.

## Gates run on the candidate (reviewer-run, this clone, each rc the command's own)

Scripts: `scripts/composition_gates.sh` and `scripts/composition_gates_2.sh`. The pinned Markdown renderer (`tools/markdown/requirements.txt`, `--require-hashes`) was installed into a private venv under `scratch/`.

| Gate | Result | Receipt |
|---|---|---|
| `cd tests && behave --no-capture -f plain` (the workflow's step) | rc 0: 14 features, 495 scenarios, 2288 steps passed, 0 failed, 0 skipped | `receipts/gates2/behave_full.*` |
| `torture_campaign.py --self-test` | rc 0: 120 tests OK | `receipts/gates/torture_selftest.*` |
| `torture_release_audio_mutants.py` | rc 0 (prints nothing) | `receipts/gates/torture_audio_mut.*` |
| Mutant anchor invariance (`scripts/mutant_anchor_counts.py`) | 377 anchors, 0 differ between dev's planner and the candidate's | `receipts/gates2/mutant_anchor_counts.log` |
| `docs_check.py` (with and without venv) | rc 0: 0 findings across 210 md files and 1423 scrubbed text files | `receipts/gates/docs_check.*`, `receipts/gates2/docs_check_venv.*` |
| `gen_toc.py --selftest`, `--verify-anchors`, `--check` | rc 0: 1501/1501 arms; 541 cross-page anchors; 149 pages | `receipts/gates2/gen_toc.*` |
| `check_em_dash.py --base 5fcec84b` (candidate parent) | rc 0: 0 findings over 401 added lines in 18 pages | `receipts/gates2/em_dash_vs_dev.*` |
| `check_em_dash.py --base 97aab1d0` (merge-base) | rc 0: 0 findings over 926 added lines in 22 pages | `receipts/gates2/em_dash_vs_mergebase.*` |
| `check_doc_style.py` and `--selftest`; `check_doc_paths.py`; `check_solution_docs.py`; `DOC_MAP.gen.py --check`; `gen_module_matrix.py --check` | rc 0 each (1071 cited paths resolve) | `receipts/gates/` |
| `check_feature_status.py` and `--self-test` | rc 0: 0 findings; 46/46 | `receipts/gates/feature_status.*` |
| `ci_events.py --check` and `--selftest` | rc 0: 2199 items, 5258 arms | `receipts/gates/ci_events.*` |
| `ci_gate_workflows.py --check`; `suite_shards.py --selftest` | rc 0, rc 0 | `receipts/gates/` |
| `check_py_idiom.py`; `measure_naming.py --check`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check`; `check_hygiene.py --check`; `check_todo_ownership.py` | rc 0 each | `receipts/gates/` |

The first pass ran behave from the repository root, where it found no steps directory, and ran `gen_toc` and the em-dash gate without the renderer. Those runs were discarded and re-run correctly in `gates2`. They were runner errors, not findings.

## Signed local CI (`receipts/signed/`)

- Downloaded read-only from `review-evidence/799-r1/local-ci/865c2f9d` at `66c8c938`. `manifest.json` sha256 is `73398d068d7ae39bb9e987ae51bbdc22e889d4abe90ca35f39abaf3d67c00091`, as stated.
- (1) `allowed_signers` holds one key, principal `milan-local-ci`, namespace `milan-local-ci`, ED25519 `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. This matches; there is no other key.
- (2) `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` returns `Good "milan-local-ci" signature ... SHA256:dRI12tvJ...`, rc 0.
- (3) The subject is PR 802, candidate `0a9f398b...` with tree `5795b676...`, candidate parent `5fcec84b`, and head `865c2f9d...` with tree `04f84471...`. The result is `success`.
  - 47 coverage entries: 46 by act, 1 not-run (`rtl/physical-gptp`, which runs on schedule and dispatch only, with its reason stated). All 47 are `ok: true`.
  - Every one of the 47 workflow job ids in the four candidate workflows has an entry.
  - 68 act jobs: 67 success, 1 skipped (physical gPTP). The banks are `full-native` (5 commands) and `manager-builder` (48 commands), every exit code 0.
- Note: act replayed the PR head, not the candidate. The banks ran the candidate. The composed behave and torture gates are therefore independently confirmed by this round's runs above.

## Hosted evidence at the PR head (read only; manager owns acceptance)

`receipts/hosted_checkruns_865c2f9d.txt`: 67 check runs succeeded, including `rtl-fast`, `bdd-conformance`, `docs-check`, `verilator-suites` and `yosys-portability`. The one skipped run is `Physical gPTP (nightly and manual)`. This is the PR head, not the candidate. No hosted run exists for the candidate, and none is claimed.

## Prior public findings at this head

| ID | Source round | Status at `0a9f398b` |
|---|---|---|
| F1 (MINOR, Docs) | R725-4 | Closed in R725-5. The candidate keeps `CI_WORKFLOWS.md` byte-identical to the PR head |
| R1, R2 (RESIDUE) | R725-4 | Closed in R725-5. The files are unchanged by composition |
| RES-A (RESIDUE, Docs, PR body expected head) | R725-5 | **Closed**: PR body line 177 now names `865c2f9d82f2394b3453f36ccf92c49317a7fddd`, matching "Status" (line 16) |
| RES-B (RESIDUE, Docs, PR body "row below") | R725-5 | **Closed**: PR body line 141 reads "as the `ca39dc1b` row above" |
| RES-C (RESIDUE, Docs, `scripts/suite_shards.py:76`) | R725-5 | **Retained**: still "except media_phase," without `milan_dp_gm_steps`. Exact fix as in R725-5: `#: #799: the ruled replay set (see CI_WORKFLOWS.md), except media_phase and milan_dp_gm_steps, carries its` |
| RES-D (RESIDUE, Docs, `docs/testing/CI_WORKFLOWS.md:483`) | R725-5 | **Retained**: still "a source this PR changes". Fix: "a source the adoption changes" |
| R3 / RES-1 (RESIDUE, Docs, `sw/mailbox/mailbox.yaml:65`) | R725-3, R726-2 | **Retained**: the line is still 105 columns. Fix: reflow that comment line to the file's column limit |
| S5 (SUGGESTION) | R725-5 | Optional. No `865c2f9d` gate row was added. Not required |

None of these is touched by the composition. All three retained items are wording only and belong to the residue checklist.

## Findings (this round)

None. No BLOCKER, MAJOR, MINOR or new RESIDUE. One SUGGESTION:

### S6 - SUGGESTION - Tests - `receipts/signed/manifest.json`, `execution.act` and `execution.banks` - act ran the head, and the bank commands are hashes only

- **Evidence:** the manifest's act section replays `865c2f9d`. The candidate is covered only through the banks, whose commands are recorded as argv hashes, so a reader cannot tell from the packet which gates ran on the composed tree.
- **Impact:** none here. This round's composed gate runs fill that gap for PR #802.
- **Suggestion (optional):** for candidates whose predecessor changes files the PR also changes, record readable bank command names beside their hashes.
- **Verification:** a later manifest lists named bank commands.

## Lenses applied this round

| Lens | Composition touches scope? | Result | Evidence |
|---|---|---|---|
| Conformance | Yes, partly: both sides edit `tb/tools/torture_campaign.py`, which carries clause claims (Milan Table 5.3 / IEEE 802.1Q 35.2.2.8 on the PR side; REQ-VER-06 release criteria on the dev side) | PASS | The PR's MAAP entry `torture_campaign.py:2649-2682` is carried unchanged, and dev's hunks avoid it (`receipts/composition.txt`). Dev's REQUIREMENTS and CONTRIBUTING wording conflicts with no PR file (grep above). The behave MAAP and release scenarios pass (`receipts/gates2/behave_full.log`) |
| RTL | No: the predecessor touches no `hdl/`, `tb/verilator/`, `syn/`, workflow or gitlink (`receipts/dev_files.txt`) | PASS, covered by source reviews | `receipts/dev_files.txt`; merge-tree replay equals the candidate tree; R725-5 at `865c2f9d` (carrying R725-3 and R726-2 RTL coverage at `4f3ebffb`, re-banked by R725-4 at `9e57d4af`) |
| Robustness | Yes, partly: release negative controls and the planner self-test share `torture_campaign.py` with the PR's edit | PASS | 377 mutant anchors invariant (`receipts/gates2/mutant_anchor_counts.log`); `--self-test` 120 OK; audio mutants rc 0 (`receipts/gates/`) |
| Tests | Yes: `tests/features/torture_campaign_plan.feature` is edited on both sides, and the step files sit side by side | PASS | Full behave: 495 scenarios pass, no ambiguous or undefined step; feature-status gate 0 findings; test-evidence ratchet rc 0; signed manifest coverage all `ok` (`receipts/gates2/behave_full.log`, `receipts/gates/`, `receipts/signed/`) |
| Docs | Yes: `docs/testing/TESTING.md` is edited on both sides, and dev edits CONTRIBUTING, README and REQUIREMENTS | PASS | `TESTING.md:275, 405-417, 544-557` against `:1022` on; `gen_toc --check/--verify-anchors`, `docs_check`, `check_doc_style`, `check_doc_paths` and `check_em_dash` (both bases) all rc 0 (`receipts/gates*/`); the PR body was re-read for RES-A and RES-B |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `tb/tools/torture_campaign.py:2649-2682` and dev hunks (`receipts/composition.txt`); dev `REQUIREMENTS.md` and `CONTRIBUTING.md` diff; `receipts/gates2/behave_full.log` | R725-6 (composition); source: R725-5 | `0a9f398b699da726e1d9244e3a4d9c44478889f8` (source: `865c2f9d82f2394b3453f36ccf92c49317a7fddd`) |
| RTL | CLEAN | `receipts/dev_files.txt` (no RTL in predecessor); `receipts/composition.txt` (merge-tree replay = candidate tree) | R725-5 (source; composition does not touch scope) | `865c2f9d82f2394b3453f36ccf92c49317a7fddd`, a parent of the candidate; no RTL change enters through the other parent |
| Robustness | CLEAN | `receipts/gates2/mutant_anchor_counts.log`; `receipts/gates/torture_selftest.log`, `torture_audio_mut.*` | R725-6 | `0a9f398b699da726e1d9244e3a4d9c44478889f8` |
| Tests | CLEAN | `tests/features/torture_campaign_plan.feature:241-250` beside `:304` on; `tests/steps/torture_plan_steps.py`, `tests/steps/torture_release_steps.py`; `receipts/gates2/behave_full.log`; `receipts/gates/feature_status.*`, `test_evidence.*`; `receipts/signed/manifest.json` | R725-6 | `0a9f398b699da726e1d9244e3a4d9c44478889f8` |
| Docs | CLEAN (RES-C, RES-D, R3/RES-1 residue retained) | `docs/testing/TESTING.md` both hunk sets; `receipts/gates2/gen_toc.log`, `em_dash_*.log`, `docs_check_venv.log`; `receipts/gates/doc_style.*`, `doc_paths.*`; PR #802 body lines 16, 141, 177 | R725-6 | `0a9f398b699da726e1d9244e3a4d9c44478889f8` |

## Source reviews relied on

- R725-5 POSITIVE at `865c2f9d82f2394b3453f36ccf92c49317a7fddd`, in the PR #802 thread.
- R726-2 POSITIVE at `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020`, in the PR #802 thread. The delta from there to `865c2f9d` (CI schedule, CI docs, planner comments) was reviewed by R725-4 (NEGATIVE, F1) and R725-5 (POSITIVE).
- In the public PR thread I found no second-reviewer verdict spelled at `865c2f9d` itself. See pending manager duties.

## Real limits

- `tb/tools/torture_release_mutants.py` (the dev-owned release mutant driver) did not finish inside a 10-minute foreground window, and it was stopped. No result is claimed for it.
  - Instead, this round shows that none of its 377 anchors changed occurrence count under the PR's edit, and that its oracle, the planner self-test, passes on the candidate.
  - Whether the manager's bank runs the full driver cannot be read from the argv hashes.
- No Verilator suite, Yosys run, builder leg or firmware gate was run here. The predecessor changes none of their inputs, and the signed banks and act cover them.
- No hosted run exists for the candidate. The hosted results quoted are at the PR head.
- Bank command contents are known only as argv hashes. The claim that the banks ran the candidate rests on the signed manifest.
- Physical calibration NOT RUN; field skips are not hardware proof. No manager source bank at the PR head is claimed.

## Pending manager duties

- Merge-turn validation against live dev, if dev moves past `5fcec84b` before the merge.
- Confirm the two-positive review bar at `865c2f9d` with `scripts/check_merge_review_integrity.py`, since the second source positive (R726-2) is at ancestor `4f3ebffb`.
- Carry RES-C, RES-D and R3/RES-1 to the residue checklist.
- Confirm that the release mutant driver ran to completion on the candidate in a bank, or run it.
- Explicit maintainer authorization before any merge.

## Restore (`receipts/restore_verify.txt`)

- HEAD is `0a9f398b`, tree `5795b676`.
- 0 porcelain lines including ignored files. The `__pycache__` directories the gates created were removed with `git clean -fdX` after a dry-run listing.
- The index digest equals the HEAD-tree digest, the worktree equals HEAD, and the index equals HEAD.
- Gitlinks: processor `f65c8ff7`, gPTP `55680bff`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, external `efeb541a` (not initialised).

R725-6 FINISHED
