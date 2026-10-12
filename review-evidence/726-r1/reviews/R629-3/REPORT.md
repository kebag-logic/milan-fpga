[R629] POSITIVE - exact head e893e4d13d99eb5ba00745f0f5cf74ee847972c2

External source review of issue #726 / PR #729, round R629-3. All five lenses were applied to the full change from `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, including both correction deltas. No open BLOCKER, MAJOR or MINOR source finding remains. One wording-only RESIDUE is recorded below. This is a source verdict, not merge authorization or a claim that hosted contexts, candidate validation or bench acceptance are complete. The review-sequencing limitation below requires manager disposition before this review is counted toward the independent-review bar.

Reviewed tree: `0e94807ebc9c4978bfb173c8d3076f9ddfefc4cf`. The final byte/mode/index audit matches this head, including all five gitlinks and the three initialized required submodules. The checkout has no tracked, untracked or ignored changes. See `receipts/checkout-verification.json`.

The controlling scope is the frozen issue acceptance plus [the packet/reset ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), [the IEEE-reference clarification](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), [the assignment](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), and [the notification-window STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604). These require per-AVTPDU FRAMES_TX/FRAMES_RX on AAF and CRF, modulo-32-bit arithmetic, talker-start and not-bound-to-bound resets, healthy counter-change events, and the existing scheduler's one-second spacing. The [Round 2](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6129163001) and [Round 3](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6131008329) directions were checked explicitly. Repository authority, requirements/interface documentation, full diff/history and public executable evidence were examined in that order; prior public findings were opened after the independent diff pass.

**R629-3-R01 | RESIDUE | Docs**

- Artifact: PR #729 body, Status paragraph, captured in this round.
- Authority/evidence: the body names the published head but still says, “The new commits remain local pending authorized publication.” The PR and exact-head hosted jobs establish publication.
- Impact: stale publication wording only; no measurement, figure, executable result, conformance claim or privacy rule changes.
- Required outcome / exact fix: delete that sentence. Optionally change “Local source head:” to “Source head:”.
- Verification: reread the published Status paragraph and confirm the sentence is absent. Carry to the manager's residue checklist. Under the supplied residue rule this does not make Docs unclean.

[R629] PASS Conformance — `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:209`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:637`, `hdl/ieee1722/crf/KL_crf_rx.sv:487`, `tb/tools/torture_campaign.py:298,734` — Checked packet, reset and window behavior against the rulings and IEEE 1722.1-2021 Tables 7.159/7.157, with Milan Table 5.4's start reset and the listener bind reset retained.

The talker increments FRAMES_TX on every indexed transmit event. A same-cycle start supersedes the old era while retaining that cycle's first transmitted packet. The listener's 32-bit pending accumulator and commit amount preserve every accepted AAF packet across a publication interval; they no longer saturate at 65,535. CRF counts every accepted AVTPDU directly. FRAMES_RX publication may lag TV/TNV without changing its counting law. Start resets TX, bind rising resets RX and retained interval state, and stop/unbind preserve the packet total. MR/TU and the remaining anomaly counters retain their own interval laws. Counters wrap rather than saturate.

The cross-device grader now judges each side by its own packet law. The unchanged public `probe_xside_law.py` accepts the ruled 32,000/32,000 packet pair over four seconds and fails an interval-rate side against that side; both interval-rate sides produce two findings. The published source names still reach the executable licence check. The unchanged receiver-backed `probe_snapshot.py` observes TV=3, TNV=0, FRAMES_RX=0 and gets INFO without division by zero, then observes FRAMES_RX=3 and gets PASS. Diagnostic measured-window rate bands do not replace exact packet accounting or the merge-turn peer comparison.

[R629] PASS RTL — `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:209,245`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:325,947,980,1154`, `hdl/ieee1722/crf/KL_crf_rx.sv:644`, `hdl/milan/milan_datapath.sv:3105,7895`, `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449` — Traced packet events through counter storage, dirty-event arbitration and the pinned notification scheduler.

The widened AAF batch has matching operand/storage widths, and the serial path preserves read/modify/write ordering and bind-wipe priority. Index bounds and context isolation remain intact. CRF's bind block still wipes ten counters and six retained flags and handles lock state last. Healthy TV/TNV and published FRAMES_RX updates mark the input descriptor dirty; every TX packet marks its output descriptor dirty. The parent pending-bit arbiter coalesces events. The unchanged processor scheduler applies 1,000 ms eligibility and completion-based spacing; there is no second stream-counter throttle. AVB_INTERFACE throttling remains separate. No clock, reset, CDC primitive, port interface, processor implementation or gitlink changed.

