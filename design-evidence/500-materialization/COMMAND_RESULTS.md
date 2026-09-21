# D3 materialization: command record

Every command the design page quotes, its real exit status and the digests
of what it read and wrote. Base of the tree: dev
`07294a76e833f1831d9fcbceb8123b8380c4ae76` (protocol-processor `424c688f`,
gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`). The
executable sources the run used are this commit's; the run started from an
EMPTY `$D3_OUT`, an EMPTY `$OOC_OUT` and an EMPTY `$PROBE_OUT`. Scratch
output (build trees, run logs, the area tool's working files, the probes'
builds) is outside the tree. Every command ran synchronously, pinned to one
set of 32 CPUs, with at most eight build jobs and one build pool.

This revision (A153, revision c) answers the round-two reviews of the page
at `40d14d92` (R217 and R218, both NEGATIVE). The round-two record was
commit `ca8cb5943f885c22aec397ff75059e2d4791f4fb`; the round-one record,
`a21b165ac1c671d10cba7255beaf75cea0f81d18`.

## Commands

| Command | Exit | Result |
|---|---|---|
| `python3 -B run.py prep` | 0 | shape 1x1 (shipped): 53 records; 8x8 (shipped): 156; 1x1r2 (SYNTHETIC): 53. The amended prototypes checked against their pinned sources |
| `python3 -B run.py build <builds 1, 5, 9, ...> --pool 1 --jobs 8` | 0 | 18 built |
| `python3 -B run.py build <builds 2, 6, 10, ...> --pool 1 --jobs 8` | 0 | 17 built |
| `python3 -B run.py build <builds 3, 7, 11, ...> --pool 1 --jobs 8` | 0 | 17 built |
| `python3 -B run.py build <builds 4, 8, 12, ...> --pool 1 --jobs 8` | 0 | 17 built: 69 in all (3 base shapes, the tracked glue, 65 mutants) |
| `python3 -B run.py run --pool 8` | 0 | `SUMMARY FULL builds 69, runs 312, checks 3462, verdict failures 0` |
| `python3 -B run.py controls --pool 8` | 0 | `CONTROLS 8, not as required 0` (each control's own exit below) |
| `python3 -B ../reviewer-probes/r217_probes.py` | 0 | 9 runs of R217's round-two probes, adapted |
| `python3 -B ../reviewer-probes/r217_check.py` | 0 | `R217 PROBES: 9 runs, 0 not as demanded` |
| `python3 -B ../reviewer-probes/r218_probe_headers.py` | 0 | 6 runs of R218's round-two probes, adapted |
| `python3 -B ../reviewer-probes/r218_check.py` | 0 | `R218 PROBES: 6 runs, 0 not as demanded` |
| R217's own `check_probes.py` (commit `7d9da877`) on the same results | 1 | `AssertionError` at its line 19, its first round-two COUNTEREXAMPLE assertion (a repeated header error reported done without failure): the counterexample no longer holds, as required |
| `ooc/run_ooc.sh` (from inside `$OOC_OUT`) | 0 | 20 rows, `ooc/results_ooc.txt` |
| `syn/yosys/ooc.sh KL_nvm_backend` (repository root, `OOC_CHPARAM` of the 1x1 shape with `N_NAME_P=30`) | 0 | `1030 LUT, 0 LUTRAM, 468 FF, 6 DSP, 114 CARRY4`, identical to the row `cal-backend-1x1-n30` |
| `python3 -B run.py receipts` | 0 | the digest tables below |

Builds were split into four synchronous commands (every fourth build of
`run.py`'s list) only to keep each under the session's command limit;
`run.py build` with no name builds all 69. The run, probe, controls and
calibration commands ran from `proposal-evidence`, the repository root for
the calibration.

Tools: Verilator 5.052, gcc 16.2.1, sv2v v0.0.13, Yosys 0.66 (git sha1
86f2ddebc), Python 3.14.7.

## The process-level controls

`run.py controls` runs the real CLI (`run.py run <build> --shapes <shape>`)
on doctored copies of the built binaries in private output trees, and
requires each exit status and diagnostic. The NON-ZERO exits below are the
required outcomes of negative controls; the action itself exited 0.

| Control | Doctored | Required exit | Observed | Diagnostic required and found |
|---|---|---|---|---|
| healthy_binary_as_mutant | `base-1x1`'s binary as `mut-M01_taint_ignored` | 1 | 1 | `MUTANT M01_taint_ignored: SURVIVED`, `verdict failures 1` |
| binary_fails_before_the_scenario | an executable that exits 1 as `mut-M06_identify_is_a_change` | 1 | 1 | `MUTANT M06_identify_is_a_change: NOT COMPLETED`, `verdict failures 1` |
| failed_baseline_result | `mut-RPL_rate`'s binary as `base-1x1r2` | 1 | 1 | `UNEXPECTED base-1x1r2 V1b_restore_everything value_restored:0x02 FAIL` |
| tracked_control_violated | `base-1x1`'s binary as `tracked-1x1` | 1 | 1 | `TRACKED K1_single_change_converges : converged@end DOES NOT FAIL` |
| vacuity_control_violated | `mut-M13_restore_applies_nothing` itself, with `D3_CONTROL_SKIP_STALE_SEED=1` | 1 | 1 | `CONTROL stale store under M13: naive read-back FAILS, cleared-first PASSES -> NOT AS REQUIRED`, `verdict failures 1` |
| tracked_control_absent | `tracked-1x1` not provided | 2 | 2 | `REFUSED: tracked-1x1 is not built` |
| partial_kill_is_survival | `base-1x1`'s binary as `mut-TRG_fmto`, with `D3_CONTROL_SKIP_V1S_DECLARED=1` | 1 | 1 | `MUTANT TRG_fmto: SURVIVED by V1a_set_everything : value_in_slot@cut:0x40 [SURVIVED] AND V1s_a_shipping_output_format : value_in_slot@cut:0x40 [KILLED] -- latest None`, `verdict failures 1` |
| empty_selection | none; build `no-such-build` | 2 | 2 | `REFUSED: no such build ['no-such-build']` |

```
CONTROL healthy_binary_as_mutant: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL binary_fails_before_the_scenario: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL failed_baseline_result: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL tracked_control_violated: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL vacuity_control_violated: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL tracked_control_absent: AS REQUIRED -- exit 2 (required 2); diagnostics found
CONTROL partial_kill_is_survival: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL empty_selection: AS REQUIRED -- exit 2 (required 2); diagnostics found
CONTROLS 8, not as required 0
```

## Verdicts (the tail of `results.txt`)

```
PREMISE base-1x1 K15: the binding manager sampled busy on the D3 writer's grant cycle at g3 (1 of 8 releases) -> reached
MUTANT A01_grant_cycle_not_busy: KILLED by K15_binding_on_the_d3_grant_cycle~g3 : both_records_committed [KILLED] -- binding None, 0x50 0016e36f, grant-cycle collisions 1
MUTANT B01_binding_walk_no_deadline: KILLED by W13_binding_walk_silent : binding_walk_bounded@terminal [KILLED] -- silence from 64, the binding walk's terminal at 0 (bound 20000 + 100)
MUTANT B02_binding_device_error_reads_as_empty: KILLED by W16_binding_header_device_error : binding_walk_failed@terminal [KILLED] -- binding fail 0 cause 0 (a device error on the header), preloads [], restore fail 0, blank 0
MUTANT B03_binding_abort_not_drained: KILLED by W13c_binding_late_after_deadline : later_change_persists@recovered [KILLED] -- latest 0076adf1, newest verified slot 0016e360
MUTANT B04_binding_unframed_reads_as_device_error: KILLED by V10_blank_first_boot : blank_boot_is_not_a_failure@boot [KILLED] -- restore fail 1 (D3 0, binding 1), causes D3 0 binding 2, done 1
MUTANT C01_device_error_reads_as_blank: KILLED by H8_header_error_sole_saved_record : header_fault_contained@terminal [KILLED] -- 0 records off their defaults []; D3 done 1 fail 0 rolled back 0 (want 0) closed 0 own 0 cause 0
MUTANT C02_port_cause_collapsed: KILLED by H1_header_error_both_passes : header_fault_contained@terminal [KILLED] -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 0 rolled back 0 (want 0) close
MUTANT C03_unframed_reads_as_device_error: KILLED by V10_blank_first_boot : blank_boot_is_not_a_failure@boot [KILLED] -- restore fail 1 (D3 1, binding 0), causes D3 2 binding 0, done 1
MUTANT D01_abandoned_read_not_drained: KILLED by W6_late_pass1_after_deadline : later_change_persists@recovered [KILLED] -- latest 0076adf1, newest verified slot 0016e360
MUTANT DF01_desc_error_is_a_refusal: KILLED by V20b_desc_error_once_after_apply : rolled_back_to_defaults@terminal [KILLED] -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x30 live (145524899430031360, 1) want (0, 0)']; D3 done 1 fail 0 rolled back
MUTANT DF02_map_revert_read_error_ignored: KILLED by V20c_desc_error_in_the_map_revert : rollback_premise@terminal [KILLED] -- 2 records applied before the fault, roll-back at 3859, abort cause 4 (want (6,))
MUTANT DF03_final_revert_read_error_ignored: KILLED by V20d_desc_error_in_the_final_revert : rolled_back_to_defaults@terminal [KILLED] -- 1 records off their defaults ['0x40 live (0, 1) want (0, 0)']; D3 done 1 fail 0 rolled back 0 (want 1) closed 0 own 0 cause 0
MUTANT DG01_guard_admits_a_request_while_owed: KILLED by V23_late_desc_beats_in_service : late_beats_never_served@restored [KILLED] -- second locate err 1 type 0x0; third locate err 0 type 0x6 (want STREAM_INPUT 0x5, never the late burst's 0x6)
MUTANT DG02_rollback_ignores_mem_debt: KILLED by V21b_desc_debt_outlasts_the_store : rolled_back_to_defaults@terminal [KILLED] -- 0 records off their defaults []; D3 done 0 fail 1 rolled back 0 (want 1) closed 1 own 1 cause 6
MUTANT F01_old_boot_order: KILLED by V1b_restore_everything : set_value_survives_power_cycle:0x50 [KILLED] -- restored None valid None, set 1500000
MUTANT G01_pend_misses_d3: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved [KILLED] -- change of 0x50 at 33739 inside a durable interval ending 4611686018427387904
MUTANT G02_restore_done_without_d3: KILLED by V1b_restore_everything : entity_enabled_after_restore@boot [KILLED] -- enabled at 188, D3 restore done at 7605, restore done at 177
MUTANT G03_restore_writes_are_changes: KILLED by V1b_restore_everything : restore_sets_no_dirty@boot [KILLED] -- 6 record writes after the restore, dirty 0, flash erases 0 -> 1
MUTANT G04_blank_ignores_d3: KILLED by V7_names_only : blank_is_both_walks@boot [KILLED] -- a name came back and no binding did: blank 1, done 1
MUTANT G05_enable_not_released_by_restore: KILLED by W14_enable_requested_before_the_restore : entity_enabled_after_terminal@boot [KILLED] -- entity enabled at 9, D3 terminal at 7605, restore done at 7605, firmware asked at 9
MUTANT IMG01_unproven_image_continues: KILLED by V22b_image_unproven_simple_records : closed_when_image_unproven@recovered [KILLED] -- abort cause 0, applied 2, refused 0, image validated 0, closed 0
MUTANT M01_taint_ignored: KILLED by K2_change_during_record_write : no_durable_claim_over_unsaved [KILLED] -- durable at 1568748: record 0x50 latest 0021e88e slot 0010f447
MUTANT M02_clear_at_latch: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved [KILLED] -- durable at 533028: record 0x50 latest 0012d687 slot None
MUTANT M03_clear_wins_same_edge: KILLED by K5_change_on_the_done_edge : same_edge_change_survives@end:0x50 [KILLED] -- latest 004c4b42, newest verified slot 004c4b41
MUTANT M04_clear_by_group: KILLED by K4_second_record_in_flight : value_in_slot@end:0x51 [KILLED] -- latest 003d0902, newest verified slot None
MUTANT M05_latch_ignores_program: KILLED by K11_name_latch_waits_for_the_program : written_value_was_set:0x80 [KILLED] -- 2 writes; first bad 4b3131207365636f6e642076616c75652042424242424242424242424242424242424242424242424242424242424242414141414141414141414141
MUTANT M06_identify_is_a_change: KILLED by K14_identify_is_not_persisted : identify_never_persisted [KILLED] -- 1 record writes, dirty 0, pend 0, flash programs 0 -> 13
MUTANT M08_restore_skips_image_check: KILLED by V7_names_only : restored_name_survives_first_command:0x80 [KILLED] -- after the first command b'Milan FPGA 1x1 TDM8\x00\x00\x00\x00\x00'
MUTANT M09_apply_blindly: KILLED by V2_refused_rate : refused_value_not_applied:0x02 [KILLED] -- rate row valid 1, refused 0
MUTANT M10_fmt_full_judge: KILLED by V6b_restore_coupled_pair : coupled_pair_restored [KILLED] -- fmto0 0 valid 0; OUT0 set matches the slot True
MUTANT M11_no_orphan_check: KILLED by V8_orphaning_format_reverted : no_orphaned_mapping_after_restore [KILLED] -- stream 0 format 0x205022000806000 (2 channels), 6 orphaned mappings
MUTANT M12_no_revert_before_readd: KILLED by V9_refused_maps_revert_their_formats : refused_group_falls_back_to_default:0x70 [KILLED] -- live OUT0 equals the default True, fmto0 0x205022002006000, ptof0 0 valid 0, rolled back 1
MUTANT M13_restore_applies_nothing: KILLED by V1b_restore_everything : value_restored:0x50 [KILLED] -- live (0, 0) want (1500000, 1) (value, valid)
CONTROL stale store under M13: naive read-back PASSES, cleared-first FAILS -> as required
MUTANT M14_clear_by_index: KILLED by K4g_second_group_in_flight : value_in_slot@end:0x0a [KILLED] -- latest 0001, newest verified slot None
MUTANT M15_overflow_forgets_the_change: KILLED by K16_map_set_larger_than_its_record : no_durable_claim_over_unsaved [KILLED] -- durable at 1601552: record 0x70 latest 00000000000000000000000100010000000000020002000000000003000300000000000400040000000000050005000000000
MUTANT M16_single_pass_restore: KILLED by V11_torn_read_restores_nothing : torn_walk_applies_nothing@boot [KILLED] -- ptof0 valid 0 (its record was read whole before the torn one), restore fail 1, D3 fail 1, applied 0, rolled back 1
MUTANT O01_own_taken_at_the_walk: KILLED by K19_command_before_the_restore : value_in_slot@end:0x50 [KILLED] -- latest 001d48d7, newest verified slot 0016e360
MUTANT P01_padding_by_first_byte: KILLED by V3a_map_index_0xff00 : map_record_verdict:0x70 [KILLED] -- live OUT0 empty (want the default set); applied 2 refused 0 blank 47 of 49
MUTANT P02_padding_holes_not_refused: KILLED by V3e_map_hole : malformed_refused_untouched:0x70 [KILLED] -- 3 map sets staged for a malformed record [(3631, 'map-remove'), (3653, 'map-add')]
MUTANT R01_no_rollback: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal [KILLED] -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 1 rolled back 0 (want 1) close
MUTANT R02_rollback_skips_dyn_store: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal [KILLED] -- 6 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 1 rolled back 1 (want 1) close
MUTANT R03_rollback_skips_desc_store: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal [KILLED] -- 1 records off their defaults ['0x80 live 443320726573746f72656420 want 4d696c616e20465047412031 from byte 0']; D3 done 1 fail 1 rolled back 
MUTANT R04_rollback_skips_maps: KILLED by V16_rollback_pass1_maps : rolled_back_to_defaults@terminal [KILLED] -- 1 records off their defaults ['0x60 live ffffffffffffffffffffffff want 000000020002000000000003 from byte 16']; D3 done 1 fail 1 rolled back
MUTANT R05_closed_releases_the_entity: KILLED by V17_rollback_cannot_validate : closed_keeps_entity_dark@recovered [KILLED] -- closed 0, restore done 1 fail 1, own 0, entity enabled 1 (first 6713), firmware asked at 6713, a GET answered 0, cause 2
MUTANT RPL_cfg: KILLED by V1b_restore_everything : value_restored:0x00 [KILLED] -- live (0, 0) want (0, 1) (value, valid)
MUTANT RPL_clks: KILLED by V1b_restore_everything : value_restored:0x0a [KILLED] -- live (0, 0) want (1, 1) (value, valid)
MUTANT RPL_fmti: KILLED by V1b_restore_everything : value_restored:0x30 [KILLED] -- live (0, 0) want (145524899430031360, 1) (value, valid) AND V1s_b_shipping_output_format_restore : value_restored:0x30 [KILLED] -- live (0, 0) want (145524899430031360, 1) (value, valid)
MUTANT RPL_fmto: KILLED by V1b_restore_everything : value_restored:0x40 [KILLED] -- live (0, 0) want (145524899438419968, 1) (value, valid) AND V1s_b_shipping_output_format_restore : value_restored:0x40 [KILLED] -- live (0, 0) want (145524899455197184, 1) (value, valid)
MUTANT RPL_mapi: KILLED by V1b_restore_everything : value_restored:0x60 [KILLED] -- live 000000020002000000000003 want ffffffffffffffffffffffff from byte 16
MUTANT RPL_mapo: KILLED by V1b_restore_everything : value_restored:0x70 [KILLED] -- live 030000000000040004000000 want 100000ffffffffffffffffff from byte 29
MUTANT RPL_name: KILLED by V1b_restore_everything : value_restored:0x80 [KILLED] -- live 4d696c616e20465047412031 want 443320726573746f72656420 from byte 0
MUTANT RPL_ptof: KILLED by V1b_restore_everything : value_restored:0x50 [KILLED] -- live (0, 0) want (1500000, 1) (value, valid)
MUTANT RPL_rate: KILLED by V1b_restore_everything : value_restored:0x02 [KILLED] -- live (0, 0) want (96000, 1) (value, valid)
MUTANT TRG_cfg: KILLED by V1a_set_everything : value_in_slot@cut:0x00 [KILLED] -- latest 0000, newest verified slot None
MUTANT TRG_clks: KILLED by V1a_set_everything : value_in_slot@cut:0x0a [KILLED] -- latest 0001, newest verified slot None
MUTANT TRG_fmti: KILLED by V1a_set_everything : value_in_slot@cut:0x30 [KILLED] -- latest 0205022000806000, newest verified slot None AND V1s_a_shipping_output_format : value_in_slot@cut:0x30 [KILLED] -- latest 0205022000806000, newest verified slot None
MUTANT TRG_fmto: KILLED by V1a_set_everything : value_in_slot@cut:0x40 [KILLED] -- latest 0205022001006000, newest verified slot None AND V1s_a_shipping_output_format : value_in_slot@cut:0x40 [KILLED] -- latest 0205022002006000, newest verified slot None
MUTANT TRG_mapi: KILLED by V1a_set_everything : value_in_slot@cut:0x60 [KILLED] -- latest 00000000000000000000000100010000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, new
MUTANT TRG_mapo: KILLED by V1a_set_everything : value_in_slot@cut:0x70 [KILLED] -- latest 0000000000000000000000010001000000000002000200000000000300100000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
MUTANT TRG_name: KILLED by V1a_set_everything : value_in_slot@cut:0x80 [KILLED] -- latest 443320726573746f72656420656e74697479206e616d650000000000000000000000000000000000000000000000000000000000000000000000000000000000, new
MUTANT TRG_ptof: KILLED by V1a_set_everything : value_in_slot@cut:0x50 [KILLED] -- latest 0016e360, newest verified slot None
MUTANT TRG_rate: KILLED by V1a_set_everything : value_in_slot@cut:0x02 [KILLED] -- latest 00017700, newest verified slot None
MUTANT W01_no_restore_watchdog: KILLED by W4_silent_pass1 : restore_terminal_bounded@terminal [KILLED] -- stall began at 3544, D3 terminal at 0 (bound 30000 cycles)
MUTANT X01_passes_may_disagree: KILLED by V18b_header_changed_between_passes : rolled_back_to_defaults@terminal [KILLED] -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 0 rolled back 0 (want 1) close
MUTANT X02_passes_compared_by_count: KILLED by V18c_changes_balance_counts : rolled_back_to_defaults@terminal [KILLED] -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 0 rolled back 0 (want 1) close
TRACKED K1_single_change_converges : converged@end FAILS, as it must at the current source
TRACKED K1_single_change_converges : value_in_slot@end:0x50 FAILS, as it must at the current source
TRACKED K10_name_change_converges : value_in_slot@end:0x80 FAILS, as it must at the current source
TRACKED K10_name_change_converges : no_durable_claim_over_unsaved FAILS, as it must at the current source
TRACKED K12_map_change_converges : value_in_slot@end:0x70 FAILS, as it must at the current source
TRACKED K12_map_change_converges : no_durable_claim_over_unsaved FAILS, as it must at the current source
TRACKED V1b_restore_everything : set_value_survives_power_cycle:0x50 FAILS, as it must at the current source
TRACKED K1_single_change_converges : no_durable_claim_over_unsaved PASSES, as it must
TRACKED V1a_set_everything : no_durable_claim_over_unsaved PASSES, as it must
TRACKED V1b_restore_everything : no_durable_claim_over_unsaved PASSES, as it must
TRACKED * : case_completed PASSES, as it must
LABEL SYNTHETIC output-format judge (a narrowed output format, product-illegal): 50 cases: H1_header_error_both_passes, H2_header_errors_balance_counts, H2b_header_errors_swap, H3_header_error_pass0_only, H4_header_error_first_record, H5_header_error_map_record, H6_header_error_last_name, H7_header_error_last_name_pass1, K19_command_before_the_restore, V12_abort_pass0_early, V13_abort_pass0_late, V14_rollback_pass1_early, V15_rollback_pass1_late, V16_rollback_pass1_maps, V17_rollback_cannot_validate, V18_header_error_pass1, V18b_header_changed_between_passes, V18c_changes_balance_counts, V1a_set_everything, V1b_restore_everything, V20_desc_error_after_apply, V20b_desc_error_once_after_apply, V20c_desc_error_in_the_map_revert, V20d_desc_error_in_the_final_revert, V21_desc_late_after_apply, V21b_desc_debt_outlasts_the_store, V21c_desc_debt_outlasts_the_deadline, V21d_desc_slow_within_the_store_bound, V22_desc_fails_before_boot, V6a_set_coupled_narrower_pair, V6b_restore_coupled_pair, V8_orphaning_format_reverted, V9_refused_maps_revert_their_formats, W10_edit_face_silent_pass1, W12_r218_read_late_after_apply, W13_binding_walk_silent, W13b_binding_late_before_deadline, W13c_binding_late_after_deadline, W14_enable_requested_before_the_restore, W15_binding_answer_after_enable, W16_binding_header_device_error, W1_silent_pass0, W2_late_pass0_before_deadline, W3_late_pass0_after_deadline, W4_silent_pass1, W5_late_pass1_before_deadline, W6_late_pass1_after_deadline, W7_silent_pass1_last_name, W8_map_face_silent_pass1, W9_judge_silent_pass1
LABEL SHIPPING output-format judge (milan_datapath.sv sfv_supported_w): V1s_a_shipping_output_format, V1s_b_shipping_output_format_restore, V1s_c_shipping_refuses_a_narrower_saved_output
SUMMARY FULL builds 69, runs 312, checks 3462, verdict failures 0
```

## Area (`ooc/results_ooc.txt`)

```
label                              top                           LUT LUTRAM LUT_TOT     FF RAMB36 RAMB18  DSP CARRY4
cal-backend-1x1-n30                KL_nvm_backend               1030      0    1030    468      0      0    6    114
cal-backend-1x1-n38                KL_nvm_backend               1051      0    1051    476      0      0    6    114
cal-backend-8x8-n99                KL_nvm_backend               1348    128    1476    515      0      0    6    113
cal-port                           KL_pp_nvm_port                197      0     197    116      0      0    0     14
cal-bindmgr-1x1                    KL_acmp_nvm_shadow            940    100    1040   1081      0      0    0     46
cal-bindmgr-8x8                    KL_acmp_nvm_shadow           1019    100    1119   1123      0      0    0     56
b-writer-1x1                       KL_aecp_nvm_writer           2186     72    2258    885      0      0    0    141
b-writer-1x1-nodsp                 KL_aecp_nvm_writer           2253     72    2325    885      0      0    0    141
b-writer-8x8                       KL_aecp_nvm_writer           3016     48    3064   1106      0      0    0    144
b-writer-8x8-nodsp                 KL_aecp_nvm_writer           2916     48    2964   1106      0      0    0    144
b-arbiter                          KL_pp_nvm_mgr_arb              52      0      52      3      0      0    0      0
s2-desc-guard                      KL_aecp_desc_mem_guard          5      0       5      1      0      0    0      0
s1-port-amended                    KL_pp_nvm_port_amd            201      0     201    118      0      0    0     14
s3-bindmgr-amended-1x1             KL_acmp_nvm_shadow_amd       1047    100    1147   1115      0      0    0     56
s3-bindmgr-amended-8x8             KL_acmp_nvm_shadow_amd       1122    100    1222   1157      0      0    0     66
a-manager-unit                     KL_acmp_nvm_shadow           1323      0    1323   1223      0      0    0     46
a-shadows-1x1                      d3a_shadow_proxy              146    112     258    228      1      0    0      0
a-shadows-8x8                      d3a_shadow_proxy              150     68     218    164      3      0    0      0
c-fabric-1x1                       d3c_fabric_proxy              530      0     530    266      0      0    0      0
c-fabric-8x8                       d3c_fabric_proxy             1631      0    1631    458      0      0    0      0
```

## The round-two reviewers' probes (`../reviewer-probes/results.txt`)

```
# r217_check.py (exit 0)
HOLDS R217 first-pass completed: rc 0
HOLDS R217 original-second-pass completed: rc 0
HOLDS R217 control completed: rc 0
HOLDS R217 header-repeat completed: rc 0
HOLDS R217 header-balanced completed: rc 0
HOLDS R217 header-pass0 completed: rc 0
HOLDS R217 descriptor-error completed: rc 0
HOLDS R217 descriptor-timeout completed: rc 0
HOLDS R217 descriptor-initial-error completed: rc 0
HOLDS R217 original payload fault first-pass: every row at its default True, restore fail 1, rolled back 0
HOLDS R217 original payload fault original-second-pass: every row at its default True, restore fail 1, rolled back 1
HOLDS R217 control: done 1 fail 0 enabled 1 applied 10
HOLDS R217 header-repeat: every row at its default True, done 1 fail 1 (D3 1, cause 2), blank 0, applied 0, enabled 1
HOLDS R217 header-balanced: every row at its default True, done 1 fail 1 (D3 1, cause 2), blank 0, applied 0, enabled 1
HOLDS R217 header-pass0: every row at its default True, done 1 fail 1 (D3 1, cause 2), blank 0, applied 0, enabled 1
HOLDS R217 descriptor-error: closed 1, done 0, enabled 0, cause 6 (the memory still fails, so the roll-back cannot prove its image)
HOLDS R217 descriptor-timeout: every row at its default True, done 1 fail 1, rolled back 1, cause 6, enabled 1
HOLDS R217 descriptor-initial-error: closed 1, done 0, enabled 0, cause 7, image validated 0, applied 0 refused 0
R217 PROBES: 9 runs, 0 not as demanded

# r218_check.py (exit 0)
HOLDS R218 V18 pass0: 0 records off their defaults, D3 done 1 fail 1 rolled back 0, restore fail 1 blank 0, cause 2, terminal 1137 enable 1148
HOLDS R218 V18 repeat: 0 records off their defaults, D3 done 1 fail 1 rolled back 0, restore fail 1 blank 0, cause 2, terminal 1137 enable 1148
HOLDS R218 V18 swap: 0 records off their defaults, D3 done 1 fail 1 rolled back 0, restore fail 1 blank 0, cause 2, terminal 1152 enable 1163
HOLDS R218 V18 pass1: 0 records off their defaults, D3 done 1 fail 1 rolled back 1, restore fail 1 blank 0, cause 2, terminal 4417 enable 4433
HOLDS R218 original F1 trigger (V11b): 0 records off their defaults, D3 done 1 fail 1 rolled back 1, restore fail 1 blank 0, cause 2, terminal 3507 enable 3518
HOLDS R218 original F2 trigger (W12): 0 records off their defaults, D3 done 1 fail 1 rolled back 1, restore fail 1 blank 0, cause 3, terminal 23954 enable 23963
R218 PROBES: 6 runs, 0 not as demanded

# R217's own check_probes.py (7d9da877), which asserts the round-two counterexamples, on the same results:
  File "$PROBE_OUT/r217/check_probes.py", line 19, in <module>
    assert obs['restore_done'] == 1 and obs['restore_fail'] == 0 and obs['entity_en'] == 1
AssertionError
exit 1
```

## Digests (`python3 -B run.py receipts`)

