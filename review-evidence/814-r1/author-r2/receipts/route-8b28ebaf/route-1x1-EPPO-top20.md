# route-1x1-EPPO: 5000 sys endpoints, worst slack +0.324 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.324 | 19 | 9.615 | 74 % | `downW_header_reg[2]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.329 | 19 | 9.616 | 74 % | `downW_header_reg[2]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 3 | +0.332 | 19 | 9.612 | 74 % | `downW_header_reg[2]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.348 | 16 | 9.378 | 78 % | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[0]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 5 | +0.348 | 16 | 9.378 | 78 % | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[1]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 6 | +0.348 | 16 | 9.378 | 78 % | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[2]` | milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 7 | +0.415 | 19 | 9.525 | 74 % | `downW_header_reg[2]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 8 | +0.496 | 14 | 9.178 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[0]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 9 | +0.496 | 14 | 9.178 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[3]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 10 | +0.496 | 14 | 9.178 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[4]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 11 | +0.524 | 13 | 9.005 | 75 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `RAMC` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC |
| 12 | +0.555 | 16 | 9.238 | 77 % | `downW_header_reg[2]` | `dma_bus_w_s2mPipe_rData_data_reg[18]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.555 | 16 | 9.238 | 77 % | `downW_header_reg[2]` | `dma_bus_w_s2mPipe_rData_data_reg[19]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.555 | 16 | 9.238 | 77 % | `downW_header_reg[2]` | `dma_bus_w_s2mPipe_rData_data_reg[22]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.555 | 16 | 9.238 | 77 % | `downW_header_reg[2]` | `dma_bus_w_s2mPipe_rData_data_reg[23]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.566 | 18 | 9.376 | 75 % | `downW_header_reg[2]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 17 | +0.568 | 14 | 9.139 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_id_buffer_level_reg[0]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] |
| 18 | +0.568 | 14 | 9.139 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_id_buffer_level_reg[1]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] |
| 19 | +0.568 | 14 | 9.139 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_id_buffer_level_reg[2]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] |
| 20 | +0.568 | 14 | 9.139 | 74 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_id_buffer_level_reg[3]` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.324 | 0.000 | 394 | 19 | 74 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.348 | 0.024 | 3 | 16 | 78 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +0.496 | 0.172 | 9 | 14 | 74 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC | +0.524 | 0.200 | 32 | 13 | 75 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.568 | 0.244 | 9 | 14 | 74 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA | +0.575 | 0.251 | 29 | 13 | 75 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA_D1 | +0.579 | 0.255 | 31 | 13 | 75 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.582 | 0.258 | 5 | 12 | 77 % |
| milansoc_ws1_reg[*] -> milansoc_rpsn_reg | +0.607 | 0.283 | 1 | 15 | 78 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC_D1 | +0.700 | 0.376 | 29 | 13 | 74 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.714 | 0.390 | 1 | 15 | 65 % |
| FDPE -> FDPE_N | +0.746 | 0.422 | 1 | 0 | 67 % |
| FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_ar_cdc_cdc_graycounter0_q_binary_reg[*] | +0.752 | 0.428 | 3 | 9 | 82 % |
| FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_ar_cdc_cdc_graycounter0_q_reg[*] | +0.758 | 0.434 | 3 | 9 | 82 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMB | +0.774 | 0.450 | 31 | 13 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.782 | 0.458 | 8 | 13 | 66 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.789 | 0.465 | 16 | 15 | 78 % |
| FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_aw_cdc_cdc_graycounter0_q_reg[*] | +0.794 | 0.470 | 3 | 9 | 81 % |
| FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> RAMA | +0.804 | 0.480 | 12 | 8 | 82 % |
| FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> RAMA_D1 | +0.804 | 0.480 | 12 | 8 | 82 % |
F1 bridge -> SPI-flash PHY: worst +2.386 ns, 2.062 ns from the worst path, 71 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.162 ns, 0.838 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.324 ns, 0.000 ns from the worst path, 394 endpoints
