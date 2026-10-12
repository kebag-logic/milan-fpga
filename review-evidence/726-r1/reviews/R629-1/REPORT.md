[R629] NEGATIVE - exact head acadfacd52c6daabf892d6ebe99da11ca06748cb

External independent review R629-1 of issue #726 / PR #729. All five lenses were applied. One MAJOR Tests finding remains open. One prose residue is non-blocking. The packet contains reproducible scripts, raw runtime receipts and the reviewer-owned coverage ledger.

Reviewed tree: `c1decf8ae9177a4cc5d3b7700404214f064b494b`. Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. The two source commits were examined, including the final receiver-comment correction. No source changes, commits, GitHub writes, submodule changes or hardware actions were performed.

The authority sequence was AGENTS.md / CONTRIBUTING.md, docs/README.md, the frozen issue and public decisions, repository requirements and interface contracts, the full diff and history, then public executable evidence. Counter-law adjudication follows the [counter ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), [reference-standard addendum](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), [assignment](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), and [window/STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604). The full standards PDFs were not among the retrieved evidence; no alternative interpretation was substituted for those explicit rulings.

**R629-1-F01 | MAJOR | Tests**

Artifact: `tests/steps/counters_contract_steps.py:629`, exercised by `tests/features/counters_contract_milan.feature:515`; changed producer at `hdl/ieee1722/crf/KL_crf_rx.sv:425` and its bind-reset block at line 644.

