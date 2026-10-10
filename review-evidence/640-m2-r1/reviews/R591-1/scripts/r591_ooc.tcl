# R591-1: out-of-context mapping of the seven retained crossings.
# Usage: vivado -mode batch -source r591_ooc.tcl -tclargs OUTDIR DIRECTIVE VARIANT...
# Each VARIANT names OUTDIR/harness_<VARIANT>.v; results go to
# OUTDIR/util_<VARIANT>_<DIRECTIVE>.rpt and OUTDIR/cells_<VARIANT>_<DIRECTIVE>.tsv.
set out [lindex $argv 0]
set directive [lindex $argv 1]
foreach variant [lrange $argv 2 end] {
    if {[llength [get_files -quiet]]} { remove_files [get_files] }
    read_verilog $out/harness_$variant.v
    synth_design -mode out_of_context -top r591_crossings -part xc7a100tfgg484-2 \
        -directive $directive
    set tag ${variant}_${directive}
    report_utilization -file $out/util_$tag.rpt
    set fh [open $out/cells_$tag.tsv w]
    puts $fh "cell\tref\tRAM_MODE\tWRITE_MODE_A\tWRITE_MODE_B\tDOA_REG\tDOB_REG\tREAD_WIDTH_A\tWRITE_WIDTH_B"
    foreach c [lsort [get_cells -hierarchical -filter {REF_NAME =~ RAMB* || REF_NAME =~ RAM32* || REF_NAME =~ RAM16* || REF_NAME =~ RAM64* || REF_NAME =~ RAM128* || REF_NAME =~ SRL*}]] {
        set r [get_property REF_NAME $c]
        if {[string match RAMB* $r]} {
            puts $fh "$c\t$r\t[get_property RAM_MODE $c]\t[get_property WRITE_MODE_A $c]\t[get_property WRITE_MODE_B $c]\t[get_property DOA_REG $c]\t[get_property DOB_REG $c]\t[get_property READ_WIDTH_A $c]\t[get_property WRITE_WIDTH_B $c]"
        } else {
            puts $fh "$c\t$r\t-\t-\t-\t-\t-\t-\t-"
        }
    }
    close $fh
    close_design
}
