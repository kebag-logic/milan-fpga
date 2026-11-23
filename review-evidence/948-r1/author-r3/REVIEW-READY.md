[A810] REVIEW READY
Commit: `64117b77cb9e5c421717835b5be032b5905c447d` (`pf-948-1`, correction round 3 on `64e55a59`; committed, not pushed).

Answers R877-2 F1/F2 and RS1-RS5 (issuecomment-7080555570), and R878-2 R1 (issuecomment-7080444396).

Changed:
- F1: both per-input pending DEPKT tallies are six bits. Half-full urgency prevents every PDU dispatch path from
  starving their drain; drainage precedes another PDU walk, bind or silence. A pulse coincident with drainage is
  retained. The lockstep reference carries the same scheduling correction.
- LCTX w11 remains two independently wrapping 16-bit vendor-diagnostic fields, outside GET_COUNTERS. Milan v1.2
  5.3.8.10/Table 5.6 specifies 32-bit wrapping standard counters, which remain unchanged. IEEE 1722.1-2021
  7.4.42.2/7.4.42.2.4 and the implemented validity mask map GET_COUNTERS to standard quadlets 0-11, not DEPKT.
- F2/RS1/RS2/RS5: correct FO12's actual lengths and its FO14 reference, state enqueue latency from the tap's
  eighth beat, and reflow the depacketizer header and datapath README. The PR body names R877/R878, describes the
  fixed-cycle shift register accurately, and discloses the stricter timing-floor failures at their actual revision.
- Mailbox contract, firmware, submodule pins and CPU service-budget limits are unchanged.

Failing-first evidence:
- Tests commit `9f8f689c`, with `64e55a59` RTL: `sim_fanout` fails 31 of 1,253 checks, all in new FO15. On this
  candidate all 1,253 pass. FO15 extends the reviewer's intra-frame-bubble overflow burst to 150 PDUs and eight
  inputs. Each input accepts 150, receives 46 correct payloads in order and counts 104 drops; its delivery tally
  also equals the observed payload count.
- Both plants fail `[FO15] every accepted PDU is delivered to the input or one of its DEPKT drops: input 2`:
  the original three-bit/idle-only tally, and the six-bit tally with urgent drainage disabled. Widening alone does
  not clear the test. Review reproduced the loss at round 1; no runtime attribution to the true pre-fan-out base
  is claimed for this counter defect.
- DT5 adds accepted-beat gap coverage: 584/584 cases at both payload leads, also passing on the prior RTL.
  A targeted packet plant freezes data-delay stages on input bubbles while valid advances: control 584/584,
  plant 0/584, exit 1, caught by the named DT5 whole-frame check. This additional probe is not included in the
  repository campaign's 11-plant count.

Validation at the candidate (receipts indexed in `948-a810/round3/receipts/INDEX.md`):
- `make -C tb/verilator/avtp_rxmon run`: PASS. Flat 97, stack 218, lockstep 116/119, ctxfmt 96, fanout 1,253,
  depacketizer 375 twice. Plants caught: lockstep 13, format 12, ctxfmt 4, fanout 23, depacketizer 11.
- `make -C tb/verilator/milan_dp`: rc=0, 14,154 checks, including the completed render mutation phase.
  `milan_dp_mclk`: 173 checks, 36/36 campaign cases. Eight other affected suites pass 548,216 checks.
- Twin, twin-plants, twin-maps, twin-maps-plants, twin-fanout, twin-fanout-plants and fan-stop-plants: PASS;
  zero twin findings and every plant caught by name, including the shared STOP gate.
- Docs workflow: 104/104; lint ratchet 89 <= 89; front-end zero findings. Portable synthesis on the touched
  monitor/depacketizer tops: 12,097/54,392 cells, tied-input and tap-purity PASS.
- AAF generator campaign: 164 pass, result artifact fresh. The four declared ordinary-sweep skips count as
  no execution. This is the affected-suite correction gate, not a new full repository sweep or manager bank.

Fit/timing: All six routes completed at this candidate, each through `vivado-slot.sh`. Recipe: split 50 MHz, one interface, the corresponding TDM shape, xc7a100tfgg484-2, AreaOptimized_high synthesis, ExploreArea optimization and eight implementation threads. Every build and image-identity check passes. #818 selects the best directive meeting WNS >= +0.030 ns and WHS >= 0 at all four signoff corners; both shapes pass. No STOP is triggered.

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

Acceptance: F1 corrected at its cause with failing-first and killing-plant evidence; F2 and all requested
residues addressed; requested source gates pass; both shapes fit and meet #818's best-of-three floor.

Open limits:
- Under overload, urgent drains can delay PDU walks and the admission ring may refuse traffic sooner; every
  accepted PDU still reconciles to delivery or its input's counted store/truncation drop.
- R877-2 S1's optional late-enqueue fail-safe is not implemented. The three-cycle contract and its FO14/FAN tests
  remain in place.
- The prior reviews do not approve this corrected head. The manager owns push/PR update, receipt publication,
  current-base candidate validation, hosted/act gates and independent re-review. No hardware run is claimed.

Packet: `948-a810/round3/HANDOFF-r3.md`, `PR-BODY.md`, this text, and indexed receipts. The working tree is clean;
the three commits have one-line subjects without bodies or trailers. No push, PR edit or merge was performed.

REVIEW READY 64117b77cb9e5c421717835b5be032b5905c447d
