// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

// Parameter definitions for Vsim_KL_mbx_pkg
constexpr VlUnpacked<IData/*31:0*/, 5> Vsim_KL_mbx_pkg::__PVT__MBX_CH_RX_WORDS_TBL_C;
constexpr VlUnpacked<IData/*31:0*/, 5> Vsim_KL_mbx_pkg::__PVT__MBX_CH_TX_WORDS_TBL_C;
constexpr VlUnpacked<IData/*31:0*/, 5> Vsim_KL_mbx_pkg::__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C;
constexpr VlUnpacked<IData/*31:0*/, 15> Vsim_KL_mbx_pkg::__PVT__MBX_TERM_TEST_TBL_C;
constexpr VlUnpacked<IData/*31:0*/, 15> Vsim_KL_mbx_pkg::__PVT__MBX_TERM_OFFSET_TBL_C;
constexpr VlUnpacked<IData/*31:0*/, 15> Vsim_KL_mbx_pkg::__PVT__MBX_TERM_MASK_TBL_C;



Vsim_KL_mbx_pkg::Vsim_KL_mbx_pkg() = default;
Vsim_KL_mbx_pkg::~Vsim_KL_mbx_pkg() = default;

void Vsim_KL_mbx_pkg::ctor(Vsim__Syms* symsp, const char* namep) {
    vlSymsp = symsp;
    vlNamep = strdup(Verilated::catName(vlSymsp->name(), namep));
    // Reset structure values
}

void Vsim_KL_mbx_pkg::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

void Vsim_KL_mbx_pkg::dtor() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
