[A362]

Refs #396

## Status

Desk acceptance items 1, 2 and 5 are implemented at
`54d9beea2888bd07369e67e5cb025d1405d03495` and await independent re-review.
Bench acceptance items 3 and 4 remain open.

## Description

Define REQ-VER-06: seven continuous days with bidirectional AAF/CRF streams,
plus 200 cold cuts split into 160 idle and 40 journal-commit cuts.
Add parameterized soak and power plans, a declared persisted-item inventory,
and independent per-repeat index, direction and CRF coverage audits.
Both campaigns use one DUT and the reference peer.
The persistence inventory currently contains stream binding.
It expands to all eight items when #70 lands.

Every cycle measures automatic restoration from T0, the power-strip ON command,
to the first valid AVTP PDU of every persisted binding.
The provisional release ceiling is 30 seconds, pending #397/#75 ratification.
After restoration, the additional controller reconnect must resume valid AVTP
strictly below one second after successful `CONNECT_RX`.
The first post-cut advertisement must arrive before T0 plus the captured
`valid_time` in two-second units. Milan 5.6.2 requires `valid_time=10`.
Boot counts against that twenty-second window; off time and pre-cut
advertisement age remain separate provenance.
Continuous UART/reset evidence lasts until the next cut or campaign end.
A repeated BIOS pass fails even if streaming subsequently recovers.

`release_eligible` judges configured prerequisites: explicit complete topology,
stream-binding inventory, sampling at most 60 seconds, restoration at most
30 seconds, and the area's duration or phase/count minimums.
Selecting one area retains the shared profile checks.
The flag does not prove measured results or descriptor provenance.

## Round 4

Implement the [recorded round-4 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855792297).
Each `tu` interval contains at least one recorded discontinuity.
Accepted kinds are PHC settime/adjtime, fabric discontinuity, and GM-identity edge.
Measure from the last recorded discontinuity before `tu` clears.
Clearing must occur within 0.5 seconds plus stated observation resolution.
Uncorrelated `tu` fails.
REQ-VER-06, TESTING 6d, the assertion text and plan arguments agree.

The observation oracle and independent controls exercise a GM change at zero
and a PHC step at 0.2 seconds. With 0.001-second resolution, clearing at
0.62 seconds passes and clearing at 0.8 seconds fails.
An interval without a recorded event fails.
Boundary, event-order and incomplete-evidence controls accompany those cases.

Take the text/test suggestions: pin key `tu` and ADP assertion phrases and the
eight-second CLI off-hold default; identify 0.25 seconds as the project's
minimum interpretation; use wire-capture and correlated event-timestamp
resolution, never the counter-read cadence; and clarify that the minimum
off time is the longer of configured hold and verified discharge.
No new numeric resolution ceiling or universal discharge duration is asserted.

## Reproduction and validation

```sh
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain
python3 -B -m behave tests/features --tags=@torture -f progress
python3 -B tb/tools/torture_release_mutants.py
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/check_feature_status.py
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
python3 -B scripts/gen_toc.py --check
python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json
git diff --check
git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check
git diff 8153576af6d739427b54f6c40299b0e57bc481ae HEAD --check
```

All 17 commands returned 0 at the stated head, in the foreground, from the
physical worktree. Markdown gates used the pinned renderer requirements.
Default plan output remains diagnostic; supply descriptor-derived topology
specifications for both participants before bench execution.

| Validation | Result |
|---|---|
| Planner self-test | 52 tests passed |
| Plan feature | 77 scenarios / 326 steps passed; none skipped |
| Full torture tier | 222 scenarios / 871 steps passed; 172 scenarios excluded by tags |
| Feature-status controls | 46/46 passed; zero findings |
| Documentation, source quality, area coverage and whitespace | Passed |
| Release mutation controls | 19 killed by named tests after a clean baseline |
| Unchanged public scripts | All 32 script files have final rc 0; bytes unchanged |
| Internal mutation suites | Round 1: 42 killed / one informational survivor / one invalid; round 2: 48 killed / two invalid; round 3: 28 killed / three optional or equivalent survivors / three invalid |
| External mutation suites | Round 1: 21/21 killed; round 2: 22/22 killed; round 3: all 23 applicable mutations killed, three old anchors unapplied |
| Omission and ADP probes | Every omission probe rejects 240 omissions; ADP hold probe has zero unexpected results |
| Required cycle transcription | Clearing stays within 0.5 seconds of the last pulse across its sweep |

Public scripts came from
[`396-review-evidence` at 0563bb47](https://github.com/kebag-logic/milan-fpga/tree/0563bb47f92f36c1f37b9a310debe93dd2795a27/review-evidence/396-r1/reviews).
They ran unchanged against the committed head or its disposable export.
The initial external contract probe lacked two documentation files in its
export; supplying those committed files made the unchanged rerun pass.

Invalid or unapplied anchors are never counted as kills. The prior boot and
ADP anchors remain superseded. Round 4 also replaces the old uncertainty
origin, resolution and assertion wording. New repository controls kill the
corresponding mutations at their current anchors. The external uncorrelated
uncertainty, ADP-text and CLI-default mutations now fail named self-tests.
Internal optional survivors are the equivalent hardcoded eight-second default,
an alternative ADP prose mutation, and a redundant step-oracle removal.
The older generic-audit informational survivor remains reported separately.
Historical prose in the unchanged cycle transcription and hardcoded round-2
ADP probe arithmetic are not verdicts on the corrected contract.

## Open acceptance

- [x] Desk decisions, normative requirements and parameterized release plans.
- [x] Every repeat covers every stream index, both directions and CRF.
- [x] Assigned repository gates and new negative controls.
- [ ] Shipping-image soak and cold-cycle campaigns with retained evidence.
- [ ] Physical known-defect negative control and resulting findings.
- [ ] Manager ratification of the provisional restoration ceiling.
- [ ] Independent re-review of this head and required merge evidence.

The bench executor supplies power-strip and journal-window instrumentation.
No physical release result is claimed. Desk evidence does not discharge #70,
#117 or acceptance items 3 and 4.
