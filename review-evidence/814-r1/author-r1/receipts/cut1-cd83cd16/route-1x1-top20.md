# route-1x1: 5000 sys endpoints, worst slack +0.253 ns
| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | +0.253 | 19 | 9.682 | 75 % | `downW_header_reg[1]` | `dma_bus_aw_rValid_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 2 | +0.254 | 17 | 9.696 | 60 % | `milansoc_socbushandler_adapted_interface_adr_reg[22]` | `milansoc_spiflash_phy_cnt_reg[8]` | F1 bridge -> SPI-flash PHY |
| 3 | +0.315 | 19 | 9.638 | 75 % | `downW_header_reg[1]` | `pendings_valids_reg[0]` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 4 | +0.394 | 19 | 9.542 | 75 % | `downW_header_reg[1]` | `logic_linkEnable_0_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 5 | +0.440 | 19 | 9.513 | 75 % | `downW_header_reg[1]` | `logic_linkEnable_1_reg` | F4 CPU DMA write bridge (inside the CPU netlist) |
| 6 | +0.479 | 16 | 9.471 | 60 % | `milansoc_socbushandler_adapted_interface_adr_reg[22]` | `milansoc_spiflash_phy_cnt_reg[7]` | F1 bridge -> SPI-flash PHY |
| 7 | +0.497 | 15 | 9.228 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine3_state_reg[0]` | F3 ZQCS timer -> bank machines |
| 8 | +0.497 | 15 | 9.228 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine3_state_reg[1]` | F3 ZQCS timer -> bank machines |
| 9 | +0.497 | 15 | 9.228 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine3_state_reg[2]` | F3 ZQCS timer -> bank machines |
| 10 | +0.497 | 15 | 9.228 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine3_state_reg[3]` | F3 ZQCS timer -> bank machines |
| 11 | +0.609 | 14 | 8.811 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine0_trascon_count_reg[0]` | F3 ZQCS timer -> bank machines |
| 12 | +0.609 | 14 | 8.811 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine0_trascon_count_reg[1]` | F3 ZQCS timer -> bank machines |
| 13 | +0.614 | 15 | 9.061 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine0_state_reg[2]` | F3 ZQCS timer -> bank machines |
| 14 | +0.614 | 15 | 9.061 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine0_state_reg[3]` | F3 ZQCS timer -> bank machines |
| 15 | +0.616 | 14 | 8.927 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine3_trascon_ready_reg` | F3 ZQCS timer -> bank machines |
| 16 | +0.616 | 14 | 8.927 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine3_trccon_count_reg[1]` | F3 ZQCS timer -> bank machines |
| 17 | +0.616 | 14 | 8.927 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine3_trccon_ready_reg` | F3 ZQCS timer -> bank machines |
| 18 | +0.631 | 15 | 9.045 | 72 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine0_state_reg[0]` | F3 ZQCS timer -> bank machines |
| 19 | +0.631 | 15 | 9.045 | 72 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `subfragments_bankmachine0_state_reg[1]` | F3 ZQCS timer -> bank machines |
| 20 | +0.666 | 14 | 8.881 | 73 % | `milansoc_sdram_zqcs_timer_count1_reg[11]` | `milansoc_sdram_bankmachine7_twtpcon_count_reg[1]` | F3 ZQCS timer -> bank machines |

| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |
|---|---:|---:|---:|---:|---:|
| F4 CPU DMA write bridge (inside the CPU netlist) | +0.253 | 0.000 | 392 | 19 | 75 % |
| F1 bridge -> SPI-flash PHY | +0.254 | 0.001 | 142 | 17 | 60 % |
| F3 ZQCS timer -> bank machines | +0.497 | 0.244 | 453 | 15 | 73 % |
| milansoc_ws1_reg[*] -> FSM_sequential_subfragments_fsm2_state_reg[*] | +0.769 | 0.516 | 3 | 13 | 77 % |
| milansoc_ws1_reg[*] -> milansoc_psn_reg | +0.798 | 0.545 | 1 | 13 | 75 % |
| milansoc_ws1_reg[*] -> milansoc_rdat1_reg[*] | +0.830 | 0.577 | 64 | 12 | 77 % |
| interface1_adr_reg[*] -> IDELAYE2_N | +0.837 | 0.584 | 62 | 4 | 87 % |
| milansoc_ws1_reg[*] -> milansoc_tmod1_reg[*] | +0.917 | 0.664 | 16 | 14 | 77 % |
| milansoc_ws1_reg[*] -> milansoc_rdat0_reg[*] | +0.959 | 0.706 | 64 | 13 | 78 % |
| milansoc_a7ddrphy_rst_storage_reg -> OSERDESE2_N | +1.018 | 0.765 | 53 | 1 | 94 % |
| interface1_adr_reg[*] -> milansoc_a7ddrphy_bitslip28_value1_reg[*] | +1.132 | 0.879 | 6 | 5 | 83 % |
| interface1_adr_reg[*] -> milansoc_a7ddrphy_bitslip24_value1_reg[*] | +1.167 | 0.914 | 6 | 5 | 83 % |
F1 bridge -> SPI-flash PHY: worst +0.254 ns, 0.001 ns from the worst path, 142 endpoints
F2 SDRAM arbitration -> crossing FIFO read register: worst +1.256 ns, 1.003 ns from the worst path, 84 endpoints
F3 ZQCS timer -> bank machines: worst +0.497 ns, 0.244 ns from the worst path, 453 endpoints
F4 CPU DMA write bridge (inside the CPU netlist): worst +0.253 ns, 0.000 ns from the worst path, 392 endpoints
