# Allow full period data path delay between internal FIFO registers
set_max_delay -datapath_only \
    -from [get_pins {ethernet_mac/tx_fifo/fifo_inst/*/C}] \
    -to   [get_pins {ethernet_mac/tx_fifo/fifo_inst/*/D}] 10.0

# Declare the specified clock groups as asynchronous
set_clock_groups -asynchronous \
  -group [get_clocks clk_100_milan_dma_clk_wiz_0_0] \
  -group [get_clocks gtx_clk_milan_dma_clk_wiz_0_0] \
  -group [get_clocks gtx90_clk_milan_dma_clk_wiz_0_0]

# Declare false path between asynchronous reset synchronizers to avoid false timing violations
set_false_path \
  -from [get_pins ethernet_mac/rx_fifo/fifo_inst/s_rst_sync1_reg_reg_replica/Q] \
  -to   [get_pins ethernet_mac/tx_fifo/fifo_inst/m_rst_sync2_reg_reg/D]


