// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___ctor_var_reset(Vsim_sim* vlSelf);

Vsim_sim::Vsim_sim() = default;
Vsim_sim::~Vsim_sim() = default;

void Vsim_sim::ctor(Vsim__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vsim_sim___ctor_var_reset(this);
}

void Vsim_sim::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vsim_sim::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
