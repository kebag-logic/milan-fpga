[A560]

# F4 handoff

Relates to #665. Parent branch: `665-f4-srp`. Head: `42a0371affceb2a07a734449d706be01fa5abc9a`.
Executor: [A560]. Independent reviewers: [R532] and [R533].
Initial resume head: `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`.
Required dev merge: `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, merged with `--no-ff` in `8b43aed`.
Original FC base: `db9aa8c9b135b34ff3d070a979dee70440b37cc6`.

## Round 2

Status: STOP. The required builder contract function exceeded the 550-second foreground window in two complete attempts. It has no passing result. The other 99 functions completed; the existing optional resource-calibration arm lacked its external report. The remaining affected gates pass. The prior recorded contract run took 1046.52 seconds, so its old result is not substituted for current-head evidence.

The implementation addresses the accepted behavior findings. It enables Milan rapid Leave for MSRP only, preserves link lifecycle events, fences stale receive records, reconciles every accepted binding sharing a StreamID, and retries failed participant recreation safely. No RTL, register-map, default all-fabric configuration or shipping-image change is introduced by F4. The only merge was the expressly authorized dev integration. Nothing was pushed or published to a PR.

This packet supersedes the old D1 conclusion and obsolete rewritten upstream hashes in the historical round-1 packet.

| Review item | Disposition and evidence |
|---|---|
| R533-1-F1 / R532-1-F1 | `LWSRP_MILAN=1` selects MSRP rapid Leave. Both IN withdrawal cases fail when the opt-in is disabled. MVRP remains generic. The original LV deadline survives later Lv, including #608 and processor #134. |
| R533-1-F2 | LINK events recreate the affected participant even across adjacent down/up. Default Domain returns; the published RX prefix cannot re-register old reservations. The second interface and its owed TX remain independent. |
| R533-1-F3 | Reconcile one Listener per interface/StreamID from every eligible binding. Different destinations and VIDs are accepted; an ineligible binding contributes nothing. Both binding orders and final withdrawal are checked on wire. |
| R533-1-F4 / R532 R2 | Linked composition measured for both entity shapes and IF=1/2, against both the merged dev base and original FC base. The table below separates static RAM from routed resource use. |
| R532-1-F2 | Boundary rates 22,698,666 and 22,698,667 bps discriminate the 75% ceiling, 22-byte tagged Ethernet overhead and 20-byte preamble/IFG. A strict mock forbids a Ready-to-ReadyFailed licence glitch. Upstream note 4/5 tests and reversals are on the local topic branch. |
| R532 S1 | The assigned integrated pin already includes per-type/per-port LeaveAll regression coverage. The upstream reversal gate passes. |
| R532 S2 | Leave the optional generic LV/rJoinIn callback change for upstream disposition. This adapter derives registrations from retained attributes; duplicate Join indications do not change its value-based Domain/Listener behavior. The manager must carry this note to dependency PR #12; public posting here is restricted to #665. |
| R532 S3 | A failed recreation owns neither participant. It counts refusal, retries, and continues servicing a surviving interface. Allocation-failure tests and two independent retry/starvation plants check this. |
| R532 R1 | Documentation now says TICK carries centiseconds; NOW_MS is the separate millisecond timestamp. |

The public assignments are issue #665 comments 6030279477 and 6033558691. The acceptance addition is 6030870481. Review reports are R532-1 and R533-1 under `review-evidence/665f4-r1/reviews/` on `665f4-review-evidence`.

## Changes with file locations

| File:line | Change |
|---|---|
| `.github/workflows/rtl-fast.yml:239` | Require SRP dependency, firmware mutation checks, the pinned compiler and failure propagation. |
| `.gitmodules:13` | Add the lwSRP remote; gitlink is the assigned integrated port. |
| `docs/testing/CI_WORKFLOWS.md:2299` | Document required dependency and firmware validation. |
| `scripts/ci_events.py:2344` | Pin the merged workflow; update the compiler-refusal control to the merged step name. |
| `sw/firmware/ctrl/README.md:10` | Describe SRP, the current dependency and freestanding build. |
| `sw/firmware/ctrl/loop/ctrl_loop.c:28` | Consult optional RX readiness before every record. |
| `sw/firmware/ctrl/loop/ctrl_loop.h:100` | Expose optional per-channel receive readiness. |
| `sw/firmware/ctrl/mbx/mbx.c:165` | Snapshot RX_HEAD and compare the consumed cursor across 16-bit wrap. |
| `sw/firmware/ctrl/mbx/mbx.h:91` | Specify the bounded RX-prefix fence API; no register change. |
| `sw/firmware/ctrl/port/shlan_port.h:19` | Specify asynchronous port callback discipline. |
| `sw/firmware/ctrl/srp/README.md:1` | Document Milan rapid Leave, lifecycle fencing, shared declarations, size fixture and remaining integration. |
| `sw/firmware/ctrl/srp/srp_entity.py:1` | Derive source, sink and static pool dimensions from the generated entity. |
| `sw/firmware/ctrl/srp/srp_mbx.c:1` | Provide per-interface MRP, 75% admission, ordered output, shared declarations, link lifecycle and atomic recreation. |
| `sw/firmware/ctrl/srp/srp_mbx.h:1` | Expose static state, configuration and binding port; retain link/fence state per interface. |
| `sw/firmware/ctrl/test/ctrl_arms.py:10` | Verify the exact lwSRP pin and compiled bytes. |
| `sw/firmware/ctrl/test/ctrl_image.c:1` | Compose reachable ADP, SRP, mailbox and loop with static storage for linked size measurement. |
| `sw/firmware/ctrl/test/ctrl_image.ld:1` | Separate text, read-only data, data, BSS and an explicit 8192-byte stack reservation. |
| `sw/firmware/ctrl/test/ctrl_image.py:1` | Link and inspect a closed RV32I/ILP32 image; report section, storage and artifact hashes. |
| `sw/firmware/ctrl/test/ctrl_image_runtime.py:1` | Rebuild bare-metal memory primitives and integer helpers; record source/header provenance. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:453` | Preserve all 100 merged controls and exact dependency refusal checks. |
| `sw/firmware/ctrl/test/ctrl_reuse.py:33` | Verify the submodule root before pinned processor reads. |
| `sw/firmware/ctrl/test/srp_arms.py:1` | Build with the MSRP-only Milan opt-in and a host-only allocation-failure port. |
| `sw/firmware/ctrl/test/srp_debug.cpp:1` | Assert on synchronous binding, receive and tick callbacks. |
| `sw/firmware/ctrl/test/srp_fixture.hpp:1` | Use actual mailbox/loop/pool paths, strict licence expectations and independent wire decoding. |
| `sw/firmware/ctrl/test/srp_latency.cpp:1` | Measure four paths against original origins and the conditional 10 ms service envelope. |
| `sw/firmware/ctrl/test/srp_latency_policy.hpp:1` | Keep the single service-budget predicate independently mutable. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:1` | Exercise 41 adapter cases for both interface counts, including every round-2 behavior fix. |
| `sw/firmware/ctrl/test/srp_mutants.py:1` | Require 58 named compiled defects to fail their intended observations. |
| `sw/firmware/ctrl/test/srp_reuse.py:1` | Verify processor blobs before extracting stimuli and Applicant rows. |
| `sw/firmware/ctrl/test/srp_shape.cpp:1` | Check all generated outputs/sinks against independent entity constants. |
| `sw/firmware/ctrl/test/srp_walk.cpp:1` | Compare selected processor wire rows; D1 now agrees with Milan rapid Leave. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:4` | Run all SRP arms and cap jobs at four; remove the duplicate merged option. |
| `sw/firmware/gtest/coverage.ratchet:8` | Regenerate the 100% per-file ratchet through its generator. |
| `third_party/lwSRP:1` | Pin 23d9a8173b07503a0ee6e8528f922fceab4e67f0, as assigned. |

