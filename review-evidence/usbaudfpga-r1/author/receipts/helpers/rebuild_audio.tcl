# Rebuild current RTL using unchanged generated inputs, then apply the route recipe.
# Arguments: original synthesis script, route helper, then its arguments.
set handle [open [lindex $argv 0] r]
set original [read $handle]
close $handle
set marker {write_checkpoint -force digilent_arty_synth.dcp}
set boundary [string first $marker $original]
if {$boundary < 0} {error {missing synthesis checkpoint boundary}}
eval [string range $original 0 [expr {$boundary+[string length $marker]-1}]]
close_design
set recipe [lindex $argv 1]
set argv [lrange $argv 2 end]
source $recipe
