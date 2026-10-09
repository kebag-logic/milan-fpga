# F5 handoff

[A572] Relates to #665. Local head `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`, branch `665-f5-aecp`.
PR #700 remains published at `0ded1f269a44d107498f177c8276665656e07d30`. These two new commits are unpushed.

## Round 3

The [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6086491737)
answers [R564-2-F1](https://github.com/kebag-logic/milan-fpga/pull/700#issuecomment-6086483772),
a MINOR under Conformance, Tests and Docs. All four requested outcomes are
implemented and locally verified. IEEE 1722.1-2021 7.4.15.1 selects subcommands
by VALID flags and ignores SAVED_STATE/STREAMING_WAIT. Milan v1.2 5.4.2.9's
requested-latency response applies when MSRP_ACC_LAT_VALID is set. With the bit
clear, current latency is returned and persistent state and notifications do
not change. The standards were checked directly; no standard text is reproduced.

Commit `a72843a18f95d52a578984a22ab73903b01b4673` strengthens native tests and
plants. Commit `fb9c57d2ae3484804ff90f67feb57bf420c93dfa` fixes the differential, oracle and README. Each step
was committed after its relevant checks passed. No production code, generated
file, submodule pin, register map, default build or shipping image changed.

## Changes at this head

| File:line | Round 3 change |
|---|---|
| `sw/firmware/ctrl/test/test_aecp.cpp:794` | Existing ignored-flag loop requests 765432 while the saved value is 123456. Response and stored value are checked independently. |
| `sw/firmware/ctrl/test/test_aecp.cpp:810` | New no-subcommand test covers flags 0/4/8/12 before and after a saved override. Checks current response, complete store, override bit, callback silence and absence of an unsolicited response to a registered peer. |
| `sw/firmware/ctrl/test/aecp_mutants.py:35` | Exact two reviewer plants plus a notification plant require named test failures and their specific diagnostics. |
| `sw/firmware/ctrl/test/aecp_wire.cpp:58` | No-subcommand transaction requests 765432 against current 67890. |
| `sw/firmware/ctrl/test/aecp_wire_oracle.py:103` | Expect requested latency only for a successful valid-latency subcommand; otherwise expect current latency. Require distinct stimulus for the clear-bit case. |
| `sw/firmware/ctrl/test/aecp_wire_oracle.py:187` | Seventh control plants a no-subcommand request echo and requires the precise latency diagnosis. |
| `sw/firmware/ctrl/test/aecp_wire.py:165` | Print each ingress's measured oracle-control count. |
| `sw/firmware/ctrl/aecp/README.md:145` | Describe the seventh control and distinct stimulus. |
| `sw/firmware/ctrl/aecp/README.md:154` | State the valid-flag exception and no-subcommand state/notification contract. |

The earlier implementation and Round 2 fixes remain documented in
`ROUND1-HANDOFF.md` and `ROUND2-HANDOFF.md`; their publication statements are
historical. Original authority and architecture references remain
REQUIREMENTS section 1, NFR-SCOUT-02/03/08, MAILBOX_SPLIT, issues #653/#637,
and processor #69/#73. The 224 KB ruling remains the applicable byte budget.

## Tests and planted defects

All 74 named AECP tests have a planted-defect owner below; all 72 source plants
were caught. The complete native composition has 70 tests at each interface
count; three image tests and one diagnostic test complete the named inventory.
The two exact reviewer plants each fail both strengthened native tests. The
new notification plant independently catches both a callback and a wire notice.
`round3/mutation-ledger.json` records exact substitutions and required diagnostics;
`round3/mutants/` and `round3/review-mutants/` retain assertion logs.

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
| `Core.BackpressureOrdersResponseBeforeNotice` at `sw/firmware/ctrl/test/test_aecp.cpp:840` | `owed-response-discarded` (sent.size()) |
| `Core.BootMapFaultsCannotPartlyReplaceTheSet` at `sw/firmware/ctrl/test/test_aecp.cpp:1143` | `boot-map-capacity-ignored` (aecp_map_restore) |
| `Core.ChangedScalarValuesAndDamagedLists` at `sw/firmware/ctrl/test/test_aecp.cpp:925` | `clock-reserved-halfword-omitted` (status for command) |
| `Core.ConfigurationAndLockedSetRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:890` | `foreign-lock-ignored` (status for command) |
| `Core.CounterNoticesCoalesceAndWaitForEligibility` at `sw/firmware/ctrl/test/test_aecp.cpp:989` | `counter-spacing-short` (sent.empty()) |
| `Core.CounterTimerArmsOnlyEligibleCompletedSnapshots` at `sw/firmware/ctrl/test/test_aecp.cpp:1213` | `counter-timer-during-output` (Unexpected mock function call); `retry-timer-lost` (Unexpected mock function call) |
| `Core.CrossInstanceInputsAreRefusedInsideRealCallbacks` at `sw/firmware/ctrl/test/test_aecp.cpp:580` | `cross-instance-guard-removed` (every cross-instance public input counts its refusal) |
| `Core.DescriptorAndObservationBoundaryFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:1385` | `stream-interface-bound-ignored` (status for command) |
| `Core.DynamicInfoSkipsOverflowAndKeepsLaterRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:945` | `dynamic-overflow-kept` (out.size()) |
| `Core.DynamicInfoWhitelistAndIndependentResults` at `sw/firmware/ctrl/test/test_aecp.cpp:866` | `dynamic-unknown-status` (per-record NOT_SUPPORTED) |
| `Core.EntityAvailableIndexUsesTheIngressObservation` at `sw/firmware/ctrl/test/test_aecp.cpp:1288` | `entity-available-index-static` (ENTITY reads current ADP available index) |
| `Core.EveryDescriptorAndReadFailures` at `sw/firmware/ctrl/test/test_aecp.cpp:554` | `descriptor-last-byte` (every READ_DESCRIPTOR is byte exact) |
| `Core.FailedSnapshotRetriesAndUnsupportedEventsAreDiscarded` at `sw/firmware/ctrl/test/test_aecp.cpp:1002` | `unsupported-events-queued` (pending) |
| `Core.FramingRejectsInvalidIdentityAndTruncation` at `sw/firmware/ctrl/test/test_aecp.cpp:1180` | `framing-version-ignored` (a.malformed) |
| `Core.GroupNameDoesNotOverwriteFirmwareVersion` at `sw/firmware/ctrl/test/test_aecp.cpp:1356` | `group-name-offset` (group_name changes only) |
| `Core.IdentifyCurrentValueAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:914` | `identify-one-accepted` (status for command) |
| `Core.InitRefusalsAndClosedService` at `sw/firmware/ctrl/test/test_aecp.cpp:1274` | `no-interface-accepted` (aecp_init) |
| `Core.LockQueriesAndExpiry` at `sw/firmware/ctrl/test/test_aecp.cpp:616` | `lock-long` (lock expires at exactly sixty seconds) |
| `Core.MapTopologyFailuresAndEmptyPartitions` at `sw/firmware/ctrl/test/test_aecp.cpp:1102` | `empty-map-no-page` (status for command) |
| `Core.MapsAreAtomicAndPaginated` at `sw/firmware/ctrl/test/test_aecp.cpp:958` | `map-capacity-ignored` (status for command) |
| `Core.MapsCompareEveryCoordinateAndBothDirectionsOnRestore` at `sw/firmware/ctrl/test/test_aecp.cpp:1252` | `map-cluster-channel-ignored` (a distinct cluster channel is a distinct input key) |
| `Core.MetadataConfigurationKeysAndRepeatedOverrides` at `sw/firmware/ctrl/test/test_aecp.cpp:1235` | `descriptor-configuration-ignored` (status for command) |
| `Core.MilanVendorCommandsAndRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1334` | `system-id-write-lost` (get(out,46,8)) |
| `Core.NameRefusalsAndNoOp` at `sw/firmware/ctrl/test/test_aecp.cpp:904` | `extra-name-accepted` (status for command) |
| `Core.NamesAndDescriptorOverlay` at `sw/firmware/ctrl/test/test_aecp.cpp:631` | `group-name-offset` (READ_DESCRIPTOR uses the same name) |
| `Core.NonAemMessageTypesFollowTheirOwnContracts` at `sw/firmware/ctrl/test/test_aecp.cpp:1298` | `hdcp-data-length-echo` (HDCP refusal clears data length) |
| `Core.NotificationBackpressureAndLatestCompletion` at `sw/firmware/ctrl/test/test_aecp.cpp:1365` | `completion-cookie-ignored` (an old completion cannot release a newer copy) |
| `Core.ObservationRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:758` | `path-failure-success` (status for command) |
| `Core.ObservationsHaveFullWireForms` at `sw/firmware/ctrl/test/test_aecp.cpp:740` | `counter-last-word` (coherent bank includes every counter) |
| `Core.OutputMappingsHaveOneGlobalOwner` at `sw/firmware/ctrl/test/test_aecp.cpp:1073` | `output-owner-crossed` (another port already owns this stream channel) |
| `Core.OutputPartitionGeometryUsesAllAdvertisedWidths` at `sw/firmware/ctrl/test/test_aecp.cpp:1125` | `empty-map-no-page` (status for command) |
| `Core.ProbeIdentityAndSequenceMustBothMatch` at `sw/firmware/ctrl/test/test_aecp.cpp:1202` | `probe-sequence-ignored` (probing) |
| `Core.ProbeRepliesResetOnlyTheirOwnInterface` at `sw/firmware/ctrl/test/test_aecp.cpp:1168` | `probe-status-matters` (probing) |
| `Core.ReentrantPortsCannotMutateState` at `sw/firmware/ctrl/test/test_aecp.cpp:1192` | `reentry-uncounted` (a.reentries) |
| `Core.RegistryCapacityInterfaceKeysAndLiveness` at `sw/firmware/ctrl/test/test_aecp.cpp:877` | `registry-no-retry` (sent.size()) |
| `Core.RestoreMapWholeSetClipAndDefaults` at `sw/firmware/ctrl/test/test_aecp.cpp:712` | `boot-clip-boundary` (m.count) |
| `Core.RestoreValuesValidateAndRollbackWithoutLiveEvents` at `sw/firmware/ctrl/test/test_aecp.cpp:678` | `restore-forgets-override` (aecp_value_latch) |
| `Core.RootDescriptorConfigurationIsIgnored` at `sw/firmware/ctrl/test/test_aecp.cpp:565` | `root-configuration-refused` (root descriptor ignores received configuration) |
| `Core.SavedValuesRejectWrongFieldsAndDamagedDescriptors` at `sw/firmware/ctrl/test/test_aecp.cpp:1085` | `saved-latency-wrong-type` (aecp_value_restore) |
| `Core.ScalarGetSetAndCurrentValueRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:647` | `scalar-refusal-reports-request` (refused SET reports current value) |
| `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` at `sw/firmware/ctrl/test/test_aecp.cpp:778` | `nosub-applies-request-latency` (ignored flags and no subcommand preserve latency); `stream-info-flags-echo` (SET response flags describe current state); `nosub-reports-request-latency` (SET latency follows Milan success and current refusal rules); `stream-info-request-echo` (SET response uses current format); `stream-info-noop-refused` (status for command) |
| `Core.SetStreamInfoWithoutSubcommandPreservesState` at `sw/firmware/ctrl/test/test_aecp.cpp:810` | `nosub-applies-request-latency` (no subcommand preserves stored latency); `nosub-applies-request-latency` (no subcommand preserves saved override); `nosub-notifies-change` (no subcommand emits no change notification); `nosub-notifies-change` (called more times than expected); `nosub-reports-request-latency` (no subcommand reports current latency, not requested latency) |
| `Core.StartIsDeferredAndHasFailureDeadline` at `sw/firmware/ctrl/test/test_aecp.cpp:852` | `start-wait-ten-ms` (sent.size()) |
| `Core.StaticMapsPreventOrphaningFormats` at `sw/firmware/ctrl/test/test_aecp.cpp:1052` | `static-map-orphan-accepted` (status for command) |
| `Core.StreamInfoDirectionFlagsAndLatency` at `sw/firmware/ctrl/test/test_aecp.cpp:768` | `latency-sign-accepted` (status for command) |
| `Core.UnavailableSnapshotsDoNotBlockIndependentNoticesOrSpin` at `sw/firmware/ctrl/test/test_aecp.cpp:1016` | `unavailable-retry-spins` (failed snapshots wait for a timed retry); `unavailable-head-blocks-notices` (backpressure retains the built independent snapshot) |
| `Core.UnsupportedAndAcquire` at `sw/firmware/ctrl/test/test_aecp.cpp:601` | `identify-refusal-body-lost` (identify refusal preserves descriptor fields); `unknown-body-lost` (unsupported command echoes its exact body) |
| `Image.EveryDescriptor` at `sw/firmware/ctrl/test/test_aecp_image.cpp:51` | `image-byte-corrupted` (descriptor defaults survive the image load) |
| `Image.RejectDirectory` at `sw/firmware/ctrl/test/test_aecp_image.cpp:90` | `image-type-ignored` (invalid descriptor directory is refused at its boundary) |
| `Image.RejectHeader` at `sw/firmware/ctrl/test/test_aecp_image.cpp:69` | `image-crc-ignored` (image CRC rejects corrupted descriptor bytes) |
| `Latency.DeferredFailureAndTimerPathsUseTheirDueTime` at `sw/firmware/ctrl/test/test_aecp.cpp:1584` | `start-wait-ten-ms` (commits.size()) |
| `Latency.EveryCommandAndRefusalUsesOneArrivalBudget` at `sw/firmware/ctrl/test/test_aecp.cpp:1505` | `latency-response-missing` (commits.size()) |
| `Latency.NotificationFanoutAndStallsRetainTheirOriginalOrigin` at `sw/firmware/ctrl/test/test_aecp.cpp:1564` | `latency-budget-relaxed` (late output cannot restart the service clock) |
| `Mailbox.EveryInterfaceAndObservationPort` at `sw/firmware/ctrl/test/test_aecp.cpp:1420` | `mailbox-interface-crossed` (fabric.tx_sent) |
| `Mailbox.FullTransmitRingAndCompletionQueueKeepTheirOwedResponse` at `sw/firmware/ctrl/test/test_aecp.cpp:1468` | `mailbox-full-completions-overwritten` (adapter.ports.send) |
| `Mailbox.OutputTailStartsCounterSpacingAfterAStall` at `sw/firmware/ctrl/test/test_aecp.cpp:1436` | `counter-spacing-short` (fabric.tx_sent) |
| `Mailbox.TimerIdentityAndAttachRefusals` at `sw/firmware/ctrl/test/test_aecp.cpp:1451` | `mailbox-stale-tag-accepted` (adapter.stale_expiries) |
| `Nvm.AbsentMapClipsButRefusedMapRevertsItsFormat` at `sw/firmware/ctrl/test/test_aecp.cpp:250` | `boot-clip-boundary` (m.count) |
| `Nvm.AcceptedStateSurvivesTheRealStorePowerCycle` at `sw/firmware/ctrl/test/test_aecp.cpp:227` | `nvm-latency-dirty-lost` (owner.port.latch) |
| `Nvm.EveryChangeQueuesOnlyItsOwnedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:311` | `nvm-latency-dirty-lost` (owner.pending) |
| `Nvm.MapRecordsRefuseMissingStorageAndNeverPartiallyLatch` at `sw/firmware/ctrl/test/test_aecp.cpp:293` | `nvm-partial-latch-writes` (owner.port.latch) |
| `Nvm.ScalarRecordsUseSharedValidationAndReserveUnknownGroups` at `sw/firmware/ctrl/test/test_aecp.cpp:269` | `restore-forgets-override` (owner.port.latch) |
| `Nvm.ShapePoolsAndNameOrdinalsMatchSavedRecords` at `sw/firmware/ctrl/test/test_aecp.cpp:193` | `group-name-offset` (b) |
| `Nvm.WholeMapFramingAndEmptySetAreDistinct` at `sw/firmware/ctrl/test/test_aecp.cpp:208` | `nvm-hole-accepted` (owner.port.apply) |

The wire grader adds `nosub-latency`: changing only the no-subcommand response
to request latency must fail `SET requested or current latency`, not some other
check. All seven controls run on each of the three ingress runs. The unchanged
Q1-Q5 review probes pass at both interface counts; Q2 stores 111, requests 999,
and observes 111 in both the response and store.

## Coverage

The full coverage generator executed both firmware banks and recorded all 30 production files. All eight AECP/application units have raw 100% lines and branches. No exclusion was added or changed. The check of the unchanged ratchet returned 0 across all 30 files.

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

Every PASS row below completed with command rc 0. Exact argument vectors and
elapsed times are in `round3/commands.json`; reproduction instructions are in
`ROUND3-REPRODUCE.md`. Tests run before the last commit covered identical working
file bytes; final scope and clean-worktree checks apply to the committed head.

| Gate | Result and evidence |
|---|---|
| Native AECP composition, interfaces 1 and 2 | PASS: 70 tests each. |
| Complete firmware bank, RV32 required, jobs 4 | PASS: 59 arms, 65 tallies, 1408 checks, zero failures. |
| Exact reviewer plants | PASS: all five killed by completed named assertion failures; no build-error credit. |
| Unchanged R564-2 probes | PASS: Q1-Q5 at interfaces 1 and 2. |
| AECP source plants | PASS: 72/72 across two partitions, 74 named tests. |
| Coverage check | PASS: 30 files, all eight AECP/application units raw 100%, no changed exclusions or ratchet. |
| Coverage, tally and RV32 grader self-tests | PASS: runtime/compiler required. |
| Sanitizer arms, interfaces 1 and 2 | PASS: 70 tests each. |
| Wire differential | PASS: 132/137/137 records; 31 commands, 17 notification types, 42 descriptors and seven controls per ingress. |
| Default mailbox gate | PASS: both buses, co-simulation, two interfaces, 369 host checks and five quick plants. |
| Mailbox generation check | PASS: zero findings. |
| Builder bank | PASS: four ordinary partitions and four profile partitions; exact fixture unions verified. The calibration row below is explicitly unexecuted. |
| Builder gate 11 resource calibration | NOT RUN: the historical placed-utilization report is absent; no hardware work was attempted. |
| Documentation workflow | PASS: all 73 commands; separate docs, style and added-line checks pass. |
| Four full RV32 links | PASS: all section/pool sizes unchanged; all load images byte-identical to Round 2. |
| Physical calibration and routed fit | NOT RUN; hardware/bench access is outside the assignment. |
| Hosted checks and local replica after push | Owed for this unpublished head; no push authorized. |
| Independent re-review and candidate merge validation | Owed; no author review verdict. |

The initial documentation environment lacked the pinned parser; those setup
attempts were rerun successfully with the locked dependencies. An initial
size-comparison assertion compared whole ELFs and rejected path-dependent
metadata; the corrected comparison checks every load byte plus sections and
pools. These superseded attempts remain in `round3/attempts.json`, not in the
passing gate table. Unchanged older control, SRP and saved-store mutation
campaigns were not rerun in Round 3; their prior receipts remain historical.

## Linked images

All spans include 8192 bytes of stack reservation. The section sizes and static
pool inventory are in `round3/size-matrix.json`; runtime provenance is unchanged.
The maximum is 221728 bytes, 2272 below the stricter 224000-byte interpretation.
This is 49 nominal 36-Kbit tiles or 55 tiles with 32-bit packing, an inherited
owner-visibility item. It is not a routed memory-fit or stack-bound proof.

| Shape | Interfaces | Text | Rodata | Data | Bss | RAM span | Delta from base | Round 3 delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 82932 | 11950 | 56 | 37252 | 140400 | +60032 | 0 |
| 1x1_tdm8 | 2 | 84220 | 11950 | 56 | 48620 | 153056 | +60032 | 0 |
| 8x8 | 1 | 82980 | 25158 | 448 | 77428 | 194224 | +99056 | 0 |
| 8x8 | 2 | 84356 | 25158 | 448 | 103556 | 221728 | +99056 | 0 |

The base for the reported deltas is `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

The largest five named static consumers in the 8x8/two-interface fixture are
`image_arena` 48064, `image_values` 11753, `image_app` 9640, `image_srp` 5864 and
`image_maps` 4608 bytes. They and the reduction options recorded in the Round 1
handoff are unchanged. Bounded pools could be reduced by configured demand;
immutable descriptor storage could be separated from mutable overlays. Either
would be separate design work requiring capacity and performance proof.

## Review and publication

R564-2 reports RTL and Robustness CLEAN at the prior published head. Round 3
changes only tests and documentation; no replacement reviewer ledger is claimed.
Conformance, Tests and Docs require re-review of this head, and the reviewer
must accept any carried coverage. R565-2 was positive on the prior head per the
assignment. No review verdict on the new head is implied.

Processor #73's common command model, physical calibration, full integration,
publication, full merge verification, hosted gates and merge validation remain owed. No push, PR edit,
merge, hardware operation or shipping-image change was performed. The final
issue comment records REVIEW READY with the local head. Public evidence must be
published with the candidate by the authorized lane owner; this local packet
is the reviewable handoff for that publication.

## Wire decisions

The independent oracle grades 42 descriptors, 31 AEM command codes, three MVU commands and 17 notification command types on each ingress. The unchanged references are `2ad2f845dd583f8310075fa2380cb60a04fd091a` (one interface) and `c9f74b6866a63dd3c0e4534724bfc07a86ad142b` (two). Reference inventories and verdicts are in `round3/wire-1/` and `round3/wire-2/`.

| Difference | Records per ingress | Clause |
|---|---:|---|
| Root descriptor configuration normalization | 4 | IEEE 7.4.5.1/.2 |
| Current SET_STREAM_INFO response and flag decisions | 7 | IEEE 7.4.15.1; Milan 5.4.2.9 |
| System unique ID support | 2 | Milan 5.4.4.2/.3 |
| Saved-default override notification | 3 | Milan 5.4.5.2 |
| Started-state GET_STREAM_INFO notice | 2 | Milan Table 5.22 |
| Permitted unlock flag alternatives | 3 | IEEE 7.4.2.1 |

The contract additionally records HDCP empty-data responses versus reference echoes, ignored reserved/extended types versus reference replies, and dynamic available_index versus the reference image constant. The wire fixture supplies zero ADP advertisements on both sides; the composed application independently proves the dynamic count. The two-interface reference exposes ingress but no physical egress-index signal; its wire counts establish registry isolation, while the core separately checks its egress index.

