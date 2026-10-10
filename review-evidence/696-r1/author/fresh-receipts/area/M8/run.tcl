set_param general.maxThreads 1
set_param synth.maxThreads 1
rename read_verilog recipe_read_verilog
proc read_verilog {args} {
  set mapped {}
  foreach arg $args {
    set group {}
    foreach token $arg {
      if {[file tail $token] eq "KL_maap.sv"} {set token {<scratch>/area-inputs/M8.sv}}
      if {[file tail $token] eq "milan_datapath.sv"} {set token {<scratch>/area-inputs/base-datapath.sv}}
      lappend group $token
    }
    lappend mapped $group
  }
  uplevel 1 [list recipe_read_verilog {*}$mapped]
}
source {<base>/syn/ooc/milan_datapath_ooc.tcl}
quit
