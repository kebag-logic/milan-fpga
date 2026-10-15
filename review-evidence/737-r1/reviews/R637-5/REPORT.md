[R637] NEGATIVE - exact head e3d25d964b5bbf0187290d0a357c6a6e4c5afd17

External independent review R637-5 of issue #737 / PR #739. This is a merge-only delta review of round 5, `08adb21a..e3d25d96`: merge commit `8db58305` (parents `08adb21a` and dev `f6260253`) and the re-projection commit `e3d25d96`. Tree `8c2bed598eee7447fe8b93158932407301f92a0a`. My round-4 verdict at `08adb21a` was POSITIVE. Code the delta does not touch keeps that verdict, except where the delta changes what the code depends on.

## Summary

- **All five named merge checks hold.** I proved each one independently (see "Assignment checks").
  - The three conflicts keep both sides' facts.
  - `gptp_tables` enters the driver-derived inventory and the collector proof at 568 s. I re-measured that window from the hosted log as 567.745 s.
  - The workflows are generator output only, and dev's six `rtl.yml` edits sit in the template byte-for-byte.
  - The generator refuses every template mismatch I planted (7 of 7).
  - All sixteen projected rows reproduce exactly. Worker 3 is at 1544 s, and every worker is within its own bound.
  - `scripts/act_ci.py` is unchanged: SHA-256 `f968f676…895c`, same blob.
- **Two MINOR findings make the verdict NEGATIVE.**
  - **F1 (Conformance, Docs).** The merge brings in dev's #671 (#715) workload. That workload invalidates the authoritative docs and elaboration projections in `CI_WORKFLOWS.md`. At the merge head, the document's own method puts the docs workflow at about 31.2 minutes, which is over the 30-minute acceptance. The document still says 29.6. The author disclosed this as an open risk, but no decision is recorded.
  - **F2 (Tests).** The generator's new derivation and its two refusals have no committed test. With the round-4 generator restored, all 18 committed scheduling and contract gates still pass, even though the generated graph regresses.
- **Two RESIDUE items:**
  - **R1.** The stale publication sentence in the PR body is still there. This retains R637-4-R1 and R636-4-R1.
  - **R2.** The phrase "whose suites all passed" is ambiguous.

## Scope and reconstruction

I read the following, in this order:

1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. The issue #737 body, including its scope change of 2026-10-14 (comment 6166823105). That change replaced acceptance items 1 and 3. Item 1 now reads: "every workflow it runs finishes in at most 30 min".
3. The round-5 ruling (6184143571) and the author's READY comment (6187136845).
4. Then the diff and its history:
   - `git show --cc 8db58305`;
   - per-file deltas against both parents and the merge base `fa820988`;
   - the `e3d25d96` commit.
5. Then the published packet at `d10bbfd0` (`review-evidence/737-r1/author-r5/round5-*`).
6. Last, the prior public review findings, read only after my own pass over the diff.

I read no private author material and no other round-5 report.

## Assignment checks

1. **The conflicts keep both sides' facts.** Evidence: `receipts/merge_side_audit.txt`.
   - **Dev-side changes are all kept.** Every file dev changed between `fa820988` and `f6260253` has the dev blob in the merge, with these exceptions, which are all conflict or contract files:
     - the generated `.github/workflows/rtl.yml`, which is the PR blob (see check 2);
     - `CI_WORKFLOWS.md`, `ci_events.py`, `suite_shards.py` and `test_builder.py`.
   - **`ci_events.py` and `test_builder.py`** got exactly dev's delta: the changed-line digests are identical (`6079c646…` and `c8dbda90…`).
   - **PR-side changes are all kept.** Every file the PR changed has the PR blob, except the six that the `--cc` diff names.
   - **The HDL from #713 merges verbatim.** The gitlinks equal dev's (`gptp-processor` `e4869fd0`).
   - **`scripts/suite_shards.py:101`** records `gptp_tables` at 568, and `PROVISIONAL_SUITES` is empty (`:141`). That follows the module rule at `:15-17`: register a provisional figure "until a hosted window is measured". The overhead stays `(122,)*16` (`:146`). The dedicated self-test landmark moved to `milan_dp_mclk__0` on the last worker.
   - **I re-measured both hosted windows from the logs** (`receipts/hosted/measure_*`, `suite_windows_*.tsv`):
     - dev run 38601263345, job 115981133898 (worker 0/6, eight PASS lines, no failure): **567.745 s**;
     - PR run 38538854504, worker 0/6: **473.465 s**.

     The run 38601263345 as a whole concluded `failure`. Worker 2/6 hit TIMEOUTs on `milan_dp_gm_steps` and `milan_dp_mclk`. That worker ran 1.57× its recorded durations across its passing suites, while worker 0/6 ran at 0.93×. So 568 s comes from a normal-speed runner (`receipts/hosted/window_ratios.txt`).
   - **Driver inventory** (`receipts/driver_inventory.txt`):
     - `run_all_suites.sh --list` returns 63 suites, `gptp_tables` among them;
     - the 16 `--ci-pieces` shards hold 80 units, each exactly once;
     - shard 3/16 is `maap__2 milan_dp__0 chmap_capture gptp_tables tdm_render`.
   - **The production collector refuses** a `gptp_tables` log that is missing from worker 3, moved to worker 0, or duplicated there. It accepts the restored fixture (`receipts/plant_gptp_tables_collect.txt`).
   - **Union and collector self-tests pass** on the real inventory (`receipts/selftests/`).
