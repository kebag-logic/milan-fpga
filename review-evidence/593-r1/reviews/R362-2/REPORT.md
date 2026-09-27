[R362] NEGATIVE - exact head 68e801b2823f75e037152f7eb2ac4c5dcda5d919

# R362-2 internal independent review: issue #593 / PR #601

- Head `68e801b2823f75e037152f7eb2ac4c5dcda5d919`, tree `d385f231213eda4bb52414ef09cb3eaf8d663097`, base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- Delta under review: `95bea7cf..68e801b2`, one commit. The whole PR diff `6d5ebd73..68e801b2` was re-read for items 5 and 6.
- Context was rebuilt from public state only, in this order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #593 body and the manager's comments 5858876858, 5858887057 and 5859221324; the #602 body and ruling 5859297355; REQ-VER-06; TESTING 6d; GM_LOSS_RECOVERY "Media re-base on a PHC step"; the diff and history; then public evidence.
- Prior public review findings were read only after this verdict and ledger were written. See "Round-1 findings: resolved or retained".

## Summary

Items 1, 4 and 7 are met at this head, and item 6's gate behaviour is met: PHC-only causes still fail. Three items are not met:

- **Item 3 (F1, MINOR).** The derived `tu` deciding resolution is 0.25 s. At that resolution the Annex B.1.1 minimum is not decided. At R = 0.249 s, a 2 ms `tu` hold after a GM change passes. At R = 0.2 s, a 60 ms hold passes. This also defeats item 2's "clears at that instant" case for any R from 0.125 s up to 0.25 s.
- **Item 5 (F2, MINOR).** Nine behaviourally distinguishable mutants of checks or assertion text added by this PR survive both the self-test and the plan feature. One of them is a key token that PR #586 had pinned and this PR unpinned.
- **Item 6 text (F3, MINOR).** REQ-VER-06, TESTING 6d and the GM_LOSS_RECOVERY "Outgoing `mr`" row still describe #602 as pending. The #602 ruling was recorded before this commit.

## Findings

### F1: MINOR. Lenses: Conformance, Robustness, Tests, Docs. The `tu` deciding resolution does not decide the 0.25 s minimum

**Where**
- `tb/tools/torture_campaign.py:3583-3586`: `resolution_limit_s = min(0.25, holdover_bound_s)`, and NOT RUN only when `R >= 0.25`.
- `tb/tools/torture_campaign.py:3623-3626`: the history oracle gates on `0 <= R < 0.25`.
- `tb/tools/torture_campaign.py:3606`: the minimum check is `clear + R < gm + 0.25` → FAIL.
- `docs/testing/TESTING.md:1022-1024`.
- `REQUIREMENTS.md:304`.
- The `SOAK_ASSERTS` text "observation_resolution_s must be less than min(0.25 s, 0.5 s)".

**Authority**
- #593 round-2 item 3: a resolution too coarse to decide the 0.25 s minimum or the 0.5 s clear bound yields NOT RUN, with the deciding resolution derived.
- Item 2: a GM change after which `tu` "clears at that instant" fails.
- Milan v1.2 Annex B.1.1, which the project reads as a minimum.
- R is defined as the relative event/capture error bound (`torture_campaign.py:3570`, `TESTING.md` "Let R be the recorded relative event/capture timestamp resolution").

**Evidence** (`receipts/r362_2_behaviour.out`, planned oracle `check_release_tu_history`)

| Probe | Input | Actual | Required at a deciding resolution |
|---|---|---|---|
| I3e | GM at 0; `tu` interval `[0, 0.002)`; R = 0.249 | `PASS` | not PASS (FAIL or NOT RUN) |
| I3f | GM at 0; `tu` interval `[0, 0.06)`; R = 0.2 | `PASS` | not PASS (FAIL or NOT RUN) |
| I3g | GM at 0; `tu` interval `[0, 0.13)`; R = 0.125 | `PASS` | not PASS (FAIL or NOT RUN) |
| I3h | GM at 0; `tu` interval `[0, 0.124)`; R = 0.124 | `FAIL` | FAIL |

