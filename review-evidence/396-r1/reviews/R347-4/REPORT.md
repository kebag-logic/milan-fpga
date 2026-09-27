[R347] NEGATIVE - exact head 54d9beea2888bd07369e67e5cb025d1405d03495

# R347-4 external independent review: issue #396 / PR #586

- Round: R347-4. External independent reviewer, cleared context. This is a delta review of `8153576a..54d9beea`. R347-3 covered `8153576a`.
- Exact head: `54d9beea2888bd07369e67e5cb025d1405d03495`, tree `f5af9ab56ca4bea9b059eeeffdf012de1d8d02ec`. The head is one commit on `8153576a`, which is three commits on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope: desk acceptance items 1, 2 and 5. Bench items 3 and 4 stay open, and the PR says `Refs #396`.
- Reconstructed from, in this order:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #396 round-4 decision (issue comment 5855792297, `receipts/decision_5855792297.txt`);
  - [A362] REVIEW READY (5855916506) and the PR body's "Round 4" section;
  - REQUIREMENTS.md REQ-VER-06, TESTING.md 6d, `KL_ptp_clock_validity.sv`, and the AAF/CRF talkers' `tu` latches;
  - `git diff 8153576a..54d9beea` and `ac18b509..54d9beea`;
  - then the public evidence: the evidence tree at `4949b127`, and hosted checks at the exact head.
- Prior public findings: I read R347-3 (5855789830) and R346-3 (5855777031) only after finishing my own pass over the delta.

## Verdict summary

The round-4 commit carries out decision 5855792297 as written:
- **One anchor, stated three times.** REQUIREMENTS.md:262-266, the 6d row (TESTING.md:915) with its prose (:925-941), and the `soak.tu-within-holdover` text (`tb/tools/torture_campaign.py:3390-3401`) all state the same rule. So do the plan args (`:3574-3578`):
  - an interval contains at least one recorded discontinuity of the three kinds;
  - it is measured from the last recorded discontinuity before `tu` clears;
  - it clears within 0.5 s plus the stated resolution;
  - uncorrelated `tu` fails.

  The three kinds (PHC settime/adjtime, fabric discontinuity, GM-identity edge) are exactly the pulse sources at `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:188-190`.
- **The required arms exist and pass:**
  - GM edge at 0 plus a step at 0.2 s: clearing at 0.62 s passes and clearing at 0.8 s fails;
  - no discontinuity fails;
  - boundary arms at 0.75/0.751 s and 0.76/0.761 s;
  - SKIP arms for incomplete capture, a disordered interval, NaN, negative resolution and bool resolution.
- **The mutants are killed.** The executor's first-event mutant is killed, and so is my own (T01).
- **No firmware, RTL, builder or gitlink change** anywhere in the PR.
- **R347-3 F1 is CLOSED** (evidence below).

One new MINOR finding is open, so the verdict is NEGATIVE:
- **F1:** the new oracle `check_release_tu` fails a correct design whose `tu` interval has a single discontinuity. The design raises `tu` in the same cycle as the discontinuity, but the first wire packet carrying `tu=1` can only follow it. The containment test gives no resolution allowance at the start edge, so the causing event falls just outside the observed interval, and the interval is graded "uncorrelated".

## Findings

### F1 MINOR - Conformance, RTL, Robustness, Tests, Docs - the `tu` oracle's containment test gives no resolution allowance at the start edge, so a lone discontinuity is graded uncorrelated

- **Where:**
  - `tb/tools/torture_campaign.py:3551`: `events_s = [event_s for event_s in discontinuities_s if start_s <= event_s < clear_s]`, with no observation-resolution allowance at `start_s`. By contrast, the clearing edge at `:3555` adds `observation_resolution_s`.
  - `docs/testing/TESTING.md:915` (the row grades "wire `tu` intervals") and `:933-941`: "Use `check_release_tu` with complete interval and discontinuity evidence". The worked example places the first event exactly at the interval start.
  - Self-test arms `tb/tools/torture_campaign.py:5148-5175`; feature `tests/features/torture_campaign_plan.feature:414-418`; steps `tests/steps/torture_release_steps.py:273-288`.
