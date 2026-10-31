# route-1x1-ASLH: 5000 endpoints over every path group, worst slack +0.126 ns
| # | Slack ns | Levels | Data ns | Routing | Clocks | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | +0.126 | 18 | 9.796 | 77 % | sys -> sys | `downW_header_reg[0]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.328 | 18 | 9.672 | 77 % | sys -> sys | `downW_header_reg[0]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 3 | +0.331 | 18 | 9.668 | 77 % | sys -> sys | `downW_header_reg[0]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.334 | 18 | 9.609 | 76 % | sys -> sys | `downW_header_reg[0]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.399 | 33 | 19.219 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[21]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 6 | +0.399 | 33 | 19.219 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[22]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 7 | +0.399 | 33 | 19.219 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[23]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 8 | +0.399 | 33 | 19.219 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[24]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 9 | +0.402 | 33 | 19.215 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[17]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 10 | +0.402 | 33 | 19.215 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[18]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 11 | +0.402 | 33 | 19.215 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[19]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 12 | +0.402 | 33 | 19.215 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[20]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 13 | +0.437 | 33 | 19.182 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[25]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 14 | +0.437 | 33 | 19.182 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[26]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 15 | +0.437 | 33 | 19.182 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[27]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 16 | +0.437 | 33 | 19.182 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[28]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 17 | +0.470 | 33 | 19.150 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[29]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 18 | +0.470 | 33 | 19.150 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[30]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 19 | +0.470 | 33 | 19.150 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[31]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 20 | +0.472 | 15 | 9.091 | 79 % | sys -> sys | `downW_header_reg[0]` | `onW_buffer_0_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 21 | +0.472 | 15 | 9.091 | 79 % | sys -> sys | `downW_header_reg[0]` | `onW_buffer_1_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 22 | +0.472 | 15 | 9.091 | 79 % | sys -> sys | `downW_header_reg[0]` | `onW_buffer_2_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 23 | +0.472 | 15 | 9.091 | 79 % | sys -> sys | `downW_header_reg[0]` | `onW_buffer_3_strb_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 24 | +0.508 | 33 | 19.107 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[13]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 25 | +0.508 | 33 | 19.107 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[14]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 26 | +0.508 | 33 | 19.107 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[15]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 27 | +0.508 | 33 | 19.107 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[16]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 28 | +0.526 | 15 | 9.280 | 72 % | sys -> sys | `milansoc_milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[17]` | `subfragments_bankmachine6_state_reg[1]` | [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] |
| 29 | +0.528 | 33 | 19.087 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[10]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |
| 30 | +0.528 | 33 | 19.087 | 67 % | milan -> milan | `desc_base_r_reg[0]` | `deb_cnt_r_reg[11]` | [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.126 | 0.000 | 372 | 18 | 77 % |
| [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] | +0.399 | 0.273 | 38 | 33 | 67 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> subfragments_bankmachineN_state_reg[*] | +0.526 | 0.400 | 32 | 15 | 72 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> storage_N_reg_N | +0.536 | 0.410 | 5 | 11 | 83 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_count_reg[*] | +0.589 | 0.463 | 24 | 14 | 73 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trascon_ready_reg | +0.628 | 0.502 | 8 | 14 | 72 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_count_reg[*] | +0.657 | 0.531 | 40 | 14 | 72 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_twtpcon_ready_reg | +0.657 | 0.531 | 8 | 14 | 72 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_count_reg[*] | +0.741 | 0.615 | 40 | 14 | 72 % |
| [sys -> sys] milansoc_milansoc_sdram_bankmachineN_pipe_valid_source_payload_addr_reg[*] -> milansoc_milansoc_sdram_bankmachineN_trccon_ready_reg | +0.741 | 0.615 | 8 | 14 | 72 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.808 | 0.682 | 16 | 14 | 77 % |
| [sys -> sys] FDPE_N -> align_cnt_r_reg[*] | +0.886 | 0.760 | 32 | 0 | 96 % |
| [eth_clocks0_rx -> eth_clocks0_rx] idx_r_reg[*] -> delta_r_reg[*] | +0.919 | 0.793 | 8 | 9 | 73 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_w_buffer_consume_reg[*] | +0.983 | 0.857 | 4 | 11 | 82 % |
| [sys -> sys] FDPE_N -> milansoc_milan_mac_liteethmaccore_preamble_errors_status_reg[*] | +1.032 | 0.906 | 32 | 0 | 96 % |
| [sys -> sys] FDPE_N -> align_evt_r_reg | +1.051 | 0.925 | 1 | 0 | 96 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMC_D1 | +1.058 | 0.932 | 4 | 12 | 81 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> RAMB_D1 | +1.063 | 0.937 | 4 | 12 | 81 % |
| [sys -> sys] milansoc_ws1_reg[*] -> milansoc_converter2_dat_r_reg[*] | +1.075 | 0.949 | 64 | 12 | 80 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_resp_buffer_level_reg[*] | +1.086 | 0.960 | 9 | 13 | 80 % |
| [eth_clocks0_rx -> eth_clocks0_rx] FSM_sequential_subfragments_txdatapath_liteethmacpreambleinserter_state_reg[*] -> src_in_r_reg[*] | +1.087 | 0.961 | 92 | 6 | 77 % |
| [sys -> sys] milansoc_milansoc_write_w_buffer_level2_reg[*] -> milansoc_milansoc_write_id_buffer_level_reg[*] | +1.094 | 0.968 | 9 | 13 | 80 % |
| [eth_clocks0_rx -> eth_clocks0_rx] FDPE_N -> FDPE_N | +1.129 | 1.003 | 4 | 0 | 53 % |
| [sys -> sys] milansoc_ws1_reg[*] -> dma_bus_w_s2mPipe_rData_data_reg[*] | +1.155 | 1.029 | 29 | 11 | 80 % |
| [milan -> milan] desc_base_r_reg[*] -> taint_r_reg | +1.158 | 1.032 | 1 | 33 | 65 % |

Families within 0.3 ns of the worst path (+0.126 ns): F4 CPU DMA write bridge (inside the CPU netlist) +0.126; [milan -> milan] desc_base_r_reg[*] -> deb_cnt_r_reg[*] +0.399
F1 bridge -> SPI-flash PHY: worst +2.085 ns, 1.959 ns from the worst path, 49 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.392 ns, 1.266 ns from the worst path, 87 endpoints
F3 ZQCS timer -> bank machines: no endpoint among the listed paths
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.126 ns, 0.000 ns from the worst path, 372 endpoints
