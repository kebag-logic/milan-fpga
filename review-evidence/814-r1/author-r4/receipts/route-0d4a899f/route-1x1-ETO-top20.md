# route-1x1-ETO: 5000 sys endpoints, worst slack +0.406 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.406 | 0 | 8.858 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[10]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 2 | +0.406 | 0 | 8.858 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[11]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 3 | +0.406 | 0 | 8.858 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[8]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 4 | +0.406 | 0 | 8.858 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[9]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 5 | +0.409 | 0 | 8.857 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[16]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 6 | +0.409 | 0 | 8.857 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[17]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 7 | +0.409 | 0 | 8.857 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[18]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 8 | +0.409 | 0 | 8.857 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[19]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 9 | +0.417 | 0 | 8.824 | 96 % | `FDPE_17` | `src_level_reg` | FDPE_N -> src_level_reg |
| 10 | +0.417 | 0 | 8.824 | 96 % | `FDPE_17` | `src_level_reg` | FDPE_N -> src_level_reg |
| 11 | +0.453 | 18 | 9.547 | 76 % | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 12 | +0.492 | 18 | 9.452 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.504 | 18 | 9.494 | 76 % | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.516 | 0 | 8.749 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[12]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 15 | +0.516 | 0 | 8.749 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[13]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 16 | +0.516 | 0 | 8.749 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[14]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 17 | +0.516 | 0 | 8.749 | 96 % | `FDPE_17` | `milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[15]` | FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] |
| 18 | +0.517 | 14 | 8.982 | 71 % | `milansoc_milansoc_sdram_bankmachine3_pipe_valid_source_payload_addr_reg[9]` | `milansoc_milansoc_sdram_bankmachine2_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 19 | +0.517 | 14 | 8.982 | 71 % | `milansoc_milansoc_sdram_bankmachine3_pipe_valid_source_payload_addr_reg[9]` | `milansoc_milansoc_sdram_bankmachine2_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 20 | +0.524 | 15 | 9.040 | 78 % | `downW_header_reg[0]` | `onW_buffer_0_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] | +0.406 | 0.000 | 32 | 0 | 96 % |
| FDPE_N -> src_level_reg | +0.417 | 0.011 | 2 | 0 | 96 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.453 | 0.047 | 390 | 18 | 76 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.517 | 0.111 | 40 | 14 | 71 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.517 | 0.111 | 8 | 14 | 71 % |
| FDPE_N -> align_cnt_r_reg[*] | +0.542 | 0.136 | 32 | 0 | 96 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.572 | 0.166 | 24 | 14 | 71 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.612 | 0.206 | 8 | 14 | 71 % |
| milansoc_milansoc_sdram_bankmachineN_level_reg[*] -> storage_N_reg_N | +0.677 | 0.271 | 5 | 9 | 82 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.680 | 0.274 | 40 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.680 | 0.274 | 8 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_level_reg[*] -> milansoc_milansoc_write_w_buffer_consume_reg[*] | +0.685 | 0.279 | 4 | 9 | 82 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.757 | 0.351 | 32 | 15 | 70 % |
| milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] | +0.820 | 0.414 | 64 | 13 | 80 % |
| milansoc_ws0_reg[*] -> milansoc_psn_reg | +0.831 | 0.425 | 1 | 14 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_tmod1_reg[*] | +0.949 | 0.543 | 16 | 14 | 78 % |
| milansoc_ws0_reg[*] -> milansoc_rdat0_reg[*] | +1.002 | 0.596 | 64 | 13 | 79 % |
| milansoc_milansoc_sdram_bankmachineN_level_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +1.048 | 0.642 | 9 | 11 | 79 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_consume_reg[*] | +1.081 | 0.675 | 24 | 13 | 70 % |
| milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +1.122 | 0.716 | 3 | 14 | 78 % |
F1 bridge -> SPI-flash PHY: worst +1.723 ns, 1.317 ns from the worst path, 104 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.472 ns, 1.066 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.453 ns, 0.047 ns from the worst path, 390 endpoints
