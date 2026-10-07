[A560]

# F4 handoff

Relates to #665. Branch: `665-f4-srp`. Head: `c1049de1970e93d2c36ace62891ee9d947cd3191`.
Status: STOP. The required full docs-check set is incomplete because its compiler-absent entry exceeded two 540-second foreground windows, including an isolated retry. Executor [A560]; reviewers [R532] and [R533]. This is an implementation/evidence handoff, not a review verdict or merge approval.

## Round 3

One additive commit follows `42a0371affceb2a07a734449d706be01fa5abc9a`: `fix: reconcile SRP link levels and shared binding replacements`. No push, PR update, merge, rebase or amend occurred in this round. The lwSRP gitlink remains `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.

The exact assignment is issue #665 comment 6035166787. R532-2 and R533-2 are under `review-evidence/665f4-r1/reviews/` on `665f4-review-evidence`. Their findings are addressed as follows; independent re-review owns closure and the lens ledger.

| Accepted item | Implemented outcome and verification |
|---|---|
| R532-2-F1 | Attach reads the current link level. Poll reconciles both directions, resets the affected participant and fences prior RX. Reattach and cancelled-record cases run at IF=1/2; both new defects are caught. |
| R532-2-F2 | Inventory, licence, fetch guidance, role, generated node/edge/raster and checker are current; all four previously failing submodule commands pass. The full docs-check claim remains unmet: its compiler-absent entry timed out twice. The separate builder bank remains delegated by the assignment. |
| R533-2-F1 | Shared Applicant state survives replacement of either slot and multiple replacements before polling. The resulting whole binding set decides withdrawals. Destination/VID changes, eligibility combinations, continued Ready, final withdrawal and absence of stale renewal are tested. Both new rebind controls are caught. |
| R532-2-F3 | The final binding releases its non-Domain VID even when it never requested membership. Both unbind orders and every interface pass; the old per-binding request guard is caught. |
| R532-2-F4 | `reset-keeps-owed-domain`, `reset-keeps-sink-vlan` and `shared-ready-uses-first-vlan` each fail their named new case and observable. |
| R533-2-F2 | Published topic `495520f5e02dd077fc9b1451942b25ec95afa1b8` is cited with the two tests and three guard reversals. Positive suites and all 40 reversals pass. Production sources are byte-identical to the unchanged parent pin. |
| R532-2-R1/R2 | Dependency publication wording is corrected. PR-BODY.md describes current evidence and the delegated builder bank. Its STOP now names the newly attempted, incomplete compiler-absent docs entry, not the superseded round-2 builder result. |
| R532-2-S1 | Added a composition test proving generic MVRP enters LV on Leave and expires at the original 5000 ms deadline. Applying Milan rapid Leave to MVRP is caught. |

## Changes with file locations

| File:line | Round 3 change |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c:270` | Evaluate ownership over the complete replacement binding set; withdraw the last non-Domain VID independent of a binding's request history. |
| `sw/firmware/ctrl/srp/srp_mbx.c:305` | Preserve shared declaration and committed VID state across replacements, including consecutive binds before reconciliation. |
| `sw/firmware/ctrl/srp/srp_mbx.c:599` | Recover from both observed link-level transitions with reset and stale-RX fencing. |
| `sw/firmware/ctrl/srp/srp_mbx.c:684` | Read current per-interface levels when attaching. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:681` | Nine new cases cover level recovery, rebind combinations, final VID ownership, three lifecycle gaps and MSRP-only rapid Leave. |
| `sw/firmware/ctrl/test/srp_mutants.py:321` | Keep prior controls planted at the renamed ownership helper. |
| `sw/firmware/ctrl/test/srp_mutants.py:479` | Add nine named controls with assertion-specific catches; compilation errors never count. |
| `sw/firmware/gtest/coverage.ratchet:15` | Regenerate the SRP row to 441/441 lines and 410/410 branches. |
| `sw/firmware/ctrl/README.md:138` | Correct the published dependency status and fetch-access requirement. |
| `sw/firmware/ctrl/srp/README.md:49` | State attach/current-level recovery and shared replacement/final-VID behavior. |
| `sw/firmware/ctrl/srp/README.md:166` | Link the published upstream follow-up and name its tests and reversals. |
| `THIRD_PARTY.md:20` | Inventory the dependency's Apache-2.0 licence, LICENSE and NOTICE. |
| `docs/reference/SUBMODULES.md:26` | Record the unchanged full gitlink, ownership, fetch command and donor/root gates. |
| `docs/diagrams/submodule_boundaries.gen.py:94` | Add the fifth dependency role, layout and C-port connection. |
| `scripts/check_submodule_docs.py:30` | Require that connection in the generated map. |
| `docs/diagrams/submodule_boundaries.drawio:1`, `docs/diagrams/submodule_boundaries.svg:1`, `docs/diagrams/PNG_MANIFEST.json:10` | Regenerate editable/vector/raster artifacts and manifest solely through the generator; PNG size/hash is recorded, not copied into this packet. |

The inherited F4 implementation and round-2 changes remain in the branch. This round changes no RTL, register map, default all-fabric configuration or shipping image. F3 is absent from the assigned base; ACMP application composition remains owed.

## Tests and planted defects

The final complete run catches all 67 SRP controls below, all 100 inherited control-suite plants and both dependency checks. Adapter positives execute 50 cases at IF=1 and IF=2. The new matrix covers either replaced slot, destination versus VID changes, whether another eligible request remains, overlapping replacements, both unbind orders and interface isolation. The lifecycle checks include backlogs spanning multiple service passes and fresh registration after the fence.

| Test artifact | Planted defect | Required failed observable |
|---|---|---|
| `sw/firmware/ctrl/test/srp_mbx.cpp:16`: `StartupDeclaresTalkersDomainAndVlan` | `startup-vid` | `d.value` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:51`: `LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline` | `short-leave` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:68`: `RegisteredListenerSubtypeChangeRevokesPermission` | `asking-is-ready` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:74`: `InterfaceStateDoesNotCross` | `ignore-link` | `adapter.ifs[i].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:89`: `SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer` | `failed-listener-ready` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:120`: `DomainUsesPeerPriorityAndVlan` | `ignore-peer-domain` | `domain.priority` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:132`: `RefusedMailboxRetainsOwedFrameAndDefersInput` | `rx-overtakes-owed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:154`: `ExpiryBacklogPrecedesSamePassReceive` | `rx-overtakes-expiry` | `adapter.stops` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:168`: `ReentryFromOutputIsRefusedAndCounted` | `reentry-uncounted` | `adapter.reentries` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:190`: `InvalidBindingsAndDuplicateBindingsPreserveState` | `invalid-vid` | `srp_mbx_bind` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:207`: `ExhaustionDuringEachStartupStageReleasesEveryBlock` | `failed-init-leaks` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:222`: `MissingBootDependenciesRefuseBeforeAttachment` | `missing-port-accepted` | `srp_mbx_init` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:230`: `AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | `attach-nonatomic` | `srp_mbx_attach` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:249`: `InvalidFramesHaveNoReservationSideEffects` | `malformed-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:612`: `RecreateAllocationFailureIsCountedAndRetried` | `reset-skips-recreate` | `adapter.ifs[0].msrp` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:273`: `ReadyFailedAndUninterestingStreamsAreSeparated` | `readyfailed-ignored` | `Actual function call count` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:282`: `DomainFilterAndDuplicateDoNotGrowDeclarations` | `foreign-domain-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:290`: `MvrpAcceptsOnlyCurrentDomainVid` | `foreign-vlan-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:308`: `WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt` | `sink-da-ignored` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:325`: `AdmissionUsesBandwidthAndEthernetMinimum` | `admission-ceiling-ignored` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:333`: `DomainExhaustionPreservesOldDeclarationUntilRetry` | `domain-refusal-lost` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:346`: `SinkDeclarationExhaustionRetriesWithoutLosingBinding` | `listener-refusal-lost` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:362`: `LinkLossCancelsItsOwedFrameOnly` | `other-link-cancels-owed` | `adapter.owed_len` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:381`: `OneLoopOwnsTheGlobalCentisecondDispatch` | `duplicate-tick-owner` | `srp_mbx_attach` |
| `sw/firmware/ctrl/test/srp_debug.cpp:6`: `SynchronousBindingFromOutputAsserts` | `binding-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_debug.cpp:18`: `SynchronousReceiveFromOutputAsserts` | `receive-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_debug.cpp:31`: `SynchronousTickFromOutputAsserts` | `tick-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:394`: `ListenerBeforeVlanCommitCannotStartTalker` | `licence-before-vlan` | `joined` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:408`: `SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind` | `unbind-shared-listener` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:432`: `BoundOldDomainVlanSurvivesDomainChange` | `withdraw-bound-domain` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:441`: `PriorityOnlyDomainChangeKeepsVlanMembership` | `withdraw-same-domain` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:449`: `SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent` | `sink-vlan-refusal-lost` | `vlan_requested` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:479`: `SinkMembershipCommitsBeforeReadyAtStartup` | `ready-before-vlan` | `joined` |
| `sw/firmware/ctrl/test/srp_latency.cpp:40`: `SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget` | `latency-missing-startup` | `commits.size()` |
| `sw/firmware/ctrl/test/srp_latency.cpp:92`: `SrpLatency.ReceiveStateMalformedDomainAndListenerPaths` | `latency-domain-unserviced` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_latency.cpp:119`: `SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog` | `latency-leave-origin` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_latency.cpp:130`: `SrpLatency.FullRingRetainsOriginalOriginAndElevenMillisecondStallFails` | `latency-relaxed-budget` | `service_limit` |
| `sw/firmware/ctrl/test/srp_walk.cpp:19`: `SrpWalk.CertifiedTwoClassDomainVectorAdoptsOnlyClassA` | `walk-domain-ignored` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_walk.cpp:31`: `SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal` | `walk-match-da-ignored` | `declared` |
| `sw/firmware/ctrl/test/srp_walk.cpp:51`: `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` | `walk-leave-shortened` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_walk.cpp:66`: `SrpWalk.ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire` | `walk-startup-is-join` | `d.event` |
| `sw/firmware/ctrl/test/srp_walk.cpp:96`: `SrpWalk.PerInterfaceWireIdentityAndUnknownOrTruncatedInput` | `walk-malformed-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_shape.cpp:6`: `EveryGeneratedOutputIsDeclaredAndEverySinkFits` | `shape-last-output-missing` | `outputs` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:539`: `AdmissionStraddlesTheExactEthernetCeiling` | `tag-overhead-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:539`: `AdmissionStraddlesTheExactEthernetCeiling` | `preamble-ifg-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:539`: `AdmissionStraddlesTheExactEthernetCeiling` | `ninety-percent-ceiling` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:529`: `ReadyToReadyFailedNeverGlitchesAnActiveLicence` | `readyfailed-callback-stop` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:548`: `AdjacentLinkEdgesResetDomainAndAllPriorRegistrations` | `short-link-interruption-ignored` | `domain.priority` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:638`: `LinkEventsDiscardOnlyTheirPublishedReceivePrefix` | `old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:579`: `SharedIdentityReconcilesBothBindingOrdersOnTheWire` | `shared-identity-overwritten` | `last` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:663`: `EventReentryAndSinkCapacityAreGuarded` | `event-reentry-unguarded` | `adapter.reentries` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:612`: `RecreateAllocationFailureIsCountedAndRetried` | `failed-interface-starves-peer` | `other_sent` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:563`: `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `backlogged-old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:650`: `LinkLevelLossAndFirstDownEventAreFailClosed` | `link-level-loss-ignored` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:260`: `ExhaustedPoolStillReusesOwnedBlocksOnLinkReset` | `reset-leaks-owned-participants` | `adapter.refused` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:563`: `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `downlink-receive-accepted` | `adapter.ifs[i].registered[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:496`: `InListenerWithdrawalRevokesLicenceImmediately` | `delayed-in-listener` | `adapter.ifs[i].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:506`: `InTalkerWithdrawalImmediatelyWithdrawsListener` | `delayed-in-talker` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:681`: `ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` | `attach-ignores-current-link` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:708`: `CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` | `cancelled-link-never-recovers` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:737`: `SharedRebindKeepsOnlyTheRemainingEligibleRequest` | `rebind-loses-shared-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:775`: `ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation` | `consecutive-rebind-loses-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:819`: `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` | `last-ineligible-vid-leaks` | `vlan_left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:849`: `RefusedPeerDomainDoesNotSurviveLinkRestart` | `reset-keeps-owed-domain` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:862`: `SinkVlanRedeclaredBeforeReadyAfterLinkRestart` | `reset-keeps-sink-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:886`: `SharedReadyWaitsForTheMatchingBindingsOwnVlan` | `shared-ready-uses-first-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:909`: `MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` | `milan-rapid-leave-leaks-to-mvrp` | `registered()` |

