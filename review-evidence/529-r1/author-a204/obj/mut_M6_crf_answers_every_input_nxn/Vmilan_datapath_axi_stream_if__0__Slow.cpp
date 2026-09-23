// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

VL_ATTR_COLD void Vmilan_datapath_axi_stream_if___ctor_var_reset(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vmilan_datapath_axi_stream_if___ctor_var_reset\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__PVT__clk = 0;
    vlSelf->__PVT__rst_n = 0;
}