2. **The workflows are generator output, and the generator derives and refuses.**
   - `python3 scripts/ci_gate_workflows.py --check` returns rc 0 (`receipts/generator_check.txt`).
   - All four generated workflows are byte-identical to `08adb21a`'s: 0 diff lines from PR to merge, and from merge to head.
   - The template's delta against `08adb21a` equals dev's `rtl.yml` delta. Both changed-line digests are `4cd44154…`, and the cross digests are `fc6c4ed4…`. So the template carries exactly dev's six edits:
     - the comment;
     - the matrix;
     - `total`;
     - the `5)` arm;
     - `--expect 6`.
   - **Generator derivation:** `scripts/ci_suite_workflows.py:100-113,125-128`.
   - **Planted mismatches** (`scripts/plant_generator.sh`, `receipts/plant_generator.txt`). Every one is refused:
     - arm `4)` with total 6;
     - `--expect 5` with total 6;
     - total 7 with arm `5)`;
     - a duplicated arm;
     - a duplicated expectation;
     - an edited template that was not regenerated;
     - a hand-edited generated file.

     The two worker-count refusals are raised by the new `ValueError`s. The last two are caught by the freshness check. The baseline returns rc 0.
3. **`CI_WORKFLOWS.md` keeps both sides' facts.**
   - Dev's #713 facts survive at `:366-377`: the provisional 1800 s figure, the sixth worker at 115 s, and "dev replaces both". Dev's "matrix of seven / stale total of six" example is at `:1369-1370`.
   - Dev's five-to-six count edits fall in passages that this branch had already restated for sixteen workers. Those passages are `:543`, `:1354`, `:2188` and `:2913`, and they are consistent with the generated graph.
   - The new claims are the placement and its figures, the 80/63 counts (`:348-349`), and the re-projected Verilator rows. I found no stale 79/62 count anywhere.
   - F1 covers the docs and elaboration rows that the merged workload invalidates.
4. **The re-projection is correct.** `scripts/project_workers.py` recomputes the projection from the head's own `suite_shards.py` and generated `rtl.yml` (`receipts/projection_head.txt`).
   - All sixteen rows equal `CI_WORKFLOWS.md:2731-2746`: 1605, 1541, 1572, **1544**, 1540, 1539, 1539, 1540, 1541, 1543, 1540, 1539, 1539, 1538, 1538 and 2032.
   - Every regular worker is at or under 1620. Worker 15 is 2032 against 2160.
   - Worker 3's margin is 76 s, and 1800 − 1544 = 256 s.
   - Counterfactual: at 1800 s the suite goes alone on worker 0, at 1922 s, which is OVER.
