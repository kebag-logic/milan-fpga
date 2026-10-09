# F5 handoff

[A572] implementation head `1e68d1b62ef2facdf0e8dbad28a202297d433c61`; branch `665-f5-aecp`, base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

Implementation and local verification are complete at the stated head. All required command families return 0; the existing physical calibration arm is explicitly NOT RUN. Independent review and publication are still owed. This document supersedes the earlier 128 KB preflight STOP. `STOP.md`, `evidence.json`, `integrity.json`, `link-receipts.json` and the old preflight scripts preserve that historical measurement only.

## Authority and scope

Assignment: issue #665 comment 6081266905. Resumption and 224 KB threshold: comment 6081705916. The full cited issues #664, #678, #697, #653 and #637 and processor #69/#73 were read. Repository workflow, documentation index, REQUIREMENTS section 1, FR_NFR NFR-SCOUT-02/03/08, MAILBOX_SPLIT, mailbox interface index, existing core/adapter/application patterns, AEM generators and processor AECP tests were the entry points. Standards citations refer to IEEE 1722.1-2021 and Milan v1.2; no standards text is reproduced.

Executor [A572]; assigned independent internal reviewer [R564], external reviewer [R565]. This packet is evidence, not a review verdict or completion ledger. Processor #73 remains open; adoption of its future single command model is owed. Processor #69 is merged and supplies the ingress-interface seam.

The default all-fabric build, shipping image, product configurations, RTL and register maps are unchanged. No non-AECP storage reduction was implemented. No push, PR mutation, merge, hardware access or flashing occurred. The linked composition is an opt-in size/ABI fixture, not a board image.

## Changes

