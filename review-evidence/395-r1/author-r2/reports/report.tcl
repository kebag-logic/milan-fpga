set_param general.maxThreads 16
open_checkpoint {$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp}
source {$LANES/395-timing-grade/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_reports {$VALIDATION_STORAGE/395-a390-work/final-3a0cb4cf4/signoff}
exit