Under the checker's own error model, a true hold `d` is observed as `h` in `[d - R, d + R]`. The minimum passes when `h + R >= 0.25`. So a true instant clear (`d = 0`, observed as `h <= R`) can pass whenever `2R >= 0.25`. A PASS certifies only `d >= 0.25 - 2R`.

The stated derivation, "resolution must be smaller than each limit being decided", guarantees only that some hold can fail. It does not guarantee that the item-2 case fails.

The same PR derives the `mr` limit from the two-sided window, `2R < 1 s` (`TESTING.md:955`, `torture_campaign.py:3762-3763`). The `tu` derivation omits that factor for the same kind of tolerance.

`test_release_deciding_resolution` (`torture_campaign.py:5734-5741`) grades only a compliant-looking 0.3 s hold at R = 0.249 s. No test places a short hold near the limit.

**Relation to round 1.** R362-1 F3 asked, "at minimum", that R ≥ 0.25 s give NOT RUN for the GM minimum, and R363-1 F4 made the same request. This head meets that floor. This finding sharpens the floor under the checker's own error model; it does not reverse it. The severity stays at round 1's MINOR.

**Impact.** Suppose GM-change timestamps come from polled gPTP publication reads with 100-240 ms correlation error, a plausible bench setup. Then a `tu` that clears immediately after a GM change passes the release gate's B.1.1 minimum, and the verdict records it as decided.

**Required outcome**
- A resolution at which a `tu` interval that clears at the GM change instant could pass the minimum yields NOT RUN. The same applies to the 0.5 s clear bound: a PASS must not admit a true hold beyond what the rule tolerates.
- The derivation is stated in TESTING 6d, REQ-VER-06 and the assertion text, consistently with the two-sided error model used for `mr`.
- A self-test places a short hold at the new boundary on both sides.
- A killed mutant pins the new limit.

**Verification**
- Re-run `probes/r362_2_behaviour.py`: I3e, I3f and I3g must not return PASS.
- A mutant that restores `R < 0.25` must be killed.

### F2: MINOR. Lens: Tests. Item 5 is not met: new checks and assertion text survive mutation

**Where**
- `tb/tools/torture_campaign.py:3637`, `3641`, `3623`, `3626`, `3659`, `3662`, `3393`, `3408`.
- `tb/tools/torture_release_mutants.py`.

**Authority.** #593 round-2 item 5: every check added by this PR, and every new assertion text, is pinned by a killed mutant.

**Evidence.** In `receipts/r362_2_mutants.out`, 52 of 63 applied mutants were killed and 11 survived both `--self-test` and the plan feature. `receipts/r362_2_survivor_witness.out` shows that each counted survivor changes a verdict or the stated evidence on a concrete input:

| Mutant | Change | Line | Witness input | Pristine result | Mutant result |
|---|---|---|---|---|---|
| C06 | GM changes in the start allowance no longer get the 0.25 s minimum | :3641 | 10 ms hold, GM 0.5 ms before rise | FAIL | PASS |
| C07 | A GM change at clear is assigned to the preceding interval, contrary to TESTING "A change at clear belongs to no preceding interval" | :3641 | two intervals | PASS | FAIL |
| C09 | Touching intervals accepted | :3637 | two touching intervals | NOT RUN | graded |
| C10 | Negative resolution accepted by the history oracle | :3626 | empty history | NOT RUN | PASS |
| C19 | The history oracle's stated `resolution_limit_s` removed. This is item 3's "stated" limit in the oracle the plan selects | :3623 | any history | `0.25` | `None` |
| C34 | Empty `stream_id` record accepted | :3659 | one record with `stream_id` "" | NOT RUN | PASS |
| C35 | Negative `pdu_index` accepted | :3662 | negative indices | NOT RUN | PASS |
| T05/T21 | Assertion text "match causes within +/- observation_resolution_s of the toggle" deleted or made one-sided | :3393 | text | text present | text removed |
| T13/T25 | Assertion text "(including PHC settime/adjtime and fabric discontinuity)" deleted or negated | :3408 | text | text present | text removed |

