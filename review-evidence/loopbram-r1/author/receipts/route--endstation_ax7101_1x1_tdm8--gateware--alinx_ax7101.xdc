################################################################################
# IO constraints
################################################################################
# serial:0.tx
set_property LOC AB15 [get_ports {serial_tx}]
set_property IOSTANDARD LVCMOS33 [get_ports {serial_tx}]

# serial:0.rx
set_property LOC AA15 [get_ports {serial_rx}]
set_property IOSTANDARD LVCMOS33 [get_ports {serial_rx}]

# clk200:0.p
set_property LOC R4 [get_ports {clk200_p}]
set_property IOSTANDARD DIFF_SSTL15 [get_ports {clk200_p}]

# clk200:0.n
set_property LOC T4 [get_ports {clk200_n}]
set_property IOSTANDARD DIFF_SSTL15 [get_ports {clk200_n}]

# cpu_reset_n:0
set_property LOC T6 [get_ports {cpu_reset_n}]
set_property IOSTANDARD LVCMOS15 [get_ports {cpu_reset_n}]

# spiflash:0.cs_n
set_property LOC T19 [get_ports {spiflash_cs_n}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_cs_n}]

# spiflash:0.mosi
set_property LOC P22 [get_ports {spiflash_mosi}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_mosi}]

# spiflash:0.miso
set_property LOC R22 [get_ports {spiflash_miso}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_miso}]

# spiflash:0.wp
set_property LOC P21 [get_ports {spiflash_wp}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_wp}]

# spiflash:0.hold
set_property LOC R21 [get_ports {spiflash_hold}]
set_property IOSTANDARD LVCMOS33 [get_ports {spiflash_hold}]

# eth_clocks:0.rx
set_property LOC K18 [get_ports {eth_clocks0_rx}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_clocks0_rx}]

# eth_clocks:0.gtx
set_property LOC G21 [get_ports {eth_clocks0_gtx}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_clocks0_gtx}]

# eth_clocks:0.tx
set_property LOC K21 [get_ports {eth_clocks0_tx}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth_clocks0_tx}]

# eth:0.rst_n
set_property LOC G20 [get_ports {eth0_rst_n}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rst_n}]

# eth:0.rx_dv
set_property LOC M22 [get_ports {eth0_rx_dv}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_dv}]

# eth:0.rx_er
set_property LOC N18 [get_ports {eth0_rx_er}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_er}]

# eth:0.rx_data
set_property LOC N22 [get_ports {eth0_rx_data[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[0]}]

# eth:0.rx_data
set_property LOC H18 [get_ports {eth0_rx_data[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[1]}]

# eth:0.rx_data
set_property LOC H17 [get_ports {eth0_rx_data[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[2]}]

# eth:0.rx_data
set_property LOC M21 [get_ports {eth0_rx_data[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[3]}]

# eth:0.rx_data
set_property LOC L21 [get_ports {eth0_rx_data[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[4]}]

# eth:0.rx_data
set_property LOC N20 [get_ports {eth0_rx_data[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[5]}]

# eth:0.rx_data
set_property LOC M20 [get_ports {eth0_rx_data[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[6]}]

# eth:0.rx_data
set_property LOC N19 [get_ports {eth0_rx_data[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_rx_data[7]}]

# eth:0.tx_en
set_property LOC G22 [get_ports {eth0_tx_en}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_en}]

# eth:0.tx_data
set_property LOC D22 [get_ports {eth0_tx_data[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[0]}]

# eth:0.tx_data
set_property LOC H20 [get_ports {eth0_tx_data[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[1]}]

# eth:0.tx_data
set_property LOC H22 [get_ports {eth0_tx_data[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[2]}]

# eth:0.tx_data
set_property LOC J22 [get_ports {eth0_tx_data[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[3]}]

# eth:0.tx_data
set_property LOC K22 [get_ports {eth0_tx_data[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[4]}]

# eth:0.tx_data
set_property LOC L19 [get_ports {eth0_tx_data[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[5]}]

# eth:0.tx_data
set_property LOC K19 [get_ports {eth0_tx_data[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[6]}]

# eth:0.tx_data
set_property LOC L20 [get_ports {eth0_tx_data[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_tx_data[7]}]

# eth:0.mdc
set_property LOC J17 [get_ports {eth0_mdc}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_mdc}]

# eth:0.mdio
set_property LOC L16 [get_ports {eth0_mdio}]
set_property IOSTANDARD LVCMOS33 [get_ports {eth0_mdio}]
set_property PULLUP TRUE [get_ports {eth0_mdio}]

# tdm:0.mclk
set_property LOC B22 [get_ports {tdm_mclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_mclk}]

# tdm:0.dout
set_property LOC A20 [get_ports {tdm_dout}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_dout}]

# tdm:0.bclk
set_property LOC B20 [get_ports {tdm_bclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_bclk}]

# tdm:0.din
set_property LOC F20 [get_ports {tdm_din}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_din}]

# tdm:0.fsync
set_property LOC F19 [get_ports {tdm_fsync}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_fsync}]

# tdm:0.lrclk
set_property LOC J16 [get_ports {tdm_lrclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {tdm_lrclk}]

# user_led:0
set_property LOC E17 [get_ports {user_led0}]
set_property IOSTANDARD LVCMOS33 [get_ports {user_led0}]

################################################################################
# Design constraints
################################################################################

set_property IOB TRUE [get_ports {eth0_tx_data[*]}]

set_property IOB TRUE [get_ports eth0_tx_en]

set_property IOB TRUE [get_ports {eth0_rx_data[*]}]

set_property IOB TRUE [get_ports eth0_rx_dv]

set_property IOB TRUE [get_ports eth0_rx_er]

set_multicycle_path 2 -setup -through [get_nets sys_rst]

set_multicycle_path 1 -hold  -through [get_nets sys_rst]

set_property IOB TRUE [get_ports tdm_bclk]

set_property IOB TRUE [get_ports tdm_fsync]

set_property IOB TRUE [get_ports tdm_dout]

################################################################################
# Clock constraints
################################################################################


create_clock -name clk200_p -period 5.0 [get_ports clk200_p]

create_clock -name eth_clocks0_rx -period 8.0 [get_ports eth_clocks0_rx]

################################################################################
# False path constraints
################################################################################


set_false_path -quiet -to [get_pins -filter {REF_PIN_NAME == PRE} -of_objects [get_cells -hierarchical -filter {ars_ff1 == TRUE || ars_ff2 == TRUE}]]

set_max_delay 2 -quiet -from [get_pins -filter {REF_PIN_NAME == C} -of_objects [get_cells -hierarchical -filter {ars_ff1 == TRUE}]] -to [get_pins -filter {REF_PIN_NAME == D} -of_objects [get_cells -hierarchical -filter {ars_ff2 == TRUE}]]

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets milan_clk]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets audio_clk]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets sys_clk]] -group [get_clocks -of [get_nets milansoc_crg_clkin_signal]] -asynchronous

set_clock_groups -group [get_clocks -of [get_nets milan_clk]] -group [get_clocks -of [get_nets audio_clk]] -asynchronous