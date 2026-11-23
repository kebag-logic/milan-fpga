[A810]

## Contents

- **[Status](#status)**: candidate and validation state.
- **[Linked Issue / roles](#linked-issue--roles)**: task and reviewers.
- **[Description](#description)**: behavior, corrections and evidence.
- **[Authoritative references](#authoritative-references)**: requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout.
- **[How to validate](#how-to-validate)**: commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: remaining limits.
- **[Definition of Done](#definition-of-done)**: review and merge bar.

## Status

Correction-round source and route gates PASS at `64117b77cb9e5c421717835b5be032b5905c447d`.
Both shapes pass #818's best-of-three floor. Published branch `948-rx-fanout` targets `dev-soft-core`;
the correction is committed locally on `pf-948-1` for the manager to push.

The requested affected suites, twin, plants and documentation gates pass. Independent re-review and the
manager's candidate/hosted validation remain outstanding. The prior reviews cover `64e55a59`, not this correction.

## Linked Issue / roles

Closes #948
Relates to #665

Executor: `[A810]`
Internal cleared-context reviewer: `[R877]`
External reviewer: `[R878]`

## Description

When several STREAM_INPUTs bound to one talker stream, the parser selected only the highest matching input.
The other inputs stopped receiving. One received PDU now reaches every bound context, with each input's own
format verdict, counters, media-clock selection and payload tag.

| Component | Resulting behavior |
|---|---|
| `avtp_stream_parser.sv` | A registered match vector identifies every enabled matching context. The highest-index output remains available for diagnostics. |
| `KL_avtp_rx_monitor_ctx.sv` | One queued PDU bundle is walked once per matched context. Each input receives its own format/sequence verdict and counters. An enqueue pulse and a completed accepting-context mask drive the depacketizer. |
| `KL_aaf_rx_depacketizer.sv` | Store each frame once; replay it for each accepting input with that input's tag. A four-entry verdict queue associates the stored frame with its accepting mask. Store-overflow and truncated-payload drops are charged to each accepting input. |
| `milan_datapath.sv` | Apply STOP independently to each input's accepting bit. A stopped input still counts FRAMES_RX; other inputs sharing the stream continue receiving. Select the followed media-clock input from the match vector. |

The mailbox contract, firmware and CPU service-budget bounds are unchanged.

**Frame-boundary corrections found by review.** The non-multiple-of-eight tail defect predates #948 and was
found by review (R878-1 F2). A hold-only final beat now carries its own tlast. Admission also checks the bound
input's full expected frame size: channels per frame times samples per frame times sample octets. An off-size
PDU is discarded whole per input, before payload transfer, and counted as UNSUPPORTED_FORMAT. The following
valid PDU retains its boundaries and input tag.

The shortest-frame defect also predates #948. A probe through each revision's own receive stack measured the
shortest delivered frame as 98 octets at the true base `15168e14`, and 82 octets at both `4ceba3d4` and `e8252323`.
Round 1 therefore improved that boundary but still lost legal short frames. The corrected store follows the tap
by a fixed three-cycle shift register, each stage carrying its beat's valid. Every legal frame from the Ethernet
minimum up can receive its enqueue verdict before its stored tlast, including the one-channel 48 kHz Base format
(62 octets untagged, 66 tagged). The three cycles start when the tap carries the eighth beat: the parser's input
register, registered match, then registered monitor pulse.

**Round 3 corrects the drop-tally cause (R877-2 F1).** Pending deliveries and drops used three-bit accumulators
that saturated when PDU walks starved their drain. Each pending tally is now six bits; when any reaches half full,
drainage takes priority over another PDU walk, bind or silence. All three PDU dispatch paths honor this priority.
The read-modify-write drains the captured count and retains a pulse arriving on its completion cycle.
Widening alone is insufficient: the separate six-bit/idle-only plant fails the new burst test.

The LCTX w11 DEPKT word remains a vendor diagnostic with two independently wrapping 16-bit fields. It is outside
GET_COUNTERS. The standard Stream Input counters remain 32-bit wrapping counters; the response's validity mask
selects quadlets 0-11. No mailbox-contract change is involved. The lockstep reference carries the same scheduling
correction; the integrated payload/drop scoreboard supplies an independent conservation oracle.

**Tests and review corrections**

| Evidence | Result |
|---|---|
| Failing first, FO15 on `64e55a59` RTL | 31 of 1,253 checks fail, all in the new 150-PDU burst with intra-frame bubbles. With the fix, each of eight inputs accounts for 150 accepted PDUs: 46 delivered and 104 dropped; all 1,253 checks pass. |
| Two counter plants | Original three-bit idle-only tallies, and six-bit tallies without urgent drainage: each fails `[FO15] every accepted PDU is delivered to the input or one of its DEPKT drops: input 2`. |
| DT5 gap coverage | 584 cases pass at both payload leads, including tvalid gaps, held beats with tready low, tagged/untagged payloads and output stalls. This also passes on the prior RTL. A packet probe freezing data-delay stages on input bubbles fails DT5 by name, 0/584, while its control passes 584/584. |
| Receive-monitor suite | Flat 97, stack 218, lockstep 116/119, context-format 96, fan-out 1,253, direct depacketizer 375 twice. All pass. Mutation campaigns catch 13 lockstep, 12 format, 4 context-format, 23 fan-out and 11 depacketizer defects. |
| Datapath suites | `milan_dp`: 14,154 checks, rc=0, including the completed render mutation phase. `milan_dp_mclk`: 173 checks and 36/36 campaign cases. Eight other affected suites: 548,216 checks, no failures. |
| Twin and plants | Zero twin findings; map, fan-out and STOP plants caught by name. STOP-one-of-two/START keeps the other input receiving while the stopped input still counts FRAMES_RX. |
| Documentation and structural gates | 104/104 documentation steps; lint 89 within ratchet 89; front-end zero findings; portable synthesis passes for both touched tops (12,097 and 54,392 cells). Tied-input and tap-purity checks pass. |
| Generator campaign | AAF field campaign 164 pass and fresh result artifact. Four declared skips in the ordinary small-suite run count as no execution; the separate AAF run supplies its covered arm. |
| F2 and residues | TESTING names FO12's actual lengths 81, 66, 99, 60, 93, 70, 63 (every remainder 1-7). Latency starts at the tap's eighth beat. FO12's comment points to FO14's short frames; the header/README paragraphs are reflowed. Reviewer names and shift-register wording are corrected here. |

**Fit and timing**

All six routes completed at this candidate, each through `vivado-slot.sh`. Recipe: split 50 MHz, one interface, the corresponding TDM shape, xc7a100tfgg484-2, AreaOptimized_high synthesis, ExploreArea optimization and eight implementation threads. Every build and image-identity check passes. #818 selects the best directive meeting WNS >= +0.030 ns and WHS >= 0 at all four signoff corners; both shapes pass. No STOP is triggered.

| Shape | Directive | Slow WNS / WHS ns | Fast WNS / WHS ns | LUTs | FFs | Slices | BRAM | DSP | Delta vs round 2b: LUT / FF / slice |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 8x8/1if | ExtraPostPlacementOpt | +0.272 / +0.044 | +1.526 / +0.013 | 44,103 | 51,272 | 15,691 | 94 | 13 | -1,058 / +57 / -15 |
| 8x8/1if | ExtraTimingOpt | +0.152 / +0.102 | +1.660 / +0.036 | 44,099 | 51,270 | 15,708 | 94 | 13 | -1,014 / +57 / +577 |
| 8x8/1if | AltSpreadLogic_high | +0.102 / +0.102 | +1.660 / +0.036 | 44,072 | 51,269 | 15,646 | 94 | 13 | -1,092 / +55 / +516 |
| 1x1/1if | ExtraPostPlacementOpt | +0.193 / +0.102 | +1.636 / +0.036 | 32,768 | 42,805 | 13,989 | 79.5 | 13 | -102 / -33 / +243 |
| 1x1/1if | ExtraTimingOpt | +0.054 / +0.102 | +1.687 / +0.036 | 32,765 | 42,804 | 14,297 | 79.5 | 13 | -155 / -38 / +80 |
| 1x1/1if | AltSpreadLogic_high | +0.020 / +0.102 | +1.687 / +0.023 | 32,778 | 42,804 | 14,299 | 79.5 | 13 | -140 / -39 / +83 |

- **8x8/1if: ExtraPostPlacementOpt**, Slow WNS/WHS +0.272/+0.044 ns; Fast +1.526/+0.013 ns. Both temperatures meet #818's floor. Against the train's archived ExtraPostPlacementOpt record (`8c5e2b4f`): LUTs +1,118, slices -7, FFs +279, BRAM -0.5 tile, DSPs +2.
- **1x1/1if: ExtraPostPlacementOpt**, Slow WNS/WHS +0.193/+0.102 ns; Fast +1.636/+0.036 ns. Both temperatures meet #818's floor. Against the train's archived ExtraPostPlacementOpt record (`8c5e2b4f`): LUTs +54, slices +296, FFs +177, BRAM -0.5 tile, DSPs +2.

- 8x8 ExtraPostPlacementOpt meets #818 but misses the stricter both-+0.030 rule (minimum hold +0.013 ns). Its original signoff rc=1 is retained.
- 1x1 AltSpreadLogic_high misses #818's floor: minimum setup +0.020 ns, minimum hold +0.023 ns. It is not selected.

The table gives whole-build deltas against round 2b at the same directive. The monitor's placed ExtraPostPlacementOpt delta against round 2b is +117 LUT/+54 FF at 8x8 and +25 LUT/+12 FF at 1x1. Whole-build differences also include placement/synthesis changes outside that module; they are measured totals, not a causal area attribution. Recipes, four-corner signoffs, per-clock figures, utilization, image identities and raw artifact hashes are in `round3/receipts/fit/`. The train deltas use its archived utilization receipt; no new full-hierarchy comparison against the retired train build is claimed.

Historical clarification for R877-2 RS4: round 2b's 8x8 ExtraPostPlacementOpt and ExtraTimingOpt builds had
Fast-corner hold +0.017 and +0.024 ns on the unchanged media-clock-restart path. Both met #818's hold floor,
but missed the stricter both-+0.030 rule, as their retained signoff rc=1 records. Those are prior-head results.

## Authoritative references

- #948's ruling of 2026-11-21: deliver each PDU to every context bound to its stream_id; best-of-three fit/timing at both shapes.
- IEEE 1722.1-2021 8.2: independent sink bindings.
- Milan v1.2 4.4.2.2: discard AVTPDUs inconsistent with the configured input format.
- IEEE 1722-2016 4.4.4.10, 7.3.5, Table 9 and I.2.4.1: payload length and AAF format/sample size.
- Milan v1.2 5.3.8.7: stopped-input discard; 5.3.8.10 and Table 5.6: per-input diagnostic counters and wrap.
- IEEE 1722.1-2021 7.4.42.2 and 7.4.42.2.4: GET_COUNTERS validity and STREAM_INPUT fields.
- Milan v1.2 6.4 and Table 6.1: advertised formats, including one channel at 48 kHz.
- #818: select the best of three directives meeting WNS >= +0.030 ns and WHS >= 0 at every signoff corner.
- `REQUIREMENTS.md`, `docs/fpga/DATAPLANE_WALKTHROUGH.md`, `docs/testing/TESTING.md`, and the manager's correction rulings.

## How to get into the same state

```sh
git fetch origin
git checkout 64117b77cb9e5c421717835b5be032b5905c447d
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

Use the versions pinned by the CI environment and the firmware SDK. The candidate becomes fetchable after the
manager pushes it. The evidence packet records the exact input identities and route recipes.

## How to validate

```sh
make -C tb/verilator/avtp_rxmon run
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants twin-fanout twin-fanout-plants fan-stop-plants
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
bash syn/yosys/run.sh --top KL_avtp_rx_monitor_ctx
bash syn/yosys/run.sh --top KL_aaf_rx_depacketizer
```

Expected: no failed runtime checks; `FANOUT N=8: 1253 checks, 0 failures`; direct depacketizer 375 checks twice;
fan-out and depacketizer campaigns 24/24 and 12/12 including their clean controls; zero twin findings and named
plant catches. Run the other affected suites and the documentation workflow steps listed in the round-3 packet.
Each route uses the recorded gating recipe through the shared route slot; select by #818's four-corner floor.

## Known limitations / out of scope

- Urgent counter drains can delay PDU walks during overload. The admission ring may refuse traffic sooner in that
  overload; accepted PDUs still reconcile to delivery or their own counted store/truncation drops.
- The fixed three-cycle store lag is a contract with parser/monitor registering. A future violation could leave a
  verdict entry unresolved and stop readout until reset. R877-2 S1's late-pulse fail-safe remains an optional
  suggestion; FO14 and FAN catch the contract violation.
- USER/reserved sample encodings have no standard octet count here and are sized as four octets. This entity
  advertises none of them.
- One stored frame is replayed for each accepting input; aggregate processing demand grows with that input count.
- Input 0's PDUS window retains the existing shared total. LCTX w11 contains the per-input diagnostic tallies.
- This is source-head correction evidence. Physical calibration, hardware runs, current-base candidate validation,
  hosted acceptance and merge authorization are not supplied by these simulations.

## Definition of Done

- [x] Linked Issue acceptance criteria are implemented
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at this candidate
- [ ] External review is positive at this candidate
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
