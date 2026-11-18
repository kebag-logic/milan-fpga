# Vivado out-of-context synthesis of cdc_pair_fifo alone, the candidate's (old.sv) and p11's (new.sv) default branch,
# at each parameter set a default-branch instance takes; utilisation of each into its own report.
foreach v {old new} {
  foreach pw {{48 3} {52 3} {48 4} {192 2}} {
    set w [lindex $pw 0]; set l [lindex $pw 1]
    read_verilog -sv $v.sv
    synth_design -mode out_of_context -top cdc_pair_fifo -part xc7a100tfgg484-2 -generic WIDTH=$w -generic LOG2D=$l -flatten_hierarchy rebuilt
    report_utilization -file util-$v-w${w}l${l}.rpt
    report_utilization -hierarchical -file hier-$v-w${w}l${l}.rpt
    close_design
  }
}