- **Authority/evidence:**
  - Decision 5855792297 and REQUIREMENTS.md:262-266: an interval "contains at least one recorded discontinuity" and "Any `tu` without a recorded discontinuity fails". REQUIREMENTS.md:267 says resolution "comes from wire capture and correlated event timestamps".
  - `KL_ptp_clock_validity.sv:211`: `ts_uncertain_o = ~sync_ok | hold | disc_p`. In the DUT, `tu` rises in the same cycle as the discontinuity pulse, so the true interval begins at the event.
  - `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:615` latches `tu` at frame start, and `hdl/ieee1722/crf/KL_crf_tx.sv:501` does the same for CRF. The first captured packet with `tu=1` is therefore launched at or after the pulse and observed later still. The clock-validity comment at `:208-210` says a launch can at best share the pulse's edge.
  - So the wire-observed start is later than the recorded event by at least the launch-to-capture latency, up to one packet period plus the event-to-capture correlation error. That is the same quantity the requirement calls the stated resolution.
  - `receipts/tu_oracle_probe.txt` (`scripts/tu_oracle_probe.py`, importing the head's oracle read-only):
    - Part A: with the interval anchored at the pulse, every phase passes for d = 0-0.2 s.
    - Part B: a lone discontinuity at t_e, with the observed start at t_e + 1.25 µs to 1 ms (all within the 0.001 s resolution) and the clear taken from the unchanged cycle model. All 6 cases return `FAIL {'why': 'uncorrelated tu fails'}`.
    - Part B': the same lag, with a GM edge before the start and a step inside the interval, passes, but only because the step falls inside.
  - Mutant T02 (`start_s <= event_s` changed to `start_s < event_s`) survives both gates (`receipts/mutants_r4.txt`). No arm has a lone event at, or just before, the observed start. The one arm with an event before the start (`:5155`, event at -0.1 s) lies 100 times outside the resolution. Informational mutant I01 applies the start-edge allowance and also survives, so the fix is compatible with every current arm.
- **Impact:**
  - The most common single discontinuity in a seven-day soak is a lone PHC settime/adjtime, or a fabric discontinuity without a following step. Graded as documented, it returns FAIL "uncorrelated" for a design that behaves exactly as `KL_ptp_clock_validity.sv` documents.
  - The MUST release gate REQ-VER-06 would then file a DUT finding (acceptance item 3) against correct behaviour. Or a grader shifts the interval start by hand, which is the grader-dependent verdict that R347-2 F2 and R347-3 F1 were opened to remove.
  - The failure is fail-closed: it gives a false red, never a false green. This is the same class and severity as R347-3 F1.
  - Why each lens:
    - **Conformance:** a `tu` interval that has a recorded discontinuity is graded as having none.
    - **RTL:** the oracle does not account for the talker's latch-at-launch latency.
    - **Robustness:** the event-before-observed-start ordering is unhandled.
    - **Tests:** the only start-edge arm reproduces the implementation's assumption that the event equals the start (T02 survives).
    - **Docs:** 6d does not say how the observed start is graded against the causing event.
- **Required outcome:** a recorded discontinuity that precedes the wire-observed `tu` start by no more than the stated observation resolution must count as contained in that interval. Either the oracle applies the resolution at the start edge, or the documented grading defines the interval start so that the causing event is contained. Events farther before the start than that resolution must still be excluded. If this changes the rule's wording, state it identically in REQUIREMENTS.md, the 6d row and prose, and the `soak.tu-within-holdover` text, or record the choice on #396.
- **Verification:**
  - a self-test arm (and ideally a feature step) with a lone event 0.5 x resolution before the observed start passes, and one 2 x resolution before it fails;
  - an arm with a lone event exactly at the start passes, so mutant T02 is killed;
  - the existing -0.1 s arm still fails;
  - `scripts/tu_oracle_probe.py` Part B returns PASS for every lag within the resolution.

### Suggestions (non-blocking; no effect on coverage)

- **S1 - Conformance, Docs.** Under the decided "contains at least one" rule, a `tu` interval that rises long before its first recorded discontinuity still passes. For example, interval (0, 10.4 s) with one event at 10.0 s is PASS (`receipts/tu_oracle_probe.txt` Part D). That follows the decision literally, and it may be intended for sync loss followed by a step on requalification (TESTING.md:932). The decision owner may want to record whether `tu` asserted before the first discontinuity is meant to pass, or bound it.
- **S2 - Docs.** [A362] REVIEW READY on #396 (5855916506) carries only the head. The Changed, Validation, Acceptance and Open-risks content lives in the PR body's "Round 4" section. The decision asked for that comment alone, and the PR body is sufficient for a cold reviewer. A one-line pointer would help the next reader.

## R347-3 findings at this head

| Finding | State | Evidence |
|---|---|---|
| R347-3 F1 MINOR (`tu` anchored at the first discontinuity of a chain) | **CLOSED** | See the note below the table. |
| R347-3 S1 (assertion text and CLI default unpinned) | Taken | `test_release_assertion_text` (`:5177`) and `test_release_cli_power_hold_default` (`:4988`). The executor's text and CLI mutants are killed (`receipts/release_mutants.txt`: 19/19). My T13 and T14 (anchor wording, kinds dropped from the assertion) are killed. |
| R347-3 S2 (B.1.1 "minimum" wording) | Taken | "B.1.1 states 0.25 seconds; the project reads this as a minimum" (REQUIREMENTS.md:271, TESTING.md:943, assertion `:3398`). |
| R347-3 S3 (no floor on `power_off_hold_s`) | Addressed as text | TESTING.md:955-956: the effective minimum is the longer of hold and verified discharge, and elapsed hold alone never proves a cold cut. No numeric floor; the PR body states this. |
| R347-3 S4 (resolution unbounded) | Addressed as text | The resolution must come from wire capture and correlated event timestamps, and counter-read cadence cannot supply it (REQUIREMENTS.md:267-268, TESTING.md:923-924, assertion `:3397`, arg `:3577`). There is no numeric ceiling. F1 above relies on this resolution statement. |

Closure note for R347-3 F1:
- **One anchor.** All three texts and `tu_time_origin` name "last recorded discontinuity before `tu` clears" (REQUIREMENTS.md:264; TESTING.md:915 and :929; `torture_campaign.py:3394` and :3575).
- **The model passes under that anchor.** `scripts/tu_anchor_model.py` was rerun unchanged, with sha256 `b58e8313…` equal to the R347-3 copy (`receipts/tu_anchor_model.txt`). For each d from 0 to 0.2 s, `tu` clears 0.251-0.499 s after the step, and 0.451-0.699 s after the GM edge when d = 0.2 s. Fed into the head's oracle with the interval anchored at the pulse, every phase and every d passes (`receipts/tu_oracle_probe.txt` Part A).
- **The required arms exist.** Clearing at 0.62 s passes, at 0.8 s fails, and no discontinuity fails: `:5152-5154`, feature `:414-418`, steps `:273-288`.
- **The first-event mutant is killed.** The executor's "tu anchor uses the first discontinuity" is killed by `test_release_tu_chained_discontinuities`, and my T01 is killed by both gates.
- The start-edge defect is in `check_release_tu`, which is new in this delta, so it is filed as new finding F1 rather than as a retention.

R346-3 raised no findings. Its S1-S3 are taken as text and tests, as above. S4 (the CONTRIBUTING.md:542 boot figure) and S5 (the "round 2" labels at `torture_campaign.py:3337` and `:5553`) are unchanged and optional. The round-1 to round-3 findings, closed at R347-3 and R346-3, stay closed: this delta touches their artifacts only in the `tu` text recorded above.

## Clean results within each lens (all five lenses are UNCLEAN under F1)

F1 is attributable to all five lenses, so none is covered clean in this round. Within each lens, this is what I applied and found clean:
- **Conformance** (REQUIREMENTS.md:250-275; TESTING.md:909-944; `torture_campaign.py:3390-3401`, :3534-3578; decision 5855792297):
  - Every numbered item of the decision is implemented.
  - The three kinds match the RTL pulse sources.
  - The 0.5 s bound is unchanged, and B.1's 5 s is still excluded.
  - The plan JSON emits the five `tu_*` args (`receipts/plan_soak_power.json`).
- **RTL** (`receipts/delta_scope.txt`; `KL_ptp_clock_validity.sv:150-212`; `KL_aaf_packetizer.sv:615`; `KL_crf_tx.sv:501`; gitlinks in `receipts/clone-integrity-after.txt`):
  - No RTL, firmware or builder file changed, and all four gitlinks are unchanged.
  - The model's line anchors still hold at the head.
  - The only RTL-lens defect is the oracle's missing allowance for the launch latency (F1).
- **Robustness** (`check_release_tu` at `:3534-3558`; `receipts/mutants_r4.txt` T03-T09, T15):
  - Refused with SKIP: bool, NaN, None and negative inputs, a disordered interval, incomplete capture, and a zero or negative bound.
  - An event at the clear instant is excluded.
  - Events after the clear are ignored.
  - Zero resolution is accepted.
  - The clearing boundary is inclusive, and exact at 0.75 s.
- **Tests:**
  - self-test 52 OK;
  - plan feature 77 scenarios / 326 steps;
  - `@torture` tier 222 scenarios / 871 steps;
  - `torture_release_mutants.py`: 19/19 killed by named tests;
  - my T01 and T03-T15 killed.

  The one boundary gap is T02 (F1).
- **Docs:**
  - `docs_check`, `check_doc_paths`, `check_doc_style`, `check_em_dash` (base `ac18b509` and `8153576a`, pinned renderer), `gen_toc --check`, `check_feature_status` (46/46, 0 findings), `check_py_idiom`, `check_hygiene`, `measure_test_evidence --check` and `git diff --check` over three ranges: all rc 0 (`receipts/doc_and_hygiene_checks.txt`, `receipts/gates_rerun.txt`).
  - Both new links point to the recorded decisions.
  - The one Docs defect is the undefined start-edge grading (F1).

## Commands and results (this reviewer, exact head, foreground)

| Command | Result |
|---|---|
| `python3 -B scripts/tu_anchor_model.py` (unchanged, sha256 b58e8313…) | rc 0; clears within 0.251-0.499 s of the last pulse for every d |
| `python3 -B tb/tools/torture_campaign.py --self-test` | 52 tests, OK |
| `python3 -B tb/tools/torture_release_mutants.py` | pristine baseline passes; 19/19 killed by named tests |
| `behave --no-capture -f plain tests/features/torture_campaign_plan.feature` | 77 scenarios / 326 steps passed |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 222 scenarios passed, 172 skipped by tag |
| `python3 -B scripts/tu_oracle_probe.py <clone>` | Part A all PASS; Part B 6/6 FAIL "uncorrelated" (F1); Part D PASS (S1) |
| `python3 -B scripts/mutants_r4.py <clone> scratch/mut` (on a `git archive` extraction) | 14 killed; T02 survived (F1); I01 survived (informational); 0 invalid |
| docs, style, idiom, hygiene, test-evidence and feature-status gates | rc 0 |
| `$MDPY -B scripts/check_em_dash.py --base ac18b509…` / `--base 8153576a…`; `$MDPY -B scripts/gen_toc.py --check` | 0 findings, 339/339 arms; 0 findings; OK |
| `git diff --check` (worktree, `ac18b509..HEAD`, `8153576a..HEAD`) | rc 0 ×3 |
| `--plan --areas soak,power --json` | rc 0 |

`$MDPY` is a virtual environment in unpublished scratch, installed with `--require-hashes` from `tools/markdown/requirements.txt` (sha256 40cdefe0…). With the system interpreter, `check_em_dash` exits 2 because the renderer is missing, as recorded in `doc_and_hygiene_checks.txt`; that is a host limit, not a finding.

Clone integrity after the probes (`receipts/clone-integrity-after.txt`):
- HEAD and tree are exact, porcelain is empty, and there are no ignored files. The bytecode caches that my first feature run left under `tb/tools` and `tests/steps` were removed.
- The index listing has sha256 `f1061396…`.
- All 8 PR-changed files hash to their HEAD blobs, with mode 100644.
- The four gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 0922e434, `third_party/verilog-axis` 48ff7a7e.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | REQUIREMENTS.md:250-275; TESTING.md:909-944; `torture_campaign.py:3390-3401`, :3534-3578; decision 5855792297; `receipts/plan_soak_power.json`; `receipts/tu_oracle_probe.txt` | R347-4 | 54d9beea2888bd07369e67e5cb025d1405d03495 |
| RTL | UNCLEAN (F1) | `KL_ptp_clock_validity.sv:150-212`; `KL_aaf_packetizer.sv:615`; `KL_crf_tx.sv:501`; `receipts/delta_scope.txt`; gitlinks; `receipts/tu_anchor_model.txt`; hosted lint and Yosys at the head | R347-4 | 54d9beea2888bd07369e67e5cb025d1405d03495 |
| Robustness | UNCLEAN (F1) | `check_release_tu` :3534-3558 input and boundary behaviour; `receipts/tu_oracle_probe.txt`; `receipts/mutants_r4.txt` | R347-4 | 54d9beea2888bd07369e67e5cb025d1405d03495 |
| Tests | UNCLEAN (F1) | `_ReleasePlanChecks` :4988, :5137-5190; feature :410-418; `torture_release_steps.py:260-288`; `torture_release_mutants.py`; `receipts/planner_selftest.txt`, `release_mutants.txt`, `behave_torture_campaign_plan.txt`, `gates_rerun.txt`, `mutants_r4.txt` | R347-4 | 54d9beea2888bd07369e67e5cb025d1405d03495 |
| Docs | UNCLEAN (F1) | REQUIREMENTS.md REQ-VER-06; TESTING.md 6d :909-962; PR body "Round 4"; [A362] REVIEW READY; `receipts/doc_and_hygiene_checks.txt`, `gates_rerun.txt` | R347-4 | 54d9beea2888bd07369e67e5cb025d1405d03495 |

## Real limits

- This is a desk review only. Physical calibration was NOT RUN, and nothing here is hardware proof. The hosted `Physical gPTP (nightly and manual)` context is skipped, and a skip is not evidence.
- F1's latency argument rests on the RTL's `tu` latch points and the documented wire-capture grading. I have no bench capture measuring the pulse-to-first-`tu`-packet lag. The argument needs only that this lag is positive, which the latch at frame start guarantees.
- No simulation was run. The delta has no RTL change, so the scoped pinned simulator was not used, and its identity was not checked.
- Hosted checks captured at 2026-09-27T12:50:55Z (`receipts/hosted-check-runs.tsv`):
  - success: `changes`, `full-ci-gate`, `bdd-conformance`, `verilator-lint`, `wire-accountability`, `docs-check-no-git`, and Yosys shards 0-3;
  - still in progress: Verilator shards 0-4, `yosys-elaboration`, `elaborate` and `docs-check`. These are recorded but not relied on.
- The linked public evidence tree at `4949b127` (`review-evidence/396-r1/`) holds only the author's round-1 logs. I found no manager bank logs for this head there or in the #396/#586 comments at capture time. The manager's source bank result at this head is taken as stated in the assignment, and I did not verify it independently. I did not run the full parent/PP/gPTP/Yosys/builder banks, Docker/act or any hardware step, as assigned.
- All mutants are textual. A survivor shows a test gap, not a defect by itself; F1 rests on the probe.

## Pending manager duties

- Route F1 to the executor, or record on #396 how the wire-observed start edge is graded against the causing discontinuity. S1 and S2 are optional.
- Hosted and act acceptance at the exact head, including the in-progress Verilator shards and elaboration.
- The final current-dev candidate at the merge turn. The source base is `ac18b509`, and live dev is `63fe4fb0`.
- Ratify `RELEASE_RESTORE_BOUND_S` from #397 and #75 when measured.
- File the Issue for the older 1722.1-2021 6.2.6 attributions, carried over since R347-1.
- Re-review of the corrected head. Bench items 3 and 4 stay open under #396.

R347-4 FINISHED
