[A531] STOP — stage 2d required timing margin

Head: `b2c81239f686592b224510c9d4f196a6c7aa7f25` on `645-ring-slip`. Required no-fast-forward merge of dev `fa450d30` is `be3ec6e57a9b22c76daef817c07cae5ade8ca012`. No push.

Ruling 4 in https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410 requires STOP if a required timing directive misses the build-defined bar. ExtraTimingOpt misses the +0.030 ns setup-margin bar:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Margin verdict |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.120 / +0.053 | +1.633 / +0.019 | PASS |
| AltSpreadLogic_high | +0.142 / +0.065 | +1.483 / +0.026 | PASS |
| ExtraTimingOpt | +0.001 / +0.001 | +1.476 / +0.012 | FAIL |

Each fixed timing model was reported at 0 and 85 C; its figures are identical at both power temperatures. All implementation commands return 0, all TNS/THS are zero, and hold meets its nonnegative bar. The required ExtraTimingOpt margin grade returns 1. No critical warnings, rejected implementation constraints, unclocked registers or unconstrained internal endpoints. External I/O coverage limitations remain explicit. The minimum setup path is receive-validator `hdr_src_mac_r_reg[0]` to transmit-arbiter `FSM_onehot_arb_st_r_reg[0..2]/CE` in the 50 MHz processor domain, with 39 logic levels. Its location does not waive the bar. No recovery change, relaxed threshold or extra placement attempt follows.

Completed at this head:

- All 139 existing physical checks retained; four new declaration-accounting checks added. Physical **143/0**, unchanged accounting **40/0**, new planted-control runner **14/0**: **197 checks / zero failures**. Startup and reset each declare exactly five repeated events in one output PDU; measured wire step agrees and both slip counters remain 0. Zero ordering errors elsewhere. Both unannounced outside-PDU repetition and a larger-than-declared step are caught.
- Four unchanged 16-phase arrival campaigns, INTERNAL cases and all five existing controls pass. Zero post-decision slips. At 0..60 us arrival lateness, minimum empty/full margins are **2.565120 / 2.234880 ticks**. No grace interval after the decision PDU.
- Full datapath **11,877/0**, render **329/0**, media-clock **168/0**, changed units and processor-shadow pass. Eighteen render pull-in phases pass with zero slips; one render window is explicitly ungradable. Boundary campaign **81/0** over 564 windows; both setpoint controls caught, unchanged nine-cycle ambiguity, 195 NOT GRADABLE windows earning no law credit.
- Builder returns 0 with required compiler and elaboration checks; one historical Arty area-calibration arm is NOT RUN because its reference report is absent. Portability **55/55** plus structural checks, vendor parser and all **26** final source/documentation gates pass. Final unique integration-log tally is **37,130 checks / zero failures**, with separately reported standalone campaigns retained.
- Fresh routed own-logic conservative bound **113 LUT / 73 FF**, below 120/120. All 73 flops are named. Shared-function exclusions have exhaustive equivalence evidence and a caught planted change. Raw whole-design delta against the identified historical baseline is +659 LUT / +153 FF, separately reported rather than attributed to this lane. Historical isolated logic delta remains +80 LUT / +73 FF.

The startup/reset bound and #396 steady-state scope are documented. Stage 2d changes only the harness and documentation after the required merge. A stale capture-module summary at `hdl/ieee1722/aaf/KL_chan_map_capture.sv:360` still says depth eight; its detailed contract, actual constant, tests and design document say sixteen. This documentation inconsistency is recorded for review under the no-DUT-change ruling.

HANDOFF.md and PR-BODY.md are complete in management output `2026-09-23/645-a531`, with commands, traces, classification, options, area, protocol effects, recommendation and stage2d receipts. The prepared body includes `Closes #645` and `Closes #647`, with bench items retained by the manager. All 134 implementation inputs matched final hashes before removing temporary links. Root and pinned submodules are clean; all jobs have ended. No retained file exceeds 200 KB; larger artifacts have size/SHA-256 receipts.

The four historical full render-mutation failures remain assigned to #657; no claim that they pass. No independent review, hosted gate, hardware/bench acceptance or release qualification is claimed. Work stops at this head pending a ruling on the failed required timing margin.
