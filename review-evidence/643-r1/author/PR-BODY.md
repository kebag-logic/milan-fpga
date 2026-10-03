[A522]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**GREEN, review ready**: `643-t30-phase` -> `dev`, head
`98729742b71d5088f250440eb46085daf1c0cbdb` (two commits on dev `5fabb46e`,
processor pin `631eeb34`).

- **The suite, under GNU make 4.3, cold.** At dev's pin: rc 0, shipping leg
  226 checks with 0 failing, two-stream leg 65/0, leg defects 5/5, 663.8 s.
  At processor `main` `c4cb84ff`, in a scratch parent with both adoption
  patches applied and never committed: rc 0, the same counts, 680.0 s.
- **The planted defect.** A2-a removed fails the settled check at all 18
  feed phases, at both processors.
- **The full mutant campaign** (`tdm8render-mutants`, from inside the suite
  directory): rc 2 at both processors, 30 checks, 26 PASS, 4 FAIL, identical
  verdicts. Every arm this change adds or touches passes. The four failures
  fail the same way with dev's own harness (see Known limitations).

## Linked Issue / roles

Closes #643
Relates to #629
Relates to #647

Executor: `[A522]`
Internal cleared-context reviewer: `[R456]`
External reviewer: `[R457]`

## Description

T30 graded the #386 render law at INTERNAL inside the aligner's pull-in after
T14's serial-clock hold, so it passed or failed with the feed's phase against
a moving grid. The second processor pin moved that phase and failed it. Item 1
measured 66 phases inside and after the transient at both processors; the
[ruling on the STOP](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039)
took option (c). This PR is (a), the test-only fix. Mechanism 2, a running
stream that keeps the pull-in's displacement, is #647.

| Piece | Change |
|---|---|
| `[LAW]` phase (`sim_tdm8_render.cpp`) | Waits for the aligner's settled report: engaged, error inside 1/64 sample for 2,048 ticks, within the 32,768-tick ceiling. Then a fresh stream at the INTERNAL grid's own cadence at each of 18 feed phases, a phase being a delay after an observed media tick (16 over one tick, plus +927 and +1,156). Per phase: the aligner held the report throughout; fill 14 at every PDU end; every first event inside (8, 9] ticks of its PDU end, plus 64 cycles. Runs in the full leg after T31 and alone as `--law-only` |
| The grading instant | Moves from the RX accept pulse to the render stage's PDU end: the accepted clone beat with tlast, which is what the stage's `pdu_end_w` is made of; the fill is read once that beat is in. The T30 CRF LAW shares the instrument and moves with it |
| The tie rule | A pop within one cycle of the PDU's last beat may read that end's fill one event toward its side: 13 with the pop taken with the beat, 15 with it taken a cycle later. The band is unchanged |
| T30's INTERNAL window | Keeps its pin and A2-a checks; it no longer grades the law |
| `tdm8_render_mutants.py` | The planted defect `mga_sel_w = follow_sel_r;` (A2-a removed) in `--law-only`, which must fail all 18 per-phase settled checks; a check name may be a tuple, every one of which must fail |
| Docs | `docs/design/MEDIA_CLOCK_FOLLOWING.md` test section (a row and "The render law's grading instant"); the suite's row in `tb/verilator/README.md`; `docs/testing/TESTING.md`; the suite's Makefile header (wall time) |

No RTL file changes. The declared law and its bounds are unchanged.

## Authoritative references

