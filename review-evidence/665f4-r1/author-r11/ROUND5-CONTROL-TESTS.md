[A560]

# Round 5 control test-to-defect map

Head: `500b8f64443777685e6a54049d933476710d26f0`. All 100 control plants pass the existing named-failure grader; every listed additional kill is required. The definitions and grader are unchanged.

| Plant | Changed production file | Required arm | Named test or parameterized prefix | Required failure text |
|---|---|---|---|---|
| `reentry-guard-removed` | `sw/firmware/ctrl/adp/adp.c` | `reentry_debug` | `AdpReentry.AdvertiseInlineExpiry` | `inline ADVERTISE expiry asserts` |
| `reentry-guard-removed` | `sw/firmware/ctrl/adp/adp.c` | `reentry_debug` | `AdpReentry.DelayInlineExpiryOnGmChange` | `inline DELAY expiry asserts` |
| `reentry-guard-removed` | `sw/firmware/ctrl/adp/adp.c` | `reentry_release` | `AdpReentry.AdvertiseInlineExpiry` | `inline ADVERTISE expiry is counted` |
| `reentry-guard-removed` | `sw/firmware/ctrl/adp/adp.c` | `reentry_release` | `AdpReentry.DelayInlineExpiryOnGmChange` | `inline DELAY expiry is counted` |
| `reentry-uncounted` | `sw/firmware/ctrl/adp/adp.c` | `reentry_release` | `AdpReentry.AdvertiseInlineExpiry` | `inline ADVERTISE expiry is counted` |
| `reentry-not-ignored` | `sw/firmware/ctrl/adp/adp.c` | `reentry_release` | `AllPorts/AdpPortEntry.RefusesBeforeTouchingState/` | `callback leaves core state unchanged` |
| `departing-keeps-index` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/` | `available_index` |
| `departing-sends-zero` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A10toA14DepartingIndex` | `A10 SHUTDOWN in WAITING` |
| `available-replaces-owed-departing` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A15OwedDepartingAcrossARestart` | `A15 with room, the next poll sends the owed ENTITY_DEPARTING first` |
| `available-passes-owed-departing` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A17RoomBackBeforeAPoll` | `A17 room back and TMR_DELAY expiring before a poll` |
| `second-departing-dropped` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A16SecondShutdownQueuesItsOwn` | `A16 a SHUTDOWN while one is owed queues its own` |
| `second-shutdown-overwrites-index` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A16SecondShutdownQueuesItsOwn` | `A16 a SHUTDOWN while one is owed queues its own` |
| `link-loss-drops-owed-departing` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A18LinkLossKeepsTheOwedDeparting` | `A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING` |
| `gm-change-drops-owed-available` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | `A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed` |
| `discover-drops-owed-available` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | `A19 so does an ENTITY_DISCOVER` |
| `stray-expiry-drops-owed-available` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | `A19 and a stray expiry, which is counted` |
| `link-loss-keeps-owed-available` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A20LinkLossDropsTheOwedAvailable` | `A20 a link loss drops the owed ENTITY_AVAILABLE at once` |
| `departing-queue-unbounded` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/` | `E5 64 SHUTDOWNs behind a full ring, expiry taken before the room: the ENTITY_AVAILABLE is committed` |
| `coalesced-departing-uncounted` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A21DepartingCapacity` | `A21 the next SHUTDOWN is coalesced into the queued one and counted` |
| `coalesce-drops-queued-departing` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A21DepartingCapacity` | `A21 the next SHUTDOWN is coalesced into the queued one and counted` |
| `coalesce-overwrites-oldest-index` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A21DepartingCapacity` | `A21 the next SHUTDOWN is coalesced into the queued one and counted` |
| `own-discover-discarded` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING` | `RCV_ADP_DISCOVER(own eid) x WAITING` |
| `down-answers-discover` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN` | `RCV_ADP_DISCOVER(eid 0) x DOWN` |
| `link-down-departs` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING` | `LINK_DOWN x WAITING: frames committed` |
| `gm-change-ignored` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING` | `GM_CHANGE x WAITING` |
| `delay-ignores-link-down` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed` | `LINK_DOWN x DELAY` |
| `shutdown-in-down-departs` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN` | `SHUTDOWN x DOWN` |
| `advertise-expiry-skips-delay` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING` | `TMR_ADVERTISE x WAITING` |
| `advertise-period-wrong` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed` | `TMR_DELAY x DELAY(timer armed)` |
| `link-up-draws-startup-kind` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN` | `LINK_UP x DOWN` |
| `draw-kinds-merged` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A9DrawKinds` | `A9 every startup draw` |
| `foreign-discover-answered` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A3toA5DiscoverAndDiscard` | `A4 a foreign DISCOVER` |
| `frame-misses-config-index` | `sw/firmware/ctrl/adp/adp.c` | `walk` | `AdpWalk.P11ConfigurationIndexBytes` | `P11` |
| `stale-tag-accepted` | `sw/firmware/ctrl/adp/adp_mbx.c` | `adp` | `AdpAdapter.B1StaleTagDiscarded` | `B1 an expiry of the arm a GM_CHANGE replaced` |
| `latency-extra-read` | `sw/firmware/ctrl/adp/adp_mbx.c` | `adp` | `AdpLatency.C0toC6EveryResponsePath` | `C0 LINK_UP -> TMR_DELAY armed` |
| `pool-free-leaks` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P2ReleaseAndBadFrees` | `P2 a released block` |
| `calloc-overflow-unchecked` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P3CallocZeroesAndRefusesAWrap` | `P3 calloc refuses` |
| `pool-double-free-accepted` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P2ReleaseAndBadFrees` | `P2 a double free` |
| `debug-truncation-uncounted` | `sw/firmware/ctrl/port/ctrl_debug.c` | `port` | `DebugSink.S2TruncatedToTheLine` | `S2 the truncation` |
| `tick-count-ignored` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `Loop.L4TickFanOut` | `L4 every centisecond` |
| `rx-pass-unbounded` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `Loop.L2PerPassRxBound` | `L2 a pass takes at most` |
| `poll-owes-nothing` | `sw/firmware/ctrl/adp/adp_mbx.c` | `adp` | `AdpOwed.E0toE3PendingWake` | `E1 the loop does not sleep while a frame is owed` |
| `events-halved` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `adp` | `AdpBacklog.F0toF7FullBacklogs` | `F2 all 16 event records are taken by pass` |
| `rx-before-events` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `adp` | `AdpBacklog.F0toF7FullBacklogs` | `F1 events first` |
| `carried-ticks-overwritten` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `Loop.L8TickRecordWhileCarried` | `L8 a TICK record taken while centiseconds are carried` |
| `tick-slice-unbounded` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `Loop.L7TickSlices` | `L7 at most CTRL_LOOP_TICKS_PER_PASS` |
| `owed-ticks-let-it-sleep` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `Loop.L7TickSlices` | `L7 and the loop keeps passing` |
| `filter-opened-before-eid` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `LoopBring.L1OpenOrder` | `L1 OWN_EID is written before` |
| `rx-no-resync` | `sw/firmware/ctrl/mbx/mbx.c` | `port` | `Driver.D1MalformedRecordResynchronises` | `D1 and the ring is resynchronised` |
| `rx-no-resync` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `Records/DriverMalformed.D7RefusedAndResynchronised/` | `and the ring is resynchronised to RX_HEAD` |
| `tx-overfills` | `sw/firmware/ctrl/mbx/mbx.c` | `port` | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` | `D3 a held merge fills the ring` |
| `lanes-big-endian` | `sw/firmware/ctrl/mbx/mbx_wire.h` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/` | `F1 frame byte k is ring word` |
| `frame-sources-from-sinks` | `sw/firmware/ctrl/adp/adp.c` | `entity` | `Fabric/EntityField.MatchesTheFabric/talker_stream_sources` | `talker_stream_sources` |
| `pool-falls-back-to-heap` | `sw/firmware/ctrl/port/shlan_port.c` | `port` | `Pool.P4ShlanFunctionsDrawOnTheBoundPool` | `P4 shlan_malloc and shlan_calloc draw on the bound pool` |
| `pool-falls-back-to-heap` | `sw/firmware/ctrl/port/shlan_port.c` | `rv32` | `` | `symbols outside the C library` |
| `model-rate-unlimited` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/RateLimit` | `T0 the frames past it count in RATE_DROP` |
| `seq-not-stamped` | `sw/firmware/ctrl/mbx/mbx.c` | `port` | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` | `D3 ACMP, ACMP, AECP committed by the driver` |
| `model-round-robin` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder` | `X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame` |
| `model-gm-hi-live` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot` | `G0 GM_HI reads the snapshot` |
| `zero-byte-class-accepted` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P5ClassTablesAndArenasRefused` | `P5 a class of zero-byte blocks is refused` |
| `zero-size-refusal-uncounted` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P6CallocOfNothingAndOnAnExhaustedPool` | `P6 and both refusals are counted` |
| `foreign-free-uncounted` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P7FreeBelowTheArenaRefused` | `P7 a free below the first class is refused and counted` |
| `port-pool-unreported` | `sw/firmware/ctrl/port/shlan_port.c` | `port` | `Pool.P8PortLayerUnbound` | `P8 the bound pool is the one reported` |
| `pool-follows-a-cut-free-list` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P9AFreeListShorterThanItsCountIsExhausted` | `crashed on signal 11` |
| `pool-cut-list-refuses-outright` | `sw/firmware/ctrl/port/ctrl_pool.c` | `port` | `Pool.P9AFreeListShorterThanItsCountIsExhausted` | `P9 a class whose list ends before its count` |
| `encoding-failure-swallowed` | `sw/firmware/ctrl/port/ctrl_debug.c` | `port` | `DebugSink.S3UnencodablePrintDiscarded` | `S3 an encoding failure is returned` |
| `rx-binds-no-function` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `LoopBring.L9TablesRefuseNullAndOverflow` | `L9 a channel bound to no function is refused` |
| `seed-left-at-zero` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A22GeneratorNeverStuckAtZero` | `A22 an entity id whose words cancel the seed constant` |
| `enable-not-idempotent` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A23RepeatedEnableOrDisableChangesNothing` | `A23 an enable while enabled draws and arms nothing` |
| `other-subtype-accepted` | `sw/firmware/ctrl/adp/adp.c` | `adp` | `AdpCore.A24OtherEtherTypeOrSubtypeDiscarded` | `A24 a DISCOVER under another EtherType or subtype is discarded` |
| `app-binds-pool-after-the-mailbox` | `sw/firmware/ctrl/app/ctrl_app.c` | `unit` | `AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox` | `unsatisfied and active` |
| `app-starts-on-an-uncarved-pool` | `sw/firmware/ctrl/app/ctrl_app.c` | `unit` | `AppComposition.U1AnUncarvablePoolStartsNothing` | `over-saturated and active` |
| `major-unchecked` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `AppComposition.U1AnotherContractOpensNothing` | `U1 a bitstream carrying another contract is refused` |
| `major-unchecked` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major` | `U2 major differs` |
| `evt-words-unchecked` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words` | `U2 evt_words differs` |
| `step-waits-twice` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `unit` | `LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed` | `U3 every turn is one pass` |
| `maap-base-shifted` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D6MaapRangeWritten` | `D6 MAAP_BASE_LO holds the base's low word` |
| `tx-negative-fill` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D8TransmitRefusals` | `D8 a TX_TAIL more than a ring behind TX_HEAD is no room` |
| `unknown-event-decoded-as-tick` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt` | `D9 an event of a type the contract does not define` |
| `whole-field-loses-its-top-bit` | `sw/firmware/ctrl/mbx/mbx_wire.h` | `unit` | `DriverUnit.D10LanesAndFieldsAtTheirBounds` | `D10 and reads whole` |
| `slots-past-the-bank` | `sw/firmware/ctrl/adp/adp_mbx.c` | `unit` | `AdpAdapterUnit.B2SlotsPastTheTimerBankRefused` | `B2 slots past the fabric's timer bank` |
| `foreign-frame-uncounted` | `sw/firmware/ctrl/adp/adp_mbx.c` | `unit` | `AdpAdapterUnit.B3ForeignInterfaceCounted` | `B3 a record, a LINK and a GM` |
| `attach-ignores-poll-room` | `sw/firmware/ctrl/adp/adp_mbx.c` | `unit` | `AdpAdapterUnit.B4LoopWithNoRoomRefused` | `B4 a loop with no room for the poll is refused` |
| `mmio-offset-as-index` | `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | `unit` | `MmioPlatform.M1OneWordAtBasePlusOffset` | `M1 a write lands in the word at base + offset` |
| `wait-without-wfi` | `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | `unit` | `MmioPlatform.M2WaitIsThePlatformWfi` | `M2 each mbx_hal_wait() waits once` |
| `model-tag-stripped` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q1 tagged, it (adp): no RX record` |
| `model-tpid-matches-a-tuple` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q1 tagged, it (srp MSRP): no RX record` |
| `model-multicast-dst-ignored` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q2 to another destination MAC, it (adp)` |
| `model-ethertype-ignored` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q3 under another control EtherType, it (adp)` |
| `model-subtype-ignored` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q4 with an unassigned AVTP subtype, it (adp)` |
| `model-own-any-unicast` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q2 to another destination MAC, it (aecp, command)` |
| `model-own-mac-of-interface-0` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/OwnMacPerInterface` | `Q8 another interface's own MAC, or one on an index with no interface, reaches no ring` |
| `model-own-mac-hi-dropped` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks` | `R1 OWN_MAC_LO keeps every bit and OWN_MAC_HI keeps MAC[47:32] only` |
| `model-aecp-command-only` | `sw/firmware/ctrl/mbx/mbx_contract.h` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/AecpBothDirections` | `Q7 the CONTROLLER_AVAILABLE response for this controller reaches the AECP ring` |
| `model-mismatch-never-counted` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q2 to another destination MAC, it (adp): FILTER_MISMATCH counts it once` |
| `model-mismatch-counts-identity-refusals` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/TupleRejections` | `Q5 ENTITY_DISCOVER for another entity: FILTER_MISMATCH does not count it` |
| `model-mismatch-sets-no-err` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/FilterMismatchCount` | `Q9 a mismatch sets IRQ_STATUS.ERR` |
| `model-msg-type-off-by-one` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast` | `Q11 a DEFEND to this interface's own MAC reaches the MAAP ring` |
| `model-tuple-msg-type-ignored` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast` | `Q11 a PROBE to this interface's own MAC: no RX record` |
| `model-msg-type-refusal-uncounted` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast` | `Q11 a PROBE to this interface's own MAC: FILTER_MISMATCH counts it once` |
| `model-defend-any-unicast` | `sw/firmware/ctrl/host/mbx_model.c` | `model` | `Suite/MbxModelGroup.PassesOnTheModel/MaapDefendToOwnUnicast` | `Q11 a DEFEND to a unicast MAC no interface owns: no RX record` |
| `own-mac-unguarded` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount` | `D11 an interface past the contract's is refused` |
| `own-mac-halves-swapped` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount` | `D11 OWN_MAC_LO holds MAC[31:0]` |
| `own-mac-halves-swapped` | `sw/firmware/ctrl/mbx/mbx.c` | `port` | `Driver.D12OwnMacAndMismatchOnTheModel` | `D12 an AEM_COMMAND to it on interface 0 passes` |
| `mismatch-read-from-bus-err` | `sw/firmware/ctrl/mbx/mbx.c` | `unit` | `DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount` | `D11 FILTER_MISMATCH is read as its COUNT field` |
| `mismatch-read-from-bus-err` | `sw/firmware/ctrl/mbx/mbx.c` | `port` | `Driver.D12OwnMacAndMismatchOnTheModel` | `D12 FILTER_MISMATCH reads the one tuple failure` |
| `own-mac-after-the-channels-open` | `sw/firmware/ctrl/loop/ctrl_loop.c` | `port` | `LoopBring.L1OpenOrder` | `L1 every interface's OWN_MAC is written before any channel opens` |
| `app-own-mac-not-the-entity-mac` | `sw/firmware/ctrl/app/ctrl_app.c` | `unit` | `AppComposition.U4EveryInterfaceOwnsTheEntityMacBeforeAChannelOpens` | `OWN_MAC is the entity's MAC` |
