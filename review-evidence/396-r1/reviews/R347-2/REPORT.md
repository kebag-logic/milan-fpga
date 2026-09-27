[R347] NEGATIVE - exact head 24d32d549fa7470318a93984403a92423a63fa25

# R347-2 external independent review: issue #396 / PR #586

- Round: R347-2, external independent reviewer, cleared context. This is a delta review of `b7b74b8b..24d32d54`. Round R347-1 covered `b7b74b8b`.
- Exact head: `24d32d549fa7470318a93984403a92423a63fa25`, tree `0a39af1c8563cf61ea28cb89e834ee92cd82acfd`. The head is one commit on `b7b74b8b`, which is one commit on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope: desk acceptance items 1, 2 and 5. Bench items 3 and 4 stay open, and the PR says `Refs #396`.
- Reconstructed from, in this order:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #396 body, the owner decision (5789765788), the round-1 assignment (5854692245) and the round-2 decision (5854930205);
  - [A359] TAKEN (5854960348), REVIEW READY (5855070445) and the PR body;
  - issues #75, #366 and #397;
  - REQUIREMENTS.md section 8, TESTING.md 6d, REGISTER_MAP.md, BUILDING.md section 4 and GM_LOSS_RECOVERY.md;
  - the cited Milan v1.2, IEEE 1722-2016 and IEEE 1722.1-2021 pages, which I extracted myself (`receipts/citation-check.txt`);
  - `git diff b7b74b8b..24d32d54` and `ac18b509..24d32d54`, then the public evidence.
- Prior public findings: after my own pass I read R346-1 (PR comment 5854927625) and my own R347-1 (5854920974). Every finding in both is resolved below.

## Verdict summary

The round-2 commit does what the round-2 decision asked:
- T0 is the power-strip ON command.
- The ADP deadline is derived per cycle from the last pre-cut ENTITY_AVAILABLE.
- `restore_bound_s` is a named, provisional 30 s bound from T0. It is inclusive, and an overrun fails.
- The #75 `CONNECT_RX` check is additional and runs after restoration.
- The boot window is `restore_bound_s + boot_margin_s`. No 480 s literal remains.
- The timing parameters are pinned at non-default values: self-test 19/11, CLI 23/7, feature 23/7.
- Every clause citation I extracted is correct.
- `release_eligible` refuses the three required cases, each with a self-test arm.
- Every round-1 survivor is killed by a named test: my 21 mutants, and R346's A04, A05, P01, P03, P07, C01 and C08.
- The single-boot oracle fails the #366 double pass.
- No firmware, RTL, builder or gitlink file changed, and no bench item is claimed done.
- Every gate I ran passes.

Four new MINOR findings are open, so the verdict is NEGATIVE:
- F1: `release_eligible` stays true for any relaxed `restore_bound_s`.
- F2: the `tu` pass bound is no longer decidable.
- F3: the ADP verdict depends on an unstated power-off duration.
- F4: two of the documented topology requirements have no test.

## Findings

### F1 MINOR - Conformance, Robustness, Tests, Docs - `release_eligible` stays true for any relaxed `restore_bound_s`

- **Where:** `tb/tools/torture_campaign.py:3491-3495` (`_release_profile_eligible`), `:3571-3573` and `:3590` (power eligibility), `:3336` (the default of 30); `docs/testing/TESTING.md:871-880` and `:958`; `tb/tools/torture_campaign.py:4970` (`test_release_eligibility_boundaries`).
- **Authority/evidence:**
  - REQ-VER-06 (`REQUIREMENTS.md:290`) says "The bound is provisionally 30 seconds; overruns fail". The decision (5854930205) adds: "A cycle exceeding it fails. It is never unbounded."
  - TESTING.md:958 says non-default values are for "diagnostic measurement without changing the provisional default".
  - The eligibility check never reads `restore_bound_s`. `receipts/probe-r2.log` shows `--restore-bound-s 3600` with both explicit specs emitting `release_eligible: [true, true, true]`. So does `restore_bound_s=31` through the API. Any positive integer is accepted.
  - No eligibility arm varies the bound, so the tests cannot catch this.
  - This is the same defect class as R346-1 F3: the flag is true for a profile the contract says cannot qualify.
- **Impact:** a plan that loosens the only automatic-restoration deadline, even to an hour, reports itself release-eligible. A bench runner that trusts the flag qualifies a candidate against a bound REQ-VER-06 forbids.
- **Required outcome:**
  - Eligibility refuses any `restore_bound_s` above the decided (or later ratified) release bound, held as one named constant. A tighter bound may stay eligible.
  - TESTING 6d lists this among the prerequisites the flag judges.
  - An eligibility arm covers a bound one second above the release value.
