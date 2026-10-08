[A560]

# Round 5 test-to-defect map

Head: `500b8f64443777685e6a54049d933476710d26f0`. All 70 SRP plants are caught by their required named failure at IF=2. The changed four fixtures retain their behavioral assertions and minimum held-block checks. Both interface counts pass all 53 adapter positives, 3 debug cases, 4 timing cases and 5 selected processor-wire cases.

| Named test and file:line | Planted defect | Required failed observable |
|---|---|---|
| `sw/firmware/ctrl/test/srp_mbx.cpp:16`: `Srp.StartupDeclaresTalkersDomainAndVlan` | `startup-vid` | `d.value` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:51`: `Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline` | `short-leave` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:68`: `Srp.RegisteredListenerSubtypeChangeRevokesPermission` | `asking-is-ready` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:74`: `Srp.InterfaceStateDoesNotCross` | `ignore-link` | `adapter.ifs[i].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:89`: `Srp.SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer` | `failed-listener-ready` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:120`: `Srp.DomainUsesPeerPriorityAndVlan` | `ignore-peer-domain` | `domain.priority` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:132`: `Srp.RefusedMailboxRetainsOwedFrameAndDefersInput` | `rx-overtakes-owed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:154`: `Srp.ExpiryBacklogPrecedesSamePassReceive` | `rx-overtakes-expiry` | `adapter.stops` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:168`: `Srp.ReentryFromOutputIsRefusedAndCounted` | `reentry-uncounted` | `adapter.reentries` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:190`: `Srp.InvalidBindingsAndDuplicateBindingsPreserveState` | `invalid-vid` | `srp_mbx_bind` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:207`: `Srp.ExhaustionDuringEachStartupStageReleasesEveryBlock` | `failed-init-leaks` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:222`: `Srp.MissingBootDependenciesRefuseBeforeAttachment` | `missing-port-accepted` | `srp_mbx_init` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:230`: `Srp.AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | `attach-nonatomic` | `srp_mbx_attach` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:249`: `Srp.InvalidFramesHaveNoReservationSideEffects` | `malformed-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:613`: `Srp.RecreateAllocationFailureIsCountedAndRetried` | `reset-skips-recreate` | `adapter.ifs[0].msrp` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:273`: `Srp.ReadyFailedAndUninterestingStreamsAreSeparated` | `readyfailed-ignored` | `Actual function call count` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:282`: `Srp.DomainFilterAndDuplicateDoNotGrowDeclarations` | `foreign-domain-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:290`: `Srp.MvrpAcceptsOnlyCurrentDomainVid` | `foreign-vlan-stored` | `ctrl_pool_in_use` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:308`: `Srp.WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt` | `sink-da-ignored` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:325`: `Srp.AdmissionUsesBandwidthAndEthernetMinimum` | `admission-ceiling-ignored` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:333`: `Srp.DomainExhaustionPreservesOldDeclarationUntilRetry` | `domain-refusal-lost` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:345`: `Srp.SinkDeclarationExhaustionRetriesWithoutLosingBinding` | `listener-refusal-lost` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:362`: `Srp.LinkLossCancelsItsOwedFrameOnly` | `other-link-cancels-owed` | `adapter.owed_len` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:381`: `Srp.OneLoopOwnsTheGlobalCentisecondDispatch` | `duplicate-tick-owner` | `srp_mbx_attach` |
| `sw/firmware/ctrl/test/srp_debug.cpp:6`: `Srp.SynchronousBindingFromOutputAsserts` | `binding-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_debug.cpp:18`: `Srp.SynchronousReceiveFromOutputAsserts` | `receive-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_debug.cpp:31`: `Srp.SynchronousTickFromOutputAsserts` | `tick-debug-guard` | `failed to die` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:394`: `Srp.ListenerBeforeVlanCommitCannotStartTalker` | `licence-before-vlan` | `joined` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:408`: `Srp.SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind` | `unbind-shared-listener` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:432`: `Srp.BoundOldDomainVlanSurvivesDomainChange` | `withdraw-bound-domain` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:441`: `Srp.PriorityOnlyDomainChangeKeepsVlanMembership` | `withdraw-same-domain` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:449`: `Srp.SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent` | `sink-vlan-refusal-lost` | `vlan_requested` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:480`: `Srp.SinkMembershipCommitsBeforeReadyAtStartup` | `ready-before-vlan` | `joined` |
| `sw/firmware/ctrl/test/srp_latency.cpp:40`: `SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget` | `latency-missing-startup` | `commits.size()` |
| `sw/firmware/ctrl/test/srp_latency.cpp:92`: `SrpLatency.ReceiveStateMalformedDomainAndListenerPaths` | `latency-domain-unserviced` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_latency.cpp:119`: `SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog` | `latency-leave-origin` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_latency.cpp:130`: `SrpLatency.FullRingRetainsOriginalOriginAndElevenMillisecondStallFails` | `latency-relaxed-budget` | `service_limit` |
| `sw/firmware/ctrl/test/srp_walk.cpp:19`: `SrpWalk.CertifiedTwoClassDomainVectorAdoptsOnlyClassA` | `walk-domain-ignored` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_walk.cpp:31`: `SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal` | `walk-match-da-ignored` | `declared` |
| `sw/firmware/ctrl/test/srp_walk.cpp:51`: `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` | `walk-leave-shortened` | `Unexpected mock function call` |
| `sw/firmware/ctrl/test/srp_walk.cpp:66`: `SrpWalk.ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire` | `walk-startup-is-join` | `d.event` |
| `sw/firmware/ctrl/test/srp_walk.cpp:96`: `SrpWalk.PerInterfaceWireIdentityAndUnknownOrTruncatedInput` | `walk-malformed-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_shape.cpp:6`: `Srp.EveryGeneratedOutputIsDeclaredAndEverySinkFits` | `shape-last-output-missing` | `outputs` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `Srp.AdmissionStraddlesTheExactEthernetCeiling` | `tag-overhead-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `Srp.AdmissionStraddlesTheExactEthernetCeiling` | `preamble-ifg-omitted` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:540`: `Srp.AdmissionStraddlesTheExactEthernetCeiling` | `ninety-percent-ceiling` | `admitted[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:530`: `Srp.ReadyToReadyFailedNeverGlitchesAnActiveLicence` | `readyfailed-callback-stop` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:549`: `Srp.AdjacentLinkEdgesResetDomainAndAllPriorRegistrations` | `short-link-interruption-ignored` | `domain.priority` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:639`: `Srp.LinkEventsDiscardOnlyTheirPublishedReceivePrefix` | `old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:580`: `Srp.SharedIdentityReconcilesBothBindingOrdersOnTheWire` | `shared-identity-overwritten` | `last` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:664`: `Srp.EventReentryAndSinkCapacityAreGuarded` | `event-reentry-unguarded` | `adapter.reentries` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:613`: `Srp.RecreateAllocationFailureIsCountedAndRetried` | `failed-interface-starves-peer` | `other_sent` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:564`: `Srp.OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `backlogged-old-prefix-accepted` | `mock function call` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:651`: `Srp.LinkLevelLossAndFirstDownEventAreFailClosed` | `link-level-loss-ignored` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:260`: `Srp.ExhaustedPoolStillReusesOwnedBlocksOnLinkReset` | `reset-leaks-owned-participants` | `adapter.refused` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:564`: `Srp.OldReceiveBacklogCannotRegisterAcrossLinkRestart` | `downlink-receive-accepted` | `adapter.ifs[i].registered[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:497`: `Srp.InListenerWithdrawalRevokesLicenceImmediately` | `delayed-in-listener` | `adapter.ifs[i].active[0]` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:507`: `Srp.InTalkerWithdrawalImmediatelyWithdrawsListener` | `delayed-in-talker` | `declared` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:682`: `Srp.ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` | `attach-ignores-current-link` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:709`: `Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` | `cancelled-link-never-recovers` | `adapter.ifs[i].link` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:738`: `Srp.SharedRebindKeepsOnlyTheRemainingEligibleRequest` | `rebind-loses-shared-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:776`: `Srp.ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation` | `consecutive-rebind-loses-applicant` | `left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:820`: `Srp.JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves` | `joining-binding-loses-applicant` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:852`: `Srp.ReboundStreamCannotInheritAnotherStreamsReady` | `applicant-inherited-across-streams` | `ready` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:887`: `Srp.FinalDomainVidUnbindKeepsSrClassMembership` | `final-unbind-withdraws-domain-vid` | `d.event` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:921`: `Srp.LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` | `last-ineligible-vid-leaks` | `vlan_left` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:951`: `Srp.RefusedPeerDomainDoesNotSurviveLinkRestart` | `reset-keeps-owed-domain` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:964`: `Srp.SinkVlanRedeclaredBeforeReadyAfterLinkRestart` | `reset-keeps-sink-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:988`: `Srp.SharedReadyWaitsForTheMatchingBindingsOwnVlan` | `shared-ready-uses-first-vlan` | `vlan` |
| `sw/firmware/ctrl/test/srp_mbx.cpp:1011`: `Srp.MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` | `milan-rapid-leave-leaks-to-mvrp` | `registered()` |

## Applicant-note merge

Dependency head: `ced667d8ee35929ab5f9e77a1c5396e173a693d8`. Both OFF and ON profiles pass 87 tests; all 94 reversals are caught in each profile. The additional note-4 plant must fail its named test, not merely any test in the executable.

| Test and location in dependency clone | Plant | Required distinction |
|---|---|---|
| `tests/unit/integration_test.c:327`, `applicant_receive_conditions_follow_link_mode` | `point-to-point-condition` | Note-4 transition must depend on point-to-point mode. |
| `tests/unit/integration_test.c:327`, `applicant_receive_conditions_follow_link_mode` | `shared-in-condition` | Note-5 transition must depend on shared-medium mode. |
| `tests/unit/integration_test.c:352`, `pending_applicant_joinin_obeys_note_four` | `point-to-point-condition` and `pending-point-to-point-condition` | Pending Applicant JoinIn distinguishes link mode, rather than sharing a no-op starting state. |

Each named plant has a retained failure receipt for both profiles. Restored positive suites pass after reversal campaigns.