Supplemental published probes are retained in `round3-receipts/reviewer-probes.log`. The unchanged R533 wire-rebind and MVRP probes, R532 P1/P2/P4/P5 and all four gap probes pass at both interface counts. R532 P3 stops on its old internal `vlan_requested == false` setup assumption after the new bind logic copies already-requested VID state. The assigned P3-or-equivalent requirement is checked by `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder`: it preserves the never-requested setup assertion, checks both wire withdrawals and kills the old guard. No published probe was edited and no wire expectation was relaxed. The full supplemental result is 20 passing cases and two setup failures, not an all-green gate.

## Coverage

The ratchet was regenerated only through `fw_coverage.py --write`, then checked with the final production and test sources. All 15 files are at 100% after the existing exclusions; no exclusion changed.

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
| `sw/firmware/ctrl/srp/srp_mbx.c` | 441/441 | 410/410 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

## Linked composition size

All values are bytes. Initialized data is zero. BSS already includes the static arena; it must not be added twice. Every span includes linker alignment and an 8192-byte stack reservation. The reservation is not a whole-call-chain proof. These are reachable control/ADP/SRP/mailbox size fixtures, not booted shipping images or routed resource measurements.

| Shape | IF | Text | Read-only data | Data | BSS | Arena within BSS | Span | Dev span | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 27480 | 2846 | 0 | 15432 | 9920 | 53968 | 19200 | 34768 |
| 1x1_tdm8 | 2 | 28456 | 2846 | 0 | 25708 | 19840 | 65216 | 19696 | 45520 |
| 8x8 | 1 | 27420 | 2846 | 0 | 30184 | 24032 | 68656 | 19200 | 49456 |
| 8x8 | 2 | 28400 | 2846 | 0 | 55212 | 48064 | 94656 | 19696 | 74960 |

