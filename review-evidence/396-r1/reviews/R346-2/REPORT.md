[R346] NEGATIVE - exact head 24d32d549fa7470318a93984403a92423a63fa25

# R346-2 internal independent review: issue #396 / PR #586 (desk lane), round 2

- Head: `24d32d549fa7470318a93984403a92423a63fa25`, tree `0a39af1c8563cf61ea28cb89e834ee92cd82acfd`. It is one commit on `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`, which is one commit on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- This is a delta review of `b7b74b8b..24d32d54`, judged against the round-2 decision (issue comment 5854930205) and the round-1 decisions (5854692245, 5789765788). The full `ac18b509..24d32d54` diff was re-read where the delta touches it.
- Reconstruction order:
  1. AGENTS.md and CONTRIBUTING.md; docs/README.md.
  2. The issue #396 decisions, issue #75, #397 and #70.
  3. REQUIREMENTS.md section 8 and TESTING.md 6d at head.
  4. The cited Milan v1.2, IEEE 1722-2016 and IEEE 1722.1-2021 pages, extracted for this round.
  5. The delta diff and the commit.
  6. Public evidence: the `396-review-evidence` branch at `68de0cfe`, including `review-evidence/396-r1/author-r2/`, and the TAKEN and REVIEW READY comments. The author's `gates.json` (head `24d32d54`, all rc 0), `internal-mutants.log` (42/44, A08 survived, C13 invalid) and `external-mutants.log` (21/21) agree with my independent reruns.

  The other reviewer's round-1 report was read only after this verdict and ledger were written (section "Round-1 findings (R347-1)").
- Bench items 3 and 4 are not claimed done. The PR says `Refs #396`, keeps both unchecked, and TESTING.md:986-992 says they remain open.

## Verdict basis

The head answers the round-1 contract. The round-2 decision is encoded as named, sourced parameters:
- T0 is the power-strip ON command.
- The ADP deadline is derived per cycle from the last pre-cut `valid_time`.
- `restore_bound_s` is a provisional 30 s, with #397/#75 ratification stated.
- #75's `CONNECT_RX` bound is an additional check after restoration.
- The boot window is `restore_bound_s + boot_margin_s`, with no 480 s literal.

The encoding is consistent across `REQUIREMENTS.md:279-303`, `TESTING.md:922-958` and the `power` step args (`torture_campaign.py:3554-3591`). The self-test pins these values at non-default settings (19/11 and 23/7). The CLI test pins interval 17 and total 3.

Other results at this head:
- Every citation checked is correct against the extracted pages (`receipts/standards_citation_check.md`).
- My round-1 mutant script, run unchanged, now kills all seven listed survivors: A04, A05, P01, P03, P07, C01 and C08 (`receipts/planner_mutants.log`).
- My unchanged omission probe still refuses all 240 planted omissions.
- All declared gates are rc 0.
- There is no RTL, firmware, builder or gitlink change.

Two MINOR findings remain open, so the verdict is NEGATIVE:
- R2-F1: the new `restore_bound_s` parameter can be raised without limit while the plan still reports `release_eligible: true`. That reopens, through a parameter, the unbounded restoration that round-1 F1 was about.
- R2-F2: the per-key rules that define an "explicit" topology have no test that can fail. Five source mutants of those rules survive.

## Findings

### R2-F1 - MINOR - Conformance, Robustness, Tests, Docs - `release_eligible` stays true for any `restore_bound_s`