- **Verification:** the probe row `restore_bound_s relaxed to 31` emits false. A mutant that drops the new check is killed.

### F2 MINOR - Conformance, Docs - the `tu` pass bound is no longer decidable

- **Where:** `docs/testing/TESTING.md:907` and `:915-916`; `REQUIREMENTS.md:262-265`; `tb/tools/torture_campaign.py:3386-3391`.
- **Authority/evidence:**
  - The decision's criterion is "no `tu` beyond holdover". At `b7b74b8b`, the TESTING 6d evidence table's "Required result" cell for `tu` read "No uncertainty beyond Milan Annex B.1.1 holdover".
  - At this head that cell holds only citations: "IEEE 1722-2016 4.4.4.7; Milan Annex B.1/B.1.1". The row no longer states a result.
  - REQ-VER-06 keeps "the applicable holdover" and now names two different values beside it:
    - B.1.1: `tu` is set for 0.25 s on a GM change;
    - B.1: a recommended media-clock holdover of at least 5 s.

    It does not say which one bounds `tu`.
  - The design reads B.1.1 as a minimum. `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:119-122` holds `tu` for 0.25 to 0.5 s, and GM_LOSS_RECOVERY.md:64 says "at least 0.25 seconds".
- **Impact:** if a GM change occurs during the seven-day soak, a correct 0.4 s `tu` interval fails under a 0.25 s reading and passes under a 5 s reading. The graders of a MUST release gate can disagree, and the table no longer tells them what passes.
- **Required outcome:**
  - REQ-VER-06 and the 6d table state the numeric bound or rule a `tu` interval is graded against. One example: "set only in correlation with a recorded discontinuity, and cleared within the implemented discontinuity holdover".
  - The `tu` row of the table carries a required result again.
  - If the bound needs a choice beyond the decision, the choice is recorded on #396.
- **Verification:** the text names one bound, the table cell states a result, and the assertion text agrees with both.

### F3 MINOR - Conformance, Robustness, Docs - the ADP verdict depends on a power-off duration the plan never states

- **Where:** `REQUIREMENTS.md:279-284`; `docs/testing/TESTING.md:921`, `:934` and `:944-950`; `tb/tools/torture_campaign.py:3576-3582` (`cold_confirmation="power removed; discharge verified"` has no duration; `adp_deadline`). Compare `tb/tools/torture_campaign.py:3231-3241` and `:4653`.
- **Authority/evidence:**
  - The decision measures the ADP deadline from the last pre-cut ENTITY_AVAILABLE. Milan v1.2 5.6.2 (PDF p109) fixes `valid_time` at 10 in ENTITY_AVAILABLE, which is 20 s with re-advertisement every 5 s. REGISTER_MAP.md:996 confirms that constant for this processor.
  - So the whole cut counts against a 20 s window: the time since the last advertisement (0 to 5 s), the power-off hold, and then boot to the first advertisement.
  - The same planner's DUT power-cycle contract (`phys.dut-cycle.power-cycle`, `:3231-3241`) holds power off for 8 s ("off for at least 8 s"), and its self-test requires `off_s >= 5` (`:4653`).
  - At that established hold, `adp_deadline` at T0 is only 7 to 12 s (`receipts/probe-r2.log`, formula rows). At 15 s it is 0, and the cycle fails by construction.
  - The release power args carry no off-time parameter. REQ-VER-06 and 6d do not say that the off time is charged against the window.
  - TAKEN and REVIEW READY do not flag the dependency. AGENTS.md section 2 requires such a gap to be published for a decision.
