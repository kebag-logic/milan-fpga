# Historical Round 2 handoff

This records evidence at the prior head. Publication statements describe the earlier session, not the current PR state.

# F5 handoff

[A572] local head `0ded1f269a44d107498f177c8276665656e07d30` on `665-f5-aecp`.
Round 2 starts at `1e68d1b62ef2facdf0e8dbad28a202297d433c61`; the lane base is `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

Status: REVIEW READY. Implementation and required local verification are complete at the stated unpushed head. Every required command family returned 0; no STOP condition was reached. Independent re-review and publication checks remain owed.

## Round 2

Assignment: [issue #665, round 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6085423196).
Findings: [R565-1](https://github.com/kebag-logic/milan-fpga/pull/700#issuecomment-6085319671) and [R564-1](https://github.com/kebag-logic/milan-fpga/pull/700#issuecomment-6085414859).
Executor [A572], internal reviewer [R564], external reviewer [R565]. This is implementation evidence; independent re-review remains owed.

1. ENTITY/CONFIGURATION reads ignore received configuration_index and return zero; other configuration and descriptor-index checks remain. IEEE 7.4.5.1/.2.
2. SET_STREAM_INFO reports current format, stream ID, MAC, VLAN and applicable flags on success and refusal. Successful latency changes retain the requested latency. SAVED_STATE/STREAMING_WAIT are ignored, no valid sub-command succeeds, and unsupported valid sub-commands fail. IEEE 7.4.15.1; Milan 5.4.2.9.
3. Unavailable events remain pending and retry after 1 ms. Eligible peer descriptors continue, including through transmit stalls. Tests cover several unavailable event types, same-descriptor recovery, interface fanout, wraparound and counter spacing. Milan 5.4.5.2/Table 5.22.
4. Every public input is guarded across AECP instances, including init, queries and saved-state inputs. Diagnostic builds assert; release builds refuse/count. Initialization checks before touching destination storage and charges a refusal to the callback owner. Issue #678.
5. HDCP commands receive an empty-data NOT_IMPLEMENTED response preserving sequence, flags and fragment offset. AA/AVC receive their typed NOT_IMPLEMENTED responses. Reserved/extended values are ignored. IEEE 9.4.4/.5, 9.5.4/.5, 9.6.4, 9.7.4 and Table 9-1. The contract records remaining reference differences.
6. ENTITY available_index comes from the ingress interface’s ADP owner through typed observation ports. The composed test emits N real advertisements and reads N. IEEE 7.2.1/6.2.2.15.
7. All four linked spans remain below 224 KB. Largest: 221728 bytes, including an 8192-byte stack reservation.

## Changes at the current head

| File:line | Change |
|---|---|
| `docs/design/MAILBOX_SPLIT.md:568` | Describe the implemented F5 notification bridge. |
| `sw/firmware/ctrl/aecp/README.md:10` | Record callback/retry/ADP contracts, non-AEM decisions and clause-specific wire differences. |
| `sw/firmware/ctrl/aecp/aecp.c:5` | Share callback ownership across instances, guard every input, schedule independent retries and form non-AEM responses. |
| `sw/firmware/ctrl/aecp/aecp.h:97` | Expose the ADP observation port and retry state; guarded queries use mutable diagnostic counters. |
| `sw/firmware/ctrl/aecp/aecp_commands.c:33` | Normalize root configuration, report current SET_STREAM_INFO fields, and observe ADP available_index. |
| `sw/firmware/ctrl/aecp/aecp_internal.h:8` | Declare the shared entry and port-boundary helpers. |
| `sw/firmware/ctrl/aecp/aecp_maps.c:276` | Refuse/count synchronous saved-map and settle inputs. |
| `sw/firmware/ctrl/aecp/aecp_mbx.c:94` | Forward available_index without owning or caching ADP state. |
| `sw/firmware/ctrl/aecp/aecp_state.c:38` | Guard restore, latch and defaults inputs. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c:105` | Observe the ingress interface’s real ADP owner. |
| `sw/firmware/ctrl/test/aecp_callback_inputs.hpp:1` | Exercise all 15 public inputs from real callbacks. |
| `sw/firmware/ctrl/test/aecp_mutants.py:35` | Own all 73 named tests with 69 source plants, including ten new plants. |
| `sw/firmware/ctrl/test/aecp_wire.cpp:49` | Add nonzero root configuration and SET flags/refusal transactions. |
| `sw/firmware/ctrl/test/aecp_wire_model.hpp:33` | Supply nonzero stream state to both sides and an explicit ADP observation. |
| `sw/firmware/ctrl/test/aecp_wire_oracle.py:92` | Grade current fields against clauses, preserve descriptor census, and classify exact reference differences. |
| `sw/firmware/ctrl/test/test_aecp.cpp:8` | Add root/current-state/retry/guard/message-type/ADP tests and HDCP service timing. |
| `sw/firmware/ctrl/test/test_aecp_debug.cpp:4` | Assert cross-instance callback refusals for every public input. |
| `sw/firmware/gtest/coverage.ratchet:10` | Regenerate the complete 100% coverage counts through the coverage generator. |