## Tests and planted defects

[ROUND2-TESTS.md](ROUND2-TESTS.md) maps every adapter, debug, timing, shape and differential case to its named planted defect and required observable. There are 41 adapter cases at each interface count and 58 SRP plants. The merged control suite contains 100 controls; two additional controls reject an edited or moved dependency.

| Case | Planted defect | Required failed observable |
|---|---|---|
| `StartupDeclaresTalkersDomainAndVlan` | `startup-vid` | `d.value` |
| `LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline` | `short-leave` | `Unexpected mock function call` |
| `RegisteredListenerSubtypeChangeRevokesPermission` | `asking-is-ready` | `adapter.ifs[0].active[0]` |
| `InterfaceStateDoesNotCross` | `ignore-link` | `adapter.ifs[i].active[0]` |
| `SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer` | `failed-listener-ready` | `declared` |
| `DomainUsesPeerPriorityAndVlan` | `ignore-peer-domain` | `domain.priority` |
| `RefusedMailboxRetainsOwedFrameAndDefersInput` | `rx-overtakes-owed` | `adapter.received` |
| `ExpiryBacklogPrecedesSamePassReceive` | `rx-overtakes-expiry` | `adapter.stops` |
| `ReentryFromOutputIsRefusedAndCounted` | `reentry-uncounted` | `adapter.reentries` |
| `InvalidBindingsAndDuplicateBindingsPreserveState` | `invalid-vid` | `srp_mbx_bind` |
| `ExhaustionDuringEachStartupStageReleasesEveryBlock` | `failed-init-leaks` | `ctrl_pool_in_use` |
| `MissingBootDependenciesRefuseBeforeAttachment` | `missing-port-accepted` | `srp_mbx_init` |
| `AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | `attach-nonatomic` | `srp_mbx_attach` |
| `InvalidFramesHaveNoReservationSideEffects` | `malformed-uncounted` | `adapter.malformed` |
| `RecreateAllocationFailureIsCountedAndRetried` | `reset-skips-recreate` | `adapter.ifs[0].msrp` |
| `ReadyFailedAndUninterestingStreamsAreSeparated` | `readyfailed-ignored` | `Actual function call count` |
| `DomainFilterAndDuplicateDoNotGrowDeclarations` | `foreign-domain-stored` | `ctrl_pool_in_use` |
| `MvrpAcceptsOnlyCurrentDomainVid` | `foreign-vlan-stored` | `ctrl_pool_in_use` |
| `WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt` | `sink-da-ignored` | `declared` |
| `AdmissionUsesBandwidthAndEthernetMinimum` | `admission-ceiling-ignored` | `admitted[0]` |
| `DomainExhaustionPreservesOldDeclarationUntilRetry` | `domain-refusal-lost` | `domain.vid` |
| `SinkDeclarationExhaustionRetriesWithoutLosingBinding` | `listener-refusal-lost` | `declared` |
| `LinkLossCancelsItsOwedFrameOnly` | `other-link-cancels-owed` | `adapter.owed_len` |
| `OneLoopOwnsTheGlobalCentisecondDispatch` | `duplicate-tick-owner` | `srp_mbx_attach` |
| `SynchronousBindingFromOutputAsserts` | `binding-debug-guard` | `failed to die` |
| `SynchronousReceiveFromOutputAsserts` | `receive-debug-guard` | `failed to die` |
| `SynchronousTickFromOutputAsserts` | `tick-debug-guard` | `failed to die` |
| `ListenerBeforeVlanCommitCannotStartTalker` | `licence-before-vlan` | `joined` |
| `SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind` | `unbind-shared-listener` | `d.event` |
| `BoundOldDomainVlanSurvivesDomainChange` | `withdraw-bound-domain` | `d.event` |
| `PriorityOnlyDomainChangeKeepsVlanMembership` | `withdraw-same-domain` | `d.event` |
| `SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent` | `sink-vlan-refusal-lost` | `vlan_requested` |
| `SinkMembershipCommitsBeforeReadyAtStartup` | `ready-before-vlan` | `joined` |
| `SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget` | `latency-missing-startup` | `commits.size()` |
| `SrpLatency.ReceiveStateMalformedDomainAndListenerPaths` | `latency-domain-unserviced` | `domain.vid` |
| `SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog` | `latency-leave-origin` | `Unexpected mock function call` |
| `SrpLatency.FullRingRetainsOriginalOriginAndElevenMillisecondStallFails` | `latency-relaxed-budget` | `service_limit` |
| `SrpWalk.CertifiedTwoClassDomainVectorAdoptsOnlyClassA` | `walk-domain-ignored` | `domain.vid` |
| `SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal` | `walk-match-da-ignored` | `declared` |
| `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` | `walk-leave-shortened` | `Unexpected mock function call` |
| `SrpWalk.ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire` | `walk-startup-is-join` | `d.event` |
| `SrpWalk.PerInterfaceWireIdentityAndUnknownOrTruncatedInput` | `walk-malformed-uncounted` | `adapter.malformed` |
| `EveryGeneratedOutputIsDeclaredAndEverySinkFits` | `shape-last-output-missing` | `outputs` |
| `AdmissionStraddlesTheExactEthernetCeiling` | `tag-overhead-omitted` | `admitted[0]` |
| `AdmissionStraddlesTheExactEthernetCeiling` | `preamble-ifg-omitted` | `admitted[0]` |
| `AdmissionStraddlesTheExactEthernetCeiling` | `ninety-percent-ceiling` | `admitted[0]` |
| `ReadyToReadyFailedNeverGlitchesAnActiveLicence` | `readyfailed-callback-stop` | `mock function call` |
| `AdjacentLinkEdgesResetDomainAndAllPriorRegistrations` | `short-link-interruption-ignored` | `domain.priority` |
| `LinkEventsDiscardOnlyTheirPublishedReceivePrefix` | `old-prefix-accepted` | `mock function call` |
| `SharedIdentityReconcilesBothBindingOrdersOnTheWire` | `shared-identity-overwritten` | `last` |
| `EventReentryAndSinkCapacityAreGuarded` | `event-reentry-unguarded` | `adapter.reentries` |
| `RecreateAllocationFailureIsCountedAndRetried` | `failed-interface-starves-peer` | `other_sent` |
| `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `backlogged-old-prefix-accepted` | `mock function call` |
| `LinkLevelLossAndFirstDownEventAreFailClosed` | `link-level-loss-ignored` | `adapter.ifs[0].active[0]` |
| `ExhaustedPoolStillReusesOwnedBlocksOnLinkReset` | `reset-leaks-owned-participants` | `adapter.refused` |
| `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `downlink-receive-accepted` | `adapter.ifs[i].registered[0]` |
| `InListenerWithdrawalRevokesLicenceImmediately` | `delayed-in-listener` | `adapter.ifs[i].active[0]` |
| `InTalkerWithdrawalImmediatelyWithdrawsListener` | `delayed-in-talker` | `declared` |

The link-backlog case spans more records than one service pass. Reset discards only the affected interface's published prefix. This is conservative: frames arriving after physical recovery but before lifecycle service can also be discarded. Fresh declarations after the fence are required. The cursor comparison is bounded by the mailbox capacity and checked every service pass.

The expanded shared-binding case tests same and different VIDs in both binding orders. It starts a new bounded wire-capture window between cases without resetting protocol state. The recreation fault fixture does not expect quiescence while retry is intentionally failing; it executes bounded service passes and verifies peer-interface output.

The reset retry mutant was re-graded to suppress retry while preserving the null guard; a crash is not a named observable. The VLAN-ordering mutant now removes eligibility in the shared reconciliation step. The owed-interface mutant follows the reset helper's interface index. None changes a test expectation to accept the original defects. The merged CI compiler control now names the merged workflow step; it retains the compiler-required refusal. The duplicate jobs option and executable mode conflict were corrected.

D1 is resolved: firmware and the processor both withdraw an IN MSRP registration immediately under Milan v1.2 4.2.7.2.2. A later withdrawal in LV retains the original five-second deadline. D2 remains: Listener Lv retains its declaration subtype; FourPackedEvent Ignore is not a Listener declaration under IEEE 802.1Q-2018 35.2.2.7.2.

The timing desk envelope retains one aggregate 1 ms CPU/preemption allowance, 100 ns per mailbox access and 100 ns uncertainty within the single 10 ms budget. It subtracts only the applicable normative Join wait. An 11 ms full-ring stall fails from the original origin. This is conditional host evidence, not target scheduling or wire-departure measurement.

## Coverage

After the existing documented exclusions, with no exclusion added:

| File | Lines | Branches |
|---|---:|---:|
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 14/14 | 8/8 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx.c` | 177/177 | 68/68 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 424/424 | 406/406 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