Authority/evidence: CONTRIBUTING requires passing regressions, and AGENTS.md makes existing regressions part of the Tests lens. This PR removes `iv_frx_r` because CRF FRAMES_RX now counts each accepted AVTPDU. The existing era-wipe assertion still requires that nonexistent flag to be cleared. The exact-head [hosted behavior job](https://github.com/kebag-logic/milan-fpga/actions/runs/38279786042/job/114913979852) fails the same assertion as the independent focused run:

```text
ASSERT FAILED: interval seen flags left standing across the era wipe, each good for one phantom event in the new binding: iv_frx_r
```

The focused command exits 1 with one failed scenario. The source-base flag inventory has no missing reset; the reviewed head fails solely on the removed symbol. See `receipts/counter-contract-bind.log`, `.rc`, `counter-contract-attribution.txt` and `hosted-bdd-excerpt.log`.

Impact: the mandatory behavior regression is red. Its failure prevents the dependent `rtl-fast` aggregate from clearing this run. This is a stale test contract, not evidence that the implemented CRF counter reset fails.

Required outcome: update the era-wipe check to the per-AVTPDU FRAMES_RX implementation and six retained anomaly flags, while preserving meaningful checks of all ten counters, pending anomaly state, bind-only reset, and unbind preservation. Do not restore interval counting to satisfy the obsolete assertion.

Verification: `python3 scripts/reproduce_contract.py <checkout>` must pass at the corrected head. Removing a retained reset must still be detected. The required behavior regression and `rtl-fast` must then pass, followed by independent re-review. This finding belongs to Tests; no packet-law or reset implementation defect was demonstrated.

**R629-1-F02 | RESIDUE | Docs**

Artifact: PR #729 body, Status, final sentence: “No push or PR action has been performed.”

Authority/evidence: the reviewed PR and its exact published head already exist. The sentence is leftover handoff wording.

Impact: stale prose only. Its removal changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and touches no privacy rule.

Required outcome / exact fix: delete that sentence from the PR body.

Verification: read the updated Status paragraph. Carry this item on the residue checklist; it does not leave Docs unclean.

**Reviewer-owned lens results and ledger**

[R629] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:207,245`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:637,1154`, `hdl/ieee1722/crf/KL_crf_rx.sv:487,644`, and `receipts/clean-1-clean.run.log` / `clean-8-clean.run.log` - AAF and CRF transmit totals equal completed MAC AVTPDUs through stop, restart and wrap. Every input returns 500 received packets, retains its unbind total and clears on rebind. MR/TU retain their existing law. Notification windows and spacing were judged against the public ruling, with bench acceptance still pending by assignment.

[R629] PASS RTL - those three counter engines; `hdl/milan/milan_datapath.sv:3163,3300,7924,7968`; pinned `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449` - Reviewed event decoding, same-cycle TX start precedence, wrapping arithmetic, the AAF pending batch and serial commit, reset ordering, CRF completion deferral, per-descriptor dirty accumulation and fair arbitration. No new clocks or crossings are introduced. The processor still owns the one-second spacing. Its source and gitlink are unchanged. AVB_INTERFACE change sources and throttle are unchanged.

[R629] PASS Robustness - `tb/verilator/tkdiag/sim_main.cpp:375,622`, `tb/verilator/crf_rx/sim_main.cpp:1332,1409,1483`, `tb/verilator/avtp_rxmon/sim_lockstep.cpp:390`, `stream_counters.hpp:139`, and `stream_counter_f5.cpp:14` - Applied the reset, stopped-input, malformed/foreign-input, context-isolation, tick-boundary, unbind/timeout, 32-bit wrap, notification-spacing and delayed-mailbox paths. The supplemental pending-batch probe seeds UINT32_MAX-1, receives three real packets, and reads 1 after publication. Feature-disabled/absent descriptor behavior remains bounded by the unchanged parent generate guards and published integration receipts.

[R629] Tests UNCLEAN - `tests/steps/counters_contract_steps.py:629` - F01 remains open. New packet/window checks and all ten new mutation/omission pairs pass their intended controls, but that does not clear the broken existing regression.

[R629] PASS Docs - `docs/reference/REGISTER_MAP.md:145,866,963`, `docs/testing/726_STREAM_COUNTERS.md`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:220`, `sw/firmware/ctrl/aecp/README.md:55`, and the dated notes in findings 117, 394/387, 629, 667 and B14 - Current contracts match the ruling, new measured numbers match regenerated receipts, historical measurements remain intact, and startup/physical/fanout limits are explicit. The archived traceability link is pinned to the old source rather than presenting the old law as current. F02 is prose residue only.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Public rulings; three counter engines; parent packet/reset/window receipts | R629-1 | acadfacd52c6daabf892d6ebe99da11ca06748cb |
| RTL | CLEAN | Counter arithmetic and reset blocks; parent event mux/arbiter; pinned scheduler; published implementation inputs and area/timing receipts | R629-1 | acadfacd52c6daabf892d6ebe99da11ca06748cb |
| Robustness | CLEAN | Tick/reset/wrap tests; stopped/unbound inputs; N=1/N=8 soak; pending-batch wrap probe; mailbox stall | R629-1 | acadfacd52c6daabf892d6ebe99da11ca06748cb |
| Tests | UNCLEAN | All changed test sources; focused unit/integration runs; ten mutation/omission pairs; existing failed era-wipe scenario, F01 | R629-1 | acadfacd52c6daabf892d6ebe99da11ca06748cb |
| Docs | CLEAN | REGISTER_MAP; measurement document; dated audit and five findings notes; firmware README; PR body, F02 residue | R629-1 | acadfacd52c6daabf892d6ebe99da11ca06748cb |

The table records source-review coverage, not completion of the issue or authorization to merge. The exact artifacts and checks behind each row are identified above.

**Independent execution**

The prescribed simulator reported version 5.050 before use; its entrypoint hash and observed version are recorded in `receipts/simulator-identity.json`. Independent campaigns ran concurrently in foreground-owned processes, with bounded compile workers and all build/probe trees under `scratch/`. No full parent, processor, synthesis or builder bank was run by this reviewer.

| Focused execution | Result |
|---|---|
| Talker diagnostics | 99 checks, zero failures |
| CRF receiver unit | 14,287 checks, zero failures; 1,086 accepted PDUs pinned |
| AAF NxN receive stack | 119 checks, zero failures |
| AAF lockstep / randomized soak | 36 checks each at N=1 and N=8, zero failures |
| Parent shipping packet/window fixture | 98 checks, zero failures |
| Parent largest-shape packet/window fixture | 427 checks, zero failures |
| Supplemental AAF pending-batch wrap | 98 checks, zero failures; wrapped total 1 |
| Firmware mailbox windows | Both shapes pass, with two recipients and a 2 ms stall |
| Existing counter-contract bind scenario | FAIL, exit 1; F01 |

The numeric TX census, restart/wrap results, service times and window rows exactly match the author's published clean receipts. Shipping AAF/CRF totals are 799/101; largest-shape AAF outputs each count 800 and CRF counts 101. The published baseline receipts, inspected rather than re-executed here, show the old transmit count of five and zero steady input notifications.

| Shape | Recorded row-windows | Graded row-windows | Notification count per graded row | Minimum gap | Maximum gap | Maximum measured service |
|---|---:|---:|---:|---:|---:|---:|
| Shipping TDM8 | 40 | 24 | 1 | 1000.996 ms | 1001.867 ms | 3.263 ms |
| Largest TDM32 | 180 | 108 | 1 | 1000.982 ms | 1012.029 ms | 14.058 ms |

The method uses real parent parsing, counters, descriptor arbitration, response memory and completed MAC frames. It checks each stream descriptor and each of two registered recipients. Windows 0 and 1 are recorded; only windows 2 through 4 are graded. Protocol milliseconds are compressed to 1000 cycles. Each maximum gap is checked against that descriptor's measured dirty-and-eligible to final-recipient completion time. These results establish the stated finite simulation windows, not an indefinite wall-clock guarantee. The firmware fixture uses the existing core/mailbox with mocked observation values and explicit change events; it does not establish processor instruction timing.

| Plant | Named failing group | Failures/assertions with check | Same plant with only that group omitted |
|---|---|---:|---|
| tx-interval | TX | 6 | PASS |
| rx-interval | RX | 1 | PASS |
| tx-reset | TX_RESET | 4 | PASS |
| aaf-reset | RX_RESET | 1 | PASS |
| crf-reset | RX_RESET | 1 | PASS |
| rx-saturation | RX | 1 | PASS |
| late | CADENCE | 12 | PASS |
| rate | RATE | 32 | PASS |
| Firmware late | CADENCE | 32 | PASS |
| Firmware rate | RATE | 48 | PASS |

All ten were independently executed. Each driver accepted a named assertion failure with executable exit 1, then an omission run with exit 0. Build failures, crashes and unrelated failures were not counted. `receipts/final-receipt-audit.json` recomputes the window and mutation totals. Existing unbind-order and licence campaigns were inspected in the public receipts; the revised short source pause retains the ordering assertions and their demonstrated defect detection.

**Published implementation evidence and limits**

The [public source evidence](https://github.com/kebag-logic/milan-fpga/tree/885f0527d9960b7594c6acc19ce4eb01230a5b53/review-evidence/726-r1) was downloaded from that immutable revision and verified against its Git blob identities. The five measured RTL/config SHA-256 inputs in `author/evidence/implementation-inputs.json` match the reviewed checkout. Source-head gate receipts are the author's evidence. No manager source bank exists or is claimed at this head.

The routed utilization report directly records 49,427 LUT, 53,378 FF and 87.5 BRAM tiles. The +35 LUT delta is against the supplied 49,392 reference, below the +200 STOP threshold; the reference build was not regenerated here. The published recipe uses the shipping TDM8 shape, part xc7a100t-fgg484-2, AreaOptimized_high synthesis, ExploreArea optimization, ExtraPostPlacementOpt placement and AggressiveExplore physical/routing directives. No seed override appears in its generated Tcl.

The handoff reports routed WNS +0.451 ns and WHS +0.036 ns. The published Slow/Fast negative-slack reports contain no negative paths. Endpoint temperature reports are operating metadata, not additional timing models. The reports leave 46 false-pathed input ports and 87 outputs without output-delay constraints; the evidence establishes constrained-path timing only. No new implementation run was performed by this reviewer.

The firmware implementation, saved-state capture inputs, processor gitlinks and lwSRP gitlink are unchanged. The only firmware-tree delta is the AECP README. The author's published capture guard passes; a new capture measurement is therefore not triggered by this diff. The public source receipts also include completed affected integration and synthesis runs, with the final audio-clock result distinct from earlier incomplete attempts. They do not constitute the full required candidate bank.

The exact-head hosted snapshot records the failed behavior job, several completed successful jobs, and still-running/queued jobs. `Physical gPTP` is explicitly skipped. No passing aggregate or completed hosted acceptance is inferred. Physical calibration is NOT RUN, and field skips provide no hardware proof.

**Prior public findings and remaining manager duties**

The independent verdict and ledger were written before the prior-findings lookup. PR conversation comments, review submissions and inline review comments contained no prior public review findings at that lookup. `receipts/prior-public-findings.json` records the empty result. No other reviewer's private report or author-private material was consulted.

F01 requires a correction and independent re-review at the resulting head. The manager must also carry F02 to the residue checklist, accept the hosted/local-replica evidence, obtain both independent reviews and publish the final coverage ledger. Full current-dev merge-candidate validation, including builder and native banks, remains the manager's merge-turn work. Source validation must not be substituted for that candidate validation.

Bench acceptance remains pending: actual link-tap cadence at shipping and largest shapes, reference-peer reset and per-second counter comparison, controller display and the authorized hardware checks. Startup windows, maximum recipient fanout and physical calibration are not proven here. Merge authorization, post-merge containment, authoritative records and issue/board completion remain separate duties. This NEGATIVE verdict authorizes none of them.

Before/after byte audits prove 1,300 parent blobs and 562/104/214 blobs in the required processor, timing-processor and stream-library submodules, together with their modes and exact index entries. All gitlinks match the reviewed head. The parent checkout is clean; no restoration was needed because probes used disposable copies and object trees.

Portable commands are in `scripts/`: run `run_checks.py <checkout> <packet> --verilator <pinned-executable> --phase clean`, then phases `plants` and `f5`; `run_units.py` takes the same paths and executable argument. `probe_batch_wrap.py <checkout> <packet>` reuses the clean shipping model. `reproduce_contract.py <checkout>` reproduces F01. `verify_tree.py <checkout>` proves bytes/modes/index/pins, and `audit_receipts.py <packet>` verifies the recorded measurements. Runtime extracts preserve the original runtime lines; compiler/bootstrap output stays outside the publication manifest. Firmware failure extracts omit only absolute source-location banner lines, preserving every assertion, value and result verbatim; original receipt hashes and extraction details are recorded in `receipts/f5-extraction.json`. Only MANIFEST-listed files and this report are intended for publication; `scratch/` is never published.

R629-1 FINISHED
