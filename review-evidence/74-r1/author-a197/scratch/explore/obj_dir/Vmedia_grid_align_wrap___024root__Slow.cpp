// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmedia_grid_align_wrap.h for the primary calling header

#include "Vmedia_grid_align_wrap__pch.h"

void Vmedia_grid_align_wrap___024root___ctor_var_reset(Vmedia_grid_align_wrap___024root* vlSelf);

Vmedia_grid_align_wrap___024root::Vmedia_grid_align_wrap___024root(Vmedia_grid_align_wrap__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vmedia_grid_align_wrap___024root___ctor_var_reset(this);
}

void Vmedia_grid_align_wrap___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vmedia_grid_align_wrap___024root::~Vmedia_grid_align_wrap___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
