# route-1x1-EPPO: 5000 sys endpoints, worst slack +0.322 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.322 | 18 | 9.559 | 74 % | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.505 | 18 | 9.433 | 74 % | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 3 | +0.510 | 18 | 9.428 | 74 % | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.512 | 18 | 9.427 | 74 % | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.516 | 14 | 9.257 | 78 % | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 6 | +0.516 | 14 | 9.257 | 78 % | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 7 | +0.516 | 14 | 9.257 | 78 % | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 8 | +0.696 | 15 | 9.076 | 70 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[8]` | `subfragments_bankmachine6_state_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 9 | +0.719 | 14 | 8.942 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[9]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 10 | +0.721 | 13 | 9.009 | 79 % | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[42]` | milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 11 | +0.721 | 13 | 9.009 | 79 % | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[43]` | milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 12 | +0.721 | 13 | 9.009 | 79 % | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[62]` | milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 13 | +0.721 | 13 | 9.009 | 79 % | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[63]` | milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 14 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[0]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 15 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[10]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 16 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[11]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 17 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[1]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 18 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[2]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 19 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[3]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 20 | +0.722 | 14 | 8.939 | 77 % | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[8]` | milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.322 | 0.000 | 421 | 18 | 74 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.516 | 0.194 | 3 | 14 | 78 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.696 | 0.374 | 20 | 15 | 70 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.719 | 0.397 | 16 | 14 | 77 % |
| milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] | +0.721 | 0.399 | 64 | 13 | 79 % |
| milansoc_ws1_reg[*] -> milansoc_psn_reg | +0.733 | 0.411 | 1 | 14 | 76 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.735 | 0.413 | 7 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.814 | 0.492 | 30 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.814 | 0.492 | 6 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.818 | 0.496 | 21 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.837 | 0.515 | 12 | 14 | 71 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.935 | 0.613 | 35 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.935 | 0.613 | 7 | 14 | 70 % |
| FDPE_N -> FDPE_N | +1.001 | 0.679 | 1 | 0 | 58 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +1.068 | 0.746 | 5 | 13 | 71 % |
| milansoc_milansoc_write_w_buffer_level0_reg[*] -> RAMB_D1 | +1.124 | 0.802 | 53 | 11 | 77 % |
| milansoc_milansoc_write_w_buffer_level0_reg[*] -> RAMC_D1 | +1.128 | 0.806 | 45 | 11 | 77 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +1.139 | 0.817 | 3 | 13 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +1.149 | 0.827 | 1 | 13 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +1.149 | 0.827 | 1 | 13 | 70 % |
F1 bridge -> SPI-flash PHY: worst +2.721 ns, 2.399 ns from the worst path, 80 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.607 ns, 1.285 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.322 ns, 0.000 ns from the worst path, 421 endpoints
