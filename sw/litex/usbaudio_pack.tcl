# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Check all audio pad registers on the placed design, including bidirectional DQ.
source [file join [file dirname [info script]] iob_pack_check.tcl]

proc kl_audio_one {objects what} {
    if {[llength $objects] != 1} {
        error "Audio packing: expected one $what, found [llength $objects]"
    }
    return [lindex $objects 0]
}

proc kl_audio_register {cells buffer role report} {
    set cell [kl_audio_one $cells "$role register"]
    if {![string is true -strict [get_property IS_SEQUENTIAL $cell]]} {
        error "Audio packing: $role reaches nonsequential cell $cell"
    }
    set location [get_property LOC $cell]
    set pad_location [get_property LOC $buffer]
    set kind [expr {$role eq "input" ? "ILOGIC" : "OLOGIC"}]
    if {![regexp {^IOB_(X[0-9]+Y[0-9]+)$} $pad_location unused coordinate]
        || $location ne "${kind}_${coordinate}"} {
        error "Audio packing: $role $cell at $location does not match pad $buffer at $pad_location"
    }
    if {$role eq "clock" && [get_property REF_NAME $cell] ne "ODDR"} {
        error "Audio packing: forwarded clock is not a double-edge output register"
    }
    puts $report "PASS $role $cell $location pad $pad_location"
    return $cell
}

proc kl_audio_buffer {port_name bidirectional} {
    set port [kl_audio_one [get_ports $port_name] "port $port_name"]
    set net [kl_audio_one [get_nets -of_objects $port] "pad net $port_name"]
    set pin_name [expr {$bidirectional ? "IO" : "O"}]
    set pins [get_pins -leaf -of_objects $net -filter "REF_PIN_NAME == $pin_name"]
    set buffer [kl_audio_one [get_cells -of_objects $pins] "pad buffer $port_name"]
    set expected [expr {$bidirectional ? "IOBUF" : "OBUF"}]
    if {[get_property REF_NAME $buffer] ne $expected} {
        error "Audio packing: $port_name does not use $expected"
    }
    return $buffer
}

proc kl_audio_output {buffer pin_name role report} {
    set pin [kl_audio_one [get_pins -of_objects $buffer -filter "REF_PIN_NAME == $pin_name"] "$role buffer pin"]
    lassign [kl_iob_net_cells $pin OUT] reached cells
    if {!$reached} { error "Audio packing: $role has no driver net" }
    return [kl_audio_register $cells $buffer $role $report]
}

proc kl_audio_pack_check {report_path} {
    set report [open $report_path w]
    set registers {}
    try {
        for {set bit 0} {$bit < 16} {incr bit} {
            set buffer [kl_audio_buffer [format {usbaudio_dq[%d]} $bit] 1]
            lassign [kl_iob_far_groups $buffer IN] reached groups
            if {!$reached} { error "Audio packing: input $bit has an incomplete pad path" }
            set inputs {}
            foreach group $groups {
                foreach cell $group { lappend inputs $cell }
            }
            lappend registers [kl_audio_register $inputs $buffer input $report]
            lappend registers [kl_audio_output $buffer I output $report]
            lappend registers [kl_audio_output $buffer T tristate $report]
        }
        foreach name {usbaudio_addr[0] usbaudio_addr[1] usbaudio_slwr_n usbaudio_slrd_n usbaudio_sloe_n usbaudio_pktend_n} {
            lappend registers [kl_audio_output [kl_audio_buffer $name 0] I control $report]
        }
        lappend registers [kl_audio_output [kl_audio_buffer usbaudio_pclk 0] I clock $report]
        if {[llength $registers] != 55 || [llength [lsort -unique $registers]] != 55} {
            error "Audio packing: expected 55 distinct pad registers"
        }
        puts $report "PASS all 55 audio pad registers"
    } finally {
        close $report
    }
}
