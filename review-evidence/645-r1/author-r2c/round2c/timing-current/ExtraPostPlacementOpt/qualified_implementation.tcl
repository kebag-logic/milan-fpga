set_param general.maxThreads 32
open_checkpoint alinx_ax7101_route.dcp
source {$VALIDATION_STORAGE/645-a531/round2c/route-source/sw/litex/timing_grade.tcl}
set ::kl_timing_grade {part xc7a100tfgg484-2 grade commercial min_c 0 max_c 85 corners {Slow Fast}}
kl_timing_grade_check
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property CONFIG_MODE SPIx4 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
write_bitstream -force alinx_ax7101.bit
quit
