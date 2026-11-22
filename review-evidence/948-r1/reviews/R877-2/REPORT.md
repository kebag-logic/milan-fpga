[R877] NEGATIVE - exact head 64e55a59e09339114926c2600056c3ad8b33b9b4

# Round R877-2: internal cleared-context review of PR #959 (issue #948), delta round 2

- **Head and tree:** head `64e55a59e09339114926c2600056c3ad8b33b9b4`, tree `ee8f0eb03b6f360cd507678ef029970ec43afc95`.
- **Delta judged:** `4ceba3d4..64e55a59`, eleven commits: round 2 (`a9ed2a6d`..`e8252323`) and round 2b (`0b4517c3`, `d24a15c8`, `64e55a59`).
- **Whole-PR context:** `15168e14..64e55a59`.
- **Lenses:** all five were applied independently.

## Verdict summary

The round-1 findings are fixed at their causes:
- R878-1 F2: an off-size PDU is discarded whole per input and counted, and the padded tail ends on its tlast.
- R878-1 F1 is fixed.
- R877-1 F1: the shared stop gate is planted with the round-1 probe's exact expression and caught by name.
- R877-1 R1 is fixed and S1 is adopted.

The manager's round-2b ruling is met. Every frame from the Ethernet minimum up, tagged and untagged, is delivered with its own tlast and tag, the 1-channel 48 kHz Base PDU included. The three-cycle lag is correct by construction:
- The parser and the depacketizer tap the same bus (`milan_datapath.sv:7308-7312`, `:8015-8019`).
- The parse fires on the accepted eighth beat (`avtp_stream_parser.sv:215-216`), and the monitor registers the pulse once more (`KL_avtp_rx_monitor_ctx.sv:948`).
- The write side is a pure three-cycle delay (`KL_aaf_rx_depacketizer.sv:211-227`).

My own tap-bubble probe confirms the lag under tap backpressure. With tvalid gaps and tready-low beats inside every frame, `sim_depkt` passes 374 of 374 at both leads. Through the real parser and monitor, `[FO11]`-`[FO14]` pass.

The same probe found one defect this PR's claim depends on (F1, MINOR):
- **What happens:** under an overflow burst, the per-input DEPKT drop tally loses counts.
- **Why:** the monitor's 3-bit pending accumulator saturates while PDU walks starve its drain.
- **What it falsifies:** the documented claim "every PDU an input accepted is delivered to it or counted as one of its own DEPKT drops".
- **Why no test sees it:** no bench drives an intra-frame tap bubble, and `[FO10]`'s live case drops only 4 frames per input, below the saturation point of 7.

The probe also found one stale figure in `TESTING.md` (F2, MINOR). Both MINORs are open, so the verdict is NEGATIVE.

Round 2b's routes are measured and meet #818's floor on all six builds: 8x8/1if best +0.339 ns, 1x1/1if best +0.139 ns.

## Findings

### F1 - MINOR - RTL, Robustness, Tests, Docs - the per-input DEPKT drop tally loses counts under an overflow burst; the tests cannot see it

