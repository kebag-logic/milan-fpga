[R475] POSITIVE - exact head 85db353400c6bf3965d279a9f5b5d47e08a0d1ed

External independent review R475-4 of issue #645, its included #647 work, and PR #672, round 2e. All five lenses are CLEAN at this source head. No BLOCKER, MAJOR or MINOR remains open within the assigned scope. One wording RESIDUE and three previously classified SUGGESTIONs are retained below. This verdict does not establish completion of the current-dev merge candidate or physical acceptance.

The reviewed tree is `67922e03f4c2d5d8add9b41f6f4c169ea3c9a364`. The review reconstructed repository instructions, documentation entry points, frozen acceptance and public decisions, linked requirements/interfaces, the full `99e4eb6c..85db3534` diff and history, then published executable evidence. The independent verdict and five-lens ledger were written to `receipts/independent-verdict.md` before opening prior public review findings. Those findings were then reconciled below. No private author material or other current-round review was used.

The controlling assignment is [6050481968](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6050481968), with [REVIEW READY 6056511818](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6056511818). Public source execution evidence is the [author-r2e packet at 00f489b1](https://github.com/kebag-logic/milan-fpga/tree/00f489b18c63d9cf7e617ddb9e0437902062d416/review-evidence/645-r1/author-r2e). All 1,304 extracted packet files matched immutable Git blob identities; `receipts/evidence-audit.json` identifies 407 examined raw receipts by path and SHA-256. These are author executions inspected and regraded here. There is no manager source-head bank at this head.

**Merge composition and source integrity.** The requested delta from `2525eae9567865a8bc741901914bdf5a1caf2c26` consists of automatic merge `9a0d68e2016c0385171107277721aa187ce19674`, followed by the two requested prose corrections. The merge's ordered parents are that lane head and `99e4eb6c14462aafa84bb1ac597fd241abc1a240`; its tree is `ab3b01f04b6954e3355add953d5e3c038bd4bc2c`.

Against common ancestor `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`, the lane's 38 changed paths and incoming dev's 91 changed paths are disjoint. Every changed entry from each parent survives exactly in the merge, and its remerge diff is empty. The final commit changes only `docs/testing/TESTING.md` and the `tb/verilator/follow_ring/mutants.py` docstring. The media-clock following, render recentre and loopback behavior therefore survives intact alongside F2, F3, processor pin #682 and GMII fix #691. The mailbox changes retain their external interface; the AAF path does not acquire a mailbox dependency. The GMII fix captures pads directly in input registers and applies sampled reset downstream, preserving the synchronous downstream contract.

`scripts/source_audit.py` checked raw tracked blob bytes, executable modes, stage-zero index entries and actual checkout heads before and after execution: 1,204 root blobs, 562 processor blobs, 104 gPTP blobs and 214 axis-library blobs, all PASS. Required gitlinks and initialized checkout heads are:

| Component | Exact gitlink/head |
|---|---|
| protocol-processor | `2ad2f845dd583f8310075fa2380cb60a04fd091a` |
| gptp-processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` |
| third_party/verilog-axis | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |

The pre-existing uninitialized `external` gitlink remains `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`. No source edit was made. Disposable mutation copies and builds remain under packet `scratch/`. Final tracked-content/index and whitespace checks pass; the clone is clean.

**Five-lens results.** Acceptance follows the public depth-16/target-11 and 0-60 us arrival ruling, symmetric correction and fine-pull amendment, the [two-PDU span ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440), [quiet-band/recovery ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115), and [held-empty accounting ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032466525). Authorities examined include `REQUIREMENTS.md`, `docs/reference/FR_NFR.md:252`, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1084`, `docs/design/TIME_SYNC.md:362` and `docs/integration/BUILDING.md`. Source selection, holdover and render-law obligations remain intact; simulation does not close the documented bench obligations.

[R475] PASS Conformance - `hdl/milan/milan_datapath.sv:6586`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:957`; `docs/design/TIME_SYNC.md:362`; public arrival/pull-in/render/timing/resource receipts - compared implementation and executable evidence against frozen acceptance and public amendments. Following waits eight 512 ms LOCKED windows; INTERNAL uses the declared quiet dwell; the ring corrects in either direction toward target 11. The declared wire action spans at most two consecutive output PDUs, with strict accounting outside it. Render-law grading begins at the declared boundary; ambiguous windows earn no pass credit. Ruled timing, IOB and own-area thresholds pass as detailed below.

[R475] PASS RTL - `hdl/milan/milan_datapath.sv:1313,6018,6533,6614,6664`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:501,885,957,1053,1101`; both merge parents and required gitlinks - checked root wiring, preserved #386 trigger, added settle trigger, render OR, reset/flush precedence, widths and same-cycle pop/push arithmetic. The 196,608-tick following dwell derives from the servo window; INTERNAL dwell/recovery is 2,048 media ticks with a 2^20 ceiling. Source changes/re-engagement take precedence. Per-stream decisions transfer to per-pair bounded holds/drops; clamped subtraction avoids underflow. `pop_dup_w` excludes declared holds, including still-empty pairs, while ordinary starvation resumes counting after the hold. Added state stays in the axis domain. Incoming dev changes compose without overwritten lane entries.

[R475] PASS Robustness - `tb/verilator/chmap_capture/sim_main.cpp:1663`; `tb/verilator/follow_ring/small_pulls.py`; `settle_control.py`; published arrival/pull-in logs - applied empty/full, unprimed, first-commit, flush/reset, both offset signs, phase/fanout, fine pulls, repeated pulls and disabled-servo/ceiling cases. Capture includes 72 span combinations: two signs, six output phases and six fanout offsets. Fresh capture and fine-pull runs pass; three targeted capture mutants fail their named checks. All 128 published arrival phases retain positive empty/full margins and no post-settle slips.

[R475] PASS Tests - `tb/verilator/follow_ring/dp_glue.py`, `sim_main.cpp`, `recovery_watch.hpp`, `mutants.py`; `tb/verilator/chmap_capture/sim_main.cpp:1663`; `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:672`; `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3745`; `scripts/gen_module_matrix.py` - checked extraction anchors, independent action/ordering expectations, strict boundaries, mutation discrimination, exact 61-suite inventory and #657 failures against dev. The physical-model wire plan derives from prefill and the declared target, rather than DUT hold outputs. Render LAW and PULLIN grading remain separate. The follow harness copies named root glue verbatim; it is not a whole-root elaboration. Optional coverage improvements remain below.

[R475] PASS Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1084,1544`; `docs/design/TIME_SYNC.md:383,489`; `docs/reference/REGISTER_MAP.md:1870`; `docs/testing/TESTING.md:514`; mutation-driver docstring; public issue/PR/evidence packet - checked dwell, recovery residual, two-PDU span, slip-accounting and test claims against code and receipts. R474-3-R1/R2 are applied. Generated traceability is current and does not misrepresent text extraction as root coverage. One locator-only residue remains; it changes no behavioral or measurement claim.

**Fresh reviewer execution.** The scoped simulator identity was verified before use as version 5.050, revision v5.050; wrapper/program hashes are in `receipts/simulator-identity.json`. All commands completed as foreground children. Independent capture/fine builds ran concurrently with eight compiler jobs each; their simulations also ran concurrently. Controller and mutation builds used at most 16 compiler jobs. No implementation run or prohibited full bank was executed.

| Fresh check | Result | Receipt |
|---|---|---|
| Capture behavioral suite, including LRC/SPAN and empty first-commit cases | 785 checks, zero failures; rc 0 | `receipts/chmap-run.log` |
| Fine INTERNAL pulls at 25 MHz, no-hold and two-pull recovery cases | 10/10; rc 0 | `receipts/fine-pulls.log`, `receipts/fine-results/` |
| Extracted settle controller at 6.25, 25, 50 and 100 MHz | All four pass; rc 0 | `receipts/settle-control.log`, `receipts/controller/` |
| SINGLE-DROP, HELD-DUP, STARVED-HELD-DUP disposable faults | Three caught at required checks; driver rc 0, fault runs rc 1 as expected | `receipts/capture-mutants.log`, `receipts/mutants/` |
| Module-matrix check | 7/7 controls; 77 modules, zero untested; rc 0 | `receipts/traceability.log` |
| Exact source/merge audit | Initial and final PASS, matching bytes/modes/index | `receipts/source-initial.json`, `receipts/source-final.json` |

**Published source evidence regraded.** These figures are from the immutable author packet, not fresh full-bank executions by this reviewer or the manager. `scripts/evidence_audit.py` checks raw rows, return codes, inventory and predicates rather than accepting summaries alone.

| Campaign | Regraded result |
|---|---|
| Complete suite sweep | Exact current inventory, each of 61 suites once; 2,185,760 checks, zero failures. Shards: 60 suites/2,173,696 checks plus milan_dp/12,064 checks. Some large logs are tails plus hashes; their full aggregate counts remain author execution evidence. |
| follow_ring standing gate | 12/12 named controls caught; 10/10 fine cases; controller at four rates. Capture receipts also report 785 behavioral checks and 20/20 netlist controls. |
| Arrival | 128 phases: both peer offsets, four envelopes, 16 phases each. All 384 post-settle windows have zero slips. Worst empty/full margins 2.17344/2.23488 ticks, both above the one-tick requirement. |
| Quiet distribution | 128 phases, 512 windows, 320,462,699 samples at 6.25 MHz. Signed peak magnitude one axis cycle; band two cycles meets the ruled factor of two. |
| Pull-in | 32 cases at 52/56 us; one action each and zero post-action slips. Four 56 us cases have pre-action slips. Grades: 28 ON THE LAW, two BEFORE NOT GRADABLE, two AFTER NOT GRADABLE. Ungradable cases earn no law pass. |
| tdm8render | All 18 pull-in phases gradable; 558 checks pass. Boundary sweep 81/81 over 564 windows; maximum walk three cycles against bound five. |
| Physical model | 197 checks, zero failures; startup/reset each declares and observes -5 events, dup/skip 0/0. Simulated wire evidence only. |

The #657 comparison is not green: dev `99e4eb6c` has 28/32, rc 2; the head has 30/34, rc 2. The same four failing lines remain: epoch-only clean control, acknowledgement arrival-skew clean control, serial-reset arrival-skew clean control, and surviving uncounted-repeat mutant. All 28 common passing rows agree; the additions are the clean pull-in leg and its missing-settle mutant. This satisfies the assignment's no-new-regression comparison while retaining #657's existing failures. None is resolved or silently reclassified here. Author builder/GMII receipts additionally report the patch-0007 gate, 1,036 GMII comparisons and six structural controls; those were inspected, not rerun as reviewer banks.

**Full-image timing and resource grades.** Applied [ruling 6045752839](https://github.com/kebag-logic/milan-fpga/issues/691#issuecomment-6045752839): grade the kept result of the three-directive sweep, requiring setup at least +0.030 ns, hold at least zero, full IOB acceptance and all nine GMII captures in ILOGIC. Raw reports use shipping 1x1 TDM8, `xc7a100tfgg484-2`, a 20 ns axis clock and the recorded common recipe. Slow/Fast timing models are distinguished from repeated 0/85 C temperature metadata; the latter does not establish four independent timing models.

| Placement directive | Worst setup WNS, ns | Worst hold WHS, ns | Grade |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.057 | +0.024 | Meets floor |
| AltSpreadLogic_high | +0.066 | +0.024 | Kept; meets floor |
| ExtraTimingOpt | +0.011 | +0.036 | Below setup floor; not selected |

All 12 corner reports have zero TNS/THS and zero failing endpoints. Each directive's full IOB check is 21 PASS, one INERT, zero FAIL; all nine GMII captures are in ILOGIC. The inert entry is unused RX error. No below-floor row has been relabelled a pass. The kept-bit receipt identifies SHA-256 `7b0c5eead7a68221c47e1f16077ec8ddbc3ca3631a033ff3e5e9235881c09977`, 3,825,992 bytes; the bitstream itself was not fetched or programmed.

The resource baseline matches source and recorded SHA-256 `aa8f90e775e76603d6179867abef9ecd7c13c91947c478ffcd12477e443128ef`. All three recorded resource checks return zero. Raw utilization reproduces:

| Endpoint | Baseline LUT / FF | Head LUT / FF | Delta |
|---|---:|---:|---:|
| Routed 1x1 | 49,957 / 54,274 | 49,913 / 54,309 | -44 / +35 |
| OOC 1x1 | 23,179 / 19,779 | 23,179 / 19,779 | 0 / 0 |
| OOC 8x8 | 30,135 / 27,380 | 30,135 / 27,380 | 0 / 0 |

The routed result is complete; slices move 15,734 to 15,754 and BRAM stays 87.5 tiles. This whole-image comparison is separate from the own-area budget: settle grows 41/51 to 74/93 LUT/FF (+33/+42); capture grows 1,076/1,336 to 1,156/1,372 (+80/+36), totaling **+113 LUT / +78 FF**, within **120/120**. Capture source blobs and extracted settle fragments match the compared base/head hashes. The complete generated source-input digest cannot be reconstructed from the trimmed public packet; exact-source admission and successful gate execution remain author receipts. The later dev resource re-record belongs to candidate validation.

**Prior public findings reconciled.** Public rounds [R475-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009109435), [R474-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009527655), [R475-2](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6031787384), [R474-2](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6032462363), [R475-3](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6041707628) and [R474-3](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6041843633) were read after the independent pass. The positive rounds at `2525eae9` are the delta baseline, not substitutes for this round's evidence.

| Prior ID, severity and attributable lenses | Disposition and verification at 85db3534 |
|---|---|
| R475-1-F1; MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED by public two-PDU amendment and matching independent SPAN oracle, exact action and consecutive-PDU checks. Fresh 72-case span coverage passes. |
| R475-1-F2 / R474-1-F4; MINOR; Docs | RESOLVED: design documents 2,048-tick INTERNAL dwell including disengaged operation; fresh controller checks pass. |
| R475-1-F3; MINOR; Conformance, Tests, Docs; also R474-1-F3, BLOCKER, Tests, Docs | RESOLVED: marked text dependency is excluded from elaboration attribution; generated artifacts pass fresh checking and exact-head hosted documentation jobs succeeded. |
| R474-1-F1; MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED: full-side multi-drop at capture line 957 is symmetric with holds; fresh capture tests pass, SINGLE-DROP is caught, both-sign arrival campaigns pass. |
| R474-1-F2; MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED: two-cycle arm band and recovery contract match code; fresh fine cases pass, with quiet/repeated-pull cases graded under public amendment. |
| R474-1-S1, subsequently R474-2-F1; MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED: `pop_dup_w` excludes all declared holds. Fresh empty-first-commit checks and HELD-DUP/STARVED-HELD-DUP discriminate the defect. Later ordinary starvation still counts. |
| R474-2-R1; RESIDUE; Docs | RESOLVED: `TIME_SYNC.md:489` states recovery residual in the accepted split wording. |
| R474-2-R2; RESIDUE; Docs | RESOLVED: `REGISTER_MAP.md:1870` says "held pops or dropped events". |
| R475-2-R1; RESIDUE; Docs | RESOLVED: current PR Status identifies the published review-ready head, replacing stale not-pushed/local status. |
| R474-3-R1; RESIDUE; Docs | RESOLVED: mutation docstring identifies all four capture controls and `--select`. |
| R474-3-R2; RESIDUE; Docs | RESOLVED: `TESTING.md:514` links all twelve controls and their named failure checks as requested. |
| R475-2-R2; RESIDUE; Docs | RETAINED below; prose locator only. |
| R474-2-S1; SUGGESTION; Tests | RETAINED below. |
| R474-2-S2; SUGGESTION; Tests, Docs | RETAINED below. |
| R474-2-S3 / R474-1-S2; SUGGESTION; Tests | RETAINED below. |

Retained items for the manager's checklist:

- **R475-2-R2; RESIDUE; Docs.** Artifact: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1086`, against `hdl/milan/milan_datapath.sv:6533`. Authority/evidence: the parenthetical locating the preserved #386 trigger says `g_settle_recentre`, but the block is `g_src_recentre`. Impact: wrong prose navigation label only; no measurement, figure, verdict, test, generated artifact, code, privacy or clause claim changes. Exact required fix: replace that parenthetical's `g_settle_recentre` with `g_src_recentre`. Verification: it names the preserved #386 block; surrounding behavior text stays unchanged.
- **R474-2-S1; SUGGESTION; Tests.** Artifacts: `tb/verilator/follow_ring/settle_control.py`, `quiet_distributions.py`, and shipped band at `hdl/milan/milan_datapath.sv:6586`. Authority/evidence: the ruled band is two axis cycles; the quiet reader takes a band argument, while controller cases do not directly pin non-arming at magnitude two. Prior public BAND1 survival remains compatible with that gap. Impact: weaker regression protection against lowering the correct constant. Optional outcome: assert +/-2 never arms, or bind the reader to the shipped constant. Verification: a one-cycle-band fault must fail while the current two-cycle design passes.
- **R474-2-S2; SUGGESTION; Tests, Docs.** Artifacts: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1107`, `tb/verilator/follow_ring/Makefile:36`, four-rate controller receipts. Authority/evidence: full quiet/arrival measurements are at 6.25 MHz; four-rate controller runs do not measure complete shipping-clock quiet distributions or pull-in latency. Impact: less standing evidence for 50 MHz dynamics. Optional outcome: add a 50 MHz quiet/pull-in case and identify its measured latency separately. Verification: no quiet arming and a recorded post-pull action at that clock.
- **R474-2-S3 / R474-1-S2; SUGGESTION; Tests.** Artifact: `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1101`. Authority/evidence: zero decisions print an uncounted NOT RUN instead of failing the physical-model scenario. The examined normal receipt contains two decisions, so that receipt is not vacuous. Impact: a future run of this leg alone could omit recentre assertions. Optional outcome: require a startup action where the scenario guarantees one. Verification: suppress the action and require a named failure. Separate controller and missing-action controls remain applicable.

**Reviewer-owned ledger.** All CLEAN entries are covered by this round at the exact source head. The residue rule and optional suggestions do not un-cover a lens. #657's unchanged failures remain outside this assignment's repair scope under its comparison ruling.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645/#647 acceptance and amendments; FR_NFR:252; MEDIA_CLOCK_FOLLOWING:1084; TIME_SYNC:362; raw campaign/timing/resource regrade in evidence-audit.json | R475-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| RTL | CLEAN | milan_datapath.sv:1313,6018,6533,6614,6664; KL_chan_map_capture.sv:501,885,957,1053,1101; both merge parents; source-final.json and gitlinks | R475-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Robustness | CLEAN | chmap_capture/sim_main.cpp:1663; fresh capture, fine-results, controller and mutant receipts; 128 arrival and 32 pull-in cases | R475-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Tests | CLEAN | follow_ring extraction/oracles/drivers; capture SPAN controls; sim_ax1x1gptp.cpp:672; sim_tdm8_render.cpp:3745; exact inventory and #657 base/head comparison | R475-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Docs | CLEAN | MEDIA_CLOCK_FOLLOWING:1084,1544; TIME_SYNC:383,489; REGISTER_MAP:1870; TESTING:514; mutation docstring; traceability.log; public task/PR/evidence and reconciled findings | R475-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |

**Limits and pending manager duties.** Source base is `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. Live dev observed during review is `17f62ef64a66562384e8a93b1d6be6f86e51f95c`, including #654 and #686's resource re-record. The manager must validate the final merge with live dev, run its builder/native candidate banks, publish candidate receipts and reapply relevant coverage if the merge changes a reviewed artifact. This report contains no manager source-bank claim and does not transfer source evidence to an unexamined candidate.

The exact-head hosted snapshot at 2026-10-08 12:31:08 UTC records successful rtl-fast, documentation checks, elaboration, firmware unit, lint, BDD, wire-accountability and all four Yosys shards. Verilator shard 3/5 succeeded; shards 0/5, 1/5, 2/5 and 4/5 were still running. Final long-gate aggregate conclusions were not established by this snapshot. Physical gPTP was SKIPPED, not executed. `receipts/hosted-snapshot.json` retains job URLs and conclusions. The manager owns final hosted/local-replica acceptance; no local replica was run here.

Physical calibration is NOT RUN; field skips and simulated physical-model checks are not hardware proof. The later bench repeat remains pending. The manager must publish this review, retain the residue and optional suggestions, reconcile the independent-review bar with no review in flight, obtain explicit merge authorization, and perform candidate validation and post-merge containment before claiming task completion. No GitHub write, source fix, commit, push, merge, hardware action or author contact was performed here.

**Reproduction and publication.** `MANIFEST.sha256` lists every publishable file; `scratch/` is excluded. The scripts accept checkout/packet paths and keep disposable material under packet `scratch/`: fetch with `fetch_public_evidence.py PACKET`; audit with `evidence_audit.py REPO PACKET/scratch/author-r2e PACKET/scratch/evidence-tree.json`; run `source_audit.py REPO`; use `focused_checks.py REPO PACKET SIMULATOR build`, then `run`, `controller`, and `mutants`. The focused driver records commands, logs and exits. `publish_receipts.py REPO PACKET SIMULATOR` exports nested raw receipts with host-path replacement only. `receipts/publication-redactions.json` records original and publication hashes; logical output and exits are preserved. The traceability check was `python3 scripts/gen_module_matrix.py --check`. No disposable tree is needed to interpret the published verdict.

R475-4 FINISHED
