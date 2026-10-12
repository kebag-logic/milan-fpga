[A576]

## Contents

- **[Status](#status)** -- Local bar result, test tally and `621-ascapable-phc-step` -> `dev`, with both heads.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor and independent reviewers.
- **[Description](#description)** -- The gPTP correction, the capture-harness grading fix, the receipt refresh, the review round 2 and 3 fixes, the `milan_dp` runtime split and the round 4 runner-test fix.
- **[Authoritative references](#authoritative-references)** -- Requirements, IEEE 802.1AS-2020 clauses, design pages and rulings.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkouts for the candidate and the base.
- **[How to validate](#how-to-validate)** -- Focused gPTP checks, the capture invariant and the full local bar.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally -- `621-ascapable-phc-step` -> `dev`. The runtime-round head is pushed; hosted results at `f5d0fb0e` are the manager's to confirm.
The round 4 head `2cf985f3` is local and unpushed.

- Round 4 head: `milan_dp`'s runner test `test_sim_pool.py` passes 17 of 17, and all 28 backpressure controls pass when run from a fixture location where the Makefile's relative paths resolve (#720).
- Round 4 head: seven planted Makefile defects, among them the pre-delta recipe, each fail both runner tests by name.
- Runtime round head: `milan_dp` passes natively in 2124.4 s (4126.6 s at `83239549`, 2870.1 s at the base); the new `milan_dp_gm_steps` suite passes in 741.0 s.
- Runtime round head: the clean gmstep leg passes 190 checks; its five sweep controls are each caught by the named check.
- Runtime round head: the explicit `gmstep-mutants` campaign, run from the new suite, catches all 20 controls on the whole leg.
- Runtime round head: `ci_events.py --check` and `--selftest`, the shard selftest and the test-evidence ratchet exit 0.
- Round 3 head: the touched `gptp_plane` suite passes (29 checks, then `phc_step` 62 checks and its campaign 8 of 8).
- Round 3 head: the test-evidence ratchet (`measure_test_evidence.py --check` and `--selftest`) exits 0.
- Round 3 head: every runnable step of the `docs-check` job passes locally.
- At `e0ee38f9`: 61/61 suites (2,186,819 checks), Yosys 58/58, vendor front end, three routes and three resource endpoints pass.
  Rounds 2 and 3 change no RTL, donor file or other suite input.

Parent head: `2cf985f3206dd519d80142fd2479afe24c3051f6`.
Donor head: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, unchanged since round 1; publish it before the parent so the gitlink is fetchable.
Branch `621-ascapable-phc-step` targets `dev`. Fourteen parent commits on `5603c353`:

| Commit | Change |
|---|---|
| `a99dbccf` | Adopt the donor fix; real-counter PHC step campaign and parent integration tests; docs and pins |
| `72848a76` | INTERNAL-source CLOCK_DOMAIN edge checks across steps |
| `034e2e30` | Capture harness: the 24.5 ms bound applies only to production arms |
| `e0ee38f9` | Capture receipt recorded from this head's campaign |
| `7ad00dbc` | Round 2: the receipt gate grades every arm as production, with a control that fails if the guard is removed |
| `47b9b7e8` | Round 2: the hold-sizing page states the refreshed receipt's identities and figures |
| `167798a0` | Round 2: test-evidence disposition for the step campaign's generator reads |
| `d96b4a84` | Round 2: a crossing exchange must count as answered before peer silence; both reviewers' plants rejected |
| `4818cc37` | Round 3: the step campaign's duplicate plant is counted once; the receipt drift attribution is narrowed |
| `83239549` | Round 3: a crossing request that is never answered earns no liveness credit; R571-2's plant rejected, its control passes |
| `9182cee7` | Runtime round: `sim_gmstep.cpp --no-small-steps` leaves out the #621 phase and nothing else |
| `0e3eef5b` | Runtime round: the gmstep leg and its five sweep controls move to the new `milan_dp_gm_steps` suite on worker 3/5 |
| `f5d0fb0e` | Runtime round: native per-leg times and the hosted projection, in the suite README and the CI policy page |
| `2cf985f3` | Round 4: `milan_dp`'s runner tests describe the split `run` recipe; the #658 `dynmap` leg joins their inventory |

## Linked Issue / roles

Relates to #621. The later lane's physical repeat completes it.

Executor: `[A576]`
Internal cleared-context reviewer: `[R570]`
External reviewer: `[R571]`

## Description

Grandmaster-driven PHC steps contaminated the neighbour-rate window.
The invalid delay cleared asCapable until two good exchanges arrived.
The regression reproduces approximately two seconds of loss for both signed 10 ms steps.

The donor invalidates rate history when applying a phase step.
An overlapping exchange proves liveness while preserving the last valid measurement.
Clean exchanges resume measurement; excessive delay and missing responses still clear capability.
The parent adopts the donor and tests independent peer timestamps, public counters and media continuity.

| Piece | Change |
|---|---|
| Donor `hdl/ucode/gen_gptp_ucode.py` | Servo step invalidates the rate seed; both completed-pair paths skip the crossing exchange; a new request rearms measurement |
| Donor images and docs | Regenerated ROMs; phase-step measurement contract in `docs/INTEGRATION.md` |
| `tb/verilator/gptp_plane/` | Real 8 MHz PHC counter, independent peer, six step placements, two liveness arms, six planted microcode defects (the two liveness-deletion controls, one per review round, plant the same deletion, so five distinct defects run) and one positive control |
| `tb/verilator/milan_dp/sim_gmstep.cpp` | Independent peer timestamps; capability, delay, uncertainty, GM-change, CLOCK_DOMAIN and media checks for both signs |
| Docs, diagrams, ROM digests | Adopted pin and phase-step contract |
| `tb/verilator/nvm_capture_cpu/run.py` | Production timing bound no longer applied to the byte-only control |
| `tb/verilator/nvm_capture_cpu/measurements.json` | Receipt recorded from this head's campaign |
| `scripts/check_nvm_capture.py`, capture README | Every receipt arm graded as production; new control and `--mutation receipt-opt-out` |
| `scripts/measure_test_evidence_readers.py` | Disposition for `tb/verilator/gptp_plane/phc_step.py` |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | Section 18 and limits item 6 quote the refreshed receipt |

The [round 1b ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087415319) permits the capture-harness correction.
The census growth in `d81198c2` had pushed the byte-only control past 24.5 ms.
The [final ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382) sets the receipt refresh's invariant.
The candidate's capture logs must be byte-identical to the base's in every arm and control. They are, in all nine:

| Arm or control | Rows | Capture log SHA-256, base and candidate |
|---|---:|---|
| 1x1-50-on | 16 | `01f72663af25e764…` |
| 1x1-50-off | 16 | `5ade9a6e67b903d9…` |
| 8x8-50-on | 16 | `1e637b00877cba32…` |
| 8x8-50-off | 16 | `6399c81cc09b798e…` |
| 8x8-100-on | 16 | `63afb13860f998a6…` |
| 8x8-100-off | 16 | `ff4a2e45e2fe2fc7…` |
| skip-copy | 2 | `eb1ac8583dd179a4…` |
| no-traffic | 2 | `914d1c10dadb5138…` |
| byte-only | 2 | `19327660eae0953a…` |

The refresh records the candidate values as measured.
All 56 changed fields are listed with their receipt lines in the handoff evidence:

| Class | Count | Source |
|---|---:|---|
| Verdict: 8x8 / 50 MHz rows 0 to 2 of ON, row 0 of OFF, minima, maximum, margins | 14 | dev capture-SoC RTL drift, `a2f17342` to `5603c353` |
| `requests` in traffic-ON rows | 24 | the same drift |
| `harness_sha256/run.py` | 1 | `034e2e30` |
| `gptp_ucode_sha256` (six arms), gPTP pin | 7 | donor `7dda9c3b` |
| Protocol-processor pin, four 8x8 `config_sha256` | 5 | dev (`2ad2f845`; `6178aa1bd`, flash image unchanged) |
| `date`, `base`, `tree`, `provenance`, `remeasurement_assignment` | 5 | this remeasurement |

The old receipt was already stale at the base.
The base writes the candidate's capture logs, and its protocol pin and 8x8 configuration already differed.
The receipt's own measured tree `a2f17342` reproduces the old values in the three arms rerun there.
The published 8x8 / 50 MHz maximum moves from 13.86484 to 13.86318 ms, a margin of 3.5345 to the 49 ms floor.
The 1x1 and 8x8 / 100 MHz maxima are unchanged. Every capture stays within 24.5 ms.
The byte-only control is 1.834x the matching maximum.

### Review round 2

The [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6095695340) answers [R570-1](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6095669772) and [R571-1](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6095689596).

| Item | Finding | Change | Evidence |
|---|---|---|---|
| 1 | R570-1-F1 = R571-1-F1 | Disposition for `phc_step.py`: it generates each arm's ROM from the donor generator and plants five named defects in scratch copies; expectations come from the peer model and link constants | `measure_test_evidence.py --check` and `--selftest` rc 0; local `docs-check` replica passes |
| 2 | R570-1-F2 | `check_receipt` grades each arm through an explicit production spec. A new control plants a capture a tick over half the floor in an arm claiming `byte-only`, and requires refusal | Gate rc 0; its five mutations rc 1. Removing the guard (mutation or two source plants) fails the control. R570-1's probe refuses both plants |
| 3 | R570-1-F3 = R571-1-F3 | Section 18 and limits item 6: date, ruling, measured commit, tree, pins, maxima, margins and both 8x8 / 50 MHz rows | Every figure and identity compares equal to `measurements.json`; the unedited page shows 16 differences |
| 4 | R570-1-F4 = R571-1-F2 | After an answered crossing exchange, the peer goes silent. asCapable must fall when the fourth unanswered request is judged lost, not the third (allowedLostResponses 3, IEEE 802.1AS-2020 11.2.13.4 and 11.2.19) | Clean: 4 unanswered. Both reviewers' deletion plants: 3, rejected by name. Donor generator unchanged |
| 5 | R571-1-R1 | Status wording | This body |

### Review round 3

The [round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6096658408) answers [R571-2](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6096652745). [R570-2](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6096655113) is positive.

| Item | Finding | Change | Evidence |
|---|---|---|---|
| 1 | R571-2-F1 | New arm: the same crossing step, but the peer also ignores the crossing request, so that exchange never completes. It earns no credit: asCapable falls at the third unanswered request after it, the fourth lost in all (allowedLostResponses 3, IEEE 802.1AS-2020 11.2.13.4 and 11.2.19). R571-2's `credit_on_step` plant, with its cease-rule deletion, joins the campaign; the deletion alone is a control that must pass | Clean: 3 after the crossing request. `credit-on-step`: 4, rejected by name, the only failure. `nocease-control`: 62 of 62. Planted text byte-identical to R571-2's. Donor generator unchanged |
| 2 | R571-2-RES-1 | The duplicate liveness plant is counted once, on the design page, in the disposition text, in the campaign comment and in this body | The design page's style gate caps sentences at 10 words, so its clause is three short sentences |
| 2 | R571-2-RES-2 | The drift attribution sentence, verbatim | Page figures still equal `measurements.json` |

### Runtime round

The [runtime-round assignment](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6101380300) answers hosted run 38048622822: `milan_dp` hit its 4800 s limit at `83239549`.

Native per-leg measurement, base `5603c353` and head `83239549` run together on one host (wall seconds):

| Leg | Base | Head | Change |
|---|---:|---:|---:|
| `gmstep` clean run | 56.4 | 262.1 | +205.7 |
| `gmstep_mutants.py`: six runs (positive control, five controls) | 264.8 | 1326.4 | +1061.6 |
| every other leg together | 2548.9 | 2538.1 | -10.8 |
| whole `milan_dp` | 2870.1 | 4126.6 | +1256.5 |

The legs that cost the time are the gmstep leg's seven runs. Each grew by its #621 phase, 173 of 222 CPU seconds in a profiled run.
Dev's own `milan_dp` already took 2972.7 to 3519.6 s on six hosted pushes, 62% to 73% of the limit.
Removing only the #621 phase could therefore not reach the required 60%.

| Piece | Change |
|---|---|
| `tb/verilator/milan_dp/sim_gmstep.cpp` | `--no-small-steps` leaves out the #621 phase and nothing else; other options are refused |
| `tb/verilator/milan_dp_gm_steps/` | New default suite: the clean leg with every phase once, then `gmstep_mutants.py --no-small-steps`; `gmstep-mutants` is the whole-leg campaign |
| `gmstep_mutants.py` | Moved there; builds and runs through `milan_dp`'s recipe and run directory; forwards the flag |
| `tb/verilator/milan_dp/Makefile` | `run` no longer runs the gmstep leg or its controls |
| `scripts/suite_shards.py` | Five-worker landmark: `milan_dp_gm_steps` on worker 3/5, the default worker with the most headroom |
| Test-evidence disposition, suite README, test, CI and design pages | The new path, the split, its measurements and projection |

The five sweep controls name checks in the media, GM change and CRF restart phases, none in the #621 phase.
With it in every run, four of them broke no #621 check; the restart-term control also broke the eight #621 `mr` and MEDIA_RESET checks, never graded.
The explicit `gmstep-mutants` campaign keeps every control on the whole leg. No RTL, donor file, check name, expected value or control changes.

At the split head `0e3eef5b`: `milan_dp` 2124.4 s, `milan_dp_gm_steps` 741.0 s, natively.
Removing the gmstep share measured at base (21.9%) from the six dev windows projects `milan_dp` to 2323 to 2750 s, at most 57.3% of 4800 s.
At the windows' worst ratio to this host the new suite projects to 909 s, 50.5% of its 1800 s budget. Hosted runs at the pushed head confirm or replace both.

### Review round 4

The [round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6103886503) answers [R570-4](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6103883668). [R571-4](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6103605946) is positive.

| Item | Finding | Change | Evidence |
|---|---|---|---|
| 1 | R570-4-F1 | `test_sim_pool.py`: after `render_mutants.py`, `make -n run` prints only make's own directory messages, and no line names `gmstep` or `GM step`. `test_sim_pool_backpressure.py`: `run`'s prerequisites must not include `gmstep`; the expected output ends with the render banner; a `gmstep_mutants.py` stand-in must never run | Seven planted Makefile defects each fail both tests by name: the `gmstep` prerequisite, the banner and controls after or before the render step, the controls line alone, another step after render, the `dynmap` leg removed, and the whole pre-delta Makefile |
| 2 | Scope ruling | The #658 `dynmap` leg joins `LEGACY_LEGS`, in recipe order | `test_sim_pool.py` 17 of 17; R570-4's `probe_sim_pool_dynmap.py` exits 0 |
| 3 | R570-4-R1 | Status wording, exactly as given | This body |
| Optional | R570-4-S1 | Not taken. The driver does not see the clean leg's transcript. Enforcing the tally would need a second full run, a new recipe contract or a pinned count | The clean leg runs every phase. R570-4's comparison holds, and nothing it reads changed |

The old backpressure test, with only the `dynmap` addition, passes all 14 recipe controls at `83239549` and fails both normal drains at `f5d0fb0e`. So F1's backpressure half is now shown by execution too.
Run as invoked, the backpressure test still hangs at its first recipe control (#720). The copied Makefile reads `../nvm_capture_cpu/recipe.py` at parse time, relative to a temporary directory where it does not exist, so make stops before any leg starts. The test then waits for a leg-start announcement that never comes.
The recipe-control evidence above runs the test's own `exercise()` with each case directory placed beside `milan_dp` instead. No test line was changed for that.

## Authoritative references

- REQUIREMENTS.md REQ-PTP-05, REQ-PTP-07 and REQ-PTP-08.
- IEEE 802.1AS-2020 clauses 11.2.2, 11.2.19.3.3, 11.2.19.3.4 and 11.2.20.
- [gPTP plane design](docs/design/GPTP_PLANE.md).
- [Time synchronization design](docs/design/TIME_SYNC.md).
- [Software grandmaster findings](docs/findings/387_SOFTWARE_GM_STEP.md), #387 and #620.
- [Capture harness recipe](tb/verilator/nvm_capture_cpu/README.md) and its [receipt](tb/verilator/nvm_capture_cpu/measurements.json).
- [Resource measurement recipe](docs/testing/PP_SHADOW_BASELINE_RECIPE.md).
- Rulings [6087415319](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087415319) (harness correction) and [6089776382](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382) (receipt invariant and refresh).
  The latter replaces 6087498843, 6087655217 and 6088189432.

## How to get into the same state

```sh
git checkout 2cf985f3206dd519d80142fd2479afe24c3051f6
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

For the capture invariant, also use a separate clean checkout of the base `5603c353137e90c1fa95429f6d00ef7a2298d9ee` at its own pins.
Those pins are donor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
The capture measurements ran from the tree of `034e2e30`, which differs from `e0ee38f9` only in the receipt.
Rounds 2, 3 and 4 and the runtime round change no capture harness file, so every `harness_sha256` entry still matches.

## How to validate

Focused gPTP checks, from the parent root:

```sh
python3 tb/verilator/gptp_plane/phc_step.py --work "$RESULTS/phc" --mutants
make -j1 -C tb/verilator/milan_dp_gm_steps VERILATOR_JOBS=2
make -j1 -C tb/verilator/milan_dp_gm_steps gmstep-mutants VERILATOR_JOBS=2
```

Expected: 62 clean checks, one passing control and six rejected microcode defects.
The suite: 190 integration checks, then the positive control and five rejected controls on the leg without the #621 phase.
The campaign: 190 checks, both clean legs and 20 rejected controls on the whole leg.
The two liveness-deletion controls, one per review round, plant the same deletion, so five distinct defects run.
Each deletion fails only `asCapable falls at the fourth unanswered request after a crossing exchange`.
`credit-on-step` fails only `asCapable falls at the third unanswered request after an unanswered crossing request`.
The control `nocease-control`, the cease-rule deletion that plant uses for ROM room, passes every check.

Capture invariant: use the [capture recipe](tb/verilator/nvm_capture_cpu/README.md) environment.
That is the product interpreter, offline dependencies, `PYTHONHASHSEED=0`, networking disabled and Verilator 5.052 first on `PATH`.
Run each receipt arm's `command` in both checkouts, plus the README's three controls, then compare:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir "$SCRATCH/capture-8x8-50-on"
cmp "$CANDIDATE/capture-8x8-50-on/capture.log" "$BASE/capture-8x8-50-on/capture.log"
python3 scripts/check_nvm_capture.py
```

Expected: every `cmp` exits 0 silently. Every candidate run exits 0.
The base byte-only control exits 1 because its unfixed grader applies the production bound to it; its log still matches.
The input gate prints `PASS`, and each of its five `--mutation` controls exits 1.

Static gates changed in rounds 2 and 3, from the parent root:

```sh
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/check_nvm_capture.py
python3 scripts/check_nvm_capture.py --mutation receipt-opt-out
make -C tb/verilator/gptp_plane
```

Expected: the first three and the suite exit 0; the mutation exits 1 with `receipt arm escaped the production timing bound`.

`milan_dp`'s runner tests, changed in round 4 (Linux, with `os.pidfd_open`):

```sh
python3 tb/verilator/milan_dp/test_sim_pool.py
python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py
```

Expected: the first exits 0 with 17 of 17. The second passes its 14 direct controls and then hangs at its first recipe control, as at the base (#720).

Full local bar at the parent head:

```sh
scripts/run_all_suites.sh "$RESULTS/suites"
syn/yosys/run.sh --results "$RESULTS/yosys"
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101-ooc" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax8x8-ooc" --endpoint ooc-8x8
```

Expected result: every command exits 0. Recorded at `e0ee38f9`, every one exits 0.
The sweep passes 61 of 61 suites with 2,186,819 checks, and Yosys passes 58 of 58 tops.
Lint is at 90 of a 90 ratchet, and xvlog has 0 findings.
The default, AltSpreadLogic_high and ExtraTimingOpt routes are fully routed with timing met: WNS +0.299, +0.100 and +0.201 ns.
`route-1x1`, `ooc-1x1` and `ooc-8x8` match the resource baseline with zero delta, and `check-baseline` passes.

## Known limitations / out of scope

- `scripts/check_nvm_capture.py` does not hash the capture SoC's RTL, configuration or pins.
  That is how the old receipt stayed green while stale at the base. Per the earlier ruling, that gap belongs to the #495 checklist.
- The capture drift is attributed to dev's capture-SoC RTL between `a2f17342` and `5603c353`. It is not narrowed to a single commit.
- The later lane's physical five-step repeat completes #621.
- Both liveness arms pin the donor's existing threshold: asCapable falls when the fourth consecutive request is judged lost.
  That follows the allowedLostResponses definition in IEEE 802.1AS-2020 11.2.13.4.
  The RESET state of Figure 11-9 compares before it increments, which read literally gives the fifth. Neither is changed here.
  A fifth-loss donor variant fails both arms' count checks and the peer-silence check.
- The round 3 count starts after the crossing request, like the round 2 count. "The third unanswered request" is therefore the fourth lost request in all, the crossing request included.
- The full sweep, Yosys and vendor stages were not rerun for rounds 2, 3 and 4 or the runtime round, which change no RTL or donor file.
  The runtime round reran the two suites whose inputs changed, `milan_dp` and `milan_dp_gm_steps`, and the static gates.
  It did not update or run `milan_dp`'s two runner tests; round 4 updated both and ran them. Round 4 changes only those tests, which no suite or workflow runs.
- #720 owns two defects that predate this lane. No gate runs either runner test. Run as invoked, the backpressure test's recipe controls hang (diagnosed in round 4 above, not changed).
- `tb/verilator/milan_dp/README.md` still says the recipe has eleven ordinary simulations. It has had twelve since #658. The round 4 ruling covers `test_sim_pool.py` only.
- The hosted figures in the runtime round are projections from native runs on a shared eight-core host.
  The `milan_dp` projection leaves about 130 s to the 60% line at the slowest dev window; hosted runs at the pushed head settle it.
- In the sweep, the restart-term control's incidental failures of the #621 `mr` and MEDIA_RESET checks now show only in the explicit campaign.
  The sweep never graded them: each control is graded by its named check, unchanged.
- In one checkout, `milan_dp` and `milan_dp_gm_steps` share `milan_dp`'s generated ROM images.
  Each suite writes them only when they are missing, before any simulation reads them; hosted workers use separate checkouts.
- Under #629 C1, CLOCK_DOMAIN counts remain unchanged for the integration harness's unlocked CRF source.
  Separate INTERNAL cases require one unlock/lock pair per step.
- The builder check passed required RV32 and elaboration coverage.
  Its historical resource-calibration arm was unavailable because its archived report was absent.
- Publication, independent review and merge remain with the assigned roles.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (simulation items; the physical repeat is later)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