The original FC spans are 18,752 bytes at IF=1 and 19,248 at IF=2. Round-2 spans were 53,856 / 65,104 / 68,592 / 94,576. This round adds 112 / 112 / 64 / 80 bytes respectively; static storage is unchanged. [ROUND3-SIZE.json](ROUND3-SIZE.json) records current artifacts. The baseline measurements and complete runtime provenance remain in ROUND2-SIZE.json and ROUND2-RUNTIME.json. Every one of the 60 recorded runtime entries was rehashed without mismatch before relinking.

## Gates

| Gate | rc | Result |
|---|---:|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | 0 | 50 adapter, 3 debug, 4 latency and 5 selected wire-differential cases at each IF count; five entity shapes at IF=1/2; RV32 checks; 100 control plants, 67 SRP plants and two dependency controls. |
| `fw_coverage.py --check --jobs 4` | 0 | 100% lines and branches in all 15 measured files after unchanged exclusions. |
| `fw_coverage.py --selftest` | 0 | 28/28 coverage-grading controls. |
| `fw_rv32_selftest.py --require-rv32` | 0 | 17 ABI, freestanding, runtime-closure and refusal controls. |
| `tally_selftest.py --mutants` | 0 | Positive/failing/crashing fixtures and 18/18 tally defects caught. |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 435 tests across five shapes and required target builds. |
| `make -C tb/verilator/mbx -j2` in the verified disk copy | 0 | WB 316, AXI-Lite 361, co-simulation 13; IF=2 WB 316, AXI-Lite 361, model 316; 5/5 plants. |
| `gen_mailbox.py --check` | 0 | Generated contract unchanged and current. |
| Local docs-check checks, excluding the delegated builder bank and incomplete compiler-absent entry | 0 | 76 host commands plus isolated offline runner self-test; all on the recorded committed head. |
| `test_firmware_compiler.py --absent --audit ...` | 124 twice | Full docs-check is incomplete: both foreground runs reached 540 seconds. |
| Documentation archive and wire-accountability jobs | 0 | Both archive checks and 77 wire checks with controls. |
| `lint_rtl.py` | 0 | Pinned release 5.050; unchanged 90-item ratchet over 78 elaborations. |
| `ctrl_image.py` at two shapes and IF=1/2 | 0 | Four closed RV32I/ILP32 linked compositions; no heap/unresolved symbols. |
| Upstream positive suites, both profiles | 0 | 46 unit cases: 2675 assertions default, 2663 Milan; three behavior scenarios and ten steps per profile. |
| Upstream reversal campaign | 0 | 40/40 controls caught, followed by restored-source pass. |