The naming correction was checked on its merits: `dirty_p_o` now documents “one clk_i cycle per update” and assigns one-second coalescing/spacing to the scheduler. The classifier still reports the existing candidate because the comment includes “second”; its identity remains in `scripts/naming.budget:53`. This is not a removed finding or raised budget. `receipts/naming-disposition.json` and `docs-44.log` record 95 candidates against the same 95 recorded identities.

[R629] PASS Robustness — `tb/verilator/tkdiag/sim_main.cpp`, `tb/verilator/crf_rx/sim_main.cpp`, `tb/verilator/avtp_rxmon/sim_main_nx.cpp`, `sim_lockstep.cpp`, `tb/verilator/milan_dp/stream_counters.hpp`, `stream_counter_f5.cpp`, `receipts/snapshot-probe.log` — Applied start/restart, bind/unbind, stopped traffic, tick-boundary, malformed/foreign packet, reset, isolation, wrap, pending-batch and mailbox-stall checks.

All five focused unit fixtures passed. The lockstep fixtures exercise random resets, window access, counter reads and traffic at one and eight listeners. Their claim is preservation of unchanged outputs and historical dirty pulses; newly required healthy pulses are allowed explicitly. A supplemental pending-batch probe seeds 0xFFFFFFFE, injects three real packets and reads one after publication. The ordinary 65,535-crossing check also passes. Near-wrap parent probes count actual emitted AAF/CRF packets across stop/start. The snapshot boundary is covered by both a real receiver probe and a standing regression that fails if the old guard is restored.

[R629] PASS Tests — `tb/verilator/milan_dp/stream_counters.py`, `stream_counters.hpp`, `stream_counter_f5.py`, `stream_counter_f5.cpp`, `tests/features/counters_contract_milan.feature`, `tests/steps/counters_contract_steps.py:601`, `tb/tools/torture_campaign.py:4101,4330`, `receipts/measurement-audit.json`, `receipts/contract-controls.json` — Checked independent observables, baseline failures, named mutation detection and omission escapes, including every new plant.

The parent fixture observes outgoing MAC AVTPDUs and decoded AECP notification completions after two real controller registrations. It covers every descriptor/recipient row at both shapes, including CRF. Five fixed windows are recorded; windows 0 and 1 retain registration/startup transients and windows 2–4 are graded. Service delay is measured for each relevant row. Protocol time uses the documented 1,000-cycles/ms acceleration; these are simulation milliseconds, not hardware timing measurements.

| Shape | Graded row-windows | Notifications in every graded window | Minimum / maximum gap | Maximum measured service |
|---|---:|---:|---|---|
| Shipping, 2 inputs + 2 outputs, two recipients | 24 | 1 | 1000.996 / 1001.867 ms | 3.263 ms |
| Largest, 9 inputs + 9 outputs, two recipients | 108 | 1 | 1000.982 / 1012.029 ms | 14.058 ms |

Both ordinary and frames-only conditions reproduce these measurements. Frames-only checks clear wire TU/MR, zero TU/MR counters, one initial start and no stop, so FRAMES_TX is the only changing steady-window output counter. Shipping TX totals match 799 AAF and 101 CRF wire packets; largest totals match 800 on each of eight AAF outputs and 101 CRF packets. Immutable author baseline receipts show TX=5 and absent healthy input notifications; their named TX/RX/CADENCE failures were checked, not independently rebuilt here.

| Disposable RTL plant | Named failing group | Failing checks | Same defect with that group omitted |
|---|---|---:|---|
| `tx-interval` | TX | 6 | PASS |
| `rx-interval` | RX | 1 | PASS |
| `tx-reset` | TX_RESET | 4 | PASS |
| `aaf-reset` | RX_RESET | 1 | PASS |
| `crf-reset` | RX_RESET | 1 | PASS |
| `rx-saturation` | RX | 1 | PASS |
| `late` | CADENCE | 12 | PASS |
| `rate` | RATE | 32 | PASS |
| `tx-nodirty` | OUTPUT_CADENCE | 16 | PASS |

F5 passes at both shapes with 40/180 recorded row-windows, one notification each and 1,000–1,002 ms gaps. Its two-millisecond stall plus one-millisecond polling allowance bounds the result at 1,003 ms. Both F5 late/rate plants fail their named groups and escape when those groups are omitted. This executes the mailbox/core with supplied observations and time; it does not prove instruction timing or a production caller's integration.

Source controls individually remove each of ten counter resets and six retained interval-flag resets: each fails the era-wipe check and escapes when that check is omitted. Restoring the old zero-snapshot guard fails the standing regression (79 other tests pass with it omitted). Suppressing side-specific cross-device findings fails the two relevant tests and passes the other 78 with them omitted. The public reproductions were run unchanged; hashes are in `receipts/probe-provenance.json`.

