# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `3b62758f2a84ac10e7230afbeff3376a846bdd5fc04c6eb87e3b1491c029f617`, 115097723 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.166 | 0.166 | yes | 37  (CARRY4=12 LUT2=7 LUT3=3 LUT4=4 LUT5=5 LUT6=6) | 19.393ns  (logic 6.494ns (33.485%)  route 12.899ns (66.515%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][1]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[13]/R` | milansoc_crg_clkout1 |
| Slow_0C | hold | 0.050 | 0.050 | yes | 0 | 0.743ns  (logic 0.304ns (40.937%)  route 0.439ns (59.063%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[252]/C` | `storage_11_reg_3/DIBDI[4]` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.166 | 0.166 | yes | 37  (CARRY4=12 LUT2=7 LUT3=3 LUT4=4 LUT5=5 LUT6=6) | 19.393ns  (logic 6.494ns (33.485%)  route 12.899ns (66.515%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][1]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[13]/R` | milansoc_crg_clkout1 |
| Slow_85C | hold | 0.050 | 0.050 | yes | 0 | 0.743ns  (logic 0.304ns (40.937%)  route 0.439ns (59.063%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[252]/C` | `storage_11_reg_3/DIBDI[4]` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.633 | 1.633 | yes | 0 | 0.269ns  (logic 0.204ns (75.759%)  route 0.065ns (24.241%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_0C | hold | 0.032 | 0.032 | yes | 0 | 0.387ns  (logic 0.141ns (36.472%)  route 0.246ns (63.528%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[252]/C` | `storage_11_reg_3/DIBDI[4]` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.633 | 1.633 | yes | 0 | 0.269ns  (logic 0.204ns (75.759%)  route 0.065ns (24.241%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_85C | hold | 0.032 | 0.032 | yes | 0 | 0.387ns  (logic 0.141ns (36.472%)  route 0.246ns (63.528%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[252]/C` | `storage_11_reg_3/DIBDI[4]` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `78766895aedfab8fa22c7ed1bdddbcf812b106f09e5749177dfe61b02935ce02`, 1356618 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `a84d811423cb4636eb53f7acb58132f9fdb8dea282a4893e940f8cb16b5d5565`, 1356619 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `7c4701ec243360de4283b8343579787744d0ac578607da67680d2d0eca94a7c5`, 1316604 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `76c411934d9ab0485d9c0253a7a8ac91b77bc6f78c92b3c6a8a26683f5774206`, 1316605 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
