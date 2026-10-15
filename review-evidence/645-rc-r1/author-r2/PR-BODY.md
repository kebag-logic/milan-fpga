[A620] A listener bind's first PDU at INTERNAL arms the settle recentre (#645)

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- The answers to R635-1 and R634-1: the B17 bound, the arming-window residual and the area headline.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at the round 2 head: `follow_ring` default (five legs) rc 0, controls 15/15, `sweep-bind` 32/32. The round 1 bank (eleven default-sweep suites, 52,122 checks, and the physical gPTP leg, 197, 0 failures) ran on the same RTL; round 2 changes only `follow_ring`'s harness constant and comments and the design page. `645-bind-recentre` -> `dev`. Round 1 reviews R635-1 and R634-1 were NEGATIVE for MINOR findings only; round 2 answers them and awaits both re-reviews.

## Linked Issue / roles

Relates to #645

The bench repeat of bench lane B17's ten binds, on an image built with this change, is #645's acceptance. The manager runs it after the merge, outside this PR.

Executor: `[A620]`
Internal cleared-context reviewer: R634
External reviewer: R635

## Description

Bench lane B17 ([PR #741](https://github.com/kebag-logic/milan-fpga/pull/741), [report](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187529947)) found that each of 10 binds at INTERNAL slipped the DUT's loopback ring one frame, at the bind's first burst of PDUs more than 20 us late, and nothing after. A bind primes the ring where its first PDU lands, and at INTERNAL nothing armed the settle recentre to centre it. The [design round](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500) decided to complete that model rather than declare the slip.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | Inside the settle recentre's block, one flop per loopback stream waits from the stream's bind rise for its first accepted `tlast` beat, the beat that primes its queue. At INTERNAL that beat arms the settle recentre, which fires by the unchanged INTERNAL rule (2,048 settled or disengaged ticks, 21.8 s ceiling) and stays the declared discontinuity: counted in `recentres_o`, not in `SLIP_LB`. Under following it arms nothing. No port, register, parameter or other module changes. |
| `tb/verilator/follow_ring` | A `bind` case replaying B17's cycles from its packet: first-PDU delay, first burst time and peak, the largest later burst, B17's mean burst decay (1.538 us per PDU). A fifth default leg (B17 cycles 5, 4 and 9 with 0 to 5 us of lateness, then one bind under CRF following). `make sweep-bind` (all ten cycles at 16 first-PDU phases, with and without lateness). Three planted controls: NO-BIND-ARM, BIND-RISE, FOLLOWING-ARM. `settle_control.py` grades the arm at all four axis rates. |
| Docs | `MEDIA_CLOCK_FOLLOWING.md` (the arm in the settle-recentre table, a new "A bind at INTERNAL", the test plan), `TIME_SYNC.md`, `REGISTER_MAP.md`'s `SLIP_LB` row, `TESTING.md` (rows and the default wall clock), and the test-evidence dispositions. |

**B17's window.** B17's cycle 5 bounds the margin its bind primed from both sides, from its own `c05.json`: below 24.565 us, the peak of the first burst, which slipped the ring; above 30.260 - 20.833 = 9.427 us, since that slip moved the ring one tick off its empty edge and the cycle's 30.260 us later burst then slipped nothing. The other nine cycles are consistent with it (their own later-burst bounds 6.74 to 9.24 us, first-burst peaks 24.97 to 29.31 us). The harness classes a bind inside the window when the margin it measures over the whole interval before the ring acts lies within 9.427 to 24.565 us.

Results (`sweep-bind`, 320 binds, 177 of them inside the window):

- **Reproduction without the arm** (dev `f6260253`'s datapath through the same harness): each of the 177 in-window binds slips the ring exactly one frame at its first burst, as at the bench. The 143 outside slip too (43 one frame, 99 two, one a frame and a pair).
- **With the arm:** all 320 binds get one arm at the first PDU, one settle recentre 2,047.0 to 2,048.0 ticks later and one counted render recentre. Nothing slips after the ring acts, and the 177 in-window binds move neither `SLIP_LB` counter. After the recentre the ring keeps at least 3.48 ticks on its empty side and 4.88 on its full side.
- **Controls:** `make mutants` catches 15/15, the three new ones by their named checks.
- **Area,** out of context, base against head (Vivado 2026.1): +3 LUT and +1 FF on the shipping 1x1 TDM8 shape. The shipping 8x8 builds no loopback lane, so the arm prunes away there (0 / 0). Against NFR-RES-01's 38,040 LUT, the current headline image is 50,013 LUT, 11,973 over (`AREA_BUDGET.md:124`); +3 LUT is 0.025 % of that gap.

## Round 2

Answers R635-1 ([comment](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6192392408)) and R634-1 ([comment](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6193454471)) as ruled in the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6193474559). The RTL does not change.

- **R635-1-F1 = R634-1-F1, the lower bound.** The harness's `kB17MarginLoUs` is now the bound B17 supports, derived in the source from cycle 5's row (`kB17[4].later_us - kTickUs` = 9.427 us; `kB17MarginHiUs` = `kB17[4].burst_us`). The reasoning that B17's 10 us listing threshold bounded the margin is gone from the harness, the design and this body. The split moved from 169 / 151 to 177 / 143: one run, `bind_j5_p05` (phase 0.3125, 0 to 5 us), primes 9.440 us at its lowest, and 8 of its binds now count inside. All 8 hold on the head; on dev's datapath all 177 slip exactly one frame at the first burst. `sweep-bind` was rerun on both datapaths, and every count in the design and here is restated from it.
- **R634-1-F2, the arming-window residual.** The arm stays as ruled. An in-window bind can take a one-pair dup (`SLIP_LB` +1 dup) 0.13 to 0.25 ms after its first PDU, before the recentre acts. It is pre-existing on dev, and the arm does not remove it. Measured at the 9.427 us bound: 1 of 151 in-window binds on 32 phases with 0 to 5 us of lateness (cycle 7, phase 0.84375); 2 of 140 on 128 phases of cycle 7 with and without lateness (phases 0.890625 and 0.9296875, both with 0 to 5 us). Under round 1's 10 us classification, R634-1 counted the same dups as 1 of 141 and 2 of 132. Out of the window, on 32 phases, 19 of 169 binds slip one frame at four phases (0.78125 to 0.875), up to 2.50 ms after the first PDU; on the dense cycle-7 grid, up to 2.88 ms. Every one of those early slips, in all three grids (6, 20 and 8 binds), is identical to the microsecond on dev's datapath. Issue #743 owns the dup's mechanism; it is not investigated here. The design's limit text and test plan now say all of this.
- **R634-1-S1, the area headline.** The area claim cites the current headline, `AREA_BUDGET.md:124` (50,013 LUT, 11,973 over), rather than the older `route-1x1` row.

## Authoritative references

- #645, its [design round](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500), the [B17 report](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187529947) and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255) it ran under; the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6193474559).
- PR #741 and its evidence branch `645-b17-review-evidence` (`review-evidence/645-b17-r1/author/summary/`), the source of every replayed parameter and of the window.
- #743, the in-window one-pair dup's mechanism.
- PR #672, the settle recentre, and its rulings on #645.
- [`docs/design/MEDIA_CLOCK_FOLLOWING.md`](../docs/design/MEDIA_CLOCK_FOLLOWING.md#a-bind-at-internal), [`docs/design/TIME_SYNC.md`](../docs/design/TIME_SYNC.md#listener-render-latency).
- NFR-RES-01 and the #640 budget ([`AREA_BUDGET.md`](../docs/design/AREA_BUDGET.md)).

## How to get into the same state

```sh
git fetch origin 645-bind-recentre
git switch 645-bind-recentre
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/verilog-axis third_party/tsn-c-stack
# Verilator 5.050 first on PATH
```

## How to validate

```sh
make -C tb/verilator/follow_ring                 # five legs, the bind leg among them
make -C tb/verilator/follow_ring mutants SWEEP_JOBS=4
make -C tb/verilator/follow_ring sweep-bind SWEEP_JOBS=8
make -C tb/verilator/chmap_capture
make -C tb/verilator/milan_dp_render
make -C tb/verilator/milan_dp_render tdm8render-pullin PULLIN_JOBS=4
make -C tb/verilator/milan_dp_render tdm8render-law-boundary
make -C tb/verilator/milan_dp SIM_JOBS=2
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/milan_dp_gm_steps
make -C tb/verilator/milan_dp_gptp
```

To see the slip the arm removes, build the harness with dev's datapath (`make -C tb/verilator/follow_ring build DP_SRC=<dev's milan_datapath.sv> MDIR=<dir>`) and run `<dir>/Vfollow_ring --case bind --b17-cycles 5,4,9 --bind-phase 0.125 --jitter-us 5 --dwell-s 0.5`: every cycle fails "no SLIP_LB change across the cycle" with +2 dups at B17's burst.

To see the in-window one-pair dup on either datapath, run `Vfollow_ring --case bind --bind-phase 0.843750 --jitter-us 5 --seed 672 --any-phase --dwell-s 0.5` (the 32-phase grid's phase 27, all ten cycles). Cycle 7 fails "no SLIP_LB change across the cycle" with +1 dup 0.127 ms after its first PDU; on dev's datapath the +2 at the burst follows.

Expected result / pass criteria: every `make` command exits 0. `follow_ring`'s bind leg reports one arm, one settle recentre about 2,048 ticks later and one render recentre per bind, `SLIP_LB` +0/+0; under CRF following no arm. `make mutants` prints 15/15 caught. `sweep-bind` passes 32/32 runs, 177 binds inside B17's window.

## Known limitations / out of scope

- **The arming window.** For the 42.7 ms between a bind's first PDU and its recentre the ring keeps its primed margin, and the arm changes nothing there; every slip in it is identical on dev's datapath.
  - Out of the window: in `sweep-bind`, 6 of the 143 out-of-window binds slip one frame, 0.13 to 2.13 ms after the first PDU, at phases 0.8125 and 0.875 with 0 to 5 us of lateness. On 32 phases, 19 of 169 do, at four phases, up to 2.50 ms after the first PDU; on 128 phases of cycle 7, 6 of 116, up to 2.88 ms. Each primed the ring at 3.52 us or less, below the 9.427 us B17 supports.
  - In the window: an in-window bind can take a one-pair dup (`SLIP_LB` +1) 0.13 to 0.25 ms after its first PDU: 1 of 151 on 32 phases, 2 of 140 on 128 phases of cycle 7. Pre-existing on dev, not removed by the arm, and not reached by `sweep-bind`'s 16 phases; #743 owns its mechanism. A bench reading of `SLIP_LB` +1 dup within a bind's first 42.7 ms is this.
  - Stated in the design, not declared.
- **Under following a bind arms nothing**, as ruled: such a ring still keeps its priming phase until the next settle recentre. The default leg shows B17's cycle-5 burst slipping it one frame under CRF following.
- **One recentre for every stream.** On a shape with several listener streams and the loopback lane, a bind at INTERNAL also recentres the other running streams; a ring at its target takes no step. The shipping 1x1 shape has one listener stream, and the shipping 8x8 has no loopback lane.
- **Wall clock.** The default `follow_ring` gains a fifth leg. Measured back to back on one four-CPU set, it costs 7.1 % (857.6 s against 800.9 s), which projects the last measured hosted window to 1193.2 s, under 1260 s. The hosted figure at this head is still owed.
- **Bench.** B17's repeat on a built image is #645's acceptance and is not part of this PR.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench repeat runs after the merge)
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