The original lane implementation and earlier evidence are retained in `ROUND1-HANDOFF.md`. The tables here supersede its counts and status. The optional stale F5 notification wording identified by the review is also updated.

## Tests and planted defects

73 unique AECP tests: 47 core, seven saved-state, eight application, four mailbox, three latency, three image and one diagnostic. The composed arm runs 69 at each interface count. All 69 source plants fail their named assertions in completed runs; crashes and compile failures do not count. Exact planting edits are in `round2/mutation-ledger.json`.

| Test and file:line | Planted defect and rejecting assertion |
|---|---|
| `AecpDebug.EveryInputRejectsSynchronousPortDelivery` at `sw/firmware/ctrl/test/test_aecp_debug.cpp:17` | `debug-guard-silent` (died but not with expected exit code) |
| `App.CompositionRefusalsLeaveExistingBindingsIntact` at `sw/firmware/ctrl/test/test_aecp.cpp:494` | `app-poll-space-short` (ctrl_app_compose_aecp) |
| `App.DeferredStartAndLockUseTheRealAcmpOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:415` | `app-start-inverted` (v.started) |
| `App.EntityReadSeesTheRealAdpAdvertisementCount` at `sw/firmware/ctrl/test/test_aecp.cpp:388` | `entity-available-index-static` (ENTITY sees N advertisements from the ADP owner) |
| `App.ExpiredAndMissingStartRequestsCannotApplyLate` at `sw/firmware/ctrl/test/test_aecp.cpp:511` | `app-expired-start-applies` (sinks[0].started) |
| `App.InputInfoReflectsAcmpSettlementAndFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:472` | `app-failure-flags-lost` (v.flags) |
| `App.MediaUnlockedNoticeCannotPassAnOwedUnbindResponse` at `sw/firmware/ctrl/test/test_aecp.cpp:430` | `app-notice-overtakes-unbind` (response) < (notice) |
| `App.PhysicalObservationsAndAcceptedWritesRetainTheirOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:452` | `app-write-owner-lost` (nvm_store_status()->dirty) |
| `App.UnboundStartAndStopAreSuccessfulNoOps` at `sw/firmware/ctrl/test/test_aecp.cpp:535` | `app-unbound-start-refused` (get(p->bytes+16,2)>>11) |
| `Core.AcceptedDefaultBecomesAnOverrideAndObservationFailureRefusesSet` at `sw/firmware/ctrl/test/test_aecp.cpp:662` | `default-is-not-override` (aecp_value_latch) |
| `Core.BackpressureOrdersResponseBeforeNotice` at `sw/firmware/ctrl/test/test_aecp.cpp:809` | `owed-response-discarded` (sent.size()) |
| `Core.BootMapFaultsCannotPartlyReplaceTheSet` at `sw/firmware/ctrl/test/test_aecp.cpp:1112` | `boot-map-capacity-ignored` (aecp_map_restore) |
| `Core.ChangedScalarValuesAndDamagedLists` at `sw/firmware/ctrl/test/test_aecp.cpp:894` | `clock-reserved-halfword-omitted` (status for command) |
| `Core.ConfigurationAndLockedSetRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:859` | `foreign-lock-ignored` (status for command) |
| `Core.CounterNoticesCoalesceAndWaitForEligibility` at `sw/firmware/ctrl/test/test_aecp.cpp:958` | `counter-spacing-short` (sent.empty()) |
| `Core.CounterTimerArmsOnlyEligibleCompletedSnapshots` at `sw/firmware/ctrl/test/test_aecp.cpp:1182` | `counter-timer-during-output` (Unexpected mock function call); `retry-timer-lost` (Unexpected mock function call) |
| `Core.CrossInstanceInputsAreRefusedInsideRealCallbacks` at `sw/firmware/ctrl/test/test_aecp.cpp:580` | `cross-instance-guard-removed` (every cross-instance public input counts its refusal) |
| `Core.DescriptorAndObservationBoundaryFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:1354` | `stream-interface-bound-ignored` (status for command) |
| `Core.DynamicInfoSkipsOverflowAndKeepsLaterRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:914` | `dynamic-overflow-kept` (out.size()) |
| `Core.DynamicInfoWhitelistAndIndependentResults` at `sw/firmware/ctrl/test/test_aecp.cpp:835` | `dynamic-unknown-status` (per-record NOT_SUPPORTED) |
| `Core.EntityAvailableIndexUsesTheIngressObservation` at `sw/firmware/ctrl/test/test_aecp.cpp:1257` | `entity-available-index-static` (ENTITY reads current ADP available index) |
| `Core.EveryDescriptorAndReadFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:554` | `descriptor-last-byte` (every READ_DESCRIPTOR is byte exact) |
| `Core.FailedSnapshotRetriesAndUnsupportedEventsAreDiscarded` at `sw/firmware/ctrl/test/test_aecp.cpp:971` | `unsupported-events-queued` (pending) |
| `Core.FramingRejectsInvalidIdentityAndTruncation` at `sw/firmware/ctrl/test/test_aecp.cpp:1149` | `framing-version-ignored` (a.malformed) |
| `Core.GroupNameDoesNotOverwriteFirmwareVersion` at `sw/firmware/ctrl/test/test_aecp.cpp:1325` | `group-name-offset` (group_name changes only) |
| `Core.IdentifyCurrentValueAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:883` | `identify-one-accepted` (status for command) |
| `Core.InitRefusalsAndClosedService` at `sw/firmware/ctrl/test/test_aecp.cpp:1243` | `no-interface-accepted` (aecp_init) |
| `Core.LockQueriesAndExpiry` at `sw/firmware/ctrl/test/test_aecp.cpp:616` | `lock-long` (lock expires at exactly sixty seconds) |
| `Core.MapTopologyFailuresAndEmptyPartitions` at `sw/firmware/ctrl/test/test_aecp.cpp:1071` | `empty-map-no-page` (status for command) |
| `Core.MapsAreAtomicAndPaginated` at `sw/firmware/ctrl/test/test_aecp.cpp:927` | `map-capacity-ignored` (status for command) |
| `Core.MapsCompareEveryCoordinateAndBothDirectionsOnRestore` at `sw/firmware/ctrl/test/test_aecp.cpp:1221` | `map-cluster-channel-ignored` (a distinct cluster channel is a distinct input key) |
| `Core.MetadataConfigurationKeysAndRepeatedOverrides` at `sw/firmware/ctrl/test/test_aecp.cpp:1204` | `descriptor-configuration-ignored` (status for command) |
| `Core.MilanVendorCommandsAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1303` | `system-id-write-lost` (get(out,46,8)) |
| `Core.NameRefusalsAndNoOp` at `sw/firmware/ctrl/test/test_aecp.cpp:873` | `extra-name-accepted` (status for command) |
| `Core.NamesAndDescriptorOverlay` at `sw/firmware/ctrl/test/test_aecp.cpp:631` | `group-name-offset` (READ_DESCRIPTOR uses the same name) |
| `Core.NonAemMessageTypesFollowTheirOwnContracts` at `sw/firmware/ctrl/test/test_aecp.cpp:1267` | `hdcp-data-length-echo` (HDCP refusal clears data length) |
| `Core.NotificationBackpressureAndLatestCompletion` at `sw/firmware/ctrl/test/test_aecp.cpp:1334` | `completion-cookie-ignored` (an old completion cannot release a newer copy) |
| `Core.ObservationRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:758` | `path-failure-success` (status for command) |
| `Core.ObservationsHaveFullWireForms` at `sw/firmware/ctrl/test/test_aecp.cpp:740` | `counter-last-word` (coherent bank includes every counter) |
| `Core.OutputMappingsHaveOneGlobalOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:1042` | `output-owner-crossed` (another port already owns this stream channel) |
| `Core.OutputPartitionGeometryUsesAllAdvertisedWidths` at `sw/firmware/ctrl/test/test_aecp.cpp:1094` | `empty-map-no-page` (status for command) |
| `Core.ProbeIdentityAndSequenceMustBothMatch` at `sw/firmware/ctrl/test/test_aecp.cpp:1171` | `probe-sequence-ignored` (probing) |
| `Core.ProbeRepliesResetOnlyTheirOwnInterface` at `sw/firmware/ctrl/test/test_aecp.cpp:1137` | `probe-status-matters` (probing) |
| `Core.ReentrantPortsCannotMutateState` at `sw/firmware/ctrl/test/test_aecp.cpp:1161` | `reentry-uncounted` (a.reentries) |
| `Core.RegistryCapacityInterfaceKeysAndLiveness` at `sw/firmware/ctrl/test/test_aecp.cpp:846` | `registry-no-retry` (sent.size()) |
| `Core.RestoreMapWholeSetClipAndDefaults` at `sw/firmware/ctrl/test/test_aecp.cpp:712` | `boot-clip-boundary` (m.count) |
| `Core.RestoreValuesValidateAndRollbackWithoutLiveEvents` at `sw/firmware/ctrl/test/test_aecp.cpp:678` | `restore-forgets-override` (aecp_value_latch) |
| `Core.RootDescriptorConfigurationIsIgnored` at `sw/firmware/ctrl/test/test_aecp.cpp:565` | `root-configuration-refused` (root descriptor ignores received configuration) |
| `Core.SavedValuesRejectWrongFieldsAndDamagedDescriptors` at `sw/firmware/ctrl/test/test_aecp.cpp:1054` | `saved-latency-wrong-type` (aecp_value_restore) |
| `Core.ScalarGetSetAndCurrentValueRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:647` | `scalar-refusal-reports-request` (refused SET reports current value) |
| `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` at `sw/firmware/ctrl/test/test_aecp.cpp:778` | `stream-info-flags-echo` (SET response flags describe current state); `stream-info-noop-refused` (status for command); `stream-info-request-echo` (SET response uses current format) |
| `Core.StartIsDeferredAndHasFailureDeadline` at `sw/firmware/ctrl/test/test_aecp.cpp:821` | `start-wait-ten-ms` (sent.size()) |
| `Core.StaticMapsPreventOrphaningFormats` at `sw/firmware/ctrl/test/test_aecp.cpp:1021` | `static-map-orphan-accepted` (status for command) |
| `Core.StreamInfoDirectionFlagsAndLatency` at `sw/firmware/ctrl/test/test_aecp.cpp:768` | `latency-sign-accepted` (status for command) |
| `Core.UnavailableSnapshotsDoNotBlockIndependentNoticesOrSpin` at `sw/firmware/ctrl/test/test_aecp.cpp:985` | `unavailable-head-blocks-notices` (backpressure retains the built independent snapshot); `unavailable-retry-spins` (failed snapshots wait for a timed retry) |
| `Core.UnsupportedAndAcquire` at `sw/firmware/ctrl/test/test_aecp.cpp:601` | `identify-refusal-body-lost` (identify refusal preserves descriptor fields); `unknown-body-lost` (unsupported command echoes its exact body) |
| `Image.EveryDescriptor` at `sw/firmware/ctrl/test/test_aecp_image.cpp:51` | `image-byte-corrupted` (descriptor defaults survive the image load) |
| `Image.RejectDirectory` at `sw/firmware/ctrl/test/test_aecp_image.cpp:90` | `image-type-ignored` (invalid descriptor directory is refused at its boundary) |
| `Image.RejectHeader` at `sw/firmware/ctrl/test/test_aecp_image.cpp:69` | `image-crc-ignored` (image CRC rejects corrupted descriptor bytes) |
| `Latency.DeferredFailureAndTimerPathsUseTheirDueTime` at `sw/firmware/ctrl/test/test_aecp.cpp:1553` | `start-wait-ten-ms` (commits.size()) |
| `Latency.EveryCommandAndRefusalUsesOneArrivalBudget` at `sw/firmware/ctrl/test/test_aecp.cpp:1474` | `latency-response-missing` (commits.size()) |
| `Latency.NotificationFanoutAndStallsRetainTheirOriginalOrigin` at `sw/firmware/ctrl/test/test_aecp.cpp:1533` | `latency-budget-relaxed` (late output cannot restart the service clock) |
| `Mailbox.EveryInterfaceAndObservationPort` at `sw/firmware/ctrl/test/test_aecp.cpp:1389` | `mailbox-interface-crossed` (fabric.tx_sent) |
| `Mailbox.FullTransmitRingAndCompletionQueueKeepTheirOwedResponse` at `sw/firmware/ctrl/test/test_aecp.cpp:1437` | `mailbox-full-completions-overwritten` (adapter.ports.send) |
| `Mailbox.OutputTailStartsCounterSpacingAfterAStall` at `sw/firmware/ctrl/test/test_aecp.cpp:1405` | `counter-spacing-short` (fabric.tx_sent) |
| `Mailbox.TimerIdentityAndAttachRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1420` | `mailbox-stale-tag-accepted` (adapter.stale_expiries) |
| `Nvm.AbsentMapClipsButRefusedMapRevertsItsFormat` at `sw/firmware/ctrl/test/test_aecp.cpp:250` | `boot-clip-boundary` (m.count) |
| `Nvm.AcceptedStateSurvivesTheRealStorePowerCycle` at `sw/firmware/ctrl/test/test_aecp.cpp:227` | `nvm-latency-dirty-lost` (owner.port.latch) |
| `Nvm.EveryChangeQueuesOnlyItsOwnedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:311` | `nvm-latency-dirty-lost` (owner.pending) |
| `Nvm.MapRecordsRefuseMissingStorageAndNeverPartiallyLatch` at `sw/firmware/ctrl/test/test_aecp.cpp:293` | `nvm-partial-latch-writes` (owner.port.latch) |
| `Nvm.ScalarRecordsUseSharedValidationAndReserveUnknownGroups` at `sw/firmware/ctrl/test/test_aecp.cpp:269` | `restore-forgets-override` (owner.port.latch) |
| `Nvm.ShapePoolsAndNameOrdinalsMatchSavedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:193` | `group-name-offset` (b) |
| `Nvm.WholeMapFramingAndEmptySetAreDistinct` at `sw/firmware/ctrl/test/test_aecp.cpp:208` | `nvm-hole-accepted` (owner.port.apply) |


