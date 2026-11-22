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
the train merges, this PR's diff is this lane's commits only. Round 2 (from `4ceba3d4`) answers the two reviews of
round 1. Round 2b (from `e8252323`) fixes the short-frame defect round 2 found: frames of eight to ten beats,
counted and never delivered.

- **Round 2b's tests failed first** on round 2's RTL (`e8252323`), then passed:
  - `sim_fanout` [FO14] and [FO8]'s drop check: 236 of 1,205 failed (FO14 234, FO8 2), then 1,205 of 1,205.
  - `sim_depkt` [DT4]: 3,077 of 5,750 failed at either payload lead (192 of 960 short-frame cases whole; no frame
    for the 1-channel 48 kHz PDU), then 374 of 374 at both leads.
  - `sim_nxn` [FAN] at one channel: 6 of 4,073 failed (FRAMES_RX counted, DEPKT 0), then 4,073 of 4,073.
- **Measured at every revision** through its own receive stack: the shortest delivered frame was 98 octets (13 beats)
  at the true base `15168e14`, 82 (11 beats) at `4ceba3d4` and `e8252323`, and the Ethernet minimum at this head.

- **Round 2's tests failed first** on round 1's RTL (`4ceba3d4`), then passed:
  - `sim_fanout` [FO11]-[FO13]: 91 of 489 failed (all in FO11-FO13), then 489 of 489.
  - `sim_depkt` (new): 2,842 of 5,150 failed at either payload lead (2,077 of 2,760 length cases whole; the review's
    65-octet probe gives no frame), then 369 of 369 at both leads (2,760 of 2,760 cases).
  - `sim_nxn` [FAN] STOP legs: they pass on the unmodified 8x8 datapath (its gate was right) and fail by name on both
    stop-gate plants (`make fan-stop-plants`), on round 1's RTL and on this head.
- **Planted defects:** `fanout_mutants.py` 21 of 21, `depkt_mutants.py` 11 of 11 (four re-break the short-frame
  path), `fan-stop-plants` 2 of 2. The `avtp_rxmon` suite's other arms still catch theirs: lockstep 13, format 12,
  ctxfmt 4.
- **The affected suites at this head, each as the sweep runs one** (every suite that builds the two touched modules):
  all 11 PASS.
  - `avtp_rxmon`; milan_dp 14,148 checks; `milan_dp_mclk` 173 (36 of 36 cases).
  - `aaf_audio_loop`, `capture_coherence`, `follow_ring`, `mbx`, `milan_dp_gm_steps`, `milan_dp_render`,
    `pp_shadow` and `tsn_fuzz`: 548,216 checks.
  - milan_dp reached the sweep's 7,200 s wall clock inside its last phase, `render_mutants`, under the host's load.
    That phase then ran alone on the same binaries: 6 of 6.
  - On the way in round 2, milan_dp found its root harness sending the 8-channel shape a 48-octet PDU, off the
    declared format. The stimulus is fixed in `29ffa248`.
- **Gates:** the twin and its plants (`twin: 0 finding(s)`); the docs workflow steps (104 of 104); the lint ratchet; the
  Vivado front end (`xvlog_gate.py`); the Yosys gate on the two touched tops; `tsn_fuzz`'s AAF campaign with its
  generator (164 pass, its results artifact fresh).
- **Fit and timing at this head:** both points meet #818's gate at every corner on all three directives (re-routed,
  the RTL changed).
  - 8x8/1if best: ExtraPostPlacementOpt, Slow WNS +0.339 / WHS +0.060 ns.
  - 1x1/1if best: AltSpreadLogic_high, Slow WNS +0.139 / WHS +0.102 ns.

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
went to the input with the higher index, and the AAF clock meter took the same one index. The twin's split half at
8x8/1if shows input 0 counting 0 of 4 PDUs beside input 1, as the bench found.

**The fix: one PDU to every bound input, nothing copied per input** (#948's ruling of 2026-11-21: fan-out, not
refusal).

