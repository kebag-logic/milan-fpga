# control-ETO: 5000 sys endpoints, worst slack +0.300 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.300 | 18 | 9.646 | 65 % | `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[1]` | `milansoc_milansoc_phy_cnt_reg[8]` | F1 bridge -> SPI-flash PHY |
| 2 | +0.384 | 15 | 9.210 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 3 | +0.384 | 15 | 9.210 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 4 | +0.385 | 19 | 9.601 | 75 % | `downW_header_reg[3]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.400 | 19 | 9.542 | 75 % | `downW_header_reg[3]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.454 | 15 | 9.324 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 7 | +0.454 | 15 | 9.324 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine3_twtpcon_count_reg[2]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 8 | +0.456 | 14 | 9.113 | 70 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine2_trascon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |
| 9 | +0.456 | 14 | 9.113 | 70 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine2_trascon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |
| 10 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[21]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 11 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[28]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 12 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[29]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[2]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[30]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.459 | 16 | 9.277 | 78 % | `downW_header_reg[3]` | `frontend_split_bufferize_AW_addr_reg[3]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.491 | 19 | 9.452 | 75 % | `downW_header_reg[3]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 17 | +0.500 | 15 | 9.049 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine1_twtpcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] |
| 18 | +0.500 | 15 | 9.049 | 69 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine1_twtpcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg |
| 19 | +0.508 | 14 | 8.991 | 70 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine2_trascon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg |
| 20 | +0.508 | 14 | 8.991 | 70 % | `milansoc_milansoc_sdram_bankmachine7_pipe_valid_source_payload_addr_reg[10]` | `milansoc_milansoc_sdram_bankmachine2_trccon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F1 bridge -> SPI-flash PHY | +0.300 | 0.000 | 155 | 18 | 65 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.384 | 0.084 | 20 | 15 | 69 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.384 | 0.084 | 4 | 15 | 69 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.385 | 0.085 | 396 | 19 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.456 | 0.156 | 24 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.508 | 0.208 | 8 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.508 | 0.208 | 40 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.508 | 0.208 | 8 | 14 | 70 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.530 | 0.230 | 32 | 15 | 69 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.885 | 0.585 | 16 | 15 | 76 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.928 | 0.628 | 3 | 15 | 76 % |
| milansoc_milansoc_write_beat_count_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.953 | 0.653 | 9 | 13 | 75 % |
| milansoc_milansoc_write_beat_count_reg[*] -> RAMC_D1 | +0.954 | 0.654 | 23 | 12 | 75 % |
| milansoc_milansoc_write_beat_count_reg[*] -> storage_N_reg_N | +0.963 | 0.663 | 5 | 11 | 78 % |
| milansoc_ws1_reg[*] -> milansoc_rpsn_reg | +1.002 | 0.702 | 1 | 15 | 75 % |
| FDPE -> FDPE_N | +1.034 | 0.734 | 1 | 0 | 52 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_wrdata_en_reg | +1.041 | 0.741 | 1 | 13 | 71 % |
| milansoc_milansoc_write_beat_count_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +1.054 | 0.754 | 9 | 13 | 74 % |
| interface1_adr_reg[*] -> OSERDESE2_N | +1.062 | 0.762 | 32 | 6 | 84 % |
| milansoc_milansoc_write_beat_count_reg[*] -> RAMB_D1 | +1.094 | 0.794 | 21 | 12 | 75 % |
F1 bridge -> SPI-flash PHY: worst +0.300 ns, 0.000 ns from the worst path, 155 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.117 ns, 0.817 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: worst +4.103 ns, 3.803 ns from the worst path, 1 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.385 ns, 0.085 ns from the worst path, 396 endpoints
