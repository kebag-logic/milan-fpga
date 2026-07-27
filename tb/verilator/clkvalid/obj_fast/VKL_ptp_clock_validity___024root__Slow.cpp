// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_ptp_clock_validity.h for the primary calling header

#include "VKL_ptp_clock_validity__pch.h"

void VKL_ptp_clock_validity___024root___ctor_var_reset(VKL_ptp_clock_validity___024root* vlSelf);

VKL_ptp_clock_validity___024root::VKL_ptp_clock_validity___024root(VKL_ptp_clock_validity__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    VKL_ptp_clock_validity___024root___ctor_var_reset(this);
}

void VKL_ptp_clock_validity___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

VKL_ptp_clock_validity___024root::~VKL_ptp_clock_validity___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
