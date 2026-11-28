// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsim__pch.h"

Vsim__Syms::Vsim__Syms(VerilatedContext* contextp, const char* namep, Vsim* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    Vsim__Syms__ctor__0();
}

Vsim__Syms::~Vsim__Syms() {
    Vsim__Syms__dtor__0();
}
