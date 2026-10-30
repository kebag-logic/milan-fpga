# route-1x1-EPPO: 5000 sys endpoints, worst slack +0.303 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.303 | 14 | 9.415 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine7_level_reg[0]` | F3 ZQCS timer -> bank machines |
| 2 | +0.303 | 14 | 9.415 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine7_level_reg[1]` | F3 ZQCS timer -> bank machines |
| 3 | +0.303 | 14 | 9.415 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine7_level_reg[2]` | F3 ZQCS timer -> bank machines |
| 4 | +0.303 | 14 | 9.415 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine7_level_reg[3]` | F3 ZQCS timer -> bank machines |
| 5 | +0.429 | 16 | 9.352 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `subfragments_bankmachine0_state_reg[0]` | F3 ZQCS timer -> bank machines |
| 6 | +0.429 | 16 | 9.352 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `subfragments_bankmachine0_state_reg[1]` | F3 ZQCS timer -> bank machines |
| 7 | +0.429 | 16 | 9.352 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `subfragments_bankmachine0_state_reg[2]` | F3 ZQCS timer -> bank machines |
| 8 | +0.429 | 16 | 9.352 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `subfragments_bankmachine0_state_reg[3]` | F3 ZQCS timer -> bank machines |
| 9 | +0.503 | 15 | 9.232 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_level_reg[0]` | F3 ZQCS timer -> bank machines |
| 10 | +0.503 | 15 | 9.232 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_level_reg[1]` | F3 ZQCS timer -> bank machines |
| 11 | +0.503 | 15 | 9.232 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_level_reg[2]` | F3 ZQCS timer -> bank machines |
| 12 | +0.503 | 15 | 9.232 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_level_reg[3]` | F3 ZQCS timer -> bank machines |
| 13 | +0.513 | 14 | 8.965 | 77 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_twtrcon_ready_reg` | F3 ZQCS timer -> bank machines |
| 14 | +0.528 | 14 | 8.978 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine2_trascon_ready_reg` | F3 ZQCS timer -> bank machines |
| 15 | +0.528 | 14 | 8.978 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine2_trccon_ready_reg` | F3 ZQCS timer -> bank machines |
| 16 | +0.533 | 14 | 8.945 | 74 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_trascon_ready_reg` | F3 ZQCS timer -> bank machines |
| 17 | +0.533 | 14 | 8.945 | 74 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine6_trccon_count_reg[1]` | F3 ZQCS timer -> bank machines |
| 18 | +0.553 | 14 | 8.826 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine5_trccon_count_reg[1]` | F3 ZQCS timer -> bank machines |
| 19 | +0.553 | 14 | 8.826 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine5_trccon_ready_reg` | F3 ZQCS timer -> bank machines |
| 20 | +0.557 | 14 | 8.946 | 76 % | `milansoc_sdram_zqcs_timer_count1_reg[13]` | `milansoc_sdram_bankmachine7_trascon_count_reg[0]` | F3 ZQCS timer -> bank machines |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F3 ZQCS timer -> bank machines | +0.303 | 0.000 | 454 | 14 | 73 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.603 | 0.300 | 364 | 17 | 77 % |
| F1 bridge -> SPI-flash PHY | +0.627 | 0.324 | 141 | 15 | 69 % |
| milansoc_write_w_buffer_level0_reg[*] -> milansoc_write_id_buffer_level_reg[*] | +0.658 | 0.355 | 9 | 14 | 78 % |
| F2 SDRAM arbitration -> crossing FIFO read register | +0.689 | 0.386 | 84 | 14 | 79 % |
| milansoc_write_w_buffer_level0_reg[*] -> milansoc_write_resp_buffer_level_reg[*] | +0.796 | 0.493 | 9 | 14 | 77 % |
| milansoc_write_w_buffer_level0_reg[*] -> RAMC | +0.824 | 0.521 | 12 | 13 | 78 % |
| milansoc_write_w_buffer_level0_reg[*] -> RAMB_D1 | +0.845 | 0.542 | 16 | 13 | 78 % |
| milansoc_write_w_buffer_level0_reg[*] -> storage_N_reg_N | +0.850 | 0.547 | 5 | 12 | 81 % |
| milansoc_write_w_buffer_level0_reg[*] -> RAMA | +0.884 | 0.581 | 12 | 13 | 78 % |
| milansoc_write_w_buffer_level0_reg[*] -> RAMA_D1 | +0.884 | 0.581 | 13 | 13 | 78 % |
| milansoc_write_w_buffer_level0_reg[*] -> RAMB | +0.884 | 0.581 | 12 | 13 | 78 % |
F1 bridge -> SPI-flash PHY: worst +0.627 ns, 0.324 ns from the worst path, 141 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +0.689 ns, 0.386 ns from the worst path, 84 endpoints
F3 ZQCS timer -> bank machines: worst +0.303 ns, 0.000 ns from the worst path, 454 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.603 ns, 0.300 ns from the worst path, 364 endpoints