- Artifacts: `tb/tools/torture_campaign.py:3491-3495` (`_release_profile_eligible`), `:3336`, `:5375`; `tb/tools/torture_campaign.py:4970-4994` (`test_release_eligibility_boundaries`, no restore-bound arm); `REQUIREMENTS.md:288-291`; `docs/testing/TESTING.md:871-880`, `:958`; receipt `receipts/eligibility_probe.log`.
- Authority and evidence:
  - The decision says the bound is "provisional 30 s ... A cycle exceeding it fails. It is never unbounded."
  - REQ-VER-06 says "The bound is provisionally 30 seconds; overruns fail."
  - TESTING.md:958 says "Parameters permit diagnostic measurement without changing the provisional default", which tells the reader that a non-default bound is diagnostic.
  - The eligibility function judges topology, inventory and interval only. With an explicit topology, `--restore-bound-s 600` and `--restore-bound-s 3600` both emit `release_eligible: true` on both power repeats, with `restore_bound_s` 600 or 3600 as the per-cycle deadline (`receipts/eligibility_probe.log`, rows "explicit restore-bound 600/3600").
  - This is the same class as round-1 F3, where the flag was true for profiles that cannot satisfy REQ-VER-06. Here it applies to the parameter that round 2 introduced to close round-1 F1.