| File:line at the head | Behavior |
|---|---|
| `docs/README.md:74` | Index the AECP ownership and verification contract. |
| `sw/firmware/ctrl/README.md:1` | Describe the opt-in AECP owner and link its contract. |
| `sw/firmware/ctrl/aecp/README.md:9` | Document APIs, boot order, interface ownership, saved state, wire differences and measurement limits. |
| `sw/firmware/ctrl/aecp/aecp.c:1` | Own frame validation, responses, registration/liveness, locks, notifications, completion spacing and reentry guards. |
| `sw/firmware/ctrl/aecp/aecp.h:78` | Portable typed environment ports, caller-owned storage and lifecycle API; no synchronous callback delivery. |
| `sw/firmware/ctrl/aecp/aecp_commands.c:1` | Implement mandatory AEM/MVU handlers, descriptor overlays and exact refusal bodies. |
| `sw/firmware/ctrl/aecp/aecp_entity.py:1` | Generate the core image and capacities through the existing AEM generators. |
| `sw/firmware/ctrl/aecp/aecp_image.c:1` | Validate CRC, directory bounds and unique keys before atomically exposing descriptor spans. |
| `sw/firmware/ctrl/aecp/aecp_image.h:1` | Separate image validation from the protocol owner. |
| `sw/firmware/ctrl/aecp/aecp_internal.h:1` | Private handler/map helpers shared by the portable units. |
| `sw/firmware/ctrl/aecp/aecp_maps.c:1` | Atomic map edits/restores, fixed pagination, global output ownership and format rollback. |
| `sw/firmware/ctrl/aecp/aecp_mbx.c:1` | AECP channel attachment, interface routing, timer service and final-word TX completion cookies. |
| `sw/firmware/ctrl/aecp/aecp_mbx.h:1` | Mailbox adapter state with bounded outstanding completions. |
| `sw/firmware/ctrl/aecp/aecp_model.h:1` | Storage-independent descriptor model. |
| `sw/firmware/ctrl/aecp/aecp_nvm.c:1` | Bind scalar/map groups to the real saved-state store and defer dirty-record work. |
| `sw/firmware/ctrl/aecp/aecp_nvm.h:1` | Saved-state adapter lifecycle and queued record state. |
| `sw/firmware/ctrl/aecp/aecp_shape.py:1` | Derive name ordinals, maps, identity defaults and pool sizes from generated descriptors. |
| `sw/firmware/ctrl/aecp/aecp_state.c:1` | Share live validation with boot restore; settle map/format compatibility and overrides. |
| `sw/firmware/ctrl/aecp/aecp_state.h:1` | Boot restore, latch and settle interface. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c:105` | Compose with ACMP/SRP, deferred START/STOP, saved state and response-before-MEDIA_UNLOCKED ordering. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.h:1` | Opt-in application bridge without replacing the default entry point. |
| `sw/firmware/ctrl/test/aecp_arms.py:1` | Build/run image, portable core, mailbox, application, sanitizer and diagnostic arms. |
| `sw/firmware/ctrl/test/aecp_latency_policy.hpp:1` | Explicit desk timing allowances and 10 ms/240 ms limits. |
| `sw/firmware/ctrl/test/aecp_mutants.py:1` | 59 exact source plants; require completed failures in each named assertion and audit test ownership. |
| `sw/firmware/ctrl/test/aecp_wire.cpp:1` | Feed paired core/fabric command, descriptor and notification transactions. |
| `sw/firmware/ctrl/test/aecp_wire.py:1` | Fingerprint unchanged reference sources, adapt only external bench providers, rebuild and independently grade wire logs. |
| `sw/firmware/ctrl/test/aecp_wire_model.hpp:1` | Core environment and canonical shape transactions for the differential. |
| `sw/firmware/ctrl/test/aecp_wire_oracle.py:1` | Standards-based wire grading, exact difference predicates and six observation controls. |
| `sw/firmware/ctrl/test/aecp_wire_timers.hpp:1` | Controller liveness, lock expiry and two-interface registration isolation on the wire. |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c:80` | Reachable F0-F5 plus F1 link fixture, real boot restore and service, explicit unavailable physical observers. |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:33` | Optional --with-aecp link arm, required retained symbols, separate sections and static pools. |
| `sw/firmware/ctrl/test/test_aecp.cpp:189` | 62 self-checking core, saved-state, application, mailbox and service-budget tests. |
| `sw/firmware/ctrl/test/test_aecp_debug.cpp:16` | Assert the no-synchronous-callback contract for every input entry point. |
| `sw/firmware/ctrl/test/test_aecp_image.cpp:51` | Three image tests covering all descriptors and hostile header/directory boundaries. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:1` | Add the AECP one/two-interface and all-shape arms plus source-plant campaign to the normal bank. |
| `sw/firmware/gtest/coverage.ratchet:10` | Generator-recorded 100% lines/branches for all eight new production C units; no exclusion. |

## Acceptance evidence

Every descriptor in the generated shape is served from validated image spans (IEEE 7.4.5). AEM covers the mandatory Milan 5.4 set, including locks/acquisition refusal, configuration/name/scalars, stream info, maps, observations, counters, dynamic info, registration and START/STOP. MVU covers Milan information and system unique ID. Unknown commands return NOT_IMPLEMENTED; solicited IDENTIFY_NOTIFICATION returns the required BAD_ARGUMENTS and preserves its descriptor fields (IEEE 7.4.39.2).

Interface-specific registration, liveness, source MAC and egress state remain separate. Entity-wide values and locks remain shared. Typed observation ports receive the descriptor interface. Reentry is asserted in the diagnostic build and refused/counted in the normal build. START/STOP is queued and delivered on a later loop pass; expiration prevents late application.

The application test holds an UNBIND_RX response behind a full ACMP TX ring and proves that its MEDIA_UNLOCKED counters notice cannot overtake it (#653). Saved scalars use live validators; maps restore atomically, absent maps clip identity defaults, and refused maps retain defaults and roll back incompatible restored formats (#637 and #658 ruling). Accepted default-valued SETs establish saved overrides. Reserved system-ID/media-clock-reference saved spans remain erased; system unique ID is volatile pending its record-format decision.

## Test-to-defect ledger

66 named AECP tests: 41 core, seven saved-state, seven application, four mailbox, three latency, three image and one diagnostic test. All 59 source plants were caught by their named assertions. Crashes, a wrong-test failure, missing assertion words and a passing run cannot count as a caught plant. The following table is the complete per-test mapping; exact before/after source seams are in `mutation-ledger.json`.

| Test and source | Planted defect and required assertion | Result |
|---|---|---|
| `AecpDebug.EveryInputRejectsSynchronousPortDelivery` at `sw/firmware/ctrl/test/test_aecp_debug.cpp:16` | `debug-guard-silent` (died but not with expected exit code) | caught |
| `App.CompositionRefusalsLeaveExistingBindingsIntact` at `sw/firmware/ctrl/test/test_aecp.cpp:463` | `app-poll-space-short` (ctrl_app_compose_aecp) | caught |
| `App.DeferredStartAndLockUseTheRealAcmpOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:384` | `app-start-inverted` (v.started) | caught |
| `App.ExpiredAndMissingStartRequestsCannotApplyLate` at `sw/firmware/ctrl/test/test_aecp.cpp:480` | `app-expired-start-applies` (sinks[0].started) | caught |
| `App.InputInfoReflectsAcmpSettlementAndFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:441` | `app-failure-flags-lost` (v.flags) | caught |
| `App.MediaUnlockedNoticeCannotPassAnOwedUnbindResponse` at `sw/firmware/ctrl/test/test_aecp.cpp:399` | `app-notice-overtakes-unbind` (response) < (notice) | caught |
| `App.PhysicalObservationsAndAcceptedWritesRetainTheirOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:421` | `app-write-owner-lost` (nvm_store_status()->dirty) | caught |
| `App.UnboundStartAndStopAreSuccessfulNoOps` at `sw/firmware/ctrl/test/test_aecp.cpp:504` | `app-unbound-start-refused` (get(p->bytes+16,2)>>11) | caught |
| `Core.AcceptedDefaultBecomesAnOverrideAndObservationFailureRefusesSet` at `sw/firmware/ctrl/test/test_aecp.cpp:595` | `default-is-not-override` (aecp_value_latch) | caught |
| `Core.BackpressureOrdersResponseBeforeNotice` at `sw/firmware/ctrl/test/test_aecp.cpp:711` | `owed-response-discarded` (sent.size()) | caught |
| `Core.BootMapFaultsCannotPartlyReplaceTheSet` at `sw/firmware/ctrl/test/test_aecp.cpp:978` | `boot-map-capacity-ignored` (aecp_map_restore) | caught |
| `Core.ChangedScalarValuesAndDamagedLists` at `sw/firmware/ctrl/test/test_aecp.cpp:796` | `clock-reserved-halfword-omitted` (status for command) | caught |
| `Core.ConfigurationAndLockedSetRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:761` | `foreign-lock-ignored` (status for command) | caught |
| `Core.CounterNoticesCoalesceAndWaitForEligibility` at `sw/firmware/ctrl/test/test_aecp.cpp:860` | `counter-spacing-short` (sent.empty()) | caught |
| `Core.CounterTimerArmsOnlyEligibleCompletedSnapshots` at `sw/firmware/ctrl/test/test_aecp.cpp:1048` | `counter-timer-during-output` (Unexpected mock function call) | caught |
| `Core.DescriptorAndObservationBoundaryFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:1165` | `stream-interface-bound-ignored` (status for command) | caught |
| `Core.DynamicInfoSkipsOverflowAndKeepsLaterRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:816` | `dynamic-overflow-kept` (out.size()) | caught |
| `Core.DynamicInfoWhitelistAndIndependentResults` at `sw/firmware/ctrl/test/test_aecp.cpp:737` | `dynamic-unknown-status` (per-record NOT_SUPPORTED) | caught |
| `Core.EveryDescriptorAndReadFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:523` | `descriptor-last-byte` (every READ_DESCRIPTOR is byte exact) | caught |
| `Core.FailedSnapshotRetriesAndUnsupportedEventsAreDiscarded` at `sw/firmware/ctrl/test/test_aecp.cpp:873` | `unsupported-events-queued` (pending) | caught |
| `Core.FramingRejectsInvalidIdentityAndTruncation` at `sw/firmware/ctrl/test/test_aecp.cpp:1015` | `framing-version-ignored` (a.malformed) | caught |
| `Core.GroupNameDoesNotOverwriteFirmwareVersion` at `sw/firmware/ctrl/test/test_aecp.cpp:1136` | `group-name-offset` (group_name changes only) | caught |
| `Core.IdentifyCurrentValueAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:785` | `identify-one-accepted` (status for command) | caught |
| `Core.InitRefusalsAndClosedService` at `sw/firmware/ctrl/test/test_aecp.cpp:1100` | `no-interface-accepted` (aecp_init) | caught |
| `Core.LockQueriesAndExpiry` at `sw/firmware/ctrl/test/test_aecp.cpp:549` | `lock-long` (lock expires at exactly sixty seconds) | caught |
| `Core.MapTopologyFailuresAndEmptyPartitions` at `sw/firmware/ctrl/test/test_aecp.cpp:937` | `empty-map-no-page` (status for command) | caught |
| `Core.MapsAreAtomicAndPaginated` at `sw/firmware/ctrl/test/test_aecp.cpp:829` | `map-capacity-ignored` (status for command) | caught |
| `Core.MapsCompareEveryCoordinateAndBothDirectionsOnRestore` at `sw/firmware/ctrl/test/test_aecp.cpp:1078` | `map-cluster-channel-ignored` (a distinct cluster channel is a distinct input key) | caught |
| `Core.MetadataConfigurationKeysAndRepeatedOverrides` at `sw/firmware/ctrl/test/test_aecp.cpp:1061` | `descriptor-configuration-ignored` (status for command) | caught |
| `Core.MilanVendorCommandsAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1114` | `system-id-write-lost` (get(out,46,8)) | caught |
| `Core.NameRefusalsAndNoOp` at `sw/firmware/ctrl/test/test_aecp.cpp:775` | `extra-name-accepted` (status for command) | caught |
| `Core.NamesAndDescriptorOverlay` at `sw/firmware/ctrl/test/test_aecp.cpp:564` | `group-name-offset` (READ_DESCRIPTOR uses the same name) | caught |
| `Core.NotificationBackpressureAndLatestCompletion` at `sw/firmware/ctrl/test/test_aecp.cpp:1145` | `completion-cookie-ignored` (an old completion cannot release a newer copy) | caught |
| `Core.ObservationRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:691` | `path-failure-success` (status for command) | caught |
| `Core.ObservationsHaveFullWireForms` at `sw/firmware/ctrl/test/test_aecp.cpp:673` | `counter-last-word` (coherent bank includes every counter) | caught |
| `Core.OutputMappingsHaveOneGlobalOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:908` | `output-owner-crossed` (another port already owns this stream channel) | caught |
| `Core.OutputPartitionGeometryUsesAllAdvertisedWidths` at `sw/firmware/ctrl/test/test_aecp.cpp:960` | `empty-map-no-page` (status for command) | caught |
| `Core.ProbeIdentityAndSequenceMustBothMatch` at `sw/firmware/ctrl/test/test_aecp.cpp:1037` | `probe-sequence-ignored` (probing) | caught |
| `Core.ProbeRepliesResetOnlyTheirOwnInterface` at `sw/firmware/ctrl/test/test_aecp.cpp:1003` | `probe-status-matters` (probing) | caught |
| `Core.ReentrantPortsCannotMutateState` at `sw/firmware/ctrl/test/test_aecp.cpp:1027` | `reentry-uncounted` (a.reentries) | caught |
| `Core.RegistryCapacityInterfaceKeysAndLiveness` at `sw/firmware/ctrl/test/test_aecp.cpp:748` | `registry-no-retry` (sent.size()) | caught |
| `Core.RestoreMapWholeSetClipAndDefaults` at `sw/firmware/ctrl/test/test_aecp.cpp:645` | `boot-clip-boundary` (m.count) | caught |
| `Core.RestoreValuesValidateAndRollbackWithoutLiveEvents` at `sw/firmware/ctrl/test/test_aecp.cpp:611` | `restore-forgets-override` (aecp_value_latch) | caught |
| `Core.SavedValuesRejectWrongFieldsAndDamagedDescriptors` at `sw/firmware/ctrl/test/test_aecp.cpp:920` | `saved-latency-wrong-type` (aecp_value_restore) | caught |
| `Core.ScalarGetSetAndCurrentValueRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:580` | `scalar-refusal-reports-request` (refused SET reports current value) | caught |
| `Core.StartIsDeferredAndHasFailureDeadline` at `sw/firmware/ctrl/test/test_aecp.cpp:723` | `start-wait-ten-ms` (sent.size()) | caught |
| `Core.StaticMapsPreventOrphaningFormats` at `sw/firmware/ctrl/test/test_aecp.cpp:887` | `static-map-orphan-accepted` (status for command) | caught |
| `Core.StreamInfoDirectionFlagsAndLatency` at `sw/firmware/ctrl/test/test_aecp.cpp:701` | `latency-sign-accepted` (status for command) | caught |
| `Core.UnsupportedAndAcquire` at `sw/firmware/ctrl/test/test_aecp.cpp:534` | `identify-refusal-body-lost` (identify refusal preserves descriptor fields); `unknown-body-lost` (unsupported command echoes its exact body) | caught |
| `Image.EveryDescriptor` at `sw/firmware/ctrl/test/test_aecp_image.cpp:51` | `image-byte-corrupted` (descriptor defaults survive the image load) | caught |
| `Image.RejectDirectory` at `sw/firmware/ctrl/test/test_aecp_image.cpp:90` | `image-type-ignored` (invalid descriptor directory is refused at its boundary) | caught |
| `Image.RejectHeader` at `sw/firmware/ctrl/test/test_aecp_image.cpp:69` | `image-crc-ignored` (image CRC rejects corrupted descriptor bytes) | caught |
| `Latency.DeferredFailureAndTimerPathsUseTheirDueTime` at `sw/firmware/ctrl/test/test_aecp.cpp:1356` | `start-wait-ten-ms` (commits.size()) | caught |
| `Latency.EveryCommandAndRefusalUsesOneArrivalBudget` at `sw/firmware/ctrl/test/test_aecp.cpp:1285` | `latency-response-missing` (commits.size()) | caught |
| `Latency.NotificationFanoutAndStallsRetainTheirOriginalOrigin` at `sw/firmware/ctrl/test/test_aecp.cpp:1336` | `latency-budget-relaxed` (late output cannot restart the service clock) | caught |
| `Mailbox.EveryInterfaceAndObservationPort` at `sw/firmware/ctrl/test/test_aecp.cpp:1200` | `mailbox-interface-crossed` (fabric.tx_sent) | caught |
| `Mailbox.FullTransmitRingAndCompletionQueueKeepTheirOwedResponse` at `sw/firmware/ctrl/test/test_aecp.cpp:1248` | `mailbox-full-completions-overwritten` (adapter.ports.send) | caught |
| `Mailbox.OutputTailStartsCounterSpacingAfterAStall` at `sw/firmware/ctrl/test/test_aecp.cpp:1216` | `counter-spacing-short` (fabric.tx_sent) | caught |
| `Mailbox.TimerIdentityAndAttachRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1231` | `mailbox-stale-tag-accepted` (adapter.stale_expiries) | caught |
| `Nvm.AbsentMapClipsButRefusedMapRevertsItsFormat` at `sw/firmware/ctrl/test/test_aecp.cpp:246` | `boot-clip-boundary` (m.count) | caught |
| `Nvm.AcceptedStateSurvivesTheRealStorePowerCycle` at `sw/firmware/ctrl/test/test_aecp.cpp:223` | `nvm-latency-dirty-lost` (owner.port.latch) | caught |
| `Nvm.EveryChangeQueuesOnlyItsOwnedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:307` | `nvm-latency-dirty-lost` (owner.pending) | caught |
| `Nvm.MapRecordsRefuseMissingStorageAndNeverPartiallyLatch` at `sw/firmware/ctrl/test/test_aecp.cpp:289` | `nvm-partial-latch-writes` (owner.port.latch) | caught |
| `Nvm.ScalarRecordsUseSharedValidationAndReserveUnknownGroups` at `sw/firmware/ctrl/test/test_aecp.cpp:265` | `restore-forgets-override` (owner.port.latch) | caught |
| `Nvm.ShapePoolsAndNameOrdinalsMatchSavedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:189` | `group-name-offset` (b) | caught |
| `Nvm.WholeMapFramingAndEmptySetAreDistinct` at `sw/firmware/ctrl/test/test_aecp.cpp:204` | `nvm-hole-accepted` (owner.port.apply) | caught |

## Coverage

The full firmware coverage generator and check return 0 across 30 production files. The eight new files have raw 100% lines and branches; no new exclusion was added. Existing F1 exclusions are unchanged. The final test-only maximum-body strengthening does not change production coverage.

| File | Lines | Branches | Exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/aecp/aecp.c` | 324/324` | 266/266 | none |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 402/402` | 350/350 | none |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77` | 80/80 | none |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222` | 290/290 | none |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 98/98` | 40/40 | none |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102` | 86/86 | none |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 62/62` | 67/67 | none |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 104/104` | 64/64 | none |

