[R629] NEGATIVE - exact head 1add0cfbcc778c5292a5935631ca7b47c612b990

External independent review of issue #726 / PR #729, round R629-4. All five lenses were applied to the full change from c6bd08c6f52632c6d33d834ce842ac3cf63f29cc, including the three correction deltas. One new MINOR remains: an executed receive-test explanation still asserts the superseded FRAMES_RX interval law. Two prior findings are retained solely for their still-unobserved required hosted confirmations; their source corrections pass the local reproductions. Numerical packet, reset, wrap and cadence checks pass. Hosted verification limitations and prior-finding dispositions are recorded separately below. This review supplies no merge authorization.

Reviewed tree: 11896ba0ce355e92ac33c444fb8b0f4aeb14554b. Repository authorities, frozen issue scope and public decisions were reconstructed before the diff and history. An independent verdict and artifact-specific ledger were written before reading any prior review report; subsequent receipt reconciliation found F01, which supersedes that preliminary verdict. No private author material or other checkout was used.

The controlling decisions are the [packet/reset ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), [IEEE-reference clarification](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), [assignment](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), [processor/throttle ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604), and [corrected consecutive-gap criterion](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6132483068). The last decision supersedes the earlier fixed-window-grid criterion. IEEE 1722.1-2021 Tables 7.159/7.157 supply the per-AVTPDU law; the Milan talker-start and not-bound-to-bound resets remain.

**R629-4-F01 | MINOR | Conformance, Tests, Docs**

Artifact: `tb/verilator/avtp_rxmon/sim_main_nx.cpp:651`; executed output `receipts/avtp_rxmon-run-2.run.log`, section IV8; captured source and receipt hashes in `receipts/finding-F01.json`.

Authority/evidence: the emitted Table 5.6 explanation says “one interval is +1 - the same law as FRX/SM/TU/UF/MR.” FRX is FRAMES_RX, whose per-AVTPDU law is the central #726 ruling. This is a current explanation printed by the passing receiver regression, without a historical qualifier. The same run correctly checks six received packets as six in IV1. Thus the output asserts incompatible laws for the same counter.

Impact: executable verification evidence still teaches the removed counter interpretation. No numerical assertion or RTL packet-count defect was demonstrated. The finding belongs to Conformance because it makes the wrong counter-law claim, Tests because the executed test emits it, and Docs because it documents the test's asserted contract. It is not RESIDUE under the supplied rule: correcting it changes an explicit clause/law claim and generated test output.

Required outcome: remove FRX from the occupied-interval anomaly list; preserve the +1-per-occupied-interval explanation for SM/TU/UF/MR and late/early timestamps. If FRAMES_RX is mentioned there, state that it counts each accepted AVTPDU and that its total may be published in a batch. No assertion weakening or RTL change is required.

Verification: rerun the receive regression and inspect IV8's emitted explanation. The existing six-packet total must remain six, the anomaly burst checks must remain +1, and the packet-law contract gate must pass. Re-review Conformance, Tests and Docs at the corrected head.

**Applied lenses and source evidence**

Conformance: `KL_talker_diag_ctx.sv:208,249` increments the transmitted-event total and retains a simultaneous first PDU at talker start. `KL_crf_rx.sv:487,644` counts each accepted CRF PDU and preserves the bind reset; stopped-but-bound observation remains active. `KL_avtp_rx_monitor_ctx.sv:329,640,949,1154` carries a 32-bit pending packet total into the existing publication walk. Packet totals, wraps and reset boundaries were checked against the controlling laws and real MAC frames, not interval counts. F01 leaves this lens unclean despite passing numeric checks.

RTL: examined the three changed counter engines and standalone monitor comments, the unchanged parent event mapping and arbiter in `hdl/milan/milan_datapath.sv:3155,3300,3669,7924`, and the pinned processor scheduler in `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449`. Every changed healthy counter marks its descriptor dirty; descriptor mapping includes CRF. Dirty bits coalesce in the existing event path. The scheduler's eligibility and completion timestamp remain the sole rate limiter, preserving #60's throttle intent without suppressing healthy updates. No new clock crossing, processor change, firmware implementation change, configuration change or gitlink change was found. The dirty pulse naming correction describes a one-cycle indication rather than a time-valued port; the naming ratchet passes on its merits.

