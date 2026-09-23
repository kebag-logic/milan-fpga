// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

void Vchmap_wrap_KL_chan_map_capture___ctor_var_reset(Vchmap_wrap_KL_chan_map_capture* vlSelf);

Vchmap_wrap_KL_chan_map_capture::Vchmap_wrap_KL_chan_map_capture() = default;
Vchmap_wrap_KL_chan_map_capture::~Vchmap_wrap_KL_chan_map_capture() = default;

void Vchmap_wrap_KL_chan_map_capture::ctor(Vchmap_wrap__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vchmap_wrap_KL_chan_map_capture___ctor_var_reset(this);
}

void Vchmap_wrap_KL_chan_map_capture::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vchmap_wrap_KL_chan_map_capture::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
