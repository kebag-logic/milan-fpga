[A560]

# F4 handoff

Relates to #665. Status: REVIEW READY for the assigned F4 scope, subject to the explicit evidence limits below.
Parent branch: `665-f4-srp`. Parent head: `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`.
Assigned base: `db9aa8c9b135b34ff3d070a979dee70440b37cc6` (FC round 2).
Executor: [A560]. Independent reviewers: [R532] and [R533].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477

## Result and scope

The adapter provides per-interface MSRP/MVRP on the SRP mailbox, static entity-sized storage, startup Talker declarations, Domain/VLAN membership and the F3 binding port. A withdrawal after LeaveAll stops the Talker at the original five-second deadline. Accepted VLAN output precedes Talker permission and Listener Ready; refused output retains immutable bytes and interface until commit. Shared bindings retain their declarations until the last user leaves.

No RTL, register map, default all-fabric build or shipping firmware changed. No push, PR operation, merge, rebase, hardware access or flashing occurred. F3 is absent from the assigned base, so application binding wiring remains owed as the assignment permits. The licence callback and MAAP allocation inputs also need final target composition. This is desk evidence, not a connected target image or wire-timing claim.

The local upstream dependency must be published before the parent can be fetched remotely. The final pin is `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da`, local branch `zephyr-api-docs`. The manager owns publication, FC/dev integration and review. The later explicit no-merge instruction left the requested final dev integration unperformed. No review verdict is claimed here.

## Assignment acceptance

| Requirement | Result and evidence |
|---|---|
| Part A licence/provenance | Apache-2.0 LICENSE, NOTICE, SPDX and contribution statement on `apache-2.0`; no conflicting notice found. |
| Exact dependency and static port | Final gitlink and build pin agree; host and freestanding RV32 builds pass; generated static pool and exhaustion paths are tested. |
| Per-interface mailbox/declarations | Thirty adapter cases at IF=1/2, three debug cases, ten generated entity shapes; owed TX, Domain/MVRP, Talker admission and Listener bindings covered. |
| No synchronous callbacks | Release counts and ignores valid/invalid reentry; debug asserts; before-fix red probes and planted controls retained. |
| #608 and timing | Original five-second leave deadline survives Lv in LV; four timing cases separate normative wait from the conditional 10 ms host service envelope. |
| Differential and sensitivity | Five selected processor wire comparisons at IF=1/2; D1/D2 documented with clauses; 43 SRP, 97 existing and 15 upstream source defects detected. |
| Coverage and gates | 100% after existing exclusions across 15 firmware files, no new exclusion; exact gate table below; optional builder calibration skip disclosed. |
| F3 composition | F3 absent from assigned base; binding port exposed and application wiring explicitly owed as permitted. |
| Scope boundaries | Tracked diff contains no RTL, non-mailbox register map, default fabric configuration or shipping-image change. |

## Changes

