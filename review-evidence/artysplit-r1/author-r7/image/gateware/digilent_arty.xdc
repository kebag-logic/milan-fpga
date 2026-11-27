################################################################################
# IO constraints
################################################################################
# serial:0.tx
set_property LOC D10 [get_ports {serial_tx}]
set_property IOSTANDARD LVCMOS33 [get_ports {serial_tx}]

# serial:0.rx
set_property LOC A9 [get_ports {serial_rx}]
set_property IOSTANDARD LVCMOS33 [get_ports {serial_rx}]

# clk100:0
set_property LOC E3 [get_ports {clk100}]
set_property IOSTANDARD LVCMOS33 [get_ports {clk100}]

# cpu_reset_n:0
set_property LOC C2 [get_ports {cpu_reset_n}]
set_property IOSTANDARD LVCMOS33 [get_ports {cpu_reset_n}]

# eth_ref_clk:0
set_property LOC G18 [get_ports {eth_ref_clk}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_ref_clk}]

# spiflash:0.cs_n
set_property LOC L13 [get_ports {spiflash_cs_n}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_cs_n}]

# spiflash:0.clk
set_property LOC L16 [get_ports {spiflash_clk}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_clk}]

# spiflash:0.mosi
set_property LOC K17 [get_ports {spiflash_mosi}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_mosi}]

# spiflash:0.miso
set_property LOC K18 [get_ports {spiflash_miso}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_miso}]

# spiflash:0.wp
set_property LOC L14 [get_ports {spiflash_wp}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_wp}]

# spiflash:0.hold
set_property LOC M14 [get_ports {spiflash_hold}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_hold}]

# i2s_rx:0.clk
set_property LOC A18 [get_ports {i2s_rx_clk}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_rx_clk}]

# i2s_rx:0.sync
set_property LOC B18 [get_ports {i2s_rx_sync}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_rx_sync}]

# i2s_rx:0.rx
set_property LOC K16 [get_ports {i2s_rx_rx}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_rx_rx}]

# i2s_rx_mclk:0
set_property LOC D13 [get_ports {i2s_rx_mclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_rx_mclk}]

# i2s_tx:0.clk
set_property LOC A11 [get_ports {i2s_tx_clk}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_tx_clk}]

# i2s_tx:0.sync
set_property LOC B11 [get_ports {i2s_tx_sync}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_tx_sync}]

# i2s_tx:0.tx
set_property LOC D12 [get_ports {i2s_tx_tx}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_tx_tx}]

# i2s_tx_mclk:0
set_property LOC G13 [get_ports {i2s_tx_mclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {i2s_tx_mclk}]

# eth_clocks:0.tx
set_property LOC H16 [get_ports {eth_clocks0_tx}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_clocks0_tx}]

# eth_clocks:0.rx
set_property LOC F15 [get_ports {eth_clocks0_rx}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_clocks0_rx}]

# eth:0.rst_n
set_property LOC C16 [get_ports {eth0_rst_n}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rst_n}]

# eth:0.mdio
set_property LOC K13 [get_ports {eth0_mdio}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_mdio}]

# eth:0.mdc
set_property LOC F16 [get_ports {eth0_mdc}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_mdc}]

# eth:0.rx_dv
set_property LOC G16 [get_ports {eth0_rx_dv}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_dv}]

# eth:0.rx_er
set_property LOC C17 [get_ports {eth0_rx_er}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_er}]

# eth:0.rx_data
set_property LOC D18 [get_ports {eth0_rx_data[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[0]}]

# eth:0.rx_data
set_property LOC E17 [get_ports {eth0_rx_data[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[1]}]

# eth:0.rx_data
set_property LOC E18 [get_ports {eth0_rx_data[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[2]}]

# eth:0.rx_data
set_property LOC G17 [get_ports {eth0_rx_data[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[3]}]

# eth:0.tx_en
set_property LOC H15 [get_ports {eth0_tx_en}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_en}]

# eth:0.tx_data
set_property LOC H14 [get_ports {eth0_tx_data[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[0]}]

# eth:0.tx_data
set_property LOC J14 [get_ports {eth0_tx_data[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[1]}]

# eth:0.tx_data
set_property LOC J13 [get_ports {eth0_tx_data[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[2]}]

# eth:0.tx_data
set_property LOC H17 [get_ports {eth0_tx_data[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[3]}]

# eth:0.col
set_property LOC D17 [get_ports {eth0_col}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_col}]

# eth:0.crs
set_property LOC G14 [get_ports {eth0_crs}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_crs}]

# user_led:0
set_property LOC H5 [get_ports {user_led0}]
set_property IOSTANDARD LVCMOS33 [get_ports {user_led0}]

################################################################################
# Design constraints
################################################################################

set_property INTERNAL_VREF 0.675 [get_iobanks 34]

set_property IOB TRUE [get_ports {eth0_tx_data[*]}]

set_property IOB TRUE [get_ports eth0_tx_en]

################################################################################
# Clock constraints
################################################################################


create_clock -name clk100 -period 10.0 [get_ports clk100]

create_clock -name eth_clocks0_tx -period 40.0 [get_ports eth_clocks0_tx]

create_clock -name eth_clocks0_rx -period 40.0 [get_ports eth_clocks0_rx]

################################################################################
# False path constraints
################################################################################


set_false_path -quiet -to [get_cells -hierarchical -filter {mr_ff == TRUE}]

set_false_path -quiet -to [get_pins -filter {REF_PIN_NAME == PRE} -of_objects [get_cells -hierarchical -filter {ars_ff1 == TRUE || ars_ff2 == TRUE}]]

set_max_delay 2 -quiet -from [get_pins -filter {REF_PIN_NAME == C} -of_objects [get_cells -hierarchical -filter {ars_ff1 == TRUE}]] -to [get_pins -filter {REF_PIN_NAME == D} -of_objects [get_cells -hierarchical -filter {ars_ff2 == TRUE}]]

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets milan_clk]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets audio_clk]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets clkin_signal]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets milan_clk]] -group [get_clocks -of [get_nets audio_clk]] -asynchronous
################################################################################
# Additional XDC constraints
################################################################################

set_clock_groups -asynchronous -group [get_clocks -of_objects [get_ports eth_clocks0_rx]]

set_clock_groups -asynchronous -group [get_clocks -of_objects [get_ports eth_clocks0_tx]]