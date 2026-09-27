# [A356] Issue #396 handoff

Status: desk assignment complete and committed locally; ready for independent review.

Repository: https://github.com/kebag-logic/milan-fpga.git
Worktree: `$LANES/396-release-gates`
Branch: `396-release-gates`
Base: `ac18b50968b12efe4d15c0a06301264b35656b31`
Head: `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`
Commit subject: `Define soak and cold power-cycle release plans for #396`
Executor: [A356]. Internal reviewer: [R346]. External reviewer: [R347].

Assignment: https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854692245
Takeover: https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854721905
Review-ready evidence: issue #396; local body `REVIEW-READY.md`.

## Scope and authority

The remote and initial full HEAD matched the assignment.
The issue body and every comment were read before implementation.
The issue is In progress, with both reviewers publicly assigned.
Desk acceptance items 1, 2 and 5 are implemented.
Items 3 and 4 remain open for later bench work.

Context included AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md,
docs/development/CODE_QUALITY.md, and docs/testing/TESTING.md.
Cited context included README.md, the existing planner and plan feature,
tests/README.md, docs/integration/BUILDING.md,
docs/reference/MILAN_COMPLIANCE_MATRIX.md, scripts/baremetal_uart_smoke.py,
docs/testing/methodology.md, and docs/reference/FR_NFR.md.
Issue #75 supplied the CONNECT_RX-to-first-valid-AVTP timing bound.
The register map supplied AVTPRX_TSD's single-index measurement boundary.

## Change list

| File:line | Change |
|---|---|
| `REQUIREMENTS.md:250` | REQ-VER-06 defines both release campaigns and acceptance criteria |
| `REQUIREMENTS.md:280` | Release blocker text ties REQ-VER-05 to campaign evidence |
| `CONTRIBUTING.md:418` | Release duty, cut mix, artifacts, and evidence links |
| `docs/testing/TESTING.md:841` | Commands, repeat-operation contract, observations, and open bench work |
| `tb/tools/torture_campaign.py:3322` | Validated duration, interval, count, mix, and persistence settings |
| `tb/tools/torture_campaign.py:3354` | Clause-backed soak and power assertions |
| `tb/tools/torture_campaign.py:3455` | Continuous soak operation with periodic and endpoint observations |
| `tb/tools/torture_campaign.py:3478` | Serial idle and journal-commit cold-cut repeat groups |
| `tb/tools/torture_campaign.py:3515` | Independent observation and direction/CRF coverage audits |
| `tb/tools/torture_campaign.py:3722` | Per-repeat coverage prevents one power phase masking another |
| `tb/tools/torture_campaign.py:4683` | Default, sparse-topology, negative-control, and CLI tests |
| `tb/tools/torture_campaign.py:5120` | Parameterized CLI and visible repeat arguments |
| `tests/features/torture_campaign_plan.feature:304` | Nine additional release coverage/decision scenarios |
| `tests/steps/torture_release_steps.py:27` | Independent release feature steps and planted omissions |
| `tests/steps/torture_plan_steps.py:862` | Default-area wording follows configured inventory |

## Acceptance results

| Item | Result | Evidence |
|---|---|---|
| 1: decisions and normative MUST gate | Met | REQ-VER-06; CONTRIBUTING; blocker cross-reference |
| 2: soak/power plans and coverage | Met | 41 planner tests; 36 feature scenarios; release-coverage.json |
| 5: authoritative documentation and gates | Met | All final gate exits are 0 below |
| 3: shipping-image physical campaigns | Open | No physical campaign was run |
| 4: physical known-defect negative control | Open | Desk omission controls do not satisfy this item |

## Plan results

| Property | Result |
|---|---|
| Default soak | 604800 continuous seconds; 60-second interval; baseline and final sample |
| Default power mix | 200 cold cuts: 160 idle, 40 journal-commit; warm resets excluded |
| Persisted state | Configurable nonempty unique inventory; default stream_binding |
| Counter observations | Every declared input/output on both endpoints, including CRF |
| Bindings | Compatible AAF and CRF in both directions; one source per listener |
| Unequal shapes | Sources multicast where needed; unbound outputs still observed |
| Sparse topology | Explicit nonzero, noncontiguous indices preserved and audited |
| Diagnostics | Shorter valid profiles emit release_eligible false |
| Restart timing | Less than one second after CONNECT_RX success, per #75 |
| Cold boot | Separate observation window of at least 480 seconds |
| Missing bench support | Unmet evidence; unsupported operations must refuse |

