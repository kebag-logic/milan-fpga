// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsemantics_probe.h for the primary calling header

#include "Vsemantics_probe__pch.h"

void Vsemantics_probe___024root___ctor_var_reset(Vsemantics_probe___024root* vlSelf);

Vsemantics_probe___024root::Vsemantics_probe___024root(Vsemantics_probe__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vsemantics_probe___024root___ctor_var_reset(this);
}

void Vsemantics_probe___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vsemantics_probe___024root::~Vsemantics_probe___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
