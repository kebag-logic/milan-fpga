[A361]

Refs #396

## Status

Desk acceptance items 1, 2 and 5 are ready for independent re-review at
`8153576af6d739427b54f6c40299b0e57bc481ae`. Bench acceptance items 3 and 4 remain open.

## Description

Define REQ-VER-06: seven continuous days with bidirectional AAF/CRF streams,
plus 200 cold cuts split into 160 idle and 40 journal-commit cuts.
Add parameterized soak and power plans, a declared persisted-item inventory,
and independent per-repeat index, direction and CRF coverage audits.
Document the required exact-image evidence and physical release acceptance.
Today the inventory contains stream binding; it expands to all eight items
when #70 lands. Both campaigns use one DUT and the reference peer.

## Round 3

Implement the [recorded round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855515133):

- `RELEASE_RESTORE_BOUND_S = 30` is the single provisional eligibility ceiling.
  Bounds above it are diagnostic; tighter bounds can remain eligible.
  Boundary controls cover 29, 30, 31 and 3600 seconds, and a mutation removing
  the eligibility check fails the named behavioral test.
- Each `tu` interval must begin with a recorded GM change or timing discontinuity
  and clear within 0.5 seconds of that event plus the recorded observation
  resolution. Uncorrelated uncertainty fails. The requirement, evidence table,
  assertion and plan parameters agree. Five-second media-clock holdover is a
  separate quantity.
- The corrected ADP rule supersedes the round-2 pre-cut-expiry rule.
  T0 is the power-strip ON command on the host monotonic clock. The first
  post-cut `ENTITY_AVAILABLE` must arrive before T0 plus the captured
  `valid_time` in two-second units. Milan 5.6.2 requires `valid_time=10`, hence
  twenty seconds. Missing capture, invalid field values or expiry fails.
  Boot counts against the window; pre-cut advertisement age and the power-off
  hold are recorded provenance and do not reduce it.
- Add `power_off_hold_s`, default eight seconds from the existing physical
  power-cycle contract, and `--power-off-hold-s`. Record actual OFF/ON timestamps,
  hold for at least the configured duration and verify discharge. Non-default
  API and CLI controls pin its propagation.
- Negative CLI controls independently omit CRF keys and listener shape on
  either device. The self-test also checks every required key, empty values,
  mixed count/index-set forms and the documented canonical `entity` key.

Take the text and test suggestions: cite Milan 5.6.2 alongside the advertiser
clause; explain the shared release-profile prerequisites; document the
`entity_id` alias limitation; pin automatic restoration of both directions and
CRF; and cover boolean and negative restart counts. Require continuous
UART/reset evidence until the next cut or campaign end, including the
post-cycle counter walk, for at least `restore_bound_s + boot_margin_s`.
A restart after that minimum window still fails.

Automatic restoration remains bounded from T0 to the first valid AVTP PDU of
each persisted binding, including both directions and CRF. The manager ratifies
the provisional ceiling from #397 and #75 measurements. After restoration,
the additional controller reconnect must produce valid AVTP strictly below
one second after `CONNECT_RX` success. The observation margin extends no
passing deadline.

`release_eligible` judges configured prerequisites only: explicit complete
topology, stream-binding inventory, sampling interval at most 60 seconds,
restoration bound at most 30 seconds, and the area's duration or phase/count
minimums. Selecting one area retains the common release-profile checks.
The flag does not prove measured results, descriptor provenance or ratification.

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
```

All commands returned 0 at the stated head, from the physical worktree path.
The two Markdown parser gates used the pinned requirements in
`tools/markdown/requirements.txt`. Default plan output is diagnostic; supply
both candidate-specific topology specifications from served descriptors for
bench planning.

| Validation | Result |
|---|---|
| Planner self-test | 49 tests passed |
| Plan feature | 76 scenarios / 321 steps passed; none skipped |
| Full torture tier | 221 scenarios / 866 steps passed; 172 scenarios excluded by tags |
| Feature-status controls | 46/46 passed; zero findings |
| Documentation, source quality, area coverage and whitespace | Passed |
| New round-3 mutation controls | Nine killed by named behavioral tests; pristine baseline passed |
| Unchanged internal round-1 mutation script | 42 killed, one informational survivor, one invalid anchor |
| Unchanged internal round-2 mutation script | 48 killed, zero survivors, two invalid anchors |
| Unchanged external mutation scripts | Round 1: 21/21 killed; round 2: 22/22 killed |
| Unchanged omission probes | Each refused all 240 omissions across three topologies |
| Unchanged audit probes | The real audit rejects all six planted defects |

Both rounds' public scripts, including probes, attribution scripts and the
gate runner, were run byte-for-byte unchanged from
[`396-review-evidence` at c8ba14ef](https://github.com/kebag-logic/milan-fpga/tree/c8ba14ef462854d6338d131a17128b1916066344/review-evidence/396-r1/reviews).
All script commands returned 0. The required internal E10-E13/E15 and external
R11/R12 topology mutants are killed, as are internal R16/B04/B09.

The prior A08 survivor remains the informational false-red-only control.
The old C13 anchor refers to the removed 480-second boot literal. Internal
round-2 R13/R19 refer to superseded ADP strings. None is counted as killed.
The new controls independently reject reinstating the pre-cut ADP formula and
skipping missing ADP evidence. The external probe's final arithmetic rows
hardcode the superseded formula; they do not evaluate the current plan's ADP
expression and are not evidence against the corrected T0 rule.

## Open acceptance

- [x] Desk decisions, normative requirements and release plans.
- [x] Every repeat covers every stream index, both directions and CRF.
- [x] Assigned gates and required negative controls.
- [ ] Shipping-image soak and cold-cycle campaigns with retained evidence.
- [ ] Physical known-defect negative control and resulting findings.
- [ ] Manager ratification of the provisional restoration ceiling.
- [ ] Independent re-review of this head and required merge evidence.

The bench executor supplies the power-strip and journal-window instrumentation.
No physical release result is claimed. Desk evidence does not discharge #70,
#117 or bench acceptance items 3 and 4.