| Independently executed work | Result / receipt |
|---|---|
| Talker, CRF receiver, AAF NxN, lockstep N=1 and N=8 | 99, 14,287, 119, 36 and 36 checks; zero failures; `unit-results.json` and runtime logs |
| Parent clean shapes/conditions and nine plants | All 13 drivers rc 0; clean checks 98/427 and frames-only 110/481; `counter-jobs-results.json` |
| F5 clean shapes and two plants | All four drivers rc 0; `f5-jobs-results.json` |
| BDD | 14 features, 406 scenarios, 1,977 steps passed; no failures/skips; `bdd.log` |
| Campaign grader | 80 tests passed; `grader.log` |
| Unchanged contract, cross-device and snapshot probes | All rc 0; corresponding probe logs and hashes |
| Reset/guard/side-finding controls and batch wrap | Intended detect/omit controls pass; `contract-controls.json`, `batch-wrap.run.log` |
| Permitted documentation workflow commands | All 79 rc 0; `docs-census.json`, individual command/log/rc receipts |

The docs run includes `measure_naming --check`, `measure_test_evidence --check`, C/C++ and Python idiom gates, their self-tests, and the remaining permitted workflow commands plus no-Git and wire-accountability jobs. No budget changed. Source-reader recognition documents the mutation driver rather than hiding its source reads. Long functions/mutable state/declarations and Python annotations/docstrings were corrected. Initial F5 setup attempts failed because third-party headers were supplied as ordinary include paths; reruns using system include paths passed without source or warning-policy changes. Both attempts remain recorded.

