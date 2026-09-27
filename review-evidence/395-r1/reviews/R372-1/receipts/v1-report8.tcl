set_param general.maxThreads 8
open_checkpoint {$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp}
source {$CLONE/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_reports {$PACKET/scratch/viv/pr-report/signoff}
exit