The last row is the PR #586 key token that this PR unpinned. The PR replaced the phrase that #586 pinned, "PHC settime/adjtime, fabric discontinuity, or GM-identity edge", and the replacement phrase is no longer pinned.

C38, the `cause_window` string in the `mr` verdict detail, also survives. It is not counted because it is not a check.

**Impact.** Regressions in these guards and texts pass every gate. C06 would let a short `tu` after a GM change inside the start allowance pass the release gate.

**Required outcome.** Each listed guard and text is pinned by a mutant that a named test kills, or the guard is removed as unnecessary with public justification.

**Verification.** Re-run `probes/r362_2_mutants.py` and `probes/r362_2_survivor_witness.py`: no counted survivor.

### F3: MINOR. Lens: Docs. The #602 text describes an open question after the ruling

**Where**
- `REQUIREMENTS.md:280-282`: "records the PHC-step conflict. Pending that decision...".
- `docs/testing/TESTING.md:936-938`: "records the conflicting PHC-step design contract. Pending its decision...".
- `docs/design/GM_LOSS_RECOVERY.md:155`: "release-rule conflict awaits #602", "Pending #602".

**Authority**
- #602 ruling 5859297355 (2026-09-27T19:54Z): a PHC step or presentation-time re-base alone is not an outgoing `mr` cause. The RTL change is implemented under #602, and "The #593 gate keeps rejecting PHC-only causes; the current image fails that check until this lands."
- The head commit is dated 19:59Z, after the ruling.
- This round's brief item 6 requires the text to match the ruling rather than an open question.

**Impact.** A cold reader of the normative requirement is told the rule may flip pending a decision. The recorded ruling says it will not. The reason the current image fails, which is an RTL change still to land under #602, is not stated.

**Required outcome.**
- The three places cite the #602 ruling: PHC-only is no `mr` cause, the RTL change is pending under #602, and until it lands a soak containing a PHC step fails on the current image.
- The GM_LOSS_RECOVERY row no longer calls the release rule a pending conflict. Its other columns remain #602's deliverable.

**Verification.** Text inspection at the new head, plus `docs_check.py`, `check_doc_style.py` and `check_em_dash.py`.

### S1: SUGGESTION. Lens: Docs. Reset wording

`TESTING.md:966-969` says every MEDIA_RESET decrease fails the soak, while `soak.counter-walk` and the soak table say "no unexplained counter reset". The code (`torture_campaign.py:3710-3712`) fails every decrease.

This is consistent with a continuous soak, since a talker start is itself an interruption. One sentence reconciling the two would help a cold reader. It does not affect coverage.

## Items 1-7 at this head (own probes, `receipts/r362_2_behaviour.out`)