[R629] PASS Docs — `docs/reference/REGISTER_MAP.md:145,866,963`, `docs/testing/726_STREAM_COUNTERS.md`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:220`, the five changed dated findings notes, `tb/verilator/milan_dp/README.md:465,499,587,1158`, `sw/firmware/ctrl/aecp/README.md:55`, `tests/features/counters_contract_milan.feature`, and the PR body — Checked current laws, measurement method/numbers, historical qualifications and evidence limits against the ruling and executable results.

The law table and trap (3) use per-AVTPDU FRAMES_RX and include an interval-rate FAIL scenario. The README packet totals, licence checks and wrap descriptions match the fixtures. Historical measurements in findings 117, 394/387, 629, 667 and B14 are preserved with dated corrections; archived traceability is pinned as history. REGISTER_MAP distinguishes stream change events from scheduler spacing. The firmware README documents the same cadence contract. R629-3-R01 is wording residue only.

| Prior public finding | Disposition at this head |
|---|---|
| R629-1-F01 / R628-1-F1 — MAJOR, Tests | Resolved: unchanged reproduction passes; all ten counters and six retained flags checked; every removed-reset control detected; BDD passes. |
| R628-1-F2 — MINOR, Tests, Docs | Resolved: frames-only outputs at both shapes, named OUTPUT_CADENCE mutation/escape, explicit baseline failure groups. |
| R628-1-F3 — MINOR, Docs | Resolved: all four cited README passages match current tests and laws. |
| R628-1-F4 — MINOR, Docs, Tests | Resolved: law table, trap (3), packet-rate grading and interval-rate FAIL scenario agree. |
| R628-2-F1 — MAJOR, Docs, Tests, RTL | Resolved: all 79 permitted docs commands pass without budget increases; naming identity retained correctly; exact-head hosted docs-check succeeded, including the previously failing and skipped gates. |
| R628-2-F2 — MINOR, Conformance, Tests, Docs | Resolved: unchanged probe accepts ruled pair and rejects each interval-rate side against itself; standing tests detect suppressed findings. |
| R629-2-F01 — MINOR, Robustness, Tests, Docs | Resolved: unpublished zero FRAMES_RX is INFO, settled equality PASS, and the old guard fails the standing test. |
| R629-1-F02 and R628-2 RS1–RS5 — RESIDUE | Prior wording corrections present: old no-push sentence removed; README bit 3/value 8, per-run wording, test banners/FRX totals, wrap wording and self-test description corrected. New Status wording is R01 above. |

This reviewer-owned ledger covers the current source head. It does not clear required hosted contexts or the review-sequencing limitation.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Counter engines; reset clauses; parent packet/window receipts; law/side grader; unchanged public probes | R629-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| RTL | CLEAN | Three engines; standalone monitor comments; parent wiring; pinned scheduler; naming contract; area/timing evidence | R629-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Robustness | CLEAN | Five fixtures; reset/wrap/batch probes; malformed/foreign/stall/isolation paths; zero-publication probe | R629-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Tests | CLEAN | Changed harnesses and BDD steps; plants/omission escapes; grader regressions; 79 docs commands; author receipts | R629-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Docs | CLEAN | Register map; design comments; measurement note; law feature; dated audit/findings; READMEs; PR body with R01 residue | R629-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |

Published area/timing evidence was inspected, not regenerated. The shipping image reports 49,427 LUTs, 53,378 FFs and 87.5 BRAMs; the supplied baseline is 49,392 LUTs, giving +35, below the +200 stop threshold. Published constrained timing is WNS +0.451 ns / WHS +0.036 ns; corner negative-path reports contain no violating paths. These are constrained-path results, not unconstrained I/O proof. The shipping recipe/device/shape were checked. All five recorded implementation inputs match current functional tokens; two files differ only in comments. `receipts/implementation-input-verification.json` records raw hashes and comparison. There is no processor/gitlink change or firmware implementation change; only its README changed. The capture guard passes, so this PR does not trigger a firmware capture re-measure.

The author's [immutable public evidence](https://github.com/kebag-logic/milan-fpga/tree/cf851544c2071f6edc611bf5600e81aec1356541/review-evidence/726-r1) was fetched with Git-blob verification. Its docs ledger records 81 successful commands. The two commands prohibited here—the full builder bank and local-runner self-test—were inspected as author receipts only. The recovered builder receipt names `ed34d0c`, preceding the final documentation-only correction, and retains 19 NOT RUN arms. It is not an independently executed exact-head builder bank. Source evidence is the author's; **there is no manager source bank at this head**. Broader/native bank receipts were examined as published evidence, not rerun under this focused assignment.

At the final exact-head hosted snapshot, `docs-check`, `rtl-fast`, BDD, elaboration, wire-accountability, no-Git docs and all four portability shards had executed successfully. The docs job's naming, test-evidence, Python/C++ idiom and remaining gate steps succeeded. All five exhaustive simulation shards were still in progress. The physical nightly/manual context was skipped. Thus hosted docs green is confirmed at this head; complete exhaustive simulation and hardware evidence are not. A successful scheduling/aggregate context is not treated as evidence that pending/skipped work executed. `receipts/hosted-summary.json` records head, URLs and step states.

Real limits and pending manager duties:

- The finite runs cover the recorded startup/steady windows, two recipients and two shapes. They do not prove indefinite fixed-window phase behavior or arbitrary recipient fanout. Rate bands are a coarse interval-law discriminator; exact hardware packet and peer comparison remains bench work.
- Physical calibration is NOT RUN. Field/environment skips are not hardware proof. Reset comparison, link-tap notification intervals and controller display/reference-peer checks belong to the merge turn.
- The manager owns hosted/local-replica acceptance and must obtain the required exact-head successful contexts, including docs-check, before merge. No local runner, container, full builder/parent/processor/gPTP/portability bank or hardware execution was performed by this review.
- Current-dev candidate validation remains separate. Supplied live dev is `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`; the manager must build the actual merge candidate, run builder/native banks, publish receipts, satisfy both independent reviews and the ledger, then follow authorized merge and post-merge containment. This report does not authorize merge.
- Sequencing limitation: after the independent diff pass, the permitted prior-finding comments were displayed with embedded complete report bodies and ledgers, before this round's verdict and ledger were written. This did not satisfy the requested report-isolation sequence. No private author material or other checkout was read. The manager must decide whether another cleared review is required before counting this review toward that procedural bar.
- Some docs gates generated ignored bytecode and builder outputs in this checkout. After commands completed, these were moved to `scratch/checkout-generated/`; the final checkout audit is clean. Peak unit memory was 5,575,495,680 bytes under the 12 GiB cap, with no OOM event. Foreground orchestrators bounded concurrent jobs; no job remains running.

Portable wrappers/job lists are in `scripts/`. Set `VERILATOR` to the verified 5.050 executable and use Python 3.12.3; F5 also needs system GoogleTest headers/libraries through `CPLUS_INCLUDE_PATH` and `LIBRARY_PATH`. `run_review.py ROOT PACKET JOBS --jobs 2` runs the counter, focused, F5 or docs JSON job lists and retains commands/logs/return codes. `run_units.py ROOT PACKET --jobs 2` runs five fixtures. `contract_controls.py ROOT PACKET` and `probe_batch_wrap.py ROOT PACKET` reproduce extra controls; the latter reuses the clean shipping build. No-Git jobs require a `git archive HEAD` extraction at `PACKET/scratch/no-git`. `fetch_public.py PACKET` retrieves author receipts used by `audit_receipts.py PACKET`; `verify_checkout.py ROOT` verifies bytes/modes/index/gitlinks. Original public probe files are unchanged. Disposable work belongs under `scratch/`.

`MANIFEST.sha256` is the publication allowlist. Runtime and gate receipts are raw unless explicitly identified as selected-field summaries. Full fetch snapshots, compiler/bootstrap noise and disposable trees are outside that allowlist and are not project dependencies. Only listed files and this report are intended for publication. No GitHub write was made.

R629-3 FINISHED
