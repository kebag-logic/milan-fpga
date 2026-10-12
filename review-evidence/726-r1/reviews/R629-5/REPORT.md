[R629] POSITIVE - exact head e7d604faa0472d505d6459883b382c2b237ad06d

External independent review R629-5 of issue #726 / PR #729. All five lenses were applied to the full change from `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. No open BLOCKER, MAJOR or MINOR remains in this source review. One PR-body wording residue remains. This verdict does not establish completion of the issue or authorize merge.

Reviewed tree: `641f45e32b484bb1da1d34379d5e19f0588f52b3`. The latest delta, `1add0cfb..e7d604fa`, changes only the receive regression's printed IV8 explanation and the integration-suite README. It changes no stimulus, assertion, RTL, firmware implementation, configuration or gitlink. See `receipts/round5-delta.diff`.

Repository contracts, documentation authorities, frozen acceptance and public scope decisions were reconstructed before the diff and history. An independent source verdict and artifact-specific ledger were written before reading earlier reviewer findings. Earlier findings were then reconciled against this head and independently exercised. No private author material, management checkout, other active review report, hardware or GitHub mutation was used.

The controlling authorities are the [packet/reset ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), [IEEE-reference addendum](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), [assignment](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), [processor/throttle ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604), [corrected consecutive-gap criterion](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6132483068), and [Round 5 disposition](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6133625608). The corrected criterion supersedes fixed-grid grading. Full standards texts were not retrieved; no alternative interpretation was substituted for the explicit rulings.

**R629-5-R01 | RESIDUE | Docs**

Artifact: PR #729 body, Status: “Round 5 local head” and “Focused local validation passes; two new commits await publication.”

Authority/evidence: the public PR head is already `e7d604faa0472d505d6459883b382c2b237ad06d`, verified again at the final hosted snapshot. The two commits are published. This is residual handoff wording, with no change to a measurement, figure, verdict, test, generated artifact or conformance claim, and no privacy implication.

Impact: readers receive stale publication status.

Required outcome / exact fix: replace those two sentences with “Round 5 published source head: `e7d604faa0472d505d6459883b382c2b237ad06d`.” and “Focused local validation passes; both Round 5 commits are published.”

Verification: read the updated Status paragraph. Carry this item on the residue checklist. It does not make Docs unclean.

**Applied lenses and reviewer-owned ledger**

[R629] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:208,249`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:329,640,1154`, `hdl/ieee1722/crf/KL_crf_rx.sv:487,644`, `tb/verilator/milan_dp/stream_counters.hpp:173` - Applied IEEE 1722.1-2021 Tables 7.159/7.157 under the maintainer rulings. AAF and CRF transmit totals count AVTPDUs; receive totals count accepted AVTPDUs. Both wrap at 32 bits. TX resets at talker start, retaining a simultaneous first TX event. RX resets on not-bound to bound and preserves unbind totals. MR/TU retain their interval laws. Each changed stream descriptor reaches the scheduler. The corrected spacing and consecutive-gap criteria pass at both shapes. IV8 now states the same receive law as its assertions.

[R629] PASS RTL - those three engines; `hdl/milan/milan_datapath.sv:3159,3300,7924,7969`; pinned `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449` - Examined event decoding, same-cycle precedence, reset ownership, array indexing, 32-bit addition, AAF batch fold/drain and commit, CRF event deferral, descriptor mapping and pending-bit arbitration. Healthy events coalesce in the existing event path; the scheduler's eligibility and latest-recipient completion stamp remain the rate limiter. The AVB_INTERFACE producer and #60 throttle are unchanged. No CDC, clock, interface, submodule or firmware implementation change was introduced. The naming correction describes a one-cycle pulse rather than removing unit documentation. Published implementation evidence and its limits are recorded below.

