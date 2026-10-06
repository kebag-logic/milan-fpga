[A557]

# Firmware test-to-defect inventory

The tables name the original campaign oracles. A row is only passed when its named oracle rejected the planted defect; a compile failure does not count. Ctrl inventory: 76; store inventory: 106. All 106 store mutants were caught by the complete driver with physical worker-directory reuse; HANDOFF.md records the execution details.

## New RV32 controls

| Control | Planted defect or positive control | Result |
|---|---|---|
| Explicit compiler selection | An explicitly absent executable must not fall back or skip a required ctrl build | PASS |
| Freestanding header/type control | Poisoned hosted sysroot; real RV32 sizes and existing memory/format declarations must compile | PASS |
| Header isolation | Restore hosted include lookup; require the poison error | PASS |
| Freestanding flag | Remove -ffreestanding; require hosted include_next failure | PASS |
| ELF width | Compile a real RV64 object; require rejection | PASS |
| Floating-point ABI | Compile an ILP32D object; require rejection | PASS |
| Compressed ISA | Compile an RV32IC object; require rejection | PASS |
| Multiply ISA | Compile an RV32IM object; require rejection | PASS |
| Object format | Replace the object with non-ELF bytes; require rejection | PASS |
| Static frame evidence | Replace the report with dynamic stack usage; require rejection | PASS |
| Ctrl heap dependency | Replace the pool call with malloc; require named undefined-symbol failure | PASS |
| Ctrl unknown service | Replace the pool call with __unexpected_service; require named failure | PASS |
| Store heap dependency | Add a malloc call; require named failure | PASS |
| Store unknown service | Add an __unexpected_service call; require named failure | PASS |
| Store stack protection | Enable stack-protector instrumentation; require __stack_chk_fail rejection | PASS |

## Ctrl campaign

