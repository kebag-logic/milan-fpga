# A664: milan-fpga #773 (AAF talker capture-to-wire latency in the stamp, #770 regression)


## ROUND 2

Assignment: https://github.com/kebag-logic/milan-fpga/pull/779#issuecomment-6383506324, answering R689-1
(issuecomment-6383502557) and R690-1 (issuecomment-6383332748). Base head `13d8f1e8` confirmed; new commits on it, no
rebase or amend. Receipts: `receipts/round2/`. TAKEN not re-posted.

Head: `1b47a3dcff0cb65cb5cebe1f86327429a76f775d` (tree `f608aefd`), two commits on `13d8f1e8`.

**Status: REVIEW READY** at `1b47a3dc`, posted https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6384707314 (text `public-review-ready-round2.txt`). Every gate the round names passes
at that exact head, the complete four-shard sweep included (64 of 64 suites). No STOP condition met: every bound,
the start-up PDU's included, fits the 2 ms default (render-queue margin 492.1 us at 1x1, 487.0 us at 8x8). No RTL line
changed (the one `.sv` edit is comment-only), so no route ran: the round 1b Vivado receipts at `13d8f1e8` stand.
Nothing pushed.

| Commit | Subject |
|---|---|
| `e85f86a2` | State the listener-buffer and Equation (1) bounds for the start-up PDU stamped from the live PHC, this talker's 8 periods in the supported range, and the MAC-level figures (#773) |
| `1b47a3dc` | Name the outputs' whole-period capture-to-wire terms in the domain event's header comment (#773) |

| Item | Outcome |
|---|---|
| 1 F1 (R689-1-F1, R690-1-F1) bounds with the start-up PDU | done: grid-live and start-up bounds stated separately, both shapes; margins 492.1 / 487.0 us; supported range with this talker's 8 Ps; Equation (1)'s lead ceiling corrected too (237 -> 231.8 us, the same omission) |
| 2 F2 (R690-1-F2) the complete four-shard sweep at the final head | see the gate table |
| 3 R1 (R689-1-R1) the domain event's comment | done, the exact wording; identical after comment stripping (`receipts/round2/r1_comment_strip.txt`) |
| 4 S2 (R689-1-S2) MAC-level figures | done, derived: one frame ahead uses 12.3 us; what remains per output and shape; 100 Mb/s not covered. The derivation also finds the 8x8 CRF output not covered when the same frame takes the arbiters first (open risk below) |
| S1, S3 | not taken (optional); no RTL line changed, so no route |

### Changes (file:line at `1b47a3dc`; clause)

| File:line | Change | Clause / finding |
|---|---|---|
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1846-1862` | the MAC-level figures at 1 Gb/s beside "The MAC's own backpressure is outside the datapath": one maximum frame (12,336 ns) ahead at the MAC leaves 5,480 / 6,576 ns (AAF 1x1 / 8x8) and 8,167 / 2,990 ns (CRF); the same frame through the arbiters first (store-and-forward FIFO), with the other output's PDU between, delays the egress 16,208 ns (AAF) / 18,040 ns (CRF): 1,608 / 2,704 ns left for AAF, 2,463 ns for 1x1 CRF, the 8x8 CRF PDU up to 2,714 ns late; not covered: more than one frame ahead, the MAC's own crossing, 100 Mb/s (123,360 ns a frame) | R689-1-S2; IEEE 1722-2016 4.3.3 Eq. (1) |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1867-1870` | Equation (1)'s lower bound: the earliest hand-over is the start-up PDU's 106.9 us after its base, so the lead ceiling is 231.8 us (was 237 us, from the grid-live 112.3 us) | 4.3.3 Eq. (1); the F1 omission in a second place |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1872-1896` | "The listener's buffer": grid-live bound (2,038,676 / 2,054,392 ns) and start-up bound (5,343 cycles, 106,860 ns after the live-PHC base: 2,059,807 ns at both shapes, 184,807 ns at 125 us); last events and margins (start-up 492.1 / 487.0 us, grid-live 513.3 / 492.4 us); the nominal-rate condition | R689-1-F1, R690-1-F1; Milan v1.2 4.4.2.1 |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:2038-2048` | the supported range: a talker's lead is its timestamp less arrival; this device's talker adds 8 Ps: transit under 2,135,548 / 2,140,725 ns, offsets up to 2,489,452 / 2,484,275 ns plus the transit (first event), and 2,385,285 / 2,380,108 ns plus the transit for a whole six-event PDU | R689-1-F1 |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191` | row 5.3.7.6 / 4.4.2.1: grid-live (2,054,392 ns 8x8, 2,038,676 ns 1x1) and start-up (2,059,807 ns, the measured `[HOLD]` maximum) bounds | R689-1-F1, R690-1-F1 |
| `hdl/ieee1722/crf/KL_media_domain_event.sv:29-33` | header comment, R689-1-R1's exact wording (comment only) | R689-1-R1 |

### Recomputed figures (`receipts/round2/bounds.txt`)

`scripts/round2_bounds.py` reuses R690-1's `check_bounds.py` method (rational periods, the RTL's term formulas) and
requires each of the 40 figures the two pages state to equal its derivation, then requires every 2 ms `[HOLD]`
maximum in the sweep's own capture_coherence log to be at or below the stated start-up bound: 40/40 equal, 23 runs,
largest 2,059,807 ns = the bound. rc 0.

| Bound | 1x1 TDM8 | 8x8 TDM32 |
|---|---:|---:|
| earliest hand-over, grid live (after the frame's instant) | 127,991 ns | 112,275 ns (talker 0, age 0) |
| earliest hand-over, start-up (after the live-PHC base: 5,208 + 78 + 57 cycles) | 106,860 ns | 106,860 ns |
| lead at arrival, 2 ms, zero transit: grid live / start-up | 2,038,676 / 2,059,807 ns | 2,054,392 / 2,059,807 ns |
| last event after arrival: grid live / start-up | 2,142,843 / 2,163,974 ns | 2,158,559 / 2,163,974 ns |
| render-queue margin: grid live / start-up | 513.3 / 492.1 us | 492.4 / 487.0 us |
| supported range, this talker at 2 ms: transit under; offsets up to (first event; whole PDU) | 2,135,548 ns; 2,489,452 / 2,385,285 ns + transit | 2,140,725 ns; 2,484,275 / 2,380,108 ns + transit |
| Equation (1) lead ceiling (earliest hand-over + 125 us) | 231.8 us (start-up) | 231.8 us |

MAC level, 1 Gb/s, derived: a maximum tagged frame is 12,336 ns on the wire.

| Case | AAF 1x1 | AAF 8x8 | CRF 1x1 | CRF 8x8 |
|---|---:|---:|---:|---:|
| spare at the hand-over (round 1b) | 17,816 | 18,912 | 20,503 | 15,326 |
| left after one frame ahead at the MAC | 5,480 | 6,576 | 8,167 | 2,990 |
| left after the same frame through the arbiters first, the other output's PDU between (egress +16,208 AAF, +18,040 CRF) | 1,608 | 2,704 | 2,463 | **-2,714** |
| 100 Mb/s (123,360 ns a frame) | not covered | not covered | not covered | not covered |

### New checks (planted mutant, failing words)

None in the tree: the round changes documentation and one comment. The round's own checks are outside the tree:
`round2_bounds.py` (each stated figure equal to its derivation, and every measured 2 ms `[HOLD]` maximum at or below
the derived start-up bound). Planted control: the same script on the two pages as they stood at `13d8f1e8` (the round
1b text) fails, rc 1, "FAIL: 30 failure(s)": the start-up bound, its margins, the range with the 8 Ps, the Equation (1)
ceiling and the MAC figures are absent there (`receipts/round2/bounds_control_13d8f1e8.txt`). `strip_compare.py` (R1):
DIFFERENT raw, IDENTICAL after comment stripping.

### Resource before/after, route timing

No RTL line changed (`receipts/round2/r1_comment_strip.txt`), so no route ran (the assignment: route-1x1 only if an RTL
line changes). The round 1b receipts at `13d8f1e8` stand: route-1x1 LUT +102, FF +7, SLICE -11, RAM/DSP 0, WNS
+0.040 ns, WHS +0.021 ns; ooc-1x1 and ooc-8x8 equal to the record.

### Gate table (all at `1b47a3dcff0cb65cb5cebe1f86327429a76f775d`, tree `f608aefd`)

| Gate | Command | Result | Receipt (`receipts/round2/`) |
|---|---|---|---|
| full sweep, 4 shard units | `native-shards.py 773-a664 <spec> <out> 4 32-47 80-95 96-111 112-127` (`scripts/run_all_suites.sh <logs> --wait --shard k/4`, Verilator 5.050, CPython 3.12.13), 12:14-13:16 UTC | every shard runner rc 0; 64 of 64 suites PASS, each once (union equals `run_all_suites.sh --list`), 0 timed out; 2,190,887 checks, 0 in-suite failures; shard times 3,613 / 2,641 / 2,675 / 3,713 s. capture_coherence 20,832/0, dp 847/0, mutation arm 42/42; aaf-start 34,020/0, startup mutants 8/8 | `sweep/SUMMARY.txt`, `sweep/shard-*/`, `sweep/excerpts/`, `sweep/spec.json` |
| behave | `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps passed | `gates/behave.log`, `.rc` |
| lint | `python3 scripts/lint_rtl.py --check` | rc 0: PASS 89 <= 89 | `gates/lint.log`, `.rc` |
| docs gates (named) | `python3 scripts/docs_check.py`; `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check` (GNU Make 4.3, CPython 3.12.13) | rc 0 each | `gates/docs_named.log` |
| docs workflow | `scripts/docs_run.sh 1b47a3dc...` (the 44 gate steps literally, GNU Make 4.3) | 41 rc 0, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git body deletes .git), gate_8 rc 128 (a clone of the lane has no `dev` to fetch): run directly with base `a032c6d6`, rc 0, 0 findings over 198 added lines; builder leg 1 with the LiteX interpreter rc 0; no-git `docs_check.py` and `check_feature_status.py` rc 0 | `docs/` |
| R1 comment only | `python3 -I scripts/strip_compare.py <lane> 13d8f1e8 1b47a3dc hdl/ieee1722/crf/KL_media_domain_event.sv` | rc 0: identical after comment stripping | `r1_comment_strip.txt` |
| bounds | `python3 -I scripts/round2_bounds.py <clone> <sweep capture_coherence log>` | rc 0: 40/40 figures, 23 `[HOLD]` maxima <= 2,059,807 ns; the control on the `13d8f1e8` pages rc 1 (30 failures) | `bounds.txt`, `bounds_control_13d8f1e8.txt` |