## Linked composition size

All values are bytes. Each image includes an 8192-byte reserved stack. Span includes linker alignment. The static arena is already in BSS; do not add it again. Initialized data is zero. The fixture has no board reset/loader or connected fabric licence port. It retains the binding entry and exercises reachable control/ADP/SRP/mailbox code with static licence observations. It is not a shipping image or routed utilization measurement.

| Entity | IF | Text | Read-only data | Data | BSS | Arena, in BSS | Span | Dev-base span | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 27376 | 2846 | 0 | 15432 | 9920 | 53856 | 19200 | 34656 |
| 1x1_tdm8 | 2 | 28352 | 2846 | 0 | 25708 | 19840 | 65104 | 19696 | 45408 |
| 8x8 | 1 | 27360 | 2846 | 0 | 30184 | 24032 | 68592 | 19200 | 49392 |
| 8x8 | 2 | 28308 | 2846 | 0 | 55212 | 48064 | 94576 | 19696 | 74880 |

The original FC base spans 18,752 bytes at IF=1 and 19,248 bytes at IF=2 for either entity shape. The merged dev base adds 448 bytes. Both comparisons use the same fixture, compiler, flags and rebuilt runtime. The base is ADP/control-only with the original 1024-byte reference arena. The F4 arena is generated from the entity dimensions. Compiler frame reports remain separate; the 8192-byte reservation is not a proven whole call-chain bound.