| Planted defect | Source | Named oracle(s) | Result |
|---|---|---|---|
| `departing-keeps-index` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/` | PASS |
| `departing-sends-zero` | `adp/adp.c` | `adp: AdpCore.A10toA14DepartingIndex` | PASS |
| `available-replaces-owed-departing` | `adp/adp.c` | `adp: AdpCore.A15OwedDepartingAcrossARestart` | PASS |
| `available-passes-owed-departing` | `adp/adp.c` | `adp: AdpCore.A17RoomBackBeforeAPoll` | PASS |
| `second-departing-dropped` | `adp/adp.c` | `adp: AdpCore.A16SecondShutdownQueuesItsOwn` | PASS |
| `second-shutdown-overwrites-index` | `adp/adp.c` | `adp: AdpCore.A16SecondShutdownQueuesItsOwn` | PASS |
| `link-loss-drops-owed-departing` | `adp/adp.c` | `adp: AdpCore.A18LinkLossKeepsTheOwedDeparting` | PASS |
| `gm-change-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `discover-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `stray-expiry-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `link-loss-keeps-owed-available` | `adp/adp.c` | `adp: AdpCore.A20LinkLossDropsTheOwedAvailable` | PASS |
| `departing-queue-unbounded` | `adp/adp.c` | `adp: Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/` | PASS |
| `coalesced-departing-uncounted` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `coalesce-drops-queued-departing` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `coalesce-overwrites-oldest-index` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `own-discover-discarded` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING` | PASS |
| `down-answers-discover` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN` | PASS |
| `link-down-departs` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING` | PASS |
| `gm-change-ignored` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING` | PASS |
| `delay-ignores-link-down` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed` | PASS |
| `shutdown-in-down-departs` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN` | PASS |
| `advertise-expiry-skips-delay` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING` | PASS |
| `advertise-period-wrong` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed` | PASS |
| `link-up-draws-startup-kind` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN` | PASS |
| `draw-kinds-merged` | `adp/adp.c` | `adp: AdpCore.A9DrawKinds` | PASS |
| `foreign-discover-answered` | `adp/adp.c` | `adp: AdpCore.A3toA5DiscoverAndDiscard` | PASS |
| `frame-misses-config-index` | `adp/adp.c` | `walk: AdpWalk.P11ConfigurationIndexBytes` | PASS |
| `stale-tag-accepted` | `adp/adp_mbx.c` | `adp: AdpAdapter.B1StaleTagDiscarded` | PASS |
| `latency-extra-read` | `adp/adp_mbx.c` | `adp: AdpLatency.C0toC6EveryResponsePath` | PASS |
| `pool-free-leaks` | `port/ctrl_pool.c` | `port: Pool.P2ReleaseAndBadFrees` | PASS |
| `calloc-overflow-unchecked` | `port/ctrl_pool.c` | `port: Pool.P3CallocZeroesAndRefusesAWrap` | PASS |
| `pool-double-free-accepted` | `port/ctrl_pool.c` | `port: Pool.P2ReleaseAndBadFrees` | PASS |
| `debug-truncation-uncounted` | `port/ctrl_debug.c` | `port: DebugSink.S2TruncatedToTheLine` | PASS |
| `tick-count-ignored` | `loop/ctrl_loop.c` | `port: Loop.L4TickFanOut` | PASS |
| `rx-pass-unbounded` | `loop/ctrl_loop.c` | `port: Loop.L2PerPassRxBound` | PASS |
| `poll-owes-nothing` | `adp/adp_mbx.c` | `adp: AdpOwed.E0toE3PendingWake` | PASS |
| `events-halved` | `loop/ctrl_loop.c` | `adp: AdpBacklog.F0toF7FullBacklogs` | PASS |
| `rx-before-events` | `loop/ctrl_loop.c` | `adp: AdpBacklog.F0toF7FullBacklogs` | PASS |
| `carried-ticks-overwritten` | `loop/ctrl_loop.c` | `port: Loop.L8TickRecordWhileCarried` | PASS |
| `tick-slice-unbounded` | `loop/ctrl_loop.c` | `port: Loop.L7TickSlices` | PASS |
| `owed-ticks-let-it-sleep` | `loop/ctrl_loop.c` | `port: Loop.L7TickSlices` | PASS |
| `filter-opened-before-eid` | `loop/ctrl_loop.c` | `port: LoopBring.L1OpenOrder` | PASS |
| `rx-no-resync` | `mbx/mbx.c` | `port: Driver.D1MalformedRecordResynchronises; unit: Records/DriverMalformed.D7RefusedAndResynchronised/` | PASS |
| `tx-overfills` | `mbx/mbx.c` | `port: Driver.D3HeldMergeFillsAndOrderAcrossChannels` | PASS |
| `lanes-big-endian` | `mbx/mbx_wire.h` | `model: Suite/MbxModelGroup.PassesOnTheModel/` | PASS |
| `frame-sources-from-sinks` | `adp/adp.c` | `entity: Fabric/EntityField.MatchesTheFabric/talker_stream_sources` | PASS |
| `pool-falls-back-to-heap` | `port/shlan_port.c` | `port: Pool.P4ShlanFunctionsDrawOnTheBoundPool; rv32: ` | PASS |
| `model-rate-unlimited` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/RateLimit` | PASS |
| `seq-not-stamped` | `mbx/mbx.c` | `port: Driver.D3HeldMergeFillsAndOrderAcrossChannels` | PASS |
| `model-round-robin` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder` | PASS |
| `model-gm-hi-live` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot` | PASS |
| `zero-byte-class-accepted` | `port/ctrl_pool.c` | `port: Pool.P5ClassTablesAndArenasRefused` | PASS |
| `zero-size-refusal-uncounted` | `port/ctrl_pool.c` | `port: Pool.P6CallocOfNothingAndOnAnExhaustedPool` | PASS |
| `foreign-free-uncounted` | `port/ctrl_pool.c` | `port: Pool.P7FreeBelowTheArenaRefused` | PASS |
| `port-pool-unreported` | `port/shlan_port.c` | `port: Pool.P8PortLayerUnbound` | PASS |
| `pool-follows-a-cut-free-list` | `port/ctrl_pool.c` | `port: Pool.P9AFreeListShorterThanItsCountIsExhausted` | PASS |
| `pool-cut-list-refuses-outright` | `port/ctrl_pool.c` | `port: Pool.P9AFreeListShorterThanItsCountIsExhausted` | PASS |
| `encoding-failure-swallowed` | `port/ctrl_debug.c` | `port: DebugSink.S3UnencodablePrintDiscarded` | PASS |
| `rx-binds-no-function` | `loop/ctrl_loop.c` | `port: LoopBring.L9TablesRefuseNullAndOverflow` | PASS |
| `seed-left-at-zero` | `adp/adp.c` | `adp: AdpCore.A22GeneratorNeverStuckAtZero` | PASS |
| `enable-not-idempotent` | `adp/adp.c` | `adp: AdpCore.A23RepeatedEnableOrDisableChangesNothing` | PASS |
| `other-subtype-accepted` | `adp/adp.c` | `adp: AdpCore.A24OtherEtherTypeOrSubtypeDiscarded` | PASS |
| `app-binds-pool-after-the-mailbox` | `app/ctrl_app.c` | `unit: AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox` | PASS |
| `app-starts-on-an-uncarved-pool` | `app/ctrl_app.c` | `unit: AppComposition.U1AnUncarvablePoolStartsNothing` | PASS |
| `major-unchecked` | `mbx/mbx.c` | `unit: AppComposition.U1AnotherContractOpensNothing; unit: IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major` | PASS |
| `evt-words-unchecked` | `mbx/mbx.c` | `unit: IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words` | PASS |
| `step-waits-twice` | `loop/ctrl_loop.c` | `unit: LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed` | PASS |
| `maap-base-shifted` | `mbx/mbx.c` | `unit: DriverUnit.D6MaapRangeWritten` | PASS |
| `tx-negative-fill` | `mbx/mbx.c` | `unit: DriverUnit.D8TransmitRefusals` | PASS |
| `unknown-event-decoded-as-tick` | `mbx/mbx.c` | `unit: DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt` | PASS |
| `whole-field-loses-its-top-bit` | `mbx/mbx_wire.h` | `unit: DriverUnit.D10LanesAndFieldsAtTheirBounds` | PASS |
| `slots-past-the-bank` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B2SlotsPastTheTimerBankRefused` | PASS |
| `foreign-frame-uncounted` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B3ForeignInterfaceCounted` | PASS |
| `attach-ignores-poll-room` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B4LoopWithNoRoomRefused` | PASS |
| `mmio-offset-as-index` | `plat/mbx_plat_mmio.c` | `unit: MmioPlatform.M1OneWordAtBasePlusOffset` | PASS |
| `wait-without-wfi` | `plat/mbx_plat_mmio.c` | `unit: MmioPlatform.M2WaitIsThePlatformWfi` | PASS |

## Store campaign

| Index | Planted defect | Source(s) | Named oracle(s) |
|---:|---|---|---|
| 0 | `no_crc_check` | `nvm_store.c` | `torn_falls_back, verdict_parity` |
| 1 | `no_crc_anywhere` | `nvm_klj2.c, nvm_store.c` | `powercut` |
| 2 | `pick_older` | `nvm_store.c` | `newer_wins` |
| 3 | `pick_no_wrap` | `nvm_store.c` | `newer_wins` |
| 4 | `tie_picks_b` | `nvm_store.c` | `newer_wins` |
| 5 | `erased_header_only` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 6 | `no_ascending` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 7 | `overrun_as_rec` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 8 | `incomplete_accepted` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 9 | `room_unchecked` | `nvm_klj2.c` | `codec_room` |
| 10 | `short_prefix_read_on` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 11 | `short_prefix_as_len` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 12 | `header_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 13 | `header_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 14 | `payload_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 15 | `payload_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 16 | `lookup_index_unbounded` | `nvm_klj2.c` | `codec_lookups` |
| 17 | `long_crc_unchecked` | `nvm_store.c` | `long_container_reads` |
| 18 | `unread_not_counted` | `nvm_store.c` | `long_container_reads` |
| 19 | `no_version_check` | `nvm_klj2.c` | `wrong_version_falls_back` |
| 20 | `no_blank_verdict` | `nvm_klj2.c` | `blank_boot` |
| 21 | `pad_not_zero` | `nvm_klj2.c` | `blank_boot` |
| 22 | `header_n_rec` | `nvm_klj2.c` | `blank_boot, first_commit_bytes` |
| 23 | `frame_crc_init` | `nvm_klj2.c` | `vector_round_trip, change_commit_bytes` |
| 24 | `no_blank_stage` | `nvm_store.c` | `blank_boot` |
| 25 | `verdict_not_named` | `nvm_store.c` | `both_torn_blank` |
| 26 | `stage_not_rechecked` | `nvm_store.c` | `read_flip_at_stage` |
| 27 | `stage_seq_unchecked` | `nvm_store.c` | `read_alias_at_stage` |
| 28 | `select_on_unchecked_reread` | `nvm_store.c` | `read_flip_boot` |
| 29 | `slot_read_fail_ignored` | `nvm_store.c` | `read_fail_boot` |
| 30 | `unread_not_held` | `nvm_store.c` | `authority_unknown, fallback_restage, read_disagreement` |
| 31 | `read_not_retried` | `nvm_store.c` | `read_fail_boot, authority_unknown` |
| 32 | `refusal_unconfirmed` | `nvm_store.c` | `authority_unknown, read_disagreement, reads_differ_in_verdict, reads_agree_in_digest_not_length` |
| 33 | `blank_unconfirmed` | `nvm_store.c` | `authority_unknown` |
| 34 | `refusal_by_verdict` | `nvm_store.c` | `read_disagreement` |
| 35 | `agreement_by_digest` | `nvm_store.c` | `reads_agree_in_digest_not_length` |
| 36 | `disagreement_not_counted` | `nvm_store.c` | `reads_differ_in_verdict, reads_agree_in_digest_not_length` |
| 37 | `restage_not_retried` | `nvm_store.c` | `read_flip_at_stage, read_alias_at_stage, read_fail_boot` |
| 38 | `fallback_restage_unchecked` | `nvm_store.c` | `fallback_restage` |
| 39 | `no_rollback` | `nvm_store.c` | `apply_fault_rolls_back, settle_fault_rolls_back` |
| 40 | `rollback_failure_ignored` | `nvm_store.c` | `rollback_fault_closes` |
| 41 | `release_on_closed` | `nvm_store.c` | `rollback_fault_closes` |
| 42 | `fault_as_refusal` | `nvm_store.c` | `apply_fault_rolls_back, binding_walk` |
| 43 | `refusal_aborts` | `nvm_store.c` | `refused_keeps_default` |
| 44 | `settle_fault_ignored` | `nvm_store.c` | `settle_fault_rolls_back` |
| 45 | `settle_after_names` | `nvm_store.c` | `golden_restore` |
| 46 | `no_settle_without_names` | `nvm_store.c` | `settle_after_the_last_record` |
| 47 | `shape_not_checked` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| 48 | `shape_mismatch_released_unproven` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| 49 | `release_before_apply` | `nvm_store.c` | `golden_restore` |
| 50 | `apply_erased` | `nvm_store.c` | `erased_records` |
| 51 | `model_ready_ignored` | `nvm_store.c` | `model_unproven_closes` |
| 52 | `bindings_skipped_unproven` | `nvm_store.c` | `model_unproven_closes` |
| 53 | `d3_rollback_takes_bindings` | `nvm_store.c` | `apply_fault_rolls_back, settle_fault_rolls_back` |
| 54 | `bindings_in_d3_walk` | `nvm_store.c` | `binding_walk, golden_restore` |
| 55 | `binding_fault_aborts_d3` | `nvm_store.c` | `binding_walk` |
| 56 | `binding_fault_keeps_preloads` | `nvm_store.c` | `binding_walk` |
| 57 | `quiet_period` | `nvm_store.c` | `debounce` |
| 58 | `no_debounce` | `nvm_store.c` | `debounce` |
| 59 | `capture_leaves_window_armed` | `nvm_store.c` | `debounce` |
| 60 | `taken_off_by_one` | `nvm_store.c` | `debounce` |
| 61 | `taken_while_capturing` | `nvm_store.c` | `capture_window_edges` |
| 62 | `taken_after_last_latch` | `nvm_store.c` | `capture_window_edges` |
| 63 | `change_of_no_record` | `nvm_store.c` | `change_unknown_record` |
| 64 | `nothing_to_save_framed` | `nvm_store.c` | `nothing_to_save` |
| 65 | `dr2b_ignores_durability` | `nvm_store.c` | `failed_commit_not_skipped` |
| 66 | `no_dr2b` | `nvm_store.c` | `unchanged_no_erase` |
| 67 | `console_force_ignored` | `nvm_store.c` | `console_commit_unchanged` |
| 68 | `no_backoff` | `nvm_store.c` | `media_failures` |
| 69 | `unbounded_attempts` | `nvm_store.c` | `media_failures` |
| 70 | `budget_rearmed_by_change` | `nvm_store.c` | `dr2c_unchanged_set` |
| 71 | `budget_rearmed_by_capture` | `nvm_store.c` | `dr2c_unchanged_set` |
| 72 | `commit_now_overrides_exhaustion` | `nvm_store.c` | `dr2c_console` |
| 73 | `commit_now_ignores_backoff` | `nvm_store.c` | `dr2c_console` |
| 74 | `success_forgives_exhaustion` | `nvm_store.c` | `recovers_after_failure, dr2c_unchanged_set` |
| 75 | `stale_kept` | `nvm_store.c` | `recovers_after_failure` |
| 76 | `dr2b_keeps_stale` | `nvm_store.c` | `recovers_after_failure` |
| 77 | `no_blankcheck` | `nvm_store.c` | `media_failures` |
| 78 | `blankcheck_first_stretch_only` | `nvm_store.c` | `blankcheck_tail` |
| 79 | `blankcheck_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| 80 | `no_verify` | `nvm_store.c` | `media_failures, failed_commit_not_skipped` |
| 81 | `verify_skips_last_stretch` | `nvm_store.c` | `verify_tail` |
| 82 | `verify_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| 83 | `program_refusal_ignored` | `nvm_store.c` | `media_verdicts` |
| 84 | `no_timeout` | `nvm_store.c` | `media_failures` |
| 85 | `same_sequence` | `nvm_store.c` | `change_commit_bytes` |
| 86 | `refused_slot_overwritten` | `nvm_store.c` | `refused_slot_kept` |
| 87 | `no_blank_slot_takes_b` | `nvm_store.c` | `first_commit_no_blank_slot` |
| 88 | `erase_authoritative` | `nvm_store.c` | `change_commit_bytes, powercut` |
| 89 | `descending_pages` | `nvm_store.c` | `first_commit_bytes` |
| 90 | `capture_in_one_step` | `nvm_store.c` | `service_bound` |
| 91 | `spin_wait` | `nvm_store.c` | `service_bound` |
| 92 | `litespi_no_wren` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| 93 | `litespi_status_ignored` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| 94 | `litespi_no_guard` | `plat/nvm_flash_litespi.c` | `port_guard` |
| 95 | `phc_time` | `plat/nvm_flash_litespi.c` | `time_base` |
| 96 | `clock_not_accumulated` | `plat/nvm_flash_litespi.c` | `time_base` |
| 97 | `ticks_per_us_truncated` | `plat/nvm_flash_litespi.c` | `port_clock, time_base` |
| 98 | `xfer_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| 99 | `open_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| 100 | `call_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_deadline, port_drain_deadline` |
| 101 | `drain_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_drain_deadline` |
| 102 | `read_runs_past_device` | `plat/nvm_flash_litespi.c` | `port_read_range` |
| 103 | `program_across_page` | `plat/nvm_flash_litespi.c` | `port_write_refusals` |
| 104 | `deadline_per_wait` | `plat/nvm_flash_litespi.c` | `port_deadline` |
| 105 | `stall_ignored` | `plat/nvm_flash_litespi.c` | `port_stall` |
