source $LANES/pp43-49-gsi-internal/syn/ooc/protocol_processor_ooc.tcl
report_timing -to [get_cells -hier -filter {NAME =~ *u_aecp/gxr_data_r_reg*}] -max_paths 2 -file gsi_path.rpt
report_timing -from [get_cells -hier -filter {NAME =~ *u_srp/u_listener/fsysid_r_reg*}] -max_paths 1 -file fsysid_path.rpt