| Item | Result | Evidence |
|---|---|---|
| 1. `tu` rise before first discontinuity fails | Met | I1a-I1e: the R347-5 S1 case `[0, 10.4)` with an event at 10 FAILs in both oracles. The R edge is inclusive. Killed mutants: C01, C02, C03 and the author's two |
| 2. Every GM change graded; never set or cleared at that instant fails | Met at fine R; defeated at coarse accepted R (F1) | I2a-I2f FAIL/PASS as required at R = 0.001. I3e-I3g PASS at R ≥ 0.125 |
| 3. Coarse resolution yields NOT RUN, limit derived and stated | Not met for `tu` (F1). `mr` limit of 0.5 s met | I3a-I3d; `resolution_limit_s` is present in all three verdicts; C19 unpinned (F2) |
| 4. One cause excuses at most one toggle per stream | Met | I4a-I4e; C22 killed; greedy earliest assignment is optimal for equal-width windows over toggles in time order |
| 5. Every new check and text pinned by a killed mutant | Not met (F2) | 11 survivors; 9 counted |
| 6. #602 referenced; PHC-only still rejected; text matches the ruling | Referenced: met. Rejection: met (I6-*, five PHC/GM kinds FAIL). Text: not met (F3) | `REQUIREMENTS.md:280`, `TESTING.md:936`, `GM_LOSS_RECOVERY.md:155` |
| 7. Capture not spanning the counter window gives NOT RUN; decrease decoded as reset | Met | I7a-I7e; C23-C28 killed |
| PR #586 arms and mutants still pass | Met, with F2's unpinned token | The author driver's 106 mutants were all killed (`receipts/release_mutants.out`). All 25 #586 mutant names are present. Three are re-anchored to unique anchors with the same replacement, and all are killed. #586 tests changed only for the assigned SKIP→NOT RUN decision and the item-1 reversal of `test_release_tu_before_first_discontinuity` |
| No firmware, RTL or builder change | Met | `receipts/scope.txt`: seven files, all planner, mutants, tests or docs; modes 100644 unchanged; gitlinks unchanged |

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `torture_campaign.py:3562-3796` against #593 items 1-7, the #602 ruling, Annex B.1.1/B.1.2 and IEEE 1722-2016 4.4.4.3/4.4.4.7; `receipts/r362_2_behaviour.out` (41 probes, 3 unexpected) | R362-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| RTL | CLEAN | `receipts/scope.txt`. The diff contains no `hdl/`, firmware or builder path. GM_LOSS_RECOVERY.md:155's "This tree" claim still matches `hdl/milan/milan_datapath.sv:3135-3137` (`mcr_restart_p_w ... \| media_rebase_p_w`) at head. That RTL change is #602's, not this PR's | R362-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Robustness | UNCLEAN (F1: behaviour at the maximum accepted resolution) | Malformed/None/NaN/bool/negative/unordered/touching/empty inputs to `check_release_tu`, `check_release_tu_history` and `check_release_mr`: all refused as NOT RUN (probes S-C09, S-C10, S-C34, S-C35, I7a-I7c). Only the maximum-resolution case fails | R362-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Tests | UNCLEAN (F1, F2) | `torture_campaign.py` `_ReleaseSoakChecks` (lines 5524-5842), `torture_release_mutants.py` (106 killed), plan feature (87 scenarios), `receipts/r362_2_mutants.out`, `receipts/r362_2_survivor_witness.out` | R362-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Docs | UNCLEAN (F1, F3) | `REQUIREMENTS.md:250-311`, `docs/testing/TESTING.md:916-1060`, `docs/design/GM_LOSS_RECOVERY.md:142-160`; docs gates in `receipts/docs_gates.out`, all rc 0 once the pinned renderer is present | R362-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |

## Commands run at this head (all foreground; receipts under `receipts/`)

| Command | Result | Receipt |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 75 tests OK | `selftest.out` |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0, 106 mutations killed | `release_mutants.out` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | rc 0, 87 scenarios, 356 steps | `behave_plan.out` |
| `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_feature_status.py --self-test` | rc 0 | `docs_gates.out` |
| `check_em_dash.py --base 6d5ebd73` and `--selftest`, `gen_toc.py --check` and `--verify-anchors` | rc 2 without the pinned renderer; rc 0 in a disposable scratch venv built from `tools/markdown/requirements.txt` with `--require-hashes` | `docs_gates.out` |
| `git diff --check 6d5ebd73 68e801b2` | rc 0 | `docs_gates.out` |
| `probes/r362_2_mutants.py` | 52 killed, 11 survived, 4 anchor collisions (re-run in the witness script) | `r362_2_mutants.out`, `r362_2_mutants.json` |
| `probes/r362_2_survivor_witness.py` | 8 witnesses; the 4 re-anchored texts killed, plus T25 surviving | `r362_2_survivor_witness.out` |
| `probes/r362_2_behaviour.py` | 38 as required, 3 unexpected (F1) | `r362_2_behaviour.out` |
| Unchanged R362-1 `oracle_probe.py` (`probes/round1/`, sha256 matches the R362-1 manifest), direct and via `probes/round1_span_shim.py` | Direct: `mr` cases NOT RUN (item 7). Via the shim: 60 of 64 met; the 3 not met are superseded M8 and suggestions B2 and E2 | `round1_oracle_probe_at_68e801b2.out`, `round1_oracle_probe_spanning_at_68e801b2.out` |
| Unchanged R362-1 `reviewer_mutants.py` (at most 8 jobs) | 32 killed, 4 invalid anchors (re-anchored equivalents killed) | `round1_reviewer_mutants_at_68e801b2.out` |

