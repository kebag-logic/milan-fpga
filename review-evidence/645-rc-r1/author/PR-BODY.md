[A620] A listener bind's first PDU at INTERNAL arms the settle recentre (#645)

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

GREEN locally: eleven default-sweep suites 52,122 checks and the physical gPTP leg 197, 0 failures; `follow_ring` controls 15/15; `sweep-bind` 32/32 -- `645-bind-recentre` -> `dev`. Not yet reviewed; no hosted run yet.

## Linked Issue / roles

Relates to #645

The bench repeat of bench lane B17's ten binds, on an image built with this change, is #645's acceptance. The manager runs it after the merge, outside this PR.

Executor: `[A620]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

Bench lane B17 ([PR #741](https://github.com/kebag-logic/milan-fpga/pull/741), [report](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187529947)) found that each of 10 binds at INTERNAL slipped the DUT's loopback ring one frame, at the bind's first burst of PDUs more than 20 us late, and nothing after. A bind primes the ring where its first PDU lands, and at INTERNAL nothing armed the settle recentre to centre it. The [design round](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500) decided to complete that model rather than declare the slip.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | Inside the settle recentre's block, one flop per loopback stream waits from the stream's bind rise for its first accepted `tlast` beat, the beat that primes its queue. At INTERNAL that beat arms the settle recentre, which fires by the unchanged INTERNAL rule (2,048 settled or disengaged ticks, 21.8 s ceiling) and stays the declared discontinuity: counted in `recentres_o`, not in `SLIP_LB`. Under following it arms nothing. No port, register, parameter or other module changes. |
| `tb/verilator/follow_ring` | A `bind` case replaying B17's cycles from its packet: first-PDU delay, first burst time and peak, the largest later burst, B17's mean burst decay (1.538 us per PDU). A fifth default leg (B17 cycles 5, 4 and 9 with 0 to 5 us of lateness, then one bind under CRF following). `make sweep-bind` (all ten cycles at 16 first-PDU phases, with and without lateness). Three planted controls: NO-BIND-ARM, BIND-RISE, FOLLOWING-ARM. `settle_control.py` grades the arm at all four axis rates. |
| Docs | `MEDIA_CLOCK_FOLLOWING.md` (the arm in the settle-recentre table, a new "A bind at INTERNAL", the test plan), `TIME_SYNC.md`, `REGISTER_MAP.md`'s `SLIP_LB` row, `TESTING.md` (rows and the default wall clock), and the test-evidence dispositions. |

Results:

- **Reproduction without the arm** (dev `f6260253`'s datapath through the same harness, 320 binds): each of the 169 binds whose first PDU primes the ring inside B17's bound (10 to 24.565 us of margin) slips it exactly one frame at its first burst, as at the bench.
- **With the arm:** all 320 binds get one arm at the first PDU, one settle recentre 2,047.0 to 2,048.0 ticks later and one counted render recentre. Nothing slips after the ring acts, and the 169 in-window binds move neither `SLIP_LB` counter. After the recentre the ring keeps at least 3.48 ticks on its empty side and 4.88 on its full side.
- **Controls:** `make mutants` catches 15/15, the three new ones by their named checks.
- **Area,** out of context, base against head (Vivado 2026.1): +3 LUT and +1 FF on the shipping 1x1 TDM8 shape. The shipping 8x8 builds no loopback lane, so the arm prunes away there (0 / 0). Against NFR-RES-01's 38,040 LUT that is 0.02 % of the current image's gap.

## Authoritative references

- #645, its [design round](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500), the [B17 report](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187529947) and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255) it ran under.
- PR #741 and its evidence branch `645-b17-review-evidence` (`review-evidence/645-b17-r1/author/summary/`), the source of every replayed parameter.
- PR #672, the settle recentre, and its rulings on #645.
- [`docs/design/MEDIA_CLOCK_FOLLOWING.md`](../docs/design/MEDIA_CLOCK_FOLLOWING.md#settle-recentre), [`docs/design/TIME_SYNC.md`](../docs/design/TIME_SYNC.md#listener-render-latency).
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

Expected result / pass criteria: every command exits 0. `follow_ring`'s bind leg reports one arm, one settle recentre about 2,048 ticks later and one render recentre per bind, `SLIP_LB` +0/+0; under CRF following no arm. `make mutants` prints 15/15 caught. `sweep-bind` passes 32/32 runs.

## Known limitations / out of scope

- **The arming window.** For the 42.7 ms between a bind's first PDU and its recentre, the ring keeps its primed margin. In the campaign, 6 of the 151 binds whose first PDU primes the ring under 10 us slipped once in that window, all within about 2 ms of the first PDU and at the two phases nearest the empty edge. B17 put the bench's margin above 10 us, and no in-window bind slipped. Stated in the design, not declared.
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
