[A560]

# SRP test sensitivity

Relates to #665. Paths below are relative to `sw/firmware/ctrl/`.
All 43 planted defects are caught by the named failing observable; compilation failures do not count.
The normal suites run at one and two interfaces; mutation grading uses two.
The shape case additionally runs on every shipped configuration at both interface counts.

| Test and source | Planted defect | Required failing observable |
|---|---|---|
| `test/srp_mbx.cpp:5` `Srp.StartupDeclaresTalkersDomainAndVlan` | `startup-vid` | `d.value` |
| `test/srp_mbx.cpp:40` `Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline` | `short-leave` | `Unexpected mock function call` |
| `test/srp_mbx.cpp:57` `Srp.RegisteredListenerSubtypeChangeRevokesPermission` | `asking-is-ready` | `adapter.ifs[0].active[0]` |
| `test/srp_mbx.cpp:63` `Srp.InterfaceStateDoesNotCross` | `ignore-link` | `adapter.ifs[i].active[0]` |
| `test/srp_mbx.cpp:78` `Srp.SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer` | `failed-listener-ready` | `declared` |
| `test/srp_mbx.cpp:109` `Srp.DomainUsesPeerPriorityAndVlan` | `ignore-peer-domain` | `domain.priority` |
| `test/srp_mbx.cpp:121` `Srp.RefusedMailboxRetainsOwedFrameAndDefersInput` | `rx-overtakes-owed` | `adapter.received` |
| `test/srp_mbx.cpp:143` `Srp.ExpiryBacklogPrecedesSamePassReceive` | `rx-overtakes-expiry` | `adapter.stops` |
| `test/srp_mbx.cpp:157` `Srp.ReentryFromOutputIsRefusedAndCounted` | `reentry-uncounted` | `adapter.reentries` |
| `test/srp_mbx.cpp:179` `Srp.InvalidBindingsAndDuplicateBindingsPreserveState` | `invalid-vid` | `srp_mbx_bind` |
| `test/srp_mbx.cpp:196` `Srp.ExhaustionDuringEachStartupStageReleasesEveryBlock` | `failed-init-leaks` | `ctrl_pool_in_use` |
| `test/srp_mbx.cpp:211` `Srp.MissingBootDependenciesRefuseBeforeAttachment` | `missing-port-accepted` | `srp_mbx_init` |
| `test/srp_mbx.cpp:219` `Srp.AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | `attach-nonatomic` | `srp_mbx_attach` |
| `test/srp_mbx.cpp:238` `Srp.InvalidFramesHaveNoReservationSideEffects` | `malformed-uncounted` | `adapter.malformed` |
| `test/srp_mbx.cpp:249` `Srp.ExhaustedPoolStillReusesOwnedBlocksOnLinkReset` | `reset-skips-recreate` | `crashed on signal` |
| `test/srp_mbx.cpp:262` `Srp.ReadyFailedAndUninterestingStreamsAreSeparated` | `readyfailed-ignored` | `Actual function call count` |
| `test/srp_mbx.cpp:271` `Srp.DomainFilterAndDuplicateDoNotGrowDeclarations` | `foreign-domain-stored` | `ctrl_pool_in_use` |
| `test/srp_mbx.cpp:279` `Srp.MvrpAcceptsOnlyCurrentDomainVid` | `foreign-vlan-stored` | `ctrl_pool_in_use` |
| `test/srp_mbx.cpp:297` `Srp.WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt` | `sink-da-ignored` | `declared` |
| `test/srp_mbx.cpp:314` `Srp.AdmissionUsesBandwidthAndEthernetMinimum` | `admission-ceiling-ignored` | `admitted[0]` |
| `test/srp_mbx.cpp:322` `Srp.DomainExhaustionPreservesOldDeclarationUntilRetry` | `domain-refusal-lost` | `domain.vid` |
| `test/srp_mbx.cpp:335` `Srp.SinkDeclarationExhaustionRetriesWithoutLosingBinding` | `listener-refusal-lost` | `declared` |
| `test/srp_mbx.cpp:351` `Srp.LinkLossCancelsItsOwedFrameOnly` | `other-link-cancels-owed` | `adapter.owed_len` |
| `test/srp_mbx.cpp:368` `Srp.OneLoopOwnsTheGlobalCentisecondDispatch` | `duplicate-tick-owner` | `srp_mbx_attach` |
| `test/srp_debug.cpp:6` `Srp.SynchronousBindingFromOutputAsserts` | `binding-debug-guard` | `failed to die` |
| `test/srp_debug.cpp:18` `Srp.SynchronousReceiveFromOutputAsserts` | `receive-debug-guard` | `failed to die` |
| `test/srp_debug.cpp:31` `Srp.SynchronousTickFromOutputAsserts` | `tick-debug-guard` | `failed to die` |
| `test/srp_mbx.cpp:381` `Srp.ListenerBeforeVlanCommitCannotStartTalker` | `licence-before-vlan` | `joined` |
| `test/srp_mbx.cpp:395` `Srp.SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind` | `unbind-shared-listener` | `d.event` |
| `test/srp_mbx.cpp:419` `Srp.BoundOldDomainVlanSurvivesDomainChange` | `withdraw-bound-domain` | `d.event` |
| `test/srp_mbx.cpp:428` `Srp.PriorityOnlyDomainChangeKeepsVlanMembership` | `withdraw-same-domain` | `d.event` |
| `test/srp_mbx.cpp:436` `Srp.SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent` | `sink-vlan-refusal-lost` | `vlan_requested` |
| `test/srp_mbx.cpp:466` `Srp.SinkMembershipCommitsBeforeReadyAtStartup` | `ready-before-vlan` | `joined` |
| `test/srp_latency.cpp:40` `SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget` | `latency-missing-startup` | `commits.size()` |
| `test/srp_latency.cpp:92` `SrpLatency.ReceiveStateMalformedDomainAndListenerPaths` | `latency-domain-unserviced` | `domain.vid` |
| `test/srp_latency.cpp:119` `SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog` | `latency-leave-origin` | `Unexpected mock function call` |
| `test/srp_latency.cpp:130` `SrpLatency.FullRingRetainsOriginalOriginAndElevenMillisecondStallFails` | `latency-relaxed-budget` | `service_limit` |
| `test/srp_walk.cpp:19` `SrpWalk.CertifiedTwoClassDomainVectorAdoptsOnlyClassA` | `walk-domain-ignored` | `domain.vid` |
| `test/srp_walk.cpp:31` `SrpWalk.StreamMatcherNearMissSwapAndDelayedWithdrawal` | `walk-match-da-ignored` | `declared` |
| `test/srp_walk.cpp:53` `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` | `walk-leave-shortened` | `Unexpected mock function call` |
| `test/srp_walk.cpp:68` `SrpWalk.ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire` | `walk-startup-is-join` | `d.event` |
| `test/srp_walk.cpp:98` `SrpWalk.PerInterfaceWireIdentityAndUnknownOrTruncatedInput` | `walk-malformed-uncounted` | `adapter.malformed` |
| `test/srp_shape.cpp:6` `Srp.EveryGeneratedOutputIsDeclaredAndEverySinkFits` | `shape-last-output-missing` | `outputs` |

The existing F0/FC campaign covers the unchanged pool, debug sink, driver and prior loop paths. All 97 controls pass, separate from these 43. The shared RV32 self-test passes 17 compiler/header/ELF/runtime controls.

## Upstream test sensitivity

The fifteen added cgreen cases each reject a separately planted source defect at the final upstream pin. Every faulty source compiled, every run returned 1 and named the intended failed test; sources were restored after each plant. The restored suite returns 0 (24 cases, 1,914 assertions). The existing nine cases and three behavior scenarios also pass at every Part B branch head.

| Test and source | Planted defect | Observed result |
|---|---|---|
| `tests/unit/timer_test.c:15` `remove_head_middle_tail_and_reinitialize` | Fire expiry during removal instead of cancelling silently. | 1; named test fails |
| `tests/unit/timer_test.c:38` `destroy_with_live_attribute_timers_then_tick` | Leave a freed port LeaveAll timer linked. | 1; named test fails |
| `tests/unit/msrp_values_test.c:8` `domain_and_vector_offsets_match_wire_fields` | Drop the Domain class vector offset. | 1; named test fails |
| `tests/unit/msrp_values_test.c:44` `domain_callback_preserves_existing_member_order` | Insert a field before the existing first callback. | 1; named test fails |
| `tests/unit/receive_test.c:18` `truncation_respects_complete_vectors_and_pdu_end` | Deliver receive callbacks before whole-PDU validation. | 1; named test fails |
| `tests/unit/receive_test.c:57` `changed_registered_listener_notifies_without_duplicate_join` | Suppress changed Listener notification while already registered. | 1; named test fails |
| `tests/unit/receive_test.c:83` `uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | Ignore the receive-interest filter and allocate uninteresting streams. | 1; named test fails |
| `tests/unit/receive_test.c:108` `withdrawal_does_not_replace_the_registered_declaration` | Overwrite the registered value with a withdrawal subtype. | 1; named test fails |
| `tests/unit/receive_test.c:129` `talker_join_replaces_the_other_type_on_the_same_port` | Skip same-port replacement of the opposite Talker attribute type. | 1; named test fails |
| `tests/unit/transmit_test.c:39` `fresh_ladder_and_refusal_are_transactional` | Encode New as JoinMt. | 1; named test fails |
| `tests/unit/transmit_test.c:66` `leaveall_then_withdrawal_retains_until_leave_expiry` | Halve the configured LeaveTime. | 1; named test fails |
| `tests/unit/transmit_test.c:83` `refused_pdu_survives_timers_without_aging_unsent_leaveall` | Discard owed TX when a new receive arrives. | 1; named test fails |
| `tests/unit/transmit_test.c:112` `receive_redeclare_requests_transmission_without_periodic_wait` | Clear the requested Applicant transmit opportunity. | 1; named test fails |
| `tests/unit/transmit_test.c:143` `a_full_pdu_retries_omitted_attributes_before_repeats` | Always visit normal order instead of deferred attributes first. | 1; named test fails |
| `tests/unit/transmit_test.c:163` `changed_listener_redeclares_from_a_quiet_applicant` | Use Join for a changed Listener instead of New. | 1; named test fails |

