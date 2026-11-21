[A810]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN. Every gate below passes. `pf-948-1` -> `dev-soft-core`, on the flip train's head `15168e14` (PR #945): once
the train merges, this PR's diff is this lane's commits only.

- **The failing tests first, then the fix:** `sim_fanout` 118 of 239 failed at the base RTL, then 239 of 239 passed;
  sim_nxn [FAN] 11 of 4027 failed, then 0; `twin-fanout` 8 failed, then 0; `milan_dp_mclk --shared` failed (the meter
  following input 0 never locked), then passed.
- **Planted defects:** 12 of 12 caught (`fanout_mutants.py`); the twin's one-entry plant, 4 of 4 words caught;
  `milan_dp_mclk` 36 of 36, its new mutant 19 among them.
- **The other suites:** the `avtp_rxmon` suite (the lockstep leg against the reference at N=1 and N=8 among it); the
  twin, its plants and its maps leg (`twin: 0 finding(s)`); the firmware gate (four shards); `fw_coverage --check`;
  the docs workflow steps (104 of 104); the lint ratchet; the Vivado front end (`xvlog_gate.py`); the Yosys gate on
  the touched tops.
- **CPU budget:** the twelve CPU budget images are byte-identical to the train's record, and the rows' checks print
  what the base prints.
- **Fit and timing:** both points meet #818's gate at every corner on all three directives.
  - 8x8/1if best: ExtraTimingOpt, Slow WNS +0.332 / WHS +0.100 ns.
  - 1x1/1if best: ExtraTimingOpt, Slow WNS +0.317 / WHS +0.096 ns.
- **Sweep (4 shards, `c2e5e5bd`):** 64 of 65 suites, 2,713,403 checks.
  - The one failure, `milan_dp_mclk`'s mutant 9 surviving: the first wiring made the AAF clock meter's compare
    redundant. Fixed in the mutant's plant site (`09e78e41`), and `milan_dp_mclk` reran at the head: 36 of 36.
  - Since `c2e5e5bd` the head changes RTL comments, the `milan_dp_mclk` files and the documentation inventory only.
  - Declared skips: `tsn_fuzz`'s external-generator campaigns. The AAF one, which drives this depacketizer, ran
    separately with the generator: 164 pass, its results artifact fresh.

## Linked Issue / roles

Closes #948
Relates to #665