| Piece | Change |
|---|---|
| `avtp_stream_parser.sv` | `match_vec_o`: every enabled entry the stream_id matches, registered with the parse pulse. `match_index_o` stays (the APRB probe, the public tap). |
| `KL_avtp_rx_monitor_ctx.sv` | `match_vec_i` replaces the index. A bundle in the PDU ring holds the matched-and-bound vector, and the walker serves that one bundle to each context in turn, lowest first. Each context gets its own format compare, MON_STATE, counters, tv tallies and accept pulse. New outputs for the depacketizer: `pdu_enq_p_o`, one cycle after the match (the PDU was queued), and `pdu_done_p_o` with `pdu_done_mask_o`, the contexts that accepted it. With one binding per stream the engine is cycle-equal to its reference (the lockstep leg at N=1 and N=8). |
| `KL_aaf_rx_depacketizer.sv` | A frame is committed on the enqueue pulse. A four-entry verdict queue matches each enqueue to its frame's fate and to its done mask. The read side reads the one stored frame once per accepting input (tuser that input), and passes over a frame no input accepted. A full store's drop counts in the DEPKT drops of the frame's accepting inputs. |
| `milan_datapath.sv` | The wiring. The Milan v1.2 5.3.8.7 stop gate is applied to the done mask input by input. The AAF clock meter sees a PDU when the followed input's bit is set in the match vector. |
| Unchanged | The route, the render queue, the loopback bucket and the latency taps. The mailbox contract, the firmware and every CPU budget image. |

**Round 2: each PDU's frame boundaries, and the stop gate's test.**

The two reviews of round 1 found:
- R878-1 F2 (MAJOR): a PDU whose stream_data_length is not a multiple of 8 lost its last beat and emitted no tlast.
  **This defect predates #948 and was found by review**: the base's direct probe gives the same result.
  - When the payload's tail lies wholly in the hold register, the depacketizer popped the frame's last stored word
    with the beat before it, so its truncated-frame resync left `R_PAY_S` without the final beat.
  - The same shape at the next frame's boundary made the next PDU's beats join it, for any input.
- R877-1 F1 (MINOR): no test failed if one input's 5.3.8.7 discard also discarded the PDU for the other inputs bound
  to its stream.

The manager's ruling on F2 is in two parts:
- (a) An AAF PDU whose stream_data_length is not the bound input's frame size is malformed, discarded whole before
  any payload transfer, per input, and counted.
- (b) The depacketizer's padded-tail contract is made true.