| File:line | Change and purpose |
|---|---|
| `.gitmodules:13` | Register the exact upstream dependency; gitlink pins the locally reviewed topic stack. |
| `.github/workflows/rtl-fast.yml:243` | Fetch SRP, install the SDK before control builds, require RV32 and the control mutation campaign. |
| `scripts/ci_events.py:2344` | Hold the changed firmware CI command order and dependency contract. |
| `docs/testing/CI_WORKFLOWS.md:2255` | Record mandatory hosted dependency/build/mutation work and its publication prerequisite. |
| `sw/firmware/ctrl/README.md:2` | Document SRP layout, updated pin and freestanding SDK requirements. |
| `sw/firmware/ctrl/loop/ctrl_loop.h:99` | Add optional receive readiness; existing users have no readiness restriction. |
| `sw/firmware/ctrl/loop/ctrl_loop.c:28` | Check readiness before each RX pop, so owed TX and earlier tick expiry retain ordering. |
| `sw/firmware/ctrl/port/shlan_port.h:19` | State the no-synchronous-callback contract at the existing port boundary. |
| `sw/firmware/ctrl/srp/srp_mbx.h:19` | Declare static state, entity-derived pool capacity and ACMP-facing binding port. |
| `sw/firmware/ctrl/srp/srp_mbx.c:14` | Implement static allocation, per-interface MRP, admission, ordered declarations and transactional output. |
| `sw/firmware/ctrl/srp/srp_entity.py:12` | Derive SRP counts from authoritative entity generation, without default counts. |
| `sw/firmware/ctrl/srp/README.md:2` | Record lifecycle, clauses, timing assumptions, differential and owed integration. |
| `sw/firmware/ctrl/test/ctrl_arms.py:226` | Require exact SRP pin; use freestanding ABI/runtime checks from #679. |
| `sw/firmware/ctrl/test/ctrl_build.py:44` | Record compiler stack usage while building RV32I/ILP32. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:438` | Reuse one isolated path for valid content-keyed compiler caching; restore source before every plant. |
| `sw/firmware/ctrl/test/ctrl_reuse.py:31` | Verify submodule root before submodule git reads. |
| `sw/firmware/ctrl/test/srp_arms.py:19` | Build both interface shapes, all entity shapes and the required RV32 objects. |
| `sw/firmware/ctrl/test/srp_fixture.hpp:26` | Drive actual mailbox/loop/pool ports with a strict licence mock and independent wire decoding. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:5` | Thirty behavior and robustness cases; release reentry rejects valid and invalid inputs without malformed-input side effects. |
| `sw/firmware/ctrl/test/srp_debug.cpp:6` | Three reentry assertion cases, including invalid arguments before validation. |
| `sw/firmware/ctrl/test/srp_latency.cpp:11` | Four service-envelope cases with original event/deadline origins. |
| `sw/firmware/ctrl/test/srp_latency_policy.hpp:5` | Named 10 ms test predicate; a relaxed 20 ms mutant is rejected. |
| `sw/firmware/ctrl/test/srp_shape.cpp:6` | All outputs and sinks fit each generated entity; compare counts against independent fabric facts. |
| `sw/firmware/ctrl/test/srp_walk.cpp:7` | Five selected processor wire comparisons using verified source stimuli. |
| `sw/firmware/ctrl/test/srp_reuse.py:9` | Verify the processor gitlink and blobs before extracting builders and Applicant tables. |
| `sw/firmware/ctrl/test/srp_mutants.py:40` | Forty-three named planted defects, each requiring its own failed observable. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:102` | Include SRP, shapes, debug and differential arms; bound compilation concurrency. |
| `sw/firmware/gtest/fw_coverage.py:419` | Forward the requested jobs cap to both firmware coverage gates. |
| `sw/firmware/gtest/coverage.ratchet:15` | Regenerate through the coverage gate; no exclusion added. |
| `sw/firmware/gtest/fw_rv32.py:29` | Import existing #679 shared freestanding compiler/ELF/runtime helper. |
| `sw/firmware/gtest/fw_rv32_selftest.py:146` | Import existing #679 hostile-header, ABI and runtime negative controls. |
| `sw/firmware/gtest/rv32_include/string.h:1` | Import existing #679 minimal freestanding declarations. |
| `sw/firmware/gtest/rv32_include/stdio.h:1` | Import existing #679 minimal debug-format declaration. |
| `sw/firmware/ctrl_nvm/test/nvm_rv32.py:36` | Import exact existing #679 helper consumer so the shared negative controls cover both users. |
| `third_party/lwSRP` | Gitlink to the exact local dependency head above. |

The #679 helper imports are byte-identical to their versions at `origin/dev` commit `910f338dbd050f4efd2d96991ddcf928a583d55f`; they are dependency integration, with no saved-state firmware change. The control helper integration uses the same checks for SRP. The pinned SDK distribution is ilp32d; the product objects are RV32I/ILP32, freestanding with no hosted headers.

## Test sensitivity

 Paths below are relative to `sw/firmware/ctrl/`.
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

The final guard correction moves entry checks before binding/frame validation (`sw/firmware/ctrl/srp/srp_mbx.c:268`, `:313`). Before the fix, the release probe observed 7 counted entries instead of 9 and two malformed-input side effects; both invalid-input debug probes failed to assert. These red results are retained as defect evidence.

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

## Coverage

The complete generator and ratchet check run both firmware populations. Counts below are after the existing documented exclusions; SRP and the changed loop have none. No exclusion was added.

| File | Lines | Branch arcs |
|---|---:|---:|
| `sw/firmware/ctrl/adp/adp.c` | 168/168 | 73/73 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 14/14 | 8/8 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx.c` | 173/173 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 359/359 | 342/342 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 195/195 | 104/104 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

## Timing and differential

