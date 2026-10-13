[R628] POSITIVE - exact head 12f00129349c889e6dbbb7de11529ab38c9d164d

# R628-6: internal cleared-context review of issue #726 / PR #729

Head `12f00129349c889e6dbbb7de11529ab38c9d164d`, tree
`e0a0682e5c703755d1e1e003967d70f66d5c0757`, source base `c6bd08c6`. This is a
full review of the PR, together with the round 2-6 deltas. I reconstructed the
task from AGENTS.md, CONTRIBUTING.md, docs/README, the issue body, the
maintainer rulings (6125741685, 6125845117, 6126028604, 6132483068,
6134121887), the assignment (6125784157) and the round decisions. Then I read
`c6bd08c6..12f00129` and its history, and ran the executable evidence myself.
I wrote my own findings and ledger before reading any prior review report.
Prior findings are resolved or retained in the last table.

**Verdict basis.** No BLOCKER, MAJOR or MINOR is open at this head. All five
lenses were applied and are clean. This is a source-review verdict, not issue
completion or merge authorization. One wording item is recorded as RESIDUE
(PR body publication status). Four optional suggestions are carried from
earlier rounds; none affects coverage.

## Findings

### R628-6-R1 - RESIDUE - Docs

- **Where.** PR #729 body:
  - Status: "Round 6 local source head: `12f00129…`." and "Focused local validation passes; two new commits await publication."
  - "How to get into the same state": "Both Round 6 commits remain local pending authorized publication."
  - "Known limitations": "Independent re-review, authorized publication and hosted acceptance remain required."
- **Authority and evidence.** The public PR head is `12f00129349c889e6dbbb7de11529ab38c9d164d` (`gh pr view 729`, resumed observation 2026-10-13T00:07:12Z). Hosted checks are running against it (`receipts/hosted_checks_resume.tsv`; body excerpt in `receipts/pr_body_status_excerpt.txt`). R628-5-R6 and R629-5-R01 corrected the same wording for Round 5, and it has now recurred for Round 6. The change is wording only. It changes no measurement, figure, verdict, test, code or conformance claim, and has no privacy implication.
- **Impact.** Readers are told the reviewed commits are unpublished.
- **Exact fix.**
  - Replace the two Status sentences with "Round 6 published source head: `12f00129349c889e6dbbb7de11529ab38c9d164d`." and "Focused local validation passes; both Round 6 commits are published."
  - Delete "Both Round 6 commits remain local pending authorized publication."
  - In Known limitations, change the item to "Independent re-review and hosted acceptance at this head remain required."
- **Verification.** Read the updated body. Carry this item on the residue checklist.

### SUGGESTION (optional; no effect on coverage)

- **R628-6-S1 - SUGGESTION - Tests.** Artifact: `tb/verilator/milan_dp/Makefile:677-687`, carried from R628-5-S1. Evidence: the per-engine plants `aaf-guard`, `crf-guard` and `aaf-rx-interval` are not in `counters-mutants`; they fail CADENCE 2, CADENCE 2 and RX 2 respectively here and escape with only their group omitted (`receipts/runs/my_*.{run,omit}.log`). Impact: this additional per-engine coverage depends on reviewer probes. Optional outcome: make those controls standing. Verification: each required group fails and its omission passes.
- **R628-6-S2 - SUGGESTION - RTL, Robustness.** Artifact: `hdl/ieee1722/crf/KL_crf_rx.sv:487-490,644-698`, carried from R628-5-S2. Evidence: bind reset has explicit priority over a coincident accepted PDU, while AAF and talker boundaries retain the coincident event. Impact: the boundary can discard at most one packet per bind. Ordering that packet before the reset is defensible under the era reset contract; this is an optional boundary-consistency improvement, not a demonstrated violation of the ruled reset. Optional outcome: align or document the asymmetry in a focused boundary test. Verification: drive accept and bind-rise together and check the chosen ordering.
- **R628-6-S3 - SUGGESTION - Tests.** Artifact: `tb/verilator/milan_dp/sim_nxn.cpp:2589,2596,2647-2649`, carried from R628-5-S3. Evidence: the `10000000L` silence bound equals 100 ms at the notification build's current 100 MHz default, but cannot fail inside the 4000 ms × 100-cycle loop bound. The actual premise is independently asserted at lines 2647-2649. Impact: a future clock change could make the comment/bound misleading. Optional outcome: derive the bound from the clock. Verification: retain the current ordering checks and exercise a changed clock parameter.
- **R628-6-S4 - SUGGESTION - Tests.** Artifact: `tb/tools/torture_campaign.py:754`, carried from R628-5-S4. Evidence: the merge-turn comparison uses `snapshot_skew_frames=8000`, one class A second; coalesced receive publication can add another interval of lag. Impact: an undisciplined cross-device read could report a false FAIL. Optional outcome: document the read discipline or explicitly budget publication lag. Verification: compare samples taken across an interval-publication boundary. Physical acceptance remains the manager's merge-turn duty.

