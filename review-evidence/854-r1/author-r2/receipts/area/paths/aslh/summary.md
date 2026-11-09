# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `d2e55e236d9b97ff9ec6db9047441c9c1f9d5940dc7adab9ac03bf21c7876655`, 43876950 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.147 | 0.147 | yes | 16  (CARRY4=2 LUT2=5 LUT3=2 LUT4=1 LUT5=1 LUT6=4 MUXF7=1) | 9.399ns  (logic 2.930ns (31.173%)  route 6.469ns (68.827%)) | `milansoc_sdram_bankmachine3_row_reg[5]/C` | `milansoc_sdram_twtrcon_ready_reg/R` | milansoc_crg_clkout0 |
| Slow_0C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_originator/tmr_arm_deadline_ms_o_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/g_armq[4].mem_r_reg_0_3_0_5/RAMA/I` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.147 | 0.147 | yes | 16  (CARRY4=2 LUT2=5 LUT3=2 LUT4=1 LUT5=1 LUT6=4 MUXF7=1) | 9.399ns  (logic 2.930ns (31.173%)  route 6.469ns (68.827%)) | `milansoc_sdram_bankmachine3_row_reg[5]/C` | `milansoc_sdram_twtrcon_ready_reg/R` | milansoc_crg_clkout0 |
| Slow_85C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_originator/tmr_arm_deadline_ms_o_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/g_armq[4].mem_r_reg_0_3_0_5/RAMA/I` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.525 | 1.525 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[52]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_132_137/RAMA/I` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.525 | 1.525 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[52]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_132_137/RAMA/I` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `9dfe7c53c41991e9200c99340ffe15bca098b6aff6a604168de6b48a1bcd5cb0`, 1353230 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `a4379a01f85c2f7add6a022e7c0eee6a872707b1ad8ffed27eaa0af01d137dc3`, 1353231 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `840f88218104dc1bc9d50b3ed2fe24184e9dc864466973822a09403061d01f7f`, 1303424 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `42c6988d641aaf865fee06b86f7be2fb43764f63416111b8d60379dd1c0806c6`, 1303425 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
