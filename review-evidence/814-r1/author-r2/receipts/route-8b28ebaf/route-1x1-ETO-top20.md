# route-1x1-ETO: 5000 sys endpoints, worst slack +0.010 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.010 | 17 | 9.667 | 75 % | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 2 | +0.010 | 17 | 9.667 | 75 % | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 3 | +0.010 | 17 | 9.667 | 75 % | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 4 | +0.059 | 18 | 9.927 | 77 % | `downW_header_reg[0]_replica` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.066 | 18 | 9.922 | 77 % | `downW_header_reg[0]_replica` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.068 | 18 | 9.922 | 77 % | `downW_header_reg[0]_replica` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 7 | +0.084 | 16 | 9.653 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[12]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 8 | +0.084 | 16 | 9.653 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[13]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 9 | +0.084 | 16 | 9.653 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[14]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 10 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[10]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 11 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[11]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 12 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[15]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[20]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[21]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[25]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[26]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 17 | +0.107 | 16 | 9.627 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[28]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 18 | +0.114 | 16 | 9.652 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[31]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.114 | 16 | 9.652 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[3]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 20 | +0.114 | 16 | 9.652 | 79 % | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[5]` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.010 | 0.000 | 3 | 17 | 75 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.059 | 0.049 | 414 | 18 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_psn_reg | +0.237 | 0.227 | 1 | 16 | 75 % |
| milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] | +0.319 | 0.309 | 64 | 15 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_rto1_reg[*] | +0.391 | 0.381 | 13 | 16 | 76 % |
| milansoc_ws0_reg[*] -> milansoc_converter1_dat_r_reg[*] | +0.466 | 0.456 | 64 | 14 | 78 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.584 | 0.574 | 5 | 12 | 81 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_err_reg | +0.623 | 0.613 | 2 | 15 | 75 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.637 | 0.627 | 1 | 15 | 66 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.642 | 0.632 | 9 | 14 | 80 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_count_reg | +0.652 | 0.642 | 2 | 15 | 75 % |
| milansoc_ws0_reg[*] -> milansoc_rto0_reg[*] | +0.686 | 0.676 | 13 | 16 | 77 % |
| milansoc_ws0_reg[*] -> milansoc_converter2_dat_r_reg[*] | +0.691 | 0.681 | 64 | 14 | 78 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] | +0.696 | 0.686 | 3 | 15 | 66 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC | +0.750 | 0.740 | 41 | 13 | 80 % |
| milansoc_ws0_reg[*] -> milansoc_werr1_reg | +0.793 | 0.783 | 1 | 16 | 75 % |
| milansoc_ws0_reg[*] -> milansoc_tmod1_reg[*] | +0.796 | 0.786 | 16 | 16 | 76 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA_D1 | +0.799 | 0.789 | 37 | 13 | 80 % |
| milansoc_ws0_reg[*] -> milansoc_rpsn_reg | +0.801 | 0.791 | 1 | 16 | 76 % |
| milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.814 | 0.804 | 3 | 17 | 75 % |
F1 bridge -> SPI-flash PHY: worst +2.228 ns, 2.218 ns from the worst path, 168 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.380 ns, 1.370 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.059 ns, 0.049 ns from the worst path, 414 endpoints