## Clean-lens lines

[R628] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:206-262`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:329-330,637-644,943-955,983-984,1154-1176`, `hdl/ieee1722/crf/KL_crf_rx.sv:484-520,644-698`, `hdl/milan/milan_datapath.sv:3156-3171,3300-3322,7924-8010` (unchanged), `receipts/runs/w_{clean,fo}_s{1,8}.run.log`; issue #726 acceptance 1, 2 and 4, assignment 6125784157, rulings 6125741685/6125845117/6126028604/6132483068/6134121887.
- **Transmit law.** FRAMES_TX counts each transmitted AVTPDU on every output, AAF and CRF. CRF arrives through the one-deep `tkd_crf_pend_r` skid, and `KL_crf_tx.sv:518` increments `tx_count_o` once per completed PDU. The counter wraps at 32 bits and resets at each talker start. A PDU completing in the start cycle stays as the first count of the new run.
- **Wire match.** The MAC counts agree: 799/101 at shipping, and 800×8/101 at the largest shape.
- **Receive law.** FRAMES_RX counts accepted AVTPDUs: AAF through a 32-bit coalesced batch, CRF per PDU. Each input receives 500 packets. The count survives unbind and is 0 after rebind (RX/RX_RESET checks pass).
- **Retained laws.** MEDIA_RESET and TIMESTAMP_UNCERTAIN keep their interval law (`KL_talker_diag_ctx.sv:227-228`).
- **Refresh.** Every changed Stream Input or Output marks itself dirty. The unchanged scheduler (`KL_aecp_notify.sv:1100-1102`) is the only limit.
- **#60 throttle.** `milan_datapath.sv` is not in the diff, so the AVB_INTERFACE throttle (`ctr_avb_dirty_w`) is unchanged.
- **Measured cadence.** Spacing is at least 1000 ms, and every consecutive gap and final wait is ≤ 1025 ms. Shipping shape: 28 gaps, 1001.000-1001.867 ms, service 3.263 ms. Largest shape: 126 gaps, 1000.982-1012.029 ms, service 14.058 ms (`receipts/gap_summary.txt`).
- **Firmware.** Only the README changed (`sw/firmware/ctrl/aecp/README.md`), so no capture re-measure is owed (`check_nvm_capture` rc 0).

