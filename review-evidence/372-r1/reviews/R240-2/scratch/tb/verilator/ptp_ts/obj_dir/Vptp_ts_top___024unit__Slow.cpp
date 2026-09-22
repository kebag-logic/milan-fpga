// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"


Vptp_ts_top___024unit::Vptp_ts_top___024unit() = default;
Vptp_ts_top___024unit::~Vptp_ts_top___024unit() = default;

void Vptp_ts_top___024unit::ctor(Vptp_ts_top__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
}

void Vptp_ts_top___024unit::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vptp_ts_top___024unit::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