- **Impact:** for the same image, the verdict of `power.adp-valid-time` changes with a bench choice that is neither recorded as a parameter nor bounded. A runner that reuses the repository's own 8 s cold-cut practice, or waits longer to "confirm discharge", can fail every cycle. It would then file findings against the DUT for a bench artifact (acceptance item 3), and two runs of one image could disagree.
- **Required outcome:** one of these, whichever the manager records:
  - a named power-off hold parameter in the release power args, with its origin and bound, pinned at a non-default value in the self-test, and REQ-VER-06/6d stating that the hold and the pre-cut interval are charged against the pre-cut advertisement window (20 s at Milan's `valid_time=10`); or
  - a recorded decision on #396 that states how the off time is set and graded.
- **Verification:** the emitted power args and the requirement row both name the hold and its bound, and a self-test arm pins it.

### F4 MINOR - Tests - two of the documented topology requirements have no test

- **Where:** `tb/tools/torture_campaign.py:3498-3507` (`_release_topology_explicit`), `:4996` (`test_release_topology_provenance_cli`); `docs/testing/TESTING.md:882-883`.
- **Authority/evidence:**
  - TESTING.md says each CLI topology "must explicitly provide `entity`, `mac`, and CRF indices" and "both AAF counts or both index sets".
  - The test's cases are: no spec, DUT only, peer only, `name=dut` with a full peer, and both full. None of them omits only the CRF keys or only the listener shape.
  - In `receipts/mutants-r2.log`, two of my 22 new mutants pass both gates:
    - R11 drops the `crf_in`/`crf_out` requirement;
    - R12 drops the listener-shape requirement.
  - The reviewed code is correct today. The probe shows a peer spec without `listener_index_set` gives `topology_explicit: false`.
  - AGENTS.md Tests lens: "Each new test can fail for the defect it claims to detect".
- **Impact:** a later edit could let a spec that inherits the fixture's CRF indices or listener count pass as explicit and release-eligible. That is exactly the desk-fixture case the decision's item 3 refuses.
- **Required outcome:** arms that omit only the CRF keys, and only one AAF shape, each expecting `topology_explicit: false`.
- **Verification:** rerun `scripts/mutants_r2.py`. R11 and R12 are killed.

### Suggestions (non-blocking; no effect on coverage)

- **S1 - Robustness:** power eligibility depends on `soak_interval_s` (`:3495`). A power-only plan with `--soak-interval-s 61` reports false. This is documented (TESTING.md:873) but mixes the areas. Consider judging the sampling ceiling on the soak area only.
- **S2 - Robustness:** `power.single-boot` observes only T0 through `restore_bound_s + boot_margin_s` (35 s by default). A restart after that and before the next cut is outside every power assertion, because the power area has no uptime-continuity check like `soak.uptime-monotonic`. Consider an uptime or boot-count reading in the post-cycle counter walk.
- **S3 - Docs:** the ADP rule decodes the `valid_time` value that Milan 5.6.2 fixes at 10. Citing 5.6.2 next to 5.6.3 would give the bench the 20 s figure directly.

## Round-1 findings at this head

| Finding | State | Evidence |
|---|---|---|
| R347-1 F1 (citations) = R346-1 F2 | CLOSED | Every release clause string and REQ-VER-06 authority line checked against the extracted pages (`receipts/citation-check.txt`): 4.4.4.6 on SEQ_NUM, 4.4.4.7 on `tu`, 4.2.6.2.4 on asCapable, 6.2.2.5 with 6.2.4/6.2.5 on ADP, 5.3.8.2/5.3.8.3 on binding, the full inventory list, 5.5.2.4 for Controller Bind (5.5.2.2 renames CONNECT_RX to BIND_RX). The REQ-VER-06 row now carries citations (R346-1 F2a). The older 6.2.6 strings at `:1456`, `:2769`, `:3096`, `:3104` are outside the diff and stay with the manager. |
| R347-1 F2 = R346-1 F1 (unbounded restore, undefined origins) | CLOSED | Decision 5854930205 is encoded in REQUIREMENTS.md:279-300, TESTING.md:922-958 and the power args at `:3556-3589`. The args carry T0, `restore_bound_s` (inclusive, provisional, with its origin), the derived ADP formula, the additional `CONNECT_RX` check and the derived boot window. `test_release_timing_and_snapshot_contract` pins 19/11, the CLI test pins 23/7, and the feature pins 23/7. My mutants R05, R06, R07, R08, R09 and R21 are killed. The residual gaps are new findings F1 and F3. |
| R347-1 F3 (one-sided audit controls) | CLOSED | Mutants A1, A2, A3, A5 and A6 are killed (`receipts/mutants.log`). The named tests are `test_release_counter_omissions_in_every_repeat`, `test_release_binding_omissions_in_every_repeat`, and feature scenario outline `:342` rows @1.1-@1.30 (`receipts/kill-attribution.log`). The audit probe still rejects D1-D6 (`receipts/audit-probe.log`). |
| R347-1 F4 (parameters pinned at defaults) | CLOSED | P1 and P2 are killed by `test_release_settings_validation` (interval 17, total 3), `test_release_cli_parameters` and feature `:381`. P3 is killed by `test_release_eligibility_boundaries` (the 199/1 and 159/41 arms). |
| R346-1 F3 (eligible profiles that cannot qualify) | CLOSED for the three named cases | `test_release_eligibility_boundaries` has arms for interval 61 and 604800, for `persisted_items=("clock_source",)` and for `topology_explicit=False`, and asserts false for the default fixture plan. `test_release_topology_provenance_cli` covers the CLI. TESTING.md:871-889 states what the flag judges. A fourth case, a relaxed restore bound, is new finding F1. |
| R346-1 F4 (surviving mutants) | CLOSED | R346's unchanged `planner_mutants.py` (sha256 `d26698bc...`, equal to its public manifest) reports 42/44 killed. A08 is informational, and C13 is invalid because its 480 s anchor was removed by the decision; my R05 covers the new derivation. Named killers (`receipts/r346-kill-attribution.log`): A04 by `test_release_binding_omissions_in_every_repeat`; A05 by both omission tests; P01 and P03 by `test_release_cli_parameters` and `test_release_settings_validation`; P07 by `test_release_cli_parameters`; C01 by `test_release_timing_and_snapshot_contract` and feature `:335`; C08 by `test_release_eligibility_boundaries`. The omission probe planted 240 omissions and all were refused. |
| R347-1 S1 (soak interval) | CLOSED | Ceiling `RELEASE_MAX_SOAK_INTERVAL_S = 60` (`:3323`). The arms for 61 and 604800 are false, and the audit probe's 7-day endpoints-only row is false. |
| R347-1 S2 (AAF set including the CRF index) | CLOSED | `_release_pairs` refuses the overlap (`:3460-3463`). Four CLI forms exit with rc 2 (`receipts/probe-r2.log`). `test_release_crf_overlap_refused` covers it, and mutants R13 and R14 are killed. |
| R347-1 S3 (#366 control has no assertion) | CLOSED | `power.single-boot` and `check_release_boot` (`:3431-3435`, `:3510-3518`) fail on (2,1), (2,0), (1,1) and (0,0), and return SKIP on incomplete capture. SKIP cannot qualify under `release.complete-evidence`. `test_release_boot_negative_control` and feature `:386` cover it, and mutants R15, R16, R17 and R20 are killed. |
| R346-1 S1-S3 | not findings | S2 is superseded, because the 480 s literal is gone. S1 and S3 are optional and outside coverage. |

## Clean-lens evidence

[R347] PASS RTL - `git diff --stat ac18b509..24d32d54` and `b7b74b8b..24d32d54`; `receipts/clone-integrity-after.txt`; `docs/reference/REGISTER_MAP.md:996` and `:1251`; `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:119-122` - Checked:
- The round-2 delta touches only REQUIREMENTS.md, TESTING.md, `tb/tools/torture_campaign.py`, the plan feature and `torture_release_steps.py`. No path under `hdl/`, `sw/` or `syn/` changed, and the four gitlinks are unchanged (`external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 0922e434, `third_party/verilog-axis` 48ff7a7e).
- The two new RTL-facing claims hold. The processor's ADP `valid_time` is the constant 10 (20 s) per Milan 5.6.2, which is what the plan decodes. `AVTPRX_TSD` stays restricted to `STREAM_INPUT[0]`.
- The RTL's `tu` holdover (0.25 to 0.5 s) is the input to F2, which is filed against the requirement text, not the RTL.
- Hosted `rtl-fast`, `verilator-lint`, `yosys-elaboration` and Yosys shards 0-3 report success at the exact head (`receipts/hosted-check-runs.tsv`).

Conformance, Robustness, Tests and Docs are UNCLEAN (F1 to F4). What I checked clean inside them:
- The decision's five elements match REQ-VER-06, TESTING 6d and the args, with the provisional status and the #397/#75 ratification path stated.
- Every citation is correct.
- `ReleaseSettings` rejects non-positive, bool and NaN bounds and margins, and a non-bool `topology_explicit`.
- The CRF-overlap refusal leaves matrix-only plans unaffected (rc 0).
- The 6d commands, artifacts and open items 3/4 are consistent, and no hardware result is claimed.

## Commands and results (this reviewer, exact head, foreground)

`receipts/gate-summary.txt` lists the exact commands. `$MDPY` is the pinned Markdown environment built from `tools/markdown/requirements.txt` (sha256 prefix 40cdefe08ebd).

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 47 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0: 68 scenarios and 297 steps passed, none skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0: 213 scenarios passed, 172 skipped by tag |
| `scripts/check_feature_status.py --self-test` / without it | rc 0, 46/46 / rc 0, 0 findings |
| `scripts/docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_py_idiom.py` | rc 0 each (0 findings; 850 paths; 22 documents; no ratchet increase) |
| `$MDPY -B scripts/check_em_dash.py --base ac18b509...`, `$MDPY -B scripts/gen_toc.py --check` | rc 0 (0 findings, 339/339 arms), rc 0 |
| `git diff --check`; `git diff ac18b509... HEAD --check` | rc 0; rc 0 |
| `torture_campaign.py --coverage-by-area --areas soak,power`; `--plan --areas soak,power --json` | rc 0; rc 0 |
| `scripts/mutants.py` (round 1, unchanged, sha256 `1e8eaec5...`) | 21/21 killed; source bytes restored |
| `scripts/kill_attribution.py` | names the killing tests for all 21 |
| `scripts/audit_probe.py` (round 1, unchanged, sha256 `add5732a...`) | the reviewed audit rejects D1-D6; the S1 row is now false |
| R346-1 `planner_mutants.py` / `plan_omission_probe.py`, unchanged | 42/44 killed (A08 informational, C13 invalid) / 240 omissions, 0 accepted |
| `scripts/r346_attribution.py` | names the killing tests for A04, A05, P01, P03, P07, C01 and C08 |
| `scripts/mutants_r2.py` (22 mutants on the round-2 code) | 20 killed; R11 and R12 survive (F4) |
| `scripts/probe_r2.py` | evidence for F1, F3 and F4, and for the S2 closure |

After the probes, the clone is byte-identical to the head (`receipts/clone-integrity-before.txt`, `-after.txt`, `-compare.txt`):
- porcelain empty;
- index listing sha256 `27effb36...` unchanged;
- `torture_campaign.py` blob `a7d1a9be` with sha256 `d7e99433...`;
- all 7 changed-file blobs match HEAD;
- the four gitlinks unchanged.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | REQUIREMENTS.md:250-310; decision 5854930205; plan args and assertions :3320-3602; Milan v1.2 p23-24, 40-44, 72-76, 108-112, 141; IEEE 1722-2016 p37; IEEE 1722.1-2021 p49, 55-58; issues #75, #366, #397 | R347-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| RTL | CLEAN | delta and full diff stat; gitlinks; REGISTER_MAP.md:996, :1251; KL_ptp_clock_validity.sv:119-122; hosted lint/Yosys at exact head | R347-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Robustness | UNCLEAN (F1, F3) | ReleaseSettings validation; eligibility, restore-bound and margin probes; CRF-overlap and topology CLI probes; `check_release_boot` edges; ADP window arithmetic against :3231-3241 | R347-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Tests | UNCLEAN (F1, F4) | `_ReleasePlanChecks` :4773-5047; feature :335-388; torture_release_steps.py; 21 + 44 + 22 mutants with kill attribution; audit and omission probes | R347-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Docs | UNCLEAN (F1, F2, F3) | REQUIREMENTS.md section 8; TESTING.md:841-992; PR body; TAKEN and REVIEW READY; docs gates | R347-2 | 24d32d549fa7470318a93984403a92423a63fa25 |

## Real limits

- Desk review only. Physical calibration was NOT RUN, and nothing here is hardware proof. The hosted `Physical gPTP` context is skipped, which is not evidence.
- At capture (2026-09-27T10:45Z), hosted `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were still in progress. They are recorded but not relied on.
- The only manager evidence for this head that I found publicly is the assignment statement. The evidence tree `4949b127` and branch tip `68de0cfe` carry round-1 material and the executor's round-2 logs. I did not rerun the full parent/PP/gPTP/Yosys/builder banks, Docker/act or any hardware step, as assigned. No simulator was needed or run, because the diff has no RTL.
- Standards handling: only the listed pages were extracted, into unpublished scratch that was deleted after use. No standards text is published beyond clause headings and short facts.
- I have no measured boot time for the AX7101. F3 rests on the plan's own formula, Milan's fixed `valid_time` and the repository's 8 s power-off practice, not on a bench number.
- All mutants are textual and target the release code. A survivor shows a gap in the tests, not a defect in the reviewed code.

## Pending manager duties

- Route F1 to F4 to the executor. F3 needs a recorded decision on the power-off hold, and F2 needs one only if the `tu` bound is not derivable from the existing decision.
- Hosted and act acceptance at the exact head, and the final current-dev candidate at the merge turn (source base and live dev both `ac18b509` at review time).
- Ratify `restore_bound_s` from #397 and #75 when measured.
- File the new Issue for the older 1722.1-2021 6.2.6 attributions (`torture_campaign.py:1456`, `:2769`, `:3096`, `:3104`), carried over from R347-1.
- Re-review of the corrected head by both reviewers. Bench items 3 and 4 stay open under #396.

R347-2 FINISHED
