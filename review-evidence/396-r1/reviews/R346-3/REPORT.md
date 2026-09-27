[R346] POSITIVE - exact head 8153576af6d739427b54f6c40299b0e57bc481ae

# R346-3 internal independent review: issue #396 / PR #586

- Round: R346-3, the internal reviewer in a cleared context, in its own detached clone.
- Exact head: `8153576af6d739427b54f6c40299b0e57bc481ae`, tree `1d174c6a4b647e00456846623993a658e894b716`. This is one commit on `24d32d549fa7470318a93984403a92423a63fa25`. Its message is one line with no trailers.
- Source base: `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope judged: the delta `24d32d54..8153576a`. R346-2 covered `24d32d54`. The full diff from `ac18b509` was re-read wherever the delta changes a contract.
- Authority, in reading order:
  - AGENTS.md, then CONTRIBUTING.md sections 3 to 6, then docs/README.md.
  - Issue #396's body, the owner decision 5789765788, and the manager decisions 5854692245, 5854930205 and **5855515133** (round 3).
  - REQ-VER-06 and TESTING.md 6d.
  - The cited clauses, extracted from Milan v1.2, IEEE 1722.1-2021 and IEEE 1722-2016.
  - `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv`.
- Prior public findings: R346-2 and R347-2 (PR comments 5855513105 and 5855194536) were read only after this round's independent pass and draft verdict. Nothing in them changed the draft.

## Verdict basis

Every round-2 finding is closed at this head, and each closure was checked by executing something:

- **R346-2 F1 = R347-2 F1** (eligibility true for any `restore_bound_s`):
  - There is one named constant, `RELEASE_RESTORE_BOUND_S = 30` (`tb/tools/torture_campaign.py:3325`), and the `ReleaseSettings` default is taken from it (`:3338`).
  - `_release_profile_eligible` (`:3500-3505`) refuses any bound above it, on the soak repeat and on both power repeats.
  - Probe results:
    - At 31 s, the self-test and behave arms report false.
    - My unchanged round-2 `eligibility_probe.py` rows for 600 and 3600 s now show `eligible=False`, where round 2 showed `True`.
  - A mutant that drops the check is killed.
- **R347-2 F2** (the `tu` bound could not be decided): one rule now runs through REQ-VER-06, the 6d row and prose, the assertion text and the plan arguments:
  - the interval must begin with a recorded GM change or timing discontinuity;
  - it must clear within 0.5 s plus the recorded observation resolution;
  - uncorrelated `tu` fails;
  - B.1's 5 s is excluded as media-clock holdover.
- **R347-2 F3** (the ADP verdict depended on an unstated off time):
  - The corrected rule runs from T0 over `2 * pre_cut_valid_time`, with `valid_time=10` required.
  - `power_off_hold_s` (default 8 s) is recorded with its origin and flagged `power_off_hold_in_adp_window=False`.
  - `receipts/adp_hold_probe.log` evaluates the formula strings the planner **emits**, with decoy hold and advert-age variables in scope:
    - Across holds of 1, 8, 60 and 3600 s and advert ages of 0 and 4.9 s, the verdict does not change: boot 19.99 s passes, and boot 20 s, 25 s and a negative elapsed time fail.
    - Under the superseded formula, the same 8 s hold fails 7.2 s and 13 s boots.

  So at the repository's 8 s hold the rule cannot fail by construction.
- **R346-2 F2 = R347-2 F4** (topology rules without negative controls):
  - The per-key controls exist on both roles, in the self-test and in the feature.
  - My unchanged `planner_mutants_r2.py` now kills E10-E13 and E15, including the listener-shape survivor E12.
  - The unchanged public R347-2 `mutants_r2.py` kills R11 (CRF keys) and R12 (listener shape), with 22 of 22 killed.
- **Constraints:**
  - No firmware, RTL, builder or gitlink change (`receipts/scope_and_gitlinks.log`).
  - Clause citations were checked against the extracted text (`receipts/standards_citation_check.md`).
  - Every assigned gate is rc 0 at this head.

No finding at MINOR or above is open. The five suggestions below are optional and do not affect coverage.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### Suggestions (non-blocking; do not affect lens coverage)

- **S1 - SUGGESTION - Conformance, Robustness, Docs - the `tu` observation resolution has no ceiling and no named source.**
  - Where: `REQUIREMENTS.md:264`; `docs/testing/TESTING.md:915`, `:923-925`; `tb/tools/torture_campaign.py:3546`.
  - Evidence: the bound is "0.5 seconds plus that recorded resolution". The soak also reads `tu` through the periodic gPTP publication (`gptp_publication` includes `"tu"`, `:3540-3541`) at up to the 60 s interval. If that cadence were recorded as the resolution, the bound would become 60.5 s.
  - Why it stays a suggestion: the head already guards against that reading. The 6d row names "wire `tu` intervals", and `:919-921` says periodic reads cannot prove the absence of transitions. The rule also follows decision 5855515133 item 2 verbatim.
  - Optional outcome: say that the resolution is that of the wire capture or event timestamps, or cap it well below 0.5 s.
- **S2 - SUGGESTION - Conformance, Docs - B.1.1's 0.25 s is called a "minimum", and nothing bounds `tu` from below.**
  - Where: `REQUIREMENTS.md:268`; `docs/testing/TESTING.md:927`; the `soak.tu-within-holdover` text (`tb/tools/torture_campaign.py:3390-3397`).
  - Evidence: Milan v1.2 Annex B.1.1, which sits in an informative annex, reads "the tu bit shall be set to 1 for the duration of 0.25 seconds". The "minimum" reading comes from the decision and the RTL header (`KL_ptp_clock_validity.sv:119-122`), and it is consistent with the implemented 0.25-0.5 s. The consequence is that a `tu` interval shorter than 0.25 s after a GM change passes the soak rule.
  - Optional outcome: present "minimum" as the project's interpretation, or add a lower bound if the manager wants B.1.1 enforced.
- **S3 - SUGGESTION - Tests - the `tu` and ADP assertion texts are not pinned.**
  - Where: `tb/tools/torture_campaign.py:3390-3397` and `:3420-3427`; receipt `receipts/planner_mutants_r3.log`.
  - Evidence: N23 reverts the `tu` assertion text to the round-2 wording, and N24 rewrites the ADP text to charge the pre-cut expiry. Both survive the self-test and behave. The structured arguments these texts describe are pinned, since N07-N14 and N19-N22 are all killed, and the texts agree with REQ-VER-06 and 6d today, as checked by reading.
  - Optional outcome: assert their key tokens, for example `0.5 s`, `uncorrelated tu fails`, `measured from T0` and `not charged`.
- **S4 - SUGGESTION - Conformance, Docs - the repository's only boot-time figures do not match the new windows.**
  - Where: `CONTRIBUTING.md:542` ("AX boot probes need >= 8 min windows (power->network ~ 7 min)"); the diagnostic `phys.dut-cycle.power-cycle` budget `net_budget_s: 360` (`tb/tools/torture_campaign.py:3232`). Compare REQ-VER-06 `:290-291`, which requires the first `ENTITY_AVAILABLE` before T0 + 20 s, and the provisional 30 s restore bound.
  - Evidence: the rule is fixed by decision ("Boot must beat the ADP valid time"). Issue #397 also lists "the ADP valid time the boot must beat". So this is not a gate defect, and a gate that the current image might fail is legitimate. But nothing records whether the 7-minute figure still describes the shipping bare-metal image.
  - Optional outcome: before bench items 3 and 4, either note that the figure is superseded or record the measured boot-to-`ENTITY_AVAILABLE` time (#397). Otherwise a first failing campaign could be read as a planner defect.
- **S5 - SUGGESTION - Docs - two stale round labels.**
  - The `ReleaseSettings` comment (`tb/tools/torture_campaign.py:3337`) and the `--restore-bound-s` help (`:5463`) still say "#396 round 2", although the ceiling is now the round-3 constant.

Carried over and outside this delta: R346-1 S3 (malformed `--dut` values raise tracebacks). This is pre-existing and unassigned.

## Round-2 findings, closed or retained at this head

| Finding | Status | Evidence |
|---|---|---|
| R346-2 F1 MINOR = R347-2 F1 MINOR: eligibility ignores `restore_bound_s` | **Closed** | Constant `:3325`, default `:3338`, check `:3504`. Arms 29 and 30 (true), 31 and 3600 (false) are in `test_release_eligibility_boundaries` (`:5000-5007`), and feature examples 29, 30 and 31 are at `torture_campaign_plan.feature:398-407`. In `r2rerun_eligibility_probe.log`, rows 600 and 3600 are false on all three repeats, and 29 is true. The mutants are killed: the executor's "restore eligibility check removed" and "restore ceiling relaxed" (`gate_release_mutants.log`), my N01-N06 (`planner_mutants_r3.log`), and R347-2 R04 (`r347_2_mutants_rerun.log`). The old contradiction at TESTING.md:958 is replaced by `:979-980`, and 6d lists the ceiling among the judged prerequisites (`:878-881`). |
| R346-2 F2 MINOR = R347-2 F4 MINOR: topology key rules untested | **Closed** | `test_release_topology_each_key` (`:5052-5090`) omits each key alone and the CRF pair alone, empties each value, accepts the mixed count/set shapes and refuses `entity_id`, on both roles. The feature outline (`torture_campaign_plan.feature:386-396`) drives the CLI by subprocess, omitting only the CRF keys or only the listener shape, on the DUT and on the peer. My unchanged `planner_mutants_r2.py` gives 48 killed, 0 survived and 2 invalid. The invalid ones are R13 and R19, whose anchors were legitimately replaced by the corrected ADP strings; my N07 and N12 retarget them and are killed. E10, E11, E12, E13 and E15 are killed. R347-2's unchanged `mutants_r2.py` kills R11 and R12 with self-test and behave both rc 1, and 22/22 overall. My N25-N31 are also killed: entity, `crf_in` alone, `crf_out` alone, a one-role check in either direction, index-set acceptance, and the `entity_id` alias. |
| R347-2 F2 MINOR: `tu` bound undecidable | **Closed** | One rule, stated in REQ-VER-06 `:262-270`, the 6d row `:915`, 6d prose `:923-929`, the assertion `:3390-3397` and the plan arguments `:3544-3547`. It is pinned by `test_release_tu_contract` (`:5092`) and the feature scenario at `:409`. Mutants N19-N22 are killed, as are the executor's "tu bound uses media-clock holdover" and "uncorrelated tu ignored". The 0.5 s figure matches `KL_ptp_clock_validity.sv:119-122`, and B.1's 5 s is excluded. See S1 and S2 (optional). |
| R347-2 F3 MINOR: ADP verdict depends on an unstated off time | **Closed** under the corrected decision | `power_off_hold_s` joins the positive-integer validation (`:3346-3351`), with refusal arms for 0, -1, `True` and NaN (`:5024-5028`). It is threaded through the CLI (`:5466`, `:5482`), pinned at 17 through the API (`:4981`) and 13 through the CLI, and emitted with its origin and `power_off_hold_in_adp_window=False` (`:3571-3573`). The ADP arguments are at `:3595-3602`. `adp_hold_probe.log` meets 157 of 157 expectations. Mutants N08, N09, N13, N14, N15, N16 and N17 are killed. |
| R346-2 S1 (cite 5.6.2; the off time is not a parameter) | Taken | 5.6.2 is cited in REQ-VER-06 `:289`/`:296`, 6d `:959`/`:972` and the assertion (`:3420-3427`). The hold is named. |
| R346-2 S2 = R347-2 S1 (power eligibility inherits the soak interval) | Taken, as documentation | 6d `:880-881`: "These shared prerequisites describe the paired release profile. Selecting only one area retains those shared profile checks." |
| R346-2 S3 (`entity_id` alias) | Taken, as documentation | 6d `:888-890`. Refused in `test_release_topology_each_key`; N31 is killed. |
| R346-2 S4 (R16, B04, B09 survivors) | Taken | `restore_requires` is pinned (`:4979-4980`), and the `(1, True)`, `(1, False)` and `(1, -1)` SKIP arms are at `:5123-5124`. R16, B04 and B09 are killed in `r2rerun_planner_mutants_r2.log`, and N33 is killed. |
| R347-2 S2 (a restart after the 35 s window is unobserved) | Taken | Boot evidence now runs "from T0 through next cut or campaign end; at least boot_observation_s" (`:3586-3587`; 6d `:954`, `:985-987`; REQ-VER-06 `:314`). N32 and the executor's control are killed. |
| R347-2 S3 (cite 5.6.2) | Taken | As R346-2 S1 above. |

The round-1 findings, closed at R346-2, stay closed. Nothing in this delta touches their artifacts except as recorded above. My unchanged round-1 `planner_mutants.py` still kills 42 of 44 at this head: A08 is the long-standing informational survivor, and C13 is invalid because its 480 s literal was removed by decision. The round-1 omission probe refused 240 of 240 plants.

## Lens results (reviewer format)

```text
[R346] PASS Conformance - REQUIREMENTS.md:250-321; docs/testing/TESTING.md:841-999; tb/tools/torture_campaign.py:3320-3620; receipts/standards_citation_check.md; receipts/adp_hold_probe.log - each item of decision 5855515133 (ceiling 30 with eligibility false above it; tu from a recorded discontinuity within 0.5 s plus resolution, uncorrelated fails; ADP from T0 within 2*valid_time with valid_time=10 required and the hold recorded, not charged; per-key topology controls) checked against REQ-VER-06, 6d, the assertion text and the emitted arguments, and all agree. Milan 5.6.2/5.6.3 and Annex B.1/B.1.1, IEEE 1722.1-2021 6.2.2.5/6.2.4/6.2.5 and IEEE 1722-2016 4.4.4.7 checked against the extracted text. Suggestions only (S1, S2, S4).
[R346] PASS RTL - receipts/scope_and_gitlinks.log (name-status ac18b509..HEAD and 24d32d54..HEAD; gitlinks for external, gptp-processor, protocol-processor and third_party/verilog-axis identical to base); hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:115-122 - no hdl/, sw/, syn/, builder, firmware or submodule path changed. The one RTL fact the delta newly relies on (HOLD_QTICK_P=2 giving a 0.25-0.5 s discontinuity holdover) is at the cited lines, and the 0.5 s tu bound matches it.
[R346] PASS Robustness - tb/tools/torture_campaign.py:3346-3351, :3500-3528, :3561-3620, :5462-5483; receipts/r2rerun_eligibility_probe.log, receipts/adp_hold_probe.log, receipts/planner_mutants_r3.log - the ceiling is inclusive at 30 (N02 killed) and applies to every repeat (N05/N06 killed). Hold values 0, -1, True and NaN are refused. Holds of 1 to 3600 s move neither the ADP verdict nor eligibility (the hold is provenance; a cold cut is judged by verified discharge). A missing, non-10 or late ADP fails, as do a negative elapsed time and uncorrelated tu. A restart before the next cut fails, and bool or negative boot counts SKIP.
[R346] PASS Tests - tb/tools/torture_campaign.py:4925-5130 (_ReleasePlanChecks); tests/features/torture_campaign_plan.feature:386-412; tests/steps/torture_release_steps.py:217-268; tb/tools/torture_release_mutants.py; receipts/gate_selftest.log, gate_behave_plan.log, gate_behave_torture_tier.log, gate_release_mutants.log, planner_mutants_r3.log, r2rerun_*.log, r347_2_mutants_rerun.log - self-test 49 OK; plan feature 76 scenarios / 321 steps; @torture tier 221 scenarios; executor driver 9/9 killed by named tests; my round-3 mutants 30/30 required killed; my round-2 scripts unchanged (48/50 killed, 2 invalid retargeted and killed; 42/44 round 1; 240/240 omissions); R347-2 script unchanged 22/22. The new tests fail for the defects they name. Assertion-text pinning is S3.
[R346] PASS Docs - REQUIREMENTS.md:262-321; docs/testing/TESTING.md:849-999; CONTRIBUTING.md:416-428 (unchanged by this delta); receipts/gate_docs_check.log, gate_doc_paths.log, gate_doc_style.log, gate_em_dash.log, gate_gen_toc.log, gate_feature_status.log, gate_feature_status_selftest.log, gate_py_idiom.log - REQ-VER-06 and 6d state the tu rule and the corrected ADP rule consistently with the plan's assertion text. Both link the round-3 decision. The command list gains the mutation driver and --power-off-hold-s. Bench items 3 and 4 remain stated as open. All documentation gates are rc 0. Suggestions only (S1, S2, S4, S5).
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:250-321; TESTING.md:841-999; torture_campaign.py:3320-3620; decisions 5789765788, 5854692245, 5854930205, 5855515133; Milan v1.2 5.6.2, 5.6.3, Annex B.1/B.1.1; IEEE 1722.1-2021 6.2.2.5, 6.2.4, 6.2.5; IEEE 1722-2016 4.4.4.7; `receipts/standards_citation_check.md`, `receipts/adp_hold_probe.log` | R346-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| RTL | CLEAN | `receipts/scope_and_gitlinks.log`; `KL_ptp_clock_validity.sv:115-122`; gitlinks at base and head; `receipts/clone_integrity.log` | R346-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Robustness | CLEAN | `ReleaseSettings.__post_init__` (:3346-3351); `_release_profile_eligible`, `_release_topology_explicit` and `check_release_boot` (:3500-3528); `plan_power` (:3561-3620); CLI (:5462-5483); `receipts/r2rerun_eligibility_probe.log`, `receipts/adp_hold_probe.log`, `receipts/planner_mutants_r3.log` | R346-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Tests | CLEAN | torture_campaign.py:4925-5130; torture_campaign_plan.feature:386-412; torture_release_steps.py; torture_release_mutants.py; `receipts/gate_selftest.log`, `gate_behave_plan.log`, `gate_behave_torture_tier.log`, `gate_release_mutants.log`, `planner_mutants_r3.log`, `r2rerun_planner_mutants_r1.log`, `r2rerun_planner_mutants_r2.log`, `r2rerun_plan_omission_probe.log`, `r347_2_mutants_rerun.log` | R346-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |
| Docs | CLEAN | REQUIREMENTS.md section 8; TESTING.md 6d (:841-999); CONTRIBUTING.md:416-428 and :540-547; TAKEN 5855545141 and REVIEW READY 5855671206; docs gate receipts | R346-3 | 8153576af6d739427b54f6c40299b0e57bc481ae |