- Impact: a bench plan can mark itself release-eligible while grading automatic restoration against an hour-long deadline. That is the post-cut restoration defect class (#75/#366) the power campaign exists for. The flag is the plan's only qualification statement, and it is wrong for this input.
- Required outcome: one of the following.
  - `release_eligible` is false whenever `restore_bound_s` exceeds the recorded bound, which is today's provisional default and later the ratified value. A self-test arm fails if that refusal is removed. TESTING.md:871-880 lists the bound among what the flag judges.
  - Or TESTING.md states explicitly that the flag does not judge `restore_bound_s` and that the bench must refuse a non-recorded bound. It must also remove the contradiction with `:958`.
- Verification: rerun `scripts/eligibility_probe.py`. The two rows must show `eligible=False` on the power repeats, or the docs must say so explicitly. Also run a source mutant that removes the new refusal; it must be killed.

### R2-F2 - MINOR - Tests - the explicit-topology key rules have no negative control

- Artifacts: `tb/tools/torture_campaign.py:3498-3507` (`_release_topology_explicit`); `:4996-5012` (`test_release_topology_provenance_cli`); `docs/testing/TESTING.md:882-885`; receipt `receipts/planner_mutants_r2.log`.
- Evidence:
  - TESTING.md:882-885 defines an explicit topology. It must carry `entity`, `mac`, both CRF indices, and an AAF count or set for each role. "Partial overrides remain diagnostic because they inherit fixture data."
  - The test's docstring claims "missing or partial device specs do not" qualify. Its only partial spec, `name=dut`, lacks every required key, so it cannot distinguish any one rule.
  - These source mutants survive both the self-test and the plan feature:
    - E10: `mac` no longer required.
    - E11: CRF indices no longer required.
    - E12: listener shape no longer required.
    - E13: talker shape no longer required.
    - E15: an empty value counts as provided.
  - The head behaves correctly today: `receipts/eligibility_probe.log` shows a DUT without `mac`, and a peer without `crf_in`, both refused. So this is test strength, not a product defect.
- Impact: a later edit can make a partial override that inherits fixture CRF indices or AAF counts release-eligible, with every gate green. That is exactly the round-1 F3 case (desk fixtures qualifying) that the round-2 decision asked to refuse.
- Required outcome: a negative control per documented key rule. Each spec that lacks exactly one required key, or carries it with an empty value, yields `topology_explicit: false` and `release_eligible: false`.
- Verification: rerun `scripts/planner_mutants_r2.py`. E10-E13 and E15 must be killed.

### Suggestions (non-blocking; do not affect coverage)

- S1 - Docs/Conformance: the Milan ADP value, "valid_time field shall be set to 10" (20 s; advertise every 5 s), is in Milan 5.6.2 (p.101). The head cites 5.6.3, the advertiser state machine, as the decision does. That is correct as phrased, but adding 5.6.2 would show the bench what the per-cycle ADP deadline implies. With a compliant DUT, T0 plus boot-to-advertise must fall within about 20 s of the last pre-cut advertisement, discharge time included. The bench's off duration is not a named parameter. This is a feasibility input for the manager's ratification (#397), not an executor defect.
- S2 - Docs/Robustness: power-area eligibility also depends on `soak_interval_s` (a power-only plan with `--soak-interval-s 120` is ineligible; `receipts/eligibility_probe.log`). It is documented at TESTING.md:873 and follows the decision's wording, but the power area has no sampling interval. Consider scoping the ceiling to the soak area, or saying why power inherits it.
- S3 - Docs: `entity_id=` is an accepted `--dut` alias, but it does not count as explicit (`receipts/eligibility_probe.log`). This fails safe, and TESTING.md:882 names `entity`. Consider accepting the alias or saying it is not accepted.
- S4 - Tests: some surviving mutants are fail-safe and informational.
  - The `restore_requires` string is unpinned (R16).
  - `check_release_boot` input-type edges survive: a bool `restarts` (B04) and a negative `restarts` (B09). Under B04, `restarts=True` gives FAIL and `restarts=False` is read as zero (PASS), where the head gives SKIP. Under B09, a negative count gives FAIL instead of SKIP. Neither mutant lets a repeated BIOS pass or a real restart PASS.
- The round-1 S3 (malformed `--dut` value tracebacks) is still pre-existing and outside this diff. Round 2 did not take it up and the decision did not assign it.

## Round-1 findings (R346-1), closed or retained at this head

| Round-1 finding | Status | Evidence |
|---|---|---|
| F1 MAJOR: automatic rebind after a cold cut unbounded | **Closed** | Decision encoded as named parameters with origins: `REQUIREMENTS.md:279-303`, `TESTING.md:922-958`, `power` args `torture_campaign.py:3554-3591` (`time_origin`, `restore_start="T0"`, `restore_end`, `restore_bound_s`, `restore_bound_provisional`, `restore_bound_origin`, `adp_reference`/`adp_deadline`/`adp_elapsed`, `rebind_requires`, `boot_observation_s = restore_bound_s + boot_margin_s`). New assertion `power.automatic-restore-bound` cites Auto Connect; `power.rebind-bound` now cites Controller Bind and is "additional". "Network readiness" is gone. Pinned at non-default values (`test_release_timing_and_snapshot_contract`, behave "release timing and totals are parameterized"); mutants R01-R15, R17-R20 killed. The residual eligibility gap is new finding R2-F1, not a retention of F1. |
| F2 MINOR: citations missing or mis-attached | **Closed** | (a) The REQ-VER-06 row now carries clause anchors for every criterion. (b) 4.4.4.6 is on the sequence assertion and 4.4.4.7 on `tu`. (c) asCapable cites 4.2.6.2.4. (d) The binding cites 5.3.8.2/5.3.8.3. (e) ADP cites 6.2.2.5 and 6.2.4/6.2.5. All were checked against extracted pages (`receipts/standards_citation_check.md`); S1 is optional. |
| F3 MINOR: `release_eligible` true for profiles that cannot qualify | **Closed** for the three named cases | Interval ceiling 60 s, the stream-binding inventory and an explicit topology are all required (`torture_campaign.py:3491-3507`). Self-test arms: `soak_interval_s` 61 and 604800, `persisted_items=("clock_source",)`, and `topology_explicit=False` (`:4970-4994`); fixture/partial CLI specs (`:4996-5012`). Probes: `receipts/eligibility_probe.log`. TESTING.md:871-889 states what the flag judges. The new parameter's gap is R2-F1. |
| F4 MINOR: arms without a failing test | **Closed** | `scripts/planner_mutants.py` run unchanged: 42/44 killed, including all of A04, A05, P01, P03, P07, C01 and C08. A08 is the informational survivor from round 1. C13 is invalid because its `boot_observation_s=480` anchor was removed by the decision; its replacements R03/R04 are killed. Killing tests: A04 by `test_release_binding_omissions_in_every_repeat` (kind `aaf`) and the behave "AAF direction" rows; A05 by `test_release_counter_omissions_in_every_repeat` and the behave rows per repeat; P01 by interval 17 in `test_release_settings_validation` and the behave parameter scenario; P07 by `test_release_cli_parameters`; P03 by total 3 (`test_release_settings_validation`, `test_release_cli_parameters`) and behave total 10; C01 by `test_release_timing_and_snapshot_contract` and the behave defaults step; C08 by the `(159, 41)` arm of `test_release_eligibility_boundaries`. |
| S1-S3 | S1 taken (commit-count/interval/items threading pinned; `crf` flag pinned by `test_release_crf_overlap_refused`, C09 killed). S2 taken (the 480 literal is removed and the window is derived). S3 not taken; it is pre-existing and was not assigned. | as above |

## Round-1 findings (R347-1), closed or retained at this head

I read the other reviewer's public report (PR #586 comment 5854920974) only after this report's verdict, findings and ledger were drafted. Nothing in it changed them. Its scripts were taken from the public evidence branch at `68de0cfe` (`review-evidence/396-r1/reviews/R347-1/scripts/`). Their sha256 matches that report's MANIFEST (`mutants.py` `1e8eaec5...`, `audit_probe.py` `add5732a...`), and both were run unchanged on a `git archive` of this head (`receipts/r347_scripts_rerun.log`).

| Round-1 finding | Status | Evidence |
|---|---|---|
| F1 MINOR (citations) | **Closed** | Parts (a), (c) and (d) are as in R346-1 F2 above. For (b), `power.adp-valid-time` now cites 1722.1-2021 6.2.2.5 and 6.2.4/6.2.5, not 6.2.6. The older 6.2.6 attributions at `torture_campaign.py:1456`, `:2769`, `:3096` and `:3104` predate this PR and are untouched by it, as that finding required. Its "new Issue" part is a manager duty (below). |
| F2 MINOR (post-cut origins and bounds) | **Closed** | Recorded decision 5854930205, encoded as in the R346-1 F1 row above. |
| F3 MINOR (one-sided audit controls) | **Closed** | `mutants.py` unchanged: A1, A2, A3, A5 and A6 (and A4, A7) are all killed. `audit_probe.py` unchanged: the head's audit rejects D1-D6. The killing tests are `test_release_counter_omissions_in_every_repeat` (every target in every repeat, both devices, both descriptor kinds), `test_release_binding_omissions_in_every_repeat` (both talkers, AAF-only/CRF-only/all, every repeat) and the 30-row behave outline "each repeat detects omissions on both sides". |
| F4 MINOR (defaults-only pinning) | **Closed** | P1, P2 and P3 are killed (21/21 overall, 0 survivors). The arms are the non-default interval 17 and totals 3 and 10, and the `(199, 1)`, `(159, 41)` and `199`-total eligibility arms. |
| S1 (interval) | Taken | `RELEASE_MAX_SOAK_INTERVAL_S = 60` (`:3323`), with arms 61 and 604800. The probe shows "7-day soak sampled only at the endpoints release_eligible: False". |
| S2 (CRF inside AAF set) | Taken | `_release_pairs` refuses the overlap (`:3459-3462`) on both devices and both roles; `test_release_crf_overlap_refused`; CLI rc 2 (`receipts/eligibility_probe.log`). Mutants O01-O04 are killed. |
| S3 (#366 control) | Taken | `power.single-boot` assertion, the `check_release_boot` oracle, `boot_max_passes=1` and `boot_max_restarts=0`; `test_release_boot_negative_control` and the behave scenario; TESTING.md:960-965 and :988-990. Mutants B01-B03 and B05-B08 are killed; the B04/B09 edges are S4. |

## Lens results and evidence (this round)

| Lens | Result | Evidence |
|---|---|---|
| Conformance | UNCLEAN, R2-F1 | The decision items 1-5 were each checked against REQ-VER-06, TESTING 6d, the plan args and the assertions, and all match, except that eligibility ignores the new bound (R2-F1). All citations are correct (`receipts/standards_citation_check.md`). |
| RTL | CLEAN | `receipts/scope_and_gitlinks.log`: the delta touches only REQUIREMENTS.md, TESTING.md, `tb/tools/torture_campaign.py` and two test files; no `hdl/`, `sw/`, `tools/`, builder or gitlink change, and the gitlinks are identical to dev. The plan's RTL anchor (`AVTPRX_TSD` 0x6EC, STREAM_INPUT[0]) is unchanged from round 1, where it was checked against `milan_csr.sv` and `KL_avtp_rx_monitor_ctx.sv`. |
| Robustness | UNCLEAN, R2-F1 | New validation: `restore_bound_s`/`boot_margin_s` positive int; `topology_explicit` bool; CRF/AAF overlap refused on both devices and both roles (rc 2); the CLI refuses 0, -1 and non-int. The boot oracle SKIPs incomplete or ill-typed observations (`receipts/eligibility_probe.log`, `receipts/planner_mutants_r2.log`). |
| Tests | UNCLEAN, R2-F1 and R2-F2 | Round-1 mutants: 42/44 killed, all required survivors killed. Round-2 mutants: 42/50 killed. The survivors are E10-E13 and E15 (R2-F2), plus R16, B04 and B09 (S4). The omission probe refused 240/240. The self-test runs 47 tests and the plan feature 68 scenarios / 297 steps. |
| Docs | UNCLEAN, R2-F1 | REQ-VER-06 and TESTING 6d state the decision, including the provisional bound and its ratification path, T0, the ADP formula, the additional #75 check and the derived window. Both keep bench items 3 and 4 open and state the #366 control. TESTING.md:958 conflicts with the eligibility behaviour (R2-F1). The docs gates are green. |

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R2-F1 MINOR) | REQUIREMENTS.md:250-305; TESTING.md:841-992; torture_campaign.py:3320-3600; issue #396 comments 5854930205, 5854692245, 5789765788; #75, #397, #70; Milan v1.2 4.2.6.2.4, 5.3.x persistence clauses, 5.3.7.7, 5.3.8.10, 5.5.1.4, 5.5.2.4, 5.5.2.6, 5.6.2-5.6.3, Annex B.1/B.1.1; IEEE 1722-2016 4.4.4.6/4.4.4.7; IEEE 1722.1-2021 6.2.2.5, 6.2.4, 6.2.5 | R346-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| RTL | CLEAN | `receipts/scope_and_gitlinks.log` (delta and full name-status, gitlinks at base and head); REQ/TESTING RTL anchor `AVTPRX_TSD` unchanged since R346-1 | R346-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Robustness | UNCLEAN (R2-F1 MINOR) | `ReleaseSettings.__post_init__` (torture_campaign.py:3342-3360), `_release_pairs` overlap refusal (:3456-3477), `_release_profile_eligible`/`_release_topology_explicit`/`check_release_boot` (:3491-3517), CLI `main` (:5344-5395); `receipts/eligibility_probe.log` | R346-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Tests | UNCLEAN (R2-F1, R2-F2 MINOR) | `_ReleasePlanChecks` (torture_campaign.py:4773-5047); torture_campaign_plan.feature:304-387; torture_release_steps.py; `receipts/planner_mutants.log`, `receipts/planner_mutants_r2.log`, `receipts/plan_omission_probe.log`, `receipts/r347_scripts_rerun.log` | R346-2 | 24d32d549fa7470318a93984403a92423a63fa25 |
| Docs | UNCLEAN (R2-F1 MINOR) | REQUIREMENTS.md section 8; TESTING.md 6d (:841-992); CONTRIBUTING.md:418-428 (unchanged in delta); PR body; TAKEN and REVIEW READY comments; docs gate receipts | R346-2 | 24d32d549fa7470318a93984403a92423a63fa25 |

## Commands run at the exact head (all in the foreground; receipts under `receipts/`)

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 47 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0, 68 scenarios / 297 steps, 0 skipped |
| `cd tests && python3 -B -m behave --tags ~@open-finding -f plain` | rc 0, 14 features / 385 scenarios / 1909 steps |
| `python3 -B scripts/check_feature_status.py --self-test`; `python3 -B scripts/check_feature_status.py` | rc 0; rc 0, 0 findings |
| `scripts/docs_check.py`, `scripts/check_em_dash.py --base ac18b509...`, `scripts/gen_toc.py --check`, `scripts/check_doc_style.py` (disposable virtual environment built from `tools/markdown/requirements.txt` with `--require-hashes`) | rc 0 each (0 findings; em-dash 339/339 arms; TOC OK; style OK) |
| `python3 -B scripts/check_doc_paths.py` (and `--self-test`); `python3 -B scripts/check_py_idiom.py` | rc 0 (850 paths resolve); rc 0 |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | rc 0 |
| `git diff --check ac18b509... 24d32d54`; `git diff --check b7b74b8b 24d32d54` | rc 0; rc 0 |
| `python3 -B scripts/planner_mutants.py <clone> <scratch>` (round-1 script, unchanged, sha256 `d26698bc...`) | 44 mutants: 42 killed, 1 survived (A08, informational), 1 invalid (C13, anchor removed by the decision) |
| `python3 -B scripts/plan_omission_probe.py <clone>` (round-1 script, unchanged, sha256 `e1b0b026...`) | 240 planted omissions over 3 topologies, 0 accepted |
| `python3 -B scripts/planner_mutants_r2.py <clone> <scratch>` (new, round-2 code) | 50 mutants: 42 killed, 8 survived (R2-F2, S4) |
| `python3 -B scripts/eligibility_probe.py <clone>` (new) | 20 CLI cases; R2-F1 rows shown |
| R347-1 `mutants.py <archive>` and `audit_probe.py <archive>` (unchanged, from the public evidence branch) | 21 mutants, 21 killed, 0 survivors; the audit rejects D1-D6; archive bytes restored |

## Real limits

- This is desk review only. No hardware, bench, power strip, Docker, act, or full parent/PP/gPTP/Yosys/builder bank was run. Physical calibration was NOT RUN, and no field skip is taken as hardware proof.
- Standards checks cover only the cited clauses and a full-text search of Milan v1.2 for persistence sentences. The #75 bound and the #397 scope are taken from the issue texts as published.
- Hosted checks were only snapshotted (`receipts/hosted_checks_snapshot.txt`, 10:42Z). At snapshot time `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability` and Yosys shards 0-3/4 had succeeded. `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0-4/5 were in progress. `Physical gPTP (nightly and manual)` was skipped. No conclusion is drawn from in-progress or skipped contexts.
- The provisional 30 s bound and the per-cycle ADP window are decision content. Their physical feasibility (S1) was not measured.
- The clone was never written. After all probes, HEAD, tree, index, the seven changed files' blob hashes and modes, and the four gitlinks were rechecked (`receipts/clone_integrity.log`).

## Pending manager duties

- Hosted and act acceptance of this exact head, and the final current-dev candidate at the merge turn.
- Route R2-F1 and R2-F2 to the executor. R2-F1 may alternatively be settled by an explicit documentation statement, as described in its required outcome.
- R347-1 F1 part (b) asked for a new Issue for the pre-existing 1722.1-2021 6.2.6 attributions (`torture_campaign.py:1456`, `:2769`, `:3096`, `:3104`). No such Issue was found by a title/body search at review time; filing it is the manager's call.
- Ratify `restore_bound_s` from #397 and #75 measurements, as REQ-VER-06 states. Consider S1 when doing so.
- Items 3 and 4 of #396 (the physical campaigns and the negative control) remain open bench work.

R346-2 FINISHED
