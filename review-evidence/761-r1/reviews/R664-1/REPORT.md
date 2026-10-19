[R664] NEGATIVE - exact head 4191b0987d1313abc86c747ad6a9c3c0963f17da

Round R664-1, external independent review of PR #767, issues #761/#762.
Tree: `5c21b067fcad3e7ff7017190f088c7ae0528b807`.
Range: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f..4191b0987d1313abc86c747ad6a9c3c0963f17da`, two commits, 25 changed files.

All five lenses were applied. Two findings remain open. The ordinary receiver and restart campaigns pass, but an independent ordering case loses a required AAF interruption. The new CRF started-only restriction also lacks a settled public scope decision.

**Authority and independence**

Reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, public issue bodies and assignment/takeover comments, REQUIREMENTS.md, architecture/interface authorities, and the exact diff/history. Read IEEE 1722-2016 4.4.4.3 and 10.4.3 and Milan v1.2 5.3.8.7, 5.3.8.10/Table 5.6 and 5.4.2.25/Table 5.16 in the standards documents. Table 5.6 defines the event; Table 5.16 requires its service. Related public issue #97 separates stopped-input observation from consumption.

The frozen [assignment](https://github.com/kebag-logic/milan-fpga/issues/761#issuecomment-6256482625) requires the CRF gain edge, unchanged existing restart causes, silence/gap/Unbind counter cases and mutants, affected gates and shipping route. No register, top-level port or parameter change appears in the delta.

This verdict and ledger were written before consulting another review report. No author-private material, source fixes, other-checkout edits, commits, pushes, GitHub writes, hardware work or full validation banks were used.

**R664-1-F1 | MAJOR | Conformance, RTL, Robustness, Tests**

Artifact: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:892`, `:1054`, `:1066`; `tb/verilator/avtp_rxmon/sim_lockstep.cpp:538`.

Title: A later Unbind erases an already published silence interruption.

Authority/evidence: Issue #762 and Milan Table 5.6 require the silence interruption to count once. The Unbind exclusion exempts that operation, not an earlier silence. The silence walk increments MEDIA_UNLOCKED and asserts dirty at phase 1, but consumes `sil_si_r` only at phase 3. The unconditional bind-fall clear can erase that mark between those operations.

`probe_silence_order.py` adds an independent counter oracle to a disposable harness, retaining unchanged exact-head RTL. It waits until GET_COUNTERS exposes MEDIA_UNLOCKED +1 while still bound, then applies Unbind. At N=1 and N=8, Unbind on the next cycle yields STREAM_INTERRUPTED +0. Delaying Unbind one additional cycle yields +1; delays 1 through 8 all preserve the count. The missing count stays missing after another complete timeout. Each `silence-order-{1,8}.log` records 80 checks and two failures, both observations of this one lost event.

Impact: A genuine silence interruption disappears according to the controller operation's phase, even after its unlock is externally observable.

Required outcome: Preserve an interruption already attributable to silence when a later Unbind arrives; an Unbind-caused unlock still adds none. Use a consistent event boundary across the unlock/interruption writes and preserve reset/rebind semantics.

Verification: Require exactly one interruption for silence-before-Unbind and zero for Unbind-before-silence across every relevant cycle, including yielding/paused walks and both shapes. The submitted sweep requires only `si <= 1` and a mixture of zero/nonzero trials, permitting this loss. The patched lockstep reference shares the defect and cannot detect it by equality.

**R664-1-F2 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `hdl/ieee1722/crf/KL_crf_rx.sv:556`; `tb/verilator/crf_rx/sim_main.cpp:199`; `docs/reference/REGISTER_MAP.md:874`; PR #767 known-limitations paragraph.

Title: The bound-input silence requirement is narrowed to started inputs without a settled public decision.

Authority/evidence: The frozen #762 acceptance/assignment says a silence unlocking a bound input counts once, with Unbind excluded. The new guard additionally requires `!stop_i`, the replica adopts that exception, and the new register documentation asserts it. The author's REVIEW READY and PR explicitly leave a possible Controller-stop ruling open; no examined maintainer/manager scope decision authorizes the restriction. Milan 5.3.8.7 separates started/stopped from bound state; Table 5.6 names Unbind, not a general stopped-state exemption.

