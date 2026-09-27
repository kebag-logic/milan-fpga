[R347] NEGATIVE - exact head 8153576af6d739427b54f6c40299b0e57bc481ae

# R347-3 external independent review: issue #396 / PR #586

- Round: R347-3, external independent reviewer, cleared context. This is a delta review of `24d32d54..8153576a`. Round R347-2 covered `24d32d54`.
- Exact head: `8153576af6d739427b54f6c40299b0e57bc481ae`, tree `1d174c6a4b647e00456846623993a658e894b716`. The head is one commit on `24d32d54`, which is two commits on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope: desk acceptance items 1, 2 and 5. Bench items 3 and 4 stay open, and the PR says `Refs #396`.
- Reconstructed from, in this order:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #396 body, the owner decision (5789765788), and the decisions of rounds 1, 2 and 3 (5854692245, 5854930205, 5855515133);
  - [A361] TAKEN (5855545141), REVIEW READY (5855671206) and the PR body;
  - REQUIREMENTS.md section 8, TESTING.md 6d, `KL_ptp_clock_validity.sv`, GM_LOSS_RECOVERY.md, and the #117 silicon findings;
  - the cited Milan v1.2 and IEEE 1722.1-2021 pages, which I extracted myself (`receipts/citation-check.txt`);
  - `git diff 24d32d54..8153576a` and `ac18b509..8153576a`, then the public evidence (the executor's round-3 packet at `641dac72`, and hosted checks).
- Prior public findings: after my own pass I read R346-2 (PR comment 5855513105). My own R347-2 (5855194536) is resolved below as well.

## Verdict summary

The round-3 commit implements the four items of decision 5855515133:
- **Item 1.** `RELEASE_RESTORE_BOUND_S = 30` is one named constant. Eligibility is false above it. There are arms at 29, 30, 31 and 3600, and a mutant that drops the check is killed.
- **Item 2.** The `tu` rule is now stated as a result in REQUIREMENTS.md, in the 6d table cell, in the soak assertion and in the plan args. All four agree.
- **Item 3.** The ADP window starts at T0. `power_off_hold_s` is a recorded parameter that is not charged against the window. At the repository's 8 s hold, the rule can no longer fail by construction.
- **Item 4.** Negative controls for CRF-only and listener-only omissions exist on both roles. R11, R12 and R346-2's E10-E15 are killed.

Also:
- Every clause citation is correct.
- No firmware, RTL, builder or gitlink file changed.
- Every gate I ran passes.
- All four round-2 findings are closed.

One new MINOR finding is open, so the verdict is NEGATIVE:
- **F1:** the `tu` pass rule measures from the discontinuity that an interval begins with. The RTL restarts its holdover at every discontinuity, and a GM change is followed by a PHC step. So under a fine-resolution measurement, the rule can fail a design that behaves exactly as documented, and graders can disagree about which event anchors the interval. This is new text in this delta.

## Findings

### F1 MINOR - Conformance, RTL, Robustness, Docs - the `tu` pass rule anchors a chained discontinuity at its first event, which the implemented holdover does not honor

- **Where:**
  - `REQUIREMENTS.md:262-269`: "Each `tu` interval begins with a recorded discontinuity ... It clears within 0.5 seconds plus stated observation resolution. Measure that interval from the recorded discontinuity."
  - `docs/testing/TESTING.md:915` and `:923-928`;
  - `tb/tools/torture_campaign.py:3390-3397` (the `soak.tu-within-holdover` text: "clears within 0.5 s of that event") and `:3544-3547` (`tu_holdover_bound_s=0.5`, `tu_time_origin`).
- **Authority/evidence:**
  - The decision (5855515133 item 2) sets 0.5 s as "the implemented holdover (`KL_ptp_clock_validity.sv:119-122`, 0.25-0.5 s)". That figure holds per pulse, but the RTL does more than one pulse:
    - `:188-190`: a PHC settime or adjtime, a fabric discontinuity pulse and a grandmaster-identity edge are all discontinuity pulses.
    - `:199`: `hold_r` is **reloaded on every pulse**.
    - `:211`: `tu = ~sync_ok | hold | disc`.

    So `tu` clears 0.25-0.5 s after the **last** discontinuity, and only once sync is healthy.
  - A GM change is not a single pulse in this design:
    - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:348-351` and `:443-444`: the DUT adopts the new grandmaster on an Announce. Then "the holdover bit set and the PHC stepped", and sync follows 0 to 0.2 s later.
    - `:346`: the first Sync lags the Announce.
    - The step needs a Sync from the new grandmaster, so it must come after the identity edge.
    - On silicon, `tu` cleared **0.41 to 0.52 s after adoption**, sampled every 0.1 s.
  - `scripts/tu_anchor_model.py` transcribes `:152-211` cycle for cycle (`receipts/tu-anchor-model.log`). It sweeps a GM change at t=0 and a step at t=d:
    - `tu` clears up to d + 0.5 s after the GM change: 0.519 s at d = 20 ms and 0.624 s at d = 125 ms;
    - it always clears within 0.5 s of the step.
  - The text does not say which recorded discontinuity anchors an interval that contains several. Read literally ("begins with", "that event"), it anchors at the first.
- **Impact:**
  - During the seven-day soak, a GM change is exactly the event this rule was written to grade.
  - If the step lands at d > 0, a correct candidate can:
    - **fail** under a wire-resolution measurement anchored at the GM change;
    - **pass** when anchored at the step;
    - **pass** when the grader records a coarse resolution. The silicon's 0.52 s is under 0.5 + 0.1 s.
  - So the verdict of a MUST release gate depends on which event the grader picks and on how coarse the recorded resolution is. Finer measurement makes a false failure more likely. This is the ambiguity class that R347-2 F2 was opened to remove, and it sits in the text that closed F2.
  - The failure is fail-closed: it gives a false red, never a false green. But it files a DUT finding (acceptance item 3) against correct behavior.
- **Required outcome:** REQUIREMENTS.md, the 6d `tu` row and the `soak.tu-within-holdover` text (and its args) must state the anchor for a `tu` interval that contains more than one recorded discontinuity, and must agree with each other. One example: "measured from the last recorded GM change or timing discontinuity before `tu` clears", which matches `KL_ptp_clock_validity.sv:199`. The alternative is a recorded decision on #396 that the first-event anchor is intended, together with how the post-GM-change PHC step is graded. If sync requalification after a GM change is meant to count inside the window, say so as well.
- **Verification:** the three texts name one anchor. Under that anchor, the modelled sequence (GM change, then a step at d ≤ 0.2 s) passes when `tu` clears within 0.5 s of the step. Any new arg is pinned by a self-test arm.

### Suggestions (non-blocking; no effect on coverage)

- **S1 - Tests:** four text mutants of the operator-facing assertion survive both gates (`receipts/mutants-r3.log`):
  - M09: the soak assertion states a 5 s `tu` bound;
  - M10: the uncorrelated-`tu` failure is dropped;
  - M15: the ADP assertion measures from the pre-cut advertisement;
  - M16: the ADP assertion charges the off time.

  The machine-readable args are pinned, and every arg mutant (M06-M08, M11-M14) is killed. The repository already pins clause substrings for other assertions (`torture_campaign.py:4705-4771`), so pinning key phrases of `soak.tu-within-holdover` and `power.adp-valid-time` would follow its own practice.

  The CLI default of `--power-off-hold-s` is not pinned either (M19). The documented command passes `8` explicitly, and the API default is pinned.
- **S2 - Conformance/Docs:** Milan Annex B.1.1 says `tu` "shall be set to 1 for the duration of 0.25 seconds". The head says B.1.1 "provides the 0.25-second minimum". That is the project's established reading (`KL_ptp_clock_validity.sv:119-122`, GM_LOSS_RECOVERY.md:64), and the decision adopts it. Wording such as "B.1.1 sets 0.25 s; the project reads it as a minimum" would keep the gloss visible. The soak rule does not grade an interval shorter than 0.25 s, which is acceptable for a stability gate.
- **S3 - Robustness:** `power_off_hold_s` accepts any positive integer, and a 1 s hold stays release-eligible (`receipts/probe-r3.log`). Discharge verification is the stated guard. The existing power-cycle self-test requires `off_s >= 5` (`torture_campaign.py:4673`). A floor, or a sentence stating the minimum, would make the recorded hold meaningful.
- **S4 - Robustness:** the `tu` resolution term has no ceiling, so any recorded resolution widens the pass bound. If F1 is settled with a fine-resolution anchor, consider requiring the resolution of the wire capture, or stating a maximum.

## Round-2 findings at this head

| Finding | State | Evidence |
|---|---|---|
| R347-2 F1 = R346-2 F1 (eligibility for any `restore_bound_s`) | CLOSED | See the note below the table. |
| R347-2 F2 (`tu` bound undecidable) | CLOSED as specified; residual is new F1 | REQUIREMENTS.md:262-270 names 0.5 s plus the recorded resolution, measured from a recorded discontinuity, and fails uncorrelated `tu`. The 6d cell `:915` states a result again. The soak assertion `:3390-3397` and the args `:3544-3547` agree. B.1's 5 s is excluded (`:270`, `:929`). Args mutants M06-M08 and the executor's two `tu` mutants are killed by `test_release_tu_contract`. The multi-discontinuity anchor is a different defect in the new text (F1). |
| R347-2 F3 (ADP verdict depended on an unstated off time) | CLOSED | See the note below the table. |
| R347-2 F4 = R346-2 F2 (topology rules without negative controls) | CLOSED | See the note below the table. |
| R347-2 S1 (power eligibility uses the soak interval) | Addressed as text | TESTING.md:878-881 states the shared release-profile prerequisites. |
| R347-2 S2 (boot observation window) | Taken | `boot_evidence` runs until the next cut or campaign end (`:3586-3587`); TESTING.md:954 and :985-987. The executor's mutant is killed by `test_release_boot_negative_control`. |
| R347-2 S3 (cite Milan 5.6.2) | Taken | REQUIREMENTS.md:289 and :296; TESTING.md:959 and :972; `:3420`. |
| R346-2 S1-S4 | Taken or addressed | S1 as above. S2: shared-profile text. S3: TESTING.md:889-890 and `test_release_topology_each_key` (my M20 is killed). S4: R16, B04 and B09 are killed. R346-1 S3 (tracebacks on a malformed `--dut`) is pre-existing and unassigned. |

Closure notes:
- **R347-2 F1 = R346-2 F1 (CLOSED):**
  - `RELEASE_RESTORE_BOUND_S = 30` (`torture_campaign.py:3325`) is the default at `:3338`, and the check is at `:3504`.
  - The arms at 29, 30, 31 and 3600 are at `:5004-5007`, with feature `:399`.
  - The probe shows API and CLI rows at 31 and 3600 as `[False, False, False]`, and 29 and 30 as true (`receipts/probe-r3.log`).
  - Mutants that drop the check (M01; the decision's required mutant), make the ceiling exclusive (M02), relax it to 31 (M03) or skip it on the soak repeat (M04) are killed by `test_release_eligibility_boundaries` and the behave feature. The executor's driver also kills its two variants.
  - Documented at REQUIREMENTS.md:301-303 and TESTING.md:878-881 and :979-980.
- **R347-2 F3 (CLOSED):**
  - The window runs from T0: `adp_start="T0"`, `adp_deadline="2 * pre_cut_valid_time"` with `adp_required_valid_time=10`, and `power_off_hold_in_adp_window=False` (`:3571-3602`).
  - Evaluating the **emitted** expressions (`receipts/probe-r3.log`) gives a 20 s deadline for holds of 8, 13 and 60 s and for pre-cut advertisement ages of 0 and 4.9 s. Boot-to-first-advertisement of 12 s and 19.9 s passes, and 20 s fails (exclusive). Neither the off time nor the pre-cut age is charged, so an 8 s hold cannot fail by construction.
  - `power_off_hold_s` is pinned at 17 through the API (`test_release_timing_and_snapshot_contract`), at 13 through the CLI, and at 8 by default.
  - The requirement and 6d state the rule: REQUIREMENTS.md:284-296 and TESTING.md:935-938, :951 and :956-972.
  - Mutants M11-M14 and M17-M18 are killed. The superseded probe arithmetic in `receipts/probe-r2.log` hardcodes the round-2 formula and is not evidence against this head.
- **R347-2 F4 = R346-2 F2 (CLOSED):**
  - My unchanged `mutants_r2.py` kills 22 of 22, including R11 (CRF keys) and R12 (listener shape), by both gates (`receipts/mutants-r2.log`).
  - R346-2's unchanged `planner_mutants_r2.py` (sha256 `e413b335...`, equal to its public manifest) kills 48 of 48 valid mutants. The listener-shape mutant E12 and E10, E11, E13 and E15 are killed; R13 and R19 are invalid because their anchors were superseded (`receipts/r346-2-planner-mutants-r2.log`).
  - `test_release_topology_each_key` (`:5052`) and feature `:387` cover each key on each role.
  - My M20-M25 are killed.

## Clean-lens evidence

[R347] PASS Tests - `tb/tools/torture_campaign.py:4793-5135` (`_ReleasePlanChecks`, including new `test_release_topology_each_key` :5052 and `test_release_tu_contract` :5092), `tests/features/torture_campaign_plan.feature:385-411`, `tests/steps/torture_release_steps.py:218-268`, `tb/tools/torture_release_mutants.py`; `receipts/mutants.log`, `mutants-r2.log`, `mutants-r3.log`, `r346-2-planner-mutants-r2.log`, `executor-release-mutants.log`, `audit-probe.log` - Checked:
- Each new test fails for the defect it claims to detect.
- My round-1 mutants kill 21 of 21 and my round-2 mutants kill 22 of 22, run unchanged (sha256 equal to the round-2 manifest; `receipts/round2-script-provenance.txt`).
- R346-2's unchanged script kills 48 of 48 valid mutants.
- The repository driver kills its 9 mutants, each by its named test.
- My 26 round-3 mutants: the 21 behavioral ones are killed, each by a named test. The 5 survivors mutate only prose or a CLI default and are suggestion S1, not a missed defect.
- The audit probe still rejects D1-D6.
- The new behave steps call the CLI as a subprocess, so they cover the real integration wiring.
- The existing regressions pass: self-test 49 tests, plan feature 76/321, `@torture` tier 221 scenarios.
- F1 is a bench grading rule that no desk test can decide, so no finding is filed under Tests.

Conformance, RTL, Robustness and Docs are UNCLEAN (F1). What I checked clean inside them:
- The four decision items match REQUIREMENTS.md, 6d, the assertions and the args.
- The citations are correct (`receipts/citation-check.txt`).
- `ReleaseSettings` rejects a zero, negative, bool or NaN `power_off_hold_s`.
- The topology rule refuses the `entity_id` alias and empty values.
- No stale round-2 string remains in the five release files (`receipts/probe-r3.log`, section 4).
- The delta touches no path under `hdl/`, `sw/`, `syn/` or a gitlink (`receipts/clone-integrity-compare.txt`).
- Hosted `rtl-fast`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3 and Verilator shard 3 report success at the exact head (`receipts/hosted-check-runs.tsv`).

## Commands and results (this reviewer, exact head, foreground)

`receipts/gate-summary.txt` lists the exact gate commands. `$MDPY` is a fresh virtual environment in unpublished scratch, installed with `--require-hashes` from `tools/markdown/requirements.txt` (sha256 prefix 40cdefe08ebd).

| Command | Result |
|---|---|
| `scripts/round2/run_gates.sh` (round 2, unchanged) | all 15 gates rc 0 |
| `python3 -B tb/tools/torture_campaign.py --self-test` | 49 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 76 scenarios and 321 steps passed, none skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 221 scenarios passed, 172 skipped by tag |
| `scripts/check_feature_status.py --self-test` / without it | 46/46 / 0 findings |
| `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_py_idiom.py` | 0 findings; 850 paths resolve; 22 documents OK; no ratchet increase |
| `$MDPY -B scripts/check_em_dash.py --base ac18b509...`; `$MDPY -B scripts/gen_toc.py --check` | 0 findings, 339/339 arms; OK |
| `git diff --check`; `git diff ac18b509... HEAD --check` | rc 0; rc 0 |
| `--coverage-by-area --areas soak,power`; `--plan --areas soak,power --json` | rc 0; rc 0 |
| `scripts/round2/mutants.py` (round 1, unchanged) | 21/21 killed |
| `scripts/round2/mutants_r2.py` (round 2, unchanged) | 22/22 killed, R11 and R12 included |
| `scripts/round2/audit_probe.py` (unchanged) | the audit rejects D1-D6 |
| `scripts/round2/probe_r2.py` (unchanged) | 31 and 3600 are now false; its last ADP rows hardcode the superseded formula |
| R346-2 `planner_mutants_r2.py` (unchanged) | 48 killed, 0 survived, 2 invalid (superseded anchors) |
| `TMPDIR=scratch python3 -B tb/tools/torture_release_mutants.py` (from an extracted tree) | 9/9 killed by named tests |
| `scripts/mutants_r3.py` (26 round-3 mutants) | 21 killed with named tests; 5 prose/default survivors (S1) |
| `scripts/probe_r3.py` | evidence for the F1, F3 and F4 closures, S3, and no stale strings |
| `scripts/tu_anchor_model.py` | evidence for F1 |

After the probes, the clone is byte-identical to the head (`receipts/clone-integrity-before.txt`, `-after.txt` and `-compare.txt`, identical):
- porcelain is empty, and there are no ignored files;
- the index listing has sha256 `e62315c3...`;
- all 8 changed-file blobs match HEAD, with mode 100644. `torture_campaign.py` is blob `712ed090` with sha256 `0cedf3a3...`;
- the four gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 0922e434, `third_party/verilog-axis` 48ff7a7e.

All probes ran on `git archive` extractions under unpublished scratch.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | REQUIREMENTS.md:250-321; TESTING.md:841-1000; decision 5855515133; plan args and assertions :3320-3605; Milan v1.2 p108-110, p141; IEEE 1722.1-2021 p49; #117 findings :300-450 | R347-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| RTL | UNCLEAN (F1) | `KL_ptp_clock_validity.sv:95-250` against the new `tu` rule; `receipts/tu-anchor-model.log`; delta and full diff stat; gitlinks; hosted lint and Yosys at the exact head | R347-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Robustness | UNCLEAN (F1) | `ReleaseSettings` validation; eligibility probes at 29/30/31/3600; hold 1/8/600; ADP expression evaluation; topology omissions per role; `check_release_boot` edges; chained-discontinuity model | R347-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Tests | CLEAN | `_ReleasePlanChecks` :4793-5135; feature :385-411; `torture_release_steps.py`:218-268; `torture_release_mutants.py`; 21 + 22 + 26 + 9 + 50 mutants with kill attribution; audit probe | R347-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Docs | UNCLEAN (F1) | REQUIREMENTS.md section 8; TESTING.md 6d; PR body; TAKEN and REVIEW READY; docs gates | R347-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |

## Real limits

- This is a desk review only. Physical calibration was NOT RUN, and nothing here is hardware proof. The hosted `Physical gPTP` context is skipped, which is not evidence.
- The assigned pinned simulator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. No simulation was run. The F1 evidence is:
  - a cycle-level transcription of `KL_ptp_clock_validity.sv:152-211`, which is a pure counter with no hidden state;
  - the repository's own silicon record.
- The timing of the PHC step after a GM change is taken from the #117 findings, which were sampled every 0.1 s. I have no finer bench measurement.
- At capture (2026-09-27T12:18Z), hosted `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were still in progress. They are recorded but not relied on.
- I found no published manager bank logs for this head. The only public manager statement is the assignment. I did not rerun the full parent/PP/gPTP/Yosys/builder banks, Docker/act or any hardware step, as assigned.
- Standards handling: I extracted only the listed pages, into unpublished scratch. No standards text is published beyond clause headings and short facts.
- All mutants are textual. A survivor shows a gap in the tests, not a defect in the reviewed code.

## Pending manager duties

- Route F1 to the executor, or record on #396 which discontinuity anchors a multi-event `tu` interval. The decision's 0.5 s rests on a per-pulse holdover that the RTL re-arms. S1-S4 are optional.
- Hosted and act acceptance at the exact head, and the final current-dev candidate at the merge turn. The source base is `ac18b509`, and live dev is `63fe4fb0`.
- Ratify `RELEASE_RESTORE_BOUND_S` from #397 and #75 when measured.
- File the Issue for the older 1722.1-2021 6.2.6 attributions (`torture_campaign.py:1456`, `:2769`, `:3096`, `:3104`), carried over since R347-1.
- Re-review of the corrected head. Bench items 3 and 4 stay open under #396.

R347-3 FINISHED
