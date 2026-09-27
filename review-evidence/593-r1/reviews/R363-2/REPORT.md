[R363] NEGATIVE - exact head 68e801b2823f75e037152f7eb2ac4c5dcda5d919

# R363-2: external independent re-review of PR #601 (issue #593)

- **Head:** `68e801b2823f75e037152f7eb2ac4c5dcda5d919`, tree `d385f231213eda4bb52414ef09cb3eaf8d663097`. The round-2 delta is one commit on `95bea7cf`, and the PR has two commits on base `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Both commit messages are one line with no trailers (`receipts/diff_scope.txt`).
- **Scope reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #593 body, assignment 5858876858 and scope note 5858887057;
  - the round-2 assignment 5859221324;
  - the #602 ruling 5859297355 (19:54:28Z) and the #602 assignment;
  - REQ-VER-06, TESTING 6d and GM_LOSS_RECOVERY.md;
  - then the diffs `6d5ebd73..68e801b2` and `95bea7cf..68e801b2`.
- **Diff scope:** 7 files: REQUIREMENTS.md, GM_LOSS_RECOVERY.md, TESTING.md, the planner, the mutation driver, the plan feature and its steps. No RTL, firmware, builder, `scripts/` or gitlink path changed (`receipts/diff_scope.txt`).
- **Verdict basis:** all five lenses were applied at this head. The planner's behaviour meets every round-2 item and my round-1 findings are all resolved, but two new MINOR findings are open, so the verdict is NEGATIVE:
  - F1 (Tests, Conformance): two boundaries of the new history oracle are not pinned by any killed mutant, so item 5 is not fully met.
  - F2 (Docs): the #602 text still describes a ruling that was already published as an open decision.

## Round-2 items at this head

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | A `tu` rise before its first recorded discontinuity fails | Met | `tb/tools/torture_campaign.py:3596-3597`. Probe I1a-I1h. Round-1 probe A1/A2 FAIL, A3 PASS. Mutants M08, M09, M10 and driver "tu rise correlation removed/made exclusive" killed. `test_release_tu_before_first_discontinuity` (`:5457`) is inverted as required. TESTING.md:1041-1044. |
| 2 | Every GM change is graded; `tu` never set, or cleared at that instant, fails | Met | `check_release_tu_history` `:3611-3653` is the plan's `tu_oracle` (`:3817`). Probe I2a-I2m. Round-1 B1/B2 FAIL. Mutants M02, M03, M05, M06 and M27 killed. Boundary gap: F1. |
| 3 | Resolution too coarse gives NOT RUN, with the derived limit stated | Met | `tu`: `:3582-3586` and `:3626`. `R < min(0.25, 0.5)`, shown as `resolution_limit_s=0.25`. `mr`: `:3762-3766`, `2R < 1 s`, shown as `0.5`. Plan args `:3815-3818`. REQUIREMENTS.md:268-270 and :303-305. TESTING.md:955-959 and :1022-1026. Probe I3a-I3h. Round-1 C1/C2 NOT RUN. Mutants M07 and M11-M14 killed. Residual semantics: S2. |
| 4 | One cause excuses at most one `mr` toggle per stream | Met | `:3683-3692` sorts causes, then consumes the earliest eligible cause for each toggle. Because all windows have the same width, this greedy choice finds a full matching whenever one exists. Probe I4a-I4f. Round-1 D1/D2 FAIL, D3 PASS. Mutants M15 and M16 killed. |
| 5 | Every new check and assertion text is pinned by a killed mutant | **Not fully met (F1)** | The driver kills 106/106 (`receipts/mutants.txt`). All my round-1 survivors and text mutants are killed now (`receipts/round1_*`). Reviewer mutants M01 (= R1-M48h) and M04 survive, and both are non-equivalent (`receipts/witness_survivors.txt`). |
| 6 | #602 referenced; PHC-only causes rejected; text matches the ruling | References and behaviour met; **text not (F2)** | REQUIREMENTS.md:280-282, TESTING.md:936-938 and GM_LOSS_RECOVERY.md:155 reference #602. `allowed` (`:3682`) excludes PHC and GM kinds. Probe I6: five PHC/GM/re-base kinds FAIL. Mutant M17 (PHC accepted) killed by `test_release_mr_gm_only`. |
| 7 | A capture short of the counter window gives NOT RUN; a MEDIA_RESET decrease is decoded as a reset | Met | Capture span `:3774-3789` with `ReleaseCapture` `:3727-3732`. Decrease `:3710-3712`. Probe I7a-I7n. Round-1 E1 NOT RUN, E2 PASS with an explicit span, F1 reason is "counter reset". Mutants M18-M25 killed. |
| - | PR #586 arms and mutants still pass | Met | All 25 #586 mutants are present: 22 verbatim and 3 re-anchored with an identical edit (`receipts/check586_mutants.txt`). All are killed in the 106 run. Six #586 tests changed (`receipts/tests_changed_586_diff.txt`), none weakened: the required rise inversion, SKIP→NOT RUN per the #593 decision, the new kind list and added phrases. |
| - | No firmware, RTL or builder change | Met | `receipts/diff_scope.txt` |

## Findings

**F1 - MINOR - Tests, Conformance - `tb/tools/torture_campaign.py:3640-3641` and `:3637`; `tb/tools/torture_release_mutants.py` - two boundaries of the new GM-history oracle are not pinned by any killed mutant**
- **Authority:**
  - Round-2 assignment 5859221324, item 5: "Every check added by this PR, and every new assertion text, is pinned by a killed mutant."
  - AGENTS.md section 6 Tests: each new test can fail for the defect it claims to detect.
- **Evidence:** with the unchanged 75-test self-test, two mutants survive (`receipts/reviewer_mutants.txt`, `receipts/round1_reanchored_mutants.txt`):
  - **M01 (= R1-M48h).** The per-interval GM list drops its `start_s - resolution_s` allowance. This is my round-1 M48, re-anchored. At round 1 it was killed on the single-interval entry, which is still pinned (R1-M48r killed). The history oracle, now the plan's `tu_oracle`, has no such pin.
  - **M04.** The separateness boundary `start_s <= intervals[-1][1]` becomes `<`. The driver removes the whole condition ("history interval order ignored", killed) but never moves its boundary.
  - **Both are non-equivalent** (`receipts/witness_survivors.txt`):
    - M01 witness: interval (0, 0.2) s, PHC step at 0, GM change at -0.0005 s, R = 1 ms. Head FAIL (`tu` held 0.2005 s after the GM change); mutant PASS.
    - M04 witness: touching intervals (0, 0.3), (0.3, 0.6). Head NOT RUN; mutant PASS.
- **Impact:** either regression turns a failing or undecidable history into PASS with every gate green. With M01, a GM change recorded just before the observed rise escapes the Annex B.1.1 minimum. The head's code is correct today; the defect is the missing pin.
- **Required outcome:** self-test arms that fail on each mutation, for example the M01 witness expecting FAIL and touching intervals expecting NOT RUN. Each needs a matching control in the driver that is killed.
- **Verification:** rerun `scripts/reviewer_mutants.py` and `scripts/round1_reanchored.py`. M01, M04 and R1-M48h must be KILLED, and the driver must still kill every control.
- **Lenses:** Tests, for the unpinned check. Conformance, because assigned item 5 is not fully met. Robustness is not attributed, because the head's behaviour on these inputs is correct.

**F2 - MINOR - Docs - `REQUIREMENTS.md:280-282`; `docs/testing/TESTING.md:936-938`; `docs/design/GM_LOSS_RECOVERY.md:155` - the PHC-step rule is still described as awaiting #602, although #602 ruled before this commit**
- **Authority:**
  - The #602 ruling 5859297355, at 2026-09-27T19:54:28Z, states: "a PHC step or presentation-time re-base alone is not an outgoing `mr` cause". Its basis is IEEE 1722-2016 §4.4.4.3, and it adds: "The #593 gate keeps rejecting PHC-only causes; the current image fails that check until this lands."
  - Commit `68e801b2` is dated 19:59:02Z.
  - Round-2 item 6 in this review's focus asks that the text match the ruling rather than an open question.
  - AGENTS.md section 6 Docs asks that changed contracts be reflected in authoritative docs.
- **Evidence:**
  - REQUIREMENTS.md:280-282: "[Issue #602] records the PHC-step conflict. Pending that decision, a PHC step alone remains no cause. A soak containing one fails on the current image."
  - TESTING.md:936-938: "records the conflicting PHC-step design contract. Pending its decision, this gate keeps the owner's rule."
  - GM_LOSS_RECOVERY.md:155: "release-rule conflict awaits #602 … Pending #602, a soak containing a PHC step fails the current release gate."
  - The enforced rule is exactly the ruling's (probe I6, M17 killed). Only the status and basis text are stale.
- **Impact:** normative REQ-VER-06 presents a decided rule as provisional, with the wrong basis. A cold reader could expect the PHC rule to flip.
  - "Fails on the current image" also gets no stated end condition in REQUIREMENTS.md or TESTING 6d.
  - The #602 assignment revises GM_LOSS_RECOVERY, TIME_SYNC and the compliance matrix, not REQUIREMENTS.md or TESTING 6d. So this text would stay stale after #602 lands.
- **Required outcome:** all three places cite the #602 ruling as decided: a PHC step or re-base alone is not an `mr` cause. They state that the current image fails the check until #602's datapath change lands.
- **Verification:** the three locations no longer say "Pending", "awaits" or "conflict" for a decided rule, and they link comment 5859297355. The docs gates pass.
- **Lenses:** Docs only. Conformance is not attributed, because the rule the gate enforces is identical to the ruling.

**S1 - SUGGESTION - Docs - `tb/tools/torture_campaign.py:3572-3581`, `:3755-3761`; `TESTING.md:959`, `:1026` - some early NOT RUN verdicts omit `resolution_limit_s`.** TESTING.md:1026 says "Each verdict records the measured resolution and applicable limits". But `check_release_tu`'s missing-evidence returns and `check_release_mr`'s incomplete-capture return carry no `resolution_limit_s` (`receipts/residual_probe.txt`). The verdict is NOT RUN either way. Consider setting the limit before the early returns, or scoping the sentence.

**S2 - SUGGESTION - Conformance - `tb/tools/torture_campaign.py:3582-3586` - the derived `tu` limit makes the minimum failable, not tight.**
- Near the limit, `clear + R >= GM + 0.25` passes almost any hold. At R = 0.24 s, a `tu` cleared 10 ms after a GM change passes, and 9.9 ms fails (`receipts/residual_probe.txt`).
- This matches item 3 as assigned: the limit is derived and stated, and it is the point beyond which the minimum can no longer fail. It also follows the benefit-of-doubt convention already decided for the 0.5 s bound.
- Consider asking the decision owner whether a practical ceiling (a fraction of 0.25 s) should apply to release evidence.

## Prior findings at this head

My round-1 findings (R363-1, comment 5859218049), re-checked with my own probes and mutants rerun at this head:

| Finding | Status | Evidence |
|---|---|---|
| F1 MAJOR (`tu` rise before first discontinuity) | Resolved | Round-1 probe A1/A2 FAIL, A3 PASS (`receipts/round1_oracle_probe_spans_at_head.txt`). Probe I1. Mutants killed. |
| F2 MAJOR (GM change never graded) | Resolved | B1/B2 FAIL. `check_release_tu_history`. Probe I2. The residual pin gap is new F1. |
| F3 MINOR (one cause, many toggles) | Resolved | D1/D2 FAIL, D3 PASS with spans supplied. Probe I4. |
| F4 MINOR (coarse resolution passes) | Resolved | C1/C2 NOT RUN. Probe I3. S2 records the residual semantics. |
| F5 MINOR (unpinned checks and texts) | Resolved for every listed mutant | My round-1 driver at head: 38 killed, 0 survived, 6 invalid anchors (`receipts/round1_reviewer_mutants_at_head.txt`). The 6 re-anchored (`receipts/round1_reanchored_mutants.txt`): 5 killed. R1-M26r is verdict-equivalent, with 0 differences over 972 inputs (`receipts/equivalence_m26r.txt`); its observable form is round-2 M02, which is killed. R1-M48h survives, which is new F1. Survivor and text recheck: every mutant is killed by the self-test (`receipts/round1_survivor_recheck_at_head.txt`). |
| S1 (capture span) | Taken and verified | E1 NOT RUN. Probe I7a-I7j. |
| S2 (decrease as wrap) | Taken and verified | F1 now reports "counter reset". Probe I7k/I7l. |
| S3 (PHC-step conflict) | Routed to #602 and ruled | The stale status text is new F2. |

In the survivor recheck, the copy tree's `@torture` behave column shows 8 errors, and those errors are in the baseline too. They come from `docs/reference/REGISTER_MAP.md` missing from that copy tree (CRF counter scenarios), not from the mutants. In the real clone the tier passes 232 scenarios with 0 failures (`receipts/behave_torture_tier.txt`).

The other reviewer's round-1 findings (R362-1, comment 5859211567) were read only after my independent pass:

| Finding | Status | Evidence |
|---|---|---|
| R362-1 F1, F2, F3 | Resolved | Same as my F1, F2 and F4 above. |
| R362-1 F4 (PHC `mr` conflict unrecorded) | Resolved by its own verification criterion: the reference is present and the decision is public | The stale status is retained as my F2. The datapath change is #602's scope, and this PR may not touch RTL. |
| R362-1 F5 survivors R08, R10-R13, R15-R17, R24, R26, R27, R29-R31 | Resolved | Each is killed at this head by my equivalent mutants: round-1 M12, M06, M15, M13, M22, M24, M28, M29, M32, M34 and T1/T2; round-2 M02, M23 and M24; driver "counter upper window widened". R13 is superseded by reset classification. |
| R362-1 S1 (shared cause) | Resolved | Item 4. |
| R362-1 S3 (reset label) | Resolved | Item 7. |
| R362-1 S2 (under-counting) and S4 (GM edge only in the discontinuity list) | Retained as suggestions, unassigned | Both still PASS (`receipts/residual_probe.txt`). The executor disclosed both. They have no coverage effect. |

## Commands run at the exact head (foreground)

| Command | Result | Receipt |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 75 tests OK, rc 0 | `receipts/selftest.txt` |
| `python3 -B tb/tools/torture_release_mutants.py` | 106/106 killed, source unchanged, rc 0 | `receipts/mutants.txt` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | 87 scenarios / 356 steps, rc 0 | `receipts/behave_plan.txt` |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 232 passed, 172 skipped, rc 0 | `receipts/behave_torture_tier.txt` |
| `git diff 6d5ebd73 68e801b2 --check`, `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` | rc 0 | `receipts/doc_gates.txt` |
| `check_em_dash.py --base 6d5ebd73`, `gen_toc.py --check` | rc 2: cannot judge, the pinned Markdown renderer is not installed. Substitute: no U+2014/U+2013 in added lines | `receipts/doc_gates.txt`, `receipts/emdash_substitute.txt` |
| `scripts/probe_r2.py` (head) | 59/59 met | `receipts/probe_r2_head.txt` |
| `scripts/probe_r2.py` (round-1 head via `scripts/round1_head_shim.py`) | 35/59 met: the probe tells the heads apart | `receipts/probe_r2_round1_head.txt` |
| `scripts/reviewer_mutants.py` (28 new mutants, at most 8 jobs) | 26 killed; M01 and M04 survive | `receipts/reviewer_mutants.txt` |
| `scripts/witness_survivors.py` | both survivors change a verdict | `receipts/witness_survivors.txt` |
| `scripts/round1/*` (my round-1 probe, mutants and recheck) and `scripts/round1_reanchored.py` | as tabled above | `receipts/round1_*` |
| `scripts/check586_mutants.py`, `scripts/tests_changed.py` | 25/25 #586 mutants kept; no #586 test weakened | `receipts/check586_mutants.txt`, `receipts/tests_changed*.txt` |
| `scripts/residual_probe.py`, `scripts/equivalence_m26r.py` | as cited | `receipts/residual_probe.txt`, `receipts/equivalence_m26r.txt` |
| `scripts/clone_integrity.sh` + `git submodule status` | clean (below) | `receipts/clone_integrity.txt` |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-2 items 1-7 against `tb/tools/torture_campaign.py:3562-3819`. IEEE 1722-2016 §4.4.4.3/§4.4.4.7 and Milan Annex B.1.1/B.1.2 and Table 5.4 as cited by the #593 decisions and the #602 ruling. `receipts/probe_r2_head.txt`, `receipts/round1_oracle_probe_spans_at_head.txt`, `receipts/residual_probe.txt` | R363-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| RTL | CLEAN | `receipts/diff_scope.txt`: no HDL, firmware, builder, `scripts/` or gitlink change. `receipts/rtl_context.txt`: `hdl/milan/milan_datapath.sv:3134-3137` still feeds `media_rebase_p_w` into `mcr_restart_p_w`, so the docs' "fails on the current image" is true. `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:116-119` (0.25-0.5 s holdover) is consistent with the graded minimum. The datapath change belongs to #602. | R363-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Robustness | CLEAN | `check_release_tu`, `check_release_tu_history`, `check_release_mr`, `_release_mr_toggles`, `_release_media_resets` and `ReleaseCapture` (`:3562-3796`). Checked: missing, None, NaN, bool, negative and coarse inputs; inverted, short, silent and incomplete captures; touching and overlapping intervals; cause ordering and foreign streams; counter decrease. Probe I1-I7 and C1-C5: 59/59 | R363-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Tests | UNCLEAN (F1) | `_ReleasePlanChecks`/`_ReleaseSoakChecks` (`:5457-5842`), `tb/tools/torture_release_mutants.py` (106/106), `tests/features/torture_campaign_plan.feature:459-462`, `tests/steps/torture_release_steps.py:266-316`. `receipts/reviewer_mutants.txt` (26/28), `receipts/round1_*`, `receipts/check586_mutants.txt`, `receipts/tests_changed_586_diff.txt`, `receipts/behave_*.txt` | R363-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |
| Docs | UNCLEAN (F2) | `REQUIREMENTS.md:262-309`, `docs/testing/TESTING.md:910-1057`, `docs/design/GM_LOSS_RECOVERY.md:155`, assertion texts `:3388-3424`. `receipts/doc_gates.txt`, `receipts/emdash_substitute.txt` | R363-2 | 68e801b2823f75e037152f7eb2ac4c5dcda5d919 |

## Limits

- **Two documentation gates not run.** `check_em_dash.py` and `gen_toc.py --check` could not run, because the pinned Markdown renderer is absent and installs are not allowed. The substitute scan of added lines found no U+2014/U+2013. The executor's round-2 comment reports rc 0 for all documentation gates at this head.
- **Public evidence is round-1 only.** The linked tree `59efc9fa` `review-evidence/593-r1` holds the executor's round-1 packet at `95bea7cf`; its gate JSON files record that head. No public evidence packet for `68e801b2` exists yet besides the executor's REVIEW READY comment. My own reruns above are the executable evidence at this head.
- **Scope of runs.** Not run: the full parent, PP, gPTP, Yosys and builder banks; `ci_scope --selftest`; `check_baremetal_only`; Docker/act; the host runner; hardware. The scoped simulator was not used, because no RTL changed.
- **Hosted checks, sampled 20:18:24Z** (`receipts/hosted_checks.txt`):
  - success: rtl-fast, verilator-lint, bdd-conformance, docs-check-no-git, full-ci-gate, yosys-elaboration, Yosys 0-3, Verilator 0 and 3, wire-accountability, changes;
  - still in progress: docs-check, elaborate, Verilator 1, 2 and 4;
  - skipped: "Physical gPTP". A skipped context is not execution evidence.
- **Source validation only.** This is not the current-dev candidate validation. No physical calibration or bench evidence exists; a field skip is not hardware proof.
- **Clone integrity.** Two ignored `__pycache__` directories created by my documentation-gate runs were removed. After all probes, HEAD, tree and index-tree equal the stated head. No tracked blob or mode mismatches, and no untracked, ignored or flagged files. The four gitlinks equal base and head; `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are checked out at their gitlinks (`receipts/clone_integrity.txt`).

## Pending manager duties

- Route F1 and F2 to the executor. Re-review the corrected head: Tests and Conformance for F1, Docs for F2. A change inside a covered lens's scope un-covers that lens.
- Decide whether S1, S2 and the retained R362-1 S2/S4 get follow-up Issues.
- Publish exact-head evidence for `68e801b2` or its successor. Accept the hosted and act results. Build the current-dev candidate at the merge turn. Obtain explicit maintainer authorization before any merge.

R363-2 FINISHED
