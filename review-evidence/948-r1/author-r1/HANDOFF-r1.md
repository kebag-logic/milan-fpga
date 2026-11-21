# HANDOFF r1, lane 948 ([A810])

STATUS (23:3x CET 2026-11-21): REVIEW READY at `4ceba3d4`. The RTL fix, its tests in the RTL suites, the 8x8 datapath
and the twin's split half, and every gate are done. The six routes (`e8a877a0`) and the sweep (`c2e5e5bd`) are of RTL
that equals the head's apart from comments; the one suite whose files changed after the sweep (`milan_dp_mclk`) was
rerun at the head. Posted: `[A810] TAKEN` (#948 issuecomment-7062093362) and `[A810] REVIEW READY`
(#948 issuecomment-7070284385, REVIEW-READY-comment.md). Nothing pushed, no PR opened (the manager's). No unit of this lane is
running.

Branch `pf-948-1` on the flip train's head `15168e14` (PR #945). Lane commits:

| Commit | What |
|---|---|
| `f3f4f7a6` | test first: `sim_fanout.cpp` + `make fanout`, the wrap's depacketizer taps (fails at the base, 91 of 176) |
| `755ed418` | test: sim_nxn [FAN] (window-bound version), sim_fanout [FO4] settle and [FO8] |
| `c4e6f7ed` | THE FIX: parser, monitor, depacketizer, datapath wiring, the four wraps, `fanout_mutants.py`, docs |
| `3171349a` | test: sim_nxn [FAN] binds over ACMP and reads GET_COUNTERS |
| `e8a877a0` | test: the twin's split half at 8x8/1if (`make twin-fanout`, `twin-fanout-plants`); THE ROUTED HEAD |
| `73f1113b` | docs gates: the evidence-reader disposition, the em dash on a touched row, the inventory |
| `63e0aa1a` | comment: the datapath's depacketizer banner |
| `f5b17cb4` | test: [FO9] and the two-entry verdict-queue plant |
| `35bcb1b7` | docs: TESTING.md for [FO9] |
| `c2e5e5bd` | test: [FO10] and the drop-attribution plant; THE SWEPT HEAD |
| `b9a88d25` | a mux on the AAF clock meter's index (superseded, section 7) |
| `09e78e41` | restores `e8a877a0`'s meter wiring; `milan_dp_mclk --shared`, mutant 19, mutant 9 re-planted |
| `4ceba3d4` | docs: the inventory for the mclk README |

## 1. Task and authority
- #948, the ruling of 2026-11-21 (issuecomment-7061889923): fan-out, not refusal. The receive parser delivers one
  PDU to every monitor context bound to its stream_id; each input its own counters, media clock and render path.
  STOP with the measured cost if 8x8/1if does not fit or close timing.
- Clauses: IEEE 1722.1-2021 8.2 (each sink binds on its own); Milan v1.2 5.3.8.10 and Table 5.6 (counters per
  Stream Input), 5.3.8.7 (a stopped input discards), 4.4.2.2 (an off-format PDU is discarded).

## 2. Cause (line numbers at `15168e14`)
- `hdl/ieee1722/avtp/avtp_stream_parser.sv:190-199`: the match loop keeps the highest matching enabled entry, one
  index (`match_index_o`).
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:430-432`: the engine queues the PDU for that one index; one verdict.
- `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:153-175`, `:237-263`: one accept pulse in the frame's flight commits
  the frame, and one index rides it as tuser.
- `hdl/milan/milan_datapath.sv:7480-7481`: the AAF clock meter took the same one index.
- So with inputs 0 and 1 bound to one stream every PDU went to input 1 only: reproduced at the base by all four new
  tests (section 5).

## 3. Design (smallest area: a match vector over the contexts, nothing copied per input)
- **Parser:** `match_vec_o`, every matching entry, registered with the existing outputs (8 FF at N=8).
  `match_index_o` stays for the APRB probe and the public tap.
- **Monitor:** the bundle ring keeps the matched-and-bound vector instead of an index; the walker serves the one
  bundle to each context in turn, lowest first (`rem_r`, `acc_r`), each with its own format compare, MON_STATE,
  counters and accept pulse. New outputs: `pdu_enq_p_o` (one cycle after the match: the PDU was queued) and
  `pdu_done_p_o` + `pdu_done_mask_o` (the queued PDU's accepting contexts). With a one-hot vector the engine is
  cycle-equal to its reference: lockstep N=1 (116) and N=8 (119) pass with the wrap feeding the index as one bit.
- **Depacketizer:** a frame is committed on the enqueue pulse (always in flight, earlier than the old accept), not
  on a verdict, because the verdicts of several contexts cannot all land before a frame's tlast. A four-entry
  verdict queue matches each enqueue to its frame's fate (committed, dropped full, or lost: the frame ended on the
  parser's match beat) and to its done mask. The read side waits for the mask, reads the one stored frame once per
  accepting input (tuser that input; each pass its own header pulse, so the render stage places each), and passes
  over a frame none accepted. The frame store is the module's own (axis_fifo cannot read a frame twice): {tlast,
  tdata}, the head frame's space freed after its last pass. A full store's drop is attributed to the frame's
  accepting inputs (DEPKT drops); a foreign frame's drop counts only in `drops_o`.
- **Datapath:** the 5.3.8.7 stop gate on the done mask, input by input (`avtprx_deliver_w`); the AAF clock meter
  sees a PDU when the followed input's bit is set in the match vector (`match_p_i`), with the followed index, so
  its index compare holds by construction there.
- **Downstream unchanged:** the route, the render queue, the loopback bucket and the latency taps see one PDU per
  receiving input, as if each input had its own stream.

## 4. Changes (file:line at `4ceba3d4`, reason)
- `hdl/ieee1722/avtp/avtp_stream_parser.sv:86` port `match_vec_o`; `:193-205` the vector beside the highest index;
  `:255` registered on the parse pulse. Banner `:12-24`.
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:139` `match_vec_i` (was `match_index_i`); `:179` `depkt_drop_mask_i`
  (was an index); `:221-223` the verdict protocol outputs; `:318-322` the ring's vector field and `rem_r`/`acc_r`;
  `:445-455` `mvec_w`, `lowest()`, `onehot()`; `:480-490` continuation first (`pcont_w`), dispatch only once a bundle
  is done, `iv_go_w` and `:501` the window read wait for it; `:508-512` the dispatched context; `:916` the enqueue
  pulse; `:981-989` dispatch and continuation; `:1060-1077` the done pulse and mask at the last context's verdict;
  `:952`, `:1128` drop attribution by mask.
- `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:79` `N_STREAMS_P`; `:94-101` `pdu_enq_p_i`, `pdu_done_p_i`,
  `pdu_done_mask_i` (were the accept pulse and index); `:133-135` `drop_mask_o`; `:140-178` the write-side
  enqueue attribution (the parser's eighth-beat rule); `:180-268` the frame store with its re-read; `:270-350` the
  verdict queue and the read side's queue; `:396-445` the passes and the read gate; `:515` the pass over a frame
  none accepted; `:564` the pass's index.
- `hdl/milan/milan_datapath.sv:7007` `avtprx_vec_w`; `:7315` parser; `:7484-7489` the clock meter; `:7872-7877`
  wires; `:7900-7906` `avtprx_deliver_w`; monitor and depacketizer instances; the depacketizer banner.
- Wraps: `tb/verilator/avtp_rxmon/avtp_rxmon_nx_wrap.sv` (vector, protocol, the depacketizer's taps),
  `avtp_rxmon_lockstep_wrap.sv` (one-bit vector for the engine, the reference's whole-index drop rule),
  `avtp_rxmon_wrap.sv` and `tb/verilator/aaf_audio_loop/aaf_audio_loop_wrap.sv` (the flat monitor's accept is its
  enqueue and done, mask 1); `tb/verilator/milan_dp/tb_split_top.sv:33`, `:344` `N_STREAMS_P` (default 1).
- Docs: `docs/fpga/DATAPLANE_WALKTHROUGH.md` rows 2b, 4, 5; `docs/fpga/FPGA_DESIGN.md` module rows;
  `docs/testing/TESTING.md` avtp_rxmon row; `tb/verilator/milan_dp/README.md` the twin fan-out section;
  `tb/verilator/milan_dp_mclk/README.md` the shared leg and mutants 9 and 19; `docs/DOCUMENTATION_AUDIT.md`
  regenerated; `scripts/measure_test_evidence_readers.py` the new driver.

## 5. New checks and their planted mutants
| Check | Holds | Base RTL | Head |
|---|---|---|---|
| `avtp_rxmon/sim_fanout.cpp` [FO1]-[FO10], N=8 (`make fanout`) | two, three, eight inputs on one stream; unbind; per-input format and sequence; two streams back to back; a frame none accepts; frames ending on the match beat, alone and three behind a committed PDU; a dense burst over the store, each accepted PDU delivered or the input's own drop | FAIL 118/239 | PASS 239/239 |
| `fanout_mutants.py` | 12 planted defects, each its named check | | 12 of 12 caught |
| `milan_dp/sim_nxn.cpp` [FAN], obj_nxn8 | ACMP binds 4+6, then 7, unbind 4; FRAMES_RX, DEPKT tally, GET_COUNTERS, the PCMRX total | FAIL 11/4027 (all [FAN]) | PASS 4027/4027 |
| `twin_split.cpp --fanout` (`make twin-fanout`), split half 8x8/1if | ACMP binds 0+1, then 2, unbind 1; GET_COUNTERS per input, each input's share | FAIL 8 (input 0 counts 0 of 4) | PASS |
| `make twin-fanout-plants` | the one-entry parser | | 4 of 4 words caught |
| `milan_dp_mclk --shared` | the meter locks on input 0, then input 1, of one shared stream | FAIL (AAFM_STAT 4: input 0 never locks) | PASS |
| `mclk_mutants.py` 19 and 9 | 19: the meter given the parser's one index; 9: the followed input's match bit ignored | | caught (36 of 36) |

`fanout_mutants.py`, each with the check that catches it:
1. parser: one entry per PDU (#948's defect): "[FO1] accept verdicts: input 0";
2. engine: a bundle served to its first context alone: "[FO1] accept verdicts: input 1";
3. engine: the done mask without the last context's accept: "[FO1] payloads reach ...: input 1";
4. engine: accepts carried into the next bundle: "[FO4] the 2-channel input: no payload: input 5";
5. depacketizer: no second pass: "[FO1] payloads reach ...: input 1";
6. depacketizer: a second pass under the first input: "[FO1] payloads reach ...: input 0";
7. depacketizer: a second pass from where the first ended: "[FO1] payloads equal ...: input 1";
8. depacketizer: a frame none accepted read out: "[FO7] the 8-channel PDU: payloads reach ...: input 0";
9. depacketizer: a frame read before its verdicts: "[FO6] payloads equal ...";
10. depacketizer: a lost PDU waits for its frame: "[FO8] only the full PDU reaches ...: input 0";
11. depacketizer: a two-entry verdict queue: "[FO9] only the three full PDUs reach ...";
12. depacketizer: a dropped frame counted for no input: "[FO10] every accepted PDU is delivered ... or one of its
    DEPKT drops".

## 6. Gate table
| Gate | Head | Result | Receipt |
|---|---|---|---|
| failing first (four tests) | base RTL | FAIL as above | receipts/failing-first/ |
| avtp_rxmon suite | `e8a877a0` tree, then the sweep | PASS (lockstep 116/119, all campaigns) | receipts/rtl/, sweep |
| milan_dp nxn8 | `3171349a` | PASS 4027/4027 | receipts/rtl/ |
| sweep, 4 shards (`run_all_suites.sh --shard k/4`) | `c2e5e5bd` | 64 of 65 suites; checks 2,713,403; the one failure `milan_dp_mclk` (mutant 9 survived: c4e6f7ed's wiring made the meter's compare redundant), fixed in `09e78e41`; declared skips: tsn_fuzz's 4 external-generator campaigns | receipts/sweep-c2e5e5bd/ |
| milan_dp_mclk (legs a, b, c and 36 cases) | `09e78e41` | PASS 36/36 | receipts/rtl/milan_dp_mclk-suite.* |
| tsn_fuzz AAF/AVTP campaign with the generator | `c2e5e5bd` | 164 pass, 0 fail; results artifact fresh | receipts/gates/ |
| twin, plants, maps, maps plant (1x1); twin-fanout and plant (8x8/1if) | `73f1113b` | PASS: twin 0 findings; every plant refused | receipts/twin/ |
| firmware gate, 4 shards | shard 0 at `73f1113b`, 1-3 at `c2e5e5bd` (no firmware input differs) | PASS | receipts/firmware/ |
| run.py --self-test, fw_coverage --check | `c2e5e5bd` | PASS | receipts/budget/long-checks.txt |
| publication census (`--check --selftest`) | `c2e5e5bd` | PASS (rerun at --jobs 3 after the first run hit its unit's 10 GB cap) | receipts/budget/ |
| CPU budget images (12) | `73f1113b` | byte-identical to the train's record at `15168e14` | receipts/budget/ |
| budget rows' checks (flip, load, shapes, rows_tiers, record classes, hot list, queued bound) | `73f1113b` | PASS; `flip_check` rc 1 identical to the base's (8x8/2if, reported, not held); `ci_tool_inventory --check` refuses alike at the base (CI image variable unset) | receipts/budget/ |
| docs workflow steps (104) | `09e78e41` + inventory recheck at `4ceba3d4` | PASS | receipts/gates/ |
| lint ratchet, xvlog gate | `4ceba3d4` | PASS 89 <= 89; PASS 0 findings | receipts/gates/ |
| Yosys gate, touched tops | `73f1113b` | PASS | receipts/gates/ |
| fit and timing | `e8a877a0` (RTL = head's but comments) | section 7 | receipts/fit/ |

## 7. Fit and timing
Recipe: the S12b gating lane's (`boot.sh`, `gprep.sh`, `gbuild.sh` from the train's gate15, only the scratch path
changed): the split boot simulation, the builder's split placement, the stand-in export, the flash map, the image
(`--interfaces 1`), then `milan_soc.py ... --eth-port e2 --synth-directive AreaOptimized_high --opt-directive
ExploreArea --place-directive <D> --build`, one Vivado at a time through `vivado-slot.sh`, 8 threads (the booked
range). Head built: `e8a877a0`; the head's RTL differs from it in comments only (`receipts/fit/rtl-since-the-routes-
and-the-sweep.txt`).

Floors: #818's gate (`docs/design/MARK_II_AREA_PLAN.md:64`), the best of the three placement directives at WNS >=
+0.030 ns and WHS >= 0 at every signoff corner, the same three directives as here. `signoff.py` (the train's copy)
also prints a stricter line, both >= +0.030, from another lane's ruling: every 8x8 build meets it; the three 1x1
builds miss it by 1-2 ps of Fast-corner hold (+0.028, +0.029, +0.029), on paths this lane does not change
(`KL_mbx_dma` on the CPU clock; the monitor's legacy counter register into the CSR snapshot, zero logic). The base
gating build's Fast hold was +0.036.

8x8/1if (`receipts/fit/8x8-*`):

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | #818 | Slice LUTs | Registers | Slices | BRAM tiles |
|---|---|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt | +0.061 / +0.102 | +1.566 / +0.033 | met | 44,277 | 51,076 | 15,659 | 94 |
| ExtraTimingOpt (best) | +0.332 / +0.100 | +1.641 / +0.036 | met | 44,291 | 51,076 | 15,431 | 94 |
| AltSpreadLogic_high | +0.313 / +0.102 | +1.641 / +0.036 | met | 44,312 | 51,078 | 15,421 | 94 |
| train gating, `8c5e2b4f`, ExtraPostPlacementOpt (16 threads) | +0.176 / +0.102 | +1.523 / +0.036 | met | 42,985 | 50,993 | 15,698 | 94.5 |

1x1/1if (`receipts/fit/1x1-*`):

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | #818 | Slice LUTs | Registers | Slices | BRAM tiles |
|---|---|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt | +0.085 / +0.102 | +1.660 / +0.028 | met | 32,543 | 42,660 | 13,671 | 79.5 |
| ExtraTimingOpt (best) | +0.317 / +0.096 | +1.636 / +0.029 | met | 32,548 | 42,660 | 14,299 | 79.5 |
| AltSpreadLogic_high | +0.201 / +0.096 | +1.636 / +0.029 | met | 32,524 | 42,661 | 14,285 | 79.5 |
| train gating, `8c5e2b4f`, ExtraPostPlacementOpt (16 threads) | +0.131 / +0.102 | +1.636 / +0.036 | met | 32,714 | 42,628 | 13,693 | 80 |

- **The fan-out's own cost** (placed hierarchy, ExtraPostPlacementOpt, against the train's gating build): 8x8 +151
  LUT and +119 FF (`aaf_rx_depkt` 209 -> 310 LUT, 143 -> 200 FF, one RAMB18 fewer; `avtp_rx_monitor` 2,071 -> 2,079,
  1,674 -> 1,715; `avtp_rx_parser` 462 -> 504, 645 -> 666); 1x1 +141 LUT and +48 FF, one RAMB18 fewer. The RAMB18:
  the store is {tlast, tdata}, 65 bits, where `axis_fifo` kept 74.
- **The totals:** 8x8 Slice LUTs +1,292, registers +83, slices -39 (-267 at the best directive), BRAM -0.5 tile;
  1x1 Slice LUTs -171, registers +32, slices -22, BRAM -0.5 tile. The 8x8 LUT move is outside the touched modules,
  `KL_mbx_cdc/u_edit` +1,700 and `milan_datapath/csr` -1,196 (the same at synthesis, +1,647 / -1,118): the attribution
  of one cross-boundary path's logic. The train's builds ran 16 threads, these 8. The 1x1 totals moving the other way
  say the same.
- **Worst paths:** none in the receive path. 8x8 Slow: `KL_mbx/u_rx` on the CPU clock (ExtraPostPlacementOpt), the
  audio-map edit path `KL_mbx_cdc/u_edit` -> `amap_edit_oclaim_expect` on the datapath clock (the base build's
  datapath-clock worst too). 1x1 Fast hold: as above.
- **The superseded route** (`receipts/fit/8x8-ExtraTimingOpt-b9a88d25-superseded/`): `b9a88d25` put a mux on the
  meter's index; its ExtraTimingOpt route gave Slow WNS +0.007 ns, below #818's floor, on `KL_mbx`'s face registers on
  the CPU clock (79 % route delay), where `e8a877a0`'s ExtraTimingOpt gave +0.332 on the same clock. Rather than
  re-route five directives and re-sweep for a three-bit mux, `09e78e41` restored `e8a877a0`'s wiring, so the six
  routes stand for the head's RTL. The run shows how far the CPU clock's margin moves between near-identical
  netlists (the base's worst path is in `KL_mbx` too).

## 8. Open questions / STOP conditions
- No STOP: 8x8/1if fits and closes timing on all three directives (best +0.332 ns), as does 1x1/1if (best +0.317).
- The CPU clock's margin: the `b9a88d25` run fell to +0.007 ns on an unrelated mailbox path. Not this lane's
  logic, but a reason the hosted gate's own route (and the next lane touching the datapath) may land anywhere in
  that band.
- The stricter both-+0.030 floor at 1x1 Fast hold (1-2 ps short on unrelated paths) if that ruling applies here;
  #818's gate is met.

## 9. Posting
- `[A810] REVIEW READY`: REVIEW-READY-comment.md, posted on #948 as issuecomment-7070284385 (23:4x).
- `PR-BODY.md`: base `dev-soft-core`, `Closes #948`, `Relates to #665`. The manager pushes and opens the PR.
- Scratch (not in this packet): the lane's scratch directory (clones `c-head`, `c-base`, the Vivado work trees,
  the sweep clones under the lanes directory `948a810-shard0..3`). No unit of this lane is running.
