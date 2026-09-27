[R362] POSITIVE - exact head 7a051e618677ecd907ed04b086afbdfe374b4336

# R362-3 internal independent review: issue #593 / PR #601

- **Head:** `7a051e618677ecd907ed04b086afbdfe374b4336`, tree `11b049b34313cb1a23a0a4578e3d77086e5413e4`.
- **Source base:** `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- **Delta under review:** `68e801b2..7a051e61`, one commit. The whole PR diff `6d5ebd73..7a051e61` was re-read where the round-3 items reach back into it: the PR #586 arms and mutants, and the GM-history oracle.
- **Order of reading:** context was rebuilt from public state only, in this order:
  1. AGENTS.md and CONTRIBUTING.md; docs/README.md.
  2. The #593 body and manager comments 5858876858, 5858887057, 5859221324 and 5859532913 (the round-3 assignment).
  3. The #602 body and ruling 5859297355.
  4. REQ-VER-06; TESTING 6d; GM_LOSS_RECOVERY "Media re-base on a PHC step".
  5. The diff and history, then public evidence.
- **Prior findings:** my own R362-2 findings were re-verified by re-running my round-2 probes and mutants. The other reviewer's round-2 findings were read only after this verdict and ledger were written. See "Prior findings: resolved or retained".

## Summary

All four round-3 items are met at this head. PR #586's controls still kill. No firmware, RTL or builder path changed. No `BLOCKER`, `MAJOR` or `MINOR` finding is open. Three `SUGGESTION`s follow; none of them affects coverage.

| Round-3 item | Result | Evidence |
|---|---|---|
| **1. Two-sided `tu` model**<br>The minimum is decided only when `2R < 0.25 s`; the 0.5 s bound uses the same model; the derivation is stated consistently; I3e/f/g do not PASS; I3h FAILs; the limit is pinned | **Met** | **Code:**<br>- `torture_campaign.py:3327-3328`: `RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2`.<br>- `:3590` and `:3634`: NOT RUN at `R >= 0.125` in both oracles.<br>- `:3614`: minimum FAIL when `h + R < 0.25`.<br>- `:3604-3616`: upper PASS iff `clear + R <= last + 0.5 + R`, that is `h <= 0.5`.<br>**Probes** (`receipts/r3_behaviour.out`):<br>- D0 is a sweep over 15 resolutions × 5 observed holds in `(0, R]`, both oracles. A true instant clear never PASSes; it FAILs for every R < 0.125 and is NOT RUN for every R ≥ 0.125.<br>- D1: the minimum is decided exactly at `h + R >= 0.25`, over 2 595 points.<br>- D2: the upper check PASSes iff `h <= 0.5`, for R up to 0.124999.<br>**Round-2 probes, unchanged** (`receipts/r362_2_behaviour_at_7a051e61.out`, sha256 equal to the R362-2 manifest): I3e, I3f and I3g are NOT RUN; I3h is FAIL. I3i, a 0.3 s hold at R = 0.2, is now NOT RUN; the new limit requires that.<br>**Derivation text:** the same eight-step derivation appears at `REQUIREMENTS.md:304-313`, `TESTING.md:1024-1037` and `torture_campaign.py:3425-3430`.<br>**Pinning:** the one-sided-limit mutant is killed (`torture_release_mutants.py:527`), as are my R3-05/06/07/09/10 and C15r/C20r/C21r |
| **2. Every check this PR adds, both GM-history boundaries, and every new assertion text pinned by a killed mutant** | **Met** for every check and text.<br>One survivor is verdict-equivalent. Metadata-only survivors are listed under S1 | **PR driver:** 132/132 killed (`receipts/mutants_head.txt`).<br>**Round-2 driver, re-run:** 54 killed and 0 survivors; 13 anchors are gone or collide (`receipts/r362_2_mutants_at_7a051e61.out`). All 13 are accounted:<br>- 7 are re-anchored and killed: C10r, C15r, C17r-C21r (`receipts/r3_extra.txt`).<br>- 4 texts are re-anchored to full literals and killed: T20r, T21r, T22r, T24r.<br>- T19 and T23 target text that round 3 replaced; its replacement is killed as R3-29/30/31.<br>**Round-2 survivors:** C06, C07, C09, C34, C35 and C38 are now killed. T05 and T13 are killed.<br>**New reviewer mutants** (`receipts/r3_mutants.txt`): of 39, every verdict or text mutant except R3-21 is killed or crashes the self-test. R3-35 and R3-37 change only verdict metadata (S1).<br>**GM-history boundaries:**<br>- The `:3645` separation and both `:3648-3649` assignment edges are killed by `test_release_tu_history_boundaries`.<br>- The second-loop edges at `:3658` are killed as R3-15/16/17/18.<br>**The one verdict survivor, R3-21:** it removes the history's own `clear_s <= start_s` guard. That guard is redundant, because `check_release_tu` refuses the same interval at `:3588`. The witness `receipts/r3_21_witness.out` shows 0 verdict differences over 15 cases |
| **3. #602 ruling stated and cited, and the current image's failure stated plainly** | **Met** | The ruling link (issuecomment-5859297355) and the sentences "The current image still toggles `mr` on PHC steps. A soak containing one therefore fails the step-only check. This remains until #602's RTL change lands." appear at:<br>- `REQUIREMENTS.md:280-283`<br>- `TESTING.md:936-939`<br>- `GM_LOSS_RECOVERY.md:155`, which also says "The current image still toggles". That claim matches `hdl/milan/milan_datapath.sv:3135-3137` (`\| media_rebase_p_w`) |
| **4. Reset wording fixed; every NOT RUN records `resolution_limit_s`** | **Met** | **Reset wording:** `TESTING.md:969-974` adds "Even an explained talker restart interrupts the continuous soak", which reconciles the fail-on-decrease rule with the table's "no unexplained resets" (R362-2 S1).<br>**NOT RUN metadata:** 16 of 16 NOT RUN paths across `check_release_tu`, `check_release_tu_history` and `check_release_mr` carry both `resolution_limit_s` and `observation_resolution_s` (probes N-* in `receipts/r3_behaviour.out`). Five FAIL paths also carry R (probes F-*) |
| PR #586's arms and mutants still pass | **Met**, with one arm flipped by the round-3 decision (S2) | **Controls:** replaying PR #586's own 25 controls against the head planner (`receipts/base586_controls_replay.txt`) gives:<br>- 24 killed on unchanged anchors.<br>- 1 ("tu oracle accepts an uncorrelated interval") re-anchored to `{..., **detail}` with the same replacement, and killed in the PR driver.<br>The raw unchanged driver stops at that anchor (`receipts/base586_mutants_on_head.txt`).<br>**Arms:** the only #586 arm whose expectation changed in round 3 is `(0.76, [0, 0.25], 0.01)` at `torture_campaign.py:5425`, from PASS to FAIL. With `h = 0.51 > 0.5`, the decision's "must not admit a true hold beyond 0.5 s plus R" requires FAIL. The new `(0.75, ..., 0.01, PASS)` arm keeps the boundary pair |
| No firmware, RTL or builder change | **Met** | `receipts/scope.txt`:<br>- The whole PR touches seven files, all planner, mutants, feature, steps or docs.<br>- All modes are 100644 and unchanged.<br>- The four gitlinks are identical at base and head |

## Findings

No `BLOCKER`, `MAJOR` or `MINOR` finding.

### S1: SUGGESTION. Lens: Tests. Verdict-metadata recording is only partly mutation-pinned

- **Where:**
  - `tb/tools/torture_campaign.py:3798-3801`: `_release_mr_toggles` NOT RUN/FAIL is returned via `detail`.
  - `:3797`: capture-window NOT RUN.
  - `:3776`: invalid-record NOT RUN.
  - `:3600`: uncorrelated FAIL.
  - `:3602`: rise FAIL.
  - `:3660`: uncovered-GM FAIL.
- **Evidence:** `receipts/r3_extra.txt` V01, V04, V05, V06, V07 and V10, with R3-35 and R3-37 as duplicates in `receipts/r3_mutants.txt`. Dropping `detail` from these returns leaves every self-test green. The behaviour is correct at this head: probes N-* and F-* show R and the limit on each of these paths.
- **Why not counted:**
  - None of these mutants changes a verdict.
  - Item 2 pins checks and assertion text.
  - The R363-2 S1 item asks for the metadata to be recorded, and it is.
  - This follows R362-2's treatment of the `cause_window` detail string (C38), which was not counted either.
- **Impact:** a later refactor could drop R from those verdict records unnoticed, although REQ-VER-06 says "Resolution appears in every timing verdict". The PR body's "Pin ... missing-evidence metadata with mutation controls" is true only for the entry guards and history paths.
- **Optional outcome:** assert `observation_resolution_s` and `resolution_limit_s` on one inner `mr` NOT RUN (packet gap or unfinished tail), the capture-span NOT RUN, and one `tu` FAIL.

### S2: SUGGESTION. Lenses: Tests, Docs. Disclose the flipped PR #586 arm

- **Where:** `tb/tools/torture_campaign.py:5425`, `(0.76, [0, 0.25], 0.01, "PASS")` → `"FAIL"`.
- **Evidence:** the flip is required by the round-3 decision (D3 and D3b in `receipts/r3_behaviour.out`). The PR body's Round 3 section does not name it. The assignment's "PR #586's arms ... still pass" is therefore true only as superseded by item 1.
- **Optional outcome:** one PR-body line naming the arm and the clause that flipped it. The round-2 SKIP→NOT RUN changes were disclosed the same way.

### S3: SUGGESTION. Lens: Docs. The #602-owned design rows (for #602's deliverable 2, not this PR)

- **Where:** `docs/design/GM_LOSS_RECOVERY.md:156`.
- **Evidence:** the "Talker MEDIA_RESET" row's "Decided reaction" still reads "Counts that one toggle". Ruling 5859297355 supersedes "the step-only MEDIA_RESET that follows from it" and assigns the MEDIA_RESET row to #602's documentation deliverable. The round-3 assignment asked only for the "Outgoing `mr`" row, which is done.
- **Optional outcome:** #602's documentation change updates this row together with the RTL. No change is needed in this PR.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **Code against the round-3 assignment 5859532913 items 1-4, #602 ruling 5859297355, Milan v1.2 Annex B.1.1/B.1.2 and IEEE 1722-2016 4.4.4.3/4.4.4.7:**<br>- `torture_campaign.py:3327-3328`, `3406-3430`, `3568-3661` and `3743-3804` (the three release oracles).<br>- `3807-3843` (the plan arguments).<br>**Probes:**<br>- `receipts/r3_behaviour.out`: 39/39 as required.<br>- `receipts/r362_2_behaviour_at_7a051e61.out`: 37 as required at round 2. The 4 changed outcomes (I3e/f/g/i) are exactly those the round-3 decision re-specifies | R362-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| RTL | CLEAN | `receipts/scope.txt`: no `hdl/`, firmware, builder or gitlink change in `6d5ebd73..7a051e61`. The GM_LOSS_RECOVERY.md:155 claim "the current image still toggles" matches `hdl/milan/milan_datapath.sv:3135-3137` at head. That RTL defect is #602's deliverable 2, and this PR's gate fails any soak that exercises it | R362-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Robustness | CLEAN | Coarse, equal-to-limit, negative, None, NaN, infinite, zero-length, reversed and touching inputs to `check_release_tu` and `check_release_tu_history` (N-*, D6b, D7a/b, `r3_21_witness.out`). `mr` gap, unfinished tail, invalid kind, short capture span, unordered reads, a single read and coarse R (N-mr-*). Every case is NOT RUN, with the limit recorded; none is PASS | R362-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Tests | CLEAN (S1, S2 are suggestions) | **Code:** `torture_campaign.py:5413-5430`, `5474-5496`, `5686-5712` and `5751-5900` (new and changed tests); `torture_release_mutants.py:18-613`.<br>**Receipts:**<br>- `receipts/selftest.txt`: 78 tests OK.<br>- `receipts/mutants_head.txt`: 132 killed.<br>- `receipts/base586_controls_replay.txt`: 25/25.<br>- `receipts/r362_2_mutants_at_7a051e61.out`: 54 killed, 0 survived.<br>- `receipts/r3_mutants.txt`: 39; 34 killed, 2 crash-only, 1 equivalent survivor, 2 metadata survivors.<br>- `receipts/r3_extra.txt`: 24; 18 killed, 6 metadata survivors.<br>- `receipts/behave_plan.out`: 87 scenarios | R362-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Docs | CLEAN (S2, S3 are suggestions) | **Text:** `REQUIREMENTS.md:262-315`, `docs/testing/TESTING.md:910-1067` and `docs/design/GM_LOSS_RECOVERY.md:142-158`. Checked against the code, the ruling, and each other: the derivation is identical in REQ-VER-06, TESTING 6d and the assertion text, and no stale `min(0.25, 0.5)` or "pending #602" text remains.<br>**Gates** (`receipts/docs_gates.out`), all rc 0 with the pinned renderer:<br>- `docs_check.py`<br>- `check_em_dash.py --base 6d5ebd73` and `--selftest`<br>- `check_doc_style.py`<br>- `check_doc_paths.py`<br>- `gen_toc.py --check` and `--verify-anchors`<br>- `check_feature_status.py --self-test`<br>- `check_archive.py`<br>- `git diff --check` over both ranges | R362-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |

## Commands run at this head

All commands ran in the foreground. Receipts are under `receipts/` and scripts under `scripts/`.

| Command | Result | Receipt |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 78 tests OK | `selftest.txt` |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0, 132 killed | `mutants_head.txt` |
| PR #586's own `torture_release_mutants.py` (at `6d5ebd73`) against the head planner, raw | Stops at the one re-anchored control, after 11 kills | `base586_mutants_on_head.txt` |
| `scripts/base586_controls.py` (PR #586's 25 controls, skipping only moved anchors, which it accounts) | 24 killed, 1 re-anchored equivalent; 0 problems | `base586_controls_replay.txt` |
| `scripts/r2/r362_2_behaviour.py` (unchanged from R362-2) | 37 OK, 4 changed by the round-3 decision | `r362_2_behaviour_at_7a051e61.out` |
| `scripts/r2/r362_2_mutants.py` (unchanged) | 54 killed, 0 survived, 13 anchors gone or colliding | `r362_2_mutants_at_7a051e61.out` |
| `scripts/r2/r362_2_survivor_witness.py` (unchanged) | C06/C07/C09 still distinguishing, then stops on C10's moved anchor. The survivors it witnessed are all killed now | `r362_2_survivor_witness_at_7a051e61.out` |
| `scripts/r3_mutants.py` | 39: 34 killed, 2 crash-only, 3 survived (R3-21 equivalent; R3-35 and R3-37 metadata) | `r3_mutants.txt` |
| `scripts/r3_extra.py` (round-2 re-anchors and metadata mutants) | 24: 18 killed, 6 metadata survivors (S1) | `r3_extra.txt` |
| `scripts/r3_21_witness.py` | 0 verdict differences over 15 cases | `r3_21_witness.out` |
| `scripts/r3_behaviour.py` | 39/39 as required | `r3_behaviour.out` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | rc 0, 87 scenarios, 356 steps | `behave_plan.out` |
| Documentation gates and `git diff --check` | all rc 0 | `docs_gates.out` |
| Read-only hosted check snapshot | See the limits below | `hosted_checks_snapshot.txt` |

The round-2 probe scripts under `scripts/r2/` are byte-identical to the R362-2 manifest:
- `r362_2_behaviour.py`: 0995d7f5…
- `r362_2_mutants.py`: 94eff879…
- `r362_2_survivor_witness.py`: 0035c26f…

All mutants ran on temporary copies, or on a `git archive` export under `scratch/`. The checkout was never written. `receipts/clone_integrity.txt` records the state after the probes:
- HEAD and tree are as above.
- `git diff-index` is empty, both against the worktree and cached.
- `git status --ignored` is empty.
- The (mode, blob, path) set of the index equals HEAD's tree.
- The seven PR files rehash to their HEAD blobs, all with mode 644.
- The four gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 870ff88a, `third_party/verilog-axis` 48ff7a7e.

The scoped Verilator was not used, since the diff contains no RTL.

## Real limits

- This is a desk review of a desk-level planner. Physical calibration, the soak and the power campaigns are NOT RUN. Field skips are not hardware proof.
- The following were not run here, by assignment:
  - the builder bank items (`ci_scope.py --selftest`, `check_baremetal_only.py`);
  - the gPTP/solution/submodule/traceability and hygiene gates;
  - the torture tier;
  - act;
  - the full parent/PP/gPTP/Yosys banks.

  For this head they rest on the executor's REVIEW READY (issue comment 5859666788) and the manager's statement. The public tree `review-evidence/593-r1` at `59efc9fa` records the gates at `95bea7cf`, not at this head.
- **Hosted checks:** a read-only snapshot at 2026-09-27T20:55:44Z shows the PR head as `7a051e61`, ready.
  - SUCCESS: rtl-fast, changes, full-ci-gate, wire-accountability, bdd-conformance, docs-check-no-git, verilator-lint, yosys-elaboration and Yosys shards 0-3.
  - Still in progress: docs-check, elaborate and Verilator shards 0-4.
  - "Physical gPTP" is SKIPPED, which is not executed evidence.
- The GM-history and two-sided proofs are over probe grids and the self-test's cases, not a formal proof. The derivation itself was checked by hand against the code: `h + R < 0.25` gives FAIL, and `h <= 0.5` gives PASS on the upper bound.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-progress Verilator shards, docs-check and elaborate.
- The final current-dev candidate build and merge validation: source base `6d5ebd73`, live dev `8bc97021`.
- Post-merge containment.
- Confirming that the second, external positive exists at this exact head before any merge.
- #602's deliverable 2 (the RTL, the gmstep leg, the GM_LOSS_RECOVERY MEDIA_RESET row) is outside this PR. Until it lands, the current image fails this gate on any soak with a PHC step, as the text now states.

## Prior findings: resolved or retained

My own R362-2 findings were re-verified with the unchanged round-2 probes.

| Prior finding | Status at 7a051e61 | Evidence |
|---|---|---|
| R362-2 F1 (MINOR): the `tu` deciding resolution does not decide the 0.25 s minimum | **Resolved** | The limit is now 0.125 s (`2R < 0.25`, equality refused). I3e/f/g are NOT RUN; I3h is FAIL. The D0 sweep shows no instant-clear PASS at any R. The derivation is identical in REQ-VER-06, TESTING 6d and the assertion text. The one-sided-limit mutant is killed |
| R362-2 F2 (MINOR): nine counted survivors | **Resolved** | C06, C07, C09, C34 and C35 are killed. C10r and C19r are killed after re-anchoring. T05, T13 and the re-anchored T21r are killed (`r362_2_mutants_at_7a051e61.out`, `r3_extra.txt`). C38, which was uncounted, is now killed |
| R362-2 F3 (MINOR): #602 described as pending | **Resolved** | `REQUIREMENTS.md:280-283`, `TESTING.md:936-939` and `GM_LOSS_RECOVERY.md:155` cite the ruling and state the current-image failure. No "pending" or "awaits" text remains |
| R362-2 S1: reset wording | **Adopted and resolved** | `TESTING.md:973` |

I read the other reviewer's round-2 findings after the verdict and ledger above were written. I checked each one at this head with `scripts/r363_2_witness_check.py`, using the inputs as their published text states them.

| Prior finding | Status at 7a051e61 | Evidence |
|---|---|---|
| R363-2 F1 (MINOR): GM-history boundaries `:3640-3641` and `:3637` unpinned (their M01 and M04) | **Resolved** | **Pins:** the driver mutants at `torture_release_mutants.py:556-566`, "history GM assignment drops start allowance / excludes start boundary / includes clear boundary" and "history accepts touching intervals", are all killed (`mutants_head.txt`). My C06, C07 and C09 are killed too.<br>**Witnesses:** their M01 witness is FAIL at head and their M04 witness is NOT RUN (`r363_2_witness_check.out`) |
| R363-2 F2 (MINOR): #602 text stale | **Resolved** | Same evidence as R362-2 F3 above. REQUIREMENTS and TESTING now state the end condition ("until #602's RTL change lands") |
| R363-2 S1: early NOT RUN verdicts omit `resolution_limit_s` | **Adopted and resolved** | Probes N-*, 16/16; the entry guards are pinned by `test_release_resolution_evidence`. Inner-path pinning is my S1 (SUGGESTION) |
| R363-2 S2: the derived limit makes the minimum failable, not tight | **Superseded by the round-3 decision and resolved** | The limit is now 0.125 s. Their two R = 0.24 s cases are NOT RUN (`r363_2_witness_check.out`). A true instant clear FAILs at every accepted R (D0) |
| R362-1 S2 (MEDIA_RESET under-count) and S4 (unkinded GM edge) | **Retained as open suggestions, unassigned** | Not in the round-3 scope. No coverage effect |

R362-3 FINISHED
