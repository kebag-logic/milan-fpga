# route-1x1-EPPO: 5000 endpoints over every path group, worst slack +0.128 ns
| # | Slack ns | Levels | Data ns | Routing | Clocks | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | +0.128 | 1 | 4.641 | 86 % | milan -> idelay/ps 200 MHz | `FDPE_3` | `psrst_sync_r_reg[0]` | [milan -> idelay/ps 200 MHz] FDPE_N -> psrst_sync_r_reg[*] |
| 2 | +0.246 | 36 | 19.752 | 64 % | milan -> milan | `uop_e_r_reg[imm][0]` | `taint_r_reg` | [milan -> milan] uop_e_r_reg[imm][*] -> taint_r_reg |
| 3 | +0.324 | 19 | 9.615 | 74 % | sys -> sys | `downW_header_reg[2]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.329 | 19 | 9.616 | 74 % | sys -> sys | `downW_header_reg[2]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.332 | 19 | 9.612 | 74 % | sys -> sys | `downW_header_reg[2]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.348 | 16 | 9.378 | 78 % | sys -> sys | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[0]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 7 | +0.348 | 16 | 9.378 | 78 % | sys -> sys | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[1]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 8 | +0.348 | 16 | 9.378 | 78 % | sys -> sys | `milansoc_ws1_reg[1]` | `FSM_sequential_subfragments_fsm1_state_reg[2]` | [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] |
| 9 | +0.390 | 6 | 7.183 | 83 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[11]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 10 | +0.390 | 6 | 7.183 | 83 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[13]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 11 | +0.390 | 6 | 7.183 | 83 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[30]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 12 | +0.390 | 6 | 7.183 | 83 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[31]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 13 | +0.390 | 6 | 7.183 | 83 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[9]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 14 | +0.393 | 35 | 19.159 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[29]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 15 | +0.393 | 35 | 19.159 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[30]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 16 | +0.393 | 35 | 19.159 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[31]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 17 | +0.411 | 23 | 19.383 | 75 % | milan -> milan | `uop_e_r_reg[fmt][1]` | `live_mux_q_reg[0]` | [milan -> milan] uop_e_r_reg[fmt][*] -> live_mux_q_reg[*] |
| 18 | +0.415 | 19 | 9.525 | 74 % | sys -> sys | `downW_header_reg[2]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 19 | +0.466 | 35 | 19.089 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[13]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 20 | +0.466 | 35 | 19.089 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[14]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 21 | +0.466 | 35 | 19.089 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[15]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 22 | +0.466 | 35 | 19.089 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[16]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 23 | +0.476 | 35 | 19.081 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[1]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 24 | +0.476 | 35 | 19.081 | 66 % | milan -> milan | `uop_e_r_reg[imm][0]` | `deb_cnt_r_reg[3]` | [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] |
| 25 | +0.496 | 14 | 9.178 | 74 % | sys -> sys | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[0]` | [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 26 | +0.496 | 14 | 9.178 | 74 % | sys -> sys | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[3]` | [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 27 | +0.496 | 14 | 9.178 | 74 % | sys -> sys | `milansoc_milansoc_write_w_buffer_level2_reg[2]` | `milansoc_milansoc_write_resp_buffer_level_reg[4]` | [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] |
| 28 | +0.501 | 6 | 7.041 | 82 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[10]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 29 | +0.501 | 6 | 7.041 | 82 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[12]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |
| 30 | +0.501 | 6 | 7.041 | 82 % | eth_clocks0_rx -> eth_clocks0_rx | `FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[0]` | `src_in_r_reg[14]` | [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| [milan -> idelay/ps 200 MHz] FDPE_N -> psrst_sync_r_reg[*] | +0.128 | 0.000 | 1 | 1 | 86 % |
| [milan -> milan] uop_e_r_reg[imm][*] -> taint_r_reg | +0.246 | 0.118 | 1 | 36 | 64 % |
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.324 | 0.196 | 366 | 19 | 74 % |
| [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] | +0.348 | 0.220 | 3 | 16 | 78 % |
| [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] | +0.390 | 0.262 | 92 | 6 | 83 % |
| [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] | +0.393 | 0.265 | 38 | 35 | 66 % |
| [milan -> milan] uop_e_r_reg[fmt][*] -> live_mux_q_reg[*] | +0.411 | 0.283 | 1 | 23 | 75 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +0.496 | 0.368 | 9 | 14 | 74 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC | +0.524 | 0.396 | 4 | 13 | 75 % |
| [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_liteethmacpreambleinserter_state_reg[*] -> eth0_tx_data_reg[*] | +0.564 | 0.436 | 5 | 2 | 88 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +0.568 | 0.440 | 9 | 14 | 74 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA | +0.575 | 0.447 | 4 | 13 | 75 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMA_D1 | +0.579 | 0.451 | 4 | 13 | 75 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.582 | 0.454 | 5 | 12 | 77 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_rpsn_reg | +0.607 | 0.479 | 1 | 15 | 78 % |
| [idelay/ps 200 MHz -> idelay/ps 200 MHz] ps_wd_r_reg[*] -> ps_wd_r_reg[*] | +0.620 | 0.492 | 12 | 4 | 77 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC_D1 | +0.700 | 0.572 | 4 | 13 | 74 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_twtrcon_ready_reg | +0.714 | 0.586 | 1 | 15 | 65 % |
| [sys -> sys] FDPE -> FDPE_N | +0.746 | 0.618 | 1 | 0 | 67 % |
| [sys -> sys] FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_ar_cdc_cdc_graycounter0_q_binary_reg[*] | +0.752 | 0.624 | 3 | 9 | 82 % |
| [sys -> sys] FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_ar_cdc_cdc_graycounter0_q_reg[*] | +0.758 | 0.630 | 3 | 9 | 82 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMB | +0.774 | 0.646 | 4 | 13 | 75 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.782 | 0.654 | 8 | 13 | 66 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.789 | 0.661 | 16 | 15 | 78 % |
| [sys -> sys] FSM_onehot_socbushandler0_axilite2wishbone_state_reg[*] -> milansoc_milannic_aw_cdc_cdc_graycounter0_q_reg[*] | +0.794 | 0.666 | 3 | 9 | 81 % |

Families within 0.3 ns of the worst path (+0.128 ns): [milan -> idelay/ps 200 MHz] FDPE_N -> psrst_sync_r_reg[*] +0.128; [milan -> milan] uop_e_r_reg[imm][*] -> taint_r_reg +0.246; F4 CPU DMA write bridge (inside the CPU netlist) +0.324; [sys -> sys] milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm1_state_reg[*] +0.348; [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_bufferizeendpoints_state_reg[*] -> src_in_r_reg[*] +0.390; [milan -> milan] uop_e_r_reg[imm][*] -> deb_cnt_r_reg[*] +0.393; [milan -> milan] uop_e_r_reg[fmt][*] -> live_mux_q_reg[*] +0.411
F1 bridge -> SPI-flash PHY: worst +2.386 ns, 2.258 ns from the worst path, 14 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.162 ns, 1.034 ns from the worst path, 88 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.324 ns, 0.196 ns from the worst path, 366 endpoints
