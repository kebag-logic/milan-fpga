// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#include "Vaxis_mux_rr_2in_1out__pch.h"


Vaxis_mux_rr_2in_1out___024unit::Vaxis_mux_rr_2in_1out___024unit() = default;
Vaxis_mux_rr_2in_1out___024unit::~Vaxis_mux_rr_2in_1out___024unit() = default;

void Vaxis_mux_rr_2in_1out___024unit::ctor(Vaxis_mux_rr_2in_1out__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
}

void Vaxis_mux_rr_2in_1out___024unit::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vaxis_mux_rr_2in_1out___024unit::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