All 12 unchanged review probes pass. Their source hashes are in `round2/review-probe-inventory.json`; sources match the evidence branch. P5’s diagnostic string remains historical and unchanged; the new application test supplies the available-index proof.

## Coverage

The full coverage generator executed both firmware banks and recorded all 30 production files. All eight AECP/application units have raw 100% lines and branches. No exclusion was added or changed. The final check of the regenerated ratchet returned 0 across all 30 files.

| File | Raw lines | Raw branches | Exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 | none |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 | none |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 | none |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 | none |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 | none |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 | none |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 | none |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 | none |

## Gate table

Exact commands and prerequisites: `ROUND2-REPRODUCE.md`. All commands run in the foreground with bounded timeouts; no gate output is piped.

| Gate | Result and evidence |
|---|---|
| Firmware bank, RV32 required | PASS: 59 named arms, 65 tallies, 1406 checks, zero failures. |
| Unchanged review probes | PASS: 12/12. |
| AECP source plants | PASS: 69/69, two complete partitions. |
| Coverage generator | PASS: generator and final check; 30 files, eight new units raw 100%. |
| Coverage/tally/RV32 grader self-tests | PASS. |
| Sanitizers | PASS: 69 tests at one interface and 69 at two. |
| Wire differential | PASS: 132 records at one interface; 137 on each two-interface ingress; six oracle controls per ingress. |
| Default mailbox target | PASS: both buses, firmware co-simulation, two interfaces and five quick plants. |
| Mailbox generation check | PASS. |
| Builder bank | PASS: all four ordinary and all four profile partitions; exact fixture-table union verified. |
| Documentation workflow | PASS: all 73 commands; em-dash and final style checks PASS. |
| Four linked images | PASS: ABI/runtime checks and all spans under 224 KB. |
| Physical timing/calibration | NOT RUN: hardware access is outside the assignment. |
| Hosted checks and local replica after push | Owed on publication; this session is not authorized to push. |
| Independent re-review/merge validation | Owed; no review verdict is claimed. |