[ROUND2-SIZE.json](ROUND2-SIZE.json) contains section, symbol, archive, map and ELF size/hash evidence. [ROUND2-RUNTIME.json](ROUND2-RUNTIME.json) identifies every compiled runtime source and included header, plus exact commands with neutral path parameters. Only RV32I/ILP32 code is accepted, including runtime objects and the linked image. The link has no unresolved or heap symbols. Build products stay in disk scratch.

## Upstream dependency

The parent builds the assigned integrated `mark2-port` commit `23d9a8173b07503a0ee6e8528f922fceab4e67f0`. The manager moves the pin to dependency PR #12's reviewed head in a later delta.

The separate local clone has branch `f4-applicant-notes` at `495520f5e02dd077fc9b1451942b25ec95afa1b8`, with commits `06fd20b0603337024ba98b888dd272be1ec43e2b` and `495520f5e02dd077fc9b1451942b25ec95afa1b8`. These change tests and the measured README count; compiled library sources remain identical to the parent pin. No upstream push occurred.

The default profile passes 46 tests and 2675 assertions; Milan enabled passes 46 tests and 2663 assertions. Behavior coverage is three scenarios and ten steps. All 40 source reversals are detected, including the original LV deadline, MSRP-only rapid Leave and the note 4/5 guards. Sentence, reference, reference self-test and authenticated link checks pass. Graph sources were unchanged.