Executor: `[A810]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

**The defect (#948).** With two of the entity's STREAM_INPUTs bound to one talker stream, the first stopped
receiving. IEEE 1722.1-2021 8.2 lets each sink bind on its own, so one stream_id can be the source of several inputs.
The receive parser's match loop kept the highest matching table entry, one index
(`hdl/ieee1722/avtp/avtp_stream_parser.sv:190-199` at the base). The monitor queued and judged the PDU for that one
context, and the depacketizer committed the frame on that one accept and tagged it with that one index. So every PDU
went to the input with the higher index, and the AAF clock meter took the same one index. The four new tests reproduce it at the base RTL. The twin's split half at
8x8/1if shows input 0 counting 0 of 4 PDUs beside input 1, as the bench found.

**The fix: one PDU to every bound input, nothing copied per input** (#948's ruling of 2026-11-21: fan-out, not
refusal).

| Piece | Change |
|---|---|
| `avtp_stream_parser.sv` | `match_vec_o`: every enabled entry the stream_id matches, registered with the parse pulse. `match_index_o` stays (the APRB probe, the public tap). |
| `KL_avtp_rx_monitor_ctx.sv` | `match_vec_i` replaces the index. A bundle in the PDU ring holds the matched-and-bound vector, and the walker serves that one bundle to each context in turn, lowest first. Each context gets its own format compare, MON_STATE, counters, tv tallies and accept pulse. New outputs for the depacketizer: `pdu_enq_p_o`, one cycle after the match (the PDU was queued), and `pdu_done_p_o` with `pdu_done_mask_o`, the contexts that accepted it. `depkt_drop_mask_i` replaces the drop index. With one binding per stream the engine is cycle-equal to its reference (the lockstep leg at N=1 and N=8). |
| `KL_aaf_rx_depacketizer.sv` | A frame is committed on the enqueue pulse, not on a verdict: the verdicts of several contexts cannot all land before a short frame's tlast. A four-entry verdict queue matches each enqueue to its frame's fate (committed, dropped by a full store, or lost because the frame ended on the parser's match beat) and to its done mask. The read side waits for the mask, reads the one stored frame once per accepting input (tuser that input, a header pulse per pass), and passes over a frame no input accepted. The frame store is the module's own, since `axis_fifo` cannot read a frame twice: {tlast, tdata}, the head frame's space freed after its last pass. A full store's drop counts in the DEPKT drops of the frame's accepting inputs. |
| `milan_datapath.sv` | The wiring. The Milan v1.2 5.3.8.7 stop gate is applied to the done mask input by input (`avtprx_deliver_w`), so a stopped input's share is discarded and the others receive. The AAF clock meter sees a PDU when the followed input's bit is set in the match vector, whichever other inputs share the stream, with the followed index (one index cannot name several matches), so its own index compare holds by construction here. |
| Unchanged | The route, the render queue, the loopback bucket and the latency taps: they see one PDU per receiving input, as if each input had its own stream. The mailbox contract, the firmware and every CPU budget image. |

**Tests, failing first** (base RTL, then the fix):

| Test | Holds | Base | Fix |
|---|---|---|---|
| `tb/verilator/avtp_rxmon/sim_fanout.cpp` [FO1]-[FO10] (`make fanout`, the receive stack at N=8) | two, three and eight inputs on one stream, each receiving every payload byte for byte under its own index and counting it; an unbind leaves the others receiving; each input judges the one PDU against its own format and counts a gap on its own; two streams back to back; a frame no input accepts; frames that end on the match beat, alone and three behind a committed PDU; a dense burst that overflows the frame store, each accepted PDU delivered or counted as the input's own drop | FAIL, 118 of 239 | PASS, 239 of 239 |
| `fanout_mutants.py` | twelve planted defects across the parser, the engine and the depacketizer, each failing its named check | | 12 of 12 caught |
| `tb/verilator/milan_dp/sim_nxn.cpp` [FAN] (the 8x8 datapath, obj_nxn8) | a controller binds inputs 4 and 6 to one talker over ACMP, then 7, then unbinds 4; FRAMES_RX, the DEPKT tally, GET_COUNTERS and the shared total per round | FAIL, 11 of 4027 (all [FAN]) | PASS, 4027 of 4027 |
| `twin_split.cpp --fanout` (`make twin-fanout`: the twin's split half at 8x8/1if with the 8x8 split image's firmware) | the bench's case through the split firmware's ACMP and AECP: inputs 0 and 1, then 2, then 1 unbound; GET_COUNTERS per input and each input's share of the depacketizer's output | FAIL, 8 (input 0 counts 0 of 4) | PASS |
| `make twin-fanout-plants` | the same binary on the one-entry parser | | 4 of 4 words caught |
| `tb/verilator/milan_dp_mclk/sim_mclk.cpp --shared` (the 2-stream TDM8 root) | each input its own media clock: AAF input 1 bound to AAF input 0's stream as well; the meter locks on input 0, then on input 1 | FAIL (input 0 never locks) | PASS |
| `mclk_mutants.py` 19, 9 | 19: the meter given the parser's one index; 9 re-planted at the selection's new place, the followed input's match bit ignored | | caught, 36 of 36 |

The twin's own shape, 1x1, has one AAF Stream Input, and the twin compares two placements of one datapath, so the
comparison itself cannot see a defect inside that datapath. The twin fan-out leg grades the split half on its own at
8x8/1if.

**Fit and timing** (the gating recipe, `--eth-port e2`, synthesis AreaOptimized_high, opt ExploreArea, each of
#818's three placement directives; #818's gate is WNS >= +0.030 ns and WHS >= 0 at every signoff corner):

| Point | Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Slice LUTs | Registers | Slices | BRAM tiles |
|---|---|---|---|---:|---:|---:|---:|
| 8x8/1if | ExtraPostPlacementOpt | +0.061 / +0.102 | +1.566 / +0.033 | 44,277 | 51,076 | 15,659 | 94 |
| 8x8/1if | **ExtraTimingOpt** | **+0.332** / +0.100 | +1.641 / +0.036 | 44,291 | 51,076 | 15,431 | 94 |
| 8x8/1if | AltSpreadLogic_high | +0.313 / +0.102 | +1.641 / +0.036 | 44,312 | 51,078 | 15,421 | 94 |
| 8x8/1if | the train's gating build, ExtraPostPlacementOpt | +0.176 / +0.102 | +1.523 / +0.036 | 42,985 | 50,993 | 15,698 | 94.5 |
| 1x1/1if | ExtraPostPlacementOpt | +0.085 / +0.102 | +1.660 / +0.028 | 32,543 | 42,660 | 13,671 | 79.5 |
| 1x1/1if | **ExtraTimingOpt** | **+0.317** / +0.096 | +1.636 / +0.029 | 32,548 | 42,660 | 14,299 | 79.5 |
| 1x1/1if | AltSpreadLogic_high | +0.201 / +0.096 | +1.636 / +0.029 | 32,524 | 42,661 | 14,285 | 79.5 |
| 1x1/1if | the train's gating build, ExtraPostPlacementOpt | +0.131 / +0.102 | +1.636 / +0.036 | 32,714 | 42,628 | 13,693 | 80 |

- **The fan-out's own cost** is in the three touched modules (placed hierarchy, ExtraPostPlacementOpt, against the
  train's gating build at the same directive):
  - 8x8/1if: +151 LUT and +119 FF. `aaf_rx_depkt` 209 -> 310 LUT, 143 -> 200 FF, one RAMB18 fewer. `avtp_rx_monitor`
    2,071 -> 2,079 LUT, 1,674 -> 1,715 FF. `avtp_rx_parser` 462 -> 504 LUT, 645 -> 666 FF.
  - 1x1/1if: +141 LUT, also one RAMB18 fewer.
  - The RAMB18: the frame store keeps {tlast, tdata}, 65 bits, where `axis_fifo` kept 74.
- **The totals against the train's gating build:**
  - 8x8/1if: Slice LUTs +1,292, registers +83, slices -39 (and -267 at the best directive), BRAM -0.5 tile.
  - 1x1/1if: Slice LUTs -171, registers +32, slices -22, BRAM -0.5 tile.
  - The 8x8 LUT move sits outside the touched modules, in `KL_mbx_cdc/u_edit` (+1,700) and `milan_datapath/csr`
    (-1,196), the attribution of one cross-boundary path's logic. The train's builds ran 16 threads, these 8.
- **No worst path is in the receive path.**
  - 8x8 Slow corner: `KL_mbx/u_rx` on the CPU clock, or the audio-map edit path on the datapath clock (the base
    build's datapath-clock worst too).
  - 1x1 Fast-corner hold: `KL_mbx_dma`, or a zero-logic hop from the monitor's legacy counter register (unchanged)
    into the CSR snapshot.

## Authoritative references

- IEEE 1722.1-2021 8.2: each sink binds on its own, so one stream_id can be the source of several Stream Inputs.
- Milan v1.2 5.3.8.10 and Table 5.6: the counters of each Stream Input, on the PDUs "received on this Stream Input".
- Milan v1.2 5.3.8.7: a stopped Stream Input discards the PDUs it receives.
- Milan v1.2 Table 5.6 and 4.4.2.2: a PDU not in the input's current format counts UNSUPPORTED_FORMAT and is discarded.
- #948's ruling of 2026-11-21: fan-out, not refusal.

## How to get into the same state

```sh
git fetch origin && git checkout <this PR's head>
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
# Verilator 5.050 (the CI image's), sv2v v0.0.12 and Yosys on PATH; the RV32 SDK for the firmware gate
```

## How to validate

```sh
# the receive stack at eight contexts: the fan-out leg and its twelve planted defects (also in `make` of the suite)
make -C tb/verilator/avtp_rxmon fanout && (cd tb/verilator/avtp_rxmon && python3 fanout_mutants.py)
# the whole receive-stack suite, the lockstep leg against the reference among it
make -C tb/verilator/avtp_rxmon
# the 8x8 datapath with the [FAN] section
make -C tb/verilator/milan_dp build-nxn8 exec-nxn8
# the twin's split half at 8x8/1if, and its plant
make -C tb/verilator/milan_dp twin-fanout twin-fanout-plants
# the media clock at the root, the shared-stream leg and the 36 cases among it
make -C tb/verilator/milan_dp_mclk
# the twin itself and its plants (1x1), unchanged
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
# the sweep, the lint ratchet, the Vivado front end
bash scripts/run_all_suites.sh <logs> --wait
python3 scripts/lint_rtl.py --check && python3 scripts/xvlog_gate.py --check
```

Expected result / pass criteria: `FANOUT N=8: 239 checks, 0 failures`; `13 checks: 13 PASS, 0 FAIL` for the
mutants; `checks: 4027 failures: 0` for obj_nxn8; `fanout: 0 failed` and `caught:` for each of the four plant words;
`36 checks: 36 PASS, 0 FAIL` for `milan_dp_mclk`; `twin: 0 finding(s)`; every sweep suite PASS; the lint and xvlog
gates PASS.

## Known limitations / out of scope

- **Throughput is the same totals as distinct streams, not more.** The engine walks each bound context once per PDU
  and the depacketizer reads one pass per receiving input, so a PDU bound to k inputs costs what k distinct streams'
  PDUs cost. A dense burst beyond the engine's ring (two waiting PDUs) is refused there as before, and one beyond the
  2 KB store is dropped whole and counted (each accepting input's DEPKT drop). At the Class A interval neither limit
  is near: [FO6] and [FO10] measure them.
- **The DEPKT drop tally's meaning moved.** Before, every frame the full store dropped was counted against the last
  accepted stream index, including frames of no stream. Now a frame the full store drops counts in the drop tally of
  each input that accepted its PDU, and a foreign frame's drop only in the depacketizer's total (`PCMRX_CNT`).
- **The CPU clock's margin moves between runs.** A route of an intermediate head (`b9a88d25`, a three-bit mux on the
  meter's index, since withdrawn) gave Slow WNS +0.007 ns at ExtraTimingOpt, below #818's floor, on `KL_mbx`'s face
  registers on the CPU clock, where `e8a877a0`'s gave +0.332 on the same clock. The base's worst path is in `KL_mbx`
  too. Not this PR's logic, but the band a later route can land in.
- **Input 0's PDUS window word stays the shared total.** The `0x800` window's index-0 PDUS word is the flat alias of
  `PCMRX_CNT` (`milan_csr`'s index-0 snapshot), every PDU the depacketizer emits for any input. With fan-out that total
  counts each receiving input's copy; inputs above 0 read their own tally. Unchanged by this PR, and noted in the
  `milan_dp` README.
- **A frame now enters the store before its verdict.** A PDU no input accepts (another format at every bound input)
  is committed and passed over by the read side, where it used to be dropped at its tlast. The output is the same;
  the store holds it until the read side reaches it.

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
