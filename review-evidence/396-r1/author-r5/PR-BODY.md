[A364]

Refs #396

## Status

Desk acceptance items 1, 2 and 5 are implemented at
`07f72ad640f99c43bc1354642ad4d7ed8ba410cc` and await independent re-review.
Bench acceptance items 3 and 4 remain open.

## Description

REQ-VER-06 requires seven continuous days with bidirectional AAF/CRF streams
and 200 cold cuts: 160 idle and 40 during journal commits.
The planner emits parameterized soak and power repeat contracts.
Every repeat observes all declared stream indices, both directions and CRF.
Independent omission controls prevent another repeat from masking missing coverage.
Use one DUT and the reference peer with descriptor-derived topology.
The persisted inventory currently contains stream binding and expands when #70 lands.

Automatic restoration runs from T0, the power-strip ON command, to the first
valid AVTP PDU of every persisted binding. The provisional release ceiling
is 30 seconds, pending manager ratification from #397/#75 measurements.
A subsequent controller reconnect must resume AVTP strictly below one second.
The first post-cut advertisement must arrive before T0 plus captured valid_time
in two-second units. Milan 5.6.2 requires valid_time=10, giving twenty seconds.
Power-off hold and pre-cut advertisement age remain separate provenance.
Continuous UART/reset evidence extends until the next cut or campaign end;
a repeated BIOS pass fails even if streaming subsequently recovers.

The release_eligible flag checks configured prerequisites, including explicit
complete topology, stream-binding inventory, sampling at most 60 seconds,
restoration at most 30 seconds, and each area's duration or cut-count minimums.
It cannot prove descriptor provenance, measured behavior or completed evidence.

## Round 5

Apply the [round-5 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5856062292)
to the start-edge finding in the [external round-4 review](https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5856058686).
The oracle contains events in `[observed_start - observation_resolution_s, clear)`.
The inclusive start allowance accounts for launch-to-capture latency and
event-to-capture correlation error. The clear edge stays exclusive.
Measure the clearing deadline from the last contained discontinuity:
0.5 seconds plus the same recorded observation resolution.
Accepted events remain PHC settime/adjtime, fabric discontinuity and GM-identity edge.
Complete intervals without an accepted event fail; incomplete evidence cannot pass.

REQ-VER-06, TESTING 6d, assertion text and the emitted event-window argument agree.
Independent self-test and feature examples cover half-resolution lag, twice-resolution
lag, exact observed start, zero resolution, the inclusive tolerance boundary,
just outside it, the original -0.1-second case and events at/after clear.
The earlier chained-event, late-clear and missing-evidence controls remain active.

The text/test suggestion about uncertainty preceding its first event is explicit:
the recorded rule adds no separate bound to that preceding duration.
An interval from zero through 10.4 seconds with one event at 10 seconds satisfies
this uncertainty check; the other soak assertions still apply independently.
The issue notification follows the requested minimal head-only format.
This replacement body carries the change, validation, acceptance and open risks.

## Reproduction and validation

Run from the physical candidate worktree. Install the pinned Markdown
requirements before the renderer checks. Every command below returned zero
at the stated head, in the foreground, with no gate piped:

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
git diff 54d9beea2888bd07369e67e5cb025d1405d03495 HEAD --check
```

| Gate | Result |
|---|---|
| Planner self-test | 54 tests passed |
| Plan feature | 86 scenarios / 353 steps passed; no skips |
| Full torture tier | 231 scenarios / 898 steps passed; 172 scenarios excluded by tags |
| Repository mutation controls | 25 mutations killed by named behavioral failures |
| Feature-status controls | 46/46 passed; zero findings |
| Documentation and source quality | Zero findings; no ratchet changes |
| Documentation paths and renderer | 850 paths resolve; 339/339 punctuation controls; contents check passes |
| Area coverage and plan output | Both areas complete; three diagnostic repeat contracts |
| Four whitespace checks | Pass |

Default topology remains diagnostic. Provide descriptor-derived topology for
both participants before bench execution.

The unchanged external round-4 scripts report 16 kills, zero survivors and
zero invalid anchors. T02 is killed by both the self-test and feature suite.
Part B of the oracle probe returns PASS for all six wire lags within resolution;
Part A and the unchanged cycle model also pass.
I01 now applies a second start allowance after the implemented allowance,
so its kill proves that doubled tolerance is refused.

All 35 public script files ran unchanged against the committed candidate or
its disposable export, including duplicate prior-round copies. Every command
returned zero and every nested gate returned zero. Final byte comparisons
match the public blobs at
[`396-review-evidence` e3df1b33](https://github.com/kebag-logic/milan-fpga/tree/e3df1b3364391368ed05d84b44b653e46d51a62e/review-evidence/396-r1/reviews).

| Public suite | Result |
|---|---|
| Internal round 1 | 42 killed; one informational survivor; one invalid anchor |
| Internal round 2 | 48 killed; zero survivors; two invalid anchors |
| Internal round 3 | 28 killed; three optional/equivalent survivors; three invalid anchors |
| External round 1 | 21/21 killed |
| External round 2 | 22/22 killed |
| External round 3 | 23 applicable mutations killed; three superseded anchors unapplied |
| External round 4 | 16/16 killed; zero survivors or invalid anchors |
| Omission/audit probes | All 240 omissions and all six audit defects rejected by every copy |

Invalid or unapplied anchors are never counted as kills. Historical exceptions
remain the generic-audit informational survivor, equivalent hardcoded default,
alternative ADP prose and redundant feature-oracle removal. Superseded boot,
ADP and uncertainty anchors have current repository controls. The external
round-3 script's three reported survivors are its unapplied anchors.
Old probe prose and hardcoded ADP arithmetic do not judge the corrected T0 rule.

## Open acceptance

- [x] Desk decisions, normative requirements and parameterized release plans.
- [x] Every repeat covers every stream index, both directions and CRF.
- [x] Start-edge allowance and independent boundary controls.
- [x] Assigned gates and all unchanged public-script reruns.
- [ ] Independent re-review of this exact head.
- [ ] Shipping-image soak and cold-cycle campaigns with retained evidence.
- [ ] Physical known-defect negative control and resulting findings.
- [ ] Ratification of the provisional restoration ceiling.
- [ ] Required publication, exact-head checks and merge evidence.

The bench executor supplies power-strip and journal-window instrumentation.
Desk evidence does not discharge #70, #117 or physical acceptance items 3 and 4.