[R628] PASS RTL - the RTL lines above; `hdl/milan/milan_datapath.sv:7940-8010` (sticky pending bits, round-robin); `receipts/gitlinks_{base,head}.txt` (identical); `receipts/lint_rtl.log` (90 ≤ ratchet 90); `receipts/hdl_code_equal_acadfacd_head.txt`.
- **Widths and reset.** `frx_acc_r`/`frx_add_r` are 32 bits with no truncation at `:642-643`, and every new or changed register is reset.
- **Start edge.** At the talker start edge, the later nonblocking assignment correctly overrides the per-PDU increment.
- **Parked walk.** A parked interval walk keeps `frx_add_r`, because `iv_go_w` is blocked while `iv_res_list_r != 0`. A bind discards the parked remainder of its own stream (`:1114`).
- **Dense pulses.** Per-PDU dirty pulses coalesce in the root's sticky pending bits, so dense traffic cannot starve a descriptor.
- **CDC and submodules.** No CDC is added, and no submodule changes.
- **Area and timing.** Every changed HDL file is code-equal (comments removed) to `acadfacd`, the routed image. So the published 49,427 LUT (+35 against 49,392, under the +200 STOP), 53,378 FF, 87.5 BRAM and WNS/WHS +0.451/+0.036 ns apply. These are author measurements; I did not rebuild.

[R628] PASS Robustness - `tb/verilator/milan_dp/stream_counters.hpp:258-324` (bind/unbind/rebind; start/stop/restart; near-wrap; the 65,534+3 batch) and `receipts/runs/*shift_*.log`. Shifts of 200, 300, 800, 900, 500,000, 999,999 and 1,000,000 cycles pass at both shapes and both output conditions (28 runs). The `MAKEFLAGS=" -w"` shape-1 leg passes (`receipts/clean_s1_w.log`). Disposable plants:
- **`tx-start-drop`.** Fails tkdiag T11 (`receipts/tkdiag_tx-start-drop.log`).
- **`tx-saturate`.** Fails tkdiag T16 (`receipts/tkdiag_tx-saturate.log`).
- **`aaf-acc-bind`.** The bind keeps the old batch. It fails the receive suite on `[M13e2]` and "new sid counts" (`receipts/accbind_avtp.log`).
- **CRF bind reset of `seq_err_o` removed.** Fails the unchanged bind-era contract (`receipts/era_plant_seqerr.log`).

[R628] PASS Tests - `tb/verilator/milan_dp/stream_counters.{py,hpp}`, `stream_counter_f5.{py,cpp}`, the `Makefile` counters targets, and the tkdiag, crf_rx, avtp_rxmon (including the lockstep superset rule) and `sim_nxn`/`sim_crf_licence` diffs; the feature, steps and `torture_campaign.py`; `receipts/plant_table.tsv`.
- **Shipped plants.** All 12 parent pairs (11 variants plus egress at shape 8) fail by name and escape with only their group omitted. So do the 3 mailbox plants.
- **Baselines.** `before` gives 12 and 54 failures in exactly TX/RX/CADENCE.
- **Prior probes.** The prior reviewer's unchanged `sched-1600`, `sched-2000` and `egress-stall` fail CADENCE at both shapes (8/36), and pass with CADENCE omitted.
- **My scheduler plants.** `sched-900` fails RATE (8), and `sched-1030` at shape 8 fails CADENCE (36).
- **Fixed bound.** At shape 8, `sched-1020` gives output gaps of 1032.0 ms (rejected) and input gaps of 1021.5 ms (accepted). So the 1025 ms bound is fixed, and the run under test does not set it. This boundary plant also fails PHASE for input rows because shifting the start removes their isolated over-bound first gap; it is an exploratory plant, not a standing single-group control.
- **Suites.** Behave: 406 scenarios / 1,977 steps. The grader self-test runs 80 tests.

