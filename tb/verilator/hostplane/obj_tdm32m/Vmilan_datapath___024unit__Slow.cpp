// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"


Vmilan_datapath___024unit::Vmilan_datapath___024unit() = default;
Vmilan_datapath___024unit::~Vmilan_datapath___024unit() = default;

void Vmilan_datapath___024unit::ctor(Vmilan_datapath__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
}

void Vmilan_datapath___024unit::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vmilan_datapath___024unit::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