### Open risks (for the manager)

- **8x8 CRF at the MAC.** The derivation finds one maximum frame that takes the arbiters just ahead of an 8x8 CRF PDU,
  with an AAF PDU between, delays that PDU's egress up to 2,714 ns past its timestamp less the applied offset
  (store-and-forward FIFO). It is outside the datapath boundary the ruling counts and outside the 2 ms fit, so no
  STOP; it is stated in the page as not covered. A second TC period at 8x8 (20,834 ns more) would cover it; that is a
  design choice for a new Issue, not this round.
- More than one maximum frame ahead is not bounded: the control gasket's 512 cycles (10.24 us) is under one maximum
  frame's 12.3 us on the wire. Derived only, nothing measured (S3 not taken).
- The supported-range paragraph adds the whole-PDU offset bound (2,385,285 / 2,380,108 ns plus the transit) beside
  the first-event figures the assignment gives: the range is per event, and a six-event PDU's last event is 5 Ps
  further ahead. It is a precision statement in the paragraph the round rewrites, not a behaviour change.

### Progress (UTC)

11:14 round 2 read (A10 assignment, R689-1, R690-1, both REPORTs' figures; HEAD `13d8f1e8` confirmed, origin
confirmed). 11:20-11:45 RTL checks for the start-up base (`aaf_tbase_w`, `live_o`), the MAC FIFO (`milan_soc.py`
`tx_sf` PacketFIFO, store-and-forward) and the CRF/AAF frame lengths; docs written; lane docs gates rc 0; commits
`e85f86a2`, `1b47a3dc`. 11:23 R1 comment-strip identity. 11:25 docs workflow started; lint, behave rc 0. 11:22-12:14
every CPU booked (another lane's four-shard sweep): the sweep waited for four free ranges (MemAvailable 50-55 GB).
12:14 sweep launched; 13:16 all four shards rc 0, 64/64. 13:20 receipts, bounds against the sweep's log (and the control on the `13d8f1e8` pages), index; HANDOFF and
PR-BODY (Round 2 section, Status claiming only what ran). 13:30 REVIEW READY posted (issuecomment-6384707314). Stopped.

---

## ROUND 1b

Assignment: https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380110812 (ruling (b): the AAF stamp is
M + (6 + 2) Ps + the offset as set; CRF adds Equation (14)'s TC as whole periods, 2 Ps at 1x1, 1 Ps at 8x8). Same
checkout and branch, base dev `a032c6d6`. TAKEN not re-posted. Receipts: `receipts/round1b/final/` (every gate at the
final head or at `bf2d96f9`, which differs from it only in `tb/verilator/aaf/start_mutants.py`), the earlier heads'
under `receipts/round1b/superseded/`. Index: `receipts/INDEX.md`.

**Head (committed, not pushed): `13d8f1e84920aac1dc3e76fb6406c44a744d8145`**, six commits on `a032c6d6`:

| Commit | Subject |
|---|---|
| `da079f3d` | Stamp the AAF talkers' crossing estimate and fixed delay, and the CRF output's Equation (14) TC, in whole periods derived from each path (#773) |
| `8a599554` | Document the talkers' capture-to-wire latency, its derived terms, its bounds and its proofs (#773) |
| `041b7922` | Count the talkers' hand-over with no frame ahead, as the #773 ruling does, so the compressed-clock test shapes still build |
| `9f9161d3` | Grade every output's hand-over at a 125 us offset in milan_dp's output walk too (#773) |
| `bf2d96f9` | Name the two enable bits without a unit and keep the new harness code to the C++ and Python idiom rules (#773) |
| `13d8f1e8` | Plant the aaf startup arm's offset-omitted defect at the stamp adder's offset term, which the #773 lead now follows |

**Status: REVIEW READY** at `13d8f1e8`, posted https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6382945476
(text `public-review-ready.txt`). Every gate passes (table below); no STOP condition met: route-1x1 SLICE -11
against the record (STOP above +10), the render queue holds the 2 ms default with 513.3 us (1x1) and 492.4 us (8x8) to
spare, every proof passes with its planted controls caught. Nothing pushed; the manager pushes and opens the PR.

| Item | Outcome |
|---|---|
| 1 AAF stamp | done: M + (6 + 2) Ps + the offset as set, the constant 166,667 ns in the existing stamp adder, derived per shape (2 periods of fixed delay at 1x1 and 8x8), refused above 125 us |
| 2 CRF stamp | done: TC 2 periods (41,667 ns) at 1x1, 1 (20,834 ns) at 8x8, a constant in the existing `ts_r` adder; Equation (14)'s round-up and the GET readback unchanged |
| 3 proofs | done at 1x1 on the wire and at the pins, at 2 ms and 125 us, with 7 planted controls; 4x4 and 8x8 entity legs at 2 ms, 1 ms, 2,010,000 ns and 125 us; 8x8 TDM32 derived (limit stated) |
| 4 gates | see the gate table |

### Changes (file:line at `13d8f1e8`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:104-122` | parameters `LEAD_P`, `FS_HZ_P`, `CLK_HZ_P`, `IN_LATE_NS_P` (off by default: other instances byte-identical) | Milan v1.2 5.3.7.6; IEEE 1722-2016 4.3.3 |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:237-265` | `PIPE_CYC_C` (its own pipeline, 4 + np + beats - 1, +3 for N > 1), `LATE_NS_C`, `DELAY_PER_C` (fewest periods covering it), `LEAD_NS_C` = ceil((6 + delay) Ps), refusal `g_lead_delay` above 125 us | 5.3.7.6 "between 0 and 125 microseconds"; 4.3.5 (whole periods) |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:783-785` | `tsw_val_r <= ptp + transit + 32'(LEAD_NS_C)`: the constant in the existing adder | 4.3.3 Equation (1) |
| `hdl/ieee1722/crf/KL_crf_tx.sv:140-153` | parameters `TC_P`, `CLK_HZ_P`, `EV_LATE_NS_P` (off by default) | IEEE 1722-2016 10.7 Equation (14) TC |
| `hdl/ieee1722/crf/KL_crf_tx.sv:302-317` | `PIPE_CYC_C` = NUM_BEATS + 1, `TC_PER_C`, `TC_NS_C` = ceil(TC x P) | 10.7 Equation (14) |
| `hdl/ieee1722/crf/KL_crf_tx.sv:543-544` | `ts_r <= ev_ns_i + mtt_ofs_r + TC_NS_C` | 10.7 Equation (14) |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:153-170` | `walk_pair_cyc()` (the capture walk), `age_max_cyc()` (the capture age) | (derivation) |
| `hdl/milan/milan_datapath.sv:1258-1291` | `CMAP_GAP_CYC_C`; the marker-latency localparams moved to their first reader (no change of value) | (derivation) |
| `hdl/milan/milan_datapath.sv:1461-1523` | the talkers' terms `TLK_*`; the packetizer bound with `LEAD_P` and its terms | 5.3.7.6, 4.3.3, 10.7 |
| `hdl/milan/milan_datapath.sv:7438-7443` | `KL_crf_tx` bound with `TC_P` and its term | 10.7 Equation (14) |
| `tb/verilator/capture_coherence/sim_dp.cpp` | CRF output on; `DP-CRF125-0..7` at 125 us (offsets poked into the processor's stored rows, `ptoff_public.vlt`); `[WIRE]`, `[GRID]`, `[HOLD]`; `[PIN]` less 8 periods | 4.3.3 Eq. (1), 10.7, 4.3.5, Milan 4.4.2.1 |
| `tb/verilator/capture_coherence/mutants.py:125-139, 272-293` | the 7 planted controls; `PIN_BAND` renamed | |
| `tb/verilator/milan_dp/sim_nxn.cpp` | output walk: Eq. (1) window [0, 125 us) replaces the old [-200, +30] us bounds; one whole number of periods per output; a 125 us step on every output | 4.3.3 Eq. (1), 4.3.5 |
| `tb/verilator/aaf/start_mutants.py:32` | the offset-omitted planting site follows the adder's new last term | |
| `tb/verilator/media_phase/ofs_wrap.sv` | comment: the lead and TC stay off where the rows are graded | |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` | new "The talkers' capture-to-wire latency"; the outputs' bullets | |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, `docs/testing/TESTING.md`, `CHANGELOG.md` | rows for 5.3.7.6 and 4.3.5/10.8; capture_coherence's checks; the changelog entry | |

### Derived figures (`receipts/round1b/final/derived_constants/`)

| Term | 1x1 TDM8 | 8x8 TDM32 | Test 2 MHz gmstep | Test 4 MHz mclk |
|---|---:|---:|---:|---:|
| span end to the last frame's close (marker latency - Ps) | 131 ns | -15,525 ns | 2,291 ns | 1,166 ns |
| capture age, cycles | 1,043 | 1,043 | 43 | 85 |
| walk to the last talker's last pair, cycles | 86 | 811 | 86 | 194 |
| packetizer, cycles | 57 | 60 | 57 | 60 |
| **hand-over after the estimate** | **23,851 ns** | **22,755 ns** | 95,291 ns | 85,916 ns |
| **fixed delay; lead** | **2 periods; 166,667 ns** | **2; 166,667 ns** | 5; 229,167 ns | 5; 229,167 ns |
| CRF path (marker + event register + 9 cycles) | 21,164 ns | 5,508 ns | 28,124 ns | 24,499 ns |
| **CRF TC** | **2 periods, 41,667 ns** | **1, 20,834 ns** | 2 | 2 |

End-to-end latency (capture at the pins to presentation at a listener): offset + 166,667 ns (291,667 ns at 125 us,
2,166,667 ns at 2 ms). Spare above the counted path: AAF 17,816 ns (1x1), 18,912 ns (8x8); CRF 20,503 and 15,326 ns,
which covers one frame ahead at the round-robin arbiters (3,960 ns for an AAF PDU, 4,400 ns for a CRF PDU).
Equation (1)'s lower bound holds for any lead up to the earliest hand-over plus 125 us (237 us; the lead is 166.7 us).
The listener's buffer at 2 ms, zero transit: a PDU arrives at most 2,038,676 ns (1x1) / 2,054,392 ns (8x8) before its
timestamp (Milan 4.4.2.1: 2.126 ms), its last event at most 2,142,843 / 2,158,559 ns, inside the render queue's
2,656,119 / 2,650,942 ns by 513.3 / 492.4 us.

Finding during the round: with the transmit-arbiter wait counted as a term (`8a599554`), the 2 MHz milan_dp gmstep
build was refused by the new guard (192,953 ns, 10 periods) and the 4 MHz milan_dp_mclk build would have been
(135,416 ns, 7). `041b7922` counts the hand-over with no frame ahead, as the ruling does; the shipping constants did
not move.

### New checks (planted mutant, failing words)

All in `tb/verilator/capture_coherence/mutants.py`, leg `dp` (the whole datapath, `--quick`), each caught by its named
check(s); the sweep's run at `bf2d96f9`: 42 checks, 42 PASS.

| Check (sim_dp.cpp) | Planted defect (milan_datapath.sv edit) | Failing words |
|---|---|---|
| `[WIRE]` AAF hand-over at or before avtp_timestamp - offset; `[GRID]` AAF; `[PIN]` | `.LEAD_P (1'b0)`: #770's stamp | "[WIRE] every AAF PDU's hand-over is at or before its avtp_timestamp less the presentation offset", "[GRID] every AAF stamp less its offset and 8 periods is a domain media event's instant", "[PIN] every slot's MSB pin instant, less its slot offset, is its AAF timestamp less the presentation offset and 8 periods, inside +/-5 % of Ps" |
| `[WIRE]` AAF, `[GRID]` AAF | `.IN_LATE_NS_P (TLK_AAF_IN_NS_C - 20834)`: 7 periods | the [WIRE] AAF and [GRID] AAF words above |
| `[WIRE]` AAF lower bound, `[HOLD]` | `.ptp_ns_i (aaf_tbase_w + 64'd125000)` | "[WIRE] ...and every AAF PDU's after it less TUmax, 125 us", "[HOLD] no AAF stamp is more than 2.126 ms after its hand-over" |
| `[WIRE]` CRF, `[GRID]` CRF | `.TC_P (1'b0)` | "[WIRE] every CRF PDU's hand-over is at or before its timestamp less the offset as applied", "[GRID] every CRF stamp less its offset applied and TC, 2 periods, is a domain media event's instant" |
| `[WIRE]` CRF, `[GRID]` CRF | `.EV_LATE_NS_P (TLK_CRF_EV_NS_C - 32'd20834)`: 1 period | the [WIRE] CRF and [GRID] CRF words above |
| `[WIRE]` CRF lower bound | `.ev_ns_i (dom_ns_w + 64'd125000)` | "[WIRE] ...and every CRF PDU's after it less TUmax, 125 us" |
| the refusal `g_lead_delay` | `.IN_LATE_NS_P (TLK_AAF_IN_NS_C + 125000)` | build refused: "exceeds the 0 to 125 us Milan v1.2 5.3.7.6 allows: refused" |

milan_dp's output walk (`sim_nxn.cpp`) adds per output and offset "#773 output N AAF/CRF at X ns: its hand-over is at
or before its timestamp less the offset, and after it less 125 us (IEEE 1722-2016 4.3.3 Eq. (1))" and "#773 output N
adds one whole number of periods to every stamp" (no planted control of its own: the capture_coherence controls plant
the same RTL defects).

Measured (capture_coherence dp leg, 31 runs, 1x1): AAF margin 17,823 to 59,807 ns (59,807 is a run's first PDU,
stamped from the live PHC before the grid is live); CRF margin 20,503 ns; [GRID] every graded stamp on a domain event;
[HOLD] max 2,059,807 ns at 2 ms. milan_dp 4x4 and 8x8 entity legs (100 MHz, audio clock 1:1): every output adds 8
periods (AAF) or 2 (CRF); AAF residual 98.6 to 114.7 us (4x4) and from 35.9 us (8x8), CRF 20,486 ns.

### Resource before/after, route timing

Against the eleventh record (#632, lane head `5282b8b6`; `syn/ooc/pp_resource_baseline.json` at `a032c6d6`),
`pp_resource_gate.py check` per endpoint, the recipe of `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged
(`--single-thread-synthesis`, `--integrated-clock`), one Vivado run at a time under the exclusive lock, in a clean
clone at `13d8f1e8` (`scripts/vivado_bank.sh`; RTL identical at `bf2d96f9`). Receipts: `receipts/round1b/final/vivado/`.

| route-1x1 | Record | `13d8f1e8` | Delta | Tolerance | Verdict |
|---|---:|---:|---:|---|---|
| LUT | 51,259 | 51,361 | +102 | +500 | ok |
| FF | 53,208 | 53,215 | +7 | +600 | ok |
| SLICE | 15,835 | 15,824 | -11 | +80 (assignment STOP above +10) | ok, below the record |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 | 0 | ok |
| WNS | +0.236 ns | +0.040 ns | -0.196 | floor +0.030, fall at most 0.25 | ok |
| WHS | +0.028 ns | +0.021 ns | -0.007 | floor 0 | ok |
| route status | | complete, no unrouted net, no routing error | | | ok |

route-1x1 ran 47.4 min (08:42-09:29 UTC), Vivado peak 8,196 MB. The gate's sub-block movements (not gated) are all
in the processor wrapper, whose RTL is unchanged: wrapper +117 LUT (`u_pp` +105, `u_pp/u_aecp` +82, `u_pp/u_srp`
+37, ...), so the rest of the image moved by -15 LUT. Placed cells of the touched blocks at the head (no per-block
figure exists at the record): `aaf_packetizer` 636 LUT / 1,332 FF, `crf_tx` 205 / 170, `media_domain_event` 13 / 79,
`chan_map_capture` 842 / 1,247. The critical setup path is the SoC's, outside the datapath: the AXI-Lite-to-Wishbone
bridge state to the SPI-flash PHY counter, 19 logic levels on the 10 ns clock (the class the #708 record named). The
datapath clock (20 ns) has 0.743 ns of slack, its worst path inside the processor (`u_talker` to `u_event_router`, 27
levels).

| ooc-1x1 | Record | `13d8f1e8` | Verdict |
|---|---:|---:|---|
| LUT / FF | 23,828 / 20,000 | 23,828 / 20,000 | equal |
| RAMB36 / RAMB18 / DSP | 16 / 3 / 8 | 16 / 3 / 8 | equal |

ooc-1x1 ran 13.6 min, peak 5,141 MB.

| ooc-8x8 | Record | `13d8f1e8` | Verdict |
|---|---:|---:|---|
| LUT / FF | 32,467 / 28,220 | 32,467 / 28,220 | equal |
| RAMB36 / RAMB18 / DSP | 21 / 5 / 8 | 21 / 5 / 8 | equal |

rtl-8x8 (the bound parameters) 1.1 min; ooc-8x8 25.4 min, peak 6,138 MB. Nothing re-recorded: the record stands.

### Gate table

Every command ran in its own clean clone of the lane at the head named (`scripts/make_clone.sh`), tools pinned:
Verilator 5.050 (CI's), CPython 3.12.13 (a venv with PyYAML, the hash-pinned markdown and hdl_reference requirements,
wavedrom 2.0.3.post3), GNU Make 4.3 for the docs gates, tsn-gen at CI's TSN_GEN_REV `deca300c`, Yosys 0.66 with sv2v
v0.0.12, Vivado 2026.1. `bf2d96f9` and `13d8f1e8` differ only in `tb/verilator/aaf/start_mutants.py`.

| Gate | Command | Head | Result | Receipt (`receipts/round1b/final/`) |
|---|---|---|---|---|
| derived constants | `scripts/elab_constants.sh` (scratch copies print the constants; lint-only) | `13d8f1e8` | 1x1 AAF 2 periods, CRF 2; 8x8 AAF 2, CRF 1; 2 MHz and 4 MHz test shapes 5 and 2, none refused | `derived_constants/` |
| full sweep, 4 shard units | `native-shards.py 773-a664 <spec> <out> 4 0-15 16-31 32-47 64-79` (`scripts/run_all_suites.sh --wait --shard k/4`) | `bf2d96f9` | 63 of 64 suites, 2,190,818 checks, 0 in-suite failures, 0 timed out; shard times 3,737 / 2,770 / 2,831 / 3,769 s. `aaf` FAILED: its startup arm's own control "offset omitted: expected one planting site" (the stale planting pattern; `13d8f1e8` fixes it) | `sweep/` |
| aaf alone | `scripts/suite_alone.sh aaf 13d8f1e8 1800` (`timeout 1800 make -C tb/verilator/aaf`, then `suite_tally.py --verdict`) | `13d8f1e8` | rc 0, verdict 0: aaf-start 34,020/0, startup mutants 8/8 (offset omitted caught), aaf 27/0, NxN 42/0 | `sweep/aaf_alone_13d8f1e8/` |
| capture_coherence (in the sweep) | suite default target | `bf2d96f9` | junction 20,832/0, dp leg 847/0, mutation arm 42/42 (the 7 new controls caught) | `sweep/excerpts/capture_coherence.txt` |
| milan_dp (in the sweep) | suite default target | `bf2d96f9` | every leg 0 failures (nxn8 3,998; nxn 2,100; base 2,098; ...) | `sweep/excerpts/milan_dp.txt` |
| media_phase, crf_tx, chmap_capture, milan_dp_gm_steps, tsn_fuzz (in the sweep) | suite default targets | `bf2d96f9` | all PASS; crf_tx 129/0; tsn_fuzz ran every campaign (677 pass, 0 fail in the gPTP field campaign) | `sweep/excerpts/` |
| Yosys | `syn/yosys/run.sh` | `bf2d96f9` | rc 0, 60/60 tops, tied-input and tap-purity PASS, 20.3 min | `yosys/` |
| lint | `python3 scripts/lint_rtl.py --check` | `13d8f1e8` | PASS 89 <= 89 | `lint.log` |
| Vivado front end | `python3 scripts/xvlog_gate.py --check` (under the lock) | `13d8f1e8` | PASS, 0 findings (hdl/ and the pinned processors) | `xvlog/` |
| docs gates | `scripts/docs_run.sh` (the docs workflow's 44 gate steps literally, GNU Make 4.3, CPython 3.12.13) | `bf2d96f9` | 41 rc 0, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git body deletes .git), gate_8 rc 128 (a clone of the lane has no `dev` to fetch): run directly with base `a032c6d6`, 0 findings over 149 added lines; builder leg 1 with the LiteX interpreter rc 0; markdown gates on 3.12.13 4/5 (gate_8 the same); no-git `docs_check.py` and `check_feature_status.py` rc 0 | `docs/` |
| docs at the head | `check_py_idiom.py` (+ `--selftest`), `docs_check.py` | `13d8f1e8` | rc 0 each | `docs/head_13d8f1e8_py_idiom_docs_check.txt` |
| tdm8render-mutants | `make -C tb/verilator/milan_dp_render tdm8render-mutants VERILATOR_JOBS=4` | `bf2d96f9` | rc 0, 31/31 PASS | `campaigns/tdm8render_mutants/` |
| pull-in | `make -C tb/verilator/milan_dp_render tdm8render-pullin PULLIN_JOBS=4 VERILATOR_JOBS=4` | `bf2d96f9` | rc 0, 19 legs (history + 18 phases), 0 failures | `campaigns/pullin/` |
| gmstep-mutants | `make -C tb/verilator/milan_dp_gm_steps gmstep-mutants VERILATOR_JOBS=4` | `bf2d96f9` | rc 0, 23/23 PASS (the 2 MHz shape builds: 5 periods) | `campaigns/gmstep/` |
| route-1x1 | `scripts/vivado_bank.sh 13d8f1e8 <sha>` (export, `pp_baseline.py --single-thread-synthesis`, `baseline_integrated.tcl`, `pp_resource_gate.py check --endpoint route-1x1`) | `13d8f1e8` | rc 0, gate PASS: LUT +102, FF +7, SLICE -11, RAM/DSP 0, WNS +0.040 ns, WHS +0.021 ns, route complete; 47.4 min, peak 8,196 MB | `vivado/route-1x1/` |
| ooc-1x1 | same bank (`--integrated-log` from the route, `--integrated-clock`) | `13d8f1e8` | rc 0, every figure equal; 13.6 min, peak 5,141 MB | `vivado/ooc-1x1/` |
| ooc-8x8 | same bank (8x8 export, RTL elaboration, `baseline_ooc.tcl`) | `13d8f1e8` | rc 0, every figure equal; 25.4 min, peak 6,138 MB | `vivado/ooc-8x8/` |

### Limits

- 8x8 TDM32 is derived only: no harness runs that shape at its clocks (the milan_dp 8x8 entity leg runs 100 MHz and a
  1:1 audio clock).
- The hand-over is the datapath's MAC transmit port, MAC ready; the MAC's own line-rate backpressure is outside.
- A frame ahead at the transmit arbiters is covered by the spare at both shipping shapes, not a derivation term.
- Bench prediction (not measured, no bench access): at 125 us, avtp_timestamp - wire time moves from -15.9..-10.2 us
  to about +150.8..+156.5 us.

### Progress (UTC)

 05:10-05:35 tests written; 05:44 first commits; 05:47 campaigns started at `8a599554`: the GM-step
build REFUSED by the new 125 us guard (its 2 MHz test clock: 192,953 ns with the arbiter term); 4 MHz `milan_dp_mclk`
would be refused too (135,416 ns). Fix `041b7922`: the arbiter wait is no derivation term (the ruling's 23.8/22.7 us
are MAC-ready, no frame ahead); shipping constants unchanged; gmstep 5 periods, mclk 5 periods, both build. Stale
campaigns at `8a599554` stopped and moved aside; 05:54 campaigns relaunched at `041b7922`; 06:01 Yosys and docs
started at `041b7922`.

06:04 milan_dp output walk at 125 us added (nxn 4x4 PASS, nxn8 3,998/0), committed `9f9161d3`; 06:22 Yosys PASS
60/60 at `041b7922`; docs gates restarted at `9f9161d3`; the Vivado bank (waiting on the lock, held by another lane)
stopped so it cannot run beside the sweep; 06:24 sweep refused by run_all_suites' preflight (the uv CPython 3.12.3
build lacks os.pidfd_open); a CPython 3.12.13 venv made; 06:25 the full sweep started as 4 shard units at `9f9161d3`
(CPUs 0-15, 16-31, 32-47, 64-79).

06:30-06:47 docs gates at `9f9161d3`: 5 steps failed (naming ratchet LEAD_P/TC_P; C++ idiom: 9 C-style casts and 2
multi-declarators in sim_dp.cpp, sim_nxn.cpp's grade_output_timestamps 127 lines; Python idiom: one 122-column line;
gate_8 cannot fetch `dev` in a clone of the lane, run directly: 0 findings; gate_25_1 needs the LiteX interpreter, run
in its own leg). Fixed in `bf2d96f9`; every one of those gates passes locally. The sweep, campaigns, Yosys and docs
restarted at `bf2d96f9` (06:50-06:55). The #632 lane's scratch tools vanished mid-run (archived): this lane now uses its
own CPython 3.12.13 venv (PyYAML, the pinned markdown requirements), a copy of GNU Make 4.3, tsn-gen built at CI's
TSN_GEN_REV `deca300c`, and a home linking the verified rv32 SDK. One sweep launch at 06:50 aborted in the runner's
own cancellation preflight under load (load average 41); relaunched 06:52, preflight passed.

07:40 the sweep's `aaf` failure read (its own arm's stale planting pattern); `13d8f1e8` fixes it; `aaf` alone PASS
at `13d8f1e8` (07:47-07:55). 07:55 sweep done (63/64 at `bf2d96f9`). 07:58 xvlog PASS. 08:22-08:41 campaigns done
(gmstep 23/23, pull-in 19 legs, tdm8render 31/31). 08:42-10:09 Vivado bank at `13d8f1e8` (route, ooc-1x1, rtl-8x8,
ooc-8x8), each gate PASS. 10:13 REVIEW READY posted (issuecomment-6382945476). Stopped.

Earlier: 04:58 round 1b read; 05:00-05:40 RTL and clause reading (GET keeps reading the offset: Milan v1.2
5.4.2.10.2 "the presentation time offset currently used", so TC and the AAF lead stay out of the readback);
05:45 derived constants printed by a scratch elaboration (`scripts/elab_constants.sh`, copies outside the tree).


---

# ROUND 1 record (kept as published)

**Status: STOP at item 1 (session 1, 2026-10-24 06:33 CEST onward).** The talker's capture-to-wire latency is above
125 us at both shapes, which is the assignment's item 1 STOP condition ("If it exceeds 125 us at a shape, STOP with the
figures"). Head `a032c6d6` = dev, branch `773-aaf-capture-to-wire-latency`, **no commits, nothing pushed**, tree clean.
STOP posted on #773: https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380097334 (text `public-stop.txt`). Items 2, 3 and 5 not started; item 4
answered with evidence only (no CRF change).

Assignment: https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6379902610
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6379920051 (text `public-taken.txt`).
Lane `$LANES/773-aaf-lead`, origin `https://github.com/kebag-logic/milan-fpga.git` (confirmed), branched
from dev `a032c6d6` (HEAD = `origin/dev` = merge-base). Submodules at the dev pins: protocol-processor `93fb0b2d`,
gptp-processor `55680bff` (no git command run inside a submodule of the lane).

## Items

| Item | Outcome |
|---|---|
| 1 derive the latency per shape, terms named | **Done: above 125 us at both shapes. STOP.** 1x1 133,110.7 to 143,690.7 ns at a settled lock (127,990.7 to 148,830.7 in any state); 8x8 117,394.7 (talker 0) to 142,594.7 ns (talker 7) at a settled lock (112,274.7 to 147,734.7 in any state). Measured at 1x1: 128,004 to 148,844 ns over 5,982 PDUs |
| 2 apply it in the stamping path | not started (STOP) |
| 3 prove at the wire and pins, planted controls | not started (STOP) |
| 4 CRF Equation (14) | answered, evidence only: the round-up adds 0 ns at 125 us (6 periods) and at 2 ms (96 periods), so it does not cover the CRF path (21.0 to 21.2 us at 1x1, 5.4 to 5.5 us at 8x8, from the stamped event to the hand-over); Eq. (14)'s TC term is the one for it and the RTL has none. Nothing changed |
| 5 gates | not run (STOP; no change to gate) |

## The derivation (item 1)

M = the instant the AAF talker stamps: `aaf_tbase_w` (`hdl/milan/milan_datapath.sv:7169`) = the crossbar's banked
instant of the walk's frame (`KL_chan_map_capture` `tdm_walk_ns_o`, from `KL_media_domain_event` `mark_ns_o`), latched
at the PDU's first pair (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv:728-735`). Hand-over = the PDU's last beat accepted at
`m_axis_mac_tx` (the datapath's MAC TX port); the first beat is 29 cycles earlier (30 beats at 8 channels). Both shapes
run the datapath at 50 MHz (`milan_clk_hz` in both configs). Script `scripts/derive_latency.py` evaluates every term
from the RTL's formulas; output `receipts/derivation/latency_a032c6d6.md`.

| Term | Set by (file:line at `a032c6d6`) | 1x1 TDM8 master | 8x8 TDM32 master on 98.304 MHz |
|---|---|---:|---:|
| A the PDU's five later frames | `KL_aaf_packetizer.sv:199` `SAMPLES_PER_FRAME_C` = 6; pend at the sixth sample's last pair `:720-725` | 5 Ps = 104,166.7 ns | 104,166.7 ns |
| B closing pair to the crossbar | `milan_datapath.sv:7125-7140` `DOM_MARK_LAT_NS_C` via `KL_media_if_latency_pkg.sv:129-133` | pair 3 of 4: 256 bit periods at 12.288 MHz (20,833) + 1 cycle at 24.576 MHz (41) + 4.5 cycles (90) = 20,964 ns | pair 3 of 16: 256 at 49.152 MHz (5,208) + 1 at 98.304 MHz (10) + 90 = 5,308 ns |
| C capture age, close to the walk's snapshot tick | aligner keep-off `milan_datapath.sv:7347-7349` (256 cycles of a 1041-cycle tick), `KL_media_grid_align.sv` LOCK TARGET; snapshot `KL_chan_map_capture.sv:1195`, `:1281-1296`; `docs/design/TIME_SYNC.md:528-529` | 256 to 785 cycles at a settled lock (5,120 to 15,700 ns); 0 to 1,042 before one | same |
| D walk, tick to talker t's last pair | `KL_chan_map_capture.sv:1385-1437` (IDLE, POP x (`LB_PAIRS_C` + 1), STEP, GAP x 25); `GAP_CYC_P` = 24 `:387`; `LB_PAIRS_C` `:526` with `milan_datapath.sv:1214-1215`; `N_SLOTS_P` `milan_datapath.sv:1272` | 4 + 4 + 26 x 3 = 86 cycles (LOOPBACK_P = 1, `LB_PAIRS_C` = 4) | 4 + 1 + 26 x (4t + 3) = 83 + 104t cycles (LOOPBACK_P = 0, `LB_PAIRS_C` = 1) |
| E packetizer, last pair to last beat | `KL_aaf_packetizer.sv:613-711`: grant, `E_CRD_S` 3 cycles for t > 0, `E_DRD_S` fetch 2 + np, `E_SEND_S` 30 beats | 4 + 24 + 29 = 57 cycles | 57 (t0), 60 (t > 0) |
| F arbiters | `milan_datapath.sv:8642` `crf_dp_mux`, `:8859` `adp_tx_mux`; `adp_tx_arbiter.sv:21` combinational grant | 0 with no other frame in flight and the MAC ready | 0 |

| Shape | Settled lock | Any state | Over 125 us |
|---|---:|---:|---|
| 1x1 | 133,110.7 to 143,690.7 ns | 127,990.7 to 148,830.7 ns | always: A + B = 125,130.7 ns before any pipeline term |
| 8x8 | 117,394.7 (t0) to 142,594.7 ns (t7) | 112,274.7 to 147,734.7 ns | talker 7 always (A + B + D = 125,694.7 ns); talker 0 above an age of 636 cycles |

Per-talker 8x8 rows are in the receipt. The packetizer is free when each 8x8 talker's PDU becomes pending (pends 104
cycles apart, a PDU takes 63), so no talker queues behind another unless the MAC stalls.

### Measured at 1x1 (corroboration)

Probe on a disposable local clone of `a032c6d6` (submodules from the lane's own module stores, same pins), in
`tb/verilator/capture_coherence` `make dp` (the shipping 1x1 TDM8 shape at 50 MHz through the whole `milan_datapath`,
`m_axis_mac_tx_tready` held 1). The probe (`scripts/probe_handover.py`, diff in the receipt) records, for every AAF
PDU at the MAC port, the PHC at the first and last accepted beat minus (avtp_timestamp - 2 ms). Run 2 separates the
PDUs below A + B (which cannot carry a domain-event base).

| Result | Value | Receipt |
|---|---|---|
| leg verdict with the probe | 447 checks, 0 failures, PASS (both runs) | `receipts/probe_1x1_a032c6d6/run2_make_dp.log` |
| domain-event-stamped PDUs, 23 runs | 5,982; last beat - M = **128,004 to 148,844 ns** (derived any-state 127,990.7 to 148,830.7: within one cycle) | `run2_probe_summary.txt` |
| per CRF lock phase (tail) | 130,324 to 148,544 ns across DP-CRF-0..7; e.g. DP-CRF-4 137,864..138,144 against about 138,021 derived for its age (tick 508 cycles after the fsync edge, the close 6.5 cycles after it: 501.5 cycles) | same |
| live-PHC fallback PDUs | one per run, PDU index 0: 106,860 or 106,880 ns = 5 tick spacings + 135 cycles, which fixes D (slot 0 to 3: 78 cycles) and E (57) to the cycle | `run1_probe_summary.txt`, `run2_probe_summary.txt` |
| bench (#773 body) | at 125 us the wire is 135.2 to 140.9 us after M; the ~32 us pre-#770 shift = B + ~11 us age | inside the 1x1 band |

The placed-engagement runs (DP-band-true) end inside the aligner's pull (up to 256 cycles at 64 ppm, about 80 ms; a run
is 31 ms), so their ages are below the settled band; that is why the measured minimum is under 133.1 us.
The 8x8 is derived only: `milan_dp` `nxn8` builds `LOOPBACK_P=1`, the default 100 MHz clock and a 1:1 audio clock
(`sim_nxn.cpp:677-686`), so it is not the shipping 8x8's timing.

## Item 4: CRF, evidence only

- `KL_mtt_round` rounds the CRF row up by Equation (14): 125,000 x 3 / 62,500 = 6 periods exactly, and 2,000,000 ns is
  96, so the ceiling adds 0 ns at both offsets (`receipts/derivation/latency_a032c6d6.md`, last section).
- `KL_crf_tx.sv:511` stamps `ev_ns_i` (the 96th domain event's instant, back-dated by B) + the rounded offset; the
  PDU's first beat is 3 cycles after the close and its last (8 beats) 10: hand-over - stamped event = 21,024 to 21,164
  ns (1x1), 5,368 to 5,508 ns (8x8), plus up to one AAF PDU in flight at `crf_dp_mux` (30 beats, 600 ns) and any
  control frame at `adp_tx_mux`.
- IEEE 1722-2016 10.7: the first CRF timestamp is offset from the transmit time plane by the Max Transit Time rounded
  up; Equation (14) TCRF = TS + ceil(TTmax / P) x P + TC, with TC "the amount of time that samples spend accumulating
  in the Talker's transmit buffer". The RTL adds no TC, so TCRF - hand-over = TTmax - 21 us at 1x1 at every
  whole-period offset (125 us and the factory 2 ms included). The issue's ~20 us CRF shift on the bench is B.

## Design constraint and options (published with the STOP)

Both outputs stamp instants of one frame grid plus their offsets, so a constant added to the AAF stamp keeps #770's
4.3.5 relation and IEEE 1722-2016 10.8's +/-5 % of Ps against the CRF timing points only if it is a whole number of
periods. 7 Ps (145,833.3 ns) covers both shapes' settled-lock maxima with 2.1 us at 1x1 for MAC-side interference;
8 Ps (166,666.7 ns, stamped 166,667) covers every state (148.8 us before a lock at 1x1) plus one maximum-size frame at
1 Gb/s (12.3 us). Equation (1)'s lower bound holds for any constant up to the earliest hand-over + 125 us (252.99 us at
1x1, 237.27 us at 8x8). Options: (a) owner exception to 5.3.7.6's 0 to 125 us, stamp M + 8 Ps + offset; (b) the same
stamp read as 5.3.7.6's two parts: crossing estimate M + 6 Ps (the end of the PDU's six-frame span), fixed delay 2 Ps
(41.7 us; worst hand-over 23.8 us past the estimate at 1x1, 22.7 us at 8x8); CRF alike with a whole-period TC (2 Ps
at 1x1, 1 Ps at 8x8). Recommendation (b). Not an option: shrinking the pipeline (1x1's A + B > 125 us), or a base
other than the frame instant (undoes #770's alignment).

For the implementer after a ruling (not done here): the constant can enter without a new adder in the AAF path by
folding it into the crossbar's banked instant (`milan_datapath.sv:1328`, `tdm_close_ns_i (dom_mark_ns_w[31:0])`) as a
32-bit constant add, or into the packetizer's existing stamp adder (`KL_aaf_packetizer.sv:733-734`); GET_STREAM_INFO
keeps reading `aecp_pres_offset` as set (`milan_datapath.sv:6249`). Neither was measured.

## Changes (file:line; clause)

None: no commit, the lane's tree is unchanged (`git status` clean at `a032c6d6`).

## New checks (planted mutant, failing words)

None in the tree. The probe is a disposable diagnostic outside the tree (`scripts/probe_handover.py`); it adds no check
and changes none.

## Resource before/after, route timing

Not measured: no RTL change (STOP at item 1). The eleventh record stands.

## Gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| derivation | `python3 -I scripts/derive_latency.py` | `a032c6d6` RTL | rc 0; figures above | `receipts/derivation/latency_a032c6d6.md` |
| 1x1 probe, run 1 | `make -C tb/verilator/capture_coherence dp VERILATOR_JOBS=8` on a clone with `probe_handover.py` (first version) | `a032c6d6` + probe | rc 0, 447 checks, 0 failures | `receipts/probe_1x1_a032c6d6/run1_*` |
| 1x1 probe, run 2 | same, with the fallback separation | `a032c6d6` + probe | rc 0, 447 checks, 0 failures; 5,982 PDUs 128,004..148,844 ns | `receipts/probe_1x1_a032c6d6/run2_*` |
| suites, sweep, Yosys, lint, docs, Vivado, campaigns | -- | -- | not run: STOP at item 1, nothing changed | -- |

Tools for the probe: Verilator 5.052 (the host's; a diagnostic, not a gate), `receipts/probe_1x1_a032c6d6/tool_versions.txt`.

## Progress (kept current)

- 04:34 UTC: HEAD `a032c6d6` = origin/dev, branch `773-aaf-capture-to-wire-latency`, tree clean; issue and assignment read.
- 04:35 UTC: TAKEN posted (issuecomment-6379920051).
- 04:36-04:44 UTC: RTL read (stamp, domain event, crossbar walk, aligner, packetizer, arbiters, CRF); clauses read
  (IEEE 1722-2016 4.3.3 Eq. (1), 4.3.5, 10.7 Eq. (14), 10.8; Milan v1.2 5.3.7.6, 5.4.2.9, 5.4.2.10.2). A + B at 1x1 is
  125,130.7 ns: the STOP condition holds at 1x1 from two elaboration constants.
- 04:45 UTC: `derive_latency.py` written and run (one off-by-one in E corrected before use: the first beat is 4 + np
  cycles after the last pair).
- 04:47 UTC: probe run 1 (1x1, 23 runs) PASS, every domain-event PDU above 125 us; 04:52 run 2 with the fallback
  separation: 5,982 PDUs, 128,004 to 148,844 ns.
- 04:53-04:56 UTC: STOP text, HANDOFF, PR-BODY and the receipts index written; STOP posted at 04:56 UTC (issuecomment-6380097334). Scratch clone and its build removed. Stopped.
