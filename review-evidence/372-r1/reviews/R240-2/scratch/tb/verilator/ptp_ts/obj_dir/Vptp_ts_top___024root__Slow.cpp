// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

void Vptp_ts_top___024root___ctor_var_reset(Vptp_ts_top___024root* vlSelf);

Vptp_ts_top___024root::Vptp_ts_top___024root(Vptp_ts_top__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vptp_ts_top___024root___ctor_var_reset(this);
}

void Vptp_ts_top___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vptp_ts_top___024root::~Vptp_ts_top___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