`probe_stopped_silence.cpp` locks a bound receiver, then sends no PDUs for longer than the timeout. Started: MEDIA_UNLOCKED=1 and STREAM_INTERRUPTED=1. Stopped after established lock: MEDIA_UNLOCKED=1 and STREAM_INTERRUPTED=0. Both remain bound and never Unbind. `stopped-silence.log` records this; the build succeeds and the independent frozen-acceptance oracle exits 1. Unlike the existing stopped-input case, this probe has actual receive silence, not continuing observed traffic.

Impact: A class of bound-input silence remains uncounted while acceptance is claimed met. Documentation promotes an unresolved interpretation into the counter contract. This is substantive scope/conformance, not wording residue. The stopped behavior predates this PR; its new guard and documentation expressly preserve it instead of resolving the assigned general silence rule.

Required outcome: Obtain a public, standards-cited disposition before claiming completion. If the frozen acceptance remains unchanged, implement and test it. A narrower scope needs an authorized public change and standards analysis; the author's caveat supplies neither. Preserve stopped-input observation and do not classify continuing received traffic as physical silence.

Verification: Independently grade started silence, stopped silence after established lock, STOP with live traffic, START recovery and Unbind. Add a mutant for the decided stopped-state rule. Align the register documentation and PR acceptance claim with that decision and result.

**Applied-lens evidence**

- Conformance: Compared the receive engines to the frozen silence/gap/Unbind rule and Milan counters; compared `milan_datapath.sv:3247` to IEEE restart clauses. Both CRF lock edges are selected-source gated; echo and AAF-meter terms are unchanged. F1/F2 prevent a clean result.
- RTL: Traced `sil_si_r` capture/reset/Unbind clear, phase-3 consumption, yielding RMW and bind-era wipe; checked the CRF timeout/PDU mutual exclusion and counter writers. Reviewed the resettable lock shadow and unchanged per-stream target/hold logic at `KL_media_clock_restart.sv:226`. No new CDC or interface. F1/F2 remain.
- Robustness: Applied silence/resume, gap, Unbind, coincident expiry, delayed Unbind, stopped-state, rebind/reset, wrap and multi-listener checks. The focused restart regression covers pending-request merging and distinct requests after the first reported PDU, with independent eight-PDU holds. F1/F2 remain.
- Tests: Examined every changed harness/Makefile/mutation driver, builder expression pins, gm-step anchors, root `[CTRS-CRF]` and mclk mutants 17/18. Rebuilt receiver controls/mutants and restart regression. Reference equality is not an independent oracle for F1. The added probes fail as described.
- Docs: Read all changed documentation hunks, counters map, clock plan, compliance matrix, test inventory and PR claims. The CRF-return/unchanged-AAF-return distinction is documented. No new prohibited source-comment identity or bench-lane instance was found. Receipt index matches its files. F2's contract remains unresolved.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1/F2 | #761/#762 assignment; IEEE 4.4.4.3/10.4.3; Milan 5.3.8.7/Tables 5.6/5.16; receive/restart delta | R664-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| RTL | UNCLEAN, F1/F2 | KL_avtp_rx_monitor_ctx.sv:892/1054/1066/1138; KL_crf_rx.sv:545/556; milan_datapath.sv:3205/3247; KL_media_clock_restart.sv:226 | R664-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Robustness | UNCLEAN, F1/F2 | silence-order-1.log; silence-order-8.log; stopped-silence.log; receiver campaigns; restart-engine.log | R664-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Tests | UNCLEAN, F1/F2 | changed tb/verilator files; sw/builder/test_builder.py:11377; independent probes and campaign receipts | R664-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Docs | UNCLEAN, F2 | REGISTER_MAP.md:874; MEDIA_CLOCK_FOLLOWING.md:1397; remaining changed docs; PR #767; published INDEX.md | R664-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |

**Execution and evidence**

