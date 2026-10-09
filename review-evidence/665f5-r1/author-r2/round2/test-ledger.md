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