[R628] PASS Docs - `docs/testing/726_STREAM_COUNTERS.md:10-236`, `docs/reference/REGISTER_MAP.md:148-153,869-872,919,963`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218-237,399-401`, `sw/firmware/ctrl/aecp/README.md:52-66`, the five dated findings notes, the `docs/history` link pinned to `c6bd08c6`, `tb/verilator/milan_dp/README.md:24-27,470-472,504-506,592-607`, `docs/README.md:92`, the design notes in the five changed HDL files, and the PR body.
- **Content.** They state the ruling, both resets, the two-condition criterion, and the fixed 25 ms ceiling with its source. Every figure I re-measured matches.
- **Gates.** The final focused documentation, style and source gates return 0. Initial TOC/em-dash attempts returned 2 for missing pinned renderer dependencies; both passed after installing those dependencies under scratch. This includes TOC (selftest, verify-anchors, check) and em-dash with the pinned renderer (`receipts/gates/SUMMARY.tsv`). Hosted `docs-check` succeeded at this head, with all 55 job steps successful (`receipts/hosted_docs_steps.tsv`).
- **Open items.** Only RESIDUE R1 remains.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | three counter engines; datapath feed and arbiter; rulings; four clean parent legs; F5 shapes 1/8 | R628-6 | 12f00129349c889e6dbbb7de11529ab38c9d164d |
| RTL | CLEAN | five changed HDL files; datapath arbiter; gitlinks; lint ratchet; code-equality against the routed `acadfacd` | R628-6 | 12f00129349c889e6dbbb7de11529ab38c9d164d |
| Robustness | CLEAN | reset, wrap, batch boundary, bind era, start edge, 28 shift runs, inherited make flags, four disposable plants | R628-6 | 12f00129349c889e6dbbb7de11529ab38c9d164d |
| Tests | CLEAN | 15 shipped pairs, 2 baselines, 6 prior-probe pairs, 6 reviewer parent plants, 2 tkdiag plants, receive and CRF suites and mutants, behave, grader | R628-6 | 12f00129349c889e6dbbb7de11529ab38c9d164d |
| Docs | CLEAN (RESIDUE R1 only) | documents listed above; 19 local gate commands; hosted docs-check | R628-6 | 12f00129349c889e6dbbb7de11529ab38c9d164d |

## Round-specific checks

| Item | Result at this head |
|---|---|
| R2: R629-1 `reproduce_contract.py`, unchanged (sha256 `fdc8be18…`) | rc 0 (`receipts/reproduce_contract.log`). Removing the CRF bind reset of `seq_err_o` gives rc 1 with the named survivor message. |
| R2: BDD gate | 14 features, 406 scenarios, 1,977 steps, 0 failed (`receipts/behave_all.log`). Hosted `bdd-conformance` succeeded at this head. |
| R2: output cadence with FRAMES_TX alone changing | Frames-only legs rc 0 (70/301 checks). OUTPUT_CONDITION shows TU=MR=0, one start, no stop, and clear wire tu/mr. `tx-nodirty` fails OUTPUT_CADENCE (4) and escapes. |
| R2: law table, trap (3), grader | Table 7.157 per AVTPDU (`torture_campaign.py:402-433`). The interval-rate FAIL scenario (`feature:418-421`) passes in the suite. |
| R3: docs workflow gates | `measure_naming --check`, `measure_test_evidence --check`, `check_py_idiom`, `check_cpp_idiom`, `docs_check`, `check_doc_style`, `gen_toc` (3 modes), `check_em_dash --base c6bd08c6` (0 findings over 347 added lines), `check_doc_paths`: all rc 0. No budget file is in the diff. Hosted `docs-check` succeeded at 2026-10-12T23:48:34Z. |
| R3: R628-2 `probe_xside_law.py`, unchanged (`c469af62…`) | Ruled 32000/32000 gives PASS. 4/32000 gives FAIL against the talker. 4/4 gives FAIL with a finding on each side. |
| R3: R629-2 `probe_snapshot.py`, unchanged (`b783a52e…`) | Before publication, 3/0/0 is INFO with `ratio: null`. After publication, 3 is PASS. rc 0. The published probe was rerun unchanged during resume. Restoring the old guard fails only `test_unpublished_zero_receive_snapshot`; omitting that test passes (`receipts/snapshot_guard.log`). |
| R4: inherited `-w` and recursive target | `MAKEFLAGS=" -w" … --shape 1` rc 0. `make -C tb/verilator/milan_dp counters` rc 0 with four `RESULT: PASS` (`receipts/make_counters.log`). |
| R4: consecutive-gap grading, shift invariance | No grid grading and no startup exclusion (`stream_counters.hpp:174-195,250-255`). The in-fixture PHASE check passes for every row. 28 external shift runs pass, and `fixed-grid` fails PHASE (8) and escapes. |
| R5: IV8 text and receive regression | 97 single-sink, 119 NxN and 36+36 lockstep checks; the four lockstep mutants are caught. IV1 publishes 9 → 15 (+6). IV8 bursts are +1, and its text no longer lists FRX. |
| R6: fixed 1025 ms bound at both shapes | `stream_counters.hpp:176,192-193` grades every gap and the final wait against `1025L*kMsCycTb`. Measured service is only printed (`:241,247-249`). |
| R6: R628-5 `probe_counters.py`, unchanged (`a53f75c9…`) | `sched-1600`, `sched-2000` and `egress-stall` each fail only CADENCE: 8 at shape 1 and 36 at shape 8. Each passes with CADENCE omitted. Correct RTL passes. |
| R6: texts | `726_STREAM_COUNTERS.md:35-39,66-67`, the audit `:228-232`, `REGISTER_MAP.md:152-153` and the PR body (Round 6) name the fixed 25 ms ceiling and its 1012.029 ms source. |
| R6: residue applied | R628-5-R1…R5 are present at the head. R628-5-R6 and R629-5-R01 are applied for Round 5; the same wording has recurred for Round 6 (R628-6-R1). |
| Other CRF regressions | crf_rx: 14,287 unit, 2,201 discontinuity and 69 talker-step checks; mutants 10/10. tkdiag: 99/99. |

## Prior findings at this head

| Prior finding | Disposition |
|---|---|
| R628-5-F1 (MINOR, Tests) | Resolved. The bound is fixed at 1025 ms. Its three probes and the standing egress plant fail CADENCE at both shapes and escape when omitted. |
| R628-5-R1…R5 (RESIDUE) | Resolved as their exact fixes stated (`sim_main_nx.cpp:548-551`, `crf_rx/sim_main.cpp:98-99`, `KL_aaf_packetizer.sv:181-185`, audit `:399-401`, `feature:396,418`). |
| R628-5-R6 / R629-5-R01 (RESIDUE) | Resolved for Round 5. The same wording recurs for Round 6 and is retained as R628-6-R1. |
| R628-5-S1…S4 (SUGGESTION) | Not taken. Carried as R628-6-S1…S4. |
| R628-1-F1 = R629-1-F01, R628-1-F2/F3/F4, R629-1-F02 | Resolved; see R2 rows. |
| R628-2-F1, R628-2-F2, R629-2-F01 | Resolved; see R3 rows. Hosted `docs-check` succeeded at this head. |
| R628-3-F1 (MAJOR), R628-3-F2 (BLOCKER) | Resolved in source; see R4 rows. Hosted shard 4/5 at this head was still in progress at my final poll (see limits). |
| R629-4-F01, R628-4-R1/R2 | Resolved; see R5 row. |
| R628-2-RS1…RS5 (RESIDUE) | Resolved: the AECP event is bit 3/value 8; README and harness descriptions use the packet law; banners and self-test names match the current contracts. |
| R628-3-R1 and R629-3-R01 (RESIDUE) | Their obsolete-head publication wording was removed. The current Round 6 recurrence is R628-6-R1. |
| R628-2-S1 (SUGGESTION) | Superseded by R628-3-F1, now resolved by the corrected public criterion and phase tests. |
| R628-2-S2 / R628-3-S2 (SUGGESTION) | Resolved: `stream_counters.hpp:counter_notification_times` excludes frames after measurement ends. |
| R628-1-S1 / R628-2-S3 / R628-3-S1; R628-1-S2 / R628-2-S4 / R628-3-S3 | Optional items retained as R628-6-S2 and S3 respectively. |

## Real limits

- **Hosted run.** At the resumed observation (2026-10-13T00:07:12Z, `receipts/hosted_checks_resume.tsv`), Verilator shards 0/5, 1/5, 2/5 and 4/5 were still in progress, so the hosted counters legs in `suite-logs-4` at this head are not observed. Shard 3/5 and elaborate had succeeded. The remaining listed contexts had succeeded: docs-check, rtl-fast, bdd-conformance, verilator-lint, the Yosys shards and yosys-elaboration, firmware unit and mutants, publication-census, full-ci-gate, wire-accountability, docs-check-no-git and changes. The physical gPTP context is skipped by design.
- **Area and timing.** These are the author's retained measurements from `acadfacd`. I verified code equality and did not rebuild.
- **Runtime.** CPython 3.14.7, not the documented 3.12.3. The pinned Markdown renderer was installed only under scratch. Only the focused gates listed were run locally, not the entire docs workflow.
- **Simulation scope.** These are finite, compressed-time simulations with two recipients. They do not cover maximum fanout, a physical link or indefinite operation. Physical calibration NOT RUN; field skips are not hardware proof.
- **Mailbox fixture.** The F5 fixture injects counter-change calls. It does not prove a production caller.
- **Standards access.** Clause interpretation follows the public maintainer rulings and linked repository contracts. Full standards texts were not independently retrieved.
- **No manager bank.** No manager source bank ran at this exact head, and none is claimed.

## Pending manager duties

- Complete the independent external review and accept the review ledger.
- Accept the hosted evidence at this head, including shard 4/5 `suite-logs-4` with the four counters `RESULT: PASS` lines, and the local replica.
- Carry R628-6-R1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `c6bd08c6`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`), with its builder and native banks.
- Run the merge-turn bench: controller display of FRAMES_TX at packet rate, Stream Input refresh, link-tap cadence and the reference-peer reset comparison.
- Obtain explicit merge authorization, check post-merge containment, and complete the issue and project.

