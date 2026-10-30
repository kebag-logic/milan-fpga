### dev-EPPO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.303 | 0.000 | +0.051 | 0.000 |
| Slow_85C | +0.303 | 0.000 | +0.051 | 0.000 |
| Fast_0C | +1.633 | 0.000 | +0.028 | 0.000 |
| Fast_85C | +1.633 | 0.000 | +0.028 | 0.000 |

LUT 51,801; FF 53,760; slices 15,834 of 15,850 (16 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.303 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_sdram_zqcs_timer_count1_reg[13]/C` -> `milansoc_sdram_bankmachine7_level_reg[0]/CE`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.415ns  (logic 2.527ns (26.840%)  route 6.888ns (73.160%)); logic levels 14  (LUT2=2 LUT3=4 LUT4=2 LUT5=2 LUT6=4)

### dev-ASLH

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.230 | 0.000 | +0.053 | 0.000 |
| Slow_85C | +0.230 | 0.000 | +0.053 | 0.000 |
| Fast_0C | +1.562 | 0.000 | +0.014 | 0.000 |
| Fast_85C | +1.562 | 0.000 | +0.014 | 0.000 |

LUT 51,846; FF 53,759; slices 15,795 of 15,850 (55 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.230 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_read_beat_count_reg[4]/C` -> `storage_10_dat1_reg[26]/D`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.438ns  (logic 1.965ns (20.819%)  route 7.473ns (79.181%)); logic levels 14  (LUT2=5 LUT3=1 LUT4=3 LUT5=2 LUT6=2 RAMD32=1)

### dev-ETO

| Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow_0C | +0.106 | 0.000 | +0.109 | 0.000 |
| Slow_85C | +0.106 | 0.000 | +0.109 | 0.000 |
| Fast_0C | +1.562 | 0.000 | +0.054 | 0.000 |
| Fast_85C | +1.562 | 0.000 | +0.054 | 0.000 |

LUT 51,833; FF 53,758; slices 15,794 of 15,850 (56 free); Block RAM tiles 87.5 of 135

Worst setup path: slack +0.106 ns at Slow_0C, Slow_85C; group `milansoc_crg_clkout0`; `milansoc_sdram_bankmachine2_level_reg[1]/C` -> `storage_13_dat1_reg[8]/D`; requirement 10.000ns  (milansoc_crg_clkout0 rise@10.000ns - milansoc_crg_clkout0 rise@0.000ns); data path 9.593ns  (logic 2.006ns (20.911%)  route 7.587ns (79.089%)); logic levels 14  (LUT2=4 LUT3=6 LUT4=1 LUT5=2 RAMD32=1)