## Gates and remaining work

Commands ran in foreground windows with disk scratch and bounded workers. Logs stay in the assigned scratch directory; the artifact table records hashes and sizes. No package, toolchain or build export is copied into this packet.

| Command | rc | Result | Evidence |
|---|---:|---|---|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware-final"` | 0 | Host, debug, shape, wire differential and RV32 arms; 100 control plants, 54 SRP plants and two dependency controls. | `firmware-selftest.log` |
| `srp_mutants.campaign($SCRATCH/srp-mutants-final, $LWSRP, 4)` | 0 | Final 57-plant campaign; every named observable fails. | `srp-head.log` |
| `srp_mutants.campaign with only downlink-receive-accepted selected` | 0 | Final added plant caught, for 58 SRP plants total; exact code below. | `downlink-control.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep "$SCRATCH/coverage-final-2"` | 0 | Regenerated 15-file ratchet; no exclusion added. | `coverage-write-final.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-closed"` | 0 | Current source and tests: 100% in all 15 files after existing exclusions. | `coverage-closed.log` |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 17 shared runtime and header controls. | `docs-53.log` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 435 tests across five shapes; RV32 builds required. | `nvm-final.log` |
| `make -C "$SCRATCH/mailbox-gate/tb/verilator/mbx" -j1` | 0 | Both bus adapters, co-simulation, IF=2 and five required mutations. | `mailbox-final.log` |
| `make -C "$SCRATCH/processor-gates/tb/srp_stream_fsms" -j1` | 0 | 1219 checks, including shape walks. | `processor-fsms.log` |
| `make -C "$SCRATCH/processor-gates/tb/srp_top" -j1` | 0 | 2200 checks, including storage shapes. | `processor-top.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | 1741 contract items, 2362 arms. | `ci-events-final.log` |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | Generated contract is current. | `docs-28.log` |
| `Original builder main-list functions, foreground batches` | 0 for 99 functions | One function remains incomplete; optional gate 11 calibration is NOT RUN. | `builder-4.log` |
| `timeout 550s python3 builder_bank.py, contract function` | 124 twice | Mandatory contract function incomplete. This is the STOP reason. | `builder-2.log; builder-3.log` |
| `ctrl_image_runtime.py, then ctrl_image.py for each shape/interface/base` | 0 | Four F4 images and eight base comparisons, closed RV32I/ILP32 link. | `image-results-final.json` |
| `cmake configure/build; ctest; unit_tests; behave` | 0 | Both profiles; 46 unit cases, 2675 default / 2663 Milan assertions; 3 scenarios / 10 steps. | `lwsrp-reversals.log` |
| `python3 tests/check_reversals.py --work-dir "$SCRATCH/lwsrp-reversals" --prefix "$CGREEN"` | 0 | All 40 compiled upstream reversals detected and restored source green. | `lwsrp-reversals.log` |

[ROUND2-GATES.md](ROUND2-GATES.md) is the command/result table and artifact manifest. The builder contract timeout prevents a REVIEW READY claim. Final coverage passes at 424/424 adapter lines and 406/406 adapter branches; all 58 SRP plants are caught across the final campaign and its last delta. There is no positive review verdict, merge approval, hosted-gate claim or release claim in this packet.

The application still owes the ACMP caller, live stream/MAAP allocation inputs and the existing fabric licence output. F3 is absent from the assigned integrated base. Target timing, two independent reviews, candidate-merge validation, protected hosted contexts and post-merge containment remain integration obligations. No hardware or bench access occurred.
