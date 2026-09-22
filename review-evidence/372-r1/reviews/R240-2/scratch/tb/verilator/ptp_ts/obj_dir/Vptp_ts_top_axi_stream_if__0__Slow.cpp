// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

VL_ATTR_COLD void Vptp_ts_top_axi_stream_if___ctor_var_reset(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___ctor_var_reset\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__PVT__clk = 0;
    vlSelf->__PVT__rst_n = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6606742779220347250ull);
}