The mutants ran on copies under `scratch/`, and the checkout was never written. After the probes:
- HEAD and tree match the values above.
- `git diff-index HEAD` is empty, and the index and worktree are clean.
- One ignored `tb/tools/__pycache__/` that this review's import created was removed.
- All four gitlinks are unchanged from base: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 870ff88a, `third_party/verilog-axis` 48ff7a7e.
- The (mode, blob, path) set of the index equals HEAD's tree (`receipts/clone_integrity.txt`, `receipts/scope.txt`).

The scoped Verilator was not used, since the diff has no RTL.

## Real limits

- This is a desk review of a desk-level planner. Physical calibration, the soak and power campaigns are NOT RUN. Field skips are not hardware proof.
- The builder bank (`ci_scope.py --selftest`, `check_baremetal_only.py`), the gPTP/solution/submodule/traceability and hygiene gates, act, and the full parent/PP/gPTP/Yosys banks were not run here, by assignment.
- The linked public evidence tree `review-evidence/593-r1` at `59efc9fa` records gates at `95bea7cf`, not at this head. The claims for this head's builder and contract gates rest on the executor's REVIEW READY comment and the manager's statement.
- Hosted checks were read-only snapshots (`receipts/hosted_checks_snapshot.txt`). At snapshot time, docs-check, elaborate and Verilator shards 1, 2 and 4 were still in progress. "Physical gPTP" was skipped, which is not executed evidence.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- Final current-dev candidate build and merge validation, source base `6d5ebd73`.
- Post-merge containment.
- Re-review at the corrected head after F1-F3 are addressed. F1 changes a checker, so Conformance, Robustness, Tests and Docs must be re-covered at that head. RTL stays covered unless an `hdl/` path changes.

## Why RTL is CLEAN while the PHC-step toggle is still in the tree

`hdl/milan/milan_datapath.sv:3135-3137` still toggles outgoing `mr` on every PHC step (`| media_rebase_p_w`). Under ruling 5859297355 that behaviour is now a defect.

This review does **not** bank that defect as resolved. It sits outside this PR's diff, for three reasons:
- The ruling assigns its removal to #602's deliverable 2.
- This round's assignment forbids RTL changes here.
- The gate this PR adds fails the current image because of it (probes I6-*). So no release can pass through this gate while the toggle remains.

The RTL lens covers this PR's changes, which touch no RTL. The stale documentation of the release rule is F3 (Docs). The row's "decided reaction" and "This tree" columns are #602's deliverable.

## Round-1 findings: resolved or retained

These were read after the verdict and ledger above were written.

Two re-runs support the table below:
- The unchanged R362-1 probe was re-run through `probes/round1_span_shim.py`, which only supplies a spanning capture window (`receipts/round1_oracle_probe_spanning_at_68e801b2.out`). It met 60 of 64 cases. Run without the shim, every `mr` case correctly reads NOT RUN under item 7 (`receipts/round1_oracle_probe_at_68e801b2.out`).
- The unchanged R362-1 mutant driver killed all 32 applicable mutants (`receipts/round1_reviewer_mutants_at_68e801b2.out`). Its 4 invalid anchors match code that changed shape:
  - R01 and R02: the cause-window line was split. The author's "mr cause window doubled" and "strict" mutants are killed.
  - R13: the wrap decode was replaced by reset detection. C27 and C28 are killed.
  - R24: the `< clear` filter was replaced by grading every supplied GM change. The author's "single interval drops future GM changes" mutant is killed.

