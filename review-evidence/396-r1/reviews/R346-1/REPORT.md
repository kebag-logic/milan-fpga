[R346] NEGATIVE - exact head b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3

# R346-1 internal independent review: issue #396 / PR #586 (desk lane)

- Head: `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`, tree `1b8951188447bddf54204e146796b6775e4bf72a`; one commit on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope reviewed: desk acceptance items 1, 2 and 5 of #396, under the decisions in issue comment 5854692245 and the owner decision in 5789765788. Bench items 3 and 4 are not claimed by the PR and are not judged here.
- Reconstruction order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and decisions, REQUIREMENTS.md section 8, TESTING.md 6/6b/6d, issue #75 (the bound), issue #366, the cited Milan v1.2 / IEEE 1722-2016 / IEEE 1722.1-2021 pages, then the diff, then the published evidence at `4949b127:review-evidence/396-r1`.
- Prior public review findings on PR #586: none existed when this round started (no PR reviews, no review comments, and only the two review-start notices among the conversation comments). Nothing to resolve or retain.

## Verdict basis

The head meets most of the desk contract. The soak and power areas are emitted from configuration. Duration, interval, cycle count, phase mix and the persisted-item list are all CLI parameters, and the head threads them correctly into the JSON (`receipts/parameter_threading.log`). The per-area audit refused all 240 omissions I planted: every single counter target, each direction, AAF-only and CRF-only removal per direction, re-attributed targets, dropped repeats and a missing phase, over three topologies, in every repeat including `power.journal_commit` (`receipts/plan_omission_probe.log`). The declared gates and the full offline behave gate pass. There is no RTL, firmware, builder or gitlink change.

One MAJOR and three MINOR findings remain open, so the verdict is NEGATIVE. The decided post-power-cycle rebind criterion was replaced by a different measurement (F1). The cited clauses are wrong or missing in places (F2). Release eligibility accepts profiles that the documentation says it refuses (F3). Several audit and threading arms have no test that can fail (F4).

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - the automatic rebind after each cold cut has no time bound

- Artifacts: `REQUIREMENTS.md:269-271`; `docs/testing/TESTING.md:901-910`; `tb/tools/torture_campaign.py:3399-3403` (`power.rebind-bound`) and `:3496-3498` (`rebind_limit_s=1`, `rebind_start="CONNECT_RX success"`); `tb/tools/torture_campaign.py:4702-4703` and `tests/steps/torture_release_steps.py` (they pin only that interval).
- Authority and evidence: the decision (issue comment 5854692245) says every cycle "rebinds within #75's bound". After a cold cut the rebind is Milan Auto Connect (v1.2 5.5.1.4, pp.65-66; 5.5.2.6, p.69). The listener waits for the talker's ENTITY_AVAILABLE and sends PROBE_TX_COMMAND, with no controller and no `CONNECT_RX`. The head instead has two parts:
  - It requires automatic restoration with no deadline other than the 480 s boot observation.
  - It moves #75's one-second bound onto a separate, controller-driven `CONNECT_RX` reconnect that runs after the restore ("verify automatic restore before any controller-assisted reconnect test"; "Measure reconnect from `CONNECT_RX` success to first valid AVTP").

  The assertion cites the Auto Connect clauses but measures the Controller Bind path (5.5.2.4). This interpretation is not flagged as a deviation in the issue or the PR (AGENTS.md section 2: publish the conflict and mark it as needing a decision).
