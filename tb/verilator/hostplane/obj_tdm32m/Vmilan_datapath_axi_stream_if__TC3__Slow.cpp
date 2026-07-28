// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath_axi_stream_if__TC3___ctor_var_reset(Vmilan_datapath_axi_stream_if__TC3* vlSelf);

Vmilan_datapath_axi_stream_if__TC3::Vmilan_datapath_axi_stream_if__TC3() = default;
Vmilan_datapath_axi_stream_if__TC3::~Vmilan_datapath_axi_stream_if__TC3() = default;

void Vmilan_datapath_axi_stream_if__TC3::ctor(Vmilan_datapath__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vmilan_datapath_axi_stream_if__TC3___ctor_var_reset(this);
}

void Vmilan_datapath_axi_stream_if__TC3::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vmilan_datapath_axi_stream_if__TC3::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
