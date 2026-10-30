# route-1x1-ASLH: 5000 sys endpoints, worst slack +0.230 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.230 | 14 | 9.438 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[26]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 2 | +0.248 | 14 | 9.381 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[16]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 3 | +0.279 | 14 | 9.333 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[14]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 4 | +0.293 | 14 | 9.391 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[4]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 5 | +0.296 | 14 | 9.333 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[12]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 6 | +0.296 | 14 | 9.390 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[8]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 7 | +0.309 | 14 | 9.342 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[20]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 8 | +0.310 | 14 | 9.413 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[46]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 9 | +0.317 | 14 | 9.403 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[16]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 10 | +0.321 | 14 | 9.355 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[12]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 11 | +0.328 | 14 | 9.353 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[22]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 12 | +0.335 | 14 | 9.385 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[28]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 13 | +0.336 | 14 | 9.470 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[17]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 14 | +0.342 | 14 | 9.341 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[24]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 15 | +0.342 | 14 | 9.341 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_13_dat1_reg[24]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 16 | +0.343 | 14 | 9.335 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[28]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 17 | +0.348 | 14 | 9.501 | 79 % | `milansoc_read_beat_count_reg[4]` | `storage_10_dat1_reg[49]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 18 | +0.353 | 16 | 9.198 | 76 % | `downW_header_reg[2]_replica` | `onW_buffer_0_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.353 | 16 | 9.198 | 76 % | `downW_header_reg[2]_replica` | `onW_buffer_1_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 20 | +0.353 | 16 | 9.198 | 76 % | `downW_header_reg[2]_replica` | `onW_buffer_2_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F2 SDRAM arbitration -> crossing FIFO read register | +0.230 | 0.000 | 84 | 14 | 79 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.353 | 0.123 | 364 | 16 | 76 % |
| F3 ZQCS timer -> bank machines | +0.432 | 0.202 | 453 | 15 | 78 % |
| milansoc_read_beat_count_reg[*] -> storage_N_reg_N | +0.524 | 0.294 | 5 | 12 | 80 % |
| milansoc_read_beat_count_reg[*] -> RAMA | +0.663 | 0.433 | 37 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMA_D1 | +0.663 | 0.433 | 44 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMB | +0.663 | 0.433 | 40 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMB_D1 | +0.663 | 0.433 | 36 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMC | +0.663 | 0.433 | 44 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMC_D1 | +0.663 | 0.433 | 32 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMD | +0.663 | 0.433 | 29 | 13 | 77 % |
| milansoc_read_beat_count_reg[*] -> RAMD_D1 | +0.663 | 0.433 | 29 | 13 | 77 % |
F1 bridge -> SPI-flash PHY: worst +0.816 ns, 0.586 ns from the worst path, 145 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +0.230 ns, 0.000 ns from the worst path, 84 endpoints
F3 ZQCS timer -> bank machines: worst +0.432 ns, 0.202 ns from the worst path, 453 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.353 ns, 0.123 ns from the worst path, 364 endpoints
