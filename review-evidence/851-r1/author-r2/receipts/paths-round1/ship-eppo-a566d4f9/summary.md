# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `c4f8c2ee1574b52992d67491bcf00fc086be1078f156e789dd79c03b36fa5a95`, 115960579 bytes (not copied).

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

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `767f8ed730315d0fa951c916e02a08d0019b588f49ec750296e05312ae702dbf`, 1365994 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `bbe0b164fb06389f1c56f26f103ced4c2813fd768a60ca36730447d422938d37`, 1365995 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `361f298034beb8b34a288a2e65ea33e24f279f340fd42c5a8c9392e43ef41ca8`, 1306288 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `4f5764cc84bdc31f5874b237c5663519189a264e9085e082df9641f8173c7d15`, 1306289 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
