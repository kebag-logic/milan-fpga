# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `7f00e872ce874d3e7d5f5fb2fde77de7d8c26c138e40c4c2b1f37ab82705928d`, 43291282 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.210 | 0.210 | yes | 37  (CARRY4=13 LUT2=6 LUT3=3 LUT4=3 LUT5=5 LUT6=7) | 19.258ns  (logic 6.316ns (32.797%)  route 12.942ns (67.203%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][1]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[10]/R` | milansoc_crg_clkout1 |
| Slow_0C | hold | 0.069 | 0.069 | yes | 0 | 0.837ns  (logic 0.304ns (36.304%)  route 0.533ns (63.696%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[254]/C` | `storage_11_reg_3/DIBDI[6]` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.210 | 0.210 | yes | 37  (CARRY4=13 LUT2=6 LUT3=3 LUT4=3 LUT5=5 LUT6=7) | 19.258ns  (logic 6.316ns (32.797%)  route 12.942ns (67.203%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][1]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[10]/R` | milansoc_crg_clkout1 |
| Slow_85C | hold | 0.069 | 0.069 | yes | 0 | 0.837ns  (logic 0.304ns (36.304%)  route 0.533ns (63.696%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mBusAxi_w_s2mPipe_rData_data_reg[254]/C` | `storage_11_reg_3/DIBDI[6]` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.520 | 1.520 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[34]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_114_119/RAMA/I` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.520 | 1.520 | yes | 0 | 0.408ns  (logic 0.175ns (42.843%)  route 0.233ns (57.157%)) | `FDPE_22/C` | `FDPE_23/D` | milansoc_crg_clkout1 |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[34]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_114_119/RAMA/I` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `d4f96f7f71721bbb6c878b0cb47be5f0e32fa409dadfedfcee878b562b4b0d88`, 1370348 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `6607a196e11d44f24e449a64259bfc26376293c4fce773e3dbee8dbb5c9f509e`, 1370349 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `1a7160e41ee308c6db98324aa20c555f4d6a90749075b515c71559c6b1c3c5b3`, 1311289 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `716a54186707badcd325e90fd01c87ac2e9504991eefb04088ed0cabf975f67e`, 1311290 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