## Wire differential

One-interface reference `2ad2f845dd583f8310075fa2380cb60a04fd091a`: 123 observations. Two-interface reference (processor #69) `c9f74b6866a63dd3c0e4534724bfc07a86ad142b`: 128 observations on each ingress. Each covers 42 descriptors, 31 AEM command codes including refusal probes, three MVU commands and 17 notification command types. Timers cover controller probes/retry/departure and lock expiry. Six observation plants per ingress reject missing records, altered payloads, lengths, status, sequences and extra frames.

Reference RTL is unchanged. The external observation/format/map providers use the generated canonical shape; the verification-only configuration adds a second declared sampling rate. The wrapper name capacity follows the shape. Sequences are checked per controller before payload comparison. The two-interface wrapper exposes ingress but no egress index: its count proves registration isolation; the core assertion separately proves its egress index. This is not physical dual-port validation.

| Difference observed on each ingress | Count | Clause and disposition |
|---|---:|---|
| Fabric refuses SET/GET_SYSTEM_UNIQUE_ID; core succeeds | 2 | Milan 5.4.4.2/3 requires both |
| First default-valued format/rate SET notifies only in core | 3 | Milan 5.4.5.2: accepted persistent override intent changes state; repeated identical SETs do not notify again |
| Bound START/STOP also produces GET_STREAM_INFO only in core | 2 | Milan 5.4.5.2 Table 5.22; both emit the IEEE 7.5.2 command notification |
| Unlock notification flag is 1 in core and 0 in fabric; owner is zero in both | 3 | IEEE 7.4.2.1 permits both flag alternatives |

No other difference is allowed. `wire-verdicts.json` records the graded observations; source fingerprints and wire log hashes are in the artifact manifest.

## Service latency

The service endpoint is response acceptance by TX_HEAD. Tests count MMIO accesses from the original arrival/due time and add 100 ns per access/observation plus a fixed 1 ms CPU allowance. They exercise both interfaces, every descriptor and command/refusal, maximum AS-path (64 identities), maximum map edit (176 rows), maximum dynamic-info response (512 bytes), maximum unknown-command body (1476 bytes), full registration fanout, TX stalls, deferred failure, controller probes/retries/departure and lock expiry. Their budgets are IEEE 9.3.2.6 and Milan 5.4.3.4 (240 ms), and NFR-SCOUT-03 (10 ms).

| Path | Maximum desk bound | Limit |
|---|---:|---:|
| Commands/refusals including maximum bodies | 1.0770 ms | 10 ms and 240 ms |
| Full notification fanout | 1.1573 ms | 10 ms |
| One-millisecond transmit stall | 2.0069 ms | 10 ms and 240 ms |
| Deferred START failure from arrival (8 ms deadline) | 9.0061 ms | 10 ms and 240 ms |
| Controller retry/departure or lock expiry from due time | 1.0059 ms | 10 ms; protocol due times retained |

These are explicit desk assumptions, not measured target CPU cycles or an end-to-end physical transmit deadline. Arbitrarily stalled hardware cannot have a finite service guarantee. The separate completion-cookie tests hold counter spacing from the last recipient's final TX_TAIL word, not TX_HEAD acceptance. Target calibration, scheduling margin and complete call-chain stack bounds remain integration obligations.

## Linked image and storage

All values below are bytes. The comparison uses the base F4 composition and final opt-in F0-F5/F1 composition with the same freestanding runtime archives. The delta includes the real F1 store now retained by the composition; it is not presented as pure AECP code size. ELF ABI, no-heap/unresolved-symbol and required-retained-symbol checks return 0 in all four cases. Span includes alignment and the reserved 8192-byte stack. Static pools are already included in BSS; do not add them twice.

| Shape | IF | text | rodata | data | bss | stack | Span | Base span | Delta | RAMB36 at 4608 B | At 4096 B data packing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 81948 | 11950 | 56 | 36908 | 8192 | 139072 | 80368 | 58704 | 31 | 34 |
| 1x1_tdm8 | 2 | 83236 | 11950 | 56 | 48276 | 8192 | 151728 | 93024 | 58704 | 33 | 38 |
| 8x8 | 1 | 81996 | 25158 | 448 | 76428 | 8192 | 192240 | 95168 | 97072 | 42 | 47 |
| 8x8 | 2 | 83372 | 25158 | 448 | 102556 | 8192 | 219744 | 122672 | 97072 | 48 | 54 |

The largest span, 219744 bytes, is below both 224000 and 224 KiB (229376). Its nominal 48 RAMB36 count uses all 36 Kibit per tile. A 32-bit data packing model requires 54; physical packing/routing is not proved here. The later default flip still owes the routed Mark II image, LUT/FF/RAMB36 accounting against NFR-RES-01, firmware in block RAM and the owner's 10% reserve.

| Five largest BSS consumers, largest shape / two interfaces | Bytes | Reduction option, not implemented |
|---|---:|---|
| `image_arena` | 48064 | Audit MRP attribute capacities and per-interface peaks before reducing arena sizing; outside F5 |
| `nvm_stage` | 13264 | Consider streamed record-group staging only after proving the existing atomic restore/commit contract; outside F5 |
| `image_values` | 11753 | Use sparse mutable descriptor overlays instead of a full mutable descriptor copy; requires new alias/bounds and read-overlay proof |
| `image_app` | 9640 | Review fixed frame/queue capacities against outstanding-command and backpressure requirements; outside F5 |
| `image_srp` | 5864 | Audit duplicated SRP state and descriptor-derived capacities before reducing storage; outside F5 |

Other largest-shape pools: mappings 4608, AECP adapter/core 3120, descriptor spans 1984, event state 1488, map scratch 576 bytes. `size-matrix.json` records every reported static pool for all four cases, section sizes and artifact hashes. The 8192-byte stack is a reservation; individual static frame reports do not prove the complete call chain.

Runtime libraries were built from recorded freestanding sources using the 2025.08-1 archive; final fixture objects use the existing RV32 selector (GCC 14.3.0, Buildroot 2026.05). Both are checked as RV32I ILP32 and no hosted libc is linked. A fresh 2025.08-1 SDK install in scratch passes archive/provenance verification; it is not falsely claimed to be the existing selector. `runtime-provenance.json` records source hashes and commands.

## Gates

All partitions were reconciled against the complete original tables with no omission or duplicate. `gate-receipts.json` records commands, exit codes, selections and source fingerprints; `artifact-manifest.json` fingerprints the supporting logs. `REPRODUCE.md` gives exact foreground invocations.

| Gate | Result | Evidence / relevant defect controls |
|---|---|---|
| Mailbox make default target, one/two interfaces, both buses, firmware co-simulation | rc 0 | Five quick plants caught; 369 host-model checks; scratch make driver limits nested builds to two |
| Mailbox generator --check | rc 0 | Generated interface files unchanged |
| Full firmware bank --require-rv32 --jobs 4 | rc 0 | One/two interfaces, five image shapes, diagnostic arm; all declared normal arms |
| AECP source plants | rc 0 | 59/59 caught, every one of 66 tests owned; latest latency plant rerun |
| AECP sanitizer, composed two-interface arm | rc 0 | 62/62 tests |
| Firmware coverage --check and coverage self-test | rc 0 | 30 files; eight new raw 100% units, 28 reader controls |
| Firmware tally / RV32 reader self-tests | rc 0 | 18 / 17 planted controls |
| F0-F4 regression source plants | rc 0 | 471 control, 169 SRP, 68 interface-sensitive SRP plants; two pin controls |
| Saved-state normal bank | rc 0 | Five shapes, 435 tests and RV32 arms |
| Saved-state source plants | rc 0 | All 109 plants selected exactly once; unchanged full test-ownership audit in each partition |
| Builder bank except profile gate | rc 0 | All 100 remaining functions partitioned exactly once; existing physical calibration arm explicitly NOT RUN |
| Builder profile gate with real RV32 selector | rc 0 | Four independent fixture tables partitioned; every other assertion repeats unchanged |
| Builder profile absent-compiler control | rc 0 | Existing audit preserves argv, hides all cross candidates and refuses host firmware compilation |
| Documentation workflow commands | rc 0 | 73 extracted Python commands, plus wire-accountability self-test and no-git export checks |
| Offline local-replica self-test | rc 0 | Disposable job container with read-only candidate, no host socket or forwarded credentials |
| SDK archive installation/provenance | rc 0 | Fresh scratch install from hash-checked pinned archive; existing unreceipted selector not replaced |
| Differential one/two interfaces | rc 0 | 123 + 128 + 128 observations; six observation plants per ingress |
| Four complete linked fixtures | rc 0 | Soft-float RV32I ABI, no heap, required composition symbols, budget |

The initial full profile, absent-compiler and combined saved-state invocations exceeded the 560-second foreground cap (rc 124); those attempts are not passing evidence. Partition drivers select only independent fixture tables or plants, retain all assertions and record each original table and selected slice. Their exact, duplicate-free unions have passed reconciliation. The physical Arty calibration report is absent and remains an explicit existing NOT RUN; hardware access was prohibited.

## Remaining integration and review obligations

Independent review and all five clean review lenses are still owed. No hosted exact-head contexts, ready PR, candidate merge validation or post-merge containment are claimed. Those steps require later authorized publication. Processor #73 command-model adoption, persistent system-ID record semantics, physical observer wiring, target timing/call-chain calibration and routed resource reserve belong to their stated future integration decisions.

All retained large artifacts stay in disk-backed scratch; the packet contains only small documents, recipes and fingerprints. The final manifest records SHA-256 and size rather than copying archives, binaries or tree exports. No generated scratch files are in the worktree. Foreground commands use the ten-minute cap; campaign workers are at most four and wire builds are at most two with eight compile jobs each. Memory was sampled and clean file cache was reclaimed with per-file advice; samples exceeded the requested 9 GB target (highest observed 10.24 GB), so uninterrupted compliance with that target is not claimed. No allocation reduction outside AECP was made.


## Per-path service ledger

The values below retain the original event clock and include the stated desk allowances. Command/refusal rows are the maximum over both valid and malformed requests. Descriptor reads cover every generated descriptor. Numeric paths 256-258 are the three MVU subcommands; 0x8000 plus descriptor type denotes the fanout paths. Exact observations are in `service-latency.json`.

| Test path | Path code | IF1 maximum ms | IF2 maximum ms |
|---|---:|---:|---:|
| DeferredFailureAndTimerPathsUseTheirDueTime | 1 | 1.0059 | 1.0059 |
| DeferredFailureAndTimerPathsUseTheirDueTime | 3 | 1.0031 | 1.0056 |
| DeferredFailureAndTimerPathsUseTheirDueTime | 34 | 9.0061 | 9.0061 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 0 | 1.0040 | 1.0040 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 1 | 1.0042 | 1.0042 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 2 | 1.0038 | 1.0038 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 4 | 1.0148 | 1.0148 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 6 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 7 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 8 | 1.0038 | 1.0038 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 9 | 1.0036 | 1.0036 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 14 | 1.0074 | 1.0074 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 15 | 1.0047 | 1.0047 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 16 | 1.0068 | 1.0068 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 17 | 1.0052 | 1.0052 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 20 | 1.0036 | 1.0036 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 21 | 1.0035 | 1.0035 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 22 | 1.0036 | 1.0036 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 23 | 1.0035 | 1.0035 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 24 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 25 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 34 | 1.0056 | 1.0056 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 35 | 1.0056 | 1.0056 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 36 | 1.0036 | 1.0036 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 37 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 38 | 1.0034 | 1.0034 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 39 | 1.0039 | 1.0039 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 40 | 1.0162 | 1.0162 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 41 | 1.0067 | 1.0067 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 43 | 1.0037 | 1.0037 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 44 | 1.0740 | 1.0740 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 45 | 1.0740 | 1.0740 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 75 | 1.0173 | 1.0173 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 256 | 1.0041 | 1.0041 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 257 | 1.0040 | 1.0040 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 258 | 1.0040 | 1.0040 |
| EveryCommandAndRefusalUsesOneArrivalBudget | 16383 | 1.0770 | 1.0770 |
| NotificationFanoutAndStallsRetainTheirOriginalOrigin | 2 | 2.0069 | 2.0069 |
| NotificationFanoutAndStallsRetainTheirOriginalOrigin | 32773 | 1.0789 | 1.1573 |
| NotificationFanoutAndStallsRetainTheirOriginalOrigin | 32774 | 1.0789 | 1.1573 |
| NotificationFanoutAndStallsRetainTheirOriginalOrigin | 32777 | 1.0789 | 1.1573 |
| NotificationFanoutAndStallsRetainTheirOriginalOrigin | 32804 | 1.0789 | 1.1573 |

## Prior F4/F1 preflight comparison

The budget ruling cites the earlier F4 plus retained F1 preflight, whereas the main table compares the actual base F4 entry point. Both baselines are retained so the additional saved-state integration is visible. The preflight was a sizing probe; the final fixture uses the real AECP/store adapters.

| Shape | IF | Prior F4/F1 preflight span | Final span | Delta |
|---|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 94688 | 139072 | 44384 |
| 1x1_tdm8 | 2 | 107344 | 151728 | 44384 |
| 8x8 | 1 | 119856 | 192240 | 72384 |
| 8x8 | 2 | 147360 | 219744 | 72384 |

The five largest BSS entries for every shape/interface case are retained in `size-matrix.json`; the same five symbols occur, in different order, with the reduction options stated above.

After the final gates, ignored generated ROMs, parser cache and builder outputs were moved from the worktree to disk-backed scratch (`post-gate-generated`). Both tracked status and ignored-output dry-run inspection are clean. All gate workers have completed.
