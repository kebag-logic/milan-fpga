Base: `dev-soft-core`. Closes #1027.

**Stacked on #1004.** This branch carries #1004's commits through its round 11 (`c0b625d1`) and merges after #1004. Until #1004 lands, the diff against `dev-soft-core` shows its commits too. Against #1004's head, this PR's own change is 28 files in 21 commits.

**Task contract.** [#1027](https://github.com/kebag-logic/milan-fpga/issues/1027) holds this point's scope, its acceptance and its five decisions. #878 stays the Arty 1x1 point's issue, and its rulings, the 80 MHz clock among them, stay in force there.

## Summary

This adds the Arty split end station at 4x4/1if: four AAF talkers and four AAF listeners on the one 100 Mb/s interface, with the CRF input and the CRF output Milan v1.2 7.2.3 requires.
It is qualified with the control CPU at 100 MHz:
- the routed image meets the #818 floor at every corner;
- the rule's scheduler row meets every owner bound;
- the 100 Mb/s egress row holds, the CRF output in its stream load;
- the held-egress rows stay within the point's own ledger.

At 80 MHz no row exists at this shape (least txL 58.71 ms, ACMP 37.39 ms), so this image runs at 100 MHz ([#1027](https://github.com/kebag-logic/milan-fpga/issues/1027), decision 1). The 1x1 keeps its 80 MHz.

## Decisions it rests on

All five are on [#1027](https://github.com/kebag-logic/milan-fpga/issues/1027):
1. Clock: 100 MHz for this image only, provided the route meets the floor at every corner.
2. Held-egress ledger: this point is its own ledger entry by #878's rule, as [#1020's ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) (item 3) makes the USB-network Arty's. The largest figure is 63.50 ms.
3. Bind bounds: #1004's rule at this point, 550 ms and 4 saves.
4. Formats: only formats that fit four-up on 100 Mb/s are advertised, so SET_STREAM_FORMAT never needs the bandwidth refusal Milan v1.2 5.4.2.7 does not allow.
5. Owed to the bench: the timestamp correction pair at 100 MHz.

## The 100 Mb/s envelope and the formats

Milan v1.2 Table 4.4 against 802.1Q 34.3.1's 75 % class-A limit:
- Egress: four 2-channel 48 kHz talkers and the CRF output reserve 35,072 kb/s, 46.8 % of the limit.
- Ingress: the worst case is four 8-channel 48 kHz inputs and the CRF input, 71,936 kb/s, 95.9 %.

The image offers:
- Stream Outputs: the 2-channel 48 kHz Base format, the stereo framer's only width.
- Stream Inputs: the 48 kHz Base family (1 to 8 channels).
- No 96 or 192 kHz Stream Input format, whose 8-channel members do not fit four-up.

## Changes

- `configs/endstation_arty_split_4x4.yaml`:
  - `endstation_arty_split`'s shape four times over, at `control.placement: split`, plus the CRF output;
  - its own hash-derived model id;
  - the AUDIO_UNIT at 48 kHz alone;
  - sys/CPU 100 MHz (the 800 MHz VCO / 8; the datapath stays at 50 MHz).
- Its generated shape include.
- `ctrl_loop.h` THE SHAPES: the (1,5,5) row the rule derives.
- The service-budget harness:
  - the `arty-4x4` point in every per-point table, with its own 100 MHz clock;
  - `arty_grade.py --point`;
  - its bind bounds by the Arty rule;
  - its own held-egress ledger in `egress_ledger.py`.
- `egress_mii.py` counts a shape's CRF output in the 100 Mb/s queue's stream load, and its self-test runs at both Arty points. `--packet` and `--structural` take `--point`.
- `egress_fixed.py` measures at another sys clock on request, runs isolated as its usage line states, and has a self-test.
- `record_classes.py` holds the 4x4 point at its own clock, configuration and ACMP record cost.
- The builder suite and the harness self-test name the new configuration and point.
- Documentation:
  - the builder and build pages, and the harness README;
  - FR_NFR 3.4.1's 100 Mb/s row, and FR-CLK-05's owed correction pair;
  - `SPLIT_CONTROL_MEMORY.md` section 15, now "Arty split points": the 4x4's decisions, stated costs, qualification and held-egress ledger.

## Results

**Route at 100 MHz.** ExtraPostPlacementOpt meets the floor at every corner: Slow WNS +0.049 / WHS +0.156 ns, Fast +1.606 / +0.012 ns, zero failing endpoints. ExtraTimingOpt and AltSpreadLogic_high meet timing but miss the floor at +0.002 ns.
Utilization: 41,858 LUT, 46,808 FF, 15,387 slices, 86 BRAM tiles. The firmware links in 49.5 of the 56 RAMB36 budget.

**Scheduler row.**
- Derived by the unchanged rule from three complete 159-case censuses at 100 MHz. The last drains egress at link rate, because at 100 MHz AECP's notice bursts overrun the 512-word ring at the line rate.
- Each cost is the largest of its three measurements, and the row is a fixed point: the link-rate census moves only `CTRL_LOOP_TX_MS`, by a value no firmware byte depends on.
- Two rows meet every rule and bound (125/5/1250 and 130/5/1000); the derivation orders them by pace, then queued-notice bound, then slice, and installs the first.
- #969's disposition applies, with #1022 owning the owed lines.

| Bound | Result | Owner |
|---|---:|---:|
| Load | 0.4689 | 0.70 |
| ACMP | 28.52 ms | 30 ms |
| txL | 48.72 ms | 49 ms |
| Last notice | 117.68 ms | 140 ms |
| THE SHARE | 1.733 ms | 2 ms |

The row is a 1250 us slice, a 5 ms pace and a 125 ms queued bound. The qualification passes over all 159 cases and eight variants.

**Thin margins, as measured.** The owner bounds are unchanged; these are the closest results:

| Quantity | Measured | Bound | Margin |
|---|---:|---:|---:|
| txL | 48.72 ms | 49 ms | 0.28 ms |
| THE SHARE (longest whole pass) | 1.733 ms | 2 ms | 0.267 ms |
| Setup, Slow WNS (ExtraPostPlacementOpt, the one directive that closes) | +0.049 ns | +0.030 ns floor | 0.019 ns |
| Hold, Fast WHS (same route) | +0.012 ns | 0 ns | 0.012 ns |

**100 Mb/s egress** (`egress_mii.py`, 159 cases): (a) holds, the census draining at link rate. (b): the largest wait 446.76 us, with gPTP and 5 %, plus the stated 320 ns fixed path (300.0 ns measured at 100 MHz), is 527.04 us of 1 ms. At most 35 records queue at once. The stream load is (90, 90, 90, 90, 46) octets, the CRF output's frame last.

**Held-egress ledger.** The link-rate census's 1655 measured instances are all within their figures, with no new miss. The 1x1's and 8x8/1if's figures are unchanged.

| Row | Measured at 100 MHz, ms | Ledger, ms |
|---|---:|---:|
| `backlog.owed.if0` | 62.64658 | 62.78 |
| `backlog.owed_behind0.if0` | 62.82023 | 62.97 |
| `backlog.owed_behind1.if0` | 62.98813 | 63.14 |
| `backlog.owed_behind2.if0` | 63.15874 | 63.32 |
| `backlog.owed_behind3.if0` | 63.32736 | 63.50 |
| `backlog-owed.service.acmp.last.if0` | 61.81513 | 61.91 |
| `backlog-owed.service.aecp.last.if0` | 61.56471 | 61.65 |

**Controls with planted defects.** Each behaviour this PR adds now has a self-checking control:
- `egress_mii.py --selftest` (35 of 35) runs at both Arty points. It holds each point's stream load to its stated octets and every frame of it on the wire in its interval. It refuses the other point's log, and catches the CRF frame left out of the queue, left out of the load, at zero length and an octet short.
- `record_classes.py --selftest` (26 Arty checks) holds the 4x4 at 100 MHz, refuses an 80 MHz leg, names its configuration to its own point, and reads its own ACMP record cost at (1,5,5).
- `egress_ledger.py --selftest` (26 mutants) holds each point's planted cycle to its configuration's `sys_clk_hz`.
- `egress_fixed.py --selftest` (3 mutants) holds the argument, build and report paths with a stub simulator.

The eight mutants both reviews named are each caught by a named control when planted in the tree. The documented commands run as written: `python3 -I tb/verilator/ctrl_service_budget/egress_fixed.py DIR 100000000` reports 300.0 ns and exits 0.

**Regradeable evidence.** The census-4 extract keeps each case's egress lines and each run's group grades. Two commands regrade it to the same result:
- `python3 -I tb/verilator/ctrl_service_budget/egress_mii.py EXTRACT/*/` gives 446.76 us and 527.04 us, with all 159 per-case grades identical to the full logs';
- `egress_ledger.py --point arty-4x4 EXTRACT/*/results` reads 1655 instances, PASS.

**Bind bounds.** 550 ms in flight and 4 burst saves, #1004's rule applied to this census's `save-bind` group.

**Identity.** These are byte-identical to the base:
- the builder outputs of all six existing configurations;
- the product firmware of `endstation_arty_split` and both AX7101 split shapes.

The 4x4 product firmware is byte-identical to the routed image's. No HDL, LiteX, mailbox or existing-configuration file changes.

**Validation.**
- Four firmware shards with RV32.
- The 4x4 split boot simulation, native controls 6/6 and the region self-test; the 1x1 boot.
- `test_ctrl_memory`; the MII and `lat` host arms; the firmware coverage ratchet.
- The service self-test, 323 of 323, and every standalone self-test named above.
- The builder suite: every gate but gate 11, which is not run. Its oracle is the place report of an earlier-architecture Arty build that is not on the desk, so it cannot be produced here.
- Every documentation and idiom check.

## Owed

- **Timestamp correction pair at 100 MHz** ([#1027](https://github.com/kebag-logic/milan-fpga/issues/1027), decision 5). The image keeps the 1409/100 ns pair, which was measured at an 80 MHz sys. Two of its ingress terms cross into sys, so the pair must be measured again on the board at 100 MHz. FR-CLK-05 records it as owed. The service-budget model and the egress row do not use it.
- **A bench session** with all 4+4 streams and CRF running at once (#1027's last acceptance item).