| Piece | Change |
|---|---|
| `KL_avtp_rx_monitor_ctx.sv` | (a) The frame size is part of the input's format. An input's frame size is channels_per_frame x samples_per_frame (IEEE 1722-2016 I.2.4.1) x the sample's octets (7.3.5, Table 9: 2 for INT_16BIT, 3 for INT_24BIT, 4 for the 32-bit formats). It is computed from the context's format word one state before the verdict (`flen_r`). A PDU whose stream_data_length (4.4.4.10) is another size counts UNSUPPORTED_FORMAT at that input and gets no accept, so that input receives none of it (Milan v1.2 4.4.2.2), while an input whose size it matches receives it whole. The reference copy carries the same lines, as it does #765's and #775's. |
| `KL_aaf_rx_depacketizer.sv` | (b) When the tail lies in the hold, the frame's last word is kept until the final, hold-only beat and popped with it, so the frame's end and the pass's end (rewind or release) fall on the beat that carries tlast. A frame that ends short of its stream_data_length is dropped whole at its tlast and counted in `drops_o` and in its accepting inputs' DEPKT drops, so the read side only reads complete payloads. The truncated-frame resync is now defensive only. The frame store, its read registers and the two small queues state why they carry no reset (R877-1 S1). |
| Stimulus | Several harnesses sent PDUs whose stream_data_length was not their format's frame size, or set a format word with samples_per_frame 0. Each now sends its format's frame size: `sim_lockstep`, `sim_main_nx`, `sim_ctxfmt`, `sim_nxn` and the milan_dp root's `sim_main`. |
| Docs | The walkthrough's diagram and rows (R878-1 F1), the media-clock meter's field table (R878-1 F1), `FPGA_DESIGN.md`'s rows, `TESTING.md`'s `avtp_rxmon` row (R877-1 R1's sentence break), the `milan_dp` README, `PCMRX_CNT`'s drops field, the evidence-reader dispositions and the inventory. |

**Tests, failing first** (round 1's RTL `4ceba3d4`, then this head):

| Test | Holds | `4ceba3d4` | Head |
|---|---|---|---|
| `sim_fanout.cpp` [FO11] | PDUs of 65 (the review's probe), 64, 200 and 191 octets between valid 192-octet ones, with a gap and back to back, to two inputs: each counts UNSUPPORTED_FORMAT and receives none; the valid ones arrive whole, in order, under each index, with no sequence mismatch. Two inputs of 192 and 224 octets on one stream each take only their own size. | FAIL (24) | PASS |
| `sim_fanout.cpp` [FO12] | frame sizes with each remainder 1 to 7 (INT_24BIT and INT_16BIT), untagged and behind a C-VLAN tag, to two inputs, with another stream's PDUs to a third input between them: each a frame of ceil(length/8) zero-padded beats with one tlast | FAIL (58) | PASS |
| `sim_fanout.cpp` [FO13] | frames that end short of their stream_data_length, by words and by one octet, untagged and tagged: counted by each input, delivered to none, one DEPKT drop for each and in `drops_o`; the PDUs around them arrive whole | FAIL (9) | PASS |
| `sim_depkt.cpp` (new, `make depkt`) | the depacketizer alone at four inputs, at no payload lead and at the datapath's. [DT1] is the review's 64-octet control and 65-octet probe. [DT2] covers every length 1-72, 184-200, 1000, 1001 and 1983, untagged and tagged, with and without trailing octets, to no input, one, two or four, under no stall, random stalls and stalls at each PDU's last two beats, each followed by an ordinary PDU to another input: beats, tlast, tuser, bytes, `pdu_out_p_o`, `pdus_o`, AXI-Stream hold. [DT3] covers frames short of their payload. | FAIL (2,842 of 5,150) | PASS |
| `depkt_mutants.py` (new) | 7 defects, among them the review's premature pass end and resynchronisation (the kept word popped early) | | 7 of 7 |
| `fanout_mutants.py` | 7 new defects: no frame-size compare, six samples assumed, every input sized by input 0's format, a 24- or 16-bit sample sized as four octets, the hold-only tail popped early, a short frame read out | | 19 of 19 |
| `sim_nxn.cpp` [FAN] STOP legs | inputs 4 and 6 on one stream; STOP_STREAMING input 4, then 6, and START each again over AECP. While one is stopped, the other's DEPKT tally counts every PDU and the stopped input's counts none, while its FRAMES_RX counts each (Table 5.6). After START both receive. | PASS (the gate is right) | PASS |
| `make fan-stop-plants` (new) | obj_nxn8 on the review's shared gate (a stopped accepting input discards the PDU for all) and on the accept pulse's one-index stop applied to every share: each named check fails | caught, both | caught, both |

**Round 2b: every frame from the Ethernet minimum up** (the manager's ruling of 2026-11-22: fixed in this PR).

The monitor's enqueue pulse lands exactly three cycles after the tap carries a frame's eighth beat: the parser's
input register, its registered match, the monitor's registered pulse. The depacketizer dropped a frame at its tlast
unless that pulse had come. So a frame of eight to ten beats (57 to 80 octets) was counted in FRAMES_RX and never
delivered. Milan's shortest Base format, one channel at 48 kHz (24 octets, a 62-octet frame, 66 tagged), is reachable
because the inputs advertise Milan 6.4's channel family, and it rendered nothing. Before #948 the commit waited for the
still later accept pulse, so 2-channel 48 kHz frames (86 octets) were lost too. Round 1's enqueue commit made those
deliverable.

| Piece | Change |
|---|---|
| `KL_aaf_rx_depacketizer.sv` | The store's write side runs `ENQ_LAT_C` = 3 cycles behind the tap (a valid-qualified shift register). The tap's own beat count names each pulse's frame, the one that passed its eighth beat last. Each frame's verdict is taken when its eighth beat reaches the write side, a pulse in that same cycle included, which is on or before its tlast however short the frame. An unqueued frame is still dropped at its tlast; the monitor's off-format discard, the whole-payload check and the tail are unchanged. |
| Docs | The walkthrough's depacketizer row, `FPGA_DESIGN.md`, `TESTING.md`'s `avtp_rxmon` row, the `milan_dp` README, the evidence dispositions, the inventory. |

| Test | Holds | `e8252323` | Head |
|---|---|---|---|
| `sim_fanout.cpp` [FO14] | payloads of 2-42 octets in one channel of INT_16BIT, INT_24BIT or INT_32BIT, the Milan 1-channel 48 kHz Base format among them, every remainder, untagged and tagged: frames of 8, 9 and 10 beats, two back to back, to two inputs, another stream's PDU to a third input between them; PDUs off the inputs' frame size in equally short frames are discarded whole and counted | FAIL (234) | PASS |
| `sim_fanout.cpp` [FO8] | the frame cut off its payload on its eighth beat is now a DEPKT drop for each input, as [FO13]'s are | FAIL (2) | PASS |
| `sim_depkt.cpp` [DT4] | frames of 8 to 10 beats, every payload length that fits, with the bench's enqueue pulse three cycles after the eighth beat (the datapath's latency) and one cycle after; an unqueued frame between two queued ones; the 1-channel 48 kHz PDU three beats with one tlast | FAIL (768 of 960 cases) | PASS |
| `sim_nxn.cpp` [FAN] | inputs 6 and 7 bound at one channel of 48 kHz: 62-octet and 66-octet tagged frames, each counted and received | FAIL (6) | PASS |
| `depkt_mutants.py`, `fanout_mutants.py` | the store taking the tap as it comes, a pulse taken only while its frame is on the tap, a same-cycle pulse missed, a two-cycle lag; the round-1 lost-PDU mutant re-anchored (a frame's fate written to the previous entry) | | 11 of 11, 21 of 21 |

**Fit and timing at this head** (the gating recipe, `--eth-port e2`, synthesis AreaOptimized_high, opt ExploreArea,
each of #818's three placement directives; #818's gate is WNS >= +0.030 ns and WHS >= 0 at every signoff corner). The
last column is the move against round 2's build at the same directive.

| Point | Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | LUTs | FFs | Slices | BRAM tiles | DSPs | vs round 2 (LUT / FF / slice) |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 8x8/1if | **ExtraPostPlacementOpt** | **+0.339** / +0.060 | +1.636 / +0.017 | 45,161 | 51,215 | 15,706 | 94 | 13 | +1,103 / +80 / +191 |
| 8x8/1if | ExtraTimingOpt | +0.174 / +0.051 | +1.641 / +0.024 | 45,113 | 51,213 | 15,131 | 94 | 13 | +1,357 / +81 / +30 |
| 8x8/1if | AltSpreadLogic_high | +0.114 / +0.100 | +1.641 / +0.036 | 45,164 | 51,214 | 15,130 | 94 | 13 | +1,373 / +80 / +40 |
| 1x1/1if | ExtraPostPlacementOpt | +0.046 / +0.102 | +1.641 / +0.036 | 32,870 | 42,838 | 13,746 | 79.5 | 13 | +253 / +170 / +302 |
| 1x1/1if | ExtraTimingOpt | +0.115 / +0.102 | +1.687 / +0.036 | 32,920 | 42,842 | 14,217 | 79.5 | 13 | +270 / +172 / -78 |
| 1x1/1if | **AltSpreadLogic_high** | **+0.139** / +0.102 | +1.687 / +0.036 | 32,918 | 42,843 | 14,216 | 79.5 | 13 | +268 / +173 / -88 |

- **Round 2b's own cost** is the depacketizer's three-cycle lag: +80 FF at every build, and +29 to +40 LUT at 8x8, +75
  to +80 at 1x1 (placed hierarchy, against round 2).
- **The whole PR's receive-path cost against round 1** (ExtraPostPlacementOpt):
  - 8x8/1if: `aaf_rx_depkt` 310 -> 445 LUT and 200 -> 298 FF. `avtp_rx_monitor` 2,079 -> 2,168 LUT and 1,715 ->
    1,737 FF, plus 2 DSP blocks for the frame-size product.
  - 1x1/1if: `aaf_rx_depkt` 363 -> 501 LUT and 207 -> 305 FF. `avtp_rx_monitor` 791 -> 814 LUT and 747 -> 769 FF,
    plus 2 DSP blocks.
- **The 8x8 totals' other ~+1,100 LUT against round 2 sit in unchanged hierarchies,** the cross-boundary attribution
  seen in rounds 1 and 2. `u_gptp_shadow`'s own level moves +1,169 against its `u_engine`'s -883 (the instance +153
  net), and `KL_mbx_cdc/u_edit` +702 against `u_pub`'s -549. No RTL outside the depacketizer changed since round 2.
- **No worst path is in the receive path.** No setup path any signoff report lists touches the parser, the monitor or
  the depacketizer. The worst setup paths are on the CPU clock (`KL_mbx`) and reset synchronisers. The 1x1
  ExtraPostPlacementOpt build's +0.046 ns is that `KL_mbx` path, which has moved between near-identical netlists
  since round 1. The 8x8 Fast-corner hold minimum, +0.017 ns, is `media_clock_restart`'s, unchanged.

## Authoritative references

- IEEE 1722.1-2021 8.2: each sink binds on its own, so one stream_id can be the source of several Stream Inputs.
- Milan v1.2 5.3.8.10 and Table 5.6: the counters of each Stream Input, on the PDUs "received on this Stream Input".
- Milan v1.2 5.3.8.7: a stopped Stream Input discards the PDUs it receives.
- Milan v1.2 4.4.2.2: a Listener discards incoming AVTPDUs that don't respect the format configured in the
  STREAM_INPUT; Table 5.6 UNSUPPORTED_FORMAT counts them.
- IEEE 1722-2016 4.4.4.10 (stream_data_length is the payload's octets), 7.3.5 (every AAF AVTPDU of a stream carries
  the same number of samples; each sample's octets are fixed by the format), Table 9 (the format values), I.2.4.1
  (samples_per_frame in the stream format).
- #948's ruling of 2026-11-21: fan-out, not refusal. The manager's ruling on R878-1 F2: discard an off-size PDU whole,
  per input, counted; make the padded-tail contract true.
- The manager's ruling of 2026-11-22 on round 2's new scope: frames of ten beats or fewer are fixed in this PR,
  since Milan v1.2 4.4.2.2 and 6.4 require an advertised format to be received. Milan v1.2 Table 6.1 gives the
  1-channel 48 kHz Base format.

## How to get into the same state

```sh
git fetch origin && git checkout <this PR's head>
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
# Verilator 5.050 (the CI image's), sv2v v0.0.12 and Yosys on PATH; the RV32 SDK for the firmware gate
```

## How to validate

```sh
# the receive stack's suite: lockstep, the N=4 stack, ctxfmt, the fan-out leg, the depacketizer leg and every arm
make -C tb/verilator/avtp_rxmon
# the 8x8 datapath with the [FAN] section, its STOP legs among it, and the two stop-gate plants
make -C tb/verilator/milan_dp build-nxn8 exec-nxn8 fan-stop-plants
# the twin's split half at 8x8/1if and its plant; the twin itself and its plants
make -C tb/verilator/milan_dp twin-fanout twin-fanout-plants twin twin-plants twin-maps twin-maps-plants
# the root suites, the media clock among them
make -C tb/verilator/milan_dp && make -C tb/verilator/milan_dp_mclk
# the sweep, the lint ratchet, the Vivado front end
bash scripts/run_all_suites.sh <logs> --wait
python3 scripts/lint_rtl.py --check && python3 scripts/xvlog_gate.py --check
```

Expected result / pass criteria:
- `FANOUT N=8: 1205 checks, 0 failures` and `22 checks: 22 PASS, 0 FAIL`.
- `DEPKT: 374 checks, 0 failures` twice and `12 checks: 12 PASS, 0 FAIL`.
- `checks: 4073 failures: 0` for obj_nxn8, and `caught (shared):` and `caught (one-index):` twice each.
- `twin: 0 finding(s)`, and every plant word caught.
- `36 checks: 36 PASS, 0 FAIL` for `milan_dp_mclk`.
- Every sweep suite PASS, and the lint and xvlog gates PASS.

## Known limitations / out of scope

- **The depacketizer's output is three cycles later than before round 2b.** That is the store's write lag behind
  the tap. Presentation is placed by timestamp (the render queue, #632), so no output moves in time, and no suite's
  check moved. The lag costs a 3 x 74-bit shift register.
- **The lag is a contract with the parser and the monitor:** the enqueue pulse lands at most `ENQ_LAT_C` cycles after
  a frame's eighth beat on the tap. A change to either module's registering must move `ENQ_LAT_C`. [FO14] runs the
  real parser and monitor, so a pulse later than the lag fails it. The plants of a shorter lag (none, and two cycles)
  show that both harnesses catch the mismatch.
- **A format whose sample size the standard does not fix is sized as four octets.** USER and the reserved format
  values have no octet count in IEEE 1722-2016 Table 9. The frame-size verdict sizes them as four. No input of this
  entity advertises one.
- **Throughput is the same totals as distinct streams, not more.** The engine walks each bound context once per PDU
  and the depacketizer reads one pass per receiving input, so a PDU bound to k inputs costs what k distinct streams'
  PDUs cost. At the Class A interval neither limit is near: [FO6] and [FO10] measure them.
- **`PCMRX_CNT`'s drops half now also counts a queued PDU's frame short of its payload,** besides store overflows.
- **The DEPKT drop tally's meaning moved (round 1).** A frame the full store drops counts in the drop tally of each
  input that accepted its PDU, and a foreign frame's drop only in the depacketizer's total.
- **Input 0's PDUS window word stays the shared total.** Unchanged by this PR, and noted in the `milan_dp` README.

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
