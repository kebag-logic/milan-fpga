# HANDOFF: #948 round 3

Status: REVIEW READY; all requested source and route gates complete. Posted once on #948:
https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7086526466
The published body exactly matches `REVIEW-READY.md`; one matching comment was verified. No owned work units remain running.

Candidate: `64117b77cb9e5c421717835b5be032b5905c447d`, tree `0c58762aaf41530ba148e99969f04bfaa3404f17`.
Branch: `pf-948-1`; PR #959 targets `dev-soft-core`. The manager pushes and updates the PR.
Review delta: `64e55a59..64117b77`. No push, PR edit, merge, hardware access or submodule change.

The interrupted session committed all source changes and completed the source gates. Resume checked the saved
receipts against the candidate and clones, retained those results, and added a targeted DT5 plant receipt.
No source changed on resume. `receipts/gates/source-identity.txt` records direct candidate-blob comparisons,
the failing-first clone's RTL/test identities, and original large-log sizes and hashes.

## Review findings and changes

R877-2 is the negative review at issuecomment-7080555570; R878-2 is positive at issuecomment-7080444396,
with the reviewer-label residue. These are prior-head verdicts, not approval of this correction.

| Finding / file:line at the candidate | Change and reason |
|---|---|
| F1: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:356` | Both pending DEPKT tallies become six bits. At half full, `depkt_urg_w` gates every PDU dispatch path (`:486`) and gives the tally drain priority over another PDU walk, bind or silence (`:1045`). Widening alone would still saturate during a long busy interval. |
| F1: same file `:1173` | Drain the captured amount while preserving a pulse on the drain cycle. The two pending totals remain per input. |
| Counter rule: same file `:60`, arithmetic `:725` | Document the two independently wrapping 16-bit LCTX w11 fields. They are vendor diagnostics, outside GET_COUNTERS. Standard Table 5.6 counters stay 32-bit and wrap. `receipts/gates/counter-rule.txt` traces the primary clauses and actual counter mapping. |
| F1: `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:325` | Apply the same pending-tally/drain scheduling change to the single-match lockstep reference. Lockstep is regression evidence; FO15's external conservation oracle establishes the fix. |
| F1: `tb/verilator/avtp_rxmon/sim_fanout.cpp:239`, `:845` | Add intra-frame bubbles and FO15: the reviewer's overflow-burst mechanism extended to 150 PDUs, eight inputs, per-input delivered/drop conservation, delivery tally and payload order. |
| F1 plants: `tb/verilator/avtp_rxmon/fanout_mutants.py:150` | Restore the original three-bit idle-only accumulator, then separately keep six bits but starve the drain. Both must fail FO15 by name. |
| Additional gap coverage: `tb/verilator/avtp_rxmon/sim_depkt.cpp:236`, `:465` | DT5 exercises accepted-beat attribution under tvalid gaps and held beats with tready low. It passes at the old RTL too; it is coverage, not a claimed prior defect. |
| Test inventory: `scripts/measure_test_evidence_readers.py:99` | Describe the two additional fan-out plants so the generated test evidence matches the executable campaign. |
| F2, RS2: `docs/testing/TESTING.md:706` | Name FO12's actual payload lengths (81, 66, 99, 60, 93, 70, 63), each remainder 1-7; specify enqueue latency from the tap's eighth beat; describe FO15/DT5. |
| RS2: `docs/fpga/DATAPLANE_WALKTHROUGH.md:175` | The three cycles start at the tap carrying the eighth beat: input register, registered match, registered monitor pulse. |
| RS1: `tb/verilator/avtp_rxmon/sim_fanout.cpp:703` | Correct the comment to locate eight-to-ten-beat frames in FO14. |
| RS5: `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:29`, `tb/verilator/milan_dp/README.md:1887` | Reflow the two paragraphs; no depacketizer behavior change in this round. |
| R878-2 R1, R877-2 RS3/RS4: `PR-BODY.md` | Name R877/R878; describe a fixed three-cycle register with per-stage valid; disclose the stricter-floor failures with their applicable revision. Replace the old fit figures with this round's measured routes. |

The loss was reproduced by review on round 1 (`4ceba3d4`), using round 1's per-input attribution built on the
older three-bit idle-only accumulators. No runtime measurement of this loss at the true pre-fan-out base is claimed.
The public counter widths, mailbox contract, firmware and CPU service-budget limits are unchanged.

## Commits

| Commit | Purpose |
|---|---|
| `9f8f689cb8` | Failing-first FO15; DT5 bubble coverage; RS1 comment. |
| `4e0f984b76` | Counter/drain correction, matching reference, two plants, counter rule, header reflow. |
| `64117b77cb` | F2 and documentation residues; evidence inventory. |

All three are on `pf-948-1`, one-line subjects, without bodies or trailers.

## New checks and killing plants

| Check | Before / after | Plant and failing words | Receipt |
|---|---|---|---|
| FO15 per-input conservation | Tests commit `9f8f689c` on `64e55a59` RTL: 31 failures of 1,253, all FO15. Candidate: 1,253/1,253. Each input accepts 150, delivers 46 and counts 104 drops. | Three-bit pending tallies with idle-only drain; also six-bit tallies with idle-only drain. Both fail `[FO15] every accepted PDU is delivered to the input or one of its DEPKT drops: input 2`. | `receipts/failing-first/fanout-on-64e55a59-rtl.log`; `receipts/rtl/avtp_rxmon-suite-64117b77.log.gz` |
| FO15 delivered tally / order / case liveness | The new check compares the LCTX delivery half with observed payloads, verifies sent payload order and more than 63 drops. Original RTL also loses delivered counts. | Same three-bit plant loses the delivered tally as well. Payload-order and liveness checks qualify the scenario; they are not separate RTL defects. | Same receipts. |
| DT5 accepted-beat gaps | Old RTL and candidate: 584/584 cases at both leads; full depacketizer run 375 checks per lead. | Resume plant freezes data-delay stages on tap bubbles while valid shifts each cycle. Control 584/584; plant 0/584, exit 1, failing `[DT5] cases whose every output frame is whole, in order, under its index`. | `receipts/rtl/dt5-plant/result.txt`, `plant.diff`, `reproduce.py`, control/plant logs. |

The extra DT5 plant is a portable packet probe, not an extra counted member of the repository's 11-plant
depacketizer campaign. Reproduce it with `python3 receipts/rtl/dt5-plant/reproduce.py <repository> <scratch>`
under the pinned simulation environment, in a separate memory-limited unit.

## Gate table

All paths below are relative to this packet. No skipped arm is counted as an execution.

| Gate / exact command or recipe | Candidate result | Receipt |
|---|---|---|
| `make -C tb/verilator/avtp_rxmon run` | PASS. Flat 97; stack 218; lockstep 116/119; ctxfmt 96; fanout 1,253; depacketizer 375 twice. Campaign checks including controls: 14, 13, 5, 24 and 12. | `receipts/rtl/avtp_rxmon-suite-64117b77.log.gz` |
| `make -C tb/verilator/milan_dp` | PASS, rc=0, 14,154 checks; render mutation phase completed. | `receipts/sweep/milan_dp-64117b77-excerpt.txt.gz` (full original log identified by size/hash) |
| `make -C tb/verilator/milan_dp_mclk` | PASS, 173 tallied checks, 36/36 campaign cases. | `receipts/sweep/milan_dp_mclk-64117b77.log.gz` and summary |
| Default make targets for `aaf_audio_loop capture_coherence follow_ring mbx milan_dp_gm_steps milan_dp_render pp_shadow tsn_fuzz` | All eight PASS; 548,216 checks. Four declared generator/freshness skips contribute zero. | `receipts/sweep/*-64117b77.log.gz`, `small-suites-SUMMARY-64117b77.txt` |
| `make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants twin-fanout twin-fanout-plants fan-stop-plants` | PASS; zero twin findings; every plant caught, shared STOP plant included. | `receipts/twin/twin-gate-64117b77.log.gz` |
| `python3 scripts/lint_rtl.py --check`; `python3 scripts/xvlog_gate.py --check` | PASS, 89 <= 89 and zero findings. | `receipts/gates/lint-ratchet.log`, `xvlog-gate.log` |
| `bash syn/yosys/run.sh --top KL_avtp_rx_monitor_ctx`; same for `KL_aaf_rx_depacketizer` | PASS, 12,097 and 54,392 cells. Tied-input and tap-purity PASS. | `receipts/gates/yosys-*.log` |
| Docs workflow steps | All 104 return 0, including inventory/reference/style checks. | `receipts/gates/docs-steps-64117b77.txt`, `docs-commands.tsv` |
| `TSN_GEN_ROOT=<generator> make -C tb/verilator/tsn_fuzz aaf` | 164 pass; result artifact fresh. This executes the AAF arm skipped by the ordinary sweep. | `receipts/gates/tsn_fuzz-aaf-campaign-with-generator.txt` |
| Fit/timing, both shapes, best of three, through `vivado-slot.sh` | All six completed; selected directive for each shape passes #818 at every corner. | `receipts/fit/SUMMARY.txt`, per-build recipes/signoffs/utilization/identity/artifact hashes |

This is the requested correction-round affected-suite execution, not a new full repository sweep or manager
candidate bank. The firmware gate and CPU-budget images were retained from earlier rounds; this round changes
neither. Hosted/act evidence, current-base merge candidate, independent re-review, push and PR update remain
manager duties. No approval or merge readiness is asserted by these author receipts.

## Fit and receipt integrity

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
The original full train hierarchy is no longer present. Train total deltas use its archived nonempty
round-1 utilization receipt, copied into each current fit directory. Round-2b same-directive deltas use the
archived `64e55a59` utilization receipt. No reconstructed full-hierarchy delta against the train is claimed.
Large reports, images and executables remain outside this packet; their sizes and full SHA-256 values are recorded.
`receipts/INDEX.md` and `MANIFEST.sha256` are generated from the files present after host-path sanitization.

## Remaining limits

R877-2 S1 remains an optional suggestion: a future enqueue-latency contract violation could wedge the read side.
This round does not implement a late-pulse fail-safe. FO14/FAN catch the latency violation. Under counter pressure,
urgent drains add a few cycles per serviced input ahead of PDU walks; the acceptance ring may refuse traffic sooner
in such overload. No normal class-A delivery or counter assertion was weakened.
