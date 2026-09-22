// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vaxis_mux_rr_2in_1out__pch.h"

Vaxis_mux_rr_2in_1out__Syms::Vaxis_mux_rr_2in_1out__Syms(VerilatedContext* contextp, const char* namep, Vaxis_mux_rr_2in_1out* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(284);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    // Setup export functions - final: 0
    // Setup export functions - final: 1
}

Vaxis_mux_rr_2in_1out__Syms::~Vaxis_mux_rr_2in_1out__Syms() {
    // Tear down scopes
    // Tear down sub module instances
}
