[R475] POSITIVE - exact head 7426045c94c317363e5589856e6f3f9fde1a2d21

External independent review R475-8 of issue #645 / PR #672, including the assigned #647 behavior. Tree `472a2a9a844429005aec3dbd396fa02be29bf39d`; source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`; focused delta `1e79ebdc..7426045c` (rounds 2h and 2i).

All five lenses are CLEAN for this assigned delta. R474-5-F1, R475-6-F1, R474-5-S1 and R475-7-F1 are RESOLVED at this head under their original severities. No new BLOCKER, MAJOR, MINOR or RESIDUE is raised. Three earlier optional suggestions remain. This verdict does not authorize merge or claim completed hardware acceptance.

The review reconstructed the repository contract and documentation map, frozen issue acceptance and public decisions, requirements/interfaces, base-to-head change inventory and production changes, focused diff/history, then public executable receipts. `receipts/independent-verdict-ledger.md` records the independent verdict and all-five-lens ledger written before prior reviewer findings were read. No private author material or other checkout was used. The formal-review and inline-comment collections are empty.

The [round 2h assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6075072415) requires four concurrent standing legs, an honest hosted timing basis, separate slip/recentre accounting and the explicit-campaign disposition. The [round 2i assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6076487047) requires exact decimal bins and measured hosted records. These preserve the existing product contract: eight LOCKED windows under following, 2,048 qualifying INTERNAL ticks, a 2^20-tick ceiling, depth 16/target 11, exact symmetric actions within two consecutive output PDUs, strict ordering outside the action, unchanged slip counters for recentres and the narrowly declared second-pull recovery residual. The issue body's physical repeat remains the manager's duty.

**Finding dispositions at this head**

**R474-5-F1 - MINOR - Tests, Docs - RESOLVED.**

Artifacts: `tb/verilator/follow_ring/Makefile:22-36,77-114`, `tb/verilator/milan_dp_render/Makefile:46-62`, `docs/testing/TESTING.md:291-344`, PR Round 2h/2i sections. Authority: the original finding and the two assignments above require figures attributable to their actual invocation and receipts. Impact of the former defect: a parallel local run substantially understated serial-hosted runtime; the subsequent correction lacked publicly verifiable raw receipts. Required outcome: bounded default concurrency and measured, source-bound timing records, with projections explicitly distinguished. Verification now establishes both:

