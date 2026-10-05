set_param general.maxThreads 32
read_verilog -sv {$VALIDATION_STORAGE/pp148-a532/head/hdl/common/pp_pkg.sv}
read_verilog -sv {$VALIDATION_STORAGE/pp148-a532/head/hdl/aecp/KL_aecp_notify.sv}
read_xdc clock.xdc
synth_design -directive AreaOptimized_high -top KL_aecp_notify -part xc7a100t-fgg484-2 -mode out_of_context -generic N_CTRL_P=16 -generic N_STREAM_IN_P=2 -generic N_STREAM_OUT_P=2 -generic TL_TIMEOUT_MS_P=300000 -generic LOCK_TIMEOUT_MS_P=60000 -generic TMR_SLOTS_P=61 -generic TMR_REGMON_BASE_P=7 -generic TMR_LOCK_SLOT_P=43 -generic TMR_IDENT_SLOT_P=44 -generic EN_IDENTIFY_NOTIF_P=0
report_utilization -file util.rpt
report_utilization -hierarchical -file hier.rpt
quit
