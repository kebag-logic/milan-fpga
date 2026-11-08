# Worst paths, report_timing of the routed checkpoint

Checkpoint: `alinx_ax7101_route.dcp`, sha256 `214a8b2d0b37ab23241cc19d915dd4a0cc80e1e2f3071204aa1182ea6c664246`, 43505059 bytes (not copied).

| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |
|---|---|---:|---:|---|---|---|---|---|---|
| Slow_0C | setup | 0.028 | 0.028 | yes | 16  (LUT2=1 LUT3=3 LUT4=3 LUT5=1 LUT6=8) | 9.844ns  (logic 2.113ns (21.465%)  route 7.731ns (78.535%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/aligner/downW_header_reg[0]/C` | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/pendings_valids_reg[0]/D` | milansoc_crg_clkout0 |
| Slow_0C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_b0_r_reg[20]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_r_reg_0_31_84_89/RAMA/I` | milansoc_crg_clkout1 |
| Slow_85C | setup | 0.028 | 0.028 | yes | 16  (LUT2=1 LUT3=3 LUT4=3 LUT5=1 LUT6=8) | 9.844ns  (logic 2.113ns (21.465%)  route 7.731ns (78.535%)) | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/aligner/downW_header_reg[0]/C` | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/pendings_valids_reg[0]/D` | milansoc_crg_clkout0 |
| Slow_85C | hold | 0.102 | 0.102 | yes | 0 | 0.424ns  (logic 0.304ns (71.652%)  route 0.120ns (28.348%)) | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_b0_r_reg[20]/C` | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store/idx_r_reg_0_31_84_89/RAMA/I` | milansoc_crg_clkout1 |
| Fast_0C | setup | 1.580 | 1.580 | yes | 0 | 0.376ns  (logic 0.175ns (46.600%)  route 0.201ns (53.400%)) | `FDPE_18/C` | `FDPE_19/D` | eth_clocks0_rx |
| Fast_0C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[40]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_120_125/RAMA/I` | milansoc_crg_clkout1 |
| Fast_85C | setup | 1.580 | 1.580 | yes | 0 | 0.376ns  (logic 0.175ns (46.600%)  route 0.201ns (53.400%)) | `FDPE_18/C` | `FDPE_19/D` | eth_clocks0_rx |
| Fast_85C | hold | 0.036 | 0.036 | yes | 0 | 0.196ns  (logic 0.141ns (71.838%)  route 0.055ns (28.162%)) | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/frame_cid_r_reg[40]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_120_125/RAMA/I` | milansoc_crg_clkout1 |

Signoff summaries (the route's own, not copied):

- `alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `e99456723aff9162b28f144e08da2d0c184945363d35d5c1629cbfb9b903e326`, 1357887 bytes
- `alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `7a3735a71fe89ed5a498be102cbb2c4c6a2c392b6b12123e52100ec2ec0530f0`, 1357888 bytes
- `alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `2a9c2d91c25a4268799cc7721e075f64968cae530a91eacf52731f626ae6fd70`, 1322301 bytes
- `alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `b54f3a0d80dd30a399ac0b1cc7535720b378926261c585c8150ff482541287a1`, 1322302 bytes

Result: PASS: every excerpt's slack equals its corner's WNS (setup) or WHS (hold).
