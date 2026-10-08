[A560]

# Round 7 SRP test-to-defect map

Head: `f74b9403b330ce316eeec6f724846f16def98443`. All 102 plants are caught by their named behavioral
observable at IF=2. The twelve new plants are also caught at IF=1.
Positive suites run at both counts: 53 original adapter cases, 17 receive
cases, two composition cases, three debug cases, five timing cases and five
processor-wire cases. The original eleven receive cases are unchanged.
One peer-interface reset body applies only when IF=2. A build error does not
count as a plant detection. Control/MAAP discriminators remain in
`ROUND6-CONTROL-TESTS.md`; all 196 are rerun across three disjoint shards.

| Test with file:line | Planted defect | Required behavioral failure |
| --- | --- | --- |
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
| `sw/firmware/ctrl/test/srp_mbx.cpp:613`: `RecreateAllocationFailureIsCountedAndRetried` | `reset-skips-recreate` | `adapter.ifs[0].msrp` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:273`: `ReadyFailedAndUninterestingStreamsAreSeparated` | `readyfailed-ignored` | `Actual function call count` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:282`: `DomainFilterAndDuplicateDoNotGrowDeclarations` | `foreign-domain-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:290`: `MvrpAcceptsOnlyCurrentDomainVid` | `foreign-vlan-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:308`: `WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt` | `sink-da-ignored` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:325`: `AdmissionUsesBandwidthAndEthernetMinimum` | `admission-ceiling-ignored` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:333`: `DomainExhaustionPreservesOldDeclarationUntilRetry` | `domain-refusal-lost` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:345`: `SinkDeclarationExhaustionRetriesWithoutLosingBinding` | `listener-refusal-lost` | `declared` |
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
| `sw/firmware/ctrl/test/srp_mbx.cpp:480`: `SinkMembershipCommitsBeforeReadyAtStartup` | `ready-before-vlan` | `joined` |
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
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `AdmissionStraddlesTheExactEthernetCeiling` | `tag-overhead-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `AdmissionStraddlesTheExactEthernetCeiling` | `preamble-ifg-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `AdmissionStraddlesTheExactEthernetCeiling` | `ninety-percent-ceiling` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:530`: `ReadyToReadyFailedNeverGlitchesAnActiveLicence` | `readyfailed-callback-stop` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:549`: `AdjacentLinkEdgesResetDomainAndAllPriorRegistrations` | `short-link-interruption-ignored` | `domain.priority` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:639`: `LinkEventsDiscardOnlyTheirPublishedReceivePrefix` | `old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:580`: `SharedIdentityReconcilesBothBindingOrdersOnTheWire` | `shared-identity-overwritten` | `last` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:664`: `EventReentryAndSinkCapacityAreGuarded` | `event-reentry-unguarded` | `adapter.reentries` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:613`: `RecreateAllocationFailureIsCountedAndRetried` | `failed-interface-starves-peer` | `other_sent` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:564`: `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `backlogged-old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:651`: `LinkLevelLossAndFirstDownEventAreFailClosed` | `link-level-loss-ignored` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:260`: `ExhaustedPoolStillReusesOwnedBlocksOnLinkReset` | `reset-leaks-owned-participants` | `adapter.refused` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:564`: `OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `downlink-receive-accepted` | `adapter.ifs[i].registered[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:497`: `InListenerWithdrawalRevokesLicenceImmediately` | `delayed-in-listener` | `adapter.ifs[i].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:507`: `InTalkerWithdrawalImmediatelyWithdrawsListener` | `delayed-in-talker` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:682`: `ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` | `attach-ignores-current-link` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:709`: `CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` | `cancelled-link-never-recovers` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:738`: `SharedRebindKeepsOnlyTheRemainingEligibleRequest` | `rebind-loses-shared-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:776`: `ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation` | `consecutive-rebind-loses-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:820`: `JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves` | `joining-binding-loses-applicant` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:852`: `ReboundStreamCannotInheritAnotherStreamsReady` | `applicant-inherited-across-streams` | `ready` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:887`: `FinalDomainVidUnbindKeepsSrClassMembership` | `final-unbind-withdraws-domain-vid` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:921`: `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` | `last-ineligible-vid-leaks` | `vlan_left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:951`: `RefusedPeerDomainDoesNotSurviveLinkRestart` | `reset-keeps-owed-domain` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:964`: `SinkVlanRedeclaredBeforeReadyAfterLinkRestart` | `reset-keeps-sink-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:988`: `SharedReadyWaitsForTheMatchingBindingsOwnVlan` | `shared-ready-uses-first-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:1011`: `MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` | `milan-rapid-leave-leaks-to-mvrp` | `registered()` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:44`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:77`: `SrpRetry.PartialPayloadKeepsLaterAttributesAndDoesNotRepeatStop` | `partial-receive-retry-removed` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:44`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-record-lost` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:44`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-refusal-malformed` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:99`: `SrpRetry.LaterRecordsCannotOvertakeRetainedInterface` | `receive-overtakes-retained` | `loop.stats.rx_records` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:123`: `SrpRetry.LinkResetCancelsRetainedPayloadAndFencesLaterOldRecords` | `reset-keeps-retained-receive` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:141`: `SrpRetry.OtherInterfaceResetPreservesRetainedPayload` | `peer-reset-cancels-retained-receive` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:160`: `SrpRetry.DestroyCancelsRetainedPayloadBeforeReinitialization` | `destroy-keeps-retained-receive` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:44`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `bind-overtakes-retained-receive` | `srp_mbx_bind` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-attach-omitted` | `app.loop.n_ticks` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-srp-irq-omitted` | `model.irq_enable` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-srp-tick-omitted` | `app.loop.stats.ticks` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:173`: `SrpRetry.FailedParticipantRecreationRetainsFreshReceive` | `recreated-receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:191`: `SrpRetry.RetainedMvrpUsesItsOriginalParticipant` | `mvrp-receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:214`: `SrpRetry.RetainedReceiveWaitsForOwedTransmit` | `receive-retry-passes-owed` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:232`: `SrpRetry.RetainedReceiveWaitsForTickAndLifecycleBacklogs` | `receive-retry-passes-backlog` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:259`: `SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped` | `future-receive-refused` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:259`: `SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped` | `invalid-suffix-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_app.cpp:6`: `SrpApp.AttachRefusalPreservesExistingComposition` | `composition-refusal-ignored` | `ctrl_app_attach_srp` |
| `sw/firmware/ctrl/test/srp_latency.cpp:142`: `SrpLatency.ReceiveRecoveryKeepsOriginalArrivalBudget` | `recovery-latency-retry-removed` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-retention-unbounded` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-retention-short` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-retention-late` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-discard-uncounted` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-discard-malformed` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:277`: `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | `receive-discard-as-success` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:307`: `SrpRetry.QueuedRefusalKeepsOriginalArrivalDeadlineAcrossClockWrap` | `receive-queue-renews-deadline` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:307`: `SrpRetry.QueuedRefusalKeepsOriginalArrivalDeadlineAcrossClockWrap` | `receive-first-refusal-never-expires` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:324`: `SrpRetry.RecoveryAtDeadlineStillAppliesTheCompleteRecord` | `receive-expiry-precedes-recovery` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:352`: `SrpRetry.FailedRecreationCannotRetainInputBeyondItsDeadline` | `receive-recreate-never-expires` | `adapter.rx_discarded` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:374`: `SrpRetry.DomainFloodCannotDelayLaterRapidLeave` | `receive-flood-unbounded` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:337`: `SrpRetry.RetainedDeadlineCrossesClockWrapWithoutEarlyDiscard` | `receive-deadline-not-modular` | `adapter.rx_discarded` |
