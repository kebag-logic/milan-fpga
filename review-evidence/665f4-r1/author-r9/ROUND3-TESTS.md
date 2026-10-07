[A560]

# Round 3 test-to-defect map

Head: `c1049de1970e93d2c36ace62891ee9d947cd3191`. All 67 SRP controls compiled and failed their named observations in the final complete firmware run.

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
