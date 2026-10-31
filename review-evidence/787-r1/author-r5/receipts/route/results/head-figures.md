### EPPO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.090 | 0.000 | +0.052 | 0.000 |
| Slow_85C | +0.090 | 0.000 | +0.052 | 0.000 |
| Fast_0C | +1.660 | 0.000 | +0.028 | 0.000 |
| Fast_85C | +1.660 | 0.000 | +0.028 | 0.000 |

LUT 51,960; FF 54,101; slices 15,820 of 15,850 (30 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.090 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout1`; `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]/C` -> `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[25]/R`; requirement 20.000ns  (milansoc_crg_clkout1 rise@20.000ns - milansoc_crg_clkout1 rise@0.000ns); data path 19.372ns  (logic 6.560ns (33.864%)  route 12.812ns (66.136%)); logic levels 36  (CARRY4=11 LUT2=7 LUT3=1 LUT4=6 LUT5=3 LUT6=8)

### ASLH

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.365 | 0.000 | +0.053 | 0.000 |
| Slow_85C | +0.365 | 0.000 | +0.053 | 0.000 |
| Fast_0C | +1.633 | 0.000 | +0.015 | 0.000 |
| Fast_85C | +1.633 | 0.000 | +0.015 | 0.000 |

LUT 52,021; FF 54,102; slices 15,787 of 15,850 (63 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.365 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/aligner/downW_header_reg[2]_replica/C` -> `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/pendings_valids_reg[0]/D`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.527ns  (logic 2.269ns (23.817%)  route 7.258ns (76.183%)); logic levels 18  (LUT2=1 LUT3=4 LUT4=6 LUT5=2 LUT6=5)

### ETO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.204 | 0.000 | +0.053 | 0.000 |
| Slow_85C | +0.204 | 0.000 | +0.053 | 0.000 |
| Fast_0C | +1.633 | 0.000 | +0.015 | 0.000 |
| Fast_85C | +1.633 | 0.000 | +0.015 | 0.000 |

LUT 52,017; FF 54,101; slices 15,787 of 15,850 (63 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.204 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout1`; `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]/C` -> `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3/deb_cnt_r_reg[0]/R`; requirement 20.000ns  (milansoc_crg_clkout1 rise@20.000ns - milansoc_crg_clkout1 rise@0.000ns); data path 19.257ns  (logic 6.698ns (34.781%)  route 12.559ns (65.219%)); logic levels 36  (CARRY4=12 LUT2=6 LUT3=1 LUT4=6 LUT5=3 LUT6=8)

