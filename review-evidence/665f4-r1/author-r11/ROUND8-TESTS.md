[A560]

# Round 8 test-to-defect map

Candidate: `a6e6916826448f81de2b779ca61a87a9f8c47278`. Tests must fail their named behavioral observable; compile failures do not count.

The full table contains 469 control/MAAP/ACMP plants and 108 SRP plants. The six four-way SRP plants are additionally run at IF=1; the full SRP table runs at IF=2.

| Campaign / plant | Test(s) | Required observable | Source |
| --- | --- | --- | --- |
| control / reentry-guard-removed | AdpReentry.AdvertiseInlineExpiry; AdpReentry.DelayInlineExpiryOnGmChange; AdpReentry.AdvertiseInlineExpiry; AdpReentry.DelayInlineExpiryOnGmChange | inline ADVERTISE expiry asserts; inline DELAY expiry asserts; inline ADVERTISE expiry is counted; inline DELAY expiry is counted | `sw/firmware/ctrl/adp/adp.c` |
| control / reentry-uncounted | AdpReentry.AdvertiseInlineExpiry | inline ADVERTISE expiry is counted | `sw/firmware/ctrl/adp/adp.c` |
| control / reentry-not-ignored | AllPorts/AdpPortEntry.RefusesBeforeTouchingState/ | callback leaves core state unchanged | `sw/firmware/ctrl/adp/adp.c` |
| control / departing-keeps-index | Table551/AdpWalkCell.Graded/ | available_index | `sw/firmware/ctrl/adp/adp.c` |
| control / departing-sends-zero | AdpCore.A10toA14DepartingIndex | A10 SHUTDOWN in WAITING | `sw/firmware/ctrl/adp/adp.c` |
| control / available-replaces-owed-departing | AdpCore.A15OwedDepartingAcrossARestart | A15 with room, the next poll sends the owed ENTITY_DEPARTING first | `sw/firmware/ctrl/adp/adp.c` |
| control / available-passes-owed-departing | AdpCore.A17RoomBackBeforeAPoll | A17 room back and TMR_DELAY expiring before a poll | `sw/firmware/ctrl/adp/adp.c` |
| control / second-departing-dropped | AdpCore.A16SecondShutdownQueuesItsOwn | A16 a SHUTDOWN while one is owed queues its own | `sw/firmware/ctrl/adp/adp.c` |
| control / second-shutdown-overwrites-index | AdpCore.A16SecondShutdownQueuesItsOwn | A16 a SHUTDOWN while one is owed queues its own | `sw/firmware/ctrl/adp/adp.c` |
| control / link-loss-drops-owed-departing | AdpCore.A18LinkLossKeepsTheOwedDeparting | A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING | `sw/firmware/ctrl/adp/adp.c` |
| control / gm-change-drops-owed-available | AdpCore.A19IgnoredInputsKeepTheOwedAvailable | A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed | `sw/firmware/ctrl/adp/adp.c` |
| control / discover-drops-owed-available | AdpCore.A19IgnoredInputsKeepTheOwedAvailable | A19 so does an ENTITY_DISCOVER | `sw/firmware/ctrl/adp/adp.c` |
| control / stray-expiry-drops-owed-available | AdpCore.A19IgnoredInputsKeepTheOwedAvailable | A19 and a stray expiry, which is counted | `sw/firmware/ctrl/adp/adp.c` |
| control / link-loss-keeps-owed-available | AdpCore.A20LinkLossDropsTheOwedAvailable | A20 a link loss drops the owed ENTITY_AVAILABLE at once | `sw/firmware/ctrl/adp/adp.c` |
| control / departing-queue-unbounded | Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/ | E5 64 SHUTDOWNs behind a full ring, expiry taken before the room: the ENTITY_AVAILABLE is committed | `sw/firmware/ctrl/adp/adp.c` |
| control / coalesced-departing-uncounted | AdpCore.A21DepartingCapacity | A21 the next SHUTDOWN is coalesced into the queued one and counted | `sw/firmware/ctrl/adp/adp.c` |
| control / coalesce-drops-queued-departing | AdpCore.A21DepartingCapacity | A21 the next SHUTDOWN is coalesced into the queued one and counted | `sw/firmware/ctrl/adp/adp.c` |
| control / coalesce-overwrites-oldest-index | AdpCore.A21DepartingCapacity | A21 the next SHUTDOWN is coalesced into the queued one and counted | `sw/firmware/ctrl/adp/adp.c` |
| control / own-discover-discarded | Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING | RCV_ADP_DISCOVER(own eid) x WAITING | `sw/firmware/ctrl/adp/adp.c` |
| control / down-answers-discover | Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN | RCV_ADP_DISCOVER(eid 0) x DOWN | `sw/firmware/ctrl/adp/adp.c` |
| control / link-down-departs | Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING | LINK_DOWN x WAITING: frames committed | `sw/firmware/ctrl/adp/adp.c` |
| control / gm-change-ignored | Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING | GM_CHANGE x WAITING | `sw/firmware/ctrl/adp/adp.c` |
| control / delay-ignores-link-down | Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed | LINK_DOWN x DELAY | `sw/firmware/ctrl/adp/adp.c` |
| control / shutdown-in-down-departs | Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN | SHUTDOWN x DOWN | `sw/firmware/ctrl/adp/adp.c` |
| control / advertise-expiry-skips-delay | Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING | TMR_ADVERTISE x WAITING | `sw/firmware/ctrl/adp/adp.c` |
| control / advertise-period-wrong | Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed | TMR_DELAY x DELAY(timer armed) | `sw/firmware/ctrl/adp/adp.c` |
| control / link-up-draws-startup-kind | Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN | LINK_UP x DOWN | `sw/firmware/ctrl/adp/adp.c` |
| control / draw-kinds-merged | AdpCore.A9DrawKinds | A9 every startup draw | `sw/firmware/ctrl/adp/adp.c` |
| control / foreign-discover-answered | AdpCore.A3toA5DiscoverAndDiscard | A4 a foreign DISCOVER | `sw/firmware/ctrl/adp/adp.c` |
| control / frame-misses-config-index | AdpWalk.P11ConfigurationIndexBytes | P11 | `sw/firmware/ctrl/adp/adp.c` |
| control / stale-tag-accepted | AdpAdapter.B1StaleTagDiscarded | B1 an expiry of the arm a GM_CHANGE replaced | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / latency-extra-read | AdpLatency.C0toC6EveryResponsePath | C0 LINK_UP -> TMR_DELAY armed | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / pool-free-leaks | Pool.P2ReleaseAndBadFrees | P2 a released block | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / calloc-overflow-unchecked | Pool.P3CallocZeroesAndRefusesAWrap | P3 calloc refuses | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / pool-double-free-accepted | Pool.P2ReleaseAndBadFrees | P2 a double free | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / debug-truncation-uncounted | DebugSink.S2TruncatedToTheLine | S2 the truncation | `sw/firmware/ctrl/port/ctrl_debug.c` |
| control / tick-count-ignored | Loop.L4TickFanOut | L4 every centisecond | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / rx-pass-unbounded | Loop.L2PerPassRxBound | L2 a pass takes at most | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / poll-owes-nothing | AdpOwed.E0toE3PendingWake | E1 the loop does not sleep while a frame is owed | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / events-halved | AdpBacklog.F0toF7FullBacklogs; AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound | F2 all 16 event records are taken by pass; F1 every event is taken by pass 2 | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / rx-before-events | AdpBacklog.F0toF7FullBacklogs | F1 events first | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / carried-ticks-overwritten | Loop.L8TickRecordWhileCarried | L8 a TICK record taken while centiseconds are carried | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / tick-slice-unbounded | Loop.L7TickSlices | L7 at most CTRL_LOOP_TICKS_PER_PASS | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / owed-ticks-let-it-sleep | Loop.L7TickSlices | L7 and the loop keeps passing | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / filter-opened-before-eid | LoopBring.L1OpenOrder | L1 OWN_EID is written before | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / rx-no-resync | Driver.D1MalformedRecordResynchronises; Records/DriverMalformed.D7RefusedAndResynchronised/ | D1 and the ring is resynchronised; and the ring is resynchronised to RX_HEAD | `sw/firmware/ctrl/mbx/mbx.c` |
| control / tx-overfills | Driver.D3HeldMergeFillsAndOrderAcrossChannels | D3 a held merge fills the ring | `sw/firmware/ctrl/mbx/mbx.c` |
| control / lanes-big-endian | Suite/MbxModelGroup.PassesOnTheModel/ | F1 frame byte k is ring word | `sw/firmware/ctrl/mbx/mbx_wire.h` |
| control / frame-sources-from-sinks | Fabric/EntityField.MatchesTheFabric/talker_stream_sources | talker_stream_sources | `sw/firmware/ctrl/adp/adp.c` |
| control / pool-falls-back-to-heap | Pool.P4ShlanFunctionsDrawOnTheBoundPool;  | P4 shlan_malloc and shlan_calloc draw on the bound pool; symbols outside the C library | `sw/firmware/ctrl/port/shlan_port.c` |
| control / model-rate-unlimited | Suite/MbxModelGroup.PassesOnTheModel/RateLimit | T0 the frames past it count in RATE_DROP | `sw/firmware/ctrl/host/mbx_model.c` |
| control / seq-not-stamped | Driver.D3HeldMergeFillsAndOrderAcrossChannels | D3 ACMP, ACMP, AECP committed by the driver | `sw/firmware/ctrl/mbx/mbx.c` |
| control / model-round-robin | Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder | X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-gm-hi-live | Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot | G0 GM_HI reads the snapshot | `sw/firmware/ctrl/host/mbx_model.c` |
| control / zero-byte-class-accepted | Pool.P5ClassTablesAndArenasRefused | P5 a class of zero-byte blocks is refused | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / zero-size-refusal-uncounted | Pool.P6CallocOfNothingAndOnAnExhaustedPool | P6 and both refusals are counted | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / foreign-free-uncounted | Pool.P7FreeBelowTheArenaRefused | P7 a free below the first class is refused and counted | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / port-pool-unreported | Pool.P8PortLayerUnbound | P8 the bound pool is the one reported | `sw/firmware/ctrl/port/shlan_port.c` |
| control / pool-follows-a-cut-free-list | Pool.P9AFreeListShorterThanItsCountIsExhausted | crashed on signal 11 | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / pool-cut-list-refuses-outright | Pool.P9AFreeListShorterThanItsCountIsExhausted | P9 a class whose list ends before its count | `sw/firmware/ctrl/port/ctrl_pool.c` |
| control / encoding-failure-swallowed | DebugSink.S3UnencodablePrintDiscarded | S3 an encoding failure is returned | `sw/firmware/ctrl/port/ctrl_debug.c` |
| control / rx-binds-no-function | LoopBring.L9TablesRefuseNullAndOverflow | L9 a channel bound to no function is refused | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / seed-left-at-zero | AdpCore.A22GeneratorNeverStuckAtZero | A22 an entity id whose words cancel the seed constant | `sw/firmware/ctrl/adp/adp.c` |
| control / enable-not-idempotent | AdpCore.A23RepeatedEnableOrDisableChangesNothing | A23 an enable while enabled draws and arms nothing | `sw/firmware/ctrl/adp/adp.c` |
| control / other-subtype-accepted | AdpCore.A24OtherEtherTypeOrSubtypeDiscarded | A24 a DISCOVER under another EtherType or subtype is discarded | `sw/firmware/ctrl/adp/adp.c` |
| control / app-binds-pool-after-the-mailbox | AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox | unsatisfied and active | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-starts-on-an-uncarved-pool | AppComposition.U1AnUncarvablePoolStartsNothing | over-saturated and active | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / major-unchecked | AppComposition.U1AnotherContractOpensNothing; IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major | U1 a bitstream carrying another contract is refused; U2 major differs | `sw/firmware/ctrl/mbx/mbx.c` |
| control / evt-words-unchecked | IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words | U2 evt_words differs | `sw/firmware/ctrl/mbx/mbx.c` |
| control / step-waits-twice | LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed | U3 every turn is one pass | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / maap-base-shifted | DriverUnit.D6MaapRangeWritten | D6 MAAP_BASE_LO holds the base's low word | `sw/firmware/ctrl/mbx/mbx.c` |
| control / tx-negative-fill | DriverUnit.D8TransmitRefusals | D8 a TX_TAIL more than a ring behind TX_HEAD is no room | `sw/firmware/ctrl/mbx/mbx.c` |
| control / unknown-event-decoded-as-tick | DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt | D9 an event of a type the contract does not define | `sw/firmware/ctrl/mbx/mbx.c` |
| control / whole-field-loses-its-top-bit | DriverUnit.D10LanesAndFieldsAtTheirBounds | D10 and reads whole | `sw/firmware/ctrl/mbx/mbx_wire.h` |
| control / slots-past-the-bank | AdpAdapterUnit.B2SlotsPastTheTimerBankRefused | B2 slots past the fabric's timer bank | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / foreign-frame-uncounted | AdpAdapterUnit.B3ForeignInterfaceCounted | B3 a record, a LINK and a GM | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / attach-ignores-poll-room | AdpAdapterUnit.B4LoopWithNoRoomRefused | B4 a loop with no room for the poll is refused | `sw/firmware/ctrl/adp/adp_mbx.c` |
| control / mmio-offset-as-index | MmioPlatform.M1OneWordAtBasePlusOffset | M1 a write lands in the word at base + offset | `sw/firmware/ctrl/plat/mbx_plat_mmio.c` |
| control / wait-without-wfi | MmioPlatform.M2WaitIsThePlatformWfi | M2 each mbx_hal_wait() waits once | `sw/firmware/ctrl/plat/mbx_plat_mmio.c` |
| control / model-tag-stripped | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q1 tagged, it (adp): no RX record | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-tpid-matches-a-tuple | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q1 tagged, it (srp MSRP): no RX record | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-multicast-dst-ignored | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q2 to another destination MAC, it (adp) | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-ethertype-ignored | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q3 under another control EtherType, it (adp) | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-subtype-ignored | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q4 with an unassigned AVTP subtype, it (adp) | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-own-any-unicast | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections; AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused | Q2 to another destination MAC, it (aecp, command); B2 a foreign unicast is refused | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-own-mac-of-interface-0 | Suite/MbxModelGroup.PassesOnTheModel/OwnMacPerInterface | Q8 another interface's own MAC, or one on an index with no interface, reaches no ring | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-own-mac-hi-dropped | Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks | R1 OWN_MAC_LO keeps every bit and OWN_MAC_HI keeps MAC[47:32] only | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-aecp-command-only | Suite/MbxModelGroup.PassesOnTheModel/AecpBothDirections | Q7 the CONTROLLER_AVAILABLE response for this controller reaches the AECP ring | `sw/firmware/ctrl/mbx/mbx_contract.h` |
| control / model-mismatch-never-counted | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections; AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused | Q2 to another destination MAC, it (adp): FILTER_MISMATCH counts it once; B2 and counted once in FILTER_MISMATCH | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-mismatch-counts-identity-refusals | Suite/MbxModelGroup.PassesOnTheModel/TupleRejections | Q5 ENTITY_DISCOVER for another entity: FILTER_MISMATCH does not count it | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-mismatch-sets-no-err | Suite/MbxModelGroup.PassesOnTheModel/FilterMismatchCount | Q9 a mismatch sets IRQ_STATUS.ERR | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-msg-type-off-by-one | Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast | Q11 a DEFEND to this interface's own MAC reaches the MAAP ring | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-tuple-msg-type-ignored | Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast | Q11 a PROBE to this interface's own MAC: no RX record | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-msg-type-refusal-uncounted | Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast | Q11 a PROBE to this interface's own MAC: FILTER_MISMATCH counts it once | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-defend-any-unicast | Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast | Q11 a DEFEND to a unicast MAC no interface owns: no RX record | `sw/firmware/ctrl/host/mbx_model.c` |
| control / own-mac-unguarded | DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount | D11 an interface past the contract's is refused | `sw/firmware/ctrl/mbx/mbx.c` |
| control / own-mac-halves-swapped | DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount; Driver.D12OwnMacAndMismatchOnTheModel | D11 OWN_MAC_LO holds MAC[31:0]; D12 an AEM_COMMAND to it on interface 0 passes | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mismatch-read-from-bus-err | DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount; Driver.D12OwnMacAndMismatchOnTheModel | D11 FILTER_MISMATCH is read as its COUNT field; D12 FILTER_MISMATCH reads the one tuple failure | `sw/firmware/ctrl/mbx/mbx.c` |
| control / own-mac-after-the-channels-open | LoopBring.L1OpenOrder | L1 every interface's OWN_MAC is written before any channel opens | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / app-own-mac-not-the-entity-mac | AppComposition.U4EveryInterfaceOwnsTheEntityMacBeforeAChannelOpens; AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused | OWN_MAC is the entity's MAC; B2 a command to this interface's own unicast MAC passes | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / acmp-init-no-interface | AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold | A0 no interface is refused | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-init-too-many-sinks | AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold | A0 more sinks than ACMP_MAX_SINKS | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-init-too-many-sources | AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold | A0 more sources than ACMP_MAX_SOURCES | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-init-sink-interface | AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold | A0 a sink on an interface the entity lacks is refused | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-init-source-interface | AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold | A0 a source on an interface the entity lacks is refused | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-init-reads-the-seed | AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled; AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | A0 init calls no port; U5 composing touches no mailbox register | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-header-no-resp-2s | AcmpCore.A1BindFromUnboundRespondsThenProbes; Table530/ListenerWalk.Graded/BIND_NEW_UNB | A1 and TMR_NO_RESP armed 200 ms; the timer's deadline | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-retry-2s | AcmpCore.A9FailureWaitsForTheRetry; Table530/ListenerWalk.Graded/PROBE_FAIL_PWR | A9 and TMR_RETRY 4 s; the timer's deadline | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-no-tk-5s | AcmpCore.A8SuccessSettles | A8 TMR_NO_RESP stopped and TMR_NO_TK 10 s started | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-valid-time-in-seconds | AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches | A22 TMR_NO_ADP is the received valid_time in two-second units | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-listener-unknown-is-2 | AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId | A2 LISTENER_UNKNOWN_ID, the command's fields echoed | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-registering-failed-bit | AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed | REGISTERING_FAILED 1 (Table 5.39) | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-header-cdl-84 | AcmpCore.A1BindFromUnboundRespondsThenProbes | A1 every frame goes to the ACMP multicast address | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-bind-count-0 | AcmpCore.A1BindFromUnboundRespondsThenProbes; Table530/ListenerWalk.Graded/BIND_NEW_UNB | A1 BIND_RX_RESPONSE is Table 5.32; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-without-fast-connect | AcmpCore.A1BindFromUnboundRespondsThenProbes; Table530/ListenerWalk.Graded/BIND_NEW_UNB | A1 PROBE_TX_COMMAND is Table 5.33; frame 1 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-before-response | AcmpCore.A1BindFromUnboundRespondsThenProbes | A1 BIND_RX_RESPONSE is Table 5.32 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-resp-2s | AcmpCore.A1BindFromUnboundRespondsThenProbes; AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot | A1 and TMR_NO_RESP armed 200 ms; B3 TMR_NO_RESP is armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-bind-starts-no-discovery | AcmpCore.A1BindFromUnboundRespondsThenProbes; Table530/ListenerWalk.Graded/BIND_NEW_UNB | A1 the discovery machine starts; discovery runs exactly while | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-bind-change-before-response | AcmpCore.A1BindFromUnboundRespondsThenProbes | A1 the change is reported after the response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-nothing-persisted | AcmpCore.A1BindFromUnboundRespondsThenProbes; AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | A1 the binding is saved; N1 the bind marks its record | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-not-persisted | AcmpStore.N2AnUnbindIsSavedAsAnUnboundRecord; Table530/ListenerWalk.Graded/UNBIND_PWR | N2 the unbind marks the record; the store marked | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-rebind-not-persisted | AcmpStore.N4AnUnreadSlotRefusesPersistence; AcmpCore.A6BindAnotherSourceRestartsTheSink | N4 a new bind is answered and taken, and its record marked; A6 the new binding is saved | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-streaming-wait-ignored | AcmpCore.A1BindFromUnboundRespondsThenProbes | STREAMING_WAIT binds it stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-sw-read-from-fast-connect | AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed | STREAMING_WAIT saved | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-getrx-count-unbound | AcmpCore.A2GetRxStateInEveryState; Table530/ListenerWalk.Graded/GETRX_UNB | A2 GET_RX_STATE_RESPONSE is Table 5.34/5.37/5.38/5.39; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-getrx-no-fast-connect | AcmpCore.A2GetRxStateInEveryState; Table530/ListenerWalk.Graded/GETRX_PWR | A2 GET_RX_STATE_RESPONSE is Table 5.34/5.37/5.38/5.39; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-getrx-no-registering-failed | AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed | REGISTERING_FAILED 1 (Table 5.39) | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unknown-sink-silent | AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId | A2 a command for a sink the entity lacks | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-echoes-the-talker | AcmpCore.A3UnbindInEveryState; Table530/ListenerWalk.Graded/UNBIND_PWR | A3 UNBIND_RX_RESPONSE is Table 5.36; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-keeps-srp | AcmpCore.A3UnbindInEveryState; Table530/ListenerWalk.Graded/UNBIND_SNR | A3 a settled sink stops SRP before the response; SRP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-srp-after-response | AcmpCore.A3UnbindInEveryState | A3 a settled sink stops SRP before the response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-keeps-discovery | AcmpCore.A3UnbindInEveryState; Table530/ListenerWalk.Graded/UNBIND_PWR | A3 then UNBOUND, binding cleared; discovery runs exactly while | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-change-before-response | AcmpCore.A3UnbindInEveryState | A3 the change is reported after the response (#653) | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-not-authorized-is-13 | AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind; ListenerScenario.LD3TheLockRefusalStatus | A4 CONTROLLER_NOT_AUTHORIZED (16; LD3 the firmware sends 16 | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-lock-ignored | AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind | A4 one response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-lock-refuses-the-holder | AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked | A4 the locking controller binds | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-rx-state-locked | AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked | A4 GET_RX_STATE asks no lock | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-rebind-same-reprobes | AcmpCore.A5RebindTheSameSourceUpdatesAndExits; Table530/ListenerWalk.Graded/BIND_SAME_PWR | A5 a re-bind of the same source sends the response alone; frames | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-rebind-same-keeps-the-controller | AcmpCore.A5RebindTheSameSourceUpdatesAndExits | A5 the controller and STREAMING_WAIT are updated | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-bind-new-keeps-srp | AcmpCore.A6BindAnotherSourceRestartsTheSink; Table530/ListenerWalk.Graded/BIND_NEW_SNR | A6 SRP is stopped and its parameters cleared; SRP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-bind-same-talker-is-the-same-source | AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding | A6 the same talker with another talker_unique_id is a new source | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-sequence-id-never-advances | AcmpCore.A12DelaySendsANewProbe; AcmpCore.A16OneCounterForEveryNewProbe | A12 a new PROBE_TX_COMMAND with the next sequence_id; A16 each new PROBE_TX_COMMAND takes the next | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-sequence-id-per-sink | AcmpCore.A16OneCounterForEveryNewProbe; Table530/ListenerWalk.Graded/BIND_NEW_UNB | A16 each new PROBE_TX_COMMAND takes the next; frame 1 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-response-keyed-on-the-source | AcmpCore.A7ResponsesKeyOnTheListenerUniqueId | A7 the response belongs to the sink | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-guard-controller-dropped | AcmpCore.A7EachGuardTermIsChecked; ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages | A7 a response with another controller; LW2 a probe response wrong in guard term 0 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-guard-talker-dropped | AcmpCore.A7EachGuardTermIsChecked; ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages | A7 a response with another controller; LW2 a probe response wrong in guard term 1 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-guard-unique-id-dropped | AcmpCore.A7EachGuardTermIsChecked; ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages | A7 a response with another controller; LW2 a probe response wrong in guard term 2 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-guard-sequence-id-dropped | AcmpCore.A7EachGuardTermIsChecked; ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages | A7 a response with another controller; LW2 a probe response wrong in guard term 3 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-guard-reads-the-binding | AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding | A7 the answer to the probe sent before a re-bind still matches | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-responses-taken-outside-probing | AcmpCore.A7ResponsesOutsideProbingAreIgnored; Table530/ListenerWalk.Graded/PROBE_OK_SNR | A7 RCV_PROBE_TX_RESP is ignored outside; SRP started | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-vlan-masked | AcmpCore.A8SuccessSettles | A8 with the response's stream_id, stream_dest_mac and stream_vlan_id exactly | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-tk-1s | AcmpCore.A8SuccessSettles; Table530/ListenerWalk.Graded/PROBE_OK_PWR | A8 TMR_NO_RESP stopped and TMR_NO_TK 10 s started; the timer's deadline | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-settle-starts-no-srp | AcmpCore.A8SuccessSettles; Table530/ListenerWalk.Graded/PROBE_OK_PWR | A8 SRP is started; SRP started | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-settle-swaps-stream-fields | AcmpCore.A8SuccessSettles; Table530/ListenerWalk.Graded/PROBE_OK_PWR | stream_vlan_id exactly; the settled stream | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-failure-status-dropped | AcmpCore.A9FailureWaitsForTheRetry; Table530/ListenerWalk.Graded/PROBE_FAIL_PWR | A9 a failed response: PRB_W_RETRY, the ACMP status is its status; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-failure-retries-at-200ms | AcmpCore.A9FailureWaitsForTheRetry; Table530/ListenerWalk.Graded/PROBE_FAIL_PWR | A9 and TMR_RETRY 4 s; the timer's deadline | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-duplicate-takes-a-new-sequence-id | AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp; Table530/ListenerWalk.Graded/TMR_CMD_PWR | A10 an exact duplicate of the first probe; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-second-timeout-keeps-status-0 | AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp; AcmpCore.A25OnlyTable522ItemsAreReported; Table530/ListenerWalk.Graded/TMR_CMD_PW2 | A10 the second: no frame, LISTENER_TALKER_TIMEOUT; A25 the ACMP status LISTENER_TALKER_TIMEOUT does; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-duplicate | AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp; Table530/ListenerWalk.Graded/TMR_CMD_PWR | A10 the first TMR_NO_RESP sends one frame; frames | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-retry-ignores-discovery | AcmpCore.A11RetryWaitsForTheTalkerOrDelays; Table530/ListenerWalk.Graded/TMR_RETRY_PWT_disc | A11 TMR_RETRY, talker discovered: TMR_DELAY; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-retry-zeroes-the-status | AcmpCore.A11RetryWaitsForTheTalkerOrDelays; Table530/ListenerWalk.Graded/TMR_RETRY_PWT_disc | A11 and the ACMP status stays; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-delay-resends-the-old-probe | AcmpCore.A12DelaySendsANewProbe; Table530/ListenerWalk.Graded/TMR_DELAY_PWD | A12 a new PROBE_TX_COMMAND with the next sequence_id; frame 0 byte for byte | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-tk-keeps-srp | AcmpCore.A13NoTalkerAttributeReprobes; Table530/ListenerWalk.Graded/TMR_NOTK_SNR | A13 TMR_NO_TK clears the SRP parameters and stops SRP; SRP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-reprobe-ignores-discovery | AcmpCore.A13NoTalkerAttributeReprobes; AcmpCore.A15UnregisteredReprobes; Table530/ListenerWalk.Graded/TMR_NOTK_SNR_disc | A13 talker discovered: TMR_DELAY, PRB_W_DELAY; A15 talker discovered: TMR_DELAY, PRB_W_DELAY; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-registered-anywhere | AcmpCore.A14RegisteredSettlesTheReservation; Table530/ListenerWalk.Graded/TK_REG_PWR | A14 EVT_TK_REGISTERED anywhere else; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-registered-keeps-no-tk | AcmpCore.A14RegisteredSettlesTheReservation; Table530/ListenerWalk.Graded/TK_REG_SNR | A14 EVT_TK_REGISTERED: TMR_NO_TK cleared; the sink's timer armed or not | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-registered-kind-dropped | AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed; Table530/ListenerWalk.Graded/TK_REG_SNR | REGISTERING_FAILED 1 (Table 5.39); registered state | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unregistered-anywhere | AcmpCore.A15UnregisteredReprobes; Table530/ListenerWalk.Graded/TK_UNREG_SNR | A15 EVT_TK_UNREGISTERED anywhere else; state, probing and ACMP status | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unregistered-keeps-srp | AcmpCore.A15UnregisteredReprobes; Table530/ListenerWalk.Graded/TK_UNREG_SOK | A15 EVT_TK_UNREGISTERED, talker not discovered: SRP stopped; SRP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-timer-at-the-latest-deadline | AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline | A17 each interface's timer is armed at the earliest | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-timer-port-called-every-time | AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline | A17 the port is called only when the earliest deadline moves | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-timer-never-stopped | AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline; AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord | A17 an interface whose sinks hold no deadline; C11 ENTITY_DEPARTING: PRB_W_AVAIL, the slot stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-expiry-takes-every-interface | AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline | A17 an expiry takes the due timers only | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-expiry-not-consumed | AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline | A17 an expiry with nothing due changes nothing and re-arms the timer it consumed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-zero-delay-waits | AcmpCore.A18AZeroDelayProbesInTheSameExpiry | A18 TMR_RETRY drawing 0 ms sends its probe in the same expiry | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-delay-up-to-4s | AcmpCore.A18AZeroDelayProbesInTheSameExpiry | A18 the longest draw is 1000 ms | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-seed-at-every-draw | AcmpCore.A18TheSeedIsTakenAtTheFirstDraw | A18 and never again | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-rng-left-at-0 | AcmpCore.A18TheSeedIsTakenAtTheFirstDraw | A18 a seed that cancels the state to 0 leaves it 1 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-response-passes-an-owed-frame | AcmpCore.A19NothingPassesAnOwedFrame | A19 a response does not pass one already owed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-poll-drains-everything | AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits; AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1 | A19 one frame per poll; E2 3 frames owed ahead | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-change-not-held-for-its-response | AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits; AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt | A19 but its change is not reported while its response waits (#653); E1 nothing reported yet | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-full-queue-acts | AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs | A19 a command whose response would find the queue full is dropped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-lost-probe-uncounted | AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered | A19 a probe the full queue cannot take is lost and counted | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-first-owed-releases-every-change | AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether | A19 the bind's response left but the unbind's is still owed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-poll-newest-first | AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1; AcmpCore.A19NothingPassesAnOwedFrame | E2 3 frames owed ahead; A19 they leave in the order they were made | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-tx-reports-asking-failed | AcmpCore.A20ProbeTxIsAnsweredFromTheSource | A20 PROBE_TX_RESPONSE is Table 5.43 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-tx-echoes-every-flag | TalkerWalk.TW1ProbeTheFlagLawAndTheSource | TW1 PROBE_TX: SUCCESS, FAST_CONNECT and STREAMING_WAIT echoed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-tx-any-interface | AcmpCore.A20ProbeTxIsAnsweredFromTheSource; TalkerWalk.TW4TheInterfaceAndTheStatelessProperty | A20 a probe from another interface than the source's; TW4 a probe from another interface | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-tx-no-destination-mac-check | AcmpCore.A20ProbeTxIsAnsweredFromTheSource; TalkerWalk.TW1ProbeTheFlagLawAndTheSource | A20 no destination MAC: TALKER_DEST_MAC_FAILED; TW1 no destination MAC | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-disconnect-always-succeeds | AcmpCore.A20DisconnectGetTxStateAndGetTxConnection; TalkerWalk.TW3DisconnectAndGetTxConnection | A20 DISCONNECT_TX of an unknown source: TALKER_UNKNOWN_ID; TD1 DISCONNECT_TX of an unknown source | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unknown-source-answered | AcmpCore.A20ProbeTxIsAnsweredFromTheSource; TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive | A20 an unknown source: TALKER_UNKNOWN_ID; TW2 an unknown source | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-tx-state-echoes-the-listener | AcmpCore.A20DisconnectGetTxStateAndGetTxConnection; TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive | A20 GET_TX_STATE: listener fields 0; TW2 GET_TX_STATE: listener fields 0 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-tx-state-registering-failed-0 | AcmpCore.A20DisconnectGetTxStateAndGetTxConnection; TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive | REGISTERING_FAILED live; TW2 GET_TX_STATE: listener fields 0 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-tx-state-unheld-mac | AcmpCore.A20DisconnectGetTxStateAndGetTxConnection | A20 with no destination MAC held, none is reported | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-tx-connection-supported | AcmpCore.A20DisconnectGetTxStateAndGetTxConnection; TalkerWalk.TW3DisconnectAndGetTxConnection | A20 GET_TX_CONNECTION: NOT_SUPPORTED; TW3 GET_TX_CONNECTION: NOT_SUPPORTED | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-every-listener-is-this-one | AcmpCore.A21MessagesNotForThisEntityAreIgnored | A21 commands for another listener or talker | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-every-talker-is-this-one | AcmpCore.A21MessagesNotForThisEntityAreIgnored | A21 commands for another listener or talker | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-short-pdu-read | AcmpCore.A21MalformedFramesAreCounted | A21 a frame shorter than the Milan ACMPDU | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-longer-pdu-refused | AcmpCore.A21MalformedFramesAreCounted | A21 the longer IEEE 1722.1-2021 PDU is accepted | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovery-reads-no-grandmaster | AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches; Table554/DiscoveryWalk.Graded/AVAILABLE_GM_mismatch__index____last__TK_NOT_DISCOVERED | A22 TK_NOT_DISCOVERED: an AVAILABLE from another grandmaster; the discovery state | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovery-reads-no-domain | AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches; Table554/DiscoveryWalk.Graded/AVAILABLE_domain_mismatch__index____last__TK_DISCOVERED | A22 and from another domain; the discovery state | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-valid-time-in-seconds | AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches; Table554/DiscoveryWalk.Graded/ | A22 TMR_NO_ADP is the received valid_time in two-second units; TMR_NO_ADP armed from the received valid_time | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovered-interface-unchecked | AcmpCore.A22DiscoveredStateCells; Table554/DiscoveryWalk.Graded/AVAILABLE_interface_index_differs__TK_DISCOVERED | A22 TK_DISCOVERED: an AVAILABLE with another interface_index is ignored; TMR_NO_ADP untouched | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restart-on-a-smaller-index-only | AcmpCore.A22DiscoveredStateCells | A22 available_index 700 <= last | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restart-raises-no-discovered | AcmpCore.A22DiscoveredStateCells; Table554/DiscoveryWalk.Graded/AVAILABLE_match__index____last__TK_DISCOVERED | EVT_TK_DEPARTED then EVT_TK_DISCOVERED; the events raised | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restart-mismatch-keeps-aging | AcmpCore.A22DiscoveredStateCells; Table554/DiscoveryWalk.Graded/AVAILABLE_GM_mismatch__index____last__TK_DISCOVERED | A22 index <= last from another grandmaster; TMR_NO_ADP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-refresh-notes-no-index | AcmpCore.A22DiscoveredStateCells; Table554/DiscoveryWalk.Graded/AVAILABLE_match__index___last__TK_DISCOVERED | A22 a rising available_index is noted; the available_index noted | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-departing-taken-undiscovered | AcmpCore.A22DepartingAndAging | A22 a DEPARTING in TK_NOT_DISCOVERED is ignored | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-departing-interface-unchecked | AcmpCore.A22DepartingAndAging; Table554/DiscoveryWalk.Graded/DEPARTING_interface_index_differs__TK_DISCOVERED | A22 a DEPARTING with another interface_index is ignored; the discovery state | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-departing-keeps-aging | AcmpCore.A22DepartingAndAging; Table554/DiscoveryWalk.Graded/DEPARTING_interface_index_matches__TK_DISCOVERED | A22 a DEPARTING: TMR_NO_ADP stopped; TMR_NO_ADP stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-aging | AcmpCore.A22DepartingAndAging; Table554/DiscoveryWalk.Graded/TMR_NO_ADP_TK_DISCOVERED | A22 TMR_NO_ADP: TK_NOT_DISCOVERED and EVT_TK_DEPARTED; the discovery state | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovery-on-every-interface | AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface | A22 every bound sink of the talker processes it | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovery-on-unbound-sinks | AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface | A22 an unbound sink runs no discovery | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-grandmaster-sampled-for-the-refresh | AcmpCore.A22DiscoveredStateCells | A22 TK_DISCOVERED: an AVAILABLE with another interface_index is ignored | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-grandmaster-sampled-per-sink | AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface | A22 and the grandmaster is sampled once for the frame | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-reentry-unguarded | AcmpCore.A23EveryEntryRefusesACallFromInsideAPort; AcmpCore.A23EveryPortIsGuarded | A23 a call made from inside the send port is refused; A23 the port kind 1 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-reentry-untrapped | AcmpCore.A23EveryEntryRefusesACallFromInsideAPort | refused, counted and trapped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-send-port-unflagged | AcmpCore.A23EveryEntryRefusesACallFromInsideAPort | A23 a call made from inside the send port is refused | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-timer-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 1 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-gptp-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 2 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-clock-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 3 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-seed-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 4 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-lock-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 5 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-source-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 6 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-srp-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 7 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-persist-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 8 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-changed-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 9 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restore-lands-in-prb-w-resp | AcmpCore.A24ARestoredBindingFastConnects; AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | A24 startup with a saved binding; N1 into PRB_W_AVAIL | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restore-starts-no-discovery | AcmpCore.A24ARestoredBindingFastConnects; AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | A24 startup with a saved binding; N1 into PRB_W_AVAIL | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restore-announced | AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | N1 probing saves nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-record-flags-swapped | AcmpStore.N3EachSinksStartedStateIsSaved | N3 each sink's started state and STREAMING_WAIT come back | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-record-unique-id-little-endian | AcmpCore.A24ARestoredBindingFastConnects | A24 the latch gives the same record back | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-restore-unique-id-little-endian | AcmpCore.A24ARestoredBindingFastConnects | A24 the record's flags and parameters, big-endian | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-roll-back-keeps-the-bindings | AcmpCore.A24UnboundRecordsRefusalsAndRollback; AcmpStore.N6TheRollBackAndEveryOtherGroup | A24 the roll-back drops every restored binding; N6 and drops what it applied | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbound-record-not-zero | AcmpCore.A24UnboundRecordsRefusalsAndRollback | A24 an unbound sink's record is all zeros | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-started-not-saved | AcmpCore.A24StartedIsSavedAndReported; AcmpStore.N3EachSinksStartedStateIsSaved | A24 the started state is saved (5.3.8.7); N3 the started state alone is a change | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovery-notifies | AcmpCore.A25OnlyTable522ItemsAreReported; Table530/ListenerWalk.Graded/TK_DISC_PWR | A25 discovery noted while settled moves no Table 5.22 item; notified exactly when a Table 5.22 item moved | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-status-not-notified | AcmpCore.A25OnlyTable522ItemsAreReported | A25 the ACMP status LISTENER_TALKER_TIMEOUT does | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probing-status-not-notified | Table530/ListenerWalk.Graded/TK_DEP_PWD | notified exactly when a Table 5.22 item moved | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-frames-on-the-adp-channel | AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder | B1 the response, then the probe, on the acmp channel | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-timer-on-the-next-slot | AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot | B3 TMR_NO_RESP is armed on interface 0's ACMP slot | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-timer-deadline-taken-as-a-delay | AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot | B3 TMR_NO_RESP is armed on interface 0's ACMP slot at NOW_MS + 200 | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-stale-tag-taken | AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded | B4 the expiry of a replaced arm | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-tag-reused | AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded | B4 the expiry of a replaced arm | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-stop-keeps-the-arm | AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded | B4 the expiry of a stopped arm is counted | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-tap-takes-discover | AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp | B5 an ENTITY_DISCOVER still goes to ADP | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-tap-drops-the-rest | AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp | B5 an ENTITY_DISCOVER still goes to ADP | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-no-tap | AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp; AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | B5 and reaches discovery through the tap; U5 ACMP binds its channel and stands in front of ADP's handler | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-domain-not-sampled | AcmpMailbox.B6TheGrandmasterIsTheInterfaces | B6 one from interface 0's grandmaster and domain is taken | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-attach-before-adp | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 attaching before ADP bound the adp channel is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-attach-ignores-sink-room | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 a loop with no room for the event sink is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-attach-ignores-poll-room | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 a loop with no room for the poll is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-slots-past-the-bank | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 a first slot of 16 is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-interfaces-past-the-mailbox | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 more interfaces than the mailbox has are refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-poll-owes-nothing | AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt | E1 nothing reported yet, and the loop does not sleep | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-bind-reads-the-clock-twice | AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | C0 BIND_RX -> response, PROBE_TX, TMR_NO_RESP | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-get-rx-state-reads-the-clock | AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | C1 GET_RX_STATE -> response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-response-reads-the-clock-twice | AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | C2 PROBE_TX_RESPONSE -> TMR_NO_TK armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-unbind-reads-the-clock | AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | C3 UNBIND_RX -> response, timer stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-talker-reads-the-clock | AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | C4 talker command -> response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-expiry-reads-the-clock-twice | AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry | C5 TMR_NO_RESP -> duplicate PROBE_TX, TMR_NO_RESP | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-available-reads-the-clock-twice | AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord | C10 ENTITY_AVAILABLE from its RX_HEAD -> TMR_DELAY armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-departing-samples-the-grandmaster | AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord | C11 ENTITY_DEPARTING from its RX_HEAD -> timer stopped | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-aging-samples-the-grandmaster | AcmpMailbox.C12AgingIsServedInThePassThatTakesTheExpiry | C12 TMR_NO_ADP -> TK_NOT_DISCOVERED | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-smallest-record-overstated | AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing | F4 the ring holds ACMP_MBX_RX_BACKLOG records of the smallest frame | `sw/firmware/ctrl/acmp/acmp_mbx.h` |
| control / acmp-pass-bound-understated | AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound | F3 the worst pass of the backlog | `sw/firmware/ctrl/acmp/acmp_mbx.h` |
| control / acmp-adp-ring-bound-understated | AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound | F5 ENTITY_AVAILABLE behind a full adp ring | `sw/firmware/ctrl/acmp/acmp_mbx.h` |
| control / acmp-discovery-takes-the-first-sink | AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound | F5 every matching bound sink takes it in the same pass | `sw/firmware/ctrl/acmp/acmp.c` |
| control / rx-one-record-per-pass | AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound; AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound | F5 the ENTITY_AVAILABLE is taken by pass; F2 every acmp record is taken by | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / acmp-second-no-resp-samples-the-grandmaster | AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry | C6 TMR_NO_RESP -> TMR_RETRY armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-retry-samples-the-grandmaster | AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry | C7 TMR_RETRY -> TMR_DELAY armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-delay-reads-the-clock-again | AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry | C8 TMR_DELAY -> PROBE_TX, TMR_NO_RESP | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-tk-samples-the-grandmaster | AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry | C9 TMR_NO_TK -> TMR_DELAY armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-backlog-understated | AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound; AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing | F0 the acmp ring holds no more records than A1 assumes; F4 the ring holds ACMP_MBX_RX_BACKLOG records of the smallest frame | `sw/firmware/ctrl/acmp/acmp_mbx.h` |
| control / model-event-ring-a-record-short | AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound | F0 the event ring is full | `sw/firmware/ctrl/host/mbx_model.c` |
| control / acmp-new-bind-never-started | AcmpCore.A1BindWithoutStreamingWaitBindsStarted | A1 a bind without STREAMING_WAIT lands started | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-bind-response-always-streaming-wait | AcmpCore.A1BindWithoutStreamingWaitBindsStarted | A1 a bind without STREAMING_WAIT lands started | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-view-without-registering-failed | AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed | A2 and the view says so | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-discovered-probing-stays-passive | AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail | A22 EVT_TK_DISCOVERED in PRB_W_AVAIL | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-grandmaster-read-twice | AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail; AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord | A22 the grandmaster is sampled once for the frame; C10 ENTITY_AVAILABLE from its RX_HEAD -> TMR_DELAY armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-adp-short-frame-taken | AcmpCore.A22OtherAdpFramesAreIgnored | A22 a short ADPDU, a DISCOVER | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-adp-ethertype-unchecked | AcmpCore.A22OtherAdpFramesAreIgnored | A22 a short ADPDU, a DISCOVER | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-adp-subtype-unchecked | AcmpCore.A22OtherAdpFramesAreIgnored | A22 a short ADPDU, a DISCOVER | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-adp-discover-taken | AcmpCore.A22OtherAdpFramesAreIgnored | A22 a short ADPDU, a DISCOVER | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-frames-to-the-own-mac | AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused; AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder | B2 and is answered, to the multicast address; B1 to the ACMP multicast address from the interface's MAC | `sw/firmware/ctrl/acmp/acmp.c` |
| control / app-acmp-before-adp | AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | B0 the app with ACMP starts on the model | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-acmp-never-composed | AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | U5 ACMP binds its channel and stands in front of ADP's handler | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / acmp-nvm-bindings-to-the-others | AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | N1 the binding parameters come back | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-refusal-applied | AcmpStore.N5ARecordTheCoreRefusesKeepsItsDefault; AcmpStore.N6TheRollBackAndEveryOtherGroup | N5 a binding record of a sink the configuration lacks is refused; N6 one of another length is refused | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-d3-roll-back-kept | AcmpStore.N6TheRollBackAndEveryOtherGroup | N6 every other group | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-latch-length-unchecked | AcmpStore.N6TheRollBackAndEveryOtherGroup | N6 a latch of another length gives nothing | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-bindings-latched-by-the-others | AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects | N1 the binding parameters come back | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-release-dropped | AcmpStore.N6TheRollBackAndEveryOtherGroup | N6 every other group | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-settle-dropped | AcmpStore.N6TheRollBackAndEveryOtherGroup | N6 every other group | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-nvm-model-always-ready | AcmpStore.N6TheRollBackAndEveryOtherGroup | N6 the model's readiness is the other owners' | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-version-unchecked | AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead; AcmpMailbox.B9AnotherAvtpVersionPassesTheFilterAndChangesNothing | A26 a BIND_RX of AVTP version 1; B9 the core discards it | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-adp-version-unchecked | AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead; AcmpMailbox.B9AnotherAvtpVersionPassesTheFilterAndChangesNothing | A26 an ENTITY_AVAILABLE of version 1; B9 and discovers nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-version-bits-misread | AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead | A26 a BIND_RX of AVTP version 1 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-header-version-1 | AcmpCore.A1BindFromUnboundRespondsThenProbes | A1 BIND_RX sends two frames: the response and the probe | `sw/firmware/ctrl/acmp/acmp.h` |
| control / acmp-owed-probe-timer-runs | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves; AcmpCore.A27AStalledDuplicateGetsItsWholeInterval; AcmpCore.A23EveryEntryRefusesACallFromInsideAPort | A27 a probe with no transmit room: PRB_W_RESP, its TMR_NO_RESP held; A27 the first TMR_NO_RESP finds no room; A23 and the outer call completes as if it had not been made | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-owed-probe-never-starts | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves; AcmpCore.A27AStalledDuplicateGetsItsWholeInterval | A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send; A27 the duplicate, the first probe's | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-owed-probe-no-resp-2s | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves | A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-owed-probe-sequence-unchecked | AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing | A27 the old probe leaving starts no timer for the new one | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-owed-probe-unnamed | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves | A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-owed-probe-names-the-next-sink | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves | A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-probe-timer-before-its-send | AcmpCore.A30AProbeTakenAtOnceRunsFromTheClockAfterItsSend; AcmpCore.A30ADuplicateTakenAtOnceRunsFromTheClockAfterItsSend | A30 the probe taken at once: TMR_NO_RESP 200 ms from the clock after its send; A30 the duplicate taken at once | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-taken-probe-timer-from-the-entry-clock | AcmpCore.A30ADuplicateTakenAtOnceRunsFromTheClockAfterItsSend | A30 the duplicate taken at once: TMR_NO_RESP 200 ms from the clock after its send, not the expiry's | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-expiry-due-at-its-first-read | AcmpCore.A30ATimerDueAfterAnEarlierSinksSendIsTakenInTheSameExpiry | A30 sink 1's 0 ms TMR_DELAY, drawn after sink 0's duplicate moved the clock | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-held-timer-expires | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves | A27 an expiry of the interface while the probe is owed takes nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-held-timer-armed | AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves | A27 a probe with no transmit room: PRB_W_RESP, its TMR_NO_RESP held, no timer armed | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-lost-probe-held | AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered | A19 and it does | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-stop-keeps-the-hold | AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing | A27 an UNBIND_RX while the probe is owed stops its timer | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-slot-sum-wraps | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 a first slot of 4294967295 is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-slot-narrowed-first | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 a first slot of 256 is refused | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-slots-one-short | AcmpAdapterUnit.B7RefusalsOfTheAdapter | B7 the last slot range that fits is taken | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-one-slot-for-all-interfaces | AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot | B3 TMR_NO_RESP is armed on interface 1's ACMP slot | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-expiry-to-interface-0 | AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot | B3 the duplicate leaves at 200 ms exactly, on interface 1 | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-gptp-of-interface-0 | AcmpMailbox.B6TheGrandmasterIsTheInterfaces | B6 one from interface 1's grandmaster and domain is taken | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-record-flag-defines-swapped | AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime | A24 bound and started: flags 0x03 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-record-valid-bit-moved | AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime | A24 bound and stopped: the valid flag alone, 0x01 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-longer-record-applied | AcmpCore.A24UnboundRecordsRefusalsAndRollback | A24 a payload of 21 bytes is refused | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-nvm-d3-rollback-drops-bindings | AcmpStore.N7AD3RollBackKeepsTheBindings; AcmpStore.N7AD3RollBackKeepsTheBindings | N7 and leaves the applied binding; N7 and the saved binding still comes back | `sw/firmware/ctrl/acmp/acmp_nvm.c` |
| control / acmp-due-unsigned | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap; AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap | A28 TMR_NO_RESP: nothing at the wrap or 1 ms before its deadline; A28 the first expiry takes sink 0 only | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-earliest-unsigned | AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap | A28 the interface timer holds the earlier deadline | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-adp-due-unsigned | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_NO_ADP: nothing before | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-resp-deadline-saturates | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_NO_RESP: nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-retry-deadline-saturates | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_RETRY: nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-tk-deadline-saturates | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_NO_TK: nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-delay-deadline-saturates | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_DELAY: nothing | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-no-adp-deadline-saturates | AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap | A28 TMR_NO_ADP: nothing before | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-admit-never-called | AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker; AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding; AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | A29 a BIND_RX admits its talker once; B8 a BIND_RX writes its sink's entry; C0 and its talker admitted in that pass | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-admit-on-every-entry | AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker; AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | A29 a re-bind to the same talker, from any controller or source, admits nothing; C1 GET_RX_STATE -> response | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-admit-ignores-another-talker | AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker; AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding | A29 a re-bind to another talker admits it; B8 a BIND_RX of another talker rewrites the entry | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-admit-on-interface-0 | AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker; AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding | A29 sink 2's talker on interface 1; B8 a BIND_RX writes its sink's entry of interface 1's table | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-admit-port-unflagged | AcmpCore.A23EveryPortIsGuarded | A23 the port kind 10 is guarded | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-reset-forgets-the-admitted | AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens | A29 a sink the store resets is withdrawn at the next open | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-open-does-nothing | AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens; AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | A29 acmp_open admits each restored binding's talker; U5 and writes the bound-talker entry of the binding restored | `sw/firmware/ctrl/acmp/acmp.c` |
| control / acmp-open-unguarded | AcmpCore.A23EveryEntryRefusesACallFromInsideAPort | A23 a call made from inside the send port is refused, counted and trapped, entry 9 | `sw/firmware/ctrl/acmp/acmp.c` |
| control / app-acmp-never-opened | AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract; AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp | U5 and writes the bound-talker entry of the binding restored; B5 the open wrote the restored binding's talker | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / acmp-mbx-admit-on-entry-0 | AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | U5 and writes the bound-talker entry of the binding restored | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / acmp-mbx-admit-always-bound | AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding; AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem | B8 an UNBIND_RX clears the entry's BOUND_EN; C3 UNBIND_RX answered in one pass, its talker withdrawn | `sw/firmware/ctrl/acmp/acmp_mbx.c` |
| control / mbx-bound-unguarded | DriverUnit.D13BoundTalkerEntries | D13 an interface past the contract's is refused | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mbx-bound-entry-unguarded | DriverUnit.D13BoundTalkerEntries | D13 an entry past the table's is refused | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mbx-bound-withdraw-writes-nothing | DriverUnit.D13BoundTalkerEntries; AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding | D13 a withdrawn entry: BOUND_EN cleared; B8 an UNBIND_RX clears the entry's BOUND_EN | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mbx-bound-enabled-before-the-identity | DriverUnit.D13BoundTalkerEntries | D13 BOUND_EN is cleared before the identity is written | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mbx-bound-halves-swapped | DriverUnit.D13BoundTalkerEntries; AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding | D13 BOUND_EID_LO holds talker[31:0]; B8 a BIND_RX writes its sink's entry | `sw/firmware/ctrl/mbx/mbx.c` |
| control / mbx-bound-entry-stride-ignored | DriverUnit.D13BoundTalkerEntries; AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | D13 BOUND_EID_LO holds talker[31:0]; U5 and writes the bound-talker entry of the binding restored | `sw/firmware/ctrl/mbx/mbx.c` |
| control / model-bound-term-misses | Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers | Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-enable-ignored | Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers | Q12 an entry with BOUND_EN clear, its identity still written | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-low-word-only | Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers | Q12 an entity_id differing from the entry in [63:32] only | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-table-of-interface-0 | Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers | Q13 on another interface, or an index with no interface, it reaches no ring | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-term-any-type | Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers | Q12 no other message_type of a bound talker passes on its entity_id | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-entry-decoded-as-0 | Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks | R1 each bound-talker entry keeps | `sw/firmware/ctrl/host/mbx_model.c` |
| control / model-bound-en-reads-the-eid | Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks | R1 each bound-talker entry keeps | `sw/firmware/ctrl/host/mbx_model.c` |
| control / app-maap-slots-overlap-acmp | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 every interface's ADP, ACMP and MAAP slots are distinct and inside the timer bank | `sw/firmware/ctrl/app/ctrl_app.h` |
| control / app-maap-slots-overlap-adp | MaapHost.ExplicitAppComposition; AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | protocol timer slots disjoint; U6 every interface's ADP, ACMP and MAAP slots are distinct | `sw/firmware/ctrl/app/ctrl_app.h` |
| control / app-maap-attached-after-open | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen; MaapHost.ExplicitAppComposition | U6 opening opens the adp, acmp and maap channels and no other;  | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-before-acmp | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen; AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened | U6 ADP, then ACMP, then MAAP attach, each with its sink and its poll; U7 before MAAP attaches | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-started-in-compose | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 composing the three touches no mailbox register | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-never-started | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen; MaapHost.ExplicitAppComposition | U6 MAAP probes from the open;  | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-channel-unbound | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound; AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | F6 events, acmp and maap records wait; U6 ACMP still stands in front of ADP's handler, and MAAP holds its own channel | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / app-maap-preferred-unchecked | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened; MaapHost.ExplicitAppComposition | U7 a preferred range below the B.4 pool is refused;  | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-last-range-refused | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened | U7 the pool's last range is not | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-range-past-the-pool | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened | U7 one that runs past the pool's end is refused | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-refusal-ignored | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened | U7 MAAP for an entity with no talker source is refused | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-acmp-refusal-ignored | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened; AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract | U7 a refused ACMP configuration fails the three-way composition; U5 an ACMP configuration the module refuses fails the composition | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-entry-takes-no-port | AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened; MaapHost.ExplicitAppComposition | U7 the explicit MAAP entry refuses a missing stream-address port;  | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-maap-entry-drops-preferred | MaapHost.ExplicitAppComposition |  | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-three-way-pass-overrun | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound | F6 the worst pass of the three-way backlog | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / app-maap-mac-per-interface | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1 | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-own-mac-per-interface | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1 | `sw/firmware/ctrl/app/ctrl_app.c` |
| control / app-three-way-bound-drops-maap | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound; AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound | F6 the three-way bound is both modules' passes; F6 the three-way bound is both modules' passes | `sw/firmware/ctrl/app/ctrl_app.h` |
| control / app-three-way-bound-one-maap-poll | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound | F6 the three-way bound is both modules' passes | `sw/firmware/ctrl/app/ctrl_app.h` |
| control / maap-down-start-keeps-owner | MaapCore.ReleaseLossAndRetry | starting down withdraws the prior owner | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-initial-send-absent | MaapCore.InitialAndThreeRetransmissions | initial PROBE is immediate | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-retransmit-count | MaapCore.InitialAndThreeRetransmissions | three retransmissions remain | `sw/firmware/ctrl/maap/maap.h` |
| control / maap-probe-count-not-decremented | MaapCore.InitialAndThreeRetransmissions | retransmission decrements once | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-wire-version | MaapCore.InitialAndThreeRetransmissions | B.2 complete PROBE bytes | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-wire-length | MaapCore.InitialAndThreeRetransmissions | B.2 complete PROBE bytes | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-wire-source | MaapCore.InitialAndThreeRetransmissions | B.2 complete PROBE bytes | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-wire-padding | MaapCore.InitialAndThreeRetransmissions | B.2 complete PROBE bytes | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-constant-probe_base | MaapCore.ConstantsStrictTimersAndSeed |  | `sw/firmware/ctrl/maap/maap.h` |
| control / maap-constant-probe_variation | MaapCore.ConstantsStrictTimersAndSeed |  | `sw/firmware/ctrl/maap/maap.h` |
| control / maap-constant-announce_base | MaapCore.ConstantsStrictTimersAndSeed |  | `sw/firmware/ctrl/maap/maap.h` |
| control / maap-constant-announce_variation | MaapCore.ConstantsStrictTimersAndSeed |  | `sw/firmware/ctrl/maap/maap.h` |
| control / maap-seed-clock-ignored | MaapCore.ConstantsStrictTimersAndSeed |  | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-zero-seed-sticks | MaapCore.ConstantsStrictTimersAndSeed | zero sum cannot lock generator | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-biased-random-bucket | MaapCore.UniformDrawRejectsIncompleteBucket | incomplete random bucket rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-numeric-mac-priority | MaapCore.ReverseOctetPriority | least significant octet decides first | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-defend-multicast | MaapCore.DefendEchoAndIntersection | echo request and exact intersection | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-defend-echo-own-range | MaapCore.DefendEchoAndIntersection | echo request and exact intersection | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-intersection-too-long | MaapCore.DefendEchoAndIntersection | echo request and exact intersection | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-adjacent-overlaps | MaapCore.DisjointAdjacentZeroAndDefendRange | half open intervals | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-zero-count-conflicts | MaapCore.DisjointAdjacentZeroAndDefendRange | half open intervals | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-defend-checks-request | MaapCore.DisjointAdjacentZeroAndDefendRange | DEFEND tests conflict fields | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-ethertype | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-subtype | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-version | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-reserved-zero | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-reserved-high | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-cdl-short | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-cdl-truncated | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-cdl-current | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-source-zero | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-source-group | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-destination | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-malformed-own-probe | MaapCore.MalformedAndVersionCompatibility | malformed input is rejected | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-valid-minimum-refused | MaapCore.MalformedAndVersionCompatibility | B.2.3 recognized future | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-future-version-refused | MaapCore.MalformedAndVersionCompatibility | B.2.3 recognized future | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-range-end-off-by-one | MaapCore.InitAndPreferredRangeBounds |  | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-port-up-keeps-claim | MaapCore.ReleaseLossAndRetry | PortOperational invalidates acquired address | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-release-keeps-enable | MaapCore.ReleaseLossAndRetry | released instance stays idle | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-expiry-forgotten-on-stall | MaapCore.StalledOutputRetainsOrderAndOriginalExpiry | original expiry remains owed | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-allocation-before-commit | MaapCore.StalledOutputRetainsOrderAndOriginalExpiry | allocation waits for committed ANNOUNCE | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-probe-announce-reordered | MaapCore.StalledOutputRetainsOrderAndOriginalExpiry |  | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-overflow-uncounted | MaapCore.QueueBoundAndWithdrawal | overload is counted as failure | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-poll-unbounded | MaapCore.QueueBoundAndWithdrawal | poll has bounded work | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-release-leaves-output | MaapCore.QueueBoundAndWithdrawal |  | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-reentry-not-counted | MaapCore.ReentrantPortsAreCountedAndIgnored | all input guards fire | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-debug-no-assert | MaapDebug.SynchronousExpiryAsserts | debug reentry assertion | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-stream-index-missing | MaapCsr.EveryStreamAddressAndLossGate | stream destination base plus index | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-selection-not-restored | MaapCsr.EveryStreamAddressAndLossGate | selection restored | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-fabric-owner-kept | MaapCsr.EveryStreamAddressAndLossGate | fabric MAAP disabled without touching seed | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-loss-keeps-crf | MaapCsr.EveryStreamAddressAndLossGate | loss closes both media gates | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-count-mismatch-accepted | MaapCsr.ShapesAndCountRefusal | wrong shape stays disabled | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-crf-index-wrong | MaapCsr.ShapesAndCountRefusal | CRF only shape | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-timer-tag-ignored | MaapHost.StaleTagsForeignInputsAndLinkEdges | old timer tag ignored | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-foreign-not-counted | MaapHost.StaleTagsForeignInputsAndLinkEdges |  | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-half-attach | MaapHost.AttachRefusalsAndTimerWrap | no partial attachment | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-interface-zero | MaapHost.InterfaceIsolationAndRangeEnvelope | record index selects state | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-no-range-filter | MaapHost.HMaapConflictLossAndRetry |  | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-filter-destination-ignored | MaapHost.HMaapFilterTupleAndRate |  | `sw/firmware/ctrl/host/mbx_model.c` |
| control / maap-late-service | MaapHost.HMaapTimerCommitsAndIntervals | H-MAAP original timer deadline | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-stall-unqueued | MaapHost.HMaapBacklogAndStallNeverRestartClock |  | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-app-channel-closed | MaapHost.ExplicitAppComposition |  | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / maap-callback-work-overrun | MaapHost.CallbackWorkAndEveryOutputCount | callback work bound | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-ignored-input-late | MaapHost.IgnoredInputCommitsStateWithinOriginalBudget | state completion uses original RX budget | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-table-b7-0 | AllStates/MaapCell.TableB7/0 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-1 | AllStates/MaapCell.TableB7/1 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-2 | AllStates/MaapCell.TableB7/2 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-3 | AllStates/MaapCell.TableB7/3 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-4 | AllStates/MaapCell.TableB7/4 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-5 | AllStates/MaapCell.TableB7/5 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-6 | AllStates/MaapCell.TableB7/6 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-7 | AllStates/MaapCell.TableB7/7 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-8 | AllStates/MaapCell.TableB7/8 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-9 | AllStates/MaapCell.TableB7/9 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-10 | AllStates/MaapCell.TableB7/10 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-11 | AllStates/MaapCell.TableB7/11 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-12 | AllStates/MaapCell.TableB7/12 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-13 | AllStates/MaapCell.TableB7/13 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-14 | AllStates/MaapCell.TableB7/14 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-15 | AllStates/MaapCell.TableB7/15 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-16 | AllStates/MaapCell.TableB7/16 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-table-b7-17 | AllStates/MaapCell.TableB7/17 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-allocation-seam-disconnected | MaapHost.AcquiredRangeFeedsExistingCsrPath | allocation reaches AAF CSR | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-app-missing-rx-interrupt | MaapHost.AppWaitWakesForMaapWithinBudget | accepted MAAP wakes idle loop | `sw/firmware/ctrl/loop/ctrl_loop.c` |
| control / maap-begin-down-forgets-range | MaapCore.BeginBeforePortOperationalRetainsRange | Begin supplied range survives port down | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-restart-reuses-range | MaapCore.RestartDrawsNewRange | fixed seed Restart draws a new range | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-reverse-five-octets | MaapCore.PriorityAfterTiedOctets | every reversed octet decides | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-compare-mac-lsb-only | MaapCore.PriorityAfterTiedOctets | every reversed octet decides | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-csr-select-listener | MaapCsr.EveryStreamAddressAndLossGate | stream destination base plus index | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-csr-enable-before-programming | MaapCsr.AdmissionAfterEveryDestinationWrite | enables follow every destination word | `sw/firmware/ctrl/maap/maap_csr.c` |
| control / maap-poll-first-interface-only | MaapHost.InterfaceOneStallDrainsWithinBudget | interface 1 poll drains deferred output | `sw/firmware/ctrl/maap/maap_mbx.c` |
| control / maap-generic-initial-handles-conflict | AllStates/MaapCell.TableB7/0 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-generic-probe-state-defends | AllStates/MaapCell.TableB7/12 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-generic-probe-defend-uses-priority | AllStates/MaapCell.TableB7/10 | Table B.7 | `sw/firmware/ctrl/maap/maap.c` |
| control / maap-generic-equal-mac-wins | MaapCore.ReverseOctetPriority | equal MAC is not lower | `sw/firmware/ctrl/maap/maap.c` |
| control / r2-saved-range-never-consumed | MaapCore.LinkBounceDrawsAfterSuppliedRange | link bounce draws after consuming supplied range | `sw/firmware/ctrl/maap/maap.c` |
| SRP / startup-vid | StartupDeclaresTalkersDomainAndVlan | d.value | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / short-leave | LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline | Unexpected mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / asking-is-ready | RegisteredListenerSubtypeChangeRevokesPermission | adapter.ifs[0].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / ignore-link | InterfaceStateDoesNotCross | adapter.ifs[i].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / failed-listener-ready | SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer | declared | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / ignore-peer-domain | DomainUsesPeerPriorityAndVlan | domain.priority | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / rx-overtakes-owed | RefusedMailboxRetainsOwedFrameAndDefersInput | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / rx-overtakes-expiry | ExpiryBacklogPrecedesSamePassReceive | adapter.stops | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reentry-uncounted | ReentryFromOutputIsRefusedAndCounted | adapter.reentries | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / invalid-vid | InvalidBindingsAndDuplicateBindingsPreserveState | srp_mbx_bind | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / failed-init-leaks | ExhaustionDuringEachStartupStageReleasesEveryBlock | ctrl_pool_in_use | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / missing-port-accepted | MissingBootDependenciesRefuseBeforeAttachment | srp_mbx_init | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / attach-nonatomic | AttachmentFailureIsAtomicAndDetachesAfterLoopReset | srp_mbx_attach | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / malformed-uncounted | InvalidFramesHaveNoReservationSideEffects | adapter.malformed | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reset-skips-recreate | RecreateAllocationFailureIsCountedAndRetried | adapter.ifs[0].msrp | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / readyfailed-ignored | ReadyFailedAndUninterestingStreamsAreSeparated | Actual function call count | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / foreign-domain-stored | DomainFilterAndDuplicateDoNotGrowDeclarations | ctrl_pool_in_use | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / foreign-vlan-stored | MvrpAcceptsOnlyCurrentDomainVid | ctrl_pool_in_use | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / sink-da-ignored | WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt | declared | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / admission-ceiling-ignored | AdmissionUsesBandwidthAndEthernetMinimum | admitted[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / domain-refusal-lost | DomainExhaustionPreservesOldDeclarationUntilRetry | domain.vid | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / listener-refusal-lost | SinkDeclarationExhaustionRetriesWithoutLosingBinding | declared | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / other-link-cancels-owed | LinkLossCancelsItsOwedFrameOnly | adapter.owed_len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / duplicate-tick-owner | OneLoopOwnsTheGlobalCentisecondDispatch | srp_mbx_attach | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / binding-debug-guard | SynchronousBindingFromOutputAsserts | failed to die | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-debug-guard | SynchronousReceiveFromOutputAsserts | failed to die | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / tick-debug-guard | SynchronousTickFromOutputAsserts | failed to die | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / licence-before-vlan | ListenerBeforeVlanCommitCannotStartTalker | joined | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / unbind-shared-listener | SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / withdraw-bound-domain | BoundOldDomainVlanSurvivesDomainChange | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / withdraw-same-domain | PriorityOnlyDomainChangeKeepsVlanMembership | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / sink-vlan-refusal-lost | SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent | vlan_requested | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / ready-before-vlan | SinkMembershipCommitsBeforeReadyAtStartup | joined | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / latency-missing-startup | SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget | commits.size() | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / latency-domain-unserviced | SrpLatency.ReceiveStateMalformedDomainAndListenerPaths | domain.vid | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / latency-leave-origin | SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog | Unexpected mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / latency-relaxed-budget | SrpLatency.FullRingRetainsOriginalOriginAndElevenMillisecondStallFails | service_limit | `sw/firmware/ctrl/test/srp_latency_policy.hpp` |
| SRP / walk-domain-ignored | SrpWalk.CertifiedTwoClassDomainVectorAdoptsOnlyClassA | domain.vid | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / walk-match-da-ignored | SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal | declared | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / walk-leave-shortened | SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener | Unexpected mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / walk-startup-is-join | SrpWalk.ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / walk-malformed-uncounted | SrpWalk.PerInterfaceWireIdentityAndUnknownOrTruncatedInput | adapter.malformed | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / shape-last-output-missing | EveryGeneratedOutputIsDeclaredAndEverySinkFits | outputs | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / tag-overhead-omitted | AdmissionStraddlesTheExactEthernetCeiling | admitted[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / preamble-ifg-omitted | AdmissionStraddlesTheExactEthernetCeiling | admitted[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / ninety-percent-ceiling | AdmissionStraddlesTheExactEthernetCeiling | admitted[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / readyfailed-callback-stop | ReadyToReadyFailedNeverGlitchesAnActiveLicence | mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / short-link-interruption-ignored | AdjacentLinkEdgesResetDomainAndAllPriorRegistrations | domain.priority | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / old-prefix-accepted | LinkEventsDiscardOnlyTheirPublishedReceivePrefix | mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / shared-identity-overwritten | SharedIdentityReconcilesBothBindingOrdersOnTheWire | last | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / event-reentry-unguarded | EventReentryAndSinkCapacityAreGuarded | adapter.reentries | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / failed-interface-starves-peer | RecreateAllocationFailureIsCountedAndRetried | other_sent | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / backlogged-old-prefix-accepted | OldReceiveBacklogCannotRegisterAcrossLinkRestart | mock function call | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / link-level-loss-ignored | LinkLevelLossAndFirstDownEventAreFailClosed | adapter.ifs[0].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reset-leaks-owned-participants | ExhaustedPoolStillReusesOwnedBlocksOnLinkReset | adapter.refused | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / downlink-receive-accepted | OldReceiveBacklogCannotRegisterAcrossLinkRestart | adapter.ifs[i].registered[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / delayed-in-listener | InListenerWithdrawalRevokesLicenceImmediately | adapter.ifs[i].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / delayed-in-talker | InTalkerWithdrawalImmediatelyWithdrawsListener | declared | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / attach-ignores-current-link | ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord | adapter.ifs[i].link | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / cancelled-link-never-recovers | CancelledLinkRecordRecoversFromLevelAndFencesOldReceive | adapter.ifs[i].link | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / rebind-loses-shared-applicant | SharedRebindKeepsOnlyTheRemainingEligibleRequest | left | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / consecutive-rebind-loses-applicant | ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation | left | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / joining-binding-loses-applicant | JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / applicant-inherited-across-streams | ReboundStreamCannotInheritAnotherStreamsReady | ready | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / final-unbind-withdraws-domain-vid | FinalDomainVidUnbindKeepsSrClassMembership | d.event | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / last-ineligible-vid-leaks | LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder | vlan_left | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reset-keeps-owed-domain | RefusedPeerDomainDoesNotSurviveLinkRestart | domain.vid | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reset-keeps-sink-vlan | SinkVlanRedeclaredBeforeReadyAfterLinkRestart | vlan | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / shared-ready-uses-first-vlan | SharedReadyWaitsForTheMatchingBindingsOwnVlan | vlan | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / milan-rapid-leave-leaks-to-mvrp | MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline | registered() | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retry-removed | SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / partial-receive-retry-removed | SrpRetry.PartialPayloadKeepsLaterAttributesAndDoesNotRepeatStop | domain.vid | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-record-lost | SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-refusal-malformed | SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission | adapter.malformed | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-overtakes-retained | SrpRetry.LaterRecordsCannotOvertakeRetainedInterface | loop.stats.rx_records | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / reset-keeps-retained-receive | SrpRetry.LinkResetCancelsRetainedPayloadAndFencesLaterOldRecords | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / peer-reset-cancels-retained-receive | SrpRetry.OtherInterfaceResetPreservesRetainedPayload | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / destroy-keeps-retained-receive | SrpRetry.DestroyCancelsRetainedPayloadBeforeReinitialization | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / bind-overtakes-retained-receive | SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission | srp_mbx_bind | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / composition-attach-omitted | SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources | app.loop.n_ticks | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / composition-srp-irq-omitted | SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources | model.irq_enable | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / composition-srp-tick-omitted | SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources | app.loop.stats.ticks | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / recreated-receive-retry-removed | SrpRetry.FailedParticipantRecreationRetainsFreshReceive | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / mvrp-receive-retry-removed | SrpRetry.RetainedMvrpUsesItsOriginalParticipant | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retry-passes-owed | SrpRetry.RetainedReceiveWaitsForOwedTransmit | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retry-passes-backlog | SrpRetry.RetainedReceiveWaitsForTickAndLifecycleBacklogs | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / future-receive-refused | SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped | adapter.ifs[0].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / invalid-suffix-uncounted | SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped | adapter.malformed | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / composition-refusal-ignored | SrpApp.AttachRefusalPreservesExistingComposition | ctrl_app_attach_srp | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / recovery-latency-retry-removed | SrpLatency.ReceiveRecoveryKeepsOriginalArrivalBudget | adapter.ifs[0].active[0] | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retention-unbounded | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retention-short | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-retention-late | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-discard-uncounted | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-discard-malformed | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.malformed | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-discard-as-success | SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-queue-renews-deadline | SrpRetry.QueuedRefusalKeepsOriginalArrivalDeadlineAcrossClockWrap | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-first-refusal-never-expires | SrpRetry.QueuedRefusalKeepsOriginalArrivalDeadlineAcrossClockWrap | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-expiry-precedes-recovery | SrpRetry.RecoveryAtDeadlineStillAppliesTheCompleteRecord | adapter.received | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-recreate-never-expires | SrpRetry.FailedRecreationCannotRetainInputBeyondItsDeadline | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-flood-unbounded | SrpRetry.DomainFloodCannotDelayLaterRapidLeave | adapter.pending_rx.len | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / receive-deadline-not-modular | SrpRetry.RetainedDeadlineCrossesClockWrapWithoutEarlyDiscard | adapter.rx_discarded | `sw/firmware/ctrl/srp/srp_mbx.c` |
| SRP / four-way-srp-irq-missing | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 exact four-channel receive and event interrupt mask | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / four-way-srp-wake-missing | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 idle loop wakes for SRP alone | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / four-way-acmp-enable-lost | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 four receive channels and no others | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / four-way-unbound-irq-enabled | AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen | U6 exact four-channel receive and event interrupt mask | `sw/firmware/ctrl/app/ctrl_app_srp.c` |
| SRP / four-way-bound-drops-srp | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound | F6 four modules count each shared event record once | `sw/firmware/ctrl/app/ctrl_app.h` |
| SRP / four-way-bound-duplicates-events | AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound | F6 four modules count each shared event record once | `sw/firmware/ctrl/app/ctrl_app.h` |

## Saved-state campaign

The inherited NVM suite is also run with its complete 109-plant table.

| Plant | Checks that must fail | Modified source | Shape override |
| --- | --- | --- | --- |
| no_crc_check | torn_falls_back, verdict_parity | nvm_store.c | default |
| no_crc_anywhere | powercut | nvm_store.c, nvm_klj2.c | default |
| pick_older | newer_wins | nvm_store.c | default |
| pick_no_wrap | newer_wins | nvm_store.c | default |
| tie_picks_b | newer_wins | nvm_store.c | default |
| erased_header_only | verdict_parity, codec_parity | nvm_klj2.c | default |
| no_ascending | verdict_parity, codec_parity | nvm_klj2.c | default |
| overrun_as_rec | verdict_parity, codec_parity | nvm_klj2.c | default |
| incomplete_accepted | verdict_parity, codec_parity | nvm_klj2.c | default |
| erased_payload_end_bound | codec_erased_loaded_prefix | nvm_klj2.c | default |
| erased_payload_guard_early | codec_erased_loaded_prefix | nvm_klj2.c | default |
| erased_payload_guard_late | codec_erased_loaded_prefix | nvm_klj2.c | default |
| room_unchecked | codec_room | nvm_klj2.c | default |
| short_prefix_read_on | codec_loaded_prefix | nvm_klj2.c | default |
| short_prefix_as_len | codec_loaded_prefix | nvm_klj2.c | default |
| header_guard_early | codec_loaded_prefix | nvm_klj2.c | default |
| header_guard_late | codec_loaded_prefix | nvm_klj2.c | default |
| payload_guard_early | codec_loaded_prefix | nvm_klj2.c | default |
| payload_guard_late | codec_loaded_prefix | nvm_klj2.c | default |
| lookup_index_unbounded | codec_lookups | nvm_klj2.c | default |
| long_crc_unchecked | long_container_reads | nvm_store.c | default |
| unread_not_counted | long_container_reads | nvm_store.c | default |
| no_version_check | wrong_version_falls_back | nvm_klj2.c | default |
| no_blank_verdict | blank_boot | nvm_klj2.c | default |
| pad_not_zero | blank_boot | nvm_klj2.c | default |
| header_n_rec | blank_boot, first_commit_bytes | nvm_klj2.c | default |
| frame_crc_init | vector_round_trip, change_commit_bytes | nvm_klj2.c | default |
| no_blank_stage | blank_boot | nvm_store.c | default |
| verdict_not_named | both_torn_blank | nvm_store.c | default |
| stage_not_rechecked | read_flip_at_stage | nvm_store.c | default |
| stage_seq_unchecked | read_alias_at_stage | nvm_store.c | default |
| select_on_unchecked_reread | read_flip_boot | nvm_store.c, nvm_store.c | default |
| slot_read_fail_ignored | read_fail_boot | nvm_store.c | default |
| unread_not_held | authority_unknown, fallback_restage, read_disagreement | nvm_store.c | default |
| read_not_retried | read_fail_boot, authority_unknown | nvm_store.c | default |
| refusal_unconfirmed | authority_unknown, read_disagreement, reads_differ_in_verdict, reads_agree_in_digest_not_length | nvm_store.c | default |
| blank_unconfirmed | authority_unknown | nvm_store.c | default |
| refusal_by_verdict | read_disagreement | nvm_store.c | default |
| agreement_by_digest | reads_agree_in_digest_not_length | nvm_store.c | default |
| disagreement_not_counted | reads_differ_in_verdict, reads_agree_in_digest_not_length | nvm_store.c | default |
| restage_not_retried | read_flip_at_stage, read_alias_at_stage, read_fail_boot | nvm_store.c | default |
| fallback_restage_unchecked | fallback_restage | nvm_store.c | default |
| no_rollback | apply_fault_rolls_back, settle_fault_rolls_back | nvm_store.c | default |
| rollback_failure_ignored | rollback_fault_closes | nvm_store.c | default |
| release_on_closed | rollback_fault_closes | nvm_store.c | default |
| fault_as_refusal | apply_fault_rolls_back, binding_walk | nvm_store.c | default |
| refusal_aborts | refused_keeps_default | nvm_store.c | default |
| settle_fault_ignored | settle_fault_rolls_back | nvm_store.c | default |
| settle_after_names | golden_restore | nvm_store.c | default |
| no_settle_without_names | settle_after_the_last_record | nvm_store.c | default |
| shape_not_checked | shape_mismatch_disables_persistence | nvm_store.c | default |
| shape_mismatch_released_unproven | shape_mismatch_disables_persistence | nvm_store.c | default |
| release_before_apply | golden_restore | nvm_store.c | default |
| apply_erased | erased_records | nvm_store.c | default |
| model_ready_ignored | model_unproven_closes | nvm_store.c | default |
| bindings_skipped_unproven | model_unproven_closes | nvm_store.c | default |
| d3_rollback_takes_bindings | apply_fault_rolls_back, settle_fault_rolls_back | nvm_store.c | default |
| bindings_in_d3_walk | binding_walk, golden_restore | nvm_store.c, nvm_store.c | default |
| binding_fault_aborts_d3 | binding_walk | nvm_store.c | default |
| binding_fault_keeps_preloads | binding_walk | nvm_store.c | default |
| quiet_period | debounce | nvm_store.c | default |
| no_debounce | debounce | nvm_store.c | default |
| capture_leaves_window_armed | debounce | nvm_store.c | default |
| taken_off_by_one | debounce | nvm_store.c | default |
| taken_while_capturing | capture_window_edges | nvm_store.c | default |
| taken_after_last_latch | capture_window_edges | nvm_store.c | default |
| change_of_no_record | change_unknown_record | nvm_store.c | default |
| nothing_to_save_framed | nothing_to_save | nvm_store.c | default |
| dr2b_ignores_durability | failed_commit_not_skipped | nvm_store.c | default |
| no_dr2b | unchanged_no_erase | nvm_store.c | default |
| console_force_ignored | console_commit_unchanged | nvm_store.c | default |
| no_backoff | media_failures | nvm_store.c | default |
| unbounded_attempts | media_failures | nvm_store.c | default |
| budget_rearmed_by_change | dr2c_unchanged_set | nvm_store.c | default |
| budget_rearmed_by_capture | dr2c_unchanged_set | nvm_store.c | default |
| commit_now_overrides_exhaustion | dr2c_console | nvm_store.c | default |
| commit_now_ignores_backoff | dr2c_console | nvm_store.c | default |
| success_forgives_exhaustion | recovers_after_failure, dr2c_unchanged_set | nvm_store.c | default |
| stale_kept | recovers_after_failure | nvm_store.c | default |
| dr2b_keeps_stale | recovers_after_failure | nvm_store.c | default |
| no_blankcheck | media_failures | nvm_store.c | default |
| blankcheck_first_stretch_only | blankcheck_tail | nvm_store.c | default |
| blankcheck_read_fail_ignored | media_verdicts | nvm_store.c | default |
| no_verify | media_failures, failed_commit_not_skipped | nvm_store.c | default |
| verify_skips_last_stretch | verify_tail | nvm_store.c | default |
| verify_read_fail_ignored | media_verdicts | nvm_store.c | default |
| program_refusal_ignored | media_verdicts | nvm_store.c | default |
| no_timeout | media_failures | nvm_store.c | default |
| same_sequence | change_commit_bytes | nvm_store.c | default |
| refused_slot_overwritten | refused_slot_kept | nvm_store.c | default |
| no_blank_slot_takes_b | first_commit_no_blank_slot | nvm_store.c | default |
| erase_authoritative | change_commit_bytes, powercut | nvm_store.c, nvm_store.c | default |
| descending_pages | first_commit_bytes | nvm_store.c, nvm_store.c | default |
| capture_in_one_step | service_bound | nvm_store.c | default |
| spin_wait | service_bound | nvm_store.c | default |
| litespi_no_wren | first_commit_bytes | plat/nvm_flash_litespi.c | default |
| litespi_status_ignored | first_commit_bytes | plat/nvm_flash_litespi.c | default |
| litespi_no_guard | port_guard | plat/nvm_flash_litespi.c, plat/nvm_flash_litespi.c | default |
| phc_time | time_base | plat/nvm_flash_litespi.c | default |
| clock_not_accumulated | time_base | plat/nvm_flash_litespi.c | default |
| ticks_per_us_truncated | port_clock, time_base | plat/nvm_flash_litespi.c, plat/nvm_flash_litespi.c | endstation_arty_current |
| xfer_unbounded | port_stall | plat/nvm_flash_litespi.c, plat/nvm_flash_litespi.c | default |
| open_unbounded | port_stall | plat/nvm_flash_litespi.c | default |
| call_deadline_ignored | port_deadline, port_drain_deadline | plat/nvm_flash_litespi.c | default |
| drain_deadline_ignored | port_drain_deadline | plat/nvm_flash_litespi.c | default |
| read_runs_past_device | port_read_range | plat/nvm_flash_litespi.c | default |
| program_across_page | port_write_refusals | plat/nvm_flash_litespi.c | default |
| deadline_per_wait | port_deadline | plat/nvm_flash_litespi.c | default |
| stall_ignored | port_stall | plat/nvm_flash_litespi.c | default |