## Negative-control results

`test_release_coverage_mutations` keeps a complete matrix in every case.
The damaged release repeat still fails its own audit.
For power, the other phase remains complete too.

| Planted omission | Soak | Power |
|---|---|---|
| One nonzero input counter index | Rejected | Rejected |
| Return direction bindings | Rejected | Rejected |
| CRF sink observation, with binding retained | Rejected | Rejected |
| CRF binding, with counter observations retained | Rejected | Rejected |
| Entire release area | Rejected | Rejected |
| Journal-commit phase | Not applicable | Rejected |

The feature tier independently exercises the first three omissions per area.
Settings tests reject zero/negative values, invalid interval/count sums,
boolean/nonfinite inputs, and empty/duplicate persisted inventories.
The real CLI threads every setting into JSON and rejects inconsistent counts.

## Gate table

All final gates below ran on `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`.
Working directory: `$LANES/396-release-gates`.
Every gate ran in the foreground with a 600-second timeout.
No gate output was piped. Logs were redirected directly to regular files.
The existing Markdown interpreter supplied the pinned rendering dependencies.
`gate-results.json` retains commands, exits, durations, and log names.

| Exact command | Exit | Result | Evidence |
|---|---:|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 41 tests passed | `planner-self-test.log` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 1 feature; 36 scenarios; 172 steps passed; no skips | `behave-plan.log` |
| `python3 -B scripts/check_feature_status.py --self-test` | 0 | 46/46 controls; zero findings | `feature-status.log` |
| `python3 -B scripts/docs_check.py` | 0 | Zero findings; scrub controls 23/23; routing controls 4/4 | `docs-check.log` |
| `python3 -B scripts/check_doc_paths.py` | 0 | 850 cited paths resolve | `doc-paths.log` |
| `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | Zero findings; 339/339 controls; base-to-head diff | `em-dash.log` |
| `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python -B scripts/gen_toc.py --check` | 0 | 111 annotated pages checked | `contents.log` |
| `python3 -B scripts/check_doc_style.py` | 0 | 22 current documents checked | `doc-style.log` |
| `python3 -B scripts/check_py_idiom.py` | 0 | All ratchets satisfied; no budget changes | `python-idiom.log` |
| `git diff --check` | 0 | Clean worktree diff | `diff-check.log` |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | 0 | Complete base-to-head change passes | `commit-diff-check.log` |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | Both release areas complete; no missing indices | `release-coverage.json` |

An earlier supplemental source-quality run returned 1.
The added steps had crossed the existing module-size ratchet.
Moving those new steps into their own focused module resolved it.
`python-idiom-initial.log` retains that diagnostic; the final run returned 0.
No test, acceptance criterion, or ratchet was weakened.

## Review and bench limits

The repeat operations are plan data; the bench executor supplies execution.
Unsupported operations must not be silently skipped.
Periodic healthy samples cannot prove uninterrupted gPTP health.
The plan therefore also requires continuous transition and uncertainty evidence.
AVTPRX_TSD measures the last accepted STREAM_INPUT[0] packet only.
Its observations do not establish margins for other streams.

The plan's generic campaign exit code is not release approval.
Each required release assertion needs a measured PASS on the exact image.
Missing records and non-PASS evidence cannot qualify the release.
Update the persisted-item inventory when #70 lands its full contract.
Retain cut-phase instrumentation, state snapshots, image hashes, UART,
wire captures, controller logs, verdicts, and the temperature log.
Link dated physical evidence from docs/findings/ and file every failure.

No push, PR operation, merge, hardware access, or submodule edit occurred.
No firmware, RTL, or sw/builder file changed.
The working tree is clean and the seven changed files are in the local commit.
The three required verification submodules remain at their original pins.
The optional external submodule remains uninitialized and was not touched.
No implementation blocker or unresolved design choice remains in the desk scope.
Independent reviews and later bench acceptance remain outstanding.