5. **The runner pin is unchanged.** `scripts/act_ci.py` has SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`. Its blob `bb3ef59b` is the same at `08adb21a` and at the head, with no diff (`receipts/act_ci_identity.txt`).

**Published packet.** Eleven round-5 receipts at `d10bbfd0` match the `published_sha256` in `MANIFEST.json`. They bind `e3d25d96` (`receipts/published_packet_check.txt`).
- The worker 3/16 receipt shows the 5 units passing with 5,518 checks, every executed step at rc 0, and no memory events.
- `round5-dev-workload.json` gives the same docs inputs I read independently from hosted runs 38601263556 and 38601263659 (`receipts/hosted/docs_*`).
- The evidence commit is unsigned. No signature file exists in that tree, so the binding rests on the manifest digests and the exact-head fields.

## Findings

### R637-5-F1 - MINOR - Conformance, Docs - `docs/testing/CI_WORKFLOWS.md:2688-2694,2721-2725,2752-2760`

**Authority and evidence.**
- Issue #737 acceptance 1, as replaced on 2026-10-14: every workflow on a PR finishes in at most 30 minutes.
- AGENTS §7: "authoritative documentation is current".
- This merge brings in #715 (#671). It was not in `08adb21a`, and `git merge-base --is-ancestor` confirms this. Hosted dev runs at `f6260253` compare with the `7032bca5` baseline as follows:

  | Measurement | `f6260253` | `7032bca5` |
  |---|---:|---|
  | docs-check job | 2682 s | 2039 s |
  | builder gate | 1400 s | 1065 s |
  | saved-state writer | 410 s | 119 s |
  | elaboration gates | 1763 s | 1441 s |
  | elaborate job | 2447 s | 2144 s |

  Sources: `receipts/hosted/docs_elab_steps_f6260253.tsv`, `docs_elab_jobs_f6260253.tsv` and `docs_check_steps_run38601263556.tsv`.
- I applied the document's own method (`:2690-2694`), which uses the larger of the local builder figure (the author's 1482 s at this head) and the hosted one (`receipts/hosted/docs_projection_recompute.txt`):
  - `docs-gates-0` = 1227 s (the table says 922);
  - `docs-gates-1` = 1602 s (the table says 1506), which leaves 18 s against its bound;
  - the docs workflow = 1872 s, **about 31.2 minutes, over 30**. On the hosted builder basis it is 29.8 minutes.
- Elaboration, from the author's re-measured legs, is about 29.1 minutes. The document says 26.4.
- At this exact head, `:2752-2755` still says "Docs now projects at 1506 seconds … about 29.6 minutes". The PR body's Round 5 table states 31.2 minutes, so the PR body and the authoritative document now disagree.
- The author disclosed the overrun as an open risk. No coordinating-role decision is recorded on #737 or #739.

**Impact.** The authoritative CI document makes a present-tense claim that is false at the merge head. Its evidence for the primary acceptance criterion now projects over the limit for the docs workflow. A cold reader would take the docs workflow as projected inside 30 minutes.

**Required outcome.** Both of the following:
- (a) `CI_WORKFLOWS.md`'s docs and elaboration projection rows and summary either reflect the merged-head inputs, or are explicitly dated to `7032bca5` with the merged-head projection stated beside them.
- (b) The docs workflow projects at or under 30 minutes at the merge head (for example, by dividing the docs builder gate), or the coordinating role publicly records how acceptance 1 is judged for docs at this head (for example, by an exact-head hosted measurement).

Either form of (b) clears F1. Moving it to another Issue does not.

**Verification.** Recompute the rows with the inputs above and the document's own formulas. Check that the text agrees with the PR body and with any recorded decision.

### R637-5-F2 - MINOR - Tests - `scripts/ci_suite_workflows.py:100-113,125-128`

**Authority and evidence.**
- AGENTS §5: "add or update self-checking tests for changed behavior".
- The delta replaces the generator's literal `4)` / `--expect 5` matching. It derives the arm and the expectation from the template's worker count and adds two refusals.
- No committed test exercises any of this. `git grep` finds both refusal messages only at their `raise` sites (`:110`, `:127`).
- `scripts/revert_generator_probe.sh` and `revert_generator_probe_git.sh` restore `08adb21a`'s `ci_suite_workflows.py` at this head and regenerate (`receipts/revert_generator_probe.txt`). The generated `rtl.yml` then regresses in two ways:
  - it carries a stray `5) … = milan_dp` arm in the 16-worker ownership step;
  - it carries `--expect 6` against 16 workers.
- Even so, all 18 committed gates return rc 0. These are every command of the docs template's "CI scheduling and evidence controls" step (`.github/ci-templates/docs.yml:457-472`), plus `ci_events.py --check` and `--selftest` (5,212 arms), `suite_shards.py --selftest` and `suite_tally_selftest.py`.
- The author's own `round5-generator-controls.json` M1 records the same blind spot: `ci_events_check_rc 0`. Its controls are ad hoc and not committed.

**Impact.** Reverting the derivation, or a future template count change that the old literals no longer match, would pass every host and docs gate. The failure would show only at run time: worker 5's ownership test, and the aggregate's `--expect` at `scripts/ci_events.py:4434`. That costs a full exhaustive run, and the gap leaves the changed behaviour unpinned.

**Required outcome.** A committed self-check that fails when generation does any of the following:
- leaves a dedicated `milan_dp` arm in the generated ownership step;
- emits a Verilator `--expect` other than the generated worker count;
- accepts a template whose arm index or `--expect` disagrees with its own `total`.

The probe I used shows the kind of mutation it must kill.

**Verification.** Run the new check at the fix head (rc 0). Then rerun `scripts/revert_generator_probe_git.sh`: at least one committed gate must return non-zero.

### R637-5-R1 - RESIDUE - Docs - PR #739 body, Status section, lines 21-28

- **Evidence.** The body says, "This head is not pushed; the coordinating role publishes it." The PR API reports `headRefOid` = `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`. This is the same stale tense as R637-4-R1 and R636-4-R1, now on the round-5 paragraph.
- **Impact.** Publication tense only.
- **Exact fix.** Replace that sentence with "The coordinating role published this head."
- **Effect.** This does not affect lens coverage.

### R637-5-R2 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:371-372`; `scripts/suite_shards.py:69-70`