The service envelope measures actual mailbox accesses at 100 ns each, adds one aggregate 1 ms CPU/preemption allowance and 100 ns observation uncertainty, and holds the single 10 ms project budget. Normal measured service is at most 1.0204 ms in the tested paths. Full elapsed Domain/Listener/withdrawal intervals include a 200 ms outstanding Join wait. The tested LeaveAll draws had no outstanding Join wait; the calculation derives any remaining wait from the previous accepted transmission. Leave expiry starts at the original five-second deadline. An 11 ms full-ring stall fails the budget predicate from its original origin.

These explicit assumptions still require target timing, scheduling, ingress and egress validation. They do not establish wire departure or a whole-call-chain stack bound. The original processor suites pass independently: `srp_stream_fsms` 1,219 checks and `srp_top` 2,200 checks, plus the SRP storage-shape runs. Five selected wire comparisons reuse the verified processor stimuli at one and two interfaces; the differential is not an exhaustive walk of all processor states.

| Difference | Observed expectation | Normative firmware result |
|---|---|---|
| D1 | Stream-FSM section E expects immediate loss on Talker Lv from IN | IEEE 802.1Q-2018 Table 10-4 retains LV until LeaveTime. Lv in LV does not restart it; #608 stops at the original deadline. |
| D2 | Stream-FSM sections B/E use Listener subtype Ignore on withdrawal | IEEE 802.1Q-2018 35.2.2.7.2 ignores the event when subtype is Ignore. Firmware retains the previous valid subtype on Lv. |

The adapter README records the detailed contracts and clauses. IEEE 802.1Q, not the fabric implementation, decides these differences.

## Resource evidence

| Entity | Interfaces | Sources / sinks | Static arena | Adapter on host | RV32 object text / data / BSS |
|---|---:|---|---:|---:|---|
| `arty_4x4` | 1 | 5 / 5 | 15968 | 3520 | 32669 / 140 / 178 |
| `arty_8ch` | 1 | 5 / 5 | 15968 | 3520 | 32669 / 140 / 178 |
| `arty_current` | 1 | 1 / 2 | 9056 | 3312 | 32305 / 140 / 178 |
| `ax7101_1x1_tdm8` | 1 | 2 / 2 | 9920 | 3344 | 32637 / 140 / 178 |
| `ax7101_8x8` | 1 | 9 / 9 | 24032 | 3752 | 32689 / 140 / 178 |
| `arty_4x4` | 2 | 5 / 5 | 31936 | 3936 | 33237 / 140 / 178 |
| `arty_8ch` | 2 | 5 / 5 | 31936 | 3936 | 33237 / 140 / 178 |
| `arty_current` | 2 | 1 / 2 | 18112 | 3520 | 32849 / 140 / 178 |
| `ax7101_1x1_tdm8` | 2 | 2 / 2 | 19840 | 3584 | 33253 / 140 / 178 |
| `ax7101_8x8` | 2 | 9 / 9 | 48064 | 4400 | 33237 / 140 / 178 |