Initial diagnostic failures were corrected: root-read padding/census predicates, the old AA-ignore assertion, a capture-ring cursor in the new advertisement test, a missing standalone C++ include, a macro/braces warning, a long Python line, README contents, two untested timer choices, and the moved descriptor plant. The first HDL-reference docs attempt lacked its pinned parser on the module path; the recorded dependency path fixed that setup. Failed attempts are not counted as gate passes.

## Wire decisions

The independent oracle grades 42 descriptors, 31 AEM command codes, three MVU commands and 17 notification command types on each ingress. The unchanged references are `2ad2f845dd583f8310075fa2380cb60a04fd091a` (one interface) and `c9f74b6866a63dd3c0e4534724bfc07a86ad142b` (two). Reference inventories and verdicts are in `round2/wire-*-*.json`.

| Difference | Records per ingress | Clause |
|---|---:|---|
| Root descriptor configuration normalization | 4 | IEEE 7.4.5.1/.2 |
| Current SET_STREAM_INFO response and flag decisions | 7 | IEEE 7.4.15.1; Milan 5.4.2.9 |
| System unique ID support | 2 | Milan 5.4.4.2/.3 |
| Saved-default override notification | 3 | Milan 5.4.5.2 |
| Started-state GET_STREAM_INFO notice | 2 | Milan Table 5.22 |
| Permitted unlock flag alternatives | 3 | IEEE 7.4.2.1 |