Every lens was applied at the exact merge-candidate source head. No BLOCKER, MAJOR or MINOR is open under any lens. S1-S5 are SUGGESTION and do not affect coverage.

## Commands run at the exact head (foreground; receipts under `receipts/`)

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 49 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0, 76 scenarios / 321 steps, 0 skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0, 221 scenarios / 866 steps passed, 172 excluded by tag |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0: the pristine baseline passed, 9/9 were killed by their named tests, and the source was unchanged |
| `python3 -B scripts/check_feature_status.py --self-test`; `python3 -B scripts/check_feature_status.py` | rc 0 (46/46); rc 0 (0 findings) |
| `python3 -B scripts/docs_check.py`; `check_doc_paths.py`; `check_doc_style.py`; `check_py_idiom.py` | rc 0 each (0 findings; 850 paths; 22 documents; no ratchet increase) |
| `check_em_dash.py --base ac18b509...`; `gen_toc.py --check` (pinned markdown environment) | rc 0 (0 findings, 339/339 arms); rc 0 |
| `torture_campaign.py --coverage-by-area --areas soak,power` | rc 0 |
| `git diff --check ac18b509.. HEAD`; `git diff --check 24d32d54.. HEAD` | rc 0; rc 0 |
| `scripts/r2_unchanged/planner_mutants.py` (round 1, sha256 `d26698bc...`) | 44 mutants: 42 killed, 1 survived (A08, informational), 1 invalid (C13) |
| `scripts/r2_unchanged/plan_omission_probe.py` (sha256 `e1b0b026...`) | 240 omissions, 0 accepted |
| `scripts/r2_unchanged/planner_mutants_r2.py` (sha256 `e413b335...`) | 50 mutants: 48 killed, 0 survived, 2 invalid (R13, R19: superseded ADP anchors) |
| `scripts/r2_unchanged/eligibility_probe.py` (sha256 `2b635b73...`) | the 600 s and 3600 s bounds are now `eligible=False` on every repeat |
| public R347-2 `scripts/mutants_r2.py` (blob `0595c826`, sha256 `bcbbd4a0...`, unchanged), on a `git archive` of the head | 22/22 killed, including R11 and R12; archive bytes restored |
| `scripts/planner_mutants_r3.py` (new) | 34 mutants: 30/30 required killed; reported and not required: N18 (equivalent), N23 and N24 (text, S3), S01 (redundant test oracle) |
| `scripts/adp_hold_probe.py` (new) | 157/157 expectations met |

