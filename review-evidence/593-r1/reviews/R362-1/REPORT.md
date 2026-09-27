[R362] NEGATIVE - exact head 95bea7cf82fcf7cf034c156ef7aa6800ee769e05

# R362-1 internal independent review: issue #593 / PR #601

- **Role:** internal independent reviewer. Cleared context, working in its own detached clone.
- **Head:** `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`, tree `0f33d799e9d44872cd4fae3ad1551cf85f2b5e1e`. This is one commit on dev `6d5ebd7357c1e468e446f18a61527c5be6118a04`, which includes PR #586. The message is one line with no trailers.
- **Changed paths:** `REQUIREMENTS.md`, `docs/testing/TESTING.md`, `tb/tools/torture_campaign.py`, `tb/tools/torture_release_mutants.py` and `tests/steps/torture_release_steps.py`.
  - No `hdl/`, `sw/`, `syn/`, builder, firmware or submodule path changed.
  - All four gitlinks match the base. See `receipts/scope_and_gitlinks.log`.
- **Authority, read in this order:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - The body of issue #593.
  - Assignment 5858876858 and scope note 5858887057.
  - The #396 correction 5857765949 and the earlier owner decision 5857762351 it supersedes.
  - The #396 round-4 and round-5 decisions, 5855792297 and 5856062292.
  - The routed suggestions R346-3 S1-S3 (PR #586, 5855777031) and R347-5 S1 (PR #586, 5856257320).
  - The cited clauses, extracted from the local standards PDFs: IEEE 1722-2016 4.4.4.3 and 4.4.4.7; Milan v1.2 Tables 5.4/5.6 and Annex B.1, B.1.1 and B.1.2 (`receipts/standards_clauses.md`).
  - After that, the diff, the history and the public evidence.
- **Prior review findings on PR #601:** none. PR #601 had no review, and no comment beyond the two review-start notices (`receipts/pr601_*.json`). This is the first round.

## Verdict summary

The seven arms in issue item 2 exist and behave as stated, and each is killed by a mutant. Cause windows are derived from the recorded resolution. The eight-PDU hold counts PDUs of the carrying stream only. Missing evidence gives NOT RUN, and nothing outside the rule changed behaviour.

The verdict is NEGATIVE for five reasons:

- **F1:** the routed R347-5 S1 is not implemented. The head's own test and 6d text still pin the opposite.
- **F2:** a GM change after which `tu` is never set is never graded.
- **F3:** a resolution too coarse to decide the new checks yields PASS.
- **F4:** the new rule contradicts the documented, decided PHC-step `mr` contract of the shipping datapath, and that conflict is not recorded.
- **F5:** 14 of 36 reviewer mutants survive, including removal of checks this head adds.

## Findings

### F1 - MAJOR - Conformance, Tests, Docs - a `tu` interval that rises before its first recorded discontinuity still passes (R347-5 S1 not implemented)

- **Where:**
  - `tb/tools/torture_campaign.py:3579`: containment is unchanged, `[observed_start - R, clear)`, with no bound on the first event.
  - `tb/tools/torture_campaign.py:5343-5349`: `test_release_tu_before_first_discontinuity` pins PASS for `(0, 10.4)` with a lone event at 10 s.
  - `docs/testing/TESTING.md:1007-1010`: "The decided rule permits uncertainty before its first recorded discontinuity ... Its lone discontinuity at 10 seconds satisfies this uncertainty check."
- **Authority:**
  - Scope note 5858887057 routes R347-5 S1 into items 1 and 2 "with no extra scope": "a `tu` interval that rises before its first recorded discontinuity must fail the containment check".
  - Assignment 5858876858 scopes items 1 and 2 "exactly as written".
  - The rationale of the round-5 decision (5856062292) is that the observed start lags its cause by at most the resolution.
- **Evidence:** `receipts/oracle_probe.log`, all at head:
  - S-R347-5-S1: the interval `(0, 10.4)` with an event at 10 gives PASS.
  - S1b: `(0, 1.2)` with an event at 1.0 gives PASS.
  - S1c: a GM change at 5.0 inside `(0, 5.3)` gives PASS.
  - The REVIEW READY comment on #593 does not mention R347-5 S1.
- **Impact:**
  - A spurious `tu` passes the release gate whenever any recorded discontinuity lands later in the same interval. This is a `tu` that rises seconds before any recorded discontinuity.
  - A routed scope item is unmet, and the tree pins the opposite behaviour in a test and in the testing contract.
- **Required outcome:**
  - An interval fails when its earliest contained recorded discontinuity lies more than the recorded resolution after the observed start.
  - The existing start-edge allowance of the round-5 decision is kept.
  - `test_release_tu_before_first_discontinuity` and TESTING.md:1007-1010 state the new rule.
  - A mutant that removes the bound is killed.
  - If the manager instead rules R347-5 S1 out of scope, that ruling is published and the scope note is corrected.
- **Verification:**
  - The unchanged `scripts/oracle_probe.py` gives FAIL for S-R347-5-S1, S1b and S1c.
  - `test_release_tu_start_resolution` keeps its expectations.

### F2 - MAJOR - Conformance, Robustness, Tests - a GM change after which `tu` is never set is never graded (B.1.1 minimum bypassed at zero duration)

- **Where:**
  - `tb/tools/torture_campaign.py:3553-3590`: the only `tu` oracle grades one observed interval. GM changes are consulted only when they precede that interval's clear (`:3584`).
  - `docs/testing/TESTING.md:988-992`: the procedure is "Use `check_release_tu`" per interval.
  - `REQUIREMENTS.md:288-291`.
- **Authority:**
  - Issue #593 item 1: "After a GM change, `tu` stays set for at least 0.25 s (Milan Annex B.1.1)".
  - Correction 5857765949: "after a grandmaster change, `tu` stays set for at least 0.25 s".
  - REQUIREMENTS.md:288: "After every GM change, `tu` remains set for 0.25 seconds."
- **Evidence:**
  - Probe B1 (`receipts/oracle_probe.log`): an interval `(0, 0.3)` with GM changes at 0 and 0.5 gives PASS. The GM change at 0.5 s has no `tu` after it and is never examined.
  - With no `tu` interval at all there is nothing to call.
  - No function, plan argument or 6d instruction maps each recorded GM change to a covering interval.
- **Impact:** a talker that does not set `tu` on a GM change passes the gate. This is the most direct B.1.1 violation. Item 2's arm ("`tu` held under 0.25 s after a GM change fails") covers only intervals that exist.
- **Required outcome:**
  - Every recorded GM change in the observation window is graded.
  - It must be covered by a `tu` interval that contains it (with the stated start allowance) and meets the 0.25 s minimum.
  - A GM change with no covering interval fails. Missing interval evidence is NOT RUN.
  - A self-test arm and a killed mutant cover this.
- **Verification:** a new arm "GM change, no `tu` interval -> FAIL" passes and its mutant is killed. Probe B1 reads FAIL.

### F3 - MINOR - Conformance, Robustness, Tests - a resolution too coarse to decide the new checks yields PASS, not NOT RUN (R346-3 S1)

- **Where:**
  - `tb/tools/torture_campaign.py:3570-3571`: `tu` accepts any finite resolution of zero or more.
  - `:3588`: the GM minimum.
  - `:3674-3676` and `:3622-3624`: the `mr` cause window.
  - `REQUIREMENTS.md:282-284`.
- **Authority:**
  - Scope note 5858887057 routes R346-3 S1: "the `tu` resolution must come from wire or event timestamps, not the 60 s periodic read".
  - Assignment 5858876858: timing is "judged against the recorded resolution", and "Missing evidence for a check is a NOT RUN, never a PASS".
- **Evidence:** `receipts/oracle_probe.log`:
  - S-R346-3-S1: with R = 60 s, a `tu` interval held 60 s gives PASS.
  - S1b: with R = 0.3 s, a `tu` clearing 0.01 s after a GM change gives PASS. For any R of 0.25 s or more, `:3588` cannot fail, because clear is always later than the GM change.
  - S1c: with R = 1 s, an `mr` cause 0.9 s from the toggle is accepted.
  - The resolution is a bare float with no provenance and no ceiling. The wire-source rule exists only as text. That text predates this head, but the GM minimum and the `mr` window added here are what make a coarse resolution decisive.
- **Impact:** evidence that cannot resolve 0.25 s, 0.5 s or a coincidence window still qualifies as PASS.
- **Required outcome:** one of the following, each with self-test arms and killed mutants:
  - A resolution that cannot decide the check it feeds yields NOT RUN. At minimum, R of 0.25 s or more gives NOT RUN for the GM minimum, and there is a stated ceiling for the 0.5 s bound and for the `mr` window.
  - Or the resolution record carries its source, and the periodic publication cadence is refused.
  - Or the manager records publicly that the text-only contract is sufficient.
- **Verification:** probes S-R346-3-S1, S1b and S1c read NOT RUN or FAIL.

### F4 - MINOR - Conformance, RTL, Docs - the new rule fails the datapath's decided PHC-step `mr` toggle, and the conflict is not recorded

- **Where:**
  - The new rule: `docs/testing/TESTING.md:935` ("A GM edge or PHC step alone is no cause.") and `REQUIREMENTS.md:262-265`.
  - The existing contract:
    - `hdl/milan/milan_datapath.sv:3124-3137`. Here `mcr_restart_p_w = ... | media_rebase_p_w`: a PHC step restarts the media clock "whichever clock source is selected".
    - `docs/design/GM_LOSS_RECOVERY.md:155-156`: "Outgoing `mr` (IEEE 1722-2016 4.4.4.3) | Toggles once", with MEDIA_RESET counting it. This is #387 decisions 5606198212/5794731090.
- **Authority:**
  - AGENTS.md section 2: conflicts are published and marked as needing a decision.
  - Section 6, `RTL` lens: "Existing module/interface contracts remain valid".
  - Section 6, `Docs` lens: changed contracts are reflected in authoritative documents.
- **Evidence:**
  - Under the head's oracle, a toggle whose only recorded event is a PHC step fails (probe A4b).
  - The shipping image toggles `mr` on every PHC step by design. So any soak that includes a PHC step fails the new gate on the current image.
  - The REVIEW READY comment names this as a "review boundary". No Issue, decision or cross-reference records it.
  - #593 routes only the CRF-disruption behaviour to #74. #74's open item is "Gate media-clock-restart propagation and `mr` on the selected CRF source", not the PHC-step toggle.
- **Impact:** two in-tree authorities disagree on whether a PHC-step `mr` toggle is conformant. A cold reader of the design row cannot learn that the release gate fails it.
- **Required outcome:**
  - The conflict is recorded as a public decision item: a new Issue or an explicit owner or manager ruling.
  - It is referenced from REQ-VER-06/6d or from the design row.
  - No RTL change is needed in this PR.
- **Verification:** the reference is present, and the decision item is public.

### F5 - MINOR - Tests - checks added by this head survive their removal

- **Where:**
  - `tb/tools/torture_campaign.py:5402-5566` (`_ReleaseSoakChecks`).
  - `:5351-5363` (`test_release_assertion_text`).
- **Authority:**
  - Issue item 2 ("mutants removing each check").
  - Scope note 5858887057 routes R346-3 S3 (pin the assertion texts).
  - AGENTS.md `Tests` lens: each new test can fail for the defect it claims.
- **Evidence:** `receipts/reviewer_mutants.log` has 36 reviewer mutants. 22 are killed and 14 survive the unchanged self-test. All 14 also survive the behave plan feature (`receipts/reviewer_mutants_behave.log`). The survivors:
  - **Counter checks:**
    - R10: the MEDIA_RESET read stream filter is removed.
    - R11: a single read is accepted, so a missing endpoint read gives PASS instead of NOT RUN.
    - R12: the read-order check is removed.
    - R13: the 32-bit wrap decode is removed. The wrap arm at `:5495-5497` passes either way, and a counter decrease then passes.
    - R15 and R16: the upper counter window drops R, or widens by 1 s.
  - **PDU and `tu` checks:**
    - R08: the PDU timestamp-order check is removed.
    - R24: the GM-minimum `< clear` filter is unpinned.
    - R26: the 0.5 s bound guard is removed.
    - R27: a zero-length interval is accepted.
    - R17: the counter window consumes the latest matching toggles instead of the earliest.
  - **Unpinned assertion text:**
    - R29: the new `tu` GM-minimum text.
    - R30: the MEDIA_RESET interval text.
    - R31: NOT RUN in the release-evidence text.
  - The executor's own driver kills all 44 (`receipts/release_mutants.log`), including the seven required arms.
- **Impact:** these checks can be deleted with every gate green. R11 and R13 turn missing or reset counter evidence into PASS with no failing test.
- **Required outcome:** each check this head adds is killed by a named test. At minimum that covers R10-R13, R15, R16, R26 and R29-R31. Any survivor claimed to be equivalent is argued in public.
- **Verification:** rerun the unchanged `scripts/reviewer_mutants.py`.

### Suggestions (non-blocking; no effect on coverage)

- **S1 - Conformance, Robustness - one recorded cause excuses several toggles.**
  - Probe E1: two toggles eight PDUs apart, both within ±R of one cause, give PASS. The net `mr` level is unchanged, but a listener sees two restarts.
  - IEEE 1722-2016 4.4.4.3 toggles "each time a media clock restart is needed".
  - Optional: each toggle consumes a distinct cause, or the sharing is stated as intended.
- **S2 - Conformance - under-counting is not graded.**
  - Probe E2: a caused toggle with no MEDIA_RESET increment passes. Tables 5.4/5.6 require the increment.
  - This is outside item 1's wording. Optional.
- **S3 - Robustness, Docs - a restart reset is mislabelled.**
  - Table 5.4 resets output MEDIA_RESET to 0 at every stream start.
  - The modulo decode reports that as "MEDIA_RESET increment without a distinct caused toggle", with a delta of 4294967293 (probe E3). It fails closed, but under the wrong label. TESTING.md:959 assigns resets to the counter-walk assertion.
  - Optional: detect a decrease and report it as a reset.
- **S4 - Robustness, Tests - `tu` evidence is a list of unkinded floats.**
  - A GM-identity edge supplied only in `discontinuities_s`, with `gm_changes_s=[]`, skips the minimum (probe B2). The plan's `tu_discontinuity_kinds` (`:3719`) lists that edge as a discontinuity kind.
  - The head's round-4 arm at `:5298` models the round-4 GM edge that way.
  - Optional: kinded records, or require every GM-identity discontinuity to appear in the GM history.

## Assignment checks

1. **Item 2 arms and their mutants: met.**
   - Every arm exists and grades as stated, per `receipts/oracle_probe.log` A1-A7b and `receipts/selftest.log`:
     - a clock-source change, a CRF disruption or a received CRF `mr` toggle each give PASS;
     - no cause, a GM-only cause and a PHC-only cause each give FAIL;
     - a hold of 7 PDUs gives FAIL, and 8 gives PASS;
     - a MEDIA_RESET increment without a cause gives FAIL;
     - `tu` 0.24 s after a GM change gives FAIL, and 0.25 s at R = 0 gives PASS.
   - The executor's driver kills all 44 mutants, and 19 of them are new. My own mutants kill the arm checks too: R01-R07, R09, R14, R18-R23, R25 and R28, plus R32-R36. Other checks survive (F5).
2. **Windows and routed suggestions: partly met.**
   - Causes are matched from recorded, kinded, stream-scoped events inside `[toggle - R, toggle + R]`. The window scales with R from 0.0001 to 0.1 (probe W1-W3), and no literal is used. The counter lag uses the Milan 1 s ceiling (`MILAN_MAX_OBSERVATION_INTERVAL_S = 1.0`, `:287`).
   - The eight-PDU hold counts only the carrying stream's PDUs. Foreign PDUs interleaved between toggles do not count (H1-H3).
   - The resolution source is text only (F3).
   - R347-5 S1 is not implemented (F1).
   - R346-3 S2 is implemented. R346-3 S3 is only partly implemented (F5).
3. **Missing evidence: met.** Missing evidence gives NOT RUN and never PASS:
   - all `None` or incomplete inputs, packet gaps, an unfinished tail, a single or foreign read, and unordered reads;
   - 2000 fuzzed corrupt inputs, which gave 0 PASS.
   - NOT RUN makes `exit_code` 2, and `release.complete-evidence` lists it as non-qualifying.
4. **Behaviour outside the rule: unchanged.**
   - Plan JSON for all nine areas, base against head (`receipts/plan_diff.log`): 312 steps each. Only the soak step changed. The two power steps changed only through the shared release-evidence text, which gained "NOT RUN".
   - The checklist and per-area coverage outputs are byte-identical (`receipts/checklist_diff.log`, `receipts/coverage_diff.log`).
   - PR #586's 25 mutants are still killed. Its `tu` arms keep their verdicts. SKIP became NOT RUN by design, and `gm_changes_s=[]` was added.
   - REQUIREMENTS and TESTING cite the clauses and restate only what the checks need (`receipts/standards_clauses.md`).
   - No firmware, RTL or builder change.

## Lens coverage (reviewer format)

```text
[R362] UNCLEAN Conformance - issue #593 items 1-2; decisions 5858876858, 5858887057, 5857765949; REQUIREMENTS.md:262-292; TESTING.md:915-1020; torture_campaign.py:3388-3420, :3548-3722; receipts/standards_clauses.md, oracle_probe.log - cited clauses verified against the standards text; mr causes, the per-stream hold, MEDIA_RESET interval semantics and the NOT RUN rule conform; open F1 (MAJOR), F2 (MAJOR), F3 (MINOR), F4 (MINOR).
[R362] UNCLEAN RTL - receipts/scope_and_gitlinks.log, clone_integrity.log; hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:115-122; hdl/milan/milan_datapath.sv:3120-3137 - no RTL, firmware, builder or submodule change; the 0.25-0.5 s holdover the tu checks rely on is at the cited lines; the documented PHC-step mr contract no longer satisfies the new requirement: open F4 (MINOR).
[R362] UNCLEAN Robustness - torture_campaign.py:3553-3722; receipts/oracle_probe.log (NOT RUN arms, 2000-input fuzz, gaps, wrap, ordering, foreign streams) - malformed and missing inputs never pass; open F2 (MAJOR), F3 (MINOR).
[R362] UNCLEAN Tests - torture_campaign.py:5294-5566; torture_release_mutants.py; tests/steps/torture_release_steps.py; receipts/selftest.log (66 OK), release_mutants.log (44/44), behave_plan.log (86 scenarios), behave_torture_tier.log (231 scenarios), reviewer_mutants.log (22/36), reviewer_mutants_behave.log - open F1 (MAJOR), F2 (MAJOR), F3 (MINOR), F5 (MINOR).
[R362] UNCLEAN Docs - REQUIREMENTS.md:262-292; TESTING.md:915-1020; GM_LOSS_RECOVERY.md:155-156; receipts/gate_docs_check.log, gate_em_dash.log, gate_doc_style.log, gate_doc_paths.log, gate_gen_toc.log, gate_gen_toc_anchors.log, gate_feature_status.log, gate_py_idiom.log (all rc 0) - gates are clean; open F1 (MAJOR: 6d pins the opposite rule) and F4 (MINOR).
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | REQUIREMENTS.md:262-292; TESTING.md:915-1020; torture_campaign.py:3388-3722; the #593 and #396 decisions; IEEE 1722-2016 4.4.4.3/4.4.4.7; Milan v1.2 Tables 5.4/5.6, B.1.1, B.1.2 | R362-1 (applied, not covered clean) | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| RTL | UNCLEAN (F4) | scope and gitlink receipts; KL_ptp_clock_validity.sv:115-122; milan_datapath.sv:3120-3137 | R362-1 (applied, not covered clean) | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Robustness | UNCLEAN (F2, F3) | torture_campaign.py:3553-3722; oracle_probe.log | R362-1 (applied, not covered clean) | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Tests | UNCLEAN (F1, F2, F3, F5) | torture_campaign.py:5294-5566; torture_release_mutants.py; torture_release_steps.py; self-test, behave and mutant receipts | R362-1 (applied, not covered clean) | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |
| Docs | UNCLEAN (F1, F4) | REQUIREMENTS.md; TESTING.md; GM_LOSS_RECOVERY.md:155-156; documentation gate receipts | R362-1 (applied, not covered clean) | 95bea7cf82fcf7cf034c156ef7aa6800ee769e05 |

## Commands run at the exact head (foreground; receipts under `receipts/`)

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 66 tests OK |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0, 44/44 killed, source unchanged |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | rc 0, 86 scenarios, 353 steps |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0, 231 scenarios passed, 172 excluded by tag |
| `scripts/oracle_probe.py <clone>` (new) | 64 cases: 53 met, 10 not met (F1, F2, F3, S1, S2, S4), 1 informational (S3 detail) |
| `scripts/reviewer_mutants.py <clone> <scratch>` (new; at most 8 jobs) | 36 mutants: 22 killed, 14 survived; the clone's planner is unchanged |
| The 14 survivors run against the behave plan feature (scratch copy) | all rc 0, so none is killed there; the scratch planner was restored |
| `scripts/plan_diff.py` on base and head `--plan --json` (all areas); checklist and coverage-by-area diffs | only the soak step changed, plus the shared evidence text; the other diffs are empty |
| `docs_check.py`; `check_doc_style.py`; `check_doc_paths.py`; `check_feature_status.py`; `check_py_idiom.py` | rc 0 each |
| `check_em_dash.py --base 6d5ebd73...`; `gen_toc.py --check`; `gen_toc.py --verify-anchors` (pinned renderer, hash-locked install in a disposable venv) | rc 0 each (0 findings over 77 added lines, arms 339/339) |
| `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check` | rc 0; rc 0 |
| `git diff --check 6d5ebd73... HEAD` | rc 0 |
| Clone integrity after the probes | clean; tracked bytes, modes, index and the four gitlinks match the head (`receipts/clone_integrity.log`) |

## Real limits

- **Desk review only.** No hardware, bench, Docker, act, host runner, or full parent, PP, gPTP, Yosys or builder bank was run.
  - Physical calibration was NOT RUN, and no field skip is taken as hardware proof.
  - The scoped Verilator was not used, because the diff contains no RTL.
- **Manager banks.** The manager's source banks at this head were not rerun. The public evidence tree `59efc9fa` `review-evidence/593-r1` contains only the author packet and its manifest (`receipts/evidence_manifest_593-r1.json`). This review relies on its own reruns.
- **Hosted checks** were snapshotted once, at 19:39Z (`receipts/hosted_checks_snapshot.txt`):
  - Succeeded: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3/4 and Verilator shard 3/5.
  - In progress: `docs-check`, `elaborate`, and Verilator shards 0, 1, 2 and 4.
  - Skipped: `Physical gPTP (nightly and manual)`.
  - No conclusion is drawn from in-progress or skipped contexts.
- **Standards scope.** Standards checks cover only the clauses the diff cites.

## Pending manager duties

- Route F1-F5 to a new round. F4 needs a public decision item (the #387 PHC-step `mr` toggle against the corrected rule). S1-S4 are optional.
- Hosted and act acceptance at the exact head. Then the current-dev candidate build at the merge turn (source base `6d5ebd73`), with its merge-tree validation and post-merge containment.
- The external review (R363) and a re-review of the corrected head. Merge requires two independent positive reviews and the full AGENTS.md section 7 bar.

R362-1 FINISHED
