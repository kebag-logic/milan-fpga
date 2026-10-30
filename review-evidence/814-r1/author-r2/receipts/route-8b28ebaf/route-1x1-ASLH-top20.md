# route-1x1-ASLH: 5000 sys endpoints, worst slack +0.039 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.039 | 19 | 9.864 | 75 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.216 | 15 | 9.202 | 66 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `milansoc_milansoc_sdram_twtrcon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] |
| 3 | +0.216 | 15 | 9.202 | 66 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `milansoc_milansoc_sdram_twtrcon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] |
| 4 | +0.231 | 15 | 9.435 | 67 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `subfragments_bankmachine1_state_reg[1]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 5 | +0.241 | 19 | 9.738 | 75 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.245 | 19 | 9.737 | 75 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 7 | +0.249 | 19 | 9.730 | 75 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 8 | +0.331 | 15 | 9.398 | 67 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `subfragments_bankmachine1_state_reg[0]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 9 | +0.331 | 15 | 9.398 | 67 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `subfragments_bankmachine1_state_reg[2]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 10 | +0.331 | 15 | 9.398 | 67 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `subfragments_bankmachine1_state_reg[3]` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 11 | +0.335 | 15 | 9.154 | 66 % | `milansoc_milansoc_sdram_bankmachine2_row_reg[3]` | `milansoc_milansoc_sdram_twtrcon_ready_reg` | milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg |
| 12 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[16]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[17]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[30]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[31]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[4]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 17 | +0.364 | 16 | 9.362 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[5]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 18 | +0.370 | 11 | 9.040 | 82 % | `milansoc_milansoc_write_w_buffer_level2_reg[1]` | `storage_15_reg_2` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N |
| 19 | +0.434 | 16 | 9.325 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 20 | +0.434 | 16 | 9.325 | 77 % | `frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` | `dma_bus_w_s2mPipe_rData_data_reg[1]` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.039 | 0.000 | 401 | 19 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] | +0.216 | 0.177 | 3 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.231 | 0.192 | 31 | 15 | 67 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.335 | 0.296 | 1 | 15 | 66 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.370 | 0.331 | 5 | 11 | 82 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p1_we_n_reg | +0.474 | 0.435 | 1 | 15 | 67 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.552 | 0.513 | 36 | 13 | 67 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.552 | 0.513 | 8 | 13 | 67 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_wrdata_en_reg | +0.580 | 0.541 | 1 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p2_we_n_reg | +0.643 | 0.604 | 1 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p0_we_n_reg | +0.680 | 0.641 | 1 | 16 | 65 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.680 | 0.641 | 9 | 13 | 80 % |
| milansoc_ws1_reg[*] -> milansoc_rto0_reg[*] | +0.713 | 0.674 | 13 | 15 | 78 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.747 | 0.708 | 3 | 16 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.781 | 0.742 | 36 | 13 | 67 % |
| milansoc_ws1_reg[*] -> milansoc_psn_reg | +0.789 | 0.750 | 1 | 15 | 76 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_dfi_p1_wrdata_en_reg | +0.801 | 0.762 | 1 | 15 | 66 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.812 | 0.773 | 21 | 13 | 67 % |
| milansoc_milansoc_sdram_bankmachineN_row_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.817 | 0.778 | 7 | 13 | 66 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.824 | 0.785 | 3 | 16 | 77 % |
F1 bridge -> SPI-flash PHY: worst +2.110 ns, 2.071 ns from the worst path, 171 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.460 ns, 1.421 ns from the worst path, 115 endpoints
F3 ZQCS timer -> bank machines: worst +4.379 ns, 4.340 ns from the worst path, 1 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.039 ns, 0.000 ns from the worst path, 401 endpoints
