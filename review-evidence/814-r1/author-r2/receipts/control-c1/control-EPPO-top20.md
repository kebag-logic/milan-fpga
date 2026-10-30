# control-EPPO: 5000 sys endpoints, worst slack +0.264 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.264 | 18 | 9.560 | 76 % | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.514 | 15 | 9.283 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[36]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 3 | +0.514 | 15 | 9.283 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[38]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 4 | +0.514 | 15 | 9.283 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[42]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 5 | +0.522 | 16 | 9.282 | 77 % | `milansoc_ws0_reg[4]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 6 | +0.522 | 16 | 9.282 | 77 % | `milansoc_ws0_reg[4]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 7 | +0.522 | 16 | 9.282 | 77 % | `milansoc_ws0_reg[4]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 8 | +0.528 | 18 | 9.337 | 76 % | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 9 | +0.531 | 18 | 9.333 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 10 | +0.553 | 18 | 9.311 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 11 | +0.556 | 15 | 9.245 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[46]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 12 | +0.556 | 15 | 9.245 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[48]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 13 | +0.556 | 15 | 9.245 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[54]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 14 | +0.556 | 15 | 9.245 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[58]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 15 | +0.556 | 15 | 9.245 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[59]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 16 | +0.570 | 14 | 9.051 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_converter2_dat_r_reg[62]` | milansoc_ws0_reg[*] -> milansoc_converter2_dat_r_reg[*] |
| 17 | +0.583 | 15 | 9.223 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[37]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 18 | +0.583 | 15 | 9.223 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[41]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 19 | +0.583 | 15 | 9.223 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[47]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |
| 20 | +0.583 | 15 | 9.223 | 78 % | `milansoc_ws0_reg[4]` | `milansoc_rdat1_reg[50]` | milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.264 | 0.000 | 402 | 18 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] | +0.514 | 0.250 | 64 | 15 | 78 % |
| milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.522 | 0.258 | 3 | 16 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_dat_r_reg[*] | +0.570 | 0.306 | 64 | 14 | 78 % |
| F1 bridge -> SPI-flash PHY | +0.677 | 0.413 | 154 | 19 | 64 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_count_reg | +0.730 | 0.466 | 2 | 15 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_err_reg | +0.730 | 0.466 | 1 | 15 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_rdat0_reg[*] | +0.734 | 0.470 | 64 | 15 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_rpsn_reg | +0.834 | 0.570 | 1 | 16 | 76 % |
| milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.871 | 0.607 | 3 | 16 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_converter1_count_reg | +0.879 | 0.615 | 2 | 15 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_converter1_err_reg | +0.879 | 0.615 | 2 | 15 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_werr1_reg | +0.900 | 0.636 | 1 | 16 | 74 % |
| milansoc_ws0_reg[*] -> milansoc_psn_reg | +0.904 | 0.640 | 1 | 16 | 74 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.910 | 0.646 | 32 | 14 | 67 % |
| milansoc_ws0_reg[*] -> milansoc_tmod1_reg[*] | +0.910 | 0.646 | 16 | 16 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_rto1_reg[*] | +0.925 | 0.661 | 13 | 16 | 76 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.971 | 0.707 | 40 | 14 | 68 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.971 | 0.707 | 8 | 14 | 68 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_level_reg[*] | +1.028 | 0.764 | 32 | 13 | 71 % |
F1 bridge -> SPI-flash PHY: worst +0.677 ns, 0.413 ns from the worst path, 154 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.367 ns, 1.103 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.264 ns, 0.000 ns from the worst path, 402 endpoints