[R629] PASS Robustness - `tb/verilator/tkdiag/sim_main.cpp:194,622`, `tb/verilator/crf_rx/sim_main.cpp:614,1129`, `tb/verilator/avtp_rxmon/sim_main_nx.cpp:566,648,796`, `tb/verilator/avtp_rxmon/sim_lockstep.cpp:390`, and `stream_counter_f5.cpp:73` - Exercised stop/restart, bind/unbind/rebind, tick boundaries, active reset, malformed and foreign input, rejected formats, context isolation, stopped-but-bound observation, wrap, anomaly preservation and delayed mailbox completion. A supplemental pending-batch probe seeds `0xfffffffe`, receives three real MAC packets, and reads `1`. The unchanged startup probe observes TV=3/TNV=0/FRAMES_RX=0 before publication and FRAMES_RX=3 afterward. The checker returns INFO with null ratio, then PASS. No-CRF descriptor paths remain controlled by the unchanged parent generate guards; finite simulated traffic is not physical proof.

[R629] PASS Tests - `tb/verilator/milan_dp/stream_counters.py:133`, `stream_counters.hpp:80,173,256,283,310`, `stream_counter_f5.py:41`, `tests/steps/counters_contract_steps.py:602`, `tests/features/counters_contract_milan.feature:42,198,318,418`, and `tb/tools/torture_campaign.py:298,829,880` - The real parser/counter/descriptor/processor/response-memory/MAC path supplies the packet census and notification timestamps. Frames-only runs isolate FRAMES_TX from TU/MR updates. Every shipped mutation has named detection and an omission escape; crashes and compilation failures do not count as detection. Existing behavior and focused RTL regressions pass. The contract probes and independent source-reader controls preserve detection of retained reset removal and the old snapshot guard.

