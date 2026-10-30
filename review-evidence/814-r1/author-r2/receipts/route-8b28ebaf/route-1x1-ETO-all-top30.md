# route-1x1-ETO: 5000 endpoints over every path group, worst slack +0.010 ns
| # | Slack ns | Levels | Data ns | Routing | Clocks | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | +0.010 | 17 | 9.667 | 75 % | sys -> sys | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[0]` | [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 2 | +0.010 | 17 | 9.667 | 75 % | sys -> sys | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[1]` | [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 3 | +0.010 | 17 | 9.667 | 75 % | sys -> sys | `milansoc_ws0_reg[5]` | `FSM_sequential_subfragments_fsm2_state_reg[2]` | [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] |
| 4 | +0.059 | 18 | 9.927 | 77 % | sys -> sys | `downW_header_reg[0]_replica` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.066 | 18 | 9.922 | 77 % | sys -> sys | `downW_header_reg[0]_replica` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.068 | 18 | 9.922 | 77 % | sys -> sys | `downW_header_reg[0]_replica` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 7 | +0.084 | 16 | 9.653 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[12]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 8 | +0.084 | 16 | 9.653 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[13]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 9 | +0.084 | 16 | 9.653 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[14]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 10 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[10]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 11 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[11]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 12 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[15]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 13 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[20]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 14 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[21]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 15 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[25]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 16 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[26]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 17 | +0.107 | 16 | 9.627 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[28]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 18 | +0.114 | 16 | 9.652 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[31]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.114 | 16 | 9.652 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[3]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 20 | +0.114 | 16 | 9.652 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[5]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 21 | +0.114 | 16 | 9.652 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[6]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 22 | +0.114 | 16 | 9.652 | 79 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[9]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 23 | +0.152 | 17 | 9.780 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_valid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 24 | +0.169 | 17 | 9.743 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 25 | +0.223 | 16 | 9.552 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[7]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 26 | +0.223 | 16 | 9.552 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[8]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 27 | +0.231 | 16 | 9.547 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[16]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 28 | +0.231 | 16 | 9.547 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[23]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 29 | +0.231 | 16 | 9.547 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[27]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 30 | +0.231 | 16 | 9.547 | 78 % | sys -> sys | `downW_header_reg[0]_replica` | `frontend_split_bufferize_AW_addr_reg[4]` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.010 | 0.000 | 3 | 17 | 75 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.059 | 0.049 | 377 | 18 | 77 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_psn_reg | +0.237 | 0.227 | 1 | 16 | 75 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_rdat1_reg[*] | +0.319 | 0.309 | 64 | 15 | 77 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_rto1_reg[*] | +0.391 | 0.381 | 13 | 16 | 76 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_converter1_dat_r_reg[*] | +0.466 | 0.456 | 64 | 14 | 78 % |
| [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] | +0.571 | 0.561 | 38 | 35 | 65 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.584 | 0.574 | 5 | 12 | 81 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_converter2_err_reg | +0.623 | 0.613 | 2 | 15 | 75 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.637 | 0.627 | 1 | 15 | 66 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.642 | 0.632 | 9 | 14 | 80 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_converter2_count_reg | +0.652 | 0.642 | 2 | 15 | 75 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_rto0_reg[*] | +0.686 | 0.676 | 13 | 16 | 77 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_converter2_dat_r_reg[*] | +0.691 | 0.681 | 64 | 14 | 78 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_count_reg[*] | +0.696 | 0.686 | 3 | 15 | 66 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC | +0.750 | 0.740 | 5 | 13 | 80 % |
| [milan -> milan] ss_r_reg[*] -> tmo_r_reg[*] | +0.788 | 0.778 | 13 | 23 | 79 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_werr1_reg | +0.793 | 0.783 | 1 | 16 | 75 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_tmod1_reg[*] | +0.796 | 0.786 | 16 | 16 | 76 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA_D1 | +0.799 | 0.789 | 5 | 13 | 80 % |
| [sys -> sys] milansoc_ws0_reg[*] -> milansoc_rpsn_reg | +0.801 | 0.791 | 1 | 16 | 76 % |
| [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.814 | 0.804 | 3 | 17 | 75 % |
| [milan -> milan] ss_r_reg[*] -> sel_r_reg[*] | +0.829 | 0.819 | 4 | 26 | 77 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_dfi_p0_we_n_reg | +0.833 | 0.823 | 1 | 16 | 66 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.837 | 0.827 | 24 | 15 | 66 % |

Families within 0.3 ns of the worst path (+0.010 ns): [sys -> sys] milansoc_ws0_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] +0.010; F4 CPU DMA write bridge (inside the CPU netlist) +0.059; [sys -> sys] milansoc_ws0_reg[*] -> milansoc_psn_reg +0.237
F1 bridge -> SPI-flash PHY: worst +2.228 ns, 2.218 ns from the worst path, 79 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.380 ns, 1.370 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.059 ns, 0.049 ns from the worst path, 377 endpoints
