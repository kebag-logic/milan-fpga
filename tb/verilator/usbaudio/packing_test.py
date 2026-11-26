#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise the physical packing grader with absent and misplaced endpoints."""
import argparse
from pathlib import Path
import shutil
import subprocess

FIXTURE = r'''
source [lindex $argv 0]
set report [lindex $argv 1]
set defect [lindex $argv 2]
set attrs {}; set ports {}; set nets {}; set netpins {}; set pincells {}
set bufferpins {}; set drivers {}; set inputs {}
set index 0
proc pad {name bidir role} {
    global attrs ports nets netpins pincells bufferpins drivers inputs index
    set b b$index
    dict set ports $name p$index
    dict set nets p$index n$index
    dict set netpins n$index bp$index
    dict set pincells bp$index $b
    dict set attrs $b REF_NAME [expr {$bidir ? "IOBUF" : "OBUF"}]
    dict set attrs $b LOC IOB_X0Y$index
    dict set bufferpins $b I ip$index
    dict set drivers ip$index out$index
    dict set attrs out$index IS_SEQUENTIAL 1
    dict set attrs out$index LOC OLOGIC_X0Y$index
    dict set attrs out$index REF_NAME [expr {$role eq "clock" ? "ODDR" : "FDRE"}]
    if {$bidir} {
        dict set inputs $b [list [list in$index]]
        dict set attrs in$index IS_SEQUENTIAL 1
        dict set attrs in$index LOC ILOGIC_X0Y$index
        dict set attrs in$index REF_NAME FDRE
        dict set bufferpins $b T tp$index
        dict set drivers tp$index tri$index
        dict set attrs tri$index IS_SEQUENTIAL 1
        dict set attrs tri$index LOC OLOGIC_X0Y$index
        dict set attrs tri$index REF_NAME FDSE
    }
    incr index
}
for {set bit 0} {$bit < 16} {incr bit} { pad [format {usbaudio_dq[%d]} $bit] 1 data }
foreach name {usbaudio_addr[0] usbaudio_addr[1] usbaudio_slwr_n usbaudio_slrd_n usbaudio_sloe_n usbaudio_pktend_n} {
    pad $name 0 control
}
pad usbaudio_pclk 0 clock
proc lookup {table args} {
    if {![dict exists $table {*}$args]} { return {} }
    return [dict get $table {*}$args]
}
proc get_ports {name} { global ports; return [lookup $ports $name] }
proc get_nets {args} { global nets; return [lookup $nets [lindex $args end]] }
proc get_cells {args} { global pincells; return [lookup $pincells [lindex $args end]] }
proc get_pins {args} {
    global netpins bufferpins
    set object [lindex $args [expr {[lsearch -exact $args -of_objects]+1}]]
    if {[dict exists $netpins $object]} { return [dict get $netpins $object] }
    set filter [lindex $args end]
    return [lookup $bufferpins $object [lindex $filter end]]
}
proc get_property {property object} { global attrs; return [lookup $attrs $object $property] }
# Pad traversal has its own repository tests. These fixtures supply the
# resulting connectivity, then exercise this grader's endpoint checks.
proc kl_iob_net_cells {pin dir} {
    global drivers
    return [list 1 [lookup $drivers $pin]]
}
proc kl_iob_far_groups {buffer dir} {
    global inputs
    return [list 1 [lookup $inputs $buffer]]
}
switch -- $defect {
    good {}
    missing_input { dict set inputs b0 {} }
    unplaced_input { dict set attrs in0 LOC {} }
    wrong_output_pad { dict set attrs out0 LOC OLOGIC_X0Y1 }
    unregistered_tristate { dict set attrs tri0 IS_SEQUENTIAL 0 }
    missing_control { dict unset ports usbaudio_slwr_n }
    wrong_forwarder { dict set attrs out22 REF_NAME FDRE }
    missing_buffer { dict unset pincells bp22 }
    disconnected_output { dict unset drivers ip0 }
    default { error "unknown fixture" }
}
kl_audio_pack_check $report
puts "PASS all 55 audio pad registers"
'''


def main() -> None:
    """Require the complete pad fixture and reject each broken placement."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fixture = args.out / "packing_fixture.tcl"
    fixture.write_text(FIXTURE)
    engine = shutil.which("tclsh")
    if engine is None:
        raise RuntimeError("script interpreter unavailable")
    source = Path(__file__).resolve().parents[3] / "sw/litex/usbaudio_pack.tcl"
    cases = ("good", "missing_input", "unplaced_input", "wrong_output_pad",
             "unregistered_tristate", "missing_control", "wrong_forwarder",
             "missing_buffer", "disconnected_output")
    for case in cases:
        result = subprocess.run([engine, str(fixture), str(source),
                                 str(args.out / (case+".rpt")), case],
                                text=True, capture_output=True, check=False)
        output = result.stdout + result.stderr
        (args.out / (case+".log")).write_text(output)
        if case == "good":
            passed = result.returncode == 0 and "PASS all 55" in output
        else:
            passed = result.returncode != 0 and "Audio packing:" in output
        if not passed:
            raise RuntimeError("packing control failed: "+case+"\n"+output)
    print("PASS audio packing grader: 55 endpoints and eight negative controls")


if __name__ == "__main__":
    main()
