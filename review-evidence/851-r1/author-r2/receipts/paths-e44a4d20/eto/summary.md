# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `e40872cbd6f2f264dad8bb9bb821f64df38235f7491fb3e3c8b913ee9686f674`, 43159767 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.018 | 0.018 | yes | 34  (CARRY4=10 LUT2=7 LUT3=2 LUT4=2 LUT5=6 LUT6=7) | 19.444ns  (logic 6.367ns (32.745%)  route 13.077ns (67.255%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/desc_base_r_reg[5]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[25]/R` | milansoc_crg_clkout1 |
| Slow_0C | hold | 0.091 | 0.091 | yes | 0 | 0.781ns  (logic 0.304ns (38.936%)  route 0.477ns (61.064%)) | `milan_datapath/pp_shadow/u_nvm/addr_r_reg[25]/C` | `storage_44_reg_0/DIADI[25]` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.018 | 0.018 | yes | 34  (CARRY4=10 LUT2=7 LUT3=2 LUT4=2 LUT5=6 LUT6=7) | 19.444ns  (logic 6.367ns (32.745%)  route 13.077ns (67.255%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/desc_base_r_reg[5]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[25]/R` | milansoc_crg_clkout1 |
| Slow_85C | hold | 0.091 | 0.091 | yes | 0 | 0.781ns  (logic 0.304ns (38.936%)  route 0.477ns (61.064%)) | `milan_datapath/pp_shadow/u_nvm/addr_r_reg[25]/C` | `storage_44_reg_0/DIADI[25]` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.520 | 1.520 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[34]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_114_119/RAMA/I` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.520 | 1.520 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[34]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_114_119/RAMA/I` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `3db35998c3f1935ce1ca12e84dfcd084f9f8b921ad1f6df8049a6c24f236b651`, 1348785 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `3e5336bfea35ced0f0e5881d3e1059c815f6974697de63ff91391885e3784267`, 1348786 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `0e834bb24f783f2ed80a5b8a9aa5b2617e817faf98c0f06fca7188955f745687`, 1297075 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `3b2f6b30cb93e139ff43826b0a63571205152c14c5168b649a12e41cb501fbf5`, 1297076 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
