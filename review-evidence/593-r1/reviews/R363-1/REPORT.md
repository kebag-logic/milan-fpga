[R363] NEGATIVE - exact head 95bea7cf82fcf7cf034c156ef7aa6800ee769e05

# R363-1: external independent review of PR #601 (issue #593)

- Head `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`, tree `0f33d799e9d44872cd4fae3ad1551cf85f2b5e1e`, one commit on base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md and docs/README.md. Also read: the #593 body; assignment 5858876858; scope note 5858887057; the #396 correction 5857765949; REQ-VER-06; TESTING 6d. The IEEE 1722-2016 §4.4.4.3/§4.4.4.7 text and the Milan v1.2 Tables 5.4/5.6 and Annex B.1.1/B.1.2 text were checked against local copies (`receipts/standards_check.txt`).
- The diff touches 5 files: `REQUIREMENTS.md`, `docs/testing/TESTING.md`, `tb/tools/torture_campaign.py`, `tb/tools/torture_release_mutants.py` and `tests/steps/torture_release_steps.py`. It changes no gitlink and no RTL, firmware or builder path (`receipts/diff_scope.log`).
- All five lenses were applied at this head. Two MAJOR and three MINOR findings are open, so the verdict is NEGATIVE.

## What holds (verified)

- **Every item-2 arm exists and grades as stated.** Checked by the self-test and by my own probe (`receipts/oracle_probe.log`, cases G/H):
  - a clock-source cause passes (`tb/tools/torture_campaign.py:5420`);
  - each CRF cause passes (`:5420`);
  - no cause fails (`:5430`);
  - GM-identity, GM time-source, PHC and fabric causes alone each fail (`:5434`, probe G);
  - a 7-PDU hold fails and exactly 8 passes (`:5465`, probe H1/H2);
  - a MEDIA_RESET increment with no cause fails (`:5475`);
  - `tu` cleared 0.24 s after a GM change at 1 ms resolution fails (`:5518`).
- **Cause windows are derived, not literal.** Causes are matched at `toggle ± observation_resolution_s` (`:3620-3625`), and MEDIA_RESET at `[before - 1 s - R, after + R]`. The 1 s is the Milan observation-interval ceiling, `MILAN_MAX_OBSERVATION_INTERVAL_S` (`:287`, `:3644-3646`).
- **The hold counts the carrying stream.** PDUs, causes and reads are filtered by `stream_id` (`:3680-3682`), and per-stream indices must be contiguous (`:3614`).
- **Missing inputs give NOT RUN.** This covers `None` inputs, an incomplete capture, a non-finite, negative or bool resolution, a PDU gap, an unfinished 8-PDU tail and missing GM history. `exit_code` treats NOT RUN as not clean (`:4112`).
- **Planner output outside the rule is unchanged.** Across `--plan`, `--plan --json`, `--checklist`, `--coverage` and `--coverage-by-area`, the audio, churn, matrix, multi, payload, physical and torture areas are byte-identical to base. The power area differs only in the shared `release.complete-evidence` text, which gains "NOT RUN" (`receipts/plan_diff.log`, `receipts/plan_output_base_vs_head.diff`).
- **PR #586's controls still pass.** Its 25 repository mutants are still killed inside the 44/44 run.
- **Gates re-run at this head:**
  - planner self-test: 66 tests OK (54 at base plus 12 new; no existing test removed);
  - repository mutants: 44/44 killed;
  - plan feature: 86 scenarios / 353 steps;
  - `@torture` tier: 231 scenarios passed, 172 skipped;
  - `docs_check`, `check_doc_style`, `check_doc_paths`, `check_feature_status --self-test`, `check_archive`, `check_py_idiom`, `ci_scope --selftest`, `check_baremetal_only --check` and `git diff --check`: all rc 0 (`receipts/gates.log`).

## Findings

