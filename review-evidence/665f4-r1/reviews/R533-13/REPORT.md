[R533] POSITIVE - exact head 154722e14781c7373f3229420b6e007f9bcf9835

R533-13 external independent delta review of issue #665 / PR #690. Tree `1928df9c4d94eadc68e864b219a68270227e9f41`. All five source-review lenses are CLEAN. R532-12-F1 is resolved; R533-12-R1 is corrected. No open BLOCKER, MAJOR or MINOR remains in this review. R532-12-S1 remains optional. This verdict does not authorize merge or complete issue #665.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, linked requirement/interface authorities, the source-base diff `99e4eb6c14462aafa84bb1ac597fd241abc1a240..154722e14781c7373f3229420b6e007f9bcf9835` and history, then public executable evidence. Detailed review focused on `efea74858dffc482820d4f19c26c38796a57ff75..154722e14781c7373f3229420b6e007f9bcf9835`. The complete changed-path inventory and history are in `receipts/scope.txt` and `receipts/history.txt`; the focused patch is `receipts/delta.patch`.

Controlling inputs: [F4 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [full testing](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385), [interface and #608 additions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6009661573), [linked-size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), [kind-change and retained-withdrawal decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6049530812), [callback-contract decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6050694779), [round-13 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6051940062), and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6052380945).

The independent pass, verdict and five-lens ledger were written in `receipts/independent-pass.md` before reading prior reviewer findings or reports. Prior public findings were then reconciled. No private author material, other checkout, or management scratchpad was read. GitHub access was read-only; no source edits, commits, pushes, sub-agents, hardware operations or merge occurred.

**Round-13 findings disposition and evidence**

| ID / severity / attributable lenses | Disposition and exact-head evidence |
| --- | --- |
| R532-12-F1 / MINOR / Tests | RESOLVED. `sw/firmware/ctrl/test/srp_feedback.hpp:87-137` adds all three required standing cases. Each enters through `mbx_model_rx`, services the real composition loop and checks exactly one received PDU. Both sinks run at IF=1/2, with sink-to-interface routing from `test_acmp_mbx.cpp:99-114`. The cases pass in normal and sanitizer builds. |
| R533-12-R1 / RESIDUE / Docs | RESOLVED. `docs/design/MAILBOX_SPLIT.md:294-297` now names `9197193e47a6bb1c45a56d90a18c1784123aba44`, matching the gitlink and harness pin. Local documentation checks pass. No residue remains from this item. |
| R532-12-S1 / SUGGESTION / RTL, Tests | RETAINED OPTIONAL, not implemented. Detailed assessment below. It does not dirty either lens. |

| Standing case in `srp_feedback.hpp` | Plant in `srp_mutants.py:802-814` | Named observable | Independent result |
| --- | --- | --- | --- |
| `FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` (:87) | `feedback-leave-clears-advertise-only`, exact q04 replacement | `retained withdrawal reprobes` | Unmodified PASS; plant CAUGHT at IF=1 and IF=2 |
| `FailedReplacementWithdrawnInsideOnePduStillReprobes` (:104) | `feedback-failed-indication-as-advertise`, exact q13 replacement | `retained withdrawal reprobes` | Unmodified PASS; plant CAUGHT at IF=1 and IF=2 |
| `BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal` (:122) | `feedback-change-clears-both-kinds`, exact q06 replacement | `continuous Advertise is not withdrawn` | Unmodified PASS; plant CAUGHT at IF=1 and IF=2 |

The first case starts settled with Failed, then places Failed Lv and Failed New inside one PDU. The second starts with Advertise, then places Failed JoinIn, Failed Lv and Advertise JoinIn inside one PDU. Both must enter the reprobe state and retire the old binding. The third proves both kinds are registered, then sends Failed Lv and Advertise refresh in one PDU. It must remain settled and bound, with Advertise reported by GET_RX_STATE and no impossible event.

Each mutation compiles and fails after ingress at its intended behavioral assertion. None is credited for a setup or build failure. `srp_mutants.caught()` requires the named test and diagnostic. Independent runs use the standing campaign function with the three-entry subset; `test_ctrl_firmware.py:197-205` includes all three in its complete IF=2 pass and its `feedback-` IF=1 selection. `receipts/probe-equivalence.json` verifies exact q04/q13/q06 replacement text. Six individual mutation logs retain the actual failures.

The byte-identical public `r12_failed_intrapdu.hpp` was appended only to disposable test copies. Its three original `SrpFeedback.R12*` cases pass at IF=1/2 (`receipts/prior-probes-if1.log`, `prior-probes-if2.log`). Header SHA-256: `7fa2d66d681f1ceaf8a0dbcbf2e98bb602bd7b4a22b081bc29fd53042ea45c32`.

**Callback contract and optional assertion**

R532-12-S1 | SUGGESTION | RTL, Tests | `sw/firmware/ctrl/srp/srp_mbx.c:30-41,159-190,572-585`.

Authority/evidence: the pinned [integrator contract](https://github.com/kebag-logic/lwSRP/blob/9197193e47a6bb1c45a56d90a18c1784123aba44/doc/integrator.md#L321-L323) prohibits synchronous callback reentry and assigns enforcement to the adapter. The receive-interest callback reads copied indication state and calls only `capture`; it makes no owning-library call. Registrar visits occur before/after receive, after timer service, and in the poll, outside callbacks. The external adapter-entry guard still asserts in debug and counts/refuses release reentry. The debug suites pass at both counts.

Impact: a future source regression restoring `snapshot()` inside the filter could evade today's runtime checks. There is no such reentry at this head. The prior q10b escape is accepted as the scope of this optional suggestion, not reported as an independently rerun probe here.

Required outcome: none for this tests-only delta. If adopted later, hold a dedicated debug flag across library receive/timer/transmit calls and assert that snapshot visitation occurs outside that interval. Verification would restore the forbidden call in a disposable copy and require its named assertion. Its absence is acceptable as a SUGGESTION; the current contract is satisfied by the examined call paths.

**Independent execution and published evidence**

All foreground drivers waited for their children. Independent builds and campaigns ran concurrently, at most sixteen requested compilation workers. All disposable copies and build outputs stayed under `scratch/`.

| Check | Result / receipt |
| --- | --- |
| Composition, normal, IF=1/2 | 52/52 tests per count; `receipts/plain-if1.log`, `plain-if2.log` |
| Three standing plants, IF=1/2 | Six named behavioral catches; `plants-if1.log`, `plants-if2.log` and six individual logs |
| AddressSanitizer, IF=1/2 | 140/140 tests per count: adapter 53, retained receive 17, bounds/application 5, composition 52, latency 5, selected processor-wire differential 5, debug 3. `asan-if1.log`, `asan-if2.log` |
| Sanitizer instrumentation | Sixteen first-party firmware objects contain 169 sanitizer references per composition build; `sanitizer-instrumentation.json`. Host-model and dependency objects retain ordinary harness flags. |
| Original round-12 probes | 3/3 per count; `prior-probe-results.json` and both logs |
| Coverage ratchet | PASS, 22 files at 100% lines/branches after unchanged exclusions; adapter 515/515 lines and 478/478 branches, delivery 82/82 and 62/62. `coverage.log`, `coverage.rc` |
| Documentation and contract | Documentation/privacy, Python idiom, C/C++ idiom and generated mailbox checks all rc 0; `docs-results.json` and individual logs. Diff whitespace check also passes. |
| Actual bytes, modes and index | Parent 1,215 blobs; processor 562, gPTP 104, axis 214, lwSRP 60. All actual blob hashes/modes and complete stage-zero indexes match their commits; `integrity-final.json`. Final status including ignored files is empty. |

The [immutable author packet](https://github.com/kebag-logic/milan-fpga/tree/ef69cd574960ff0ed632630d82d41383e38b1acc/review-evidence/665f4-r1/author-r13) supplies source validation evidence. All 86 final command records report rc 0; all 85 retained logs match published sizes and hashes (`public-gates-audit.json`). The full campaign's complete raw log is not published. Its structured receipt records 471 control plants, 169 SRP plants at IF=2, 68 at IF=1 and both pin-refusal controls. Both SRP inventories match the standing driver exactly, including the three new plants (`public-source-campaign-audit.json`). This is an audit of that published full run, not a fresh execution of the complete campaign.

The final commit only wraps a Python line. Its parsed syntax tree equals parent `29b51b5d9b5f4f3a8349f2bed1e36ce48a94f7ad`; firmware, test-case bytes, definitions and build inputs are unchanged. Published source hashes match this head. This verifies the author's declared input equivalence for gates running across that formatting commit; the independent focused, sanitizer and coverage runs above execute this exact head. Two disclosed development attempts are superseded: unsupported coverage `--build-dir` was replaced by `--keep`, and the long Python line was wrapped.

**Earlier public findings retained or resolved**

The [R533-12](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6051926602) and [R532-12](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6051937140) verdicts at `efea74858dffc482820d4f19c26c38796a57ff75` are the baseline. Prior public finding sections were read after the independent pass. The delta changes only two test files and one pin citation, so earlier source fixes remain byte-identical. The table explicitly carries their dispositions; it does not claim rerunning every historical mutation or bank.

| Finding IDs | Disposition at this head and retained artifacts |
| --- | --- |
| R532-11-F1 | RESOLVED retained: no library reentry from the filter; `srp_mbx.c:159-190,424-433,572-585`, pinned callback contracts. |
| R532-11-F2 | RESOLVED retained: identical supersession, settled link resets and pre-withdrawal kind cases at `srp_feedback.hpp:239-295`; current composition/sanitizer suites pass. `p11-*` plants remain in both standing selections. |
| R533-10-F1; R532-10-F1 | RESOLVED retained: authorized kind-only entry at `acmp.h:420`, `acmp.c:1132`, `ctrl_app_srp.c:84`; both current wire-view cases pass. |
| R533-10-F2 | RESOLVED retained: latched withdrawal, single-PDU ordering, expiry/receive, isolation and retirement at `srp_mbx.c:562`, `ctrl_app_srp.c:78-98`; current temporal cases pass, now including Failed. |
| R532-10-F2/F3 | RESOLVED retained: pending-replacement and accumulated-refusal cases plus discovered-talker feedback measurements at `srp_feedback.hpp:298-343`. Current suite passes. |
| R532-9-F1/F2/F3 | RESOLVED retained: deferred registration delivery, invalid-VID parking and independent bound terms; `ctrl_app_srp.c:39-104`, `srp_binding.hpp`, `srp_app.cpp`; all relevant suites pass. |
| R533-8-F1 | RESOLVED retained: binding requests are owned and delivered by the composition, with retry and supersession; `ctrl_app_srp.c:36-133`, `srp_binding.hpp`. |
| R532-8-F1 | Source/test defect remains RESOLVED: owned extra-byte source-count fixture in `test_acmp.cpp:208-221` is unchanged. Its historical source evidence remains the baseline. Hosted firmware-unit/rtl-fast acceptance remains a manager duty, not cleared here. |
| R532-8-F2/F3/F4 | RESOLVED retained: real access measurements in `srp_app.cpp`, three-module attribution in `maap/README.md:134`, and narrowed plant claim in `ctrl/README.md:143`. |
| R533-1-F1; R532-1-F1 | RESOLVED retained: MSRP-only Milan immediate IN leave and original LV/#608 deadline in the unchanged pin; adapter and differential cases pass. Generic MVRP behavior remains. |
| R533-1-F2; R532-2-F1 | RESOLVED retained: current-level reconciliation, link restart and receive fencing at `srp_mbx.c:674-770`; lifecycle cases pass. |
| R533-1-F3; R533-2-F1; R532-2-F3/F4; R532-3-F1/F2 | RESOLVED retained: shared identity reconciliation, replacement inheritance, final-user VLAN withdrawal and Domain ownership at `srp_mbx.c:324-393,587-667`; adapter/shared-binding cases pass. |
| R532-1-F2 parts 1/2 | RESOLVED retained: admission-boundary and Ready/ReadyFailed cases remain in the passing adapter suite. |
| R532-1-F2 part 3; R533-2-F2 | RESOLVED retained from baseline: unchanged public lwSRP pin contains the note-4/5 cases and reversals. Full upstream suites were not rerun. |
| R532-2-F2 | RESOLVED retained in source: lwSRP licence, inventory, fetch instructions and diagram remain unchanged; local documentation check passes. Hosted acceptance stays separate. |
| R533-5-F1; R532-5-F1; R532-6-F1 | RESOLVED retained: whole-record recovery and original-arrival 1000 ms expiry at `srp_mbx.c:409-483,742-762`; seventeen receive-recovery cases pass under sanitizer at each count. |
| R533-1-F4; R532-6-F2 | RESOLVED retained from baseline: published linked composition/base-delta evidence and image fixture inputs are unchanged. No fresh linked image or routed measurement is claimed. |
| R533-6-F1 | RESOLVED retained: current public mailbox export recipe and NVM include paths retain the corrected form. No mailbox bank was rerun. |
| R532-1-R1/R2; R532-2-R1/R2; R532-3-R1; R532-5-R1/R2; R532-6-R1; R532-7-R1; R532-8-R1/R2; R533-6-R1; R533-7-R1; R533-8-R1 | Prior wording resolutions retained under the round-12 baseline: tick units, publication tense, retry completion/expiry, composition and checkout instructions remain corrected. R533-12-R1 is separately resolved above. |
| Optional suggestions through round 11 | Baseline addressed/optional dispositions retained. In particular R532-11-S1's CPU-work calibration text remains at `MAILBOX_SPLIT.md:735-739`; optional historical naming/upstream recommendations create no new obligation in this delta. R532-12-S1 is explicitly retained above. |

**Reviewer-owned source-head ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen issue decisions; REQUIREMENTS.md:24-52; FR_NFR.md:330-390; srp_feedback.hpp:87-137 against mailbox ingress, Milan immediate-leave and authorized retained-event contracts; six original probe passes | R533-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| RTL | CLEAN | receipts/delta.patch and integrity-final.json establish unchanged firmware/RTL/pins/registers; ctrl_app_srp.c:49-104 and srp_mbx.c:159-190,424-433,572-585 preserve serialized interfaces and callback boundaries | R533-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Robustness | CLEAN | srp_feedback.hpp:87-137 and existing reset/supersession/expiry cases; srp_rx_retry.cpp; fourteen sanitizer arms, 280 cases, IF=1/2; per-kind coexistence and both lost/false withdrawal paths | R533-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Tests | CLEAN | srp_mutants.py:802-814,857-890; test_ctrl_firmware.py:197-205; six named catches; 104 normal composition passes; original R12 probes; coverage.log and public-source-campaign-audit.json | R533-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Docs | CLEAN | MAILBOX_SPLIT.md:294-297 vs exact lwSRP gitlink; srp/README.md:70-82 and current PR Round 13 claims; docs-results.json; verified public source receipts and explicitly bounded execution claims | R533-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |

**Real limits and pending manager duties**

- This is a focused source review. Licensed IEEE/Milan editions were not freshly read in full; the public decisions, repository requirements and pinned interface authorities define the reviewed contracts. No protocol interpretation changed in this delta.
- Full parent, processor, gPTP, synthesis and builder banks, full historical mutations and fresh linked images were not run here. No HDL build was necessary because the delta contains no HDL; the scoped HDL executable was not invoked.
- Source validation is the author's published gate evidence plus the independent executions above. There was no manager source bank at this exact head. The older manager compiler-absent comment concerns `c1049de1` only and supplies no current-head bank evidence.
- Hosted state in `receipts/hosted-checks.json` is one exact-head snapshot: completed successes include changes, full-ci-gate, RTL lint, all four synthesis shards, behavior conformance, wire accountability and docs-check-no-git. Firmware-unit, docs-check, elaborate, synthesis elaboration and all five simulation shards were still running. Required aggregates were not yet all available. The physical job was skipped. No skipped or unfinished job is counted as executed acceptance.
- Physical calibration NOT RUN. Field skips, host service envelopes and linked-size fixtures provide no hardware, boot, audio-soak or target timing proof. Target scheduling, CPU work, stack depth, live stream configuration and fabric licence integration remain their documented obligations.
- The manager must validate the current-dev merge candidate at the merge turn, including builder and native banks, and link its receipts on the PR. Assigned source base and live dev were both `99e4eb6c14462aafa84bb1ac597fd241abc1a240`; recheck live dev before constructing that candidate. This source ledger does not replace candidate validation.
- The manager owns hosted and local-replica acceptance, the remaining hosted half of R532-8-F1, the complete independent review bar, explicit maintainer merge authorization, and post-merge containment. No review may remain in flight at merge. F4 remains partial issue #665 work; this verdict does not close that umbrella issue.

Portable replay commands are in `REPRODUCE.md`. All publishable receipts and scripts are listed in `MANIFEST.sha256`; `scratch/` is excluded. All foreground executions have completed. The checkout remains detached, clean, and byte/mode/index exact at the assigned head, with all four required submodules verified at their pins.

R533-13 FINISHED