The contract additionally records HDCP empty-data responses versus reference echoes, ignored reserved/extended types versus reference replies, and dynamic available_index versus the reference image constant. The wire fixture supplies zero ADP advertisements on both sides; the composed application independently proves the dynamic count. The two-interface reference exposes ingress but no physical egress-index signal; its wire counts establish registry isolation, while the core separately checks its egress index.

## Linked images

All numbers are bytes. Spans include alignment and the 8192-byte stack reservation; static pools are included in data/bss. `round2/size-matrix.json` records every static pool plus artifact size/SHA-256, baseline sections, and both deltas. The baseline uses the unchanged F4 input units from `5603c353` and the same runtime archives.

| Shape | Interfaces | Text | Rodata | Data | Bss | RAM span | Delta from base | Round 2 delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 82932 | 11950 | 56 | 37252 | 140400 | +60032 | +1328 |
| 1x1_tdm8 | 2 | 84220 | 11950 | 56 | 48620 | 153056 | +60032 | +1328 |
| 8x8 | 1 | 82980 | 25158 | 448 | 77428 | 194224 | +99056 | +1984 |
| 8x8 | 2 | 84356 | 25158 | 448 | 103556 | 221728 | +99056 | +1984 |

The 221728-byte maximum leaves 2272 bytes below a conservative decimal 224000-byte ceiling. The opt-in fixture is RV32I/ILP32 with retained boot/service paths and no hosted runtime. Routed memory fit, board calibration and complete call-chain stack bounds remain integration obligations.

## Scope and publication

The default all-fabric build, shipping image, product configurations, RTL and register maps are unchanged from the lane base. No push, PR mutation, merge, rebase, amendment, hardware access or flashing occurred. Processor #73 still owes the common command model; #69 supplies the interface seam. The only permitted final publication is a new REVIEW READY or STOP comment on issue #665.

The observed service-unit memory peak is 7495839744 bytes, below 9 GB. Simulation builds were limited to two concurrently, eight compile jobs per build, and campaign workers to four. The mailbox quick campaign used two build workers. Logs larger than 200 KB remain in scratch; this packet records hashes and sizes instead. No generated tree, binary, runtime, package or toolchain is stored here.

Builder profile union: 38 accepted_cases.items(), 4 accepted_makefiles.items(), 359 mutations, 43 disconnected identity controls. Every partition returned 0 with no non-executed arm.

Final containment: tracked and untracked status is clean. Generated ROMs, parser cache and builder outputs were moved to scratch after all gates finished. All foreground gate processes completed. The final issue publication is REVIEW READY for the stated unpushed head; PR #700 remains at `1e68d1b62ef2facdf0e8dbad28a202297d433c61`.

