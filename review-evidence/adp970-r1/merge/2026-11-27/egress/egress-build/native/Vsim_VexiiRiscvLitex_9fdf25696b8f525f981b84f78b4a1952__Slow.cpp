// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);

Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952::Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952() = default;
Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952::~Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952() = default;

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952::ctor(Vsim__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset(this);
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
