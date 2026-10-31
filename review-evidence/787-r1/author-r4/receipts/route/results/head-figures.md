### ExtraPostPlacementOpt (shipping)

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.018 | 0.000 | +0.062 | 0.000 |
| Slow_85C | +0.018 | 0.000 | +0.062 | 0.000 |
| Fast_0C | +1.633 | 0.000 | +0.033 | 0.000 |
| Fast_85C | +1.633 | 0.000 | +0.033 | 0.000 |

LUT 52,291; FF 53,833; slices 15,837 of 15,850 (13 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.018 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_sdram_zqcs_timer_count1_reg[2]/C` -> `subfragments_bankmachine3_state_reg[0]/CE`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.654ns  (logic 2.493ns (25.823%)  route 7.161ns (74.177%)); logic levels 18  (LUT2=4 LUT3=1 LUT4=2 LUT5=3 LUT6=7 MUXF7=1)

### AltSpreadLogic_high

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.000 | 0.000 | +0.058 | 0.000 |
| Slow_85C | +0.000 | 0.000 | +0.058 | 0.000 |
| Fast_0C | +1.456 | 0.000 | +0.030 | 0.000 |
| Fast_85C | +1.456 | 0.000 | +0.030 | 0.000 |

LUT 52,370; FF 53,833; slices 15,824 of 15,850 (26 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.000 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_sdram_zqcs_timer_count1_reg[13]/C` -> `subfragments_bankmachine2_state_reg[0]/CE`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.771ns  (logic 2.059ns (21.073%)  route 7.712ns (78.927%)); logic levels 16  (LUT2=1 LUT3=2 LUT4=1 LUT5=4 LUT6=8)

### ExtraTimingOpt

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.017 | 0.000 | +0.051 | 0.000 |
| Slow_85C | +0.017 | 0.000 | +0.051 | 0.000 |
| Fast_0C | +1.513 | 0.000 | +0.013 | 0.000 |
| Fast_85C | +1.513 | 0.000 | +0.013 | 0.000 |

LUT 52,367; FF 53,833; slices 15,824 of 15,850 (26 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.017 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_sdram_zqcs_timer_count1_reg[10]/C` -> `milansoc_sdram_bankmachine0_level_reg[2]/CE`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.756ns  (logic 2.373ns (24.323%)  route 7.383ns (75.677%)); logic levels 17  (LUT2=3 LUT3=3 LUT4=3 LUT5=1 LUT6=6 MUXF7=1)

