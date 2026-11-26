// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim___024root___ctor_var_reset(Vsim___024root* vlSelf);

Vsim___024root::Vsim___024root(Vsim__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vsim___024root___ctor_var_reset(this);
}

void Vsim___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vsim___024root::~Vsim___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