[ROUND3-GATES.md](ROUND3-GATES.md) lists every exact command, exit and receipt. The compiler-absent docs entry timed out at 540 seconds twice, including on the isolated retry. It calls `test_baremetal_profile_contract`; the manager's builder-bank delegation is recorded without silently extending it to claim this separate docs entry passed. Development compile/site mismatches are documented separately and are not counted as catches. The docs runner self-test ran only inside a disposable job boundary, without host credentials, network or daemon access.

Foreground commands remained bounded, compiler workers stayed within four per campaign, and HDL builds stayed within two concurrent builds with eight inner workers. The service's recorded memory peak was 10,242,949,120 bytes (9.54 GiB), exceeding the requested 9 GB working target. Sampled current use was later about 1.2 GB. This resource exception is disclosed rather than claiming the target was maintained. Observed free space stayed above 59 GB, exceeding the 30 GB floor. Build products, dependencies, exports and tools remain in disk scratch. The packet contains only bounded evidence files; oversized artifacts are represented by size and hash.

## Upstream dependency

The published [applicant follow-up](https://github.com/kebag-logic/lwSRP/tree/495520f5e02dd077fc9b1451942b25ec95afa1b8) is branch `f4-applicant-notes` at `495520f5e02dd077fc9b1451942b25ec95afa1b8`, two commits above `23d9a8173b07503a0ee6e8528f922fceab4e67f0`. It follows dependency PR #12 as a small separate review. This round neither edits that clone nor moves the parent pin.

`applicant_receive_conditions_follow_link_mode` discriminates note 4 in VO and note 5's rIn behavior for both PointToPointMAC values. `pending_applicant_joinin_obeys_note_four` adds VP in both modes. The three guard reversals are `point-to-point-condition`, `pending-point-to-point-condition` and `shared-in-condition`; their individual logs name the failing tests. Positive results and restored-source results are included. `ROUND3-INTEGRITY.json` records the production-source equality and exact clean checkouts.

## Protocol and integration limits

D1 remains resolved: Milan v1.2 4.2.7.2.2 makes MSRP IN/rLv immediate; a later Lv in LV preserves its original five-second deadline. MVRP retains IEEE Table 10-4. D2 remains documented: Listener Lv retains the last declaration subtype because FourPackedEvent Ignore is not a Listener declaration under IEEE 802.1Q-2018 35.2.2.7.2. The five selected processor-wire cases are a differential subset, not exhaustive processor-state coverage. The original processor suites were run in round 2, not rerun in this firmware/documentation-only round.

The latency result remains a conditional desk envelope: 100 ns per mailbox access, one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty in a single 10 ms budget, subtracting only the applicable normative Join wait. Its 11 ms stall control fails from the original origin. It proves neither target scheduling nor wire departure.

The manager owns the compiler-present builder/candidate bank, dependency follow-up integration, hosted evidence, trusted local replication after the next push, fresh independent reviews, candidate-merge validation and post-merge containment. The existing generic LV/rJoin callback suggestion remains upstream; the adapter does not depend on duplicate indications. ACMP application wiring, live MAAP/stream inputs and the actual fabric licence output remain integration work. No hardware, bench, flash, code publication or merge action occurred.

## Earlier rounds

The original FC base is `db9aa8c9b135b34ff3d070a979dee70440b37cc6`. The authorized round-2 no-ff integration merged dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` in `8b43aed`. The old builder timeout was assigned to the manager by ruling 6034653240 and again by round-3 assignment 6035166787; it is not the current status. ROUND2-GATES.md, ROUND2-TESTS.md, ROUND2-SIZE.json and ROUND2-RUNTIME.json are historical evidence, not substitutes for the current results.