Robustness: the focused talker, CRF receiver, four-context AAF receiver and one/eight-context lockstep fixtures exercise malformed/foreign frames, rejects, stop/unbind/rebind, simultaneous start/PDU, tick boundaries, per-context isolation, active reset, wrap and preservation of anomaly behavior. The lockstep comparison deliberately permits the newly required healthy dirty pulses while retaining the old event pulses and unchanged outputs. The mailbox fixture exercises its injected stall; it is a firmware fallback test, not proof of a firmware implementation change. The unchanged startup snapshot probe reads TV=3, TNV=0, FRAMES_RX=0 before publication (INFO, null ratio), then FRAMES_RX=3 after publication (PASS).

Tests: examined all changed harnesses, `stream_counters.py:133`, `stream_counters.hpp:173`, `stream_counter_f5.cpp:18`, the behavior feature and steps, law table and bench grading helpers. The parent fixture uses real descriptor images, parser, counters, event arbiter, processor and response-memory/MAC path. It compares counter growth with wire frames, verifies resets and wrap, and isolates FRAMES_TX as the only steadily changing output counter in both frames-only shapes. Mutation drivers require a named behavioral failure, reject crashes/build errors as detection, then require success with only that named check omitted. The inherited make flag failure is reproduced as fixed. F01 remains in the emitted evidence.

