// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VKL_mmcm_drp_servo__pch.h"

VKL_mmcm_drp_servo__Syms::VKL_mmcm_drp_servo__Syms(VerilatedContext* contextp, const char* namep, VKL_mmcm_drp_servo* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(336);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
}

VKL_mmcm_drp_servo__Syms::~VKL_mmcm_drp_servo__Syms() {
    // Tear down scopes
    // Tear down sub module instances
}
