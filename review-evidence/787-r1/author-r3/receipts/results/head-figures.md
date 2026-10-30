### head-EPPO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.165 | 0.000 | +0.102 | 0.000 |
| Slow_85C | +0.165 | 0.000 | +0.102 | 0.000 |
| Fast_0C | +1.565 | 0.000 | +0.036 | 0.000 |
| Fast_85C | +1.565 | 0.000 | +0.036 | 0.000 |

LUT 51,568; FF 53,680; slices 15,749 of 15,850 (101 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.165 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_write_w_buffer_readable_reg/C` -> `storage_15_reg_1/ENARDEN`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.173ns  (logic 1.533ns (16.712%)  route 7.640ns (83.288%)); logic levels 10  (LUT2=2 LUT3=1 LUT4=3 LUT5=1 LUT6=3)

### head-ASLH

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.151 | 0.000 | +0.061 | 0.000 |
| Slow_85C | +0.151 | 0.000 | +0.061 | 0.000 |
| Fast_0C | +1.331 | 0.000 | +0.032 | 0.000 |
| Fast_85C | +1.331 | 0.000 | +0.032 | 0.000 |

LUT 51,520; FF 53,682; slices 15,837 of 15,850 (13 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.151 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_write_w_buffer_level0_reg[0]/C` -> `storage_10_dat1_reg[20]/D`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.536ns  (logic 1.755ns (18.404%)  route 7.781ns (81.596%)); logic levels 12  (LUT2=4 LUT3=1 LUT4=1 LUT5=1 LUT6=4 RAMD32=1)

### head-ETO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.120 | 0.000 | +0.101 | 0.000 |
| Slow_85C | +0.120 | 0.000 | +0.101 | 0.000 |
| Fast_0C | +1.331 | 0.000 | +0.036 | 0.000 |
| Fast_85C | +1.331 | 0.000 | +0.036 | 0.000 |

LUT 51,524; FF 53,680; slices 15,837 of 15,850 (13 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.120 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `FSM_sequential_subfragments_fsm2_state_reg[0]/C` -> `milansoc_tmod1_reg[11]/CE`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.592ns  (logic 2.238ns (23.332%)  route 7.354ns (76.668%)); logic levels 16  (LUT2=4 LUT3=3 LUT4=3 LUT5=2 LUT6=4)

