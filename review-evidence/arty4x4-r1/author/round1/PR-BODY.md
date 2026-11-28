Base: `dev-soft-core`. Relates to #878.

## Summary

This adds the Arty split end station at 4x4/1if: four AAF talkers and four AAF listeners on the one 100 Mb/s interface, plus the CRF input and output.
It adds the configuration, its scheduler shape, its own service-budget point `arty-4x4`, and the census that measures that point.
**The census finds no row that meets every owner bound**, so this branch installs no row of its own and is not a qualified image. It is published as the measurement and the decision it needs.

## The 100 Mb/s envelope

Milan v1.2 4.3.3.2 Table 4.4's recipe, against 802.1Q 34.3.1's 75 % class-A limit (75,000 kb/s each way):
- Egress: four 2-channel 48 kHz talkers (7,360 kb/s each) and the CRF output (5,632 kb/s) reserve 35,072 kb/s, 46.8 % of the limit. The builder states the same figure.
- Ingress: the worst admissible case, four 8-channel 48 kHz inputs and the CRF input, reserves 71,936 kb/s, 95.9 %.

What the image offers:
- Stream Outputs: the 2-channel 48 kHz Base format only. The framer is stereo, and SET_STREAM_FORMAT admits only the declared output shape.
- Stream Inputs: 2-channel 48 kHz current, with Milan v1.2 6.4's 48 kHz family (1 to 8 channels) derived after it. All of it fits four-up.
- No 96 or 192 kHz Stream Input format: 6.4 would then owe that rate's 8-channel formats, and four of those (28,864 and 53,440 kb/s) exceed the limit.
- The AUDIO_UNIT advertises 48 kHz alone.

Milan v1.2 5.4.2.7 allows SET_STREAM_FORMAT only two refusals, STREAM_IS_RUNNING and BAD_ARGUMENTS for mapped channels. "In all other cases a PAAD-AE shall return SUCCESS." So the image keeps every format that does not fit out of its advertisement rather than refusing it at SET_STREAM_FORMAT. This needs a decision if a bandwidth refusal is wanted as well.

## Changes

- `configs/endstation_arty_split_4x4.yaml`: `endstation_arty_split`'s shape four times over at `control.placement: split`, 80/50 MHz, the board's 1409/100 ns pair, plus the CRF output Milan v1.2 7.2.3 requires. It has its own hash-derived model id and no pin.
- Its generated shape include. No other tracked generated file moves.
- `ctrl_loop.h` THE SHAPES: the (1,5,5) row, at the 1x1's statements, the basis its census ran at.
- The service-budget harness: the `arty-4x4` point in every per-point table, and `arty_grade.py --point`. The harness self-test and the builder suite name the new point and configuration.
- Documentation: the builder and build pages, the harness README and `SPLIT_CONTROL_MEMORY.md` section 15.

## Service budget

The census ran 159 native cases across eight image variants at exactly 80 MHz. Every case passed natively, with no refusal and no pass over THE SHARE (longest 1.897 ms). Costs come from the existing rule (measured plus 5 %, rounded up to 5 us), with #969's disposition as at the 1x1.

The rule's derivation tried every queued-notice bound from 125 to 140 ms and every pace from 1 to 13 ms, with the slice by the rule. **No candidate meets every owner bound.**

| Bound | Owner | Least any candidate reaches |
|---|---:|---:|
| Long-window load | 0.70 | 0.578 |
| ACMP | 30 ms | 37.39 ms |
| txL | 49 ms | 58.71 ms |
| Last queued notice | 140 ms | 201.93 ms |
| THE SHARE | 2 ms | 1.897 ms |

Without #969's disposition, the control #1022 asks for, the load is 1.03 and no last-notice row is finite. #1022 also owns the owed registration lines at this point.

At the 1x1's own costs, the 4x4's counts alone already leave no row (least ACMP 29.84 ms and txL 48.79 ms, never together). The 4x4's measured costs then add 3 to 10 ms.

The seven `backlog-owed` held-egress rows measure 61.92 to 64.13 ms. No ledger is stated for them at this point.

## Egress at 100 Mb/s

A lane-local replay of every commit of the 159 traces runs through the shipping transmit queue: the rings, the gasket, the merges, the store-and-forward FIFO, 80 ns an octet, and the 4x4's SR and gPTP frames.
- (a) Every free-space test keeps its census outcome.
- (b) The worst wait is 535.88 us, 564.67 us with 5 % and a 2 us fixed path, within 1000 us.

The in-tree grader with planted defects is #1004's, and the fixed path here is an analytic bound, not the shipping-chain measurement the ruling asks for.

## Fit

Routed at the census image's firmware, all three #818 directives meet the floor at every corner.
- ExtraPostPlacementOpt: WNS +0.486 ns, WHS +0.054 ns, 41,745 LUT, 46,802 FF, 15,333 slices, 86 BRAM tiles. This is the 4x4's first baseline.
- The firmware links in 49.5 of the 56 RAMB36 budget.

## Identity

Every existing image's inputs are byte-identical to the base:
- the builder outputs of all six existing configurations;
- the product firmware ELFs of `endstation_arty_split` and both AX7101 split shapes.

No HDL, LiteX, mailbox or existing configuration file changes.

## Validation

- Four firmware shards with RV32.
- The 4x4 split boot simulation, native controls 6/6 and region self-test; the 1x1 boot.
- `test_ctrl_memory`; the MII and `lat` host arms, 15/15 plants.
- The service self-test, 323/323 mutants; the standalone `rows_tiers`, `load_grade` (28/28), `egress_ledger`, `record_classes`, `shape_costs` and `arty_grade` self-tests.
- `arty_grade` at `arty-1x1` PASS; at `arty-4x4` it refuses the point.
- The builder suite; `test_clock_contract`.
- Every documentation and idiom gate.

## Decision needed

No rule-conforming row exists at 4x4/1if on the 80 MHz Arty. Options include a smaller Arty shape, firmware cost work at this shape, or a clock ruling. None is taken here.