- Serial outer make and outer `make -j16` each execute one shared `b8`/`pullin` build, the separate fine-clock build, all four controller rates and all standing checks. The unchanged Makefile's instrumented scheduling probes reach exactly four simultaneous legs, with consumers after the shared build, and propagate each failed leg to a nonzero outer verdict. No target or suite list changed.
- The public [round 2h archive](https://github.com/kebag-logic/milan-fpga/tree/5c575da7157c814088ea4df12aab6c5877841f4b/review-evidence/645-r1/author-r2h) now supplies the missing receipts. All 277 manifest entries and 45 candidate-source bindings verify. The serial four-CPU cold receipts record 437.204 s for follow_ring and 793.308 s for render, both rc 0, with invocation and affinity. The former is below the assigned 708 s replica limit. The 1.78 and 1.324 historical ratios yield the stated projections, 778.2 and 1050.3 s.
- The records now identify measured `8e4b1e53` hosted windows from [run 37892515345, job 113696564335](https://github.com/kebag-logic/milan-fpga/actions/runs/37892515345/job/113696564335), sequential `make -C`, `ubuntu-latest`/`ubuntu-24.04`. Independently downloaded raw log SHA-256 `d7ae7e49d237e8da6c96be21fa2f7bdac33d61b3060d1fcd088bc7d37a678142` matches the published receipt. Exact verdict-timestamp differences round to 1114.2 and 1218.7 s. All three records match the table below. Render's lower projection is explicitly acknowledged. Later-head hosted acceptance remains separate.

| Measured hosted suite at 8e4b1e53 | PASS window | Margin to 1440 s | Margin to 1800 s |
|---|---:|---:|---:|
| follow_ring | 1114.2 s | 325.8 s | 685.8 s |
| milan_dp_render | 1218.7 s | 221.3 s | 581.3 s |

Receipts: `public-verification.json`, `public-author/`, `hosted/round2h-*`, `defaults/`, `schedule/`, all under `receipts/`. The follow_ring hosted measurement also leaves 145.8 s below its assigned 1260 s line.

**R475-6-F1 - MINOR - Tests, Docs - RESOLVED.**

Artifacts: `tb/verilator/follow_ring/sim_main.cpp:550-559,618-626`, `trace_table.py:9-28,54-62,90-98`, `test_trace_table.py:47-82`. Authority: `MEDIA_CLOCK_FOLLOWING.md:1096` and `REGISTER_MAP.md:1870` distinguish declared actions from slip counters. Former impact: the diagnostic falsely counted a passing recentre as a slipped frame. Required outcome: counter-derived duplicate/skip counts, a separate recentre count and the current ring law. Verification: the unchanged public margin-step probe prints zero slips and marks missing event evidence as unavailable; fresh passing simulations each have 18 checks and rc 0. The declared pulse at 5.454116560 s yields counts 0/0/1, the genuine duplicate at 1.580711280 s yields 1/0/0, and the genuine skip at 38.557170800 s yields 1/1/0 (slips/skips/recentres). A simultaneous action and duplicate remains counted by the standing test. The docstring states 16 entries and target 11. Receipts: `legacy/`, `fresh-traces/`, `standing-trace.log`.

**R475-7-F1 - MINOR - Robustness, Tests, Docs - RESOLVED.**

Artifacts: `tb/verilator/follow_ring/trace_table.py:43-51,72-105,117-131`, `test_trace_table.py:85-156`. Authority: the documented exact `[start, end)` contract and round 2i assignment. Former impact: decimal arithmetic could omit an inclusive-start event, admit an exclusive-end event or assign an interior event to the preceding bin. Required outcome: identical exact time arithmetic for event and PDU data, preserving both sides of an edge without a grace interval. Verification: the unchanged public decimal driver passes 9/9; all eight standing methods pass, retaining the five original tests. Twelve independent integer-clock-oracle cases pass for all three event kinds, checking event counts and PDU range membership at decimal edges, negative origins, a partial last bin, large absolute times and 1e-30-second separations. Eleven invalid CLI inputs are rejected. The earlier reader fails the same public driver 0/9, rc 1, proving discrimination. Servo comparisons also use exact timestamps; row labels retain their documented rounding. Receipts: `public-decimal.log`, `decimal-boundaries/`, `own-boundaries/`, `invalid-cli.json`, `earlier-reader-negative.*`.

**R474-5-S1 - SUGGESTION - Docs - RESOLVED.**

Artifact: `scripts/measure_test_evidence_readers.py:92-98`. Authority: the original suggestion and round 2h item 4. Former impact: the disposition omitted the driver's explicit scheduling status. Required outcome: identify the mutants target as outside the default sweep. The exact clause is present. The evidence-contract check passes and its self-test passes 105/105. No campaign was silently removed. Receipts: `focused-gates/evidence-*`; the public round 2h mutant receipt records 12/12 caught.

**Earlier findings retained or resolved**

These are delta dispositions against unchanged artifacts, not claims of fresh full-campaign execution. Original severities and lenses remain assigned by their reviewers. No prior finding is worsened.

| Prior ID | Original severity / lenses | Disposition and current artifact evidence |
|---|---|---|
| R474-4-F1 | MAJOR / Tests, Docs | RESOLVED defect. The public 1e79ebdc hosted pass closed the original timeout; 8e4b1e53 independently confirms both corrected defaults. Acceptance of the latest hosted run remains a manager duty. |
| R475-1-F1; R474-1-F1/F2 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | Remain RESOLVED. The symmetric capture correction, two-PDU amendment and qualified recovery are unchanged. `KL_chan_map_capture.sv:879-916,1053-1101`; `milan_datapath.sv:6566-6653`; fresh four-rate controller and ten fine/paired-pull cases pass. |
| R474-1-F3 | BLOCKER / Tests, Docs | Remains RESOLVED. `gen_module_matrix.py:140-163` excludes the declared text input; fresh matrix check passes with seven controls. |
| R475-1-F3 | MINOR / Conformance, Tests, Docs | Remains RESOLVED by the same compiled-source traceability and unchanged marker at `follow_ring/Makefile:46`. |
| R474-1-F4; R475-1-F2 | MINOR / Docs | Remain RESOLVED. `MEDIA_CLOCK_FOLLOWING.md:1092` and `TIME_SYNC.md:386` state the disengaged 2048-tick dwell; controller checks pass. |
| R474-2-F1, superseding R474-1-S1 | MINOR / Conformance, RTL, Robustness, Tests, Docs | Remains RESOLVED. `KL_chan_map_capture.sv:895-897` excludes held pops. Capture bytes are unchanged; published round 2h HELD-DUP and STARVED-HELD-DUP controls are caught. |
| R474-2-R1/R2; R475-2-R1/R2 | RESIDUE / Docs | Remain RESOLVED. Recovery exception in `TIME_SYNC.md:489-492`; plural drops in `REGISTER_MAP.md:1870`; current PR Status names this head; `MEDIA_CLOCK_FOLLOWING.md:1086` names `g_src_recentre`. |
| R474-3-R1/R2; R474-4-R1 | RESIDUE / Docs | Remain RESOLVED. `follow_ring/mutants.py:6-13` identifies the four capture plants and selector; `TESTING.md:584` identifies all twelve controls and links to `#simulation`. |
| R474-2-S1 | SUGGESTION / Tests | RETAINED, optional; detailed below. |
| R474-2-S2 | SUGGESTION / Tests, Docs | RETAINED, optional; detailed below. |
| R474-2-S3 / R474-1-S2 | SUGGESTION / Tests | RETAINED, optional; detailed below. |

R475-3, R475-4 and R475-5 introduced no additional unresolved required defect. R474-6 stopped without a verdict and supplies no coverage.

- **R474-2-S1 - SUGGESTION - Tests.** Artifacts: `follow_ring/settle_control.py:53-60`, `quiet_distributions.py:68`, production two-cycle band. Authority/evidence: the directed tests cover magnitude 1 as quiet and 3 as an excursion but do not directly pin magnitude 2; the distribution reader accepts a supplied band. Impact: weaker protection against lowering the band. Optional required outcome: pin the inclusive two-cycle boundary to the production contract. Verification: +/-2 stays quiet and a one-cycle-band mutation fails.
- **R474-2-S2 - SUGGESTION - Tests, Docs.** Artifacts: `MEDIA_CLOCK_FOLLOWING.md:1119-1149`, the follow/render clock configurations. Authority/evidence: full quiet distributions use 6.25 MHz, fine pulls 25 MHz, and the four-rate controller tests do not measure complete 50 MHz loop dynamics. Impact: shipping-clock quiet/recovery behavior has less standing executable evidence. Optional required outcome: record a full-loop 50 MHz quiet/pull-in case and its latency. Verification: no quiet arming and measured action/rearm times on a gradable stream.
- **R474-2-S3 / R474-1-S2 - SUGGESTION - Tests.** Artifact: `milan_dp/sim_ax1x1gptp.cpp:1101`. Authority/evidence: the no-decision branch reports uncounted NOT RUN; separate missing-action controls supply non-vacuity evidence. Impact: this scenario alone can omit recentre checks. Optional required outcome: require an action where the scenario guarantees one. Verification: suppress that action and require a named failure. This review did not execute that physical-network simulation.

**Reviewer execution and provenance**

The scoped simulator was verified as 5.050, revision v5.050, before use; launcher SHA-256 is in `receipts/defaults/identity.json`. Independent cold defaults overlapped in separate archive copies and disjoint four-CPU sets, with MAKEFLAGS unset. Every subprocess was joined by its foreground parent. Compiler workers and campaign workers were capped at two; no more than sixteen compiler workers could run across the two builds. Fresh trace acquisitions overlapped after compilation. Disposable trees and full large traces stay in scratch. No vendor build ran.

| Independent execution | Result |
|---|---|
| Cold serial outer default | rc 0; 620.118 s |
| Cold outer `make -j16` default | rc 0; 619.423 s |
| Each default's unchanged checks | b8 48/0; pullin 18/0; fine/paired pulls 10/10; controller PASS at 6.25, 25, 50 and 100 MHz |
| Makefile orchestration probes | 10/10; shared build once, separate fine build, four-leg overlap and each failed leg propagated under both invocations |
| Fresh real trace controls | Declared, duplicate and skip: each 18/0, rc 0; tables give expected counts |
| Standing CLI / public decimal / independent boundaries | 8/8 methods; 9/9 public cases; 12/12 own cases |
| Invalid CLI / earlier-reader negative control | 11/11 rejected; earlier reader 0/9, expected rc 1 |
| Evidence and traceability | Contract check PASS; self-test 105/105; matrix current, controls 7/7 |
| Public author evidence verification | Round 2h 277/277 manifest entries and 45 bindings; round 2i 407/407 entries and five bindings; all 48 round-2i validation result rc files match zero |
| Final checkout integrity | All 1232 superproject files and required submodules match raw blobs, modes and stage-zero indexes; clean status |

The two cold timings above use reduced worker counts for the review resource limit. They prove both real invocation forms and preserved checks; they do not replace the published 437.204/793.308 timing basis. The render default and twelve-mutant campaign were verified through the author's published round 2h logs, not rerun here. The author's source-head builder receipt is rc 0 in 1231.392 s with its historical gate-11 calibration explicitly NOT RUN. It is not a manager source-bank result.

**Reviewer-owned coverage ledger**

Every row is applied at this exact head. Coverage is for the assigned round 2h/2i delta and the unchanged artifacts identified, not a claim of new full-bank, synthesis or physical validation.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645 frozen acceptance and decisions 6075072415/6076487047; `follow_ring/Makefile:77-120`; `trace_table.py:43-131`; `TESTING.md:291-344`; public timing receipts and preserved ring contract | R475-8 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| RTL | CLEAN | Base comparison of `KL_chan_map_capture.sv` and `milan_datapath.sv`; `sim_main.cpp:550-559,618-626` observation-only output; four-rate reset/dwell/recovery/ceiling checks; `scope-invariants.json` proves unchanged RTL, synthesis inputs and round-2f records | R475-8 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Robustness | CLEAN | `trace_table.py:43-131`; strict boundaries and partial bins; invalid CLI; simultaneous action/slip test; real counter traces; per-leg scheduling faults; controller and paired-pull receipts | R475-8 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Tests | CLEAN | `test_trace_table.py:47-156`; both actual cold defaults; instrumented unchanged Makefile; earlier-reader negative control; independent event/PDU oracle; public mutation logs; evidence 105/105 and matrix controls | R475-8 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Docs | CLEAN | `TESTING.md:291-360`; both Makefile timing headers; `trace_table.py:9-28`; `measure_test_evidence_readers.py:92-98`; PR Round 2h/2i; source-bound public receipts and downloaded hosted timestamps | R475-8 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |

**Hosted snapshot and limits**

At 2026-10-09T08:15:28.791377+00:00, `gh pr checks 672` was bound to this exact head. In [run 37901896695](https://github.com/kebag-logic/milan-fpga/actions/runs/37901896695), Verilator shard 3/5 and all four Yosys shards had succeeded; Verilator shards 0/1/2/4 were still running. The Yosys shard execution steps succeeded with restored caches; only their compiler-build-on-cache-miss steps were skipped. Lint, Yosys elaboration, bdd-conformance, wire-accountability, docs-check-no-git and full-ci-gate had passed. Firmware-unit, docs-check and elaborate remained pending. The exhaustive aggregate was not yet complete. Physical gPTP was SKIPPED, with no executed steps. Receipts: `hosted/checks-final.*` and `hosted/exact-head-*.json`. Pending hosted work is not a reason to withhold this source-review verdict; its acceptance belongs to the manager.

No full parent, processor, time-processor, portability, builder or physical bank ran in this review. No manager source bank exists at this exact head and none is inferred. Physical calibration is NOT RUN; field skips and simulation are not hardware proof. No hardware, shared install, external write, commit, push, merge or author contact occurred.

`receipts/scope-invariants.json` confirms no RTL, configuration, synthesis-input or resource-record change since round 2f. The target lists, suite discovery and budgets are unchanged. Both Makefiles' non-comment content is unchanged since round 2h. The round-2f resource records remain applicable as prior measurements; this is not new area/timing evidence. The real limits of the existing diagnostic loopback latency, narrow recovery residual, resource headroom and physical acceptance remain.

Two preparation issues were corrected without source edits: the first disposable archive omitted a shared harness header, and the clone initially lacked the populated lwSRP submodule. The failed preparation receipts remain in scratch and are not counted as passing tests. lwSRP was initialized at its existing pin. Final raw integrity proof covers processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, time processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce` and lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`. `external` stays uninitialized as received; its gitlink is verified. All review jobs finished, and no tracked source bytes or modes were altered.

**Pending manager duties**

Accept exact-head hosted checks, including follow_ring <=1260 s, and the required local replica. Obtain the independent internal verdict for both rounds and finish the public coverage ledger. At the merge turn, build the current-dev candidate and run the manager's builder/native banks and required explicit campaigns, linking their candidate receipts on the PR. The observed source base and live dev were both `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`; this source review is distinct from final-candidate validation. Preserve the three optional suggestions and the unproved calibration/physical limits. Run the assigned INTERNAL-to-AAF and AAF-to-CRF bench repeat, obtain merge authorization, perform containment, and complete public issue/project bookkeeping only under the repository completion contract.

Portable scripts and receipts are listed in `MANIFEST.sha256`. Local installation and checkout prefixes are normalized for publication; `receipts/path-normalization.json` records the raw and published hashes without changing commands' flags, measurements or verdicts. Raw originals and disposable products stay in scratch, which is excluded from publication. The manager publishes the listed files and this report.

R475-8 FINISHED
