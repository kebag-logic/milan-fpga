// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_RegFileMem___ctor_var_reset(Vsim_RegFileMem* vlSelf);

Vsim_RegFileMem::Vsim_RegFileMem() = default;
Vsim_RegFileMem::~Vsim_RegFileMem() = default;

void Vsim_RegFileMem::ctor(Vsim__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vsim_RegFileMem___ctor_var_reset(this);
}

void Vsim_RegFileMem::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vsim_RegFileMem::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
