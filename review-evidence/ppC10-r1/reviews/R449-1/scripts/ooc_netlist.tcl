# Source the in-tree OOC recipe of the tree given as argv 0, then write the
# synthesized netlist. Run in an empty directory:
#   vivado -mode batch -source ooc_netlist.tcl -tclargs <tree>
set TREE [file normalize [lindex $argv 0]]
source $TREE/syn/ooc/protocol_processor_ooc.tcl
write_verilog -force -mode design netlist.v
