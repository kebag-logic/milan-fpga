# SPDX-License-Identifier: CERN-OHL-W-2.0
# #607: class constraints run after synthesis, where clock objects exist.

proc kl_quasi_static_constraints {} {
    set cells [get_cells -hierarchical -quiet -filter {quasi_static == "yes"}]
    if {[llength $cells]} {
        set_multicycle_path 4 -setup -from $cells
        set_multicycle_path 3 -hold -from $cells
    }
    puts "CONSTRAINTS: quasi_static cells=[llength $cells] setup=4 hold=3"
}

proc kl_net_clock {name} {
    set clocks [get_clocks -of_objects [get_nets $name]]
    if {[llength $clocks] != 1} {
        error "CONSTRAINTS: expected one clock on net $name, got $clocks"
    }
    return $clocks
}

# #817: KL_mmcm_drp_servo samples the milan-domain reset level into its PS
# clock through a two-flop ASYNC_REG synchronizer, so the reset's arrival at
# the first flop is a crossing, not a single-cycle path between related PLL
# outputs. Only that D pin, from the reset's own clock, is cut; the handshake
# beside it keeps its timing. The chain is found by structure and refused if
# the attribute, the chain or the clock pair is not as stated.
proc kl_servo_reset_sync_constraints {milan_net} {
    set src [kl_net_clock $milan_net]
    set stages [get_cells -hierarchical -quiet \
        -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg*"}]
    if {[llength $stages] != 2} {
        error "CONSTRAINTS: expected two servo reset synchronizer flops, got $stages"
    }
    set first {}; set second {}; set dst {}
    foreach cell $stages {
        if {![string is true -strict [get_property ASYNC_REG $cell]]} {
            error "CONSTRAINTS: servo reset synchronizer $cell lacks ASYNC_REG"
        }
        lappend dst {*}[get_clocks -of_objects [get_pins -of_objects $cell -filter {IS_CLOCK == 1}]]
        set d [get_nets -of_objects [get_pins -of_objects $cell -filter {REF_PIN_NAME == D}]]
        set feed [get_cells -quiet -of_objects \
            [get_pins -quiet -leaf -of_objects $d -filter {DIRECTION == OUT}]]
        if {[llength $feed] == 1 && [lindex $feed 0] in $stages} {
            lappend second $cell
        } else {
            lappend first $cell
        }
    }
    if {[llength $first] != 1 || [llength $second] != 1} {
        error "CONSTRAINTS: servo reset synchronizer is not a two-flop chain: $stages"
    }
    set dst [lsort -unique $dst]
    if {[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]} {
        error "CONSTRAINTS: servo reset synchronizer clock $dst is not one clock distinct from $src"
    }
    set pin [get_pins -of_objects $first -filter {REF_PIN_NAME == D}]
    set_false_path -from $src -to $pin
    puts "CONSTRAINTS: servo reset synchronizer from=$src to=$dst cut=$pin"
}

proc milan_eth_constraints {eth_port part_nets other_nets} {
    set eth [get_clocks -of_objects [get_ports $eth_port]]
    if {[llength $eth] != 1} {
        error "CONSTRAINTS: expected one clock on port $eth_port, got $eth"
    }
    set part {}
    foreach net $part_nets {lappend part [kl_net_clock $net]}
    set other {}
    foreach net $other_nets {lappend other [kl_net_clock $net]}

    # Restore LiteX's MultiReg exception everywhere except the bounded pairs.
    # Destination classes follow the register clock, including reset-extended
    # aliases. No hierarchy spelling or per-register waiver selects a crossing.
    set eth_mr {}; set part_mr {}; set other_mr {}
    foreach cell [get_cells -hierarchical -quiet -filter {mr_ff == TRUE}] {
        set clocks [get_clocks -of_objects [get_pins -of_objects $cell -filter {IS_CLOCK == 1}]]
        if {[llength $clocks] != 1} {
            error "CONSTRAINTS: expected one MultiReg clock for $cell, got $clocks"
        }
        if {$clocks in $eth} {
            lappend eth_mr $cell
        } elseif {$clocks in $part} {
            lappend part_mr $cell
        } else {
            lappend other_mr $cell
        }
    }
    foreach {targets excluded} [list $eth_mr $part $part_mr $eth] {
        if {![llength $targets]} {continue}
        set sources {}
        foreach clock [get_clocks] {
            if {$clock ni $excluded} {lappend sources $clock}
        }
        if {[llength $sources]} {set_false_path -from $sources -to $targets}
        # Asynchronous board inputs retain the original synchronizer exception.
        set inputs [all_inputs]
        if {[llength $inputs]} {set_false_path -from $inputs -to $targets}
    }
    if {[llength $other_mr]} {set_false_path -to $other_mr}

    # Keep LiteX's PRE-pin asynchronous-assert exceptions and its 2 ns
    # inter-stage reset bound. The 8 ns budget covers data crossings, not
    # asynchronous reset assertion. Hold has no phase meaning on either pair.
    # An unbounded Ethernet synchronizer route previously caused a warm-die
    # receive failure; #607 makes that placement-dependent delay visible to STA.
    foreach clock $part {
        set_false_path -hold -from $eth -to $clock
        set_max_delay 8.000 -datapath_only -from $eth -to $clock
        set_false_path -hold -from $clock -to $eth
        set_max_delay 8.000 -datapath_only -from $clock -to $eth
    }
    if {[llength $other]} {
        set_clock_groups -asynchronous -group $eth -group $other
    }
    puts "CONSTRAINTS: eth=$eth bounded=$part async=$other budget_ns=8.000"
    puts "CONSTRAINTS: MultiReg eth=[llength $eth_mr] part=[llength $part_mr] other=[llength $other_mr]"
}
