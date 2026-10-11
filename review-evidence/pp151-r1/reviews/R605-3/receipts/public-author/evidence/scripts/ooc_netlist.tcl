# usage: vivado -mode batch -source ooc_netlist.tcl -tclargs <tree> [SI SO]
# the tree's own syn/ooc/protocol_processor_ooc.tcl, then the funcsim netlist
set tree [file normalize [lindex $argv 0]]
source $tree/syn/ooc/protocol_processor_ooc.tcl
write_verilog -force -mode funcsim netlist.v
