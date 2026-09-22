// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#include "Vaxis_mux_rr_2in_1out__pch.h"

void Vaxis_mux_rr_2in_1out___024root___ctor_var_reset(Vaxis_mux_rr_2in_1out___024root* vlSelf);

Vaxis_mux_rr_2in_1out___024root::Vaxis_mux_rr_2in_1out___024root(Vaxis_mux_rr_2in_1out__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vaxis_mux_rr_2in_1out___024root___ctor_var_reset(this);
}

void Vaxis_mux_rr_2in_1out___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vaxis_mux_rr_2in_1out___024root::~Vaxis_mux_rr_2in_1out___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
