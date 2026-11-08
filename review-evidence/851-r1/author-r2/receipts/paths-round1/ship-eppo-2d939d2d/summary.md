# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `9557932cfa08146f7dda4e70d6b432b5cd2db2eeaaeffd5bbc0e2226feef1028`, 115918396 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.044 | 0.044 | yes | 36  (CARRY4=11 LUT2=7 LUT3=2 LUT4=4 LUT5=3 LUT6=9) | 19.588ns  (logic 6.749ns (34.454%)  route 12.839ns (65.545%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[17]/R` | milansoc_crg_clkout1 |
| Slow_0C | hold | 0.066 | 0.066 | yes | 0 | 0.753ns  (logic 0.304ns (40.347%)  route 0.449ns (59.653%)) | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[5][1]/C` | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc/mem_r_reg_1/DIBDI[17]` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.044 | 0.044 | yes | 36  (CARRY4=11 LUT2=7 LUT3=2 LUT4=4 LUT5=3 LUT6=9) | 19.588ns  (logic 6.749ns (34.454%)  route 12.839ns (65.545%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[17]/R` | milansoc_crg_clkout1 |
| Slow_85C | hold | 0.066 | 0.066 | yes | 0 | 0.753ns  (logic 0.304ns (40.347%)  route 0.449ns (59.653%)) | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[5][1]/C` | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc/mem_r_reg_1/DIBDI[17]` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.408 | 1.408 | yes | 0 | 0.525ns  (logic 0.175ns (33.353%)  route 0.350ns (66.647%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_0C | hold | 0.035 | 0.035 | yes | 0 | 0.387ns  (logic 0.141ns (36.388%)  route 0.246ns (63.612%)) | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[7][18]/C` | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc/mem_r_reg_2/DIBDI[10]` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.408 | 1.408 | yes | 0 | 0.525ns  (logic 0.175ns (33.353%)  route 0.350ns (66.647%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_85C | hold | 0.035 | 0.035 | yes | 0 | 0.387ns  (logic 0.141ns (36.388%)  route 0.246ns (63.612%)) | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[7][18]/C` | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc/mem_r_reg_2/DIBDI[10]` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `9e9143237ce55546d66db7df0362958aafd7a6880d23c1c364dbcfd489ba15c0`, 1365994 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `38eee5686c5c27c6c0017b02300681f17291e74025d3686f2948ba598ec5c815`, 1365995 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `e3fc6448f0639274a581c37371f229851b358d96fa7995a5e3662ebcec400d77`, 1306288 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `85928fe0ea19947e818df2b46ea91424438023a58d1f26e1aaf14c4f7cca6156`, 1306289 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