- **Evidence.** In both places the text reads "dev run 38601263345 at `f6260253`, whose suites all passed". Grammatically, "whose" attaches to the run, but that run concluded `failure` (worker 2/6 TIMEOUTs). Only worker 0/6 passed everything, and the PR body states that correctly.
- **Impact.** Wording only. The figure, its source job and the measurement are correct.
- **Exact fix.** In both places, replace ", whose suites all passed" with ", where that worker passed all eight of its suites".
- **Effect.** This does not affect lens coverage.

## Per-lens results

[R637] UNCLEAN Conformance - `docs/testing/CI_WORKFLOWS.md:2752-2760` against #737 acceptance 1 (replaced). F1 is open. Checks 1, 2, 4 and 5 are proved (`receipts/merge_side_audit.txt`, `generator_check.txt`, `projection_head.txt`, `act_ci_identity.txt`, `hosted/measure_*`).

[R637] PASS RTL - `scripts/ci_suite_workflows.py:100-128`; generated `.github/workflows/rtl.yml` (byte-identical to `08adb21a`); `.github/ci-templates/rtl.yml` (dev's six edits only); HDL and gitlinks equal to dev `f6260253` (`receipts/merge_side_audit.txt`). The generated ownership step has no dedicated arm, and worker 15 runs `milan_dp_mclk__0` alone. The aggregate expects 16. Fail-closed runtime `--expect` is at `scripts/ci_events.py:4434`. No architecture or interface contract changes beyond dev's.

[R637] PASS Robustness - `receipts/plant_generator.txt` (7 of 7 malformed templates refused), `receipts/plant_gptp_tables_collect.txt` (missing, moved and duplicated suite logs refused), `receipts/projection_head.txt` (provisional counterfactual OVER, so the selector would refuse it). The hosted window comes from a passing normal-speed worker, not from a slow or failed one (`receipts/hosted/window_ratios.txt`).

[R637] UNCLEAN Tests - `scripts/ci_suite_workflows.py:100-128` (F2), proved by `receipts/revert_generator_probe.txt`. Otherwise all 12 head self-tests plus `ci_events.py --selftest` (5,212 arms) return rc 0 (`receipts/selftests/*.rc`). The worker 3/16 execution receipt (5 of 5 units, 5,518 checks) was checked against the manifest.

[R637] UNCLEAN Docs - `docs/testing/CI_WORKFLOWS.md:2688-2760` (F1). Otherwise:
- `:348-349`, `:366-377` and `:2731-2750` match the code and recomputation;
- `scripts/docs_check.py` returns rc 0 (208 files);
- `scripts/check_gptp_docs.py` returns rc 0;
- no added line in the merge-resolved files contains U+2014 (`receipts/em_dash_fallback.txt`).

The R1 and R2 RESIDUE items do not affect coverage.

## Prior public findings reconciled at this head

| Finding | Status at `e3d25d96` | Evidence |
|---|---|---|
| R637-4-R1 / R636-4-R1, RESIDUE: PR body publication tense | Retained as R637-5-R1 | The new round-5 Status sentence has the same defect |
| R636-4-S1, SUGGESTION: union "listed above" wording (`scripts/ci_builder_legs.py`) | Unchanged, still a SUGGESTION | The file is not in the delta |
| R636-4-S2, SUGGESTION: `scripts/ci_suite_workflows.py:21-35` | Unchanged, still a SUGGESTION | Lines 21-35 are not in the delta. Only `generate()` changed |
| R636-4-S3, SUGGESTION: builder driver selection refusals | Unchanged, still a SUGGESTION | Dev's only `sw/builder/test_builder.py` change is the self-test timeout (`:28846`) |
| R636-3-F1, R637-1/2 and R636-1/2 findings | Resolved at `08adb21a` (round 4) and retained | No file they depend on is touched, except the generator: see F2 |

## Reviewer-owned coverage ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #737 acceptance 1 (replaced); round-5 ruling; `scripts/suite_shards.py:64-146`; projection recompute; `scripts/act_ci.py` digest; hosted runs 38601263345, 38538854504, 38601263556 and 38601263659 | R637-5 | e3d25d964b5bbf0187290d0a357c6a6e4c5afd17 |
| RTL | CLEAN | `scripts/ci_suite_workflows.py:100-128`; template and generated `rtl.yml`; merge-side blob audit; gitlinks | R637-5 | e3d25d964b5bbf0187290d0a357c6a6e4c5afd17 |
| Robustness | CLEAN | Generator plants (7); collector plants (3); provisional counterfactual; `scripts/ci_events.py:4434` | R637-5 | e3d25d964b5bbf0187290d0a357c6a6e4c5afd17 |
| Tests | UNCLEAN (F2) | Head self-tests (13); generator revert probe (18 gates); worker 3/16 receipt | R637-5 | e3d25d964b5bbf0187290d0a357c6a6e4c5afd17 |
| Docs | UNCLEAN (F1) | `docs/testing/CI_WORKFLOWS.md:348-377,1354-1370,2688-2760`; `scripts/suite_shards.py:1-24,64-71`; PR body; `docs_check.py`; `check_gptp_docs.py` | R637-5 | e3d25d964b5bbf0187290d0a357c6a6e4c5afd17 |

## Real limits

- `scripts/check_em_dash.py` could not run because its pinned renderer is not installed here, and shared installs are not allowed. I substituted a direct U+2014 scan of the added lines. The author's receipts report the real gate passing.
- I did not run any suite, the builder, docs-check or rtl-fast myself. The worker 3/16 execution, the builder legs and the 26 host gates are the author's published receipts. I verified those receipts by digest and spot-checked them; I did not re-execute them.
- The 1482 s local builder figure that F1 uses is the author's measurement. The hosted 1400 s figure is mine, from the run API. F1 holds on the document's stated rule. On the hosted basis alone, docs projects at 29.8 minutes.
- Projections are not hosted times. Physical calibration was NOT RUN. Field skips are not hardware proof.
- The evidence commit `d10bbfd0` is unsigned. Its integrity rests on `MANIFEST.json` digests and exact-head fields.
- No manager source bank exists at this head, and none is inferred.

## Pending manager duties

- Decide F1(b), or route the docs-builder division to the executor. Then re-review F1 and F2 at a fix head. The Conformance, Tests and Docs lenses must be covered again there.
- Carry R637-5-R1 and R637-5-R2 to the residue checklist, and decide R636-4-S1 to S3.
- Build and validate the current-dev merge candidate (builder and native banks). Own hosted and act acceptance at the ready head.
- Dev `f6260253`'s own rtl-full push run 38601263345 failed: worker 2/6 hit TIMEOUTs on `milan_dp_gm_steps` (1800 s) and `milan_dp_mclk` (3600 s) on a runner 1.57× slower than recorded. The scheduled run 38689483489 also concluded `failure`. Both are dev-side conditions the merge candidate inherits, and I did not judge them here.

## Integrity and reproduction

- After the probes, the review clone is at `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`, tree `8c2bed598eee7447fe8b93158932407301f92a0a`.
  - `git status` is empty, and the worktree and index match HEAD.
  - All 1,375 index entries were re-hashed with zero blob or mode mismatches. The index digest equals the `ls-tree` digest (`233df808…`).
  - The gitlinks are `gptp-processor` `e4869fd0`, `protocol-processor` `2ad2f845`, `third_party/tsn-c-stack` `70936b77` and `third_party/verilog-axis` `48ff7a7e`.
  - No ignored non-cache files remain (`receipts/clone_integrity.txt`).
- All mutations ran in disposable copies under `scratch/`, which is not published.
- To reproduce, use `scripts/plant_generator.sh <clone> <scratch>`, `scripts/revert_generator_probe.sh` / `revert_generator_probe_git.sh <clone> <scratch>`, `python3 -I scripts/project_workers.py <clone> [suite=seconds]`, `python3 -I scripts/plant_gptp_tables_collect.py <clone>` and `python3 -I scripts/suite_windows.py <hosted logs>`. The hosted-log digests are in `receipts/hosted/hosted_log_digests.sha256`.

R637-5 FINISHED
