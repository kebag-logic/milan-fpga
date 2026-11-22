[A810] REVIEW READY
Commit: `64e55a59e09339114926c2600056c3ad8b33b9b4` (`pf-948-1`, round 2b on round 2's `e8252323`; not pushed, the manager pushes)

Answers the manager's ruling of 2026-11-22 on round 2's new scope: frames of ten beats or fewer were counted in
FRAMES_RX and never delivered, so a 1-channel 48 kHz Base stream rendered nothing. It is fixed in this PR. Round 2's
answers to R878-1 and R877-1 stand (issuecomment-7075385669); their evidence is rerun at this head below.

Measured first, at each revision through its own receive stack (`probe_minframe2.cpp`, input 0, 3 PDUs per length):
- At `15168e14` (the true base), the shortest delivered frame is 98 octets (13 beats). Milan's 2-channel 48 kHz frames
  (86 octets) and 1-channel ones (62, 66 tagged) were never delivered.
- At `4ceba3d4` (round 1) and `e8252323` (round 2), the shortest is 82 octets (11 beats). Round 1's enqueue commit made
  2-channel streams deliverable, so it changed the behaviour for the better, but 1-channel was still never delivered.
- At this head, every length from the Ethernet minimum up is delivered, tagged and untagged, the 1-channel 48 kHz Base
  frames included.
- The cause, at every revision: the monitor's enqueue pulse lands exactly three cycles after the tap carries a frame's
  eighth beat (the parser's input register, its registered match, the monitor's registered pulse). The depacketizer
  dropped a frame at its tlast unless that pulse had come, so a frame of eight to ten beats was gone before it. Before
  #948 the commit waited for the still later accept pulse.

Changed:
- `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv`:
  - The store's write side runs `ENQ_LAT_C` = 3 cycles behind the tap.
  - The tap's own beat count names each pulse's frame, the one that passed its eighth beat last (`taw_r`, `tq_r`,
    `te_r`).
  - Each frame's verdict is taken when its eighth beat reaches the write side, a pulse in that same cycle included.
    That is on or before its tlast, however short the frame.
  - An unqueued frame is still dropped at its tlast. Nothing else changes: the off-format discard in the monitor, the
    whole-payload check, the tail.
- Tests:
  - `sim_fanout` [FO14].
  - `sim_depkt` [DT4], with the bench's pulse now scheduled from the eighth beat at a chosen latency.
  - `sim_nxn` [FAN]: inputs 6 and 7 at one channel.
  - [FO8]: the cut 64-octet frame is now a DEPKT drop, as [FO13]'s frames are.
- Mutants: `depkt_mutants.py` +4 (11). `fanout_mutants.py` +2, and the round-1 "lost PDU" mutant re-anchored to its
  analogue in this design (21).
- Docs: the walkthrough's depacketizer row, `FPGA_DESIGN.md`, `TESTING.md`'s `avtp_rxmon` row, the `milan_dp` README,
  the evidence dispositions, the inventory.

Validation (failing first on `e8252323`'s RTL, the tests commit `0b4517c3`, then the head):
- `sim_fanout`: 236 of 1,205 failed (FO14 234; FO8's new drop check 2; FO1-FO13 pass), then 1,205 of 1,205. [FO14]:
  - Payloads of 2-42 octets in one channel of INT_16BIT, INT_24BIT or INT_32BIT, the Milan 1-channel 48 kHz Base
    format among them. Every remainder, untagged and tagged.
  - Frames of 8, 9 and 10 beats, two back to back (the second starts inside the first's three cycles), to two
    inputs, with another stream's PDU to a third input between them.
  - PDUs off the inputs' frame size, one octet each way, in equally short frames: discarded whole and counted as
    UNSUPPORTED_FORMAT.
- `sim_depkt`, at no payload lead and at the datapath's 16:
  - `e8252323`'s RTL: 3,077 of 5,750 failed at each lead. [DT4] had 192 of 960 cases whole, and no frame for the
    1-channel PDU, untagged or tagged.
  - The head: 374 of 374 at each lead.
- `sim_nxn` (obj_nxn8): 6 of 4,073 failed, then 4,073 of 4,073. The failures were the 1-channel rounds: FRAMES_RX
  counted every PDU, DEPKT tallies 0.
- Plants re-breaking the short-frame path, each caught by name:
  - The store taking the tap as it comes: [DT4] and [FO14].
  - A pulse taken only while its frame is still on the tap: [DT4] and [FO14] 28 octets.
  - A same-cycle pulse missed, and a two-cycle lag: [DT4]'s 1-channel PDU.
  - The re-anchored mutant: [FO8].
  - All arms: `depkt_mutants.py` 11 of 11, `fanout_mutants.py` 21 of 21. The suite's other arms catch 13, 12 and 4.
- The `avtp_rxmon` suite at the head: flat 97, N=4 stack 218, lockstep N=1 116 and N=8 119, ctxfmt 96, fanout 1,205,
  depkt 374 twice. Every arm passes.
- The affected suites, each as `run_all_suites.sh` runs one: all 11 pass.
  - `avtp_rxmon`; milan_dp 14,148 checks; `milan_dp_mclk` 173 (36 of 36 cases).
  - `aaf_audio_loop`, `capture_coherence`, `follow_ring`, `mbx`, `milan_dp_gm_steps`, `milan_dp_render`,
    `pp_shadow` and `tsn_fuzz`: 548,216 checks.
  - milan_dp reached the sweep's 7,200 s wall clock inside its last phase, `render_mutants` (`rc=124`, the sweep's
    UNKNOWN, under a host load near 145). Every check before it had passed. That phase then ran alone on the same
    binaries: 6 of 6.
  - `tsn_fuzz`'s four declared skips are not counted.
- The twin, `twin-plants`, `twin-maps`, `twin-maps-plants`, `twin-fanout`, `twin-fanout-plants`, `fan-stop-plants`:
  `twin: 0 finding(s)`, every plant refused.
- `tsn_fuzz`'s AAF campaign with its generator: 164 pass, its artifact fresh.
- Docs workflow steps 104 of 104; `lint_rtl.py --check` 89 <= 89; `xvlog_gate.py --check` 0 findings.
- Yosys on the touched tops: `KL_aaf_rx_depacketizer` 54,392 cells (54,236 at round 2), `KL_avtp_rx_monitor_ctx`
  12,034. Tied-input and tap-purity gates PASS.
- Fit and timing at this head, after the sweep: the gating recipe, #818's three placement directives, 8 Vivado
  threads, two Vivado at a time through `vivado-slot.sh`.

  | Point | Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | LUTs | FFs | Slices | BRAM tiles | DSPs | vs round 2 (LUT / FF / slice) |
  |---|---|---|---|---:|---:|---:|---:|---:|---|
  | 8x8/1if | **ExtraPostPlacementOpt** | **+0.339** / +0.060 | +1.636 / +0.017 | 45,161 | 51,215 | 15,706 | 94 | 13 | +1,103 / +80 / +191 |
  | 8x8/1if | ExtraTimingOpt | +0.174 / +0.051 | +1.641 / +0.024 | 45,113 | 51,213 | 15,131 | 94 | 13 | +1,357 / +81 / +30 |
  | 8x8/1if | AltSpreadLogic_high | +0.114 / +0.100 | +1.641 / +0.036 | 45,164 | 51,214 | 15,130 | 94 | 13 | +1,373 / +80 / +40 |
  | 1x1/1if | ExtraPostPlacementOpt | +0.046 / +0.102 | +1.641 / +0.036 | 32,870 | 42,838 | 13,746 | 79.5 | 13 | +253 / +170 / +302 |
  | 1x1/1if | ExtraTimingOpt | +0.115 / +0.102 | +1.687 / +0.036 | 32,920 | 42,842 | 14,217 | 79.5 | 13 | +270 / +172 / -78 |
  | 1x1/1if | **AltSpreadLogic_high** | **+0.139** / +0.102 | +1.687 / +0.036 | 32,918 | 42,843 | 14,216 | 79.5 | 13 | +268 / +173 / -88 |

  - #818's floor (WNS >= +0.030 ns, WHS >= 0) is met at every corner on all six builds. The image identity gate
    agrees on each.
  - The depacketizer's placed cost against round 2 at the same directive is +80 FF (the lag's stages) at every
    build. In LUTs it is +29 to +40 at 8x8 and +75 to +80 at 1x1.
  - The 8x8 totals' other ~+1,100 LUT sit in unchanged hierarchies, the cross-boundary attribution of rounds 1
    and 2: `u_gptp_shadow`'s own level +1,169 against its `u_engine` -883 (+153 net), and `KL_mbx_cdc/u_edit`
    +702 against `u_pub` -549. No RTL outside the depacketizer changed since round 2.
  - No setup path a signoff report lists touches the parser, the monitor or the depacketizer. The worst are on the
    CPU clock (`KL_mbx`) and reset synchronisers.
  - The 1x1 ExtraPostPlacementOpt build's +0.046 ns is `KL_mbx`'s CPU-clock path, which has moved between
    near-identical netlists since round 1. The 8x8 Fast-corner hold minimum, +0.017 ns, is `media_clock_restart`'s
    and unchanged.

Acceptance criteria (the ruling of 2026-11-22):
- (1) Measured at `15168e14`, `4ceba3d4` and the head: met, above. Round 1 changed the behaviour (13 to 11 beats), and
  1-channel was never delivered at any revision before this one.
- (2) Every frame size an input can advertise and receive is delivered with its own tlast and input tag, and an
  off-format frame is still discarded whole and counted: met.
  - The shortest legal AVTPDU of every advertised format, down to 1 channel at 48 kHz, the lowest rate, is 62 octets
    untagged and 66 tagged. It is delivered in [FO14], [DT4] and [FAN].
  - Every frame from the Ethernet minimum up is delivered (the probe).
- (3) Tests failing at `e8252323` for each size class (8, 9, 10 beats; no AVTPDU the parser can match is shorter),
  every remainder kept, and plants re-breaking the short-frame path: met.
- (4) Suites, twin, the datapath sweep pieces, Yosys and docs gates: met. Re-route (the RTL changed): met.
  #818's floor holds at every corner at 8x8/1if and 1x1/1if on all three directives. Best: 8x8
  ExtraPostPlacementOpt +0.339 ns, 1x1 AltSpreadLogic_high +0.139 ns. No STOP.

Open risks/questions:
- The receive path's depacketizer output is three cycles later than at round 2: the store's write lag.
  - Presentation is placed by timestamp (the render queue, #632), so no sample's presentation time moves, and no
    suite's check moved.
  - The lag costs 3 x 74 bits of shift register (`dd_r`/`dk_r`/`dl_r`, no reset, read only with their valid).
- The lag is a contract with the parser and the monitor: the enqueue pulse lands at most `ENQ_LAT_C` cycles after a
  frame's eighth beat on the tap. A change to either module's registering must move `ENQ_LAT_C`. [FO14] and [FAN] run
  the real parser and monitor, so a pulse later than the lag fails them. The plants of a shorter lag show the
  mismatch is caught: none in [FO14] and [DT4], two cycles in [DT4].
- Round 2's open items stand: USER and reserved formats are sized as four octets; `PCMRX_CNT`'s drops half counts a
  queued PDU's frame short of its payload.

REVIEW READY 64e55a59e09339114926c2600056c3ad8b33b9b4
