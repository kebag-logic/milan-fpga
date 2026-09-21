# D3 materialization: command record

Every command the design page quotes, its real exit status and the digests
of what it read and wrote. Base of the tree: dev
`07294a76e833f1831d9fcbceb8123b8380c4ae76` (protocol-processor `424c688f`,
gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`). The
executable sources the run used are this commit's; the run started from an
EMPTY `$D3_OUT` and an EMPTY `$OOC_OUT`. Scratch output (build trees, run
logs, the area tool's working files) is outside the tree, under `$D3_OUT`,
`$OOC_OUT` and `$OOC_TMP`. Every command ran synchronously, pinned to one
set of 32 CPUs, with at most eight build jobs and one build pool.

This revision (A152) answers the round-one reviews of the page at
`d0256846`. The round-one record was commit
`a21b165ac1c671d10cba7255beaf75cea0f81d18`.

## Commands

| Command (from `design-evidence/500-materialization/proposal-evidence`) | Exit | Result |
|---|---|---|
| `python3 -B run.py prep` | 0 | shape 1x1 (shipped): 53 records; 8x8 (shipped): 156; 1x1r2 (SYNTHETIC): 53 |
| `python3 -B run.py build <the first 28 builds> --pool 1 --jobs 8` | 0 | 28 built |
| `python3 -B run.py build <the other 27 builds> --pool 1 --jobs 8` | 0 | 27 built: 55 in all (3 base shapes, the tracked glue, 51 mutants) |
| `python3 -B run.py run --pool 8` | 0 | `SUMMARY FULL builds 55, runs 230, checks 2524, verdict failures 0` |
| `python3 -B run.py controls --pool 8` | 0 | `CONTROLS 7, not as required 0` (each control's own exit below) |
| `ooc/run_ooc.sh` (from inside `$OOC_OUT`) | 0 | 16 rows, `ooc/results_ooc.txt` |
| `syn/yosys/ooc.sh KL_nvm_backend` (repository root, `OOC_CHPARAM` of the 1x1 shape with `N_NAME_P=30`) | 0 | `1030 LUT, 0 LUTRAM, 468 FF, 6 DSP, 114 CARRY4`, identical to the row `cal-backend-1x1-n30` |
| `python3 -B run.py receipts` | 0 | the digest tables below |

The builds were split in two synchronous commands only to keep each under
the session's command limit; `run.py build` with no name builds all 55.

Tools: Verilator 5.052, gcc (host), sv2v v0.0.13, Yosys 0.66 (git sha1
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
| empty_selection | none; build `no-such-build` | 2 | 2 | `REFUSED: no such build ['no-such-build']` |

```
CONTROL healthy_binary_as_mutant: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL binary_fails_before_the_scenario: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL failed_baseline_result: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL tracked_control_violated: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL vacuity_control_violated: AS REQUIRED -- exit 1 (required 1); diagnostics found
CONTROL tracked_control_absent: AS REQUIRED -- exit 2 (required 2); diagnostics found
CONTROL empty_selection: AS REQUIRED -- exit 2 (required 2); diagnostics found
CONTROLS 7, not as required 0
```

## Verdicts (the tail of `results.txt`)

```
PREMISE base-1x1 K15: the binding manager sampled busy on the D3 writer's grant cycle at g3 (1 of 8 releases) -> reached
MUTANT A01_grant_cycle_not_busy: KILLED by K15_binding_on_the_d3_grant_cycle~g3 : both_records_committed -- binding None, 0x50 0016e36f, grant-cycle collisions 1
MUTANT D01_abandoned_read_not_drained: KILLED by W6_late_pass1_after_deadline : later_change_persists@recovered -- latest 0076adf1, newest verified slot 0016e360
MUTANT F01_old_boot_order: KILLED by V1b_restore_everything : value_restored:0x50 -- live (0, 0) want (1500000, 1) (value, valid)
MUTANT G01_pend_misses_d3: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved -- change of 0x50 at 33739 inside a durable interval ending 4611686018427387904
MUTANT G02_restore_done_without_d3: KILLED by V1b_restore_everything : entity_enabled_after_restore@boot -- enabled at 188, D3 restore done at 7605, restore done at 177
MUTANT G03_restore_writes_are_changes: KILLED by V1b_restore_everything : restore_sets_no_dirty@boot -- 6 record writes after the restore, dirty 0, flash erases 0 -> 1
MUTANT G04_blank_ignores_d3: KILLED by V7_names_only : blank_is_both_walks@boot -- a name came back and no binding did: blank 1, done 1
MUTANT G05_enable_not_released_by_restore: KILLED by W14_binding_walk_late_after_fw_deadline : entity_enabled_after_terminal@boot -- entity enabled at 3000074, D3 terminal at 3107603, restore done at 3107603, firmware asked at 3000074
MUTANT M01_taint_ignored: KILLED by K2_change_during_record_write : no_durable_claim_over_unsaved -- durable at 1568748: record 0x50 latest 0021e88e slot 0010f447
MUTANT M02_clear_at_latch: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved -- durable at 533028: record 0x50 latest 0012d687 slot None
MUTANT M03_clear_wins_same_edge: KILLED by K5_change_on_the_done_edge : same_edge_change_survives@end:0x50 -- latest 004c4b42, newest verified slot 004c4b41
MUTANT M04_clear_by_group: KILLED by K4_second_record_in_flight : value_in_slot@end:0x51 -- latest 003d0902, newest verified slot None
MUTANT M05_latch_ignores_program: KILLED by K11_name_latch_waits_for_the_program : written_value_was_set:0x80 -- 2 writes; first bad 4b3131207365636f6e642076616c75652042424242424242424242424242424242424242424242424242424242424242414141414141414141414141
MUTANT M06_identify_is_a_change: KILLED by K14_identify_is_not_persisted : identify_never_persisted -- 1 record writes, dirty 0, pend 0, flash programs 0 -> 13
MUTANT M08_restore_skips_image_check: KILLED by V7_names_only : restored_name_survives_first_command:0x80 -- after the first command b'Milan FPGA 1x1 TDM8\x00\x00\x00\x00\x00'
MUTANT M09_apply_blindly: KILLED by V2_refused_rate : refused_value_not_applied:0x02 -- rate row valid 1, refused 0
MUTANT M10_fmt_full_judge: KILLED by V6b_restore_coupled_pair : coupled_pair_restored -- fmto0 0 valid 0; OUT0 set matches the slot True
MUTANT M11_no_orphan_check: KILLED by V8_orphaning_format_reverted : no_orphaned_mapping_after_restore -- stream 0 format 0x205022000806000 (2 channels), 6 orphaned mappings
MUTANT M12_no_revert_before_readd: KILLED by V9_refused_maps_revert_their_formats : refused_group_falls_back_to_default:0x70 -- live OUT0 equals the default True, fmto0 0x205022002006000, ptof0 0 valid 0, rolled back 1
MUTANT M13_restore_applies_nothing: KILLED by V1b_restore_everything : value_restored:0x50 -- live (0, 0) want (1500000, 1) (value, valid)
CONTROL stale store under M13: naive read-back PASSES, cleared-first FAILS -> as required
MUTANT M14_clear_by_index: KILLED by K4g_second_group_in_flight : value_in_slot@end:0x0a -- latest 0001, newest verified slot None
MUTANT M15_overflow_forgets_the_change: KILLED by K16_map_set_larger_than_its_record : no_durable_claim_over_unsaved -- durable at 1601552: record 0x70 latest 00000000000000000000000100010000000000020002000000000003000300000000000400040000000000050005000000000
MUTANT M16_single_pass_restore: KILLED by V11_torn_read_restores_nothing : torn_walk_applies_nothing@boot -- ptof0 valid 0 (its record was read whole before the torn one), restore fail 1, D3 fail 1, applied 1, rolled back 1
MUTANT O01_own_taken_at_the_walk: KILLED by K19_command_before_the_restore : value_in_slot@end:0x50 -- latest 001d48d7, newest verified slot 0016e360
MUTANT P01_padding_by_first_byte: KILLED by V3a_map_index_0xff00 : map_record_verdict:0x70 -- live OUT0 empty (want the default set); applied 2 refused 0 blank 47 of 49
MUTANT P02_padding_holes_not_refused: KILLED by V3e_map_hole : malformed_refused_untouched:0x70 -- 3 map sets staged for a malformed record [(3631, 'map-remove'), (3653, 'map-add')]
MUTANT R01_no_rollback: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 1 rolled back 0 (want 1) close
MUTANT R02_rollback_skips_dyn_store: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal -- 6 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 1 rolled back 1 (want 1) close
MUTANT R03_rollback_skips_desc_store: KILLED by V15_rollback_pass1_late : rolled_back_to_defaults@terminal -- 1 records off their defaults ['0x80 live 443320726573746f72656420 want 4d696c616e20465047412031 from byte 0']; D3 done 1 fail 1 rolled back 
MUTANT R04_rollback_skips_maps: KILLED by V16_rollback_pass1_maps : rolled_back_to_defaults@terminal -- 1 records off their defaults ['0x60 live ffffffffffffffffffffffff want 000000020002000000000003 from byte 16']; D3 done 1 fail 1 rolled back
MUTANT R05_closed_releases_the_entity: KILLED by V17_rollback_cannot_validate : closed_keeps_entity_dark@recovered -- closed 0, restore done 1 fail 1, own 0, entity enabled 1 (first 6713), firmware asked at 6713, a GET answered 0
MUTANT RPL_cfg: KILLED by V1b_restore_everything : value_restored:0x00 -- live (0, 0) want (0, 1) (value, valid)
MUTANT RPL_clks: KILLED by V1b_restore_everything : value_restored:0x0a -- live (0, 0) want (1, 1) (value, valid)
MUTANT RPL_fmti: KILLED by V1b_restore_everything : value_restored:0x30 -- live (0, 0) want (145524899430031360, 1) (value, valid)
MUTANT RPL_fmto: KILLED by V1b_restore_everything : value_restored:0x40 -- live (0, 0) want (145524899438419968, 1) (value, valid)
MUTANT RPL_mapi: KILLED by V1b_restore_everything : value_restored:0x60 -- live 000000020002000000000003 want ffffffffffffffffffffffff from byte 16
MUTANT RPL_mapo: KILLED by V1b_restore_everything : value_restored:0x70 -- live 030000000000040004000000 want 100000ffffffffffffffffff from byte 29
MUTANT RPL_name: KILLED by V1b_restore_everything : value_restored:0x80 -- live 4d696c616e20465047412031 want 443320726573746f72656420 from byte 0
MUTANT RPL_ptof: KILLED by V1b_restore_everything : value_restored:0x50 -- live (0, 0) want (1500000, 1) (value, valid)
MUTANT RPL_rate: KILLED by V1b_restore_everything : value_restored:0x02 -- live (0, 0) want (96000, 1) (value, valid)
MUTANT TRG_cfg: KILLED by V1a_set_everything : value_in_slot@cut:0x00 -- latest 0000, newest verified slot None
MUTANT TRG_clks: KILLED by V1a_set_everything : value_in_slot@cut:0x0a -- latest 0001, newest verified slot None
MUTANT TRG_fmti: KILLED by V1a_set_everything : value_in_slot@cut:0x30 -- latest 0205022000806000, newest verified slot None
MUTANT TRG_fmto: KILLED by V1a_set_everything : value_in_slot@cut:0x40 -- latest 0205022001006000, newest verified slot None
MUTANT TRG_mapi: KILLED by V1a_set_everything : value_in_slot@cut:0x60 -- latest 00000000000000000000000100010000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, new
MUTANT TRG_mapo: KILLED by V1a_set_everything : value_in_slot@cut:0x70 -- latest 0000000000000000000000010001000000000002000200000000000300100000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
MUTANT TRG_name: KILLED by V1a_set_everything : value_in_slot@cut:0x80 -- latest 443320726573746f72656420656e74697479206e616d650000000000000000000000000000000000000000000000000000000000000000000000000000000000, new
MUTANT TRG_ptof: KILLED by V1a_set_everything : value_in_slot@cut:0x50 -- latest 0016e360, newest verified slot None
MUTANT TRG_rate: KILLED by V1a_set_everything : value_in_slot@cut:0x02 -- latest 00017700, newest verified slot None
MUTANT W01_no_restore_watchdog: KILLED by W4_silent_pass1 : restore_terminal_bounded@terminal -- stall began at 3544, D3 terminal at 0 (bound 30000 cycles)
MUTANT X01_passes_may_disagree: KILLED by V18_header_error_pass1 : rolled_back_to_defaults@terminal -- 9 records off their defaults ['0x00 live (0, 1) want (0, 0)', '0x0a live (1, 1) want (0, 0)']; D3 done 1 fail 0 rolled back 0 (want 1) close
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
SUMMARY FULL builds 55, runs 230, checks 2524, verdict failures 0
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
b-writer-1x1                       KL_aecp_nvm_writer           2153     72    2225    859      0      0    0    142
b-writer-1x1-nodsp                 KL_aecp_nvm_writer           2191     72    2263    859      0      0    0    142
b-writer-8x8                       KL_aecp_nvm_writer           2780     48    2828    984      0      0    0    144
b-writer-8x8-nodsp                 KL_aecp_nvm_writer           2737     48    2785    984      0      0    0    144
b-arbiter                          KL_pp_nvm_mgr_arb              48      0      48      3      0      0    0      0
a-manager-unit                     KL_acmp_nvm_shadow           1323      0    1323   1223      0      0    0     46
a-shadows-1x1                      d3a_shadow_proxy              146    112     258    228      1      0    0      0
a-shadows-8x8                      d3a_shadow_proxy              150     68     218    164      3      0    0      0
c-fabric-1x1                       d3c_fabric_proxy              530      0     530    266      0      0    0      0
c-fabric-8x8                       d3c_fabric_proxy             1631      0    1631    458      0      0    0      0
```

## Digests (sha256)

Every file this commit tracks under `design-evidence/500-materialization`
but this record itself, as `git ls-files` lists them: an ignored or
untracked file, such as the empty `abc.history` the area tool used to leave
beside its scripts, cannot enter it. The round-one record listed 39 entries
and one of them, `ooc/abc.history`, was never in its commit; its other 38
matched. The area tool now runs inside `$OOC_OUT`, where that file lands.
The ticket drafts are work contracts, not executed evidence; they are listed
so that the drafts this commit carries are pinned too.

| File (relative to design-evidence/500-materialization) | sha256 |
|---|---|
| `proposal-evidence/README.md` | `b9743bc9e0f432107f965d932d720309944dc008f5fbb8aa25d1dcb6408cd492` |
| `proposal-evidence/harness/d3_api.h` | `5295aeecaab9adea6297a58760049f0b6b97faa9c1039035a8fdc4ba2c99efc0` |
| `proposal-evidence/harness/d3_bridge.cpp` | `ee14234889dc6b2e9028fff9e065ff1c39fd81f656f3fe1e52815c2579895c02` |
| `proposal-evidence/harness/d3_bridge.h` | `a3b8825c9bea1149b57f90f4ff0ef93e70af17785672fffa138b4706a4c4199c` |
| `proposal-evidence/harness/d3_cases.cpp` | `1be0b24e382a630556ccddaaa0a4d5e2321ca5e77a0cace72ae326bdbacef30c` |
| `proposal-evidence/harness/d3_host.c` | `df2149af53dac5c5d61c9ae73d6ebbc3fed9ba69011a7f2faf9417c47cf6fce4` |
| `proposal-evidence/harness/d3_top.sv` | `e40a5531cf8b818247f05a428968a71d7bc07eef4739d7374e21977a226c43a8` |
| `proposal-evidence/harness/stubs/command.h` | `a1582388437e74cf2c246cdc544e7a5abed9e94b655b5ba92053bdc65d6de6cc` |
| `proposal-evidence/harness/stubs/generated/csr.h` | `67d05a5b35dc82b1033675225a3bd24e446dda43535cf11cd7c538f0e3b2491a` |
| `proposal-evidence/harness/stubs/generated/mem.h` | `7dc2ecfb649dd841484877cedd8495068d5bcc773fb11ebf9f8bc6013f9343f8` |
| `proposal-evidence/harness/stubs/hw/common.h` | `d56b44d934a02d0b75b0b6bd10c123abeef08d3cb3c55c1aca07527d4e787598` |
| `proposal-evidence/harness/stubs/init.h` | `9e32c0958ab0f57feb8bfa3e7bb79ed57916f11243fc751f673fb7e805054c79` |
| `proposal-evidence/harness/stubs/libbase/crc.h` | `e8eba505669fd27493a523d28e841b210e221c2ef6d45ddf1e7f649c426fc18e` |
| `proposal-evidence/harness/stubs/nvm_host.h` | `f95dde646067c2bed12e5b09dbd428b2b9313780a6e83dc2a1a79c891c16b9cd` |
| `proposal-evidence/harness/stubs/system.h` | `50cfa4347bae790a1ba511881d76f72801c3ac93a7096915475991f5527b2cfa` |
| `proposal-evidence/ooc/d3a_shadow_proxy.sv` | `71f89c38d8017bed308e7b24991a27ddc5e345423a9eed5d071dba86b2b98148` |
| `proposal-evidence/ooc/d3c_fabric_proxy.sv` | `5420360d9187335cf1a6beed9691a35df61bdfdf3bea54192453e67943661c87` |
| `proposal-evidence/ooc/ooc_measure.sh` | `d9c9ac5144439a08522297c58cabf2fafb7ff0a9ec9482b1a692c73eba22de64` |
| `proposal-evidence/ooc/results_ooc.txt` | `d983246c9ea0ecabf1713139747761736b4d8dd9223abbaa2ace23ad08370df4` |
| `proposal-evidence/ooc/run_ooc.sh` | `69b39aeff320f93a77a296dd101dff46846dc6f00172f5d5f390b7d0c19af9bd` |
| `proposal-evidence/prototype/KL_aecp_nvm_writer.proto.sv` | `c5774fa1de04c9cbc8e7f7d0e3aef4a0ed473b2c2b80badd5503c82f1c6a9497` |
| `proposal-evidence/prototype/KL_pp_nvm_mgr_arb.proto.sv` | `2af5258b1fe419c3fbd41b1321453c35ab31fc13ab8d941250bd28575eaee1a1` |
| `proposal-evidence/results.json` | `3806a7df050b5a31239f808203b1236f7d30e9a81d58df240ce97bd08712ebcd` |
| `proposal-evidence/results.txt` | `2537596f56a0cdbbaef80286d9664d47e7e5c1da50e1fe729d3665bb011bdc86` |
| `proposal-evidence/run.py` | `107a911c8ef57b47f6d1e2a96d8264573e4550213bf8c99df020b574bcf9a5b4` |
| `tickets/README.md` | `221d01c9d54eb3534f30b8a4c880344a080079aecc8070b6239a9248be3c5219` |
| `tickets/T1-processor-stage1-dynamic-state-writer.md` | `b48affce20513f9e821ecb894266f4cdd043aebb5d8cbc74a1494b1f846ac393` |
| `tickets/T2-processor-stage2-names.md` | `afa3f82b1b243e807f5911901c12cd875777501aa00387bca7e982818bf77735` |
| `tickets/T3-processor-stage3-channel-maps.md` | `6f88b8b2d9ab7f63560224f800f3afee7ff4aed4a6377bfd462eca5768eb08a9` |
| `tickets/T4-parent-glue-firmware-and-silicon-proof.md` | `8bd1310e51b273f59875dcb30028582f8300b79efc3cf873490006a8c7969a23` |
| `tickets/T5-output-map-record-size-at-8x8.md` | `14cdbeaedfe776baa3ed6cc7cc233fadf216cb78ad9d911a589f61bfa625c1d8` |
| `tickets/T6-mark-tail-durable-window.md` | `9f4bd29181c70200830f481a353818b2e1e1a939bb600759c4feea20adeeb6bc` |
| `tickets/T7-fastconnect-area-table-predates-484.md` | `cf578f71718ec4d5c7fd98bed16313866fbf713934693536c91537e9db0ea01f` |
| `tickets/T8-processor-issue-15-port-deadline.md` | `510a0059cf93ed78a84d46782776c6f6fa599e66234610d86028dce0b2302d08` |

| Repository file | sha256 |
|---|---|
| `protocol-processor/hdl/acmp/pp_acmp_pkg.sv` | `b504951db8c81134ef54030e37879431f84ea8005e38c46479c8f66dcc4bbb85` |
| `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv` | `c0916f98d71691f72b880b5332157beafbfe9b9dd5dc64bd351294d6edbee099` |
| `protocol-processor/hdl/aecp/KL_aecp_desc_store.sv` | `63bb80169ed4118b1d4e6e7ddc819a71648a9801abdd4b3984b7f75801039211` |
| `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv` | `d159048760dbe89a9d76570bf82b16f7ce7411608340e29543205631a1a0c351` |
| `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv` | `194e8120bf715103645e095288cbed84e7c3f1704647c2efbe3f2585f2dd76b6` |
| `hdl/milan/KL_nvm_backend.sv` | `d651d148f933d90dec5d8633c58adc86717bd8c8785b1c2edaf3ce5e9b9480a0` |
| `sw/firmware/milan_baremetal/milan_baremetal.c` | `b9bf12aeefd07ce59cb3d33f3c66337ac28847c5ca69acf7faa0219895aa90a2` |
| `scripts/nvm_klj2.py` | `eaa31c5956a6808a2bb94356cbb35e90074942134196dbf446d37b65f5a1c913` |
| `scripts/nvm_shape.py` | `fc1f93e32cbacdded00db6464d98b3fedf57e9e6a7b3bf93265e89a5b8afbb20` |
| `scripts/check_nvm_record_space.py` | `1883d2a55945e8aad0e897a21a81acbbbaeff0b5825839ff7f04573b31bbdc9d` |
| `sw/firmware/nvm_hosttest/test_nvm_firmware.py` | `e3bf8ff2295e733e496f3e866e44b72099aae730ef949b39ccf2e1fea9aacb74` |
| `configs/endstation_ax7101_1x1_tdm8.yaml` | `d2c757e2fcd24d3f494e8c3d2e9f798bf7eba9b7e201741e7125d4f27692c807` |
| `configs/endstation_ax7101_8x8.yaml` | `4cdb07dd064239e6403d3428134067f31fe70a92cab886ffa85f9d6b5794edac` |
| `sw/builder/endstation_builder.py` | `67a1262a282f2e23092b0f03c8e7bd96ba63fdef1415ab80aa7cc181b147234f` |
