[R629] NEGATIVE - exact head 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb

External independent review R629-2 of issue #726 / PR #729. All five lenses were applied to the full source delta and the Round 2 corrections. The prior required source corrections are verified. One new MINOR remains: the revised snapshot checker falsely fails a valid receive-publication boundary. This affects Robustness, Tests and Docs; no RTL packet-count or reset defect was demonstrated.

Reviewed tree: `037ca71afbbb78009f8116a6f1227b81d38af79b`. Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Round 2 delta: `acadfacd52c6daabf892d6ebe99da11ca06748cb..37944f8ac9d1a2212a3a32f36d921434ea0cbdeb`.

Authority reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README, frozen acceptance and public decisions, requirements/interfaces, the full diff/history, then public executable evidence. Prior public findings were consulted after the independent diff pass. The governing decisions are the [packet ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), [reference-standard addendum](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), [assignment](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), [window ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604), and [Round 2 scope](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6129163001). Full standards PDFs were not independently retrieved; the explicit rulings govern this review.

**R629-2-F01 | MINOR | Robustness, Tests, Docs**

Artifact: [`tb/tools/torture_campaign.py:326`](https://github.com/kebag-logic/milan-fpga/blob/37944f8ac9d1a2212a3a32f36d921434ea0cbdeb/tb/tools/torture_campaign.py#L326), with its revised contract at lines 305-307 and 1363-1369; `tests/features/counters_contract_milan.feature:190`; PR body, Round 2 snapshot statement.

Authority/evidence: Round 2 deliberately keeps single-snapshot differences diagnostic because AAF FRAMES_RX is published in batches. `KL_avtp_rx_monitor_ctx.sv:179-183,637-642,1154-1173` implements that contract. The retained `if frx and total > frx` guard excludes zero, so a valid unpublished total falls into FAIL. The revised docstring and assertion description incorrectly promise that a lower FRAMES_RX snapshot is inconclusive without excluding this reachable boundary.

Independent reproduction drives three real AAF packets through the existing parser/context wrapper, with no counter seeding or RTL changes:

| Observation | TIMESTAMP_VALID | TIMESTAMP_NOT_VALID | FRAMES_RX | Actual checker result | Required result |
|---|---:|---:|---:|---|---|
| Before publication | 3 | 0 | 0 | FAIL | Diagnostic/inconclusive |
| After publication | 3 | 0 | 3 | PASS | PASS |

Receipts: `receipts/snapshot-rtl.log`, `receipts/snapshot-probe.log`, `receipts/snapshot-probe.rc`. `scripts/probe_snapshot.py CHECKOUT PACKET` exits 1 for the checker-contract mismatch; its RTL checks all pass. This is a retained boundary defect in the newly revised checker, not a new RTL failure.

Impact: a valid early counter snapshot is reported as a packet-counter defect. The passing standing scenario covers a lower nonzero FRAMES_RX, leaving zero untested. This changes a verdict and is not prose RESIDUE.

Required outcome: treat a lower, unpublished zero FRAMES_RX as inconclusive, without dividing by zero. Add the real startup boundary to the standing contract. Preserve all-zero/unclaimed non-evidence handling, settled packet identity, and FAIL for interval-rate FRAMES_RX over a measured flowing window. Keep the description consistent with that behavior.

Verification: the receiver-backed probe must pass the diagnostic contract; a standing zero-publication regression must detect restoration of the retained guard. The full behavior gate, grader self-tests, and receive-law mutation control must remain green. Re-review the corrected head under Robustness, Tests and Docs.

**Prior public finding dispositions**

| Finding | Original severity and lenses | Disposition at this head and evidence |
|---|---|---|
| R629-1-F01 / R628-1-F1 | MAJOR, Tests | Source defect resolved. `tests/steps/counters_contract_steps.py:601-625` checks all ten counters and six retained flags. The byte-identical published R629-1 reproduction passes. All 17 source controls detect their plants and pass omission controls, including retained flag/counter resets and the bind-edge rule. BDD passes 405 scenarios / 1,971 steps without failures or skips; its command/result are named in the PR. Exact-head hosted `bdd-conformance` succeeded. Aggregate acceptance remains separate. |
| R628-1-F2 | MINOR, Tests, Docs | Resolved. `stream_counters.hpp:105-160` verifies clear wire TU/MR, zero TU/MR counters, one initial start and no stop at both shapes. All output row-windows pass. `tx-nodirty` fails OUTPUT_CADENCE 16 times and escapes when only that group is omitted. `stream_counters.py:161-170` requires baseline TX/RX/CADENCE failures; both baseline runs satisfy it. The measurement note identifies both output conditions. |
| R628-1-F3 | MINOR, Docs | Resolved. `tb/verilator/milan_dp/README.md:465,499,587,1158` now describes packet totals, the current licence checks and CRF packet wrap. Historical measurements remain historical. All five documentation gates pass. |
| R628-1-F4 | MINOR, Docs, Tests | Its required law correction is resolved. The law table and trap (3), `torture_campaign.py:442`, and the flowing-window scenario at feature line 410 follow Table 7.157. The interval-law plant is rejected and its omission control passes. F01 above is a separate boundary defect in the revised snapshot treatment. |
| R629-1-F02 | RESIDUE, Docs | Resolved. The captured published PR body no longer contains the stale sentence “No push or PR action has been performed.” |
| R628-1-S1 | SUGGESTION, Robustness | Retained as optional: CRF bind-rise precedence can discard a coincident accept. The existing source states the ordering; no alignment change was made. This suggestion does not affect coverage. |
| R628-1-S2 | SUGGESTION, Tests | Retained as optional: derive the unbind fixture's silence bound from the clock parameter. The current bound remains correct for its existing build. This suggestion does not affect coverage. |

**Reviewer-owned lens evidence and ledger**

[R629] PASS Conformance - `KL_talker_diag_ctx.sv:207-258`, `KL_avtp_rx_monitor_ctx.sv:637-642,946-951,1154-1173`, `KL_crf_rx.sv:487-490,644-690`; `receipts/frames-only-1.run.log` and `frames-only-8.run.log` - Checked packet totals on all AAF/CRF outputs and inputs, 32-bit wrap, talker-start reset, bind reset and unbind retention against the rulings. Counter changes enter the existing scheduler; the finite steady windows obey the prescribed cadence and spacing. Bench acceptance remains pending by assignment.

[R629] PASS RTL - the three counter engines above; `hdl/milan/milan_datapath.sv:3155-3170,3300-3322,7924-8020`; pinned `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449` - Checked event decoding, same-cycle TX start precedence, 32-bit accumulation and serial publication, CRF reset precedence, deferred CRF completion, descriptor arbitration and scheduler timestamps. No clocks/crossings or module interfaces are added. AVB_INTERFACE producer/throttle, firmware implementation and submodule pins are unchanged.

[R629] UNCLEAN Robustness - `tb/verilator/tkdiag/sim_main.cpp`, `tb/verilator/crf_rx/sim_main.cpp`, `tb/verilator/avtp_rxmon/sim_main_nx.cpp`, `sim_lockstep.cpp`, `stream_counter_f5.cpp`, and `receipts/snapshot-probe.log` - Reset, tick-boundary, stop/unbind, malformed/foreign input, isolation, wrap, batch saturation boundary and mailbox stall paths were applied. F01 leaves the snapshot boundary unclean.

[R629] UNCLEAN Tests - all changed harnesses, the counter-contract feature/steps, nine parent and two mailbox mutation/omission pairs, BDD and grader self-tests - The named controls pass, but the new receiver-backed probe establishes F01's missing boundary coverage.

[R629] UNCLEAN Docs - REGISTER_MAP, `726_STREAM_COUNTERS.md`, the dated Milan audit, five findings notes, the suite and firmware READMEs, the executable law table, checker descriptions and captured PR body - Packet/reset/window descriptions and dated history were checked against code and receipts. F01 leaves the revised snapshot description false at zero.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Counter engines; public packet/reset/window rulings; both parent shapes | R629-2 | 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb |
| RTL | CLEAN | Counter arithmetic/reset blocks; parent event mux/arbiter; pinned scheduler; source hashes and implementation receipts | R629-2 | 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb |
| Robustness | UNCLEAN | Focused reset/wrap/isolation/stall tests; snapshot boundary, F01 | R629-2 | 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb |
| Tests | UNCLEAN | Changed tests; BDD; packet/window fixtures; mutation controls; snapshot checker, F01 | R629-2 | 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb |
| Docs | UNCLEAN | Current contracts, measurement note, historical notes, READMEs, law table and revised snapshot description, F01 | R629-2 | 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb |

This ledger records source-review results; it does not release the merge.

**Independent execution and measurements**

The prescribed simulator reported version 5.050 before execution; its entrypoint hash is recorded in `receipts/simulator-identity.json`. Campaigns ran concurrently in foreground-owned processes, with two parent builds at a time and bounded compiler workers. All generated/build/probe trees are under `scratch/`. No source fix was made.

| Focused check | Result |
|---|---|
| Talker diagnostics | 99 checks, zero failures |
| CRF receiver unit | 14,287 checks, zero failures; 1,086 accepted PDUs pinned |
| AAF NxN stack | 119 checks, zero failures |
| AAF lockstep/soak at N=1 and N=8 | 36 checks each, zero failures |
| Output-only parent fixtures | 110 shipping / 481 largest checks, zero failures |
| Firmware mailbox windows | Both shapes pass with two recipients and a 2 ms stall |
| Behavior suite | 405 scenarios, 1,971 steps; no failures or skips |
| Grader self-tests | 78 pass |
| Prior bind reproduction; source controls | PASS; 17 reset/edge controls and receive-law control detect and escape as required |
| Documentation / capture guard | All five documentation gates and the capture guard pass |
| Supplemental snapshot contract | FAIL, F01; underlying receiver behaves as documented |

The two renderer-dependent gates initially refused missing dependencies. They passed using the repository's hash-locked dependencies installed only in the packet's disposable environment; both initial refusals and final results are retained.

| Shape | Recorded row-windows | Graded row-windows | Output graded rows | Notifications per graded row | Minimum gap | Maximum gap | Maximum service |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping TDM8 | 40 | 24 | 12 | 1 | 1000.996 ms | 1001.867 ms | 3.263 ms |
| Largest TDM32 | 180 | 108 | 54 | 1 | 1000.982 ms | 1012.029 ms | 14.058 ms |

The fixture uses actual parsing, counter engines, descriptor arbitration, processor and response memory; departures are completed frames at the parent MAC interface. Every stream descriptor and both recipients are graded in windows 2-4. Windows 0-1 are recorded startup transients. Protocol time is compressed to 1000 cycles/ms; clocks run together. Service runs from dirty-and-eligible to the final recipient's MAC tail. Each row's gap is checked against its own measured service time. This establishes the stated finite windows, not indefinite wall-clock cadence or physical timing.

Shipping AAF/CRF TX totals are 799/101; largest-shape AAF totals are 800 each and CRF is 101. Every input returns 500 received packets, preserves its unbind total and clears on rebind. Output restart/wrap and the 65,534-plus-three AAF batch boundary pass. Under frames-only conditions, every output has clear wire TU/MR and zero TU/MR counters. The baseline's output condition is explicitly uncertain; those baseline output notifications are not proof of the new packet-event path.

`receipts/receipt-audit.json` recomputes window and mutation totals. Nine parent plants require named TX, RX, TX_RESET, RX_RESET, CADENCE, RATE or OUTPUT_CADENCE failures and a passing omission run. Both mailbox plants likewise require their named cadence/rate failures and omission passes. Crashes and build failures do not count as detection. Existing unbind-order and licence changes were also reviewed against the published integration and control receipts.

**Published evidence and real limits**

The [immutable public source evidence](https://github.com/kebag-logic/milan-fpga/tree/995bc12029480944568d6af441482965e47bb595/review-evidence/726-r1) supplies the author's gate receipts. Five recorded image-input hashes and all eight Round 2 source hashes match this checkout (`receipts/source-input-audit.json`). Round 2 changes no production RTL, firmware, configuration or gitlink. The only firmware-tree change in the full PR is the AECP README, so no new saved-state capture measurement is triggered.

The published routed report records 49,427 LUT, 53,378 FF and 87.5 BRAM tiles. The +35 LUT delta uses the supplied 49,392 baseline, which was not rebuilt here. The recipe is shipping TDM8, part xc7a100t-fgg484-2, AreaOptimized_high synthesis, ExploreArea optimization, ExtraPostPlacementOpt placement and AggressiveExplore physical/routing directives; no seed override appears in the generated recipe. The author reports constrained WNS/WHS +0.451/+0.036 ns. Published Slow/Fast negative-slack reports contain no negative paths. Timing excludes 46 false-pathed inputs and 87 outputs without output-delay constraints; it is constrained-path evidence only. No new implementation run was performed here.

The exact-head hosted snapshot records successful `bdd-conformance`, `verilator-lint`, `docs-check-no-git` and `wire-accountability`; other jobs were queued or running. Physical gPTP was skipped. See `receipts/hosted-checks.json` for capture time and job links. This is observation, not manager acceptance of hosted contexts or the local replica.

No manager source bank exists or is inferred at this head. The author owns source-head execution evidence. The current-dev merge candidate is separate; the manager builds and validates it at the merge turn and links receipts on the PR. The supplied live-dev tip is `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`, distinct from source base `c6bd08c6`.

Only two controller recipients and finite simulation windows were measured. Maximum fanout, physical cadence and instruction-level firmware timing are not proved. The firmware fixture drives observation values/change events through the unchanged core/mailbox adapter. No full parent/processor/gPTP/synthesis/builder bank, container replica, host orchestration, hardware action, commit, push or GitHub write was performed. Physical calibration was NOT RUN; field skips are not hardware proof.

**Pending manager duties**

- Resolve F01 and obtain independent re-review at the corrected head for every affected lens.
- Own hosted and local-replica acceptance, including completion of required aggregates.
- Validate the current-dev candidate with the required builder/native/full local banks and publish its receipts.
- Perform merge-turn link-tap cadence, reference-peer reset/count comparison and controller-display acceptance. Complete issue acceptance is not claimed here.
- Obtain the full independent review bar and explicit merge authorization; wait for all review rounds, then perform containment and public issue/project closure as required.

**Checkout and packet integrity**

`verify_checkout.py` checks every tracked blob's raw bytes and executable/symlink mode against the exact tree, independently compares index entries, and verifies all required initialized submodule bytes and pins with replacement objects disabled. The parent has 1,300 verified blobs; the required submodules have 104, 562 and 214. All five gitlinks remain at their original stage-zero pins. The checkout is clean; no restoration of source edits was needed. Final verification is in `receipts/checkout-verification.json`.

Portable entry points are `run_focused.py`, `run_native.py`, `run_f5.py`, `reproduce_contract.py`, `era_controls.py`, `law_controls.py`, `probe_snapshot.py`, `audit_receipts.py` and `verify_checkout.py` under `scripts/`. Pass CHECKOUT/PACKET as their help or positional arguments specify. The snapshot probe deliberately returns 1 at this head. `MANIFEST.sha256` lists publishable scripts and receipts using packet-relative paths. Scratch and unlisted downloaded material are excluded from publication.

R629-2 FINISHED
