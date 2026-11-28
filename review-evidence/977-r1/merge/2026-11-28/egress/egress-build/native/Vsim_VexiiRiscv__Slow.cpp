// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscv___ctor_var_reset(Vsim_VexiiRiscv* vlSelf);

Vsim_VexiiRiscv::Vsim_VexiiRiscv() = default;
Vsim_VexiiRiscv::~Vsim_VexiiRiscv() = default;

void Vsim_VexiiRiscv::ctor(Vsim__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vsim_VexiiRiscv___ctor_var_reset(this);
}

void Vsim_VexiiRiscv::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vsim_VexiiRiscv::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
