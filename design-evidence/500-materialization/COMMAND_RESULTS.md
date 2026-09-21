# D3 materialization: command record

Every command the design page quotes, its exit status and the digests of what it read and wrote.
Base of the tree: dev `07294a76e833f1831d9fcbceb8123b8380c4ae76` (protocol-processor `424c688f`).
Scratch output (build trees, run logs) is outside the tree: `$D3_OUT`, `$OOC_OUT`. The run below started
from an EMPTY `$D3_OUT`.

## Commands

| Command (from `design-evidence/500-materialization/proposal-evidence`) | Exit | Result |
|---|---|---|
| `python3 -B run.py prep` | 0 | shape 1x1: 53 records; shape 8x8: 156 records |
| `python3 -B run.py build --pool 1 --jobs 8` | 0 | 27 builds: base-1x1, base-8x8, tracked-1x1, 24 mutants |
| `python3 -B run.py run --pool 8` | 0 | `SUMMARY runs 121, checks 778, verdict failures 0` |
| `ooc/run_ooc.sh` | 0 | 16 rows, `ooc/results_ooc.txt` |
| `syn/yosys/ooc.sh KL_nvm_backend` (repository root, `OOC_CHPARAM` of the 1x1 shape with `N_NAME_P=30`) | 0 | `1030 LUT, 0 LUTRAM, 468 FF, 6 DSP, 114 CARRY4`, identical to the row `cal-backend-1x1-n30` |

Tools: Verilator 5.052, gcc (host), sv2v v0.0.13, Yosys 0.66 (git sha1 86f2ddebc).

## Verdicts (the tail of `results.txt`)

```
PREMISE base-1x1 K15: the binding manager sampled busy on the D3 writer's grant cycle at g3 (1 of 8 releases) -> reached
MUTANT A01_grant_cycle_not_busy: KILLED by K15_binding_on_the_d3_grant_cycle~g3 : both_records_committed
MUTANT F01_old_boot_order: KILLED by V1b_restore_everything : value_restored:0x50
MUTANT G01_pend_misses_d3: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved
MUTANT G02_restore_done_without_d3: KILLED by V1b_restore_everything : entity_enabled_after_restore@boot
MUTANT G03_restore_writes_are_changes: KILLED by V1b_restore_everything : restore_sets_no_dirty@boot
MUTANT G04_blank_ignores_d3: KILLED by V7_names_only : blank_is_both_walks@boot
MUTANT M01_taint_ignored: KILLED by K2_change_during_record_write : no_durable_claim_over_unsaved
MUTANT M02_clear_at_latch: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved
MUTANT M03_clear_wins_same_edge: KILLED by K5_change_on_the_done_edge : same_edge_change_survives@end:0x50
MUTANT M04_clear_by_group: KILLED by K4_second_record_in_flight : value_in_slot@end:0x51
MUTANT M05_latch_ignores_program: KILLED by K11_name_latch_waits_for_the_program : written_value_was_set:0x80
MUTANT M06_identify_is_a_change: KILLED by K14_identify_is_not_persisted : identify_never_persisted
MUTANT M08_restore_skips_image_check: KILLED by V7_names_only : restored_name_survives_first_command:0x80
MUTANT M09_apply_blindly: KILLED by V2_refused_rate : refused_value_not_applied:0x02
MUTANT M10_fmt_full_judge: KILLED by V6b_restore_coupled_pair : coupled_pair_restored
MUTANT M11_no_orphan_check: KILLED by V8_orphaning_format_reverted : no_orphaned_mapping_after_restore
MUTANT M12_no_revert_before_readd: KILLED by V9_refused_maps_revert_their_formats : refused_group_falls_back_to_default:0x70
MUTANT M13_restore_applies_nothing: KILLED by V1b_restore_everything : value_restored:0x50
CONTROL stale store under M13: naive read-back PASSES, cleared-first FAILS -> as required
MUTANT M14_clear_by_index: KILLED by K4g_second_group_in_flight : value_in_slot@end:0x0a
MUTANT M15_overflow_forgets_the_change: KILLED by K16_map_set_larger_than_its_record : no_durable_claim_over_unsaved
MUTANT M16_single_pass_restore: KILLED by V11_torn_read_restores_nothing : torn_walk_applies_nothing@boot
MUTANT M17_trigger_misses_ptof: KILLED by K1_single_change_converges : no_durable_claim_over_unsaved
MUTANT M18_trigger_misses_names: KILLED by K10_name_change_converges : no_durable_claim_over_unsaved
MUTANT M19_trigger_misses_out_maps: KILLED by K12_map_change_converges : no_durable_claim_over_unsaved
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
SUMMARY runs 121, checks 778, verdict failures 0
```

