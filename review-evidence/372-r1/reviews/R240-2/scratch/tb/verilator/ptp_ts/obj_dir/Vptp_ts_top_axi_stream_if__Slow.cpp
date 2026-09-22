// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

void Vptp_ts_top_axi_stream_if___ctor_var_reset(Vptp_ts_top_axi_stream_if* vlSelf);

Vptp_ts_top_axi_stream_if::Vptp_ts_top_axi_stream_if() = default;
Vptp_ts_top_axi_stream_if::~Vptp_ts_top_axi_stream_if() = default;

void Vptp_ts_top_axi_stream_if::ctor(Vptp_ts_top__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
    Vptp_ts_top_axi_stream_if___ctor_var_reset(this);
}

void Vptp_ts_top_axi_stream_if::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vptp_ts_top_axi_stream_if::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
