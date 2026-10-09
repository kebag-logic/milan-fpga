[A540] Mark II area plan ([#640](https://github.com/kebag-logic/milan-fpga/issues/640))

## Status

Round 1d is REVIEW READY at `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`.
Executor: [A540]. Reviewers: [R492] internal, [R493] external.
Relates to #640: stage-1 planning; implementation acceptance remains outstanding.
Only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` change.
Comparison base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Round 1d adds two commits after `39258a1486897127288f82fbb1b86333febf6f00`.

## Description

The prior plan omitted the owner's increased firmware-memory allocation.
Both documents now budget 224 KB at about 50 RAMB36 tiles.
They bind the estimate to the recorded baseline and the unchanged reserve.
They name conditional fabric reclamation and require measured checkpoint accounting.

## Round 1d

Assignment: [firmware-memory update](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732).
Decision: [224 KB allocation](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413).
Evidence: [F5 preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432).
Checkpoint duties: [F5 and default-flip ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916).

| Step | Outcome | Commit |
|---|---|---|
| 1 | Decision, preflight sizes, memory ledger, reclamation order and checkpoint duties mirrored | `9b6a04e10499b060eb25dc7c3d489e03c177c566` |
| 2 | Ledger arithmetic recomputed; RAM equation and unchanged LUT estimates recorded | `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783` |

F5's preflight measured 94,688 bytes for shipping 1x1 with one interface.
The largest supported shape with two interfaces measured 147,360 bytes.
Both exclude AECP and its descriptor image.
These are sizing fixtures, not completed F5 or mapped-memory measurements.

The memory ledger starts at 74 RAMB36 and 27 RAMB18, or 87.5 tiles.
Its equation is `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5`.
The 18.5-tile CPU-memory reuse is an explicitly historical estimate.
Further wrapper reclamation releases eleven tiles conditionally, giving 109.5.
The ceiling stays 121.5; the separate reserve stays 13.5 tiles, or 10 percent.

If firmware needs more than fifty tiles, named residual wrapper storage gives way.
The plan lists RX pools, MRP strip, TX slots, timer, trace, validator and control FIFO.
Every replacement buffer is charged, and equivalent diagnostics remain required.
Later M2/M6/M7 RAM conversions yield next, with their LUT savings repriced.
A 4 KiB usable mapping needs 56 tiles for 224 KiB.
That case reaches 115.5 after conditional reclamation, before unpriced buffers.
It is a packing illustration, not a change to the owner's byte threshold.
Partial placement with the same firmware hold reaches 126.5 before extra AECP staging.
It cannot claim full-split reclamation and needs actual allocation evidence.

M0s's two routes, the default flip and M9 reconcile RAMB36/RAMB18 use.
The image census covers both supported shapes at one and two interfaces.
It includes code, data, stack, pools, descriptor images, alignment and staging.
Five largest BSS consumers each receive a reduction option.
The default flip needs a routed image with firmware in block RAM and the reserve intact.
The LUT estimate remains 31,667 centrally, with the 27,567-35,867 range.

## How to reproduce

Compare the plan's baseline and memory tables against `syn/ooc/pp_resource_baseline.json`.
The source measurement is `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
The source checkpoint is `alinx_ax7101_route.dcp` from that recorded measurement.
Its receipt is in `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`.
The CPU-memory estimate comes from `649_RESOURCE_MAP_AND_SENSITIVITY.md`'s SoC census.
The mailbox debit comes from `MAILBOX_SPLIT.md`'s measured-area section.
The linked comments above supply the preflight and the changed firmware limit.

Set `EVIDENCE` to the directory containing the packet's three arithmetic scripts.
Run the command table from the repository root with the pinned Markdown dependencies.
No new synthesis measurement was made in this round.

## How to validate

At `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`, **51/51 commands returned 0**.
The campaign used eight concurrent workers, separate log/rc files and no shell pipes.
`make` used `-j16`; required submodule roots were verified before the gates.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |
| recompute_ledger | `rtk proxy python3 "$EVIDENCE/recompute_ledger.py" .` | 0 |
| verify_round1c | `rtk proxy python3 "$EVIDENCE/verify_round1c.py" .` | 0 |
| verify_round1d | `rtk proxy python3 "$EVIDENCE/verify_round1d.py" .` | 0 |

The resource self-test passed 260 arms and 500 generated cases.
Its control passed and all 174 mutants were rejected.
The preserved LUT checker passes 174 checks; the scenario checker verifies 54 cells.
The memory checker verifies 80 cells, release partitioning and reserve arithmetic.
`ROUND1D-GATE-RECEIPTS.txt` records command results, log sizes and digests.
These are author checks, not independent review verdicts.

## DoD

- [x] Owner decision and F5 preflight incorporated into both documents.
- [x] Baseline, fabric changes, firmware and reserve reconciled in one ledger.
- [x] Named fabric memory yields conditionally if firmware needs more than fifty tiles.
- [x] M0s and default-flip measurement duties recorded.
- [x] Arithmetic and documentation/resource-policy checks pass at the stated head.
- [ ] Independent reviews and publication.
- [ ] Measured implementation fit, timing and qualification.

The historical reuse and packing assumptions still need actual checkpoint measurements.
No RTL, interface, parameter, record, policy-value or gate implementation changed.

## Round 1c

Public readiness receipt: [A540 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081871164).

Assignment: [measurement and review ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590).
Answers [R492-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081481326) and [R493-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081524243).

| Assignment / review | Outcome | Commit |
|---|---|---|
| Step 1, R492-1-F1 | M0s owner, two steps, dependencies and D7 ordering mirrored | `da590e495` |
| Step 2, R492-1-F2 | Correct units, unowned remainder, explicit repricing and ledger | `72ee30833` |
| Step 3, R492-1-F3 | Inclusive no-split, partial-flip assumptions, both bars and residual gaps | `72a215f17` |
| Step 4, R492-1-R1/R2/R3/R4; R493-1-R1/R2 | Shortened prose, M3 basis table, linked authorities, historical tense and blank-line fix | `30b539ad8` |
| Step 5, R492-1-S1/S2 | Exact core reproduction command and surviving M2 FIFO scope | `cee00f59f` |
| Final wording check | Three new sentences shortened | `39258a148` |

The Round 1c assignment and both reviews are addressed in documentation.
M0s belongs to the manager's resource bench. Its first route selects F0-F4 with fabric AECP; its second follows F5's merge. Both precede week 4 and the default flip. D7 compares M0s figures with the last accepted record; later lanes also show their matching-placement delta. Missing integration or measurement is a missed checkpoint, not a pass.

M8a now credits 1,000 LUTs (400-1,500). The 823 controller and 873 PHY figures count pre-packing cells. The 3,231 anonymous cells receive no credit. Explicit 50/75/100 percent packing assumptions, less 400/250/100 LUT replacement costs, produce the rounded cases. These assumptions need routed validation.

Full split finishes at 31,667 LUTs centrally, 35,867 conservatively and 27,567 optimistically. All clear 38,040 and 37,659 arithmetically. Without M8b, conservative full split is 37,167.
No split including M3/M10 reaches 41,867 centrally; every priced case misses both bars.
Partial split with F5 unqualified reaches 37,957 centrally: 83 below the requirement, 298 above the planning-margin bar. Conservative partial is 43,557; optimistic partial is 32,557. Without M8b, central partial is 39,657. The manager must qualify F5 or commission additional redesign against the published gaps.

M2 names the retained MAC packet/CDC and CSR AW/W/B/AR/R FIFOs. DDR3, core/protocol-memory bridges, mailbox rings and media/gPTP tables receive no overlapping M2 credit. Already mapped block RAM supplies no second saving.
The L11b section contains source sizes and digests, all Tcl inputs/options, and the serial lock-held reproduction command. Shell syntax passes, and all three command traces equal the retained originals under a Tcl recording harness. No synthesis was executed.

## Evidence

The baseline remains the recorded measurement of `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
The three endpoints are unchanged: 50,267, 23,179 and 30,135 LUTs.
Source receipts are in `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`.
Round 1c adds no Vivado measurement.

At Round 1c head `39258a148`, **48/48 commands returned 0**.
They used the pinned Markdown environment and initialized submodules.
The campaign used separate logs/rc files, eight concurrent workers and no shell pipes.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |

The adapted reviewer arithmetic checker passes 174 checks.
Its preserved original and adaptation diff show the changed assumptions.
A supplementary recomputation checks all 54 scenario cells in both documents,
M8a rounding, partial ownership costs, conditional-core cases and unchanged records.
All documented shell blocks parse; all three Tcl command traces match the retained originals.
The trace check executes no synthesis.
These results are author evidence, not review verdicts.

## Round 1b history

Round 1b merged the assigned dev revision and incorporated the placement decisions.
It introduced the recorded baseline, split accounting and D7/D8 planning contract.
Round 1c supersedes its M8a estimate and fallback arithmetic.
All new commits descend from `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970`.
No history was rewritten.

## Remaining obligations

The manager carries remaining presentation residue to #495 at merge.
The packet's `RESIDUE-495.md` lists those observations.
Corrected-head independent reviews, publication and hosted/replica acceptance remain.
The merge candidate still needs its required validation.

Implementation must prove M0s integration and both routed placements, F5 memory capacity,
bounded core service, F2-F5 suite/bench qualification and final routed fit/timing.
M8b remains conditional. Only qualified functions may change shipping placement.
No RTL, interface, parameter, record, policy-value or gate implementation changes occur here.