[R629] PASS Docs - `docs/testing/726_STREAM_COUNTERS.md:10,31,51,135`, `docs/reference/REGISTER_MAP.md:149,869,963`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:220`, `sw/firmware/ctrl/aecp/README.md:55`, `tb/verilator/milan_dp/README.md:24,470,504,592,1163`, and the dated notes in findings 117, 394/387, 629, 667 and B14 - Current law and cadence claims match the rulings and executable measurements. Historical measurements remain dated; the archived traceability row points at the old source. COUNTERS is documented as bit 3, value 8. The suite README names all four temporary counter elaborations. Local documentation gates pass with unchanged budgets. R01 is wording residue only.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Rulings; three counter engines; IV8; real packet/reset/gap receipts | R629-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| RTL | CLEAN | Counter arithmetic and reset paths; parent event mux/arbiter; pinned scheduler; implementation provenance | R629-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Robustness | CLEAN | Focused receiver/talker/lockstep tests; pending wrap; startup snapshot; mailbox stall; shape guards | R629-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Tests | CLEAN | Four recursive counter legs; thirteen mutation/omission pairs; prior probes; retained-reset and snapshot controls; BDD and helper tests | R629-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Docs | CLEAN | Register map; measurement page; audit; findings notes; firmware and suite READMEs; IV8; PR body; documentation receipts | R629-5 | e7d604faa0472d505d6459883b382c2b237ad06d |

**Independent execution and measurement**

The prescribed simulator reported 5.050 before use; `receipts/tool-identity.json` retains its entrypoint hash and version. Tests ran in foreground-owned processes, with independent campaigns concurrent and bounded workers. No full parent, processor, synthesis or builder bank was run. All disposable trees and builds stayed under `scratch/`.

| Execution | Result |
|---|---|
| Receive regression | 97 single-sink, 119 NxN, 36 at each lockstep shape; all pass; clean control and four existing mutants pass |
| Talker diagnostics | 99 checks pass; existing clean/mutation controls pass |
| CRF receiver unit | 14,287 checks pass; 1,086 accepted PDUs pinned |
| `make -j16 -C tb/verilator/milan_dp counters` | rc 0; four `RESULT: PASS` lines |
| Direct shipping and largest counter fixtures, inherited `MAKEFLAGS=" -w"` | rc 0 at both shapes; 58/247 checks |
| Earlier shift launcher, unchanged | 0/200/300/800/900/1,000,000 cycles at both shapes: twelve PASS results |
| Full behavior gate | 14 features, 406 scenarios, 1,977 steps; zero failures or skips |
| Counter helper self-test | 80 tests pass |
| Earlier contract / cross-side / startup probes, unchanged | all pass; ruled pair PASS; interval-rate side FAIL attributed to that side |
| Retained reset controls | Ten counter resets and six anomaly flags individually detected; other era checks pass with the wipe check omitted |
| Old snapshot guard restored | Exactly the named startup test fails; the 79-test omission control passes |
| Pending AAF accumulator wrap | `0xfffffffe + 3 -> 1`; 58-check run passes |
| Firmware mailbox | Both shapes pass; 2 ms stall exercised; three mutation/omission pairs pass |
| Focused documentation/source checks | 73 workflow-derived commands plus HDL reference generation, imported documentation and two no-git checks: all rc 0 |

The local documentation selection includes `measure_naming --check`, `measure_test_evidence --check`, `check_py_idiom`, `check_cpp_idiom`, later idiom/CI/archive/TOC/shape gates and their applicable self-tests. No budget file differs from the base. It excludes prohibited full builder execution and host orchestration, so it is not claimed as the entire local workflow. The published author workflow ledger separately records its complete execution, including explicit NOT RUN arms and recovered/invalid invocations.

Cadence is measured over five compressed seconds, with 1000 simulation cycles per protocol millisecond and two registered recipients. Service runs from dirty-and-eligible to the final recipient's MAC tail. Every consecutive gap from the first notification and the final wait is checked. At least two notifications prevent a vacuous result; observations after the capture ends are excluded. Fixed bins are descriptive only.

| Shape | Descriptor/recipient rows | Consecutive gaps | Minimum gap | Maximum gap | Maximum measured service |
|---|---:|---:|---:|---:|---:|
| Shipping | 8 | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest | 36 | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

`receipts/local-gap-audit.json` independently recomputes these values from local NOTE timestamps, checking each row against its own service bound. `published-gap-audit.json` repeats the calculation on the public uncertain and frames-only receipts. The recursive local target also passes both frames-only shapes. Their output TU/MR counters and wire bits stay zero; the only initial start is followed by continuing FRAMES_TX changes. The output rows supply 16/72 gaps. The earlier 24/108 figures were graded fixed-grid row/windows, not the corrected acceptance metric.

Shipping AAF/CRF totals equal 799/101 completed MAC packets; largest-shape AAF outputs each equal 800 and CRF equals 101. Each input serves 500 received packets, preserves its unbind total and resets on rebind. Start/stop/restart and near-wrap output runs compare against actual emitted packets. The published source-base controls, independently audited rather than re-executed here, contain exactly 12/54 failures in TX, RX and CADENCE. Base output totals remain five and inputs cease recurring notifications.

| Plant | Required group | Named failures | Detection / omission exit |
|---|---|---:|---|
| tx-interval | TX | 6 | 1 / 0 |
| rx-interval | RX | 1 | 1 / 0 |
| tx-reset | TX_RESET | 4 | 1 / 0 |
| aaf-reset | RX_RESET | 1 | 1 / 0 |
| crf-reset | RX_RESET | 1 | 1 / 0 |
| rx-saturation | RX | 1 | 1 / 0 |
| late | CADENCE | 4 | 1 / 0 |
| rate | RATE | 8 | 1 / 0 |
| tx-nodirty, frames-only | OUTPUT_CADENCE | 4 | 1 / 0 |
| fixed-grid | PHASE | 8 | 1 / 0 |
| mailbox late | CADENCE | 8 | 1 / 0 |
| mailbox rate | RATE | 8 | 1 / 0 |
| mailbox fixed-grid | PHASE | 8 | 1 / 0 |

All thirteen pairs were executed in this round. Raw runtime logs and `mutation-audit.json` retain the named failures and clean escapes.

**Prior public finding dispositions**

| Prior finding and original lenses | Disposition at this head |
|---|---|
| R629-4-F01, MINOR, Conformance/Tests/Docs | Resolved. IV8 removes FRX from the anomaly list and states per-AVTPDU counting with batched publication. Local receive output shows six packets add six; late/early and other anomaly bursts remain +1. No assertion or RTL changed. |
| R628-4-R1/R2, RESIDUE, Docs | Resolved as specified: prior-head hosted result is attributed to Round 4; the two cited old statements are removed; README names the four temporary elaborations. R629-5-R01 is separate newly stale publication wording. |
| R628-1-F1 / R629-1-F01, MAJOR, Tests | Resolved. Unchanged contract reproduction and full BDD pass; sixteen retained resets are individually detected. The PR validation list names BDD. Current-head hosted bdd-conformance succeeds. |
| R628-1-F2, MINOR, Tests/Docs | Resolved. Both frames-only shapes pass; missing-output-event plant fails OUTPUT_CADENCE and escapes. Source-base driver requires TX/RX/CADENCE; published baseline failures match. |
| R628-1-F3, MINOR, Docs | Resolved. Four suite passages describe current packet laws and wire-count/reset/wrap checks, with the old numerical observation retained as history. |
| R628-1-F4, MINOR, Tests/Docs | Resolved. Trap (3), law table, grader and flowing interval-rate FAIL scenario implement Table 7.157. |
| R628-2-F1, MAJOR, Docs/Tests/RTL | Resolved. The naming boundary retains its unit meaning; source-reader disposition and Python/C++ idioms pass without budget changes. Public author workflow receipts and the directly verified successful Round 4 hosted docs-check settle the prior retained confirmation under decision 6133625608. Current-head hosted docs-check is still pending, separately recorded below. |
| R628-2-F2, MINOR, Conformance/Tests/Docs | Resolved. Unchanged cross-side probe passes the ruled pair and attributes an interval-rate regression to the correct side. Concurrent-flow and assertion contracts require the measured packet law. |
| R629-2-F01, MINOR, Robustness/Tests/Docs | Resolved. Unchanged receiver-backed zero-publication probe passes; restoration of the old guard fails the standing startup regression and passes only its omission control. |
| R628-3-F1, MAJOR, Conformance/Tests/Docs | Resolved by public ruling 6132483068 and its implementation. Consecutive gaps replace grid grading, all twelve shifts pass, PHASE plants detect the old grader, and current texts explain drift. |
| R628-3-F2, BLOCKER, Tests/Robustness | Resolved. Inherited `-w` and recursive target pass locally. The prior head's successful hosted shard 4/5 and its four counter PASS lines are independently verified, settling the retained item under decision 6133625608. This is not current-head aggregate acceptance. |
| R629-1-F02; R628-2 RS1-RS5; R628-3-R1 / R629-3-R01, RESIDUE | Their exact corrections remain: obsolete publication wording removed, COUNTERS bit 3/value 8, per-run terms, specified harness banners, wrapped comment and corrected self-test descriptions. |
| R628-2-S1, SUGGESTION, Conformance/Tests | Its drift concern became R628-3-F1, now resolved. |
| R628-2-S2 / R628-3-S2, SUGGESTION, Tests | Resolved: capture-end filtering is present in both gap collection and grading. |

Optional suggestions remain optional, with no clean-coverage effect:

| ID / severity / all lenses | Artifact and evidence | Impact; optional outcome; verification |
|---|---|---|
| R628-1-S1 / R628-2-S3 / R628-3-S1 / R628-4-S2; SUGGESTION; RTL, Robustness | `hdl/ieee1722/crf/KL_crf_rx.sv:487,644`: explicitly ordered bind reset follows acceptance | Coincident CRF acceptance belongs before the reset, unlike the retained TX event. Optional alignment or clarification; verify simultaneous bind/PDU ordering. No new defect severity is assigned. |
| R628-1-S2 / R628-2-S4 / R628-3-S3 / R628-4-S3; SUGGESTION; Tests | `tb/verilator/milan_dp/sim_nxn.cpp:2596`: constant pause bound matches the present notify clock | Future clock changes could stale the bound. Optionally derive it from the clock parameter; verify current and alternate clock recipes. |
| R628-4-S1; SUGGESTION; Tests | `tb/verilator/milan_dp/stream_counters.py:26`: standing RX interval plant targets CRF; healthy suppression plant targets inputs jointly | Optional per-engine mutation inventory expansion; verify each new plant's named failure and omission escape. Existing assertions and required plants pass. |
| R628-4-S4; SUGGESTION; Tests | `tb/verilator/milan_dp/stream_counters.hpp:64,190`: service allowance is measured in the same run, as ruled | Uniform service degradation could enlarge its allowance. Optionally add an independently specified ceiling; verify a delay exceeding it fails. Current measured maxima remain explicit. |

**Published implementation evidence, hosted state and limits**

The [public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/727f29284f7f6a15d6529df6884bd2ef028320d0/review-evidence/726-r1) was read through immutable blobs; `public-provenance.json` records verified object identities and SHA-256 values. The five measured RTL/configuration hashes match the initial reviewed head. Three still match exactly; the two differing RTL files have identical non-comment tokens. `implementation-provenance.json` records that narrower equivalence claim.

The routed report contains 49,427 LUT, 53,378 FF and 87.5 BRAM tiles. The author-reported +35 LUT delta is against 49,392, below the +200 STOP threshold; the base build was not regenerated. The published shipping TDM8 recipe names part `xc7a100t-fgg484-2`, AreaOptimized_high synthesis, ExploreArea optimization, ExtraPostPlacementOpt placement and AggressiveExplore physical/routing directives, with no seed override in the Tcl. WNS/WHS +0.451/+0.036 ns are retained author measurements, not a new review measurement. Published Slow/Fast negative-path reports contain no negative paths. External I/O constraints remain limited; endpoint temperature reports are metadata, not independent timing models. No implementation run was performed here.

Firmware implementation and saved-state capture inputs are unchanged; the firmware-tree delta is its AECP README. `check_nvm_capture` passes. This diff does not trigger capture remeasurement. The F5 fixture explicitly injects counter-change calls into the real core/mailbox adapter; it does not prove a production caller supplies them or establish processor instruction timing.

The prior Round 4 docs-check and shard 4/5 succeeded. The downloaded `suite-logs-4` archive matches digest `ce8ade113234c8ae0243dfa226405e90a04e69eaf235e4aea087d3af94f5ae0b` and contains four counter PASS lines. Its actual tested merge was `fb261fdb0b7ae4ccce5379f78119bb1a48d8d1a1`, whose parents are live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae` and Round 4 head `1add0cfb...`. The prior overall aggregate later failed with shards 1/5 and 2/5 cancelled; no full green aggregate is inferred from shard 4.

