# route-1x1-ASLH: 5000 sys endpoints, worst slack +0.126 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.126 | 18 | 9.796 | 77 % | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.328 | 18 | 9.672 | 77 % | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 3 | +0.331 | 18 | 9.668 | 77 % | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.334 | 18 | 9.609 | 76 % | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.472 | 15 | 9.091 | 79 % | `downW_header_reg[0]` | `onW_buffer_0_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.472 | 15 | 9.091 | 79 % | `downW_header_reg[0]` | `onW_buffer_1_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 7 | +0.472 | 15 | 9.091 | 79 % | `downW_header_reg[0]` | `onW_buffer_2_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 8 | +0.472 | 15 | 9.091 | 79 % | `downW_header_reg[0]` | `onW_buffer_3_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 9 | +0.526 | 15 | 9.280 | 72 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine6_state_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 10 | +0.536 | 11 | 8.867 | 83 % | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `storage_15_reg_4` | milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N |
| 11 | +0.589 | 15 | 9.185 | 70 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine7_state_reg[0]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 12 | +0.589 | 15 | 9.185 | 70 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine7_state_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 13 | +0.589 | 15 | 9.185 | 70 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine7_state_reg[2]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 14 | +0.589 | 15 | 9.185 | 70 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine7_state_reg[3]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 15 | +0.589 | 14 | 8.949 | 73 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `milansoc_milansoc_sdram_bankmachine1_trascon_count_reg[0]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |
| 16 | +0.589 | 14 | 8.949 | 73 % | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `milansoc_milansoc_sdram_bankmachine1_trascon_count_reg[1]` | milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] |
| 17 | +0.592 | 15 | 9.155 | 79 % | `downW_header_reg[0]` | `onW_buffer_0_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 18 | +0.592 | 15 | 9.155 | 79 % | `downW_header_reg[0]` | `onW_buffer_1_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.592 | 15 | 9.155 | 79 % | `downW_header_reg[0]` | `onW_buffer_2_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 20 | +0.592 | 15 | 9.155 | 79 % | `downW_header_reg[0]` | `onW_buffer_3_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.126 | 0.000 | 389 | 18 | 77 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.526 | 0.400 | 32 | 15 | 72 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.536 | 0.410 | 5 | 11 | 83 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.589 | 0.463 | 24 | 14 | 73 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.628 | 0.502 | 8 | 14 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.657 | 0.531 | 40 | 14 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.657 | 0.531 | 8 | 14 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.741 | 0.615 | 40 | 14 | 72 % |
| milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.741 | 0.615 | 8 | 14 | 72 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.808 | 0.682 | 16 | 14 | 77 % |
| FDPE_N -> align_cnt_r_reg[*] | +0.886 | 0.760 | 32 | 0 | 96 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_w_buffer_consume_reg[*] | +0.983 | 0.857 | 4 | 11 | 82 % |
| FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] | +1.032 | 0.906 | 32 | 0 | 96 % |
| FDPE_N -> align_evt_r_reg | +1.051 | 0.925 | 1 | 0 | 96 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC_D1 | +1.058 | 0.932 | 32 | 12 | 81 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMB_D1 | +1.063 | 0.937 | 43 | 12 | 81 % |
| milansoc_ws1_reg[*] -> milansoc_converter2_dat_r_reg[*] | +1.075 | 0.949 | 64 | 12 | 80 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +1.086 | 0.960 | 9 | 13 | 80 % |
| milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +1.094 | 0.968 | 9 | 13 | 80 % |
| milansoc_ws1_reg[*] -> dma_bus_w_s2mPipe_rData_data_reg[*] | +1.155 | 1.029 | 29 | 11 | 80 % |
F1 bridge -> SPI-flash PHY: worst +2.085 ns, 1.959 ns from the worst path, 101 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.392 ns, 1.266 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.126 ns, 0.000 ns from the worst path, 389 endpoints