Used the assigned 5.050 executable after checking its reported identity. Receiver campaigns ran concurrently in disposable trees. Four compiler workers per build, at most three overlapping builds, stayed below 16 jobs. Candidate RTL was unchanged. Portable scripts and console receipts accompany this report.

| Evidence | Result |
|---|---|
| receiver-lockstep-campaign.log | 8/8 campaign results, both shapes; rc 0 |
| crf-counter-campaign.log | 15/15 controls/mutants; rc 0 |
| restart-engine.log | 99 clean checks; 5/5 campaign results; rc 0 |
| silence-order-build.log | Build rc 0; both executions rc 1 on F1 |
| stopped-silence-build.log | Build rc 0; execution rc 1 on frozen acceptance |
| receipt-audit.log | 170 indexed receipts, 171 files including INDEX.md; no missing/extra/hash/size discrepancies |
| tree-integrity.log | 1,422 root blobs and all five required submodule populations: raw bytes, modes, index, gitlinks match; checkout clean |

Reproduce: `python3 run_focused.py SOURCE_ROOT PINNED_SIMULATOR`; `python3 probe_silence_order.py SOURCE_ROOT PINNED_SIMULATOR`; `python3 run_stopped_probe.py`; `python3 run_restart.py`; `python3 verify_tree.py SOURCE_ROOT`. The defect probes intentionally return 1. `audit_receipts.py` takes the extracted public `review-evidence/761-r1` directory. Scratch is disposable and unpublished.

The [published author receipts](https://github.com/kebag-logic/milan-fpga/tree/9020398b728636ec6a976a5b1e02c6979e0c24c6/review-evidence/761-r1) report 63/63 suites, 2,187,305 checks, zero failures/timeouts; all 42 final static gates rc 0; synthesis 58/58; front-end analysis zero findings; builder rc 0 with calibration gate 11 NOT RUN. Shard 3's first attempt was a preflight refusal followed by a clean rerun. The mclk campaign is 34/34 with both added edge mutants caught. The full gm-step campaign is at first commit `f443ed9b`; the final-head sweep separately includes the gm-step suite. See `public-evidence-audit.log`. These are author source-head receipts, not manager source-bank execution or this reviewer's full-bank reruns. Large public logs may be explicit tails.

The route-1x1 receipt uses the unchanged recipe, default seed, implementation release 2026.1 build 6511674, `xc7a100tfgg484-2`, Physopt postRoute. Base `e9cbb676` matches the record: LUT 49,613, FF 52,353, WNS +0.215 ns, WHS +0.036 ns. Candidate `4191b098`: LUT 49,411, FF 52,297, 15,751 slices, WNS +0.161 ns, WHS +0.036 ns, zero TNS/THS and complete route. Resource gate rc 0; WNS exceeds +0.03 ns. Worst setup path is within the CPU. Passing the incremental gate does not satisfy the separately documented 60-percent LUT target. No physical calibration or field proof is inferred.

An initial restart campaign used default temporary storage, cleaned itself up, and was repeated with TMPDIR explicitly set to packet scratch; only the corrected run's receipt is retained. Published console logs normalize host paths; receipt-normalization.tsv records original/published hashes. Original console bytes stay in unpublished scratch.

**Prior public findings**

After writing this independent verdict and ledger, queried the PR reviews, inline review comments and issue-comment thread. There were zero review bodies and zero inline comments. The thread contained only the internal/external review-start comments, 6260500367 and 6260505862, neither with findings. Thus there are no prior public findings to resolve or retain at this head. No other reviewer's report was consulted. See prior-public-findings.log.

**Limits and pending manager duties**

No full parent/processor/gPTP/synthesis/builder bank was run by this reviewer. No hosted/act acceptance verdict is claimed. Physical calibration remains NOT RUN; field skips and desk gates are not hardware evidence. The manager owns hosted/act acceptance, internal review, public disposition of F1/F2, and the final current-dev merge candidate's builder/native receipts. Source base and supplied live dev are both `e9cbb676`; this does not pre-validate a later merge result. Fixes require new exact-head review before authorized merge, post-merge containment and issue/project closure. This report does not authorize merge.

R664-1 FINISHED
