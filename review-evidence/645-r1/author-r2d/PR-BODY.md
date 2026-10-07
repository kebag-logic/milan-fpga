[A531]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2d](#round-2d)** — R474-2's finding, its fix, the new case and controls, and the wording fixes.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED at the timing gate, at `2525eae9567865a8bc741901914bdf5a1caf2c26`
(dev `e21c1ca0` merged with `--no-ff`). Functional evidence is green: 61/61
default suites, 2,185,420 checks, 0 failures, every explicit leg and both
campaigns. The BUILDING.md section 5 sweep has no bitstream: every directive
stops at the shipping IOB-pack check on `eth0_rx_dv` (see Round 2d).
`645-ring-slip` -> `dev`. The executor does not push. This head is local
until the manager publishes it; it then awaits independent re-review.

## Linked Issue / roles

Closes #645
Closes #647
Relates to #629, #643, #657

Desk acceptance here does not discharge the issues' physical bench or release
obligations.

Executor: `[A531]`
Internal cleared-context reviewer: `[R474]`
External reviewer: `[R475]`

## Description

A late **settle recentre** fixes two residues of a media-clock transient:

- **#645.** The loopback ring keeps the servo's pull-in walk after a source
  locks, so it slips one frame 15 to 45 s later.
- **#647.** An INTERNAL aligner pull-in leaves a running stream's render
  latency shifted.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | Settle recentre armed by a CLOCK_SOURCE change, aligner re-engagement or an aligner excursion past a two-axis-cycle quiet band. It fires after 8 LOCKED servo windows (following) or 2,048 quiet ticks (INTERNAL), with a 2^20-tick ceiling. After an action, excursion arming waits for 2,048 consecutive quiet ticks (recovery qualification, one state bit, existing counter). |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | Loopback queue 16 deep, derived target 11. The settle action holds missing pops or drops exactly the excess, in lockstep across pairs. `SLIP_LB` does not count it. |
| `tb/verilator/follow_ring/` (new) | Real meter, CRF receiver, servo, NCO, aligner, loopback ring and render stage with the datapath's glue. Arrival campaigns (both offset signs, four envelopes, 16 phases), INTERNAL pull-in campaign, fine and paired pulls, controller regression at four clock rates, twelve planted controls, quiet-distribution reader. |
| `tb/verilator/chmap_capture/` | Symmetric action, a held walk before a pair's first commit counting no dup, the ruled two-PDU span check at six phases and on a two-talker fanout with offsets 0 to 5, and span controls. |
| `tb/verilator/milan_dp*/` | Physical wire check of each recentre's step and span; render pull-in leg; recentre controls. |
| Docs | `MEDIA_CLOCK_FOLLOWING.md` (contract, quiet band per clock rate, measured distribution, recovery window, declared residual), `TIME_SYNC.md`, `TESTING.md`, READMEs, regenerated module matrix (compiled sources only). |

No port or register-map change.

## Round 2d

[Round 2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032466525)
on [R474-2](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032462363).

- **R474-2-F1.** A held walk on a pair whose first commit of the PDU had not
  landed counted one `SLIP_LB` dup. `pop_dup_w` now excludes `pop_hold_w`.
  The action's pops, holds, drops and wire output are unchanged.
- **Standing case.** `[LRC]` drains a stream to zero left, pulses, drives
  only the decision beat, and walks before pair 1's first commit. It
  requires e6 five times, then e7, on both pairs, with zero dup and skip
  deltas. The same stimulus without the pulse must count exactly one dup,
  which proves the walk lands in that gap.
- **Controls.** HELD-DUP (every held pop counted) fails the new case, the
  `[LRC]` counter check and the span counter check. STARVED-HELD-DUP (the
  round-2c term) fails the new case and the `[LRC]` counter check, and no
  pre-existing check.
- **R474-2's probe P1** at this head: pulsed dup delta 0 (was +1).
- **Campaigns.** Quiet/arrival 128/128 with the reader PASS; INTERNAL
  pull-in 32/32. All 160 logs and the quiet-distribution JSON are
  byte-identical to round 2c, so the quiet distribution and the arrival grid
  are unchanged.
- **Area.** OOC own logic +113 LUT / +78 FF (limit 120 / 120). Only the
  capture head row changed; its 4 FF / 6 LUT drop from round 2c is synthesis
  replication variance, so +119 / +82 stays the conservative figure.
- **Timing gate: not met.** Synthesis now maps the LiteEth RX register
  `milansoc_phy_source_valid_reg`'s synchronous reset into a LUT in front of
  D (`eth0_rx_dv & ~eth_rx_rst`), so it cannot pack into the ILOGIC. Place
  30-722 follows, and the #475 check stops all three directives before
  routing. The remap is deterministic. Round 2c's inputs, re-synthesized
  today, still keep the reset on the pin. The only synthesized difference is
  this round's one term, so this is a latent fragility of the shipping
  build that the change happened to set off. The recommended fix is a
  separate Issue that makes the GMII RX IOB capture registers independent of
  control-set remapping; the handoff lists the options.
- **Wording.** `REGISTER_MAP.md` 0x8D4 reads "dropped events" verbatim.
  R474-2's `TIME_SYNC.md` sentence is 17 words, but the style gate allows
  10 per sentence in that file, so the same content is split into short
  sentences and line 492 is verbatim. The handoff shows both texts.

## Authoritative references

- [Round 2 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884),
  [two-PDU span ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440),
  [quiet-band and recovery ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115),
  [timing bar](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009790232).
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` (settle recentre), `docs/design/TIME_SYNC.md`,
  `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/integration/BUILDING.md` section 5,
  `REQUIREMENTS.md`.

## How to get into the same state

```sh
git fetch origin 645-ring-slip && git checkout 645-ring-slip
git rev-parse HEAD   # 2525eae9567865a8bc741901914bdf5a1caf2c26
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
git -C protocol-processor rev-parse HEAD        # ead8036035affd53ef4b29979190f2f4f67084c0
git -C gptp-processor rev-parse HEAD            # 5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
git -C third_party/verilog-axis rev-parse HEAD  # 48ff7a7e2ef782cf778d47910cf85835c64b1bce
```

Use Verilator 5.050.

## How to validate

```sh
S=/tmp/645-check            # any scratch outside the tree
cd tb/verilator/follow_ring
make VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR=$S/fr
make sweep-pullin VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR=$S/pullin
cd ../../..
bash scripts/run_all_suites.sh $S/sweep
bash scripts/run_all_suites.sh $S/physical --physical-gptp
(cd tb/verilator/milan_dp_render && make tdm8render-pullin && make tdm8render-law-boundary)
python3 docs/traceability/gen_module_matrix.py --check
```

The full arrival campaign (128 runs) and its reader are in the handoff
packet; one run takes about 10 to 40 minutes.

Expected result / pass criteria: every command exits 0.

- `small pulls: 10/10 passed`, `follow_ring mutants: 12/12 caught`, and the
  settle controller PASS at 6.25, 25, 50 and 100 MHz.
- `follow_ring pullin campaign: 32/32 runs passed`.
- `quiet distributions: 128 phases, 512 windows, peak 1 axis cycles; band 2: PASS`.
- `chmap_capture`: `KL_chan_map_capture: 785 checks, 0 failures`.

Measured at `3eee12dc`, the last commit that changed shipping HDL, or at this
head. The dev merges `701b8332` and `2525eae9` change only firmware, the `mbx`
Makefile and one design note. The gates that read those files (`mbx`, dev's
firmware-unit job, the source and docs gates) were rerun at this head:

| Gate | Result |
|---|---|
| Arrival campaigns | 128/128 runs; quiet error within +/-1 axis cycle over 320,462,699 samples; one settle recentre per transient; no slip after it; minimum margins 2.17 (empty) and 2.24 (full) ticks; every log byte-identical to round 2c |
| INTERNAL pull-in | 32/32, byte-identical to round 2c |
| `chmap_capture` | 785 checks, 0 failures; netlist leg 20/0 |
| Default sweep | 61/61 suites, 2,185,420 checks, 0 failures; follow_ring controls 12/12 |
| Physical gPTP | 197 checks, 0 failures; two recentres on the wire at the exact step inside the span; counters unchanged; recentre controls 14/0 |
| Render pull-in, LAW boundary | 18/18 phases; 81/81 over 564 windows |
| Builder, selftests | rc 0 (builder's Arty calibration arm NOT RUN: build tree absent) |
| `mbx`, firmware unit job | at this head: 316, 361, 316 and 13 checks, 0 failures, mutants 5/5; 7/7 |
| Portability, vendor parser | 58 modules PASS; xvlog PASS at the ratchet, 0 findings in `hdl/` (at this head) |
| Source and docs gates | 28/28 at this head |
| Timing | **FAIL**: synthesis rc 0; ExtraPostPlacementOpt, AltSpreadLogic_high and ExtraTimingOpt each stop at the IOB-pack check on `eth0_rx_dv` (Place 30-722); no bitstream, no WNS/WHS. Round 2c's `f6bd415f` gateware passed (+0.368 ns) |
| Own area | OOC +113 LUT / +78 FF (limit 120 / 120); round 2c's +119 / +82 is the conservative figure |

## Known limitations / out of scope

- **Declared residual.** A second INTERNAL pull that starts inside the
  previous action's recovery window gets no new recentre and may keep its
  render shift. The worst observed isolated window is 0.551 s. Continuing
  disturbances can extend it.
- **Loopback latency.** The diagnostic loopback target is 11 events, three
  ticks (62.5 us) later than 8. AAF presentation latency and the render law
  are unchanged.
- **#657.** Four render-mutation failures exist on `dev` as well; they are
  out of scope and the full mutation campaign is not claimed.
- **Not run here.** Hardware, flashing and the bench campaigns are outside
  this lane.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
