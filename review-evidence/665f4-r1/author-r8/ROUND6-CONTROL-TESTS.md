[A560]

# Round 6 control test-to-defect map

Head: `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`. All 196 control/MAAP plants are covered by two disjoint shards. Each listed additional kill is required.

| Plant | Changed file | Arm | Named test or prefix | Failure text |
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
| `maap-down-start-keeps-owner` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReleaseLossAndRetry` | `starting down withdraws the prior owner` |
| `maap-initial-send-absent` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `initial PROBE is immediate` |
| `maap-retransmit-count` | `sw/firmware/ctrl/maap/maap.h` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `three retransmissions remain` |
| `maap-probe-count-not-decremented` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `retransmission decrements once` |
| `maap-wire-version` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `B.2 complete PROBE bytes` |
| `maap-wire-length` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `B.2 complete PROBE bytes` |
| `maap-wire-source` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `B.2 complete PROBE bytes` |
| `maap-wire-padding` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitialAndThreeRetransmissions` | `B.2 complete PROBE bytes` |
| `maap-constant-probe_base` | `sw/firmware/ctrl/maap/maap.h` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `` |
| `maap-constant-probe_variation` | `sw/firmware/ctrl/maap/maap.h` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `` |
| `maap-constant-announce_base` | `sw/firmware/ctrl/maap/maap.h` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `` |
| `maap-constant-announce_variation` | `sw/firmware/ctrl/maap/maap.h` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `` |
| `maap-seed-clock-ignored` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `` |
| `maap-zero-seed-sticks` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ConstantsStrictTimersAndSeed` | `zero sum cannot lock generator` |
| `maap-biased-random-bucket` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.UniformDrawRejectsIncompleteBucket` | `incomplete random bucket rejected` |
| `maap-numeric-mac-priority` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReverseOctetPriority` | `least significant octet decides first` |
| `maap-defend-multicast` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DefendEchoAndIntersection` | `echo request and exact intersection` |
| `maap-defend-echo-own-range` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DefendEchoAndIntersection` | `echo request and exact intersection` |
| `maap-intersection-too-long` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DefendEchoAndIntersection` | `echo request and exact intersection` |
| `maap-adjacent-overlaps` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DisjointAdjacentZeroAndDefendRange` | `half open intervals` |
| `maap-zero-count-conflicts` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DisjointAdjacentZeroAndDefendRange` | `half open intervals` |
| `maap-defend-checks-request` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.DisjointAdjacentZeroAndDefendRange` | `DEFEND tests conflict fields` |
| `maap-malformed-ethertype` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-subtype` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-version` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-reserved-zero` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-reserved-high` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-cdl-short` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-cdl-truncated` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-cdl-current` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-source-zero` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-source-group` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-destination` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-malformed-own-probe` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `malformed input is rejected` |
| `maap-valid-minimum-refused` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `B.2.3 recognized future` |
| `maap-future-version-refused` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.MalformedAndVersionCompatibility` | `B.2.3 recognized future` |
| `maap-range-end-off-by-one` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.InitAndPreferredRangeBounds` | `` |
| `maap-port-up-keeps-claim` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReleaseLossAndRetry` | `PortOperational invalidates acquired address` |
| `maap-release-keeps-enable` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReleaseLossAndRetry` | `released instance stays idle` |
| `maap-expiry-forgotten-on-stall` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.StalledOutputRetainsOrderAndOriginalExpiry` | `original expiry remains owed` |
| `maap-allocation-before-commit` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.StalledOutputRetainsOrderAndOriginalExpiry` | `allocation waits for committed ANNOUNCE` |
| `maap-probe-announce-reordered` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.StalledOutputRetainsOrderAndOriginalExpiry` | `` |
| `maap-overflow-uncounted` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.QueueBoundAndWithdrawal` | `overload is counted as failure` |
| `maap-poll-unbounded` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.QueueBoundAndWithdrawal` | `poll has bounded work` |
| `maap-release-leaves-output` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.QueueBoundAndWithdrawal` | `` |
| `maap-reentry-not-counted` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReentrantPortsAreCountedAndIgnored` | `all input guards fire` |
| `maap-debug-no-assert` | `sw/firmware/ctrl/maap/maap.c` | `maap_debug` | `MaapDebug.SynchronousExpiryAsserts` | `debug reentry assertion` |
| `maap-stream-index-missing` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.EveryStreamAddressAndLossGate` | `stream destination base plus index` |
| `maap-selection-not-restored` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.EveryStreamAddressAndLossGate` | `selection restored` |
| `maap-fabric-owner-kept` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.EveryStreamAddressAndLossGate` | `fabric MAAP disabled without touching seed` |
| `maap-loss-keeps-crf` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.EveryStreamAddressAndLossGate` | `loss closes both media gates` |
| `maap-count-mismatch-accepted` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.ShapesAndCountRefusal` | `wrong shape stays disabled` |
| `maap-crf-index-wrong` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.ShapesAndCountRefusal` | `CRF only shape` |
| `maap-timer-tag-ignored` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.StaleTagsForeignInputsAndLinkEdges` | `old timer tag ignored` |
| `maap-foreign-not-counted` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.StaleTagsForeignInputsAndLinkEdges` | `` |
| `maap-half-attach` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.AttachRefusalsAndTimerWrap` | `no partial attachment` |
| `maap-interface-zero` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap_if2` | `MaapHost.InterfaceIsolationAndRangeEnvelope` | `record index selects state` |
| `maap-no-range-filter` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.HMaapConflictLossAndRetry` | `` |
| `maap-filter-destination-ignored` | `sw/firmware/ctrl/host/mbx_model.c` | `maap` | `MaapHost.HMaapFilterTupleAndRate` | `` |
| `maap-late-service` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.HMaapTimerCommitsAndIntervals` | `H-MAAP original timer deadline` |
| `maap-stall-unqueued` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapHost.HMaapBacklogAndStallNeverRestartClock` | `` |
| `maap-app-channel-closed` | `sw/firmware/ctrl/app/ctrl_app.c` | `maap` | `MaapHost.ExplicitAppComposition` | `` |
| `maap-callback-work-overrun` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.CallbackWorkAndEveryOutputCount` | `callback work bound` |
| `maap-ignored-input-late` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap` | `MaapHost.IgnoredInputCommitsStateWithinOriginalBudget` | `state completion uses original RX budget` |
| `maap-table-b7-0` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/0` | `Table B.7` |
| `maap-table-b7-1` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/1` | `Table B.7` |
| `maap-table-b7-2` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/2` | `Table B.7` |
| `maap-table-b7-3` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/3` | `Table B.7` |
| `maap-table-b7-4` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/4` | `Table B.7` |
| `maap-table-b7-5` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/5` | `Table B.7` |
| `maap-table-b7-6` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/6` | `Table B.7` |
| `maap-table-b7-7` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/7` | `Table B.7` |
| `maap-table-b7-8` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/8` | `Table B.7` |
| `maap-table-b7-9` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/9` | `Table B.7` |
| `maap-table-b7-10` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/10` | `Table B.7` |
| `maap-table-b7-11` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/11` | `Table B.7` |
| `maap-table-b7-12` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/12` | `Table B.7` |
| `maap-table-b7-13` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/13` | `Table B.7` |
| `maap-table-b7-14` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/14` | `Table B.7` |
| `maap-table-b7-15` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/15` | `Table B.7` |
| `maap-table-b7-16` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/16` | `Table B.7` |
| `maap-table-b7-17` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/17` | `Table B.7` |
| `maap-allocation-seam-disconnected` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapHost.AcquiredRangeFeedsExistingCsrPath` | `allocation reaches AAF CSR` |
| `maap-app-missing-rx-interrupt` | `sw/firmware/ctrl/app/ctrl_app.c` | `maap` | `MaapHost.AppWaitWakesForMaapWithinBudget` | `accepted MAAP wakes idle loop` |
| `maap-begin-down-forgets-range` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.BeginBeforePortOperationalRetainsRange` | `Begin supplied range survives port down` |
| `maap-restart-reuses-range` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.RestartDrawsNewRange` | `fixed seed Restart draws a new range` |
| `maap-reverse-five-octets` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.PriorityAfterTiedOctets` | `every reversed octet decides` |
| `maap-compare-mac-lsb-only` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.PriorityAfterTiedOctets` | `every reversed octet decides` |
| `maap-csr-select-listener` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.EveryStreamAddressAndLossGate` | `stream destination base plus index` |
| `maap-csr-enable-before-programming` | `sw/firmware/ctrl/maap/maap_csr.c` | `maap` | `MaapCsr.AdmissionAfterEveryDestinationWrite` | `enables follow every destination word` |
| `maap-poll-first-interface-only` | `sw/firmware/ctrl/maap/maap_mbx.c` | `maap_if2` | `MaapHost.InterfaceOneStallDrainsWithinBudget` | `interface 1 poll drains deferred output` |
| `maap-generic-initial-handles-conflict` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/0` | `Table B.7` |
| `maap-generic-probe-state-defends` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/12` | `Table B.7` |
| `maap-generic-probe-defend-uses-priority` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `AllStates/MaapCell.TableB7/10` | `Table B.7` |
| `maap-generic-equal-mac-wins` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.ReverseOctetPriority` | `equal MAC is not lower` |
| `r2-saved-range-never-consumed` | `sw/firmware/ctrl/maap/maap.c` | `maap` | `MaapCore.LinkBounceDrawsAfterSuppliedRange` | `link bounce draws after consuming supplied range` |
