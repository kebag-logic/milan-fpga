# control-ASLH: 5000 sys endpoints, worst slack +0.342 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.342 | 15 | 9.225 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 2 | +0.342 | 15 | 9.225 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 3 | +0.364 | 13 | 8.970 | 71 % | `milansoc_milansoc_sdram_bankmachine1_row_reg[4]` | `milansoc_milansoc_sdram_bankmachine5_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 4 | +0.415 | 15 | 9.178 | 68 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 5 | +0.415 | 15 | 9.178 | 68 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 6 | +0.458 | 14 | 9.404 | 73 % | `milansoc_milansoc_sdram_bankmachine1_row_reg[4]` | `milansoc_milansoc_sdram_dfi_p0_wrdata_en_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_wrdata_en_reg |
| 7 | +0.528 | 15 | 9.250 | 75 % | `milansoc_ws1_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 8 | +0.528 | 15 | 9.250 | 75 % | `milansoc_ws1_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 9 | +0.528 | 15 | 9.250 | 75 % | `milansoc_ws1_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 10 | +0.550 | 13 | 8.855 | 71 % | `milansoc_milansoc_sdram_bankmachine1_row_reg[4]` | `milansoc_milansoc_sdram_bankmachine5_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 11 | +0.554 | 15 | 9.079 | 75 % | `milansoc_ws1_reg[5]` | `milansoc_rpsn_reg` | milansoc_ws1_reg[*] -> milansoc_rpsn_reg |
| 12 | +0.554 | 14 | 8.997 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_trccon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] |
| 13 | +0.554 | 14 | 8.997 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_trccon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg |
| 14 | +0.559 | 18 | 9.384 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.562 | 18 | 9.380 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.578 | 14 | 8.982 | 72 % | `milansoc_milansoc_sdram_bankmachine1_row_reg[4]` | `milansoc_milansoc_sdram_twtrcon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] |
| 17 | +0.578 | 14 | 8.982 | 72 % | `milansoc_milansoc_sdram_bankmachine1_row_reg[4]` | `milansoc_milansoc_sdram_twtrcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] |
| 18 | +0.588 | 18 | 9.394 | 76 % | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.591 | 14 | 8.889 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_trascon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |
| 20 | +0.591 | 14 | 8.889 | 66 % | `milansoc_milansoc_sdram_bankmachine7_row_reg[3]` | `milansoc_milansoc_sdram_bankmachine1_trascon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.342 | 0.000 | 40 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.342 | 0.000 | 8 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_wrdata_en_reg | +0.458 | 0.116 | 1 | 14 | 73 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.528 | 0.186 | 3 | 15 | 75 % |
| milansoc_ws1_reg[*] -> milansoc_rpsn_reg | +0.554 | 0.212 | 1 | 15 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.554 | 0.212 | 40 | 14 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.554 | 0.212 | 8 | 14 | 66 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.559 | 0.217 | 386 | 18 | 76 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] | +0.578 | 0.236 | 3 | 14 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.591 | 0.249 | 24 | 14 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_we_n_reg | +0.595 | 0.253 | 1 | 15 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.608 | 0.266 | 1 | 14 | 72 % |
| F1 bridge -> SPI-flash PHY | +0.614 | 0.272 | 154 | 18 | 64 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_new_master_wdata_ready0_reg | +0.624 | 0.282 | 1 | 14 | 69 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_level_reg[*] | +0.626 | 0.284 | 32 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.648 | 0.306 | 8 | 13 | 73 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.658 | 0.316 | 16 | 15 | 74 % |
| milansoc_ws1_reg[*] -> milansoc_psn_reg | +0.708 | 0.366 | 1 | 15 | 77 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.749 | 0.407 | 32 | 14 | 66 % |
| milansoc_milansoc_write_w_buffer_level0_reg[*] -> RAMC_D1 | +0.778 | 0.436 | 19 | 12 | 79 % |
F1 bridge -> SPI-flash PHY: worst +0.614 ns, 0.272 ns from the worst path, 154 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +0.921 ns, 0.579 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.559 ns, 0.217 ns from the worst path, 386 endpoints
