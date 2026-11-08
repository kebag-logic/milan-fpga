# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `e9711def60d3df609ad6232b1061241d21db8291a6b9d65f666ed2b611cebeae`, 43689699 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.258 | 0.258 | yes | 29  (CARRY4=2 LUT2=4 LUT3=4 LUT4=4 LUT5=4 LUT6=11) | 19.439ns  (logic 5.202ns (26.760%)  route 14.237ns (73.240%)) | `milan_datapath/pp_shadow/u_pp/u_notify/ctr_pend_r_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/u_nvm_shadow/hs_r_reg[1]/CE` | milansoc_crg_clkout1 |
| Slow_0C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_b0_r_reg[14]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_r_reg_0_31_78_83/RAMA/I` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.258 | 0.258 | yes | 29  (CARRY4=2 LUT2=4 LUT3=4 LUT4=4 LUT5=4 LUT6=11) | 19.439ns  (logic 5.202ns (26.760%)  route 14.237ns (73.240%)) | `milan_datapath/pp_shadow/u_pp/u_notify/ctr_pend_r_reg[0]/C` | `milan_datapath/pp_shadow/u_pp/u_nvm_shadow/hs_r_reg[1]/CE` | milansoc_crg_clkout1 |
| Slow_85C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_b0_r_reg[14]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_r_reg_0_31_78_83/RAMA/I` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.375 | 1.375 | yes | 0 | 0.585ns  (logic 0.175ns (29.889%)  route 0.410ns (70.111%)) | `FDPE_14/C` | `FDPE_15/D` | eth_clocks0_rx |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/cap_l_r_reg[18]/C` | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/u_tcdc/mem_r_reg_0_7_42_47/RAMA/I` | milansoc_crg_audio_mclk_raw |
| Fast_85C | setup | 1.375 | 1.375 | yes | 0 | 0.585ns  (logic 0.175ns (29.889%)  route 0.410ns (70.111%)) | `FDPE_14/C` | `FDPE_15/D` | eth_clocks0_rx |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/cap_l_r_reg[18]/C` | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/u_tcdc/mem_r_reg_0_7_42_47/RAMA/I` | milansoc_crg_audio_mclk_raw |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `9acaf0197977fd88d11558c1281308ce3093b10aa447d2010be6a4137da5d578`, 1349419 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `cdc1334e62f2822fa548c9825543ad868ac3f9ca9d4054e5568a7c9004af3b09`, 1349420 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `1028395ba8461a9e3058f88a101cf8079a8702d090338d521f74e1186e8fabe5`, 1310470 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `970155ff1fcd23e25c2943053c11f50810e4175a9ecc330cd889129ec5586f20`, 1310471 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
