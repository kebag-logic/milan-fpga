set_param general.maxThreads 8
open_checkpoint {$PACKET/scratch/dcp/alinx_ax7101_route.dcp}
source {$CLONE/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_reports {$PACKET/scratch/committed/signoff}
exit
