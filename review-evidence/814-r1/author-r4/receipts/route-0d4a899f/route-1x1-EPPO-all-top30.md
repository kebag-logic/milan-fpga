# route-1x1-EPPO: 5000 endpoints over every path group, worst slack +0.322 ns
| # | Slack ns | Levels | Data ns | Routing | Clocks | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | +0.322 | 18 | 9.559 | 74 % | sys -> sys | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.505 | 18 | 9.433 | 74 % | sys -> sys | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 3 | +0.510 | 18 | 9.428 | 74 % | sys -> sys | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.512 | 18 | 9.427 | 74 % | sys -> sys | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.516 | 14 | 9.257 | 78 % | sys -> sys | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 6 | +0.516 | 14 | 9.257 | 78 % | sys -> sys | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 7 | +0.516 | 14 | 9.257 | 78 % | sys -> sys | `milansoc_ws1_reg[0]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 8 | +0.696 | 15 | 9.076 | 70 % | sys -> sys | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[8]` | `subfragments_bankmachine6_state_reg[1]` | [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 9 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[0]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 10 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[1]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 11 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[2]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 12 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[3]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 13 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[4]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 14 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[5]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 15 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[6]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 16 | +0.711 | 9 | 6.876 | 73 % | eth_clocks0_rx -> eth_clocks0_rx | `idx_r_reg[1]` | `delta_r_reg[7]` | [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] |
| 17 | +0.719 | 14 | 8.942 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[9]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 18 | +0.721 | 13 | 9.009 | 79 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[42]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 19 | +0.721 | 13 | 9.009 | 79 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[43]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 20 | +0.721 | 13 | 9.009 | 79 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[62]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 21 | +0.721 | 13 | 9.009 | 79 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_rdat1_reg[63]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] |
| 22 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[0]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 23 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[10]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 24 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[11]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 25 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[1]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 26 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[2]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 27 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[3]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 28 | +0.722 | 14 | 8.939 | 77 % | sys -> sys | `milansoc_ws1_reg[0]` | `milansoc_tmod1_reg[8]` | [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] |
| 29 | +0.725 | 15 | 9.020 | 70 % | sys -> sys | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[8]` | `subfragments_bankmachine2_state_reg[0]` | [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 30 | +0.725 | 15 | 9.020 | 70 % | sys -> sys | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[8]` | `subfragments_bankmachine2_state_reg[1]` | [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.322 | 0.000 | 369 | 18 | 74 % |
| [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.516 | 0.194 | 3 | 14 | 78 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.696 | 0.374 | 20 | 15 | 70 % |
| [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] | +0.711 | 0.389 | 8 | 9 | 73 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.719 | 0.397 | 16 | 14 | 77 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] | +0.721 | 0.399 | 64 | 13 | 79 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_psn_reg | +0.733 | 0.411 | 1 | 14 | 76 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.735 | 0.413 | 7 | 14 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.814 | 0.492 | 30 | 14 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.814 | 0.492 | 6 | 14 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.818 | 0.496 | 21 | 14 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.837 | 0.515 | 12 | 14 | 71 % |
| [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] | +0.853 | 0.531 | 38 | 33 | 67 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.935 | 0.613 | 35 | 14 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.935 | 0.613 | 7 | 14 | 70 % |
| [sys -> sys] FDPE_N -> FDPE_N | +1.001 | 0.679 | 1 | 0 | 58 % |
| [milan -> milan] amap_stage_r_reg -> amr_k_r_reg[*] | +1.044 | 0.722 | 8 | 23 | 62 % |
| [milan -> milan] amap_stage_r_reg -> amr_st_r_reg[*] | +1.046 | 0.724 | 3 | 24 | 61 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +1.068 | 0.746 | 5 | 13 | 71 % |
| [eth_clocks0_rx -> eth_clocks0_rx] subfragments_txdatapath_liteethmacgap_state_reg -> storage_N_reg_N | +1.105 | 0.783 | 10 | 7 | 81 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level0_reg[*] -> RAMB_D1 | +1.124 | 0.802 | 8 | 11 | 77 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level0_reg[*] -> RAMC_D1 | +1.128 | 0.806 | 8 | 11 | 77 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +1.139 | 0.817 | 3 | 13 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +1.149 | 0.827 | 1 | 13 | 70 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +1.149 | 0.827 | 1 | 13 | 70 % |

Families within 0.3 ns of the worst path (+0.322 ns): F4 CPU DMA write bridge (inside the CPU netlist) +0.322; [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] +0.516
F1 bridge -> SPI-flash PHY: worst +2.721 ns, 2.399 ns from the worst path, 23 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.607 ns, 1.285 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.322 ns, 0.000 ns from the worst path, 369 endpoints