- #643 and its [assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856), the [item 1 STOP](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973437153) and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039)
- #629's D4 = A2-a and its design page, [`docs/design/MEDIA_CLOCK_FOLLOWING.md`](docs/design/MEDIA_CLOCK_FOLLOWING.md#simulation)
- The render law and the settle band: [`docs/design/TIME_SYNC.md`](docs/design/TIME_SYNC.md#listener-render-latency); `hdl/milan/milan_datapath.sv:6264-6266` (`SRC_SETTLE_*`), `:5905` (A2-a)
- The stage's own reference: `hdl/ieee1722/aaf/KL_render_setpoint.sv:56`, `:73`, `:533-534`
- #647, the open design gap for a stream running through an aligner pull-in

## How to get into the same state

```sh
git fetch origin && git checkout 643-t30-phase      # head 98729742
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# the pinned Verilator 5.050 and GNU make 4.3
```

For processor `c4cb84ff`: a copy of this tree with the `protocol-processor`
gitlink and checkout at `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`, then
`git apply` the two adoption patches (c8 `bbf704ec`, then p2/p1 `1269cdaf`),
never committed.

## How to validate

```sh
make -C tb/verilator/milan_dp_render VERILATOR=<pinned verilator 5.050>
# the campaign from INSIDE the suite directory: under `make -C` the outer -w
# reaches the nested print-srcs and every arm "does not compile" (pre-existing)
cd tb/verilator/milan_dp_render && make tdm8render-mutants VERILATOR=<pinned verilator 5.050>
```

Expected result / pass criteria:

- The default target exits 0: `tdm8_render: checks: 226 failures: 0`, then
  `checks: 65 failures: 0`, then `5 checks: 5 PASS, 0 FAIL`. The `[LAW]` lines
  show, for each of the 18 phases, 124 PDUs, fill 14..14, a delay inside
  (8, 9] ticks of the PDU end and 0 ticks outside the settle band.
- The campaign prints `30 checks: 26 PASS, 4 FAIL` and exits 2. Among the
  passes: `[PASS] mutant caught (ship --law-only): A2-a removed: the aligner
  is not engaged at INTERNAL - breaks "T30 INTERNAL LAW +0: ..." and 17 more`,
  and the `--law-only` positive control. The four failures are the
  pre-existing ones under Known limitations, which dev's own harness also
  fails.
- The same with processor `c4cb84ff` in the scratch parent.

## Known limitations / out of scope

- **A running stream through a pull-in is not graded.** It keeps the
  displacement, one event at some phases; that is #647's design question.
- **No standing phase is a tie.** A one-cycle scan from +2,010 to +2,045 found
  ties at +2,025 and +2,026 only; at +2,026, 11 of 124 PDUs read 15 and pass
  only by the rule. It is evidence in the hand-off, not a suite check.
- **`--law-only` dwells 0.3 s before its wait.** From boot the aligner's error
  overshoots (-201 to +49 cycles) and its crossing spends just over 2,048
  ticks in the band, so the declared report can fire there and then lapse. The
  full leg never meets it there. `milan_datapath.sv:6256` calls the loop
  overdamped; this overshoot is measured at the INTERNAL boot pull-in only and
  is left to the owner.
- **`--epoch-only` no longer grades the INTERNAL law**; the full leg and
  `--law-only` do.
- **Wall time.** The shipping leg went from 113.0 s to 215.4 s side by side;
  the default target from 560.0 s to 663.8 s cold (about 1,049 s at the 1.58x
  hosted slowdown, inside the 1,800 s budget).
- **Not run locally:** the Yosys elaboration (reads only `hdl/`, unchanged)
  and `act` (nothing pushed from this lane).
- **Pre-existing at dev `5fabb46e`, left for new Issues (each reproduced with
  dev's own harness):**
  - `make -C tb/verilator/milan_dp_render tdm8render-mutants`, the form
    TESTING.md documents, reports every arm "did not compile" under make 4.3
    and 4.4.1. The outer `-C` puts `w` in MAKEFLAGS, and the nested
    `$(shell $(MAKE) -s -C ../milan_dp print-srcs)` captures "make[1]:
    Entering directory" into the source list.
  - The `--epoch-only` positive control has been red since #629's A2-a: it
    runs `[CRF]` without the boot dwell `--crf-only` got, so four "T30 CRF ...
    recentre" checks read 0. Its two clean controls fail on exactly those
    four.
  - The `--serial-only` mutant "uncounted repeat: the underrun counter never
    increments" survives.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