Docs: reviewed `docs/testing/726_STREAM_COUNTERS.md:29,51,135`, `docs/reference/REGISTER_MAP.md:149,869,963`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218`, the five dated findings-page notes, suite README passages, firmware event-mask description, archived traceability link, public issue/body and author receipts. Current cadence text uses consecutive gaps plus measured service, with no fixed-grid grading or startup exclusion. Historical silicon observations remain dated and are not recast as current proof. The PR's old local/unpublished status wording is gone. F01 is the remaining current-law contradiction.

**Cadence and executable results**

Protocol milliseconds are 1000 simulation cycles; these are finite compressed-time measurements. Each consecutive per-descriptor/per-recipient gap is graded from the first notification, with spacing at least 1000 ms and maximum gap at most 1000 ms plus that descriptor's measured service. Service is measured from dirty-and-eligible through the final recipient's MAC tail. The final wait is bounded and at least two observations are required, preventing vacuous silence. Notifications after the measurement end are excluded.

| Shape / output condition | Descriptor-recipient rows | Consecutive gaps | Minimum gap | Maximum gap | Maximum measured service |
|---|---:|---:|---:|---:|---:|
| Shipping 1x1, uncertain | 8 | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest 8x8, uncertain | 36 | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |
| Shipping 1x1, frames-only | 8 | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest 8x8, frames-only | 36 | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

The public NOTE timestamps were independently recomputed against each row's own service bound (`independent-receipt-audit.json`). Local uncertain-shape timestamps give the same results (`local-runtime-audit.json`). The recursive target independently ran all four shapes/conditions. Frames-only output rows contribute 16/72 gaps; TU, MR and their wire bits remain zero, with only the initial start and no stop during measurement. The earlier 24/108 figures counted fixed-grid row/windows; they are historical measurements, not the current acceptance test. Descriptive bins remain in the logs and are never graded.

The unchanged published shift launcher was run at starts 0, 200, 300, 800, 900 and 1,000,000 cycles at both shapes: all twelve child exits are zero. The current fixture also exhausts every discrete start through one second per row. The old fixed-grid plant fails PHASE and escapes when PHASE is omitted. Its historical instrumentation patch was retained for provenance but not reapplied: the current fixture already exposes the shift input and timestamp output.

| Local execution | Result |
|---|---|
| `MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1` with scratch output | rc 0 |
| `make -j16 -C tb/verilator/milan_dp counters` | rc 0; all four legs RESULT: PASS |
| Talker / CRF / AAF / lockstep N=1,N=8 | 99 / 14,287 / 119 / 36 / 36 checks; all pass |
| Full BDD gate | 14 features, 406 scenarios, 1,977 steps; zero failures or skips |
| Bench grader offline self-test | 80 tests pass |
| Documentation/focused plan | 74 tasks pass, including the four specifically requested gates and their self-tests |
| Supplemental documentation checks | Imported documentation, parent documentation, offline SDK control and exported no-git checks pass |
| Unchanged prior contract / cross-side / snapshot probes | all rc 0; interval-rate sides fail against the correct side |
| Independent retained-reset controls | all ten counter resets and six retained flags detected individually; other era checks pass when the wipe check is omitted |
| Restored old snapshot guard | exactly the named startup regression fails; 79-test omission control passes |
| Pending receive accumulator | 0xfffffffe plus three real MAC packets publishes 1; pass |
| Mailbox clean N=1,N=8 and three mutation/omission pairs | pass; fixed-grid, late and rate defects detected, each omitted-check escape passes |

| Parent plant | Required group | Named failures | Omission result |
|---|---|---:|---|
| tx-interval | TX | 6 | PASS |
| rx-interval | RX | 1 | PASS |
| tx-reset | TX_RESET | 4 | PASS |
| aaf-reset | RX_RESET | 1 | PASS |
| crf-reset | RX_RESET | 1 | PASS |
| rx-saturation | RX | 1 | PASS |
| late | CADENCE | 4 | PASS |
| rate | RATE | 8 | PASS |
| tx-nodirty, frames-only | OUTPUT_CADENCE | 4 | PASS |
| fixed-grid | PHASE | 8 | PASS |

Public base-source receipts contain exactly 12/54 named TX/RX/CADENCE failures at the two shapes. They were audited, not described as local base-bank executions. Every new parent plant and omission pair was executed locally. Portable plans, drivers, raw runtime logs, return codes and source provenance are included in the manifest.

The naming gate reports 95 recorded candidates; test evidence reports 66 <= 77 suites without a mutation arm, 10 <= 10 unseeded draws, zero unexplained source readers and 3 <= 3 wall-clock-dependent suite files. Python and C/C++ idiom gates pass. No budget was raised. The documentation source-reader additions are disclosed by their actual source-edit/compile/simulate mutation behavior. The local plan intentionally excludes the prohibited full builder bank, compiler-absent builder controls, real SDK installation and host orchestration self-test. It does not claim a complete local workflow execution.

**Prior public findings**

| Prior finding | Disposition at this head |
|---|---|
| R629-1-F01 / R628-1-F1, MAJOR Tests | Resolved: unchanged reproduction passes; the step checks ten counters and six retained flags; all sixteen removed-reset controls detect; BDD gate passes and is named publicly. |
| R628-1-F2, MINOR Tests/Docs | Resolved: frames-only outputs at both shapes, zero unrelated changing output counters, named OUTPUT_CADENCE detection and omission escape. |
| R628-1-F3, MINOR Docs | Resolved: the four suite README passages now describe packet totals or explicitly dated historical observations. |
| R628-1-F4, MINOR Docs/Tests | Resolved: Table 7.157 law table, trap (3), flowing interval-rate FAIL scenario and current grader agree. |
| R628-2-F1, MAJOR Docs/Tests/RTL | Source/local correction verified: all four named gates and related permitted gates pass; no budget increased; pulse naming is semantically correct. Hosted completion is addressed below. |
| R628-2-F2, MINOR Conformance/Tests/Docs | Resolved: the unchanged cross-side probe passes the ruled packet pair and attributes every interval-rate side correctly; standing regressions pass. |
| R629-2-F01, MINOR Robustness/Tests/Docs | Resolved: real unpublished-zero probe passes; the old guard fails its standing check and escapes with that check omitted. |
| R628-3-F1, MAJOR Conformance/Tests/Docs | Resolved under the corrected ruling: consecutive-gap grading, first-notification coverage, exhaustive phase checks, unchanged shift probes, fixed-grid controls, and the three required public texts agree. |
| R628-3-F2, BLOCKER Tests/Robustness | Source/local correction verified: both make exports suppress inherited directory banners, the exact inherited-flag reproduction and recursive counter target pass. Required hosted shard/artifact confirmation is addressed below. |
| R629-1-F02; R628-2 RS1-RS5; R628-3-R1 / R629-3-R01, RESIDUE | Their cited corrections are present: old no-push/local-unpublished body wording removed, bit 3/value 8, per-run wording, specified counter banners, wrapped banner and self-test descriptions corrected. F01 is a separate surviving law assertion at IV8. |
| R628-2-S1, SUGGESTION, phase/window drift | Superseded and resolved by the corrected ruling and phase-invariant grading. |
| R628-2-S2 / R628-3-S2, SUGGESTION Tests | Resolved: `counter_notification_times()` filters at the measurement end before gap grading. |

R628-1-S1 / R628-2-S3 / R628-3-S1 remains **SUGGESTION, Robustness/RTL** at `hdl/ieee1722/crf/KL_crf_rx.sv:487,644`: bind reset has priority over an acceptance on the same edge. No required boundary behavior contradicting that ordering was established. Optional outcome: add an explicit coincident-edge test and document its ordering; verify adjacent and coincident bind/accept cases. This does not leave a lens unclean.

R628-1-S2 / R628-2-S4 / R628-3-S3 remains **SUGGESTION, Tests** at `tb/verilator/milan_dp/sim_nxn.cpp:2596`: the 10,000,000-cycle silence bound assumes the current fixture clock. It is correct for that recipe; optional outcome is deriving it from the clock parameter, checked at the supported clocks. This does not leave a lens unclean.

**Implementation evidence and limits**

The [immutable public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/907f0116a8b7f548ce33dc2821a23f576ac0bab3/review-evidence/726-r1) is the author source evidence. Retrieved blobs were checked against their public Git object IDs. The original routed image's five recorded inputs match the published hashes; the functional HDL tokens and configuration remain identical at this head, with only comment changes in two counter modules and a firmware README change afterward.

The published shipping route report gives 49,427 LUT, 53,378 FF and 87.5 BRAM. Against the supplied 49,392-LUT reference this is +35, below the +200 stop threshold; the reference was not independently rebuilt. The reports identify xc7a100t-fgg484-2, the shipping TDM8 configuration, AreaOptimized_high synthesis and the recorded implementation directives. No explicit seed override appears in the supplied script. The four fast/slow, 0/85-degree negative-path reports contain no negative paths. Published WNS +0.451 ns / WHS +0.036 ns are author-reported exact values; a raw summary establishing those exact margins was not present in the retrieved set. The timing check reports zero unconstrained internal endpoints but 46 no-input-delay and 87 no-output-delay entries, so external I/O timing is not established by the internal closure result. No implementation run was performed by this reviewer.

The author's 78 documentation command receipts were audited. The initial builder observer timed out with rc 124; the separately published completion receipt records observer/container/log retrieval rc 0. Nineteen optional NOT RUN arms remain non-executed. The earlier unsupported strict invocation is superseded by its corrected rc-0 receipt. None of these author runs is a manager source bank, and no manager source bank is claimed at this exact head.

At the final read-only hosted snapshot, **2026-10-12 21:57:24 UTC**, each run's `head_sha` is the reviewed source head. `rtl-fast` run 38311301106 and `elaborate` run 38311300993 completed successfully. All four portability shards, wire-accountability and docs-check-no-git succeeded. The physical context was **skipped**. The documentation job and all five exhaustive simulation shards were still running. In particular:

- [docs-check, job 115017406895](https://github.com/kebag-logic/milan-fpga/actions/runs/38311300974/job/115017406895) was in its builder step; no final successful documentation verdict was available.
- [shard 4/5, job 115017606642](https://github.com/kebag-logic/milan-fpga/actions/runs/38311301025/job/115017606642) was executing its suite; `suite-logs-4` had not been published, so its counter-leg RESULT lines could not be inspected.

`receipts/hosted-final.json` preserves job and step status. Run association with this source head is not a claim that a worker checked out the source commit directly: pull-request workers may execute a generated merge tree. No hosted success is inferred from local success, and no pending or skipped context is counted as executed proof. Hosted/local-replica acceptance belongs to the manager.

**R628-2-F1 | MAJOR | Docs, Tests, RTL | RETAINED pending required verification**

Artifact: the exact-head documentation job above; current source fixes at the dirty pulse contract, `scripts/measure_test_evidence_readers.py`, and the Python/C++ counter fixtures. Authority/evidence: the public round-3 scope requires the documentation workflow to finish successfully; all named local checks now pass, but the hosted job had no final verdict. Impact: the finding's required full-workflow confirmation is not yet demonstrated; this is not a claim of a newly failing source check. Required outcome: a successful exact-head documentation result with unchanged budgets. Verification: inspect the completed job and its named gate outcomes, then explicitly clear the retained finding. The original severity and lenses are preserved rather than silently treating pending evidence as resolution.

**R628-3-F2 | BLOCKER | Tests, Robustness | RETAINED pending required verification**

Artifact: `stream_counters.py:144,162`, `receipts/makeflags-shape1.log`, `receipts/make-counters.log`, and the shard 4/5 job above. Authority/evidence: the round-4 acceptance specifically requires that hosted shard to succeed with counter legs showing RESULT: PASS in `suite-logs-4`. The inherited-flag source failure is fixed and both local commands pass; the hosted confirmation was unavailable. Impact: the exact integration path whose earlier failure motivated the blocker has not yet supplied its required successful hosted receipt. Required outcome: successful shard 4/5 at this source head with the counter legs present and passing in the artifact. Verification: inspect run/head metadata, completed job status and the uploaded raw suite log, then explicitly clear the finding. No new runtime defect is asserted.


This reviewer-owned ledger records coverage applied at this head. Pending prior-finding verification is kept open at its original lenses; clean source observations alone do not bank those lenses.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Counter engines and reset boundaries; parent packet/gap/phase receipts; law grader; sim_main_nx.cpp:651, F01 | R629-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| RTL | UNCLEAN | Three counter engines; unchanged parent wiring and pinned scheduler; input/area review; retained R628-2-F1 confirmation | R629-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Robustness | UNCLEAN | Five focused fixtures; start/bind/reset/wrap/malformed/stall and zero-snapshot probes; retained R628-3-F2 confirmation | R629-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Tests | UNCLEAN | BDD, grader, docs gates, all new mutation/omission pairs and shift probes; F01; retained R628-2-F1 and R628-3-F2 | R629-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Docs | UNCLEAN | REGISTER_MAP, measurement note, dated audit/findings, READMEs, PR body and public receipts; F01; retained R628-2-F1 | R629-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |


Final direct verification matched all 1,300 superproject tracked blob bytes and executable modes, all index entries and all five unchanged gitlinks. It also matched 562 processor, 104 timing-processor and 214 stream-library tracked files against the required initialized pins. Root and dependency checkouts have no tracked, untracked or ignored changes. Generated probe outputs were confined or relocated into packet scratch; all foreground executions finished. See `receipts/checkout-verification.json`. Peak memory was 4,855,144,448 bytes under the 12,884,901,888-byte cap, with zero OOM events. The scoped simulator identity was verified before use and recorded in `receipts/tool-identity.json`.

`MANIFEST.sha256` names the publishable report, portable scripts and raw receipts using packet-relative paths. Scratch trees, preliminary notes, downloaded review bodies and bulky build/bootstrap transcripts are excluded. Public source receipts remain byte-for-byte copies with provenance hashes; the report distinguishes them from this review's executions.

The simulated runs cover two recipients, finite five-second protocol windows and the selected shipping/largest shapes. They do not establish arbitrary controller fanout, exhaustive system performance, physical link timing or hardware calibration. Physical calibration was NOT RUN; field skips and a skipped hosted physical context are not hardware proof. No full parent, processor, gPTP, portability or builder bank, host orchestration/self-test, container action or hardware operation was run here. No firmware implementation changed, so this lane did not trigger a new firmware capture measurement.

The manager must carry F01 to correction and independent re-review, resolve the hosted confirmations, accept hosted/local-replica evidence, complete the two-review bar and publish a reviewer-accepted ledger. The manager's final current-dev candidate uses the live dev base dc4d06cbfec209cc2ff76806f4b49c51f46639ae rather than the source base c6bd08c6; builder/native banks and their receipts belong to that merge turn. Bench comparison, explicit merge authorization and post-merge containment also remain manager duties. Source validation and this report do not substitute for them.

R629-4 FINISHED