## Real limits

- This is desk review only. No hardware, bench, power strip, Docker, act, host runner or full parent/PP/gPTP/Yosys/builder bank was run. Physical calibration was NOT RUN, and no field skip is taken as hardware proof.
- The pinned Verilator was not used, because the delta contains no RTL.
- The linked public evidence tree at `4949b127` is the round-1 author packet. The round-3 author packet is at `396-review-evidence` `641dac72`. No manager source-bank evidence for `8153576a` was found on the issue or the PR at review time. This review relies only on its own reruns above.
- Hosted checks were only snapshotted (`receipts/hosted_checks_snapshot.txt`, 12:16Z):
  - Succeeded: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, and Yosys shards 0-3/4.
  - Still in progress: `docs-check`, `elaborate`, `yosys-elaboration`, and Verilator shards 0-4/5.
  - Skipped: `Physical gPTP (nightly and manual)`.

  No conclusion is drawn from in-progress or skipped contexts.
- The 30 s ceiling is provisional by decision. The feasibility of the 20 s T0 ADP window and the 30 s restore bound on the shipping image is unmeasured (S4, #397).
- Standards checks cover only the clauses the delta cites or changes.
- The clone was never written. After all probes, the checks in `receipts/clone_integrity.log` pass:
  - HEAD, tree, and index equal to HEAD;
  - every tracked blob's bytes, with 0 mismatches;
  - the modes of the changed files;
  - no assume-unchanged or skip-worktree flags;
  - the four gitlinks.

  `external` is uninitialised, exactly as it was cloned.

## Pending manager duties

- Hosted and act acceptance of this exact head, and the final current-dev candidate at the merge turn (source base `ac18b509`, live dev `63fe4fb0`).
- Ratify `RELEASE_RESTORE_BOUND_S` from the #397 and #75 measurements, as REQ-VER-06 states. Consider S4 at the same time.
- Decide whether to take S1-S5. They are optional.
- R347-1 F1 part (b), the pre-existing 1722.1-2021 6.2.6 attributions at `torture_campaign.py:1456`, `:2769`, `:3096` and `:3104`, remains the manager's call for a new Issue.
- Items 3 and 4 of #396 (the physical campaigns and the negative control) remain open bench work.
- Merge requires two independent positive reviews and the full AGENTS.md section 7 bar. This report is one of them.

R346-3 FINISHED
