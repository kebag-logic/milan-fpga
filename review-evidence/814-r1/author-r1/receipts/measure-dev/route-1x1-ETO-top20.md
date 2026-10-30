# route-1x1-ETO: 5000 sys endpoints, worst slack +0.106 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.106 | 14 | 9.593 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[8]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 2 | +0.164 | 14 | 9.680 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[35]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 3 | +0.183 | 14 | 9.515 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[0]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 4 | +0.198 | 14 | 9.646 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[47]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 5 | +0.202 | 14 | 9.515 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[6]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 6 | +0.223 | 14 | 9.493 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[16]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 7 | +0.265 | 14 | 9.422 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[14]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 8 | +0.275 | 14 | 9.440 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[34]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 9 | +0.278 | 14 | 9.394 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[26]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 10 | +0.279 | 14 | 9.403 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[2]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 11 | +0.283 | 14 | 9.452 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[46]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 12 | +0.295 | 14 | 9.605 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[17]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 13 | +0.306 | 14 | 9.597 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[7]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 14 | +0.307 | 14 | 9.390 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[32]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 15 | +0.311 | 14 | 9.571 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[45]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 16 | +0.313 | 14 | 9.566 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[13]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 17 | +0.315 | 14 | 9.542 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[3]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 18 | +0.332 | 14 | 9.340 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[20]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 19 | +0.332 | 14 | 9.276 | 78 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_10_dat1_reg[14]` | F2 SDRAM arbitration -> crossing FIFO read register |
| 20 | +0.334 | 14 | 9.408 | 79 % | `milansoc_sdram_bankmachine2_level_reg[1]` | `storage_13_dat1_reg[48]` | F2 SDRAM arbitration -> crossing FIFO read register |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F2 SDRAM arbitration -> crossing FIFO read register | +0.106 | 0.000 | 84 | 14 | 79 % |
| milansoc_ws0_reg[*] -> milansoc_tmod1_reg[*] | +0.427 | 0.321 | 16 | 12 | 79 % |
| milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_sdram_bankmachineN_level_reg[*] | +0.465 | 0.359 | 16 | 13 | 70 % |
| F3 ZQCS timer -> bank machines | +0.572 | 0.466 | 290 | 15 | 79 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMA | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMA_D1 | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMB | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMB_D1 | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMC | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMC_D1 | +0.615 | 0.509 | 12 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMD | +0.615 | 0.509 | 11 | 13 | 77 % |
| milansoc_sdram_bankmachineN_level_reg[*] -> RAMD_D1 | +0.615 | 0.509 | 11 | 13 | 77 % |
F1 bridge -> SPI-flash PHY: worst +0.784 ns, 0.678 ns from the worst path, 146 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +0.106 ns, 0.000 ns from the worst path, 84 endpoints
F3 ZQCS timer -> bank machines: worst +0.572 ns, 0.466 ns from the worst path, 290 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.686 ns, 0.580 ns from the worst path, 372 endpoints