- Impact: a candidate can take minutes after every cold boot to resume either direction's stream automatically. That is the #75 / #366 defect class on exactly the path the power torture exists for. It still passes all 200 cycles as long as streaming resumes inside the boot window and a later manual `CONNECT_RX` restarts in under a second. The gate cannot fail on the behaviour the decision bounds.
- Required outcome: either
  - bound the automatic post-cycle rebind with defined start and end events that a bench can timestamp, in both directions, consistently in REQ-VER-06, TESTING.md 6d, the `power` step args and assertions, and the tests. For example, the first post-boot ENTITY_AVAILABLE of the relevant talker (or the listener's first PROBE_TX_COMMAND) to the first valid AVTP PDU, under #75's one second. Or
  - obtain a recorded manager or owner decision on #396 that the controller-driven `CONNECT_RX` interval is the intended reading, and cite it.

  In either case, define "network readiness", the start event of the ADP criterion (`REQUIREMENTS.md:268`, `TESTING.md:907`), so that criterion is also decidable.
- Verification: re-read the three artifacts for one consistent criterion. A self-test or behave check must fail if the automatic-path bound (or the cited decision) is removed from the emitted `power` steps.

### F2 - MINOR - Conformance, Docs - standards citations are missing or mis-attached

- Artifacts: `REQUIREMENTS.md:250-275`; `tb/tools/torture_campaign.py:3370-3378`, `:3391-3398`; receipt `receipts/standards_citation_check.md`.
- Authority and evidence (clause text checked against the cited pages):
  - (a) The REQ-VER-06 row cites no standard. Its counter, `tu`/holdover, ADP valid-time, auto-restore and persistence criteria have no Milan or IEEE anchor, and the review brief requires the row to carry correct citations.
  - (b) `soak.tu-within-holdover` cites IEEE 1722-2016 4.4.4.6, which is the `sequence_num` field. 4.4.4.7 is `tu`, and 4.4.4.6 belongs with the `SEQ_NUM_MISMATCH` assertion.
  - (c) `soak.gptp-continuity` cites Milan 4.2.6.2.2/4.2.6.2.3 (Tables 4.1/4.2, the interval and timeout tolerances) as the proof of "no asCapable loss". asCapable is 4.2.6.2.4 (802.1AS 10.2.4.1), and no assertion measures the Table 4.1/4.2 tolerances.
  - (d) `power.state-restored` cites 5.3.5.1/5.3.7.1/5.3.8.7/5.3.11.1/5.3.13 but not 5.3.8.2/5.3.8.3 (p.34). Those are the persistence clauses for the stream binding, the only item in today's inventory.
  - (e) `power.adp-valid-time` cites 1722.1-2021 6.2.6, the Discovery state machine. `valid_time` is 6.2.2.5, and the advertiser's obligation is in 6.2.4/6.2.5.
- Impact: a cold reviewer or bench grader following the citations checks the wrong clause. The one criterion enforced today (binding restore) has no normative anchor.
- Required outcome: the row and each release assertion cite the clause that actually states the criterion. The row at least anchors Tables 5.4/5.6, Annex B.1.1, ADP `valid_time`, Auto Connect and the binding-persistence clauses.
- Verification: compare each citation against the standard page.

### F3 - MINOR - Conformance, Robustness, Docs - `release_eligible: true` for profiles the contract says cannot qualify

- Artifacts: `tb/tools/torture_campaign.py:3461-3462`, `:3489-3491`; `docs/testing/TESTING.md:863-870`; receipt `receipts/parameter_threading.log`.
- Evidence: the flag is true in three cases the contract says cannot qualify:
  - `--soak-interval-s 604800` (only a baseline and an endpoint walk, while REQ-VER-06 requires "periodic counter observations").
  - `--persisted-items clock_source` (an inventory without the stream binding, while `REQUIREMENTS.md:264` says the list currently contains it).
  - The default built-in desk-fixture topology (`TESTING.md:864`: "desk fixtures, not discovered hardware").

  TESTING.md:869 states "Reduced profiles remain diagnostic and emit `release_eligible: false`".
- Impact: the plan's own eligibility claim can be true for a plan that cannot satisfy REQ-VER-06. That makes it a misleading qualification input for the bench runner.
- Required outcome: either the flag also refuses these cases (an interval bound, the binding in the inventory, an explicit topology) or the documentation states exactly what the flag does and does not judge.
- Verification: CLI probes as in `receipts/parameter_threading.log`, plus a self-test arm for each refused case.

### F4 - MINOR - Tests - several audit and threading arms have no test that can fail

- Artifacts: `tb/tools/torture_campaign.py:4722-4754` (`test_release_coverage_mutations` plants every omission in the first repeat only, `:4731`), `:4785`, `:4807` (interval 60 = default); `tests/steps/torture_release_steps.py:72-86`; receipt `receipts/planner_mutants.log`.
- Evidence: of 44 source mutants graded by the head's own `--self-test` plus the plan feature, 9 survive:
  - A05: the audit checks only the first repeat of an area. The `power.journal_commit` repeat's audit is untested, although the REVIEW READY comment claims per-repeat audits and negative controls.
  - A04: the AAF-binding-per-direction check is removed. Tests only drop whole directions, which the CRF arm also catches.
  - P01 and P07: the soak interval is hardcoded or ignored by the CLI. Every test uses the default 60.
  - P03: `total_cycles` is hardcoded to 200.
  - C01: the idle and commit snapshot policies are swapped, so an idle cut would accept "old or new".
  - C08: power eligibility ignores the commit count.
  - C09 (the `crf` flag on counter targets) and A08 (a false-red-only change) are informational.

  My plan-level and CLI probes show the head behaves correctly on all of these, so this is test strength, not a product defect.
- Impact: a later edit can silently break the journal-commit repeat's coverage, the interval parameter or the idle-cut restore policy with every gate green.
- Required outcome: each listed arm has a negative control that fails when the arm is broken. That includes an omission planted in a non-first repeat, an AAF-only direction removal, a non-default interval and total, per-phase snapshot policy, and commit-count eligibility.
- Verification: rerun `scripts/planner_mutants.py`. A04, A05, P01, P03, P07, C01 and C08 must be killed.

### Suggestions (non-blocking; do not affect coverage)

- S1 - Docs/Tests: the release assertion texts embed 604800 / 200 / 160 / 40 even when a diagnostic profile emits other values, and the counter-target `crf` flag is untested. Consider rendering the texts from the settings.
- S2 - Docs: `boot_observation_s=480` equals the physical family's 360 s network plus 120 s gPTP budgets (`torture_campaign.py:3232`) but is uncited and fixed. Cite that source, or derive it from those budgets.
- S3 - Robustness (pre-existing, outside this diff): a malformed `--dut` value (for example `crf_in=`) exits with a traceback (rc 1) rather than an argparse error, because `parse_device_spec` runs outside the new `try`. Worth a separate issue.

## Lens results and evidence

| Lens | Result | Evidence |
|---|---|---|
| Conformance | findings F1, F2, F3 | REQ-VER-06 row checked clause by clause against comment 5854692245. Duration, bidirectional + CRF, 200 cold cuts (160 idle / 40 commit, no resets), zero SEQ_NUM_MISMATCH/STREAM_INTERRUPTED, explained MEDIA_UNLOCKED, no asCapable loss, `tu` within holdover, persisted items as data, ADP valid time, one DUT + reference peer, and the REQ-VER-05 reference (`REQUIREMENTS.md:280`) all match. The rebind criterion (F1) and citations (F2) do not. `--plan` emits both areas with the Table 5.6 counter walk of every index plus the CRF sink, gPTP publication fields, `AVTPRX_TSD` (0x6EC, STREAM_INPUT[0]) and uptime. |
| RTL | PASS | `receipts/scope_and_gitlinks.log`: the diff touches only CONTRIBUTING.md, REQUIREMENTS.md, TESTING.md, `tb/tools/torture_campaign.py` and three test files; no `hdl/`, `sw/`, builder or gitlink change. The plan's RTL claims were checked against RTL: `AVTPRX_TSD` at `hdl/common/csr/milan_csr.sv:763/2361`, sourced from `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:219` ("stream-0 last signed ts_delta"), matching `REGISTER_MAP.md:1251` and the plan's single-index restriction. |
| Robustness | findings F1, F3 | `ReleaseSettings` validation (non-positive, bool, NaN, sum mismatch, interval > duration, empty/duplicate/whitespace items) and CLI refusal with exit 2 (`receipts/cli_boundary_probes.log`); distinct-DUT and missing-CRF refusal; sparse and wide topologies (`receipts/plan_omission_probe.log`). |
| Tests | findings F1, F4 | `receipts/planner_mutants.log` (44 mutants, 35 killed); the new scenarios and self-test arms read against the audit code. |
| Docs | findings F1, F2, F3 | REQUIREMENTS.md section 8, CONTRIBUTING.md section 3 bullet (gate, 160/40 mix, artifacts, desk gates do not discharge), TESTING.md 6d (plan commands, evidence table, retained artifacts, items 3/4 open, no hardware claim). Docs gates are green. |

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | REQUIREMENTS.md:250-281; torture_campaign.py:3320-3544; issue #396 decisions; issue #75; Milan v1.2 pp.16, 29-39, 65-69, 134; IEEE 1722-2016 4.4.4.6-7; IEEE 1722.1-2021 6.2.2.5, 6.2.4-6.2.6 | R346-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| RTL | CLEAN | full diff name-status and gitlinks; milan_csr.sv:307/763/2361; KL_avtp_rx_monitor_ctx.sv:219; milan_datapath.sv:5817; REGISTER_MAP.md:1251 | R346-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Robustness | UNCLEAN (F1 MAJOR, F3 MINOR) | ReleaseSettings and CLI paths; `_release_pairs`/`_release_coverage`; boundary and topology probes | R346-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Tests | UNCLEAN (F1 MAJOR, F4 MINOR) | `_ReleasePlanChecks` (torture_campaign.py:4683-4823); torture_campaign_plan.feature:304-340; torture_release_steps.py; source mutants; plan omission probe | R346-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | REQUIREMENTS.md section 8; CONTRIBUTING.md:418-428; TESTING.md:841-935; PR body; REVIEW READY comment | R346-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |

## Commands run at the exact head (all in the foreground; receipts under `receipts/`)

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 41 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0, 36 scenarios / 172 steps, 0 skipped |
| `cd tests && python3 -B -m behave --tags @torture -f plain` | rc 0, 181 passed, 172 skipped by tag |
| `cd tests && python3 -B -m behave --tags ~@open-finding -f plain` | rc 0, 14 features / 353 scenarios / 1784 steps |
| `python3 -B scripts/check_feature_status.py --self-test`; `python3 -B scripts/check_feature_status.py` | rc 0; rc 0, 0 findings |
| `python3 -B scripts/docs_check.py`; `python3 -B scripts/check_doc_paths.py` (and `--self-test`) | rc 0 (0 findings; 850 paths resolve) |
| `python3 -B scripts/check_doc_style.py`; `python3 -B scripts/check_py_idiom.py` | rc 0 |
| `python3 -B scripts/gen_toc.py --check`; `python3 -B scripts/check_em_dash.py --base ac18b509...` | rc 2 with the system interpreter (pinned renderer absent); rc 0 in a disposable virtual environment built from `tools/markdown/requirements.txt` (TOC OK; em-dash 0 findings, 339/339 arms) |
| `git diff --check ac18b509... HEAD` | rc 0 |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | rc 0 |
| `python3 -B scripts/plan_omission_probe.py <clone>` | rc 0, 240 planted omissions, 0 accepted |
| `python3 -B scripts/planner_mutants.py <clone> <scratch>` | 44 mutants, 35 killed, 9 survived (F4) |

The published author evidence (`4949b127:review-evidence/396-r1/author/`) agrees with these counts. Its `gate-results.json`, `planner-self-test.log`, `behave-plan.log` and `feature-status.log` hashes match that tree's MANIFEST.json.

## Real limits

- This is desk review only. No hardware, bench, power strip, Docker, act, or full parent/PP/gPTP/Yosys/builder bank was run. Physical calibration was NOT RUN, and no field skip is taken as hardware proof.
- Standards checks read only the cited pages. The #75 bound is taken from the issue text as published.
- Hosted checks were only snapshotted (`receipts/hosted_checks_snapshot.txt`). At snapshot time `rtl-fast`, `bdd-conformance`, `full-ci-gate`, `yosys-elaboration`, the Yosys shards 0-3/4 and Verilator shard 3/5 had succeeded. `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were in progress. `Physical gPTP (nightly and manual)` was skipped. No conclusion is drawn from the in-progress or skipped contexts.
- The clone was never written. After all probes, HEAD, tree, index modes and blobs, the seven changed files' blob hashes and the four gitlinks were rechecked (`receipts/clone_integrity.log`).

## Pending manager duties

- Hosted and act acceptance of this exact head, and the final current-dev candidate at the merge turn.
- Routing F1-F4 to the executor. F1 may alternatively be settled by a recorded decision on #396.
- Items 3 and 4 of #396 (the physical campaigns and the negative control) remain open bench work. This PR correctly says `Refs #396`, not `Closes`.

R346-1 FINISHED
