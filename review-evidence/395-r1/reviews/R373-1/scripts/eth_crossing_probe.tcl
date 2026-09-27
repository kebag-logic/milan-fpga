# Reviewer probe: do the eth-RX crossing exceptions from sw/litex/milan_soc.py:1520-1534
# reach the shipping design? Opens a COPY of the routed checkpoint; writes nothing back.
#   vivado -mode batch -nojournal -notrace -log eth.log -source eth_crossing_probe.tcl -tclargs <route.dcp copy>
set_param general.maxThreads 8
lassign $argv dcp
open_checkpoint $dcp
set eth [get_clocks -of_objects [get_ports eth_clocks0_rx]]
puts "ETH clock=$eth period=[get_property PERIOD $eth]"
foreach name {crg_clkout0 crg_clkout1 crg_audio_ref_raw crg_clkout2} {
    puts "ETH get_clocks $name -> '[get_clocks -quiet $name]'"
}
foreach c [get_clocks] {puts "ETH clock [format %-32s $c] period=[get_property PERIOD $c]"}
report_clock_interaction -delay_type min_max -file eth_clock_interaction.rpt
proc pair {label from to} {
    foreach type {max min} {
        set p [get_timing_paths -from $from -to $to -delay_type $type -max_paths 1 -nworst 1]
        if {[llength $p] == 0} {puts "ETH $label $type: no timed path"; continue}
        puts [format "ETH %s %s: slack=%s requirement=%s exception=<%s> datapath=%s from=%s to=%s" \
            $label $type [get_property SLACK $p] [get_property REQUIREMENT $p] \
            [get_property EXCEPTION $p] [get_property DATAPATH_DELAY $p] \
            [get_property STARTPOINT_PIN $p] [get_property ENDPOINT_PIN $p]]
    }
    set n [llength [get_timing_paths -from $from -to $to -delay_type max -max_paths 100000 -nworst 1]]
    puts "ETH $label timed endpoints (setup): $n"
}
set clk0 [get_clocks milansoc_crg_clkout0]
set clk1 [get_clocks milansoc_crg_clkout1]
pair "eth->clkout0" $eth $clk0
pair "eth->clkout1" $eth $clk1
pair "clkout0->eth" $clk0 $eth
pair "clkout1->eth" $clk1 $eth
# In-memory only: the constraints as the source intends them, with the real names.
set part_cks [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
foreach {a b} [list $eth $part_cks $part_cks $eth] {
    set_false_path -hold -from $a -to $b
    set_max_delay -datapath_only -from $a -to $b 8.000
}
puts "ETH --- after applying the intended exceptions in memory ---"
pair "eth->clkout0" $eth $clk0
pair "eth->clkout1" $eth $clk1
pair "clkout0->eth" $clk0 $eth
pair "clkout1->eth" $clk1 $eth
report_clock_interaction -delay_type min_max -file eth_clock_interaction_intended.rpt
puts "ETH FINISHED"
exit
