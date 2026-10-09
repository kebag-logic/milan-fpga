# AECP test-to-defect ledger

Head `1e68d1b62ef2facdf0e8dbad28a202297d433c61`. Each named assertion fails in a completed run with its planted source defect; crashes, a different test failure and a missing assertion token are rejected. All 59 source plants were caught; all 66 tests have at least one. Exact before/after source seams are in `mutation-ledger.json`. The final maximum-body latency strengthening also reran its plant.

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
