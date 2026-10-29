# Out-of-context engine: the repository's synthesis (syn/ooc/engine_ooc.tcl)
# followed by opt_design and place_design, so the report counts slices.
# usage: vivado -mode batch -source engine_place.tcl -tclargs <repo> <tag>
# Run in a directory holding gptp_ucode.hex.
set SPEC [file normalize [lindex $argv 0]]
set TAG [lindex $argv 1]
read_xdc $SPEC/syn/ooc/ooc_clock.xdc
read_verilog -sv \
    $SPEC/hdl/ucpu/gptp_ucpu_pkg.sv \
    $SPEC/hdl/ucpu/KL_gptp_ucpu.sv \
    $SPEC/hdl/wire/KL_gptp_rx_parser.sv \
    $SPEC/hdl/wire/KL_gptp_tx_slot.sv \
    $SPEC/hdl/common/KL_gptp_timer.sv \
    $SPEC/hdl/top/KL_gptp_engine.sv
synth_design -mode out_of_context -top KL_gptp_engine -part xc7a100tfgg484-2 \
    -generic UCODE_HEX_P=gptp_ucode.hex
report_utilization -file ${TAG}_synth_util.rpt
opt_design
place_design
report_utilization -file ${TAG}_place_util.rpt
report_timing_summary -delay_type max -max_paths 3 -file ${TAG}_place_timing.rpt