Object totals include the port, driver, loop, SRP adapter and five library sources. Caller-owned state and pool are separate. Largest compiler-reported static frame is 192 bytes for every shape. The SDK archive is 102,597,892 bytes, SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`. No package, toolchain or large artifact is in this packet.

## Local dependency branches

 All branches are local; publication and upstream reviews are owed.
Final parent pin: `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da` on `zephyr-api-docs`.
The branches form one ancestry stack; publish prerequisites before dependent heads.

| Branch | Commit | Unit tests | Assertions | Behavior suite |
|---|---|---:|---:|---|
| `apache-2.0` | `fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b` | 9 | 1690 | Baseline setup failure; fixed by `test-entrypoints` |
| test-entrypoints | 58ed80ee13d6bc708d0017e8ec87a19b11b267b0 | 9 | 1690 | 3 scenarios / 10 steps |
| timer-lifetime | 9c7ee482888c57dd95599233756337f90303c935 | 11 | 1704 | 3 scenarios / 10 steps |
| msrp-wire-values | d8d10b58fb513465cc746bd07307f84d35a7c1c9 | 12 | 1725 | 3 scenarios / 10 steps |
| mrp-receive-validation | 7e81da9c6ad03090f380e17fbf84b3cb5016434a | 13 | 1777 | 3 scenarios / 10 steps |
| mrp-transmit | 33651955c213d0d6e03155e718e9e64508850f78 | 15 | 1803 | 3 scenarios / 10 steps |
| freestanding-headers | d11a55281d6aaae42e3995821e85b0c073decac8 | 15 | 1803 | 3 scenarios / 10 steps |
| mrp-transmit-retry | 5724550c0f96c65c4cd5e5d42f699a67fb14d2f0 | 16 | 1818 | 3 scenarios / 10 steps |
| mrp-registration-updates | 7d72af7a6c8cf0c35472de415d5b3a096897f5e0 | 17 | 1829 | 3 scenarios / 10 steps |
| parser-vector-reads | c09d91299f65575835b78b7e1653cd981d35b0a1 | 17 | 1829 | 3 scenarios / 10 steps |
| mrp-transmit-opportunities | 96b323fa43f98b0d8329212d81335982873ec67a | 18 | 1837 | 3 scenarios / 10 steps |
| mrp-bounded-storage | bb35392c2c75f0a8e874dd1a5bd816cd9eef6c92 | 19 | 1845 | 3 scenarios / 10 steps |
| mrp-pdu-segmentation | 4d09ed27f57958eb9e2625ae18200593308b79f7 | 20 | 1895 | 3 scenarios / 10 steps |
| mrp-withdrawal-value | f8fb5528eff0a1f1519b4e896bbd0f235762815b | 21 | 1900 | 3 scenarios / 10 steps |
| msrp-context-compatibility | 4c6a0fe3ca5ab02de804d99408ba957dd673ee9b | 22 | 1902 | 3 scenarios / 10 steps |
| msrp-talker-replacement | 8e6ecc885495c0cf3b13689ad5203091a9c52d30 | 23 | 1909 | 3 scenarios / 10 steps |
| bare-metal-api-docs | f5e244eb2f5bbe8f207ac6e5770ba45fcfd6d156 | 23 | 1909 | 3 scenarios / 10 steps |
| msrp-listener-new | a832b2813671037a2027a683a110767aa07995ae | 24 | 1914 | 3 scenarios / 10 steps |
| zephyr-api-docs | ef8a28b9f991ad2f6a466b377c25c2f7bcb310da | 24 | 1914 | 3 scenarios / 10 steps |

Part A adds the full official Apache-2.0 licence, NOTICE, SPDX labels and the company-contribution statement. The ownership decision is in the assignment. No conflicting copyright/licence notice was found. The original queue credits an algorithm; it carries no separate code licence.

Every Part B row was rebuilt at that exact local branch head with CMake, CTest and behave. All four commands returned zero. The final row only updates Zephyr help; the compiled source tree equals its predecessor.

## Upstream file map

Paths in this table are relative to the separate lwSRP clone at the final pin. Every changed source, header, test and build entry also carries its Apache-2.0 identifier.

| File:line | Change |
|---|---|
| `CMakeLists.txt:35` | Build exported entry points and the added cgreen regression suites. |
| `Kconfig.zephyr:6` | Describe the actual centisecond timer and asynchronous transmit integration. |
| `LICENSE:1` | Full Apache-2.0 licence text. |
| `NOTICE:1` | Required project notice. |
| `README.md:61` | Document contributions, bounded storage, timer/TX ownership and bare-metal integration. |
| `behave.ini:1` | Add the Apache-2.0 SPDX identifier. |
| `build.sh:2` | Add the Apache-2.0 SPDX identifier. |
| `src/core/mrp_mad.c:13` | Bound registration storage; manage timers and state; validate receive before mutation; retain transactional output and segment PDUs. |
| `src/core/mrp_pdu.c:13` | Correct wire parsing, vector bounds, lengths and checked encoding. |
| `src/core/switch.c:1` | Export switch entry points for the existing behavior harness. |
| `src/core/switch_ctrl.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/error.h:1` | Provide stable freestanding API error values without hosted errno state. |
| `src/include/shish_lan/mmrp.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/mrp.h:231` | Expose bounded port configuration, receive filtering, visitation, reclaim and committed TX hooks. |
| `src/include/shish_lan/mrp_pdu.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/msrp.h:33` | Expose context compatibility, Talker registration replacement and Listener subtype updates. |
| `src/include/shish_lan/mvrp.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/switch.h:27` | Declare exported switch entry points. |
| `src/include/shish_lan/switch_ctrl.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/modules/mmrp.c:10` | Use freestanding error values and remove hosted allocation headers. |
| `src/modules/msrp.c:22` | Correct wire values, registration updates, Talker replacement and Listener New redeclaration. |
| `src/modules/mvrp.c:9` | Use freestanding error values and remove hosted allocation headers. |
| `src/modules/sim_adapter.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/modules/sim_adapter.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/ports/alloc.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/ports/alloc.h:5` | Use the freestanding size declaration. |
| `src/ports/timer.c:36` | Unlink destroyed timers and prevent stale or duplicate timer ownership. |
| `src/ports/timer.h:42` | Declare timer finalization. |
| `tests/features/environment.py:9` | Load the explicitly built shared library for each branch gate. |
| `tests/features/steps/switch_steps.py:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/features/switch.feature:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/unit/mrp_pdu_test.c:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/unit/msrp_values_test.c:1` | Check independent MSRP wire values and context compatibility. |
| `tests/unit/placeholder.c:13` | Register all new cgreen suites. |
| `tests/unit/receive_test.c:1` | Check malformed input, registration replacement, resource limits and subtype changes. |
| `tests/unit/timer_test.c:1` | Check destruction, callback order and timer lifetime. |
| `tests/unit/transmit_test.c:1` | Check refusal retry, opportunities, segmented output and retained withdrawal values. |
| `zephyr/module.yml:1` | Add the Apache-2.0 SPDX identifier. |

## Gates

The lane's final firmware, upstream, mailbox, processor, generation and documentation commands return zero. The builder bank completes all 100 original functions; its existing gate 11 calibration arm explicitly skips because the external mf48 utilization report is absent. That arm is not claimed as passed. Detailed command provenance, attempt history and SHA-256/size records are in GATES.md; the per-function builder ledger is BUILDER-RESULTS.json.

| Command | rc | Result and log |
|---|---:|---|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "${SCRATCH}/firmware-guard-final"` | 0 | All host, debug, timing, differential, entity and RV32 arms; 97 existing and 43 SRP mutants; two pin controls. `firmware-guard-final.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4` | 0 | Generator records 15 files, 100% after existing exclusions. `coverage-guard-write.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | Ratchet passes; SRP 359 lines / 342 arcs, no exclusions. `coverage-guard-check.log` |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 17 negative controls pass. `rv32-nvm-final-0.log` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 434 saved-state cases and required RV32 builds pass. `nvm-normal-final.log` |
| `make -C "${SCRATCH}/mailbox-gate/tb/verilator/mbx" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | Both RTL bus adapters, model differential, IF=2 and five mutations pass. `mailbox-gate.log` |
| `make -C "${SCRATCH}/processor-gates/tb/srp_stream_fsms" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | 1,219 checks and shape walks pass. `processor-srp_stream_fsms.log` |
| `make -C "${SCRATCH}/processor-gates/tb/srp_top" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | 2,200 checks and storage-shape runs pass. `processor-srp_top.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | Final firmware workflow: 2,358 self-test arms pass. `ci-events-final.log` |

| Original builder main-list functions, resumed in foreground batches | 0 per function | 100/100 functions complete; optional gate 11 calibration skipped. |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | Generated mailbox contract current. |
| Documentation, source quality and gate controls | 0 each | Exact commands and logs in GATES.md. |
| CMake configure/build, CTest and behave on all 18 Part B heads | 0 each | Final 24 cgreen tests / 1,914 assertions; three scenarios / ten steps. |
| Fifteen upstream source-defect controls | 0 aggregate | Each compiled plant returns 1 with its named failed test; restored suite returns 0. |

The parent and all checked submodules are clean at the recorded heads. Generated test images and bytecode were preserved in scratch; the temporary builder output link was removed. The complete parent tree is locally committed. Hosted contexts, the repository-wide exhaustive RTL/synthesis merge bar, independent review and candidate-merge validation remain manager-owned publication/integration obligations. This evidence is not a review verdict or a merge approval.

## Reproduction and remaining obligations

Initialize the recorded submodules after the manager publishes the upstream pin. Use the CI-pinned SDK and Verilator 5.050; set `TMPDIR` to disk scratch and `MILAN_RV32_CC` to the verified SDK compiler. Keep the public gate commands at four jobs or less. The user-assigned scratch area holds the raw logs named by the packet's evidence manifest.

Before merge: publish/review the upstream topic stack, make its pin fetchable, integrate FC/dev, complete the two independent reviews and their five-lens ledger, validate the candidate merge and satisfy protected hosted gates. The application binding and licence wiring, dynamic MAAP allocation integration and physical timing evidence remain part of #665 integration; this lane does not close that issue.
