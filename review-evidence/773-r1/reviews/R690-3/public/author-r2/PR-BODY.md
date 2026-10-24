[A664]

## Contents

- **[Status](#status)** — Gates, head and branch, and what round 2 changed.
- **[Linked Issue / roles](#linked-issue--roles)** — #773, executor and reviewers.
- **[Description](#description)** — The crossing estimate, the fixed delay and the CRF TC, each derived and in whole periods, and what they change.
- **[Authoritative references](#authoritative-references)** — IEEE 1722-2016 and Milan v1.2 clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout.
- **[How to validate](#how-to-validate)** — The legs that prove it and the gates.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is derived only, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar.

## Status

READY FOR REVIEW at `1b47a3dc` (eight commits on dev `a032c6d6`), `773-aaf-capture-to-wire-latency` -> `dev`. Round 2 adds two commits on `13d8f1e8`: documentation and one comment, no RTL line. Each gate below ran at the head it names, and nothing else is claimed.

| Gate | Head | Result |
|---|---|---|
| Full Verilator sweep, 4 shards | `1b47a3dc` | every shard rc 0; 64 of 64 suites pass, each run once, none timed out; 2,190,887 checks, 0 in-suite failures. capture_coherence 20,832/0, its dp leg 847/0, its mutation arm 42/42; aaf startup mutants 8/8 |
| `cd tests && behave --no-capture -f plain` | `1b47a3dc` | 406 scenarios passed |
| lint | `1b47a3dc` | 89 <= 89 |
| `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` (GNU Make 4.3) | `1b47a3dc` | rc 0 each |
| docs workflow's gate steps (GNU Make 4.3) | `1b47a3dc` | 41 pass, 2 skipped by rule; the em-dash gate run directly against `a032c6d6`: 0 findings |
| The domain event's header edit is comment-only | `13d8f1e8` -> `1b47a3dc` | identical after comment stripping |
| Vivado front end | `13d8f1e8` | 0 findings |
| Yosys | `bf2d96f9` | 60/60 tops |
| tdm8render-mutants, pull-in, gmstep-mutants | `bf2d96f9` | 31/31; 19 legs, 0 failures; 23/23 |
| route-1x1 against the eleventh record | `13d8f1e8` | LUT +102, FF +7, SLICE -11, RAM and DSP 0, WNS +0.040 ns (from +0.236), WHS +0.021 ns: PASS |
| ooc-1x1, ooc-8x8 | `13d8f1e8` | every figure equal: PASS |

The rows at `13d8f1e8` and `bf2d96f9` were not re-run at `1b47a3dc`. From `bf2d96f9` to `13d8f1e8` only `tb/verilator/aaf/start_mutants.py` changed. From `13d8f1e8` to `1b47a3dc` only two documentation pages and a comment changed. Hosted contexts at the head are not claimed here.

### Round 2

This round answers the round 1 reviews' findings.

- **R689-1-F1, R690-1-F1.** "The listener's buffer" now states two bounds:
  - grid live: 2,038,676 ns (1x1) and 2,054,392 ns (8x8);
  - start-up: a PDU stamped from the live PHC before the grid is live, handed over at least 5,343 cycles (106,860 ns) after that base. That bound is 2,059,807 ns at both shapes, the `[HOLD]` maximum measured in every 2 ms run.

  The render-queue margins become 492.1 us (1x1) and 487.0 us (8x8). The grid-live margins are still 513.3 / 492.4 us. Equation (1)'s lead ceiling is now taken from the start-up PDU: 231.8 us, where it was 237 us. The supported-range paragraph counts this talker's 8 Ps: transit under 2,135,548 ns (1x1) or 2,140,725 ns (8x8); offsets up to 2,489,452 / 2,484,275 ns plus the transit for a PDU's first event, and 2,385,285 / 2,380,108 ns plus the transit for a whole six-event PDU. The compliance matrix row states both bounds.
- **R690-1-F2.** The complete four-shard sweep ran at the final head (above).
- **R689-1-R1.** `KL_media_domain_event.sv`'s header carries the reviewer's wording.
- **R689-1-S2.** The MAC-level figures at 1 Gb/s are stated, derived:
  - one maximum frame ahead at the MAC takes 12.3 us of the spare. That leaves 5,480 / 6,576 ns for AAF (1x1 / 8x8) and 8,167 / 2,990 ns for CRF;
  - 100 Mb/s is not covered.

  The same derivation finds one case outside the cover (Known limitations).
- S1 and S3 (optional) were not taken.

## Linked Issue / roles

Relates to #773
<!-- Every acceptance item is met at 1x1. The 8x8 TDM32 proof is derived only, as the round 1b ruling allows, so this PR does not close #773 by itself. -->
Relates to #632, #764

Executor: `[A664]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Since #770 the AAF talker stamps the instant its PDU's first frame started at the media interface (IEEE 1722-2016 4.3.5). The PDU cannot leave until its sixth frame has closed and been carried to the MAC, 112 to 149 us later. So at a 125 us offset every PDU reached the wire after its own timestamp. The ruling ([option (b)](https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380110812)) reads Milan v1.2 5.3.7.6's two parts:

- **The crossing estimate:** the end of the PDU's six-sample span, the instant plus 6 periods.
- **The fixed delay:** the fewest whole periods covering the worst hand-over after that estimate. It is derived at elaboration and refused above 125 us. It is 2 periods at both shipping shapes.
- **The stamp:** the instant plus 8 Ps (166,667 ns) plus the offset as set. The end-to-end latency is the offset plus 166,667 ns. GET_STREAM_INFO reads the offset as set.
- **CRF:** Equation (14)'s TC, the fewest whole periods covering the path from the timing point's frame instant to its hand-over: 2 periods (41,667 ns) at 1x1 and 1 (20,834 ns) at 8x8. The round-up of the offset and the readback are unchanged.

Both constants are whole periods and sit in the existing stamp adders, so the two outputs still stamp one grid's instants.

| Piece | Change |
|---|---|
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv` | `LEAD_P`, `FS_HZ_P`, `CLK_HZ_P`, `IN_LATE_NS_P`: its own pipeline term `PIPE_CYC_C`, the delay `DELAY_PER_C`, the lead `LEAD_NS_C` (a constant in the stamp adder) and the refusal `g_lead_delay`. Default off: other instances are byte-identical |
| `hdl/ieee1722/crf/KL_crf_tx.sv` | `TC_P`, `CLK_HZ_P`, `EV_LATE_NS_P`: its pipeline (9 cycles), `TC_PER_C`, `TC_NS_C` (a constant in the `ts_r` adder). Default off |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv` | `walk_pair_cyc()`, `age_max_cyc()`: the capture walk and the capture age |
| `hdl/milan/milan_datapath.sv` | the terms `TLK_*` beside the packetizer, the marker-latency localparams moved to their first reader, the crossbar's gap bound from one value, both talkers bound with their terms |
| `tb/verilator/capture_coherence` | the dp leg runs the CRF output beside the talker, at 2 ms and at 125 us: `[WIRE]`, `[GRID]`, `[HOLD]`, the `[PIN]` grade with the 8 periods; 7 planted controls in `mutants.py` |
| `tb/verilator/milan_dp/sim_nxn.cpp` | the output walk grades IEEE 1722-2016 Equation (1)'s window and one whole number of periods per output, at 2 ms, 1 ms, 2,010,000 ns and 125 us |
| docs | `MEDIA_CLOCK_FOLLOWING.md` (the talkers' capture-to-wire latency), the compliance matrix, `TESTING.md`, `CHANGELOG.md` |

The derived terms at 50 MHz:

| Term | 1x1 TDM8 | 8x8 TDM32 |
|---|---:|---:|
| The span's end to the last frame's close (marker latency less one period) | 131 ns | -15,525 ns |
| Capture age, at most | 1,043 cycles | 1,043 cycles |
| Capture walk to the last talker's last pair | 86 cycles | 811 cycles |
| Packetizer | 57 cycles | 60 cycles |
| **Hand-over after the estimate** | **23,851 ns** | **22,755 ns** |
| **Fixed delay** | **2 periods, 17,816 ns spare** | **2 periods, 18,912 ns spare** |
| CRF path (marker, event register, 9 cycles) | 21,164 ns | 5,508 ns |
| **CRF TC** | **2 periods, 20,503 ns spare** | **1 period, 15,326 ns spare** |

The spare covers one frame ahead at the round-robin transmit arbiters (3,960 ns for an AAF PDU, 4,400 ns for a CRF PDU). That wait is no derivation term, as the ruling counts the hand-over; counting it would refuse two compressed-clock test shapes that grade no stamp.

## Authoritative references

- IEEE 1722-2016 4.3.3, Equation (1): PT - TTmax - TUmax < TT < PT - TTmax.
- IEEE 1722-2016 4.3.5: whole media periods between a generated stream and a recovered one.
- IEEE 1722-2016 10.7, Equation (14), with TC; 10.8, Equation (15).
- Milan v1.2 5.3.7.6: the presentation time offset and the fixed delay of 0 to 125 us.
- Milan v1.2 5.4.2.9, 5.4.2.10.2: SET_STREAM_INFO and GET_STREAM_INFO on a Stream Output.
- Milan v1.2 4.4.2.1: a listener buffers up to 2.126 ms.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md`, "The talkers' capture-to-wire latency".

## How to get into the same state

```sh
git fetch origin
git checkout 773-aaf-capture-to-wire-latency
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
make -C tb/verilator/capture_coherence dp
make -C tb/verilator/capture_coherence mutants
make -C tb/verilator/milan_dp run-nxn
make -C tb/verilator/milan_dp run-nxn8
```

Expected result / pass criteria: the dp leg prints `capture_coherence_dp: checks: 847   failures: 0`, with `[WIRE]`, `[GRID]` and `[HOLD]` passing in every one of its 31 runs at 2 ms and 125 us. `mutants` ends `42 checks: 42 PASS, 0 FAIL`, the seven #773 controls among them. Both milan_dp legs end `failures: 0`, and every output adds one whole number of periods (AAF 8, CRF 2 on those test shapes).

## Known limitations / out of scope

- The 8x8 TDM32 figures are derived only. No harness runs that shape at its clocks. `milan_dp`'s 8x8 entity leg runs a 100 MHz test clock with the audio clock 1:1, where it adds 8 periods (AAF) and 2 (CRF) and keeps Equation (1)'s window at every offset.
- The hand-over is the datapath's MAC transmit port. The MAC's own backpressure at line rate is outside it. Its figures at 1 Gb/s, derived and not measured, are in `MEDIA_CLOCK_FOLLOWING.md`:
  - one maximum frame ahead at the MAC is covered at both shapes and both outputs;
  - the MAC's transmit FIFO is store-and-forward. If a maximum frame takes the arbiters just ahead of an 8x8 CRF PDU, with an AAF PDU between them, that PDU leaves up to 2,714 ns after its timestamp less the applied offset;
  - more than one maximum frame ahead is not bounded, and neither is 100 Mb/s.
- The start-up and grid-live bounds are at the nominal frame rate. A media clock fast by 1,000 ppm moves them by 104 ns.
- A frame ahead at the transmit arbiters is covered by the spare at both shipping shapes, not by a derivation term.
- The bench prediction at 125 us is that avtp_timestamp minus the wire time moves from -15.9..-10.2 us to about +150.8..+156.5 us. It is not measured here: no bench access.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