## Evidence index and integrity

- **Toolchain.** Pinned simulator 5.050 (wrapper sha256 `905795b9…`). Builds were forced to two workers, and at most 16 jobs ran at once.
- **Raw logs.** `receipts/runs/` holds every run, escape, omission and shift log, path-normalized to `$PACKET`/`$CLONE`. Driver stdout is in `receipts/*.log`, with `.rc` files where recorded. Expected mutation failures are not gate failures; `accbind_avtp.rc=2` is the make wrapper propagating two named receive-test failures.
- **Scripts.** The manifest lists portable reviewer drivers and the four prior public probes. The prior probes' complete hashes and public Git-blob identities are in `receipts/public_source_index.tsv`. Set `VERILATOR` explicitly as shown in `REPRODUCE.md`; the optional two-worker wrapper takes `PINNED_VERILATOR`. Old background-launch helpers are excluded from publication.
- **Resumed verification.** `receipts/resume_receipt_audit.log` independently re-grades 88 retained runtime logs. The original snapshot probe's local executable fallback had been substituted in the interrupted packet; I restored the exact published bytes and reran it successfully with the executable supplied by environment. No source bytes changed. The guard mutation and final integrity check also ran in the foreground.
- **Public source evidence.** The eight saved author evidence files were verified against Git blobs at [the published evidence commit](https://github.com/kebag-logic/milan-fpga/tree/cedfdbdacb2ca61e40a487e5f9b460f0376f278e/review-evidence/726-r1); the index records their original paths and hashes. These author receipts establish source execution, not a manager source bank.
- **Clone integrity.** `receipts/final_tree_check.txt` shows exact head and tree, 1,300 regular-file blobs byte-identical, modes matching, index equal to HEAD with no flags or stages, and an empty status including ignored files. Initialized submodules sit at their gitlinks and are clean. All probes used scratch copies; ignored caches created during the runs were removed.

R628-6 FINISHED