At `receipts/hosted-final.json`'s timestamp, the current-head bdd-conformance, simulator lint, firmware AECP mutation job, wire-accountability and no-git documentation check succeeded. Docs-check, elaboration and other fast jobs were still running. The exhaustive workflow had no completed current-head acceptance. These are workflow observations associated with the published head, not a reviewer-run source bank. Hosted and local-replica acceptance belong to the manager.

Local runtime was Python 3.14.7, not the documented 3.12.3. The pinned Markdown/HDL-reference dependencies were installed only under this packet's scratch directory. Full builder/compiler installation and prohibited host orchestration were not run. Source-head gate evidence beyond the focused checks is the author's published evidence. No manager source bank ran at this exact head, and none is claimed.

Physical calibration is NOT RUN. Field skips provide no hardware proof. Finite compressed-time runs cover two recipients, not maximum fanout, indefinite wall-clock operation or a physical link. Acceptance's controller display, link-tap measurements and reference-peer reset comparison remain merge-turn work.

**Remaining manager duties and packet integrity**

The manager must accept the current-head hosted and local-replica evidence, complete both independent-review requirements, and carry R01 to the residue checklist. The manager must build and validate the final current-dev merge candidate, including builder and native banks, and link its receipts. Source base `c6bd08c6` is distinct from live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`; neither source review nor the prior hosted merge substitutes for the final candidate. Merge-turn physical acceptance, explicit merge authorization, post-merge containment, final documentation and issue/project completion remain pending.

`checkout-verification.json` proves the original review clone's exact head/tree, all 1,300 regular-file blob bytes and modes, stage-zero index equality and absence of hidden index flags. All five gitlinks equal the base. The initialized processor, gPTP and stream-library submodules match their gitlinks and tracked bytes/modes/index; `external` and `third_party/lwSRP` remain uninitialized with unchanged pins. The original clone is clean. No source restoration was needed because all builds and probes used disposable scratch trees.

Portable drivers and raw runtime receipts are listed in `MANIFEST.sha256`. Build transcript copies normalize workspace paths for publication; numeric results, assertions, return codes and verdicts are unchanged. Original build transcripts remain unpublished under scratch. The packet's scope deliberately excludes scratch, downloaded source trees, build products and private material. All reviewer-owned jobs finished before this report was finalized.

R629-5 FINISHED