| Prior finding | Status at 68e801b2 | Evidence |
|---|---|---|
| R362-1 F1 (MAJOR) = R363-1 F1: rise before first discontinuity passes | **Resolved** | Round-1 S-R347-5-S1/S1b/S1c now FAIL; I1a-I1e; `test_release_tu_before_first_discontinuity` inverted; TESTING 6d replaced (`TESTING.md:1041-1044`); C01-C03 killed |
| R362-1 F2 (MAJOR) = R363-1 F2: GM change with no `tu` never graded | **Resolved at decidable R**; residual at coarse accepted R retained as R362-2 F1 | Round-1 B1 now FAIL; I2a-I2f; `check_release_tu_history` selected by the plan (C08, C04, C05 killed) |
| R362-1 F3 (MINOR) = R363-1 F4: coarse resolution yields PASS | **Partly resolved.** R ≥ 0.25 (`tu`) and R ≥ 0.5 (`mr`) now give NOT RUN, and the limit is stated. **Retained** as R362-2 F1 for 0.125 ≤ R < 0.25 | Round-1 S-R346-3-S1/S1b/S1c now NOT RUN; I3a-I3g |
| R362-1 F4 (MINOR) = R363-1 S3: PHC-step conflict unrecorded | **Resolved** as to recording (#602 opened, ruled, referenced from all three places). **Retained** as R362-2 F3 for the stale "pending" wording | `REQUIREMENTS.md:280`, `TESTING.md:936`, `GM_LOSS_RECOVERY.md:155`; ruling 5859297355 |
| R362-1 F5 (MINOR): 14 reviewer mutants survived | **Resolved** for all 14 (R08, R10-R17, R24, R26, R27, R29-R31 are killed or have killed re-anchored equivalents). New survivors in the round-2 code are retained as R362-2 F2 | `round1_reviewer_mutants_at_68e801b2.out`; `release_mutants.out` |
| R363-1 F3 (MINOR): one cause excuses many toggles | **Resolved** | I4a-I4c; round-1 E1 now FAIL; C22 and the author's "mr reuses one cause" / "cause order ignored" killed |
| R363-1 F5 (MINOR): unpinned checks and texts | **Resolved** for M06, M12-M15, M19, M20, M22, M24, M28, M29, T1-T4, M32 and M34 (the author's named mutants for each are killed). **Retained** for M26's analogue, a GM change at clear counted by the covering interval (C07), within R362-2 F2 | `release_mutants.out`; `r362_2_survivor_witness.out` |
| R362-1 S1: one cause, several toggles | **Adopted and resolved** (item 4) | as for R363-1 F3 |
| R362-1 S2: MEDIA_RESET under-count not graded | **Open suggestion**, not assigned (the executor disclosed it) | Round-1 E2 still PASS |
| R362-1 S3 = R363-1 S2: reset decoded as wrap | **Adopted and resolved** (item 7) | I7d, I7e; round-1 E3 now FAIL with "counter reset". Round-1 M8's wrap expectation is superseded by this assigned decision |
| R362-1 S4: unkinded GM edge bypasses the minimum | **Open suggestion**, not assigned | Round-1 B2 still PASS |
| R363-1 S1: capture span not checked | **Adopted and resolved** (item 7) | I7a-I7c; C23-C26 killed |

The #396-routed suggestions:
- R346-3 S1 is resolved by the resolution ceiling, with the F1 residual.
- R346-3 S2 is resolved.
- R346-3 S3 is resolved except the T05 and T13 texts (F2).
- R347-5 S1 is resolved.

R362-2 FINISHED