**F1 - MAJOR - Conformance, Robustness, Tests, Docs - `tb/tools/torture_campaign.py:3579`, `:5343-5349`; `docs/testing/TESTING.md:1007-1010` - a `tu` interval that rises long before its first recorded discontinuity still passes (R347-5 S1 not implemented)**
- Authority: scope note 5858887057 routes R347-5 S1 into this rule: "a `tu` interval that rises before its first recorded discontinuity must fail the containment check". This is part of the frozen items 1/2, with no extra scope.
- Evidence:
  - `check_release_tu((0, 10.4), [10], R=0.001, gm_changes_s=[])` returns PASS (`receipts/oracle_probe.log` A1). A GM change 1 s after the rise also passes (A2).
  - `test_release_tu_before_first_discontinuity` pins that 10.4 s interval as PASS.
  - TESTING.md:1007-1010 still states that the rule "adds no separate bound" for the time before the first discontinuity.
- Impact: up to 10 s of uncaused `tu` passes the release soak whenever a discontinuity lands shortly before the clear.
- Required outcome: an interval fails when its first contained discontinuity lies more than the resolution after the observed start. The test and TESTING 6d must say so, and a mutant removing that bound must be killed.
- Verification: probe cases A1/A2 give FAIL and A3 gives PASS. The pinned test is inverted, and the TESTING text is replaced.

**F2 - MAJOR - Conformance, Robustness, Tests, Docs - `tb/tools/torture_campaign.py:3584-3590`; `docs/testing/TESTING.md:1014-1015`; `REQUIREMENTS.md:288` - a GM change after which `tu` is never set (or clears at that instant) is never graded**
- Authority:
  - Issue item 1: "After a GM change, `tu` stays set for at least 0.25 s (Milan Annex B.1.1)".
  - REQ-VER-06: "After every GM change, `tu` remains set for 0.25 seconds".
  - Item 2 arm: "`tu` held under 0.25 s after a GM change fails". A zero hold is under 0.25 s.
- Evidence:
  - The minimum is evaluated only inside a supplied `tu` interval, and only against GM changes strictly before its clear. No oracle grades the GM history against the set of intervals.
  - Interval (0, 0.3) with a GM change at 0.35 or at 0.3 returns PASS (`oracle_probe.log` B1/B2).
  - A campaign with GM changes and no `tu` interval at all has nothing to grade.
- Impact: a talker that ignores GM changes for `tu` passes the soak's `tu` rule.
- Required outcome: every recorded GM change is covered by an interval that includes it and satisfies the minimum, or the check fails. Missing GM history stays NOT RUN, and TESTING 6d states the procedure.
- Verification: probe B1/B2 give FAIL, and new self-test arms plus a mutant control are killed.

**F3 - MINOR - Conformance, Robustness, Tests - `tb/tools/torture_campaign.py:3620-3625` - one recorded cause can excuse any number of `mr` toggles**
- Authority: §4.4.4.3 says `mr` is toggled "each time a media clock restart is needed". The corrected rule says every toggle must coincide with a recorded cause, and "anything else fails".
- Evidence:
  - A cause is matched per toggle with `any(...)` and is never consumed. The MEDIA_RESET path, by contrast, consumes distinct toggles (`:3652`).
  - One clock-source change with toggles at PDU 1 and PDU 9 passes at R = 2 ms. Four toggles pass at R = 4 ms (`oracle_probe.log` D1/D2).
  - At 8 kHz, 8 PDUs take 1 ms, so an R of a few milliseconds is realistic.
- Impact: a talker that flaps and restarts listeners repeatedly for one source change passes.
- Required outcome: each toggle is matched to a distinct recorded cause, or a decided exception is documented.
- Verification: D1/D2 give FAIL and D3 gives PASS, and a mutant restoring shared causes is killed.