## Digests of the evidence (sha256)

| File | sha256 |
|---|---|
| `README.md` | `5b12c3492c584922d024e8c251291d015f391708a4db2c5203ab5692b1114d04` |
| `harness/d3_api.h` | `b5eecc8141f61235df83ae6832a565931314d454d201e0dd01e772793fd76905` |
| `harness/d3_bridge.cpp` | `35abbc83ebb6b783e37185e52029b44190a9ecf709627699e0d496644e73837c` |
| `harness/d3_bridge.h` | `ee38975fa435248e36df55bd02d449454ec140392b43d3f9dffc191299b20f25` |
| `harness/d3_cases.cpp` | `6f9f3a8c6bdf2218d285addb679b89e233f33f6a896ff24cb392a3a2a8ebe599` |
| `harness/d3_host.c` | `f213221a6f4f877a380362f6b9ab81dccd144ca49438d75da1e7f76eed3ee4e9` |
| `harness/d3_top.sv` | `f4dce1b825f241b0358bc78c932b1939e188054987eb4fc567c77de485973336` |
| `harness/stubs/command.h` | `a1582388437e74cf2c246cdc544e7a5abed9e94b655b5ba92053bdc65d6de6cc` |
| `harness/stubs/generated/csr.h` | `67d05a5b35dc82b1033675225a3bd24e446dda43535cf11cd7c538f0e3b2491a` |
| `harness/stubs/generated/mem.h` | `7dc2ecfb649dd841484877cedd8495068d5bcc773fb11ebf9f8bc6013f9343f8` |
| `harness/stubs/hw/common.h` | `d56b44d934a02d0b75b0b6bd10c123abeef08d3cb3c55c1aca07527d4e787598` |
| `harness/stubs/init.h` | `9e32c0958ab0f57feb8bfa3e7bb79ed57916f11243fc751f673fb7e805054c79` |
| `harness/stubs/libbase/crc.h` | `e8eba505669fd27493a523d28e841b210e221c2ef6d45ddf1e7f649c426fc18e` |
| `harness/stubs/nvm_host.h` | `f95dde646067c2bed12e5b09dbd428b2b9313780a6e83dc2a1a79c891c16b9cd` |
| `harness/stubs/system.h` | `50cfa4347bae790a1ba511881d76f72801c3ac93a7096915475991f5527b2cfa` |
| `ooc/abc.history` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `ooc/d3a_shadow_proxy.sv` | `71f89c38d8017bed308e7b24991a27ddc5e345423a9eed5d071dba86b2b98148` |
| `ooc/d3c_fabric_proxy.sv` | `5420360d9187335cf1a6beed9691a35df61bdfdf3bea54192453e67943661c87` |
| `ooc/ooc_measure.sh` | `fac7ab44abbe09d59c6b6db9629f25aefe175c7e818432a6254054fc5420a4ac` |
| `ooc/run_ooc.sh` | `69b39aeff320f93a77a296dd101dff46846dc6f00172f5d5f390b7d0c19af9bd` |
| `prototype/KL_aecp_nvm_writer.proto.sv` | `8cec2d1ade635b95424f19f31fcc12d203a18f22598b79e1ea2428ba4cb43df1` |
| `prototype/KL_pp_nvm_mgr_arb.proto.sv` | `4498fcbe9d6d90dc14ac5ce5c0d26df10f9e9ba55f9043a12279ca9d26722c6a` |
| `run.py` | `705241f4335dc7049abbc9508c27e0a2695b0e13435833d90ddd435ce4d3f9cd` |
| `results.txt` (output) | `0b112180e3770dc410e916327411f5852b887598bb2164e84fea99dd2beb49e2` |
| `results.json` (output) | `7816c802c03a3ac1e50b721b8874d1789b254793dc365af5b6d8a12271945720` |
| `ooc/results_ooc.txt` (output) | `3656422d6a7199018251ffca428b9c984a80d7737dc6d05b5e17e0006e531cad` |

## Digests of the repository files the model reads or compiles (sha256)

| File | sha256 |
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
