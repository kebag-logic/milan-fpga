# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `73fa48442e1071786186c8353c235ef3c58843aac5629eadded9de7cd6bb48f2`, 114847928 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.112 | 0.112 | yes | 13  (LUT2=3 LUT3=2 LUT4=4 LUT5=2 LUT6=2) | 9.355ns  (logic 2.520ns (26.938%)  route 6.835ns (73.062%)) | `milansoc_write_w_buffer_readable_reg/C` | `storage_17_reg_0_15_0_5/RAMA/WE` | milansoc_crg_clkout0 |
| Slow_0C | hold | 0.063 | 0.063 | yes | 0 | 0.741ns  (logic 0.304ns (41.033%)  route 0.437ns (58.967%)) | `milansoc_dd_reg[22]/C` | `storage_37_reg/DIBDI[14]` | milansoc_crg_clkout0 |
| Slow_85C | setup | 0.112 | 0.112 | yes | 13  (LUT2=3 LUT3=2 LUT4=4 LUT5=2 LUT6=2) | 9.355ns  (logic 2.520ns (26.938%)  route 6.835ns (73.062%)) | `milansoc_write_w_buffer_readable_reg/C` | `storage_17_reg_0_15_0_5/RAMA/WE` | milansoc_crg_clkout0 |
| Slow_85C | hold | 0.063 | 0.063 | yes | 0 | 0.741ns  (logic 0.304ns (41.033%)  route 0.437ns (58.967%)) | `milansoc_dd_reg[22]/C` | `storage_37_reg/DIBDI[14]` | milansoc_crg_clkout0 |
| Fast_0C | setup | 1.465 | 1.465 | yes | 0 | 0.453ns  (logic 0.204ns (45.062%)  route 0.249ns (54.938%)) | `FDPE_10/C` | `FDPE_11/D` | milansoc_crg_clkout4 |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/pp_shadow/u_pp/u_listener/tmr_arm_owner_o_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/g_armq[0].mem_r_reg_0_3_42_46/RAMA/I` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.465 | 1.465 | yes | 0 | 0.453ns  (logic 0.204ns (45.062%)  route 0.249ns (54.938%)) | `FDPE_10/C` | `FDPE_11/D` | milansoc_crg_clkout4 |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/pp_shadow/u_pp/u_listener/tmr_arm_owner_o_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/g_armq[0].mem_r_reg_0_3_42_46/RAMA/I` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `010305fbc7d16e94859a786dd7c128385b354970b47332e20ffa51b4984e8258`, 1352881 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `cc7e468cb18019e28458396384d09bac5470ba7139a2ccdbefcb03bf77504ed4`, 1352882 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `eff5ed5ceabba64f29dc4cf3e61a0765051c2d0d078554ff97736b3bc5196ad6`, 1274216 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `f3b77a7d1f40510f5edde9e72bdc5cecc8068144d1817e5855166800a208de30`, 1274217 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