**F4 - MINOR - Conformance, Robustness, Tests - `tb/tools/torture_campaign.py:3571`, `:3588` - a resolution too coarse to decide the new 0.25 s minimum or the 0.5 s bound still yields PASS**
- Authority:
  - Assignment decisions: the 0.5 s clear and the 0.25 s minimum "are judged against the recorded resolution", and missing evidence is NOT RUN, never PASS.
  - The scope note routes R346-3 S1 in: the resolution comes from wire or event timestamps, not the 60 s periodic read.
- Evidence:
  - The code refuses only `R < 0`.
  - At R = 0.25, `tu` cleared 1 ms after a GM change returns PASS, so the minimum cannot fail.
  - At R = 60, a 60 s interval returns PASS (`oracle_probe.log` C1/C2).
  - The resolution's source is enforced only by prose.
- Impact: undecidable evidence produces a PASS record instead of NOT RUN.
- Required outcome: a resolution at which the minimum or the bound cannot be decided gives NOT RUN, against a stated and derived ceiling. Otherwise the decision owner records that text-only enforcement is accepted.
- Verification: C1/C2 give NOT RUN, and a boundary test and a mutant are added.

**F5 - MINOR - Tests - `tb/tools/torture_campaign.py:5402-5566`, `:5351-5365` - several new checks and the new assertion texts are not pinned (R346-3 S3 routed into scope)**
- Evidence: these mutants survive both the self-test and the `@torture` feature tier (`receipts/reviewer_mutants.log`, `receipts/survivor_recheck.log`):
  - M06: MEDIA_RESET reads are not filtered by stream.
  - M15: a single counter read is accepted. This is missing endpoint evidence that should be NOT RUN, and it passes.
  - M14: counter-wrap decoding is removed. The wrap arm at `:5495` cannot fail, because a negative delta also passes.
  - M12 and M13: the PDU and read ordering checks are removed.
  - M19 and M20: value-range and kind-type validation are removed.
  - M22: the MEDIA_RESET upper edge loses R.
  - M24: MEDIA_RESET consumes the latest toggle instead of the earliest.
  - M26: a GM change exactly at the clear is counted.
  - M28: any holdover bound is accepted.
  - M29: a zero-length interval is accepted.
  - T1 and T2: the `tu` assertion text drops the GM minimum, "Annex B.1.1 minimum" and "missing GM history is NOT RUN".
  - T3, T4 and M34: the `mr` assertion text drops the cause list, the toggle/increment scope and the interval counting.
  - M32: `release.complete-evidence` drops "NOT RUN".
- Impact: regressions in the missing-evidence arms, the stream scoping and the operator-facing texts would pass silently.
- Required outcome: each of these behaviours and texts is pinned by a test that fails on its removal.
- Verification: rerun `scripts/reviewer_mutants.py` and `scripts/survivor_recheck.py`, and every listed mutant is killed.

**S1 - SUGGESTION - Robustness - `tb/tools/torture_campaign.py:3657-3691`; `TESTING.md:961` - the capture span is not checked against the counter-read window.** With `capture_complete=True`, a 5 ms capture passes against a 3600 s counter window (`oracle_probe.log` E1). Consider giving NOT RUN when the PDU capture does not span `[first read - 1 s - R, last read]`.

**S2 - SUGGESTION - Robustness, Docs - `tb/tools/torture_campaign.py:3643` - a MEDIA_RESET decrease is decoded as a 32-bit wrap.** Milan Table 5.4 resets the output counter when the talker starts. The oracle reports the decrease as an uncaused increment of 4294967293 (`oracle_probe.log` F1). It fails safe, but the reason is misleading. A wrap is not reachable in 7 days at no more than 1 increment per second.

**S3 - SUGGESTION - Conformance, Docs - `docs/design/GM_LOSS_RECOVERY.md:155` - disclosed conflict with the shipping design.**
- That document says the design toggles outgoing `mr` once per PHC step, whatever the media clock source, per the #387 decision.
- Under the new REQ-VER-06 that toggle fails unless a permitted cause is also recorded.
- The conflict is disclosed in REVIEW READY. It is routed only loosely to the #74 `mr` gating item.
- Consider an explicit owner decision that links #387 and the corrected rule.

