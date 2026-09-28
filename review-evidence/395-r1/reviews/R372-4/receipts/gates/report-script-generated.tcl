set_param general.maxThreads 16
open_checkpoint {<packet>/scratch/report-gen/input/dummy_route.dcp}
source {<repo>/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_reports {<packet>/scratch/report-gen/out/signoff}
exit