**Artifacts:**
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:351-352` (`dpdu_pend_r`, `ddrop_pend_r`, 3 bits each).
- `:984-986` (the increment saturates at 7).
- `:1038-1044` (the w11 drain is taken only when no PDU walk, bind or silence is pending).
- `:1161-1165`.
- `tb/verilator/avtp_rxmon/sim_fanout.cpp:231-249` (`feed`: one beat a cycle, no intra-frame gap).
- `:597-630` (`[FO10]`).
- `docs/testing/TESTING.md:706` ("every PDU an input accepted is then delivered to it, in order, or counted as one of its own DEPKT drops").
- The PR body's Description and Known-limitations rows on DEPKT drops.

**Authority and evidence:**
- **What the PR claims:** since round 1, a full store's drop counts in the DEPKT drops of each accepting input. Round 2 sends a queued frame short of its payload through the same pulse (`KL_aaf_rx_depacketizer.sv:442-464`). The PR states this conservation unconditionally, and `[FO10]` grades it.
- **AXI-Stream allows bubbles:** tvalid may drop inside a frame, and the depacketizer's own tap counts only accepted beats (`:159`). The benches never do this: `sim_fanout`'s and `sim_depkt`'s feeds drive one beat a cycle, and the wraps tie the tap's tready high.
- **Probe:** `scripts/plant_tap_bubbles.py` puts 1-3 idle cycles before 60% of beats. Results (`receipts/fo10_under_bubbles_summary.txt`, `receipts/bub_fanout.log.gz`):
  - All 30 PDUs are queued and accepted by all eight inputs.
  - Each input gets 15 payloads, in order.
  - Inputs 0 and 1 count 15 DEPKT drops each (30 = 15 + 15).
  - Inputs 2-7 count only 9 or 7 (`got=24 exp=30`, `got=22 exp=30`).
  - So 6-8 of each input's accepted PDUs are neither delivered nor counted.
- **Cause, confirmed:**
  - Widening `ddrop_pend_r` to 6 bits (`scripts/widen_ddrop_pend.py`, `receipts/probe_widened_ddrop_pend.diff`) makes every `[FO10]` check pass under the same bubbles (`receipts/bub_fanout_widened.log.gz`).
  - The accumulator saturates at 7 while the walker, busy serving eight contexts per PDU, never reaches the w11 drain.
  - Its lowest inputs are drained first, which is why inputs 0 and 1 balance.
- **Why the shipped `[FO10]` passes:** the same section at the head, unplanted, queues only 15 of 30 PDUs (the monitor's ring fills) and drops 4 frames per input (`receipts/rxmon_all.log.gz`). That is below the saturation point, so the test cannot fail for this bound.
- **Attribution:**
  - The same loss reproduces identically with round 1's depacketizer and monitor (`4ceba3d4`) under the bubble bench (`receipts/bub_fanout_r1rtl.log.gz`, `[FO10]` lines).
  - So it comes from round 1's per-input drop attribution, built on the base's 3-bit accumulator. Round 2b's lag did not introduce it.
  - Round 2 widened its use: short-frame drops now share the pulse, and `TESTING.md:706` was rewritten in this delta with the unconditional claim.
  - No prior lens covered RTL, Robustness or Tests clean at round 1, so there is no banked verdict for it to inherit.
- **Not affected:**
  - The audio path: every delivered payload is correct and in order.
  - Milan Table 5.6 counters.
  - FRAMES_RX.

**Impact:**
- **On hardware:** under a burst that overflows the frame store with several inputs on one stream, the DEPKT drop half of the LCTX w11 word under-counts for the higher inputs. The `PCMRX_CNT` total does not.
- **For a reader:** a controller or test reading DEPKT to reconcile against FRAMES_RX sees PDUs that vanished.
- **Wider bound:** `dpdu_pend_r` (the delivered tally) has the same 3-bit saturating structure and the same drain. Its bound is not graded either.

**Required outcome:**
- The DEPKT tallies of every input must account for every accepted PDU under any reachable burst, or the bound must be stated where the claim is made.
  - For example: pending accumulators wide enough for the most drops or deliveries that can wait for one drain (the store's 32 committed frames plus the verdict queue), or a drain that cannot starve.
  - Otherwise: `TESTING.md`, the PR body and the RTL comment state the saturation (seven pending per input) instead of unconditional conservation.
- A bench must drive intra-frame tap bubbles, at least for `[FO10]`'s overflow case, so the claim is graded at a drop count above the saturation point.

**Verification:** with a corrected head, `plant_tap_bubbles.py` plus `make fanout` passes every `[FO10]` check, or the restated bound is what the bench grades. A plant restoring the 3-bit saturation fails a named check.

### F2 - MINOR - Docs - `docs/testing/TESTING.md:706` names `[FO12]`'s frame sizes as round 1 had them

**Authority and evidence:**
- **What the doc says:** the `tb/verilator/avtp_rxmon` row says the fan-out leg's non-whole-beat frame sizes are "33, 36, 63, 66 and 70 octets".
- **What the test does at the head:** since `6ab8b355`, `[FO12]` runs 81, 66, 99, 60, 93, 70 and 63 octets, every remainder 1 to 7 (`tb/verilator/avtp_rxmon/sim_fanout.cpp:690-698`). The section's own header comment (`:53-58`) and the PR body ("each remainder 1 to 7") say so. The run log names them (`[FO12] 81 octets ...`).
- **Not caught by gates:** the row was regenerated in `64e55a59`, and the docs gates do not compare prose with a bench.

**Impact:** the authoritative testing document misstates a test's coverage. Remainders 3 and 5 read as untested, and 33 and 36 as tested, though they are not run.

**Required outcome:** the row names the sizes `[FO12]` runs (or "every remainder 1 to 7"). Note: unsure whether this is only wording, so filed MINOR, since it is a coverage figure.

**Verification:** compare the row with `sim_fanout.cpp:690-698` at the corrected head; docs gates pass.

### RS1 - RESIDUE - Tests (comment) - `tb/verilator/avtp_rxmon/sim_fanout.cpp:688-689`

- **Problem:** "Each frame is at least 13 beats, long enough for its PDU to be queued in its flight ([FO8] holds the frames that are not)" is stale since round 2b. Every frame from the Ethernet minimum up is now queued in its flight; frames of 8-10 beats are `[FO14]`'s, and `[FO8]` holds the cut frame.
- **Exact fix:** "Each frame is at least 13 beats ([FO14] holds frames of eight to ten beats)".

### RS2 - RESIDUE - Docs - latency wording

- **Where:**
  - `docs/testing/TESTING.md:706`: "three cycles after the parser's match on the eighth beat".
  - `docs/fpga/DATAPLANE_WALKTHROUGH.md:175`, row 5: "three cycles late, the monitor's enqueue latency after the parser's match on a frame's eighth beat".
- **Problem:** both can be read as three cycles after the parser's registered match. The RTL (`KL_aaf_rx_depacketizer.sv:161-166`) states it exactly: three cycles after the tap carries the eighth beat. The parser's registered match comes at +2 and the pulse at +3.
- **Exact fix:** in both places use "three cycles after the tap carries the frame's eighth beat (the parser's input register, its registered match, the monitor's registered pulse)".

### RS3 - RESIDUE - PR body - Round 2b's `KL_aaf_rx_depacketizer.sv` row, "(a valid-qualified shift register)"

- **Problem:** the delay shifts every cycle, bubbles included (`KL_aaf_rx_depacketizer.sv:211-223`). That is what keeps it equal to the pulse's latency. "Valid-qualified" can be read as shifting only on valid beats, which would break that.
- **Exact fix:** "(a fixed three-cycle shift register, each stage carrying its beat's valid)". The same phrase is in the fit `SUMMARY.txt` comment.

### RS4 - RESIDUE - PR body - the fit section omits the stricter rule's result at 8x8

- **What the receipts record:** `fit/8x8-ExtraPostPlacementOpt/signoff.txt` and `fit/8x8-ExtraTimingOpt/signoff.txt` record `ruling floors NOT met`, `rc=1`. Their Fast-corner hold is +0.017 and +0.024 ns, against both-+0.030.
- **Why it is only wording:** #818's floor (WHS >= 0) is met, so no verdict changes. Round 2's text disclosed the analogous 1x1 case.
- **Exact fix:** add "The 8x8 ExtraPostPlacementOpt and ExtraTimingOpt builds' Fast-corner hold (+0.017, +0.024 ns) meets #818's floor and misses the stricter both-+0.030 rule (their `signoff.txt` rc=1), on `media_clock_restart`'s unchanged path."

### RS5 - RESIDUE - Docs and comment layout

- `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:29-31`: the header wraps "A / committed frame is / read out". Re-flow the paragraph.
- `tb/verilator/milan_dp/README.md:1895`: the line runs past the file's wrap width. Re-flow the paragraph.

### S1 - SUGGESTION - RTL - `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:263`, `:403-404`, `:435-441`: make a late enqueue pulse fail safe

- **What happens today:** if a future change to the parser's or monitor's registering put the pulse later than `ENQ_LAT_C` while `taw_r` is still set:
  - The frame's `good_r` has already latched 0, so it is dropped at its tlast without a fate.
  - The pulse still allocates an entry (`te_r`), whose `rq_res_r` then never sets.
  - Retirement stops at that entry for good, which wedges the read side until reset rather than losing one PDU.
- **Why it is only a suggestion:** the contract holds by construction at this head (verified above). `[FO14]` and `[FAN]` would fail on such a change, and the PR states the contract.
- **Suggested change:** resolve the entry as dropped when its frame ends unqueued, or add a simulation-only assertion that a pulse with `taw_r` set lands in the stored eighth beat's cycle.

## Prior public findings, resolved or retained at this head

| Finding | State at `64e55a59` | Evidence |
|---|---|---|
| R878-1 F1 (MINOR, Docs) | **Resolved** | `DATAPLANE_WALKTHROUGH.md:157` shows `pdu_enq_p`, then `pdu_done_p` and the accepting inputs less each stopped input. That matches `milan_datapath.sv:8023-8025`. `MEDIA_CLOCK_FOLLOWING.md:444` names `avtprx_match` with `avtprx_vec_w[aaf_follow_idx_r]` and the index `aaf_follow_idx_r`, which matches `milan_datapath.sv:7481,7488`. The parser's index is marked diagnostic. |
| R878-1 F2 (MAJOR, RTL, Robustness, Tests, Docs) | **Resolved** | **Ruling (a), off-size discard:** `KL_avtp_rx_monitor_ctx.sv:548-566,577-594,1078-1084`. The frame size is cpf x spf x the sample octets (IEEE 1722-2016 7.3.5, Table 9, I.2.4.1), compared with stream_data_length (4.4.4.10), so an off-size PDU gets no accept (Milan v1.2 4.4.2.2). `fmt_r`'s low word is valid in `M_PFRD3_S` on both the stream-0 alias and the RAM path (`:1020-1025`, `:1074-1084`). **Ruling (b), padded tail:** `keep_w` (`KL_aaf_rx_depacketizer.sv:503-504`, `:569-572`) pops the last word with the hold-only beat. **Direct probe re-run:** `[DT1]` 64 octets is 8 beats with tlast, and 65 octets is one frame of 9 beats with tlast on the last, at both payload leads (`receipts/rxmon_all.log.gz`). **The 65-octet tail through the fan-out path:** `[FO11]` sends it to two inputs. Both count UNSUPPORTED_FORMAT and receive none, and the valid PDUs around it arrive whole, in order and under their own index. 65 matches no format's frame size, so admission now discards it whole. **Admitted non-multiple tails:** `[FO12]`, every remainder 1-7, tagged and untagged, through the real stack. **Hold tail:** `[DT2]` covers the tagged hold tail, stalls at the last word, and the following PDU. **Mutants:** the planted premature pass end is caught by `depkt_mutants.py` (`[DT1]` 65) and `fanout_mutants.py` (`[FO12]` 81). The PR body records that F2 predates #948. |
| R877-1 F1 (MINOR, Tests, Robustness) | **Resolved** | `sim_nxn.cpp` `[FAN]` stops input 4 and then 6 over AECP, then starts each again. The other input receives every PDU, and the stopped one receives none while its FRAMES_RX counts each (Table 5.6). `fan_stop_plant.py`'s `shared` plant is the round-1 `probeB.diff` expression character for character. Reran here at the head: obj_nxn8 4,073 of 4,073 pass. `make fan-stop-plants` rc 0: `shared` fails 4 checks, among them "input 4 stopped: input 6 receives every PDU" and "input 6 stopped: input 4 receives every PDU". `one-index` fails 4 (`receipts/fanstop.log.gz`, `receipts/fan_stop_plant_*_run.log.gz`). |
| R877-1 R1 (RESIDUE) | **Resolved** | `TESTING.md:706` reads "and passes. Its fan-out leg". |
| R877-1 S1 (SUGGESTION) | **Adopted** | `KL_aaf_rx_depacketizer.sv:204-206`, `:293-297`. |

## The manager's round-2b ruling, checked at its cause

**Claim:** at the base the shortest delivered frame was 98 octets, and 82 octets at rounds 1 and 2.
- Consistent with the published four-revision probe (`round2b/probe/minframe2-four-revisions.txt`).
- At the head, every length is accepted 3 of 3 and delivered 3 of 3, from 60 octets up, untagged and tagged.

**Mechanism:** read in the RTL, not taken from the description.
- `fire` needs `hdr_ready` (seven beats held) and an accepted eighth beat (`avtp_stream_parser.sv:215-216`), so a frame of seven beats never matches. The depacketizer's `tp7_w` counts the same accepted beats (`KL_aaf_rx_depacketizer.sv:159,179`).
- **Attribution:** the next frame's eighth beat is at least eight accepted beats, so eight cycles, after this one's. So `tq_r` and `te_r` name the right frame for the three cycles that matter.
- **Same-cycle case:** a same-cycle pulse and fate is handled by `fate_e_w`, and the fate assignment wins over the enqueue's default (`:404`, `:435-446`).
- **Verdict queue depth:** with the store's write side three cycles late, at most one entry waits for its fate, so the four-entry queue still covers every case.

**Tests at the head:** all reproduced here with the scoped Verilator 5.050 (`receipts/rxmon_all.log.gz`, `receipts/nxn8_exec.log.gz`).
- `sim_fanout` `[FO14]`: 1,205 of 1,205.
- `sim_depkt` `[DT4]`: 374 of 374 at lead 0 and at lead 16.
- `sim_nxn` `[FAN]` at one channel, 62-octet and 66-octet tagged frames: inputs 6 and 7 count and receive 4 of 4 each, and PCMRX counts 8.
- `depkt_mutants.py` 11 of 11, its four short-frame plants among them; `fanout_mutants.py` 21 of 21.

**Under tap backpressure (my probe):**
- `sim_depkt` with stalls inside every frame: 374 of 374 at both leads (`receipts/bub_depkt.log.gz`). The stalls are tvalid low and tvalid high with tready low, and the pulse is scheduled from the accepted eighth beat.
- `sim_fanout` with tvalid gaps, through the real parser and monitor: `[FO11]`-`[FO14]` all pass. That covers back to back, mixed sizes, three inputs and two talkers.
- Only `[FO10]` (F1) and one `[FO4]` check fail. The `[FO4]` failure, UNSUPPORTED_FORMAT 2 rather than 1, is a timing artefact: the slower feed spans two 2,000-cycle Table 5.6 observation intervals, and that counter counts once per interval.

## Lens results

```text
[R877] PASS Conformance - hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:548-594,1078-1084; hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:158-235,403-446; hdl/milan/milan_datapath.sv:7488,8023-8025; sim_nxn [FAN] STOP and one-channel legs (4,073/0, rerun) - frame-size verdict against IEEE 1722-2016 4.4.4.10, 7.3.5, Table 9, I.2.4.1 and Milan v1.2 4.4.2.2 (off-size counted UNSUPPORTED_FORMAT, no accept, per input; inputs of different sizes on one stream each take their own); Milan v1.2 5.3.8.7 and Table 5.6 (a stopped input discards while FRAMES_RX counts; START restores); every advertisable frame size down to 1 channel at 48 kHz (Table 6.1, 62/66 octets) delivered with its own tlast and tuser; the issue's fan-out ruling and the manager's two rulings; #818's fit floor on all six receipts. F1 concerns a vendor diagnostic tally (LCTX w11 DEPKT), not a Table 5.6 counter or delivery, so it is not attributed here.
[R877] FINDING RTL - KL_avtp_rx_monitor_ctx.sv:351-352,984-986,1038-1044 - F1 (MINOR). Otherwise examined: the tap attribution and the 3-cycle delay against the parser's fire condition and the monitor's registered pulse (same bus, direct wires); the verdict queue's fate/enqueue same-cycle precedence and depth; keep_w/hold_only ready logic and pass end; the whole-payload check (wvlan_r/wowe_r/wshort_w) and its commit/drop pointers; frame_octets widths (10x10 -> 20 -> 22 bits) and the fmt_r timing; reset of the new state; no-reset data stages read only with their valid. S1 (late-pulse wedge) is a suggestion.
[R877] FINDING Robustness - sim_fanout [FO10] under tap bubbles (receipts/bub_fanout.log.gz) - F1 (MINOR). Otherwise examined under tap bubbles and tap tready-low: malformed lengths (off-size, short by words and octets, tagged/untagged), minimum frames (8-10 beats, every remainder), back to back with mixed sizes and inputs, unqueued frames between queued ones, output stalls incl. at the last stored word, STOP/START ordering on a shared stream.
[R877] FINDING Tests - sim_fanout.cpp:231-249,597-630; sim_depkt.cpp feed - F1 (MINOR): no bench drives an intra-frame tap bubble, and [FO10]'s live case (4 drops per input) sits below the bound it claims to grade. Otherwise examined: each new test fails first on the prior RTL (published receipts) and each plant is caught by name (rerun here: 21/21, 11/11, 2/2, plus lockstep 13, format 12, ctxfmt 4); oracles derived from the stimulus, not the RTL; real parser+monitor integration in [FO11]-[FO14] and [FAN].
[R877] FINDING Docs - docs/testing/TESTING.md:706 - F1 (the unconditional conservation claim) and F2 (FO12's sizes), MINOR. Otherwise examined: DATAPLANE_WALKTHROUGH.md:157,171-175; MEDIA_CLOCK_FOLLOWING.md:444; FPGA_DESIGN.md:269,293; REGISTER_MAP.md:2001 and register_descriptions.json; milan_dp README:1887-1900; RTL header comments; the PR body and both REVIEW READY comments against the receipts. Source-comment rule: no bench lane label, lane name, review round, reviewer ID or issue-comment ID added in the delta's hdl/ or tb/ lines. Gates rerun here: docs_check 0 findings (223 md + 1,916 text files), docs_inventory fresh, check_doc_style OK, measure_test_evidence PASS, lint ratchet 89 <= 89. Residue RS1-RS5.
```

## Route, area and gate claims (focus item 5), verified from the published receipts

- **Packet integrity:**
  - `review-evidence/948-r1/MANIFEST.json` at `463845aa`: 456 entries, 456 published hashes match, none missing, none unlisted (20 path-redacted).
  - The packet commit carries no cryptographic signature. The manifest's hashes are the integrity evidence.
- **Routes (`round2b/fit/*/signoff.txt`):** all six builds meet #818's floor (WNS >= +0.030 ns, WHS >= 0) at every corner.
  - 8x8/1if best: ExtraPostPlacementOpt +0.339 / +0.060 ns (Fast +1.636 / +0.017).
  - 1x1/1if best: AltSpreadLogic_high +0.139 / +0.102 ns.
  - The image identity gate agrees on each build. Recipes name the gating flags and 8 threads.
- **Area:** the deltas against round 2 match `SUMMARY.txt`. The depacketizer costs +80 FF at every build, +29 to +40 LUT at 8x8 and +75 to +80 at 1x1. The 8x8's remaining ~+1,100 LUT is cross-boundary movement in unchanged hierarchies, as in rounds 1 and 2. That attribution is the author's reading of the hierarchy receipts, not a controlled experiment.
- **milan_dp render_mutants, run alone:** the excerpt records `milan_dp rc=124 seconds=7200` with 14,148 checks and 0 in-suite failures before the cut. `render_mutants-64e55a59.log` records its control in both modes and four plants caught, "6 checks: 6 PASS, 0 FAIL". That log does not itself record the head or the binaries' hashes (see limits).
- **Twin and gates:**
  - Twin gate log: every plant caught, `twin-fanout-plants rc=0`, `fan-stop-plants rc=0`, `END rc=0`.
  - Yosys `KL_aaf_rx_depacketizer` 54,392 cells and `KL_avtp_rx_monitor_ctx` 12,034, tied-input and tap-purity PASS.
  - Docs steps 104 of 104. xvlog 0 findings. tsn_fuzz AAF campaign 164 pass, artifact fresh.

## Receipts run in this round

All runs were at the exact head in disposable copies, with Verilator 5.050 (wrapper verified: `Verilator 5.050 2026-07-01 rev v5.050`). Receipts are in `receipts/`.

**`avtp_rxmon` suite (`make run`), rc 0:** `rxmon_all.log.gz`
- flat 97/0
- N=4 stack 218/0
- lockstep N=1 116/0 and N=8 119/0
- lockstep mutants 13/13
- format mutants 12/12
- ctxfmt 96/0, mutants 4/4
- fanout 1,205/0, mutants 21/21
- depkt 374/0 at lead 0 and at lead 16, mutants 11/11

**8x8 datapath:**
- obj_nxn8: 4,073/0 (`nxn8_exec.log.gz`).
- `fan-stop-plants`: rc 0, both caught by name (`fanstop.log.gz`, `fan_stop_plant_*_run.log.gz`).

**Probes:**
- Tap bubbles: `probe_tap_bubbles.diff`, `bub_depkt.log.gz` (rc 0), `bub_fanout.log.gz` (rc 2: F1 and the `[FO4]` interval artefact).
- Widened accumulator: `probe_widened_ddrop_pend.diff`, `bub_fanout_widened.log.gz` (only the `[FO4]` artefact left).
- Round-1 RTL attribution: `bub_fanout_r1rtl.log.gz`, `probe_r1rtl_swap.txt`.
- Summary: `fo10_under_bubbles_summary.txt`.

**Gates:**
- `gate_docs_check.log`, `gate_docs_inventory.log`, `gate_check_doc_style.log`, `gate_measure_test_evidence.log`, `gate_lint_rtl.log`.
- `gate_gen_register_reference_REFUSED.log`: the renderer package is absent here, so I relied on the author's step 79 receipt.

**Clone integrity:** `clone_integrity.txt`.
- Head and tree as above.
- Index equals the HEAD tree: 1,947 entries (mode, blob, path).
- Worktree equals the index.
- 0 untracked files.
- Gitlinks: protocol-processor `801ef228`, gptp-processor `1616fc8f`, lwSRP `08ee86e8`, tsn-c-stack `715589c1`, verilog-axis `48ff7a7e`, all checked out at their gitlinks. `external` is not initialised, as in the clone handed over.

**Scripts:** `scripts/` (`README.md` gives the reproduction).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Monitor frame-size verdict `KL_avtp_rx_monitor_ctx.sv:548-594,1078-1084`; depacketizer `:158-235,403-446`; datapath stop gate and meter `milan_datapath.sv:7488,8023-8025`; `[FAN]` STOP and one-channel legs; the two rulings; six fit signoffs | R877-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| RTL | UNCLEAN (F1) | Depacketizer tap attribution, delay, verdict queue, tail and short-frame paths; monitor `ddrop_pend_r`/`dpdu_pend_r` and drain priority; parser fire condition; datapath wiring | R877-2, applied, not clean | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Robustness | UNCLEAN (F1) | Tap-bubble and tap-backpressure probes through `sim_depkt` and the real stack; `[FO8]`-`[FO14]`, `[DT1]`-`[DT4]`; STOP/START ordering | R877-2, applied, not clean | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Tests | UNCLEAN (F1) | `sim_fanout.cpp`, `sim_depkt.cpp`, `sim_nxn.cpp` `[FAN]`, `depkt_mutants.py`, `fanout_mutants.py`, `fan_stop_plant.py`; failing-first receipts; full `avtp_rxmon` rerun | R877-2, applied, not clean | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Docs | UNCLEAN (F1, F2) | `TESTING.md:706`, `DATAPLANE_WALKTHROUGH.md`, `MEDIA_CLOCK_FOLLOWING.md:444`, `FPGA_DESIGN.md`, `REGISTER_MAP.md`, milan_dp README, RTL comments, PR body and both REVIEW READY comments; docs gates rerun | R877-2, applied, not clean | 64e55a59e09339114926c2600056c3ad8b33b9b4 |

RESIDUE RS1-RS5 leave no lens unclean; the manager carries them. S1 is optional.

## Real limits of this round

**No manager source bank exists at this head, and none is inferred.** Source-head execution evidence is the author's published receipts plus the focused runs above. I did not run the sweep, the twin, Yosys, the firmware gate, the full milan_dp suite or any Vivado build; those claims rest on the published receipts.

**Hosted checks:** at the time of review, most hosted contexts at this head were queued or in progress. Only `bdd-conformance`, `changes` and `elaborate-gates-3` had completed (success). None is counted here, and skipped contexts are not executions.

**Probe scope:**
- The tap-bubble probe uses one deterministic pattern (60% of beats, 1-3 cycles).
- In `sim_fanout`, tready-low on the tap was not driven, because the wrap ties it high. `sim_depkt` drove it.
- The round-1 attribution run used the head's bench. Only its `[FO10]` lines are meaningful there.
- The base `15168e14` could not run the head bench (no match vector), so F1 is attributed to round 1, not to the base.

**Published evidence gaps:**
- `render_mutants-64e55a59.log` records the run's result but not the head or the binaries' identity it ran on.
- The full milan_dp log is published only as an excerpt with its sha256.

**Hardware:** no physical calibration or hardware run. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 and F2 back to the author.
- Carry RS1-RS5 to the residue checklist.
- Re-review RTL, Robustness, Tests and Docs at the corrected head.
- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), with its builder and native banks.
- The external review's verdict.
- The completion ledger, an authorized merge, and post-merge containment.

R877-2 FINISHED
