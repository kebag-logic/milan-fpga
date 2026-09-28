set_max_delay 8 -datapath_only -from [get_clocks wrong_clock_607] -to [get_clocks -of_objects [get_nets sys_clk]]
set_clock_groups -asynchronous -group [get_clocks wrong_clock_607] -group [get_clocks -of_objects [get_nets sys_clk]]
if {1} {set_false_path -from [get_clocks wrong_clock_607]}
