[A810] REVIEW READY
Commit: `4ceba3d40e3b94e9bda2407e64ef906c283b63a4` (`pf-948-1`, on the flip train's head `15168e14`; not pushed, the PR is the manager's to open)

Changed:
- `hdl/ieee1722/avtp/avtp_stream_parser.sv`: `match_vec_o`, every enabled table entry a PDU's stream_id matches. The highest index stays, for the APRB probe.
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`: a queued bundle holds the matched-and-bound vector, and the walker serves the one bundle to each context in turn. Each context gets its own format compare, sequence state, counters and accept. New for the depacketizer: an enqueue pulse one cycle after the match, and a done pulse with the accepting contexts. With one binding per stream the engine is cycle-equal to its reference.
- `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv`:
  - A frame is committed on the enqueue and read out of its one stored copy once per accepting input, tuser that input. A frame no input accepted is passed over.
  - Its own frame store (`axis_fifo` cannot read a frame twice) and a four-entry verdict queue.
  - A full store's drop counts for the frame's accepting inputs.
- `hdl/milan/milan_datapath.sv`: the wiring. The 5.3.8.7 stop gate on the done mask, input by input. The AAF clock meter sees the followed input's bit of the match vector.
- Tests below; the four test wraps; `tb_split_top.sv`'s `N_STREAMS_P` (default 1).
- Docs: `DATAPLANE_WALKTHROUGH.md`, `FPGA_DESIGN.md`, `TESTING.md`, the `milan_dp` and `milan_dp_mclk` READMEs.
- Not changed: the mailbox contract, the firmware, and every CPU budget image and bound.

Validation:
- Failing first (base RTL, then the head):
  - `make -C tb/verilator/avtp_rxmon fanout`, the stack at N=8, [FO1]-[FO10]: 118 of 239 failed, then 239 of 239 passed.
  - `sim_nxn` [FAN] on the 8x8 datapath (ACMP binds 4+6, then 7, unbind 4; FRAMES_RX, DEPKT tally, GET_COUNTERS): 11 of 4027 failed, then 0.
  - `make -C tb/verilator/milan_dp twin-fanout`, the twin's split half at 8x8/1if with the 8x8 split image's firmware: 8 failed (input 0 counted 0 of 4 beside input 1, the bench's case), then 0.
  - `milan_dp_mclk --shared`, each input its own media clock: the meter following input 0 never locked, then it locks on input 0 and on input 1.
- Planted defects: `fanout_mutants.py` 12 of 12 caught. `twin-fanout-plants` (the one-entry parser): 4 of 4 words. `milan_dp_mclk` 36 of 36, with mutant 19 (the parser's one index) and mutant 9 re-planted at the meter's new selection.
- The sweep, `run_all_suites.sh --shard k/4`, four units, at `c2e5e5bd`: 64 of 65 suites, 2,713,403 checks.
  - The one failure: `milan_dp_mclk`'s mutant 9 survived because the first wiring made the meter's compare redundant. Fixed in `09e78e41`, and that suite reran at `09e78e41`: 36 of 36.
  - Since `c2e5e5bd` the head changes RTL comments, the `milan_dp_mclk` files and the documentation inventory only.
  - The four declared `tsn_fuzz` skips. Its AAF campaign, which drives this depacketizer, ran with the generator: 164 pass, the results artifact fresh.
- The `avtp_rxmon` suite: lockstep 116 and 119 against the reference, all four campaigns.
- The twin, `twin-plants`, `twin-maps` and `twin-maps-plants`: `twin: 0 finding(s)`, every plant refused.
- The firmware gate (four shards), `fw_coverage --check`, `run.py --self-test`, the publication census: PASS.
- The 12 CPU budget images are byte-identical to the train's record at `15168e14`. The rows' checks print what the base prints: `flip_check`'s 8x8/2if rows are the base's, reported and not held.
- The docs workflow steps 104 of 104; `lint_rtl.py --check` 89 <= 89; `xvlog_gate.py --check` 0 findings; the Yosys gate on the three touched tops.
- Fit and timing at `e8a877a0` (the head's RTL but for comments): the gating recipe, #818's three directives, one Vivado at a time.

  | Point | Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | LUTs | FFs | Slices | BRAM tiles |
  |---|---|---|---|---:|---:|---:|---:|
  | 8x8/1if | ExtraPostPlacementOpt | +0.061 / +0.102 | +1.566 / +0.033 | 44,277 | 51,076 | 15,659 | 94 |
  | 8x8/1if | **ExtraTimingOpt** | **+0.332** / +0.100 | +1.641 / +0.036 | 44,291 | 51,076 | 15,431 | 94 |
  | 8x8/1if | AltSpreadLogic_high | +0.313 / +0.102 | +1.641 / +0.036 | 44,312 | 51,078 | 15,421 | 94 |
  | 1x1/1if | ExtraPostPlacementOpt | +0.085 / +0.102 | +1.660 / +0.028 | 32,543 | 42,660 | 13,671 | 79.5 |
  | 1x1/1if | **ExtraTimingOpt** | **+0.317** / +0.096 | +1.636 / +0.029 | 32,548 | 42,660 | 14,299 | 79.5 |
  | 1x1/1if | AltSpreadLogic_high | +0.201 / +0.096 | +1.636 / +0.029 | 32,524 | 42,661 | 14,285 | 79.5 |

  - #818's floor (WNS >= +0.030, WHS >= 0) is met at every corner on every build. No worst path is in the receive path.
  - Deltas against the train's gating builds (ExtraPostPlacementOpt):
    - 8x8/1if: LUTs +1,292, FFs +83, slices -39 (-267 at the best directive), BRAM -0.5 tile.
    - 1x1/1if: LUTs -171, FFs +32, slices -22, BRAM -0.5 tile.
  - The fan-out's own cost is in the touched modules: +151 LUT and +119 FF at 8x8, +141 LUT and +48 FF at 1x1, and one RAMB18 fewer at each.
  - The rest of the 8x8 LUT move is outside them, in `KL_mbx_cdc/u_edit` (+1,700) and `milan_datapath/csr` (-1,196), the attribution of one cross-boundary path's logic (8 threads here, 16 in the train's builds).

Acceptance criteria (#948's ruling of 2026-11-21):
- Fan-out, each input its own counters, media clock and render path: met. Counters: FRAMES_RX, the Table 5.6 set and GET_COUNTERS per input. Media clock: the meter on either input of a shared stream. Render path: each input's own copy, its own tuser, at the depacketizer's output.
- A failing test first, two then three inputs, an unbind leaving the others receiving: met, in the RTL suite, the 8x8 datapath and the twin.
- The RTL suites and the twin: met.
- The CPU service-budget rows unchanged: met (images byte-identical).
- Fit and timing at 1x1/1if and 8x8/1if, best of three: met. No STOP.

Open risks/questions:
- The CPU clock's margin moves between near-identical netlists. An intermediate head's route (`b9a88d25`, a three-bit mux on the meter's index, withdrawn in `09e78e41` so the routes above stand) gave Slow WNS +0.007 ns at ExtraTimingOpt on `KL_mbx`'s face registers (CPU clock, 79 % route), against +0.332 here. Not this lane's logic.
- The stricter both-+0.030 floor another lane's ruling used is met at 8x8. At 1x1 it is missed by 1-2 ps of Fast-corner hold (+0.028/+0.029) on unrelated paths (`KL_mbx_dma`; the monitor's unchanged legacy counter register into the CSR snapshot).
- The DEPKT drop tally now counts a full store's drop for the frame's accepting inputs, and a foreign frame's drop only in the total. It used to charge every drop to the last accepted index.
- Index 0's `0x800` PDUS word stays the shared depacketizer total (unchanged, noted in the `milan_dp` README).