## Routed #396 suggestions

| Item | Status at 95bea7cf |
|---|---|
| R346-3 S1 (resolution source) | Retained as F4. The source is text-only, and a coarse R yields PASS. |
| R346-3 S2 (0.25 s lower bound) | Implemented for GM changes inside intervals. A GM change with no following `tu` interval is F2. |
| R346-3 S3 (pin assertion texts) | Partly done: 7 `mr` phrases are pinned at `:5546-5566`. The new `tu` and evidence texts are F5. |
| R347-5 S1 (`tu` rising before its first discontinuity fails) | Not implemented, and pinned the other way: F1. |

This PR had no prior public review findings when I checked, after my independent pass. PR #601 had only the two review-start comments and no reviews.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | IEEE 1722-2016 §4.4.4.3/§4.4.4.7, Milan Tables 5.4/5.6 and Annex B.1.1/B.1.2 against `tb/tools/torture_campaign.py:3553-3722` and #593 items 1/2 plus decisions; `receipts/oracle_probe.log`, `receipts/standards_check.txt` | R363-1 | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| RTL | CLEAN | `receipts/diff_scope.log`: no HDL, firmware, builder or gitlink change. `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:116-122` (0.25-0.5 s holdover) is consistent with the new minimum. The design/rule conflict is S3 only. | R363-1 | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Robustness | UNCLEAN (F1, F2, F3, F4) | NOT RUN arms, boundaries, ordering and stream scoping in `check_release_mr`/`check_release_tu` (`:3553-3691`); probes A-H; `receipts/plan_diff.log` | R363-1 | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | `_ReleaseSoakChecks` `:5402-5566`; `tb/tools/torture_release_mutants.py` (44/44); `receipts/reviewer_mutants.log` (30/44 killed); `receipts/survivor_recheck.log` (18 survivors including text mutants); `receipts/selftest.log`; `receipts/behave_plan.log`; `receipts/behave_torture_tier.log` | R363-1 | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Docs | UNCLEAN (F1, F2) | `REQUIREMENTS.md:262-295`; `docs/testing/TESTING.md:910-1021`; assertion texts `:3388-3415`; `receipts/gates.log` (docs, style, paths, archive and feature-status gates rc 0; no U+2014 and no heading added) | R363-1 | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |

## Limits

- `check_em_dash.py` and `gen_toc.py --check/--verify-anchors` could not run here, because the pinned Markdown renderer is not installed and installs are not allowed. As substitutes, a scan of the added lines found no U+2014 and no new Markdown headings. The executor's published logs record rc 0 for both at this head.
- The full parent, PP, gPTP, Yosys and builder banks, Docker/act and hardware were not run, as instructed. The scoped simulator was not used, because nothing under RTL changed.
- Hosted checks were sampled at 19:38Z (`receipts/hosted_checks.log`):
  - successful: lint, Yosys shards 0-3, bdd-conformance, docs-check-no-git and full-ci-gate;
  - still in progress: Verilator shards 0/1/2/4, yosys-elaboration, docs-check and elaborate;
  - skipped: "Physical gPTP". A skipped context is not execution evidence.
- Source validation only. This is not a candidate-merge validation against live dev. No physical calibration and no bench evidence was produced.
- The clone was not modified. After all probes, HEAD, tree, index-tree, every tracked blob and mode, and all 4 gitlinks match, with no untracked, ignored or flagged files (`receipts/clone_integrity.log`).

## Pending manager duties

- Route F1-F5 back to the executor and re-review the corrected head across all five lenses. Coverage is banked per commit.
- Obtain an owner decision if F3 or F4 is to be accepted as text-only rather than fixed. Consider S3 (#387 against the corrected rule) with #74.
- Accept the hosted and act results for the exact head, build the current-dev candidate at the merge turn, and obtain explicit maintainer authorization before any merge.

R363-1 FINISHED
