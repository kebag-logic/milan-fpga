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

**GREEN, review ready (round 2)**: `643-t30-phase` -> `dev`, head
`6b96391d13c5d777a98b1c7be9265c63d651c911`. Round 1's `98729742`, then a `--no-ff` merge of dev `241f9184`
(PR #638), then two commits. Processor pin `631eeb34`.

- **The suite, under GNU make 4.3, cold.** At dev's pin: rc 0, shipping leg
  245 checks with 0 failing, two-stream leg 65/0, leg defects 5/5, 661.3 s.
  At processor `main` `c4cb84ff`, in a scratch parent with both adoption
  patches applied and never committed: rc 0, the same counts, 673.8 s.
- **Every standing window is gradable**, its margin from the 8-cycle
  ambiguity window a check: the least is 48 cycles (+0, `--law-only`).
- **The setpoint +/-1 mutants** fail the fill and band checks at all 18
  feed phases, at both processors. A2-a removed still fails all 18 settled
  checks.
- **The boundary-band diagnostic** (`tdm8render-law-boundary`): rc 0, 81 of
  81, at both processors.
- **The full mutant campaign**: rc 2 at both processors, 32 checks, 28 PASS, 4 FAIL,
  identical verdicts. Every arm this change adds or touches passes. The four
  failures are round 1's pre-existing four, which dev's own harness also
  fails (see Known limitations).

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

### Round 2

R456-1 (MAJOR) and R457-1 found the same flaw in round 1's tie rule: its
premise of one cycle of feed jitter is false after settle. Within one phase
the offset from a PDU end to its nearest pop walks by up to 3 cycles, and
where it sits depends on the run's history. At the boundary phase a sound
design failed and a setpoint -1 defect passed. The
[round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974715857)
withdrew the tie rule for a stated ambiguity window:

| Item | Change |
|---|---|
| 1. The spread | `--law-boundary` scanned every phase from +1,986 to +2,066 (the boundary is near +2,026) at both processors, ascending, descending and each phase alone: 486 windows. No graded window failed the sound design. The walk was at most 3 cycles in any `[LAW]` phase and 4 in T30's CRF window, identically at both processors. **W = 4 + a guard of 4 = 8 cycles** |
| 2. Grading by the window | A window with a PDU end whose nearest pop is within 8 cycles of the boundary its fill reads across is **NOT GRADABLE**: named with the PDU and the offset, its law neither passed nor failed. Every standing window (the 18 `[LAW]` phases and the T30 CRF window) must be gradable, a check of its own, with its margin printed. A graded window needs a fill of exactly 14, no allowance, and a first event in (8, 9] ticks plus the pop pulse's one-cycle register: the 64-cycle tie slack is gone. Each `[LAW]` phase grades exactly 124 PDUs (R457-1 S1) |
| 3. Standing proof | `tdm8_render_mutants.py`: the render setpoint one event low and one event high in `--law-only`, each required to fail the fill and band checks at all 18 phases. `--law-boundary [--jobs N]` (the `tdm8render-law-boundary` target): the unmutated gateware and both setpoint defects, each in three histories; every phase must come out graded or not gradable, a graded one passing on the sound design and failing both law checks on a defect, and each scan must hold both kinds |
| 4. Docs | `TIME_SYNC.md:451` restated for the PDU end (R456-1 F2 = R457-1 F2); `MEDIA_CLOCK_FOLLOWING.md` (the `[LAW]` row, a diagnostic row, and "The ambiguity window" in place of the tie rule); the suite's row in `tb/verilator/README.md`; `TESTING.md` |
| 5. Dev | Merged dev `241f9184` (PR #638) with `--no-ff`; its touched gates run at the head |

Round 1's pieces, as they stand now:

| Piece | Change |
|---|---|
| `[LAW]` phase (`sim_tdm8_render.cpp`) | Waits for the aligner's settled report: engaged, error inside 1/64 sample for 2,048 ticks, within the 32,768-tick ceiling. Then a fresh stream at the INTERNAL grid's own cadence at each of 18 feed phases, a phase being a delay after an observed media tick (16 over one tick, plus +927 and +1,156). Per phase: the aligner held the report throughout; the window is gradable; fill 14 at every PDU end; every first event inside (8, 9] ticks of its PDU end, plus one cycle. Runs in the full leg after T31 and alone as `--law-only` |
| The grading instant | The render stage's PDU end: the accepted clone beat with tlast, which is what the stage's `pdu_end_w` is made of; the fill is read once that beat is in. The T30 CRF LAW shares the instrument |
| T30's INTERNAL window | Keeps its pin and A2-a checks; it no longer grades the law |
| `tdm8_render_mutants.py` | The planted defect `mga_sel_w = follow_sel_r;` (A2-a removed) in `--law-only`, which must fail all 18 per-phase settled checks; a check name may be a tuple, every one of which must fail |

No RTL file changes. The declared law and its bounds are unchanged.

## Authoritative references

- #643 and its [assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856), the [item 1 STOP](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973437153), the [ruling](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039) and the [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974715857)
- The round-1 reviews: [R456-1](https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5974712082), [R457-1](https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5974627143), and their packets on `643-review-evidence`
- #629's D4 = A2-a and its design page, [`docs/design/MEDIA_CLOCK_FOLLOWING.md`](docs/design/MEDIA_CLOCK_FOLLOWING.md#simulation)
- The render law and the settle band: [`docs/design/TIME_SYNC.md`](docs/design/TIME_SYNC.md#listener-render-latency); `hdl/milan/milan_datapath.sv:6264-6266` (`SRC_SETTLE_*`), `:5905` (A2-a), `:6426` (the setpoint)
- The stage's own reference and its pop: `hdl/ieee1722/aaf/KL_render_setpoint.sv:56`, `:73`, `:533-534`, and the registered pop pulse
- #647, the open design gap for a stream running through an aligner pull-in

## How to get into the same state

```sh
git fetch origin && git checkout 643-t30-phase      # head 6b96391d
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
# the campaign and the boundary diagnostic from INSIDE the suite directory:
# under `make -C` the outer -w reaches the nested print-srcs and every
# rebuilt arm "does not compile" (pre-existing)
cd tb/verilator/milan_dp_render
make tdm8render-mutants VERILATOR=<pinned verilator 5.050>
make tdm8render-law-boundary VERILATOR=<pinned verilator 5.050> LAW_BOUNDARY_JOBS=8
```

Expected result / pass criteria:

- The default target exits 0: `tdm8_render: checks: 245 failures: 0`, then
  `checks: 65 failures: 0`, then `5 checks: 5 PASS, 0 FAIL`. For each of the
  18 phases and the CRF window the `[LAW]` lines show the nearest pop, the
  walk, the least clearance and a positive margin from the 8-cycle window,
  then 124 PDUs (292 for CRF), fill 14..14 and a delay inside (8, 9] ticks of
  the PDU end; and 0 ticks outside the settle band.
- The campaign prints `32 checks: 28 PASS, 4 FAIL` and exits 2. Among the
  passes: `[PASS] mutant caught (ship --law-only): the render setpoint one
  event low - breaks "T30 INTERNAL LAW +0: the fill ..." and 35 more`, the
  same for one event high, and A2-a removed with its 18 settled checks.
  The four failures are the pre-existing ones under Known limitations,
  which dev's own harness also fails.
- The boundary diagnostic prints `81 checks: 81 PASS, 0 FAIL` and exits 0:
  for each design, the leg's own scan and the descending scan leave
  +2,017..+2,034 not gradable, and the phases run alone leave +2,016..+2,036.
- The same with processor `c4cb84ff` in the scratch parent.

## Known limitations / out of scope

- **A running stream through a pull-in is not graded.** It keeps the
  displacement, one event at some phases; that is #647's design question.
- **The standing phases' margin is asserted, not assumed.** Each standing
  window carries a check that no PDU end has a pop within 8 cycles of the
  boundary. The nearest, +0, clears it by 56 cycles in `--law-only` and 57 in
  the full leg: a margin of 48 and 49. The CRF window's margin is 579 (dev's
  pin) and 327 (`c4cb84ff`). A change that moved the RX path's end-to-tick
  relation by more than that would fail the suite by name rather than move a
  phase onto the boundary silently. Round 1's statement that a one-cycle scan
  found ties at +2,025 and +2,026 only is withdrawn: it was one run history.
- **The window is a measurement of this model.** W = 8 is the largest walk
  measured (4, in the CRF window) plus an equal guard. A graded phase
  tolerates a walk of up to 9 cycles before a crossing could reach a graded
  end. `tdm8render-law-boundary` re-measures it.
- **The reviewers' tie probes that edit the removed tie code do not apply**
  (R457-1's `probe-instrument.patch`; R456-1's `tieoff`, `tietr18`,
  `tietr36`). Their phase lists and setpoint defects were run with the head's
  own instrument instead; every one of their boundary phases is now not
  gradable, and their setpoint defects fail every graded phase.
- **`--law-only` dwells 0.3 s before its wait.** From boot the aligner's error
  overshoots (-201 to +49 cycles) and its crossing spends just over 2,048
  ticks in the band, so the declared report can fire there and then lapse. The
  full leg never meets it there. `milan_datapath.sv:6256` calls the loop
  overdamped; this overshoot is measured at the INTERNAL boot pull-in only and
  is left to the owner.
- **`--epoch-only` no longer grades the INTERNAL law**; the full leg and
  `--law-only` do.
- **Wall time.** The default target measured 661.3 s cold at this head
  (673.8 s at `c4cb84ff`) on a shared host, against round 1's 663.8 s; the
  stated 663.8 s stands (about 1,049 s at the 1.58x hosted slowdown, inside
  the 1,800 s budget). `tdm8render-law-boundary` took 2,600 s and 2,686 s at
  six legs at a time; it is an explicit target, like the campaign.
- **Not run locally:** the Yosys elaboration and the `syn/ooc` steps that need
  the pinned sv2v (no `hdl/` file changed; this host's sv2v is v0.0.13), and
  `act` (nothing pushed from this lane).
- **Pre-existing at dev `5fabb46e`, left for new Issues (each reproduced with
  dev's own harness in round 1):**
  - `make -C tb/verilator/milan_dp_render tdm8render-mutants`, the form
    TESTING.md documents, reports every arm "did not compile" under make 4.3
    and 4.4.1. The outer `-C` puts `w` in MAKEFLAGS, and the nested
    `$(shell $(MAKE) -s -C ../milan_dp print-srcs)` captures "make[1]:
    Entering directory" into the source list. The new
    `tdm8render-law-boundary` target shares the cause, so TESTING.md states
    it is run from the suite directory.
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
