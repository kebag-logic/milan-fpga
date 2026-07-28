// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

VL_ATTR_COLD void Vmilan_datapath_axi_stream_if__TC3___stl_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0(Vmilan_datapath_axi_stream_if__TC3* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if__TC3___stl_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tdest = (7U & vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem
                       [(0x0000001fU & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_rd))]);
    vlSelfRef.tvalid = (((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg) 
                         >> 1U) & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_97));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18 = ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg) 
                                                 & (IData)(vlSelfRef.tvalid));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18) {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94 = 
            ((~ (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                 >> 8U)) & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg));
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 = 
            (1U & (~ (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_reg)));
    } else {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94 = vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg;
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 = 0U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17)
                                                  ? 
                                                 (5U 
                                                  <= (IData)(vlSelfRef.tdest))
                                                  : (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg));
}

VL_ATTR_COLD void Vmilan_datapath_axi_stream_if__TC3___ctor_var_reset(Vmilan_datapath_axi_stream_if__TC3* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if__TC3___ctor_var_reset\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__PVT__clk = 0;
    vlSelf->__PVT__rst_n = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11580290079671979871ull);
    vlSelf->tdest = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6208692596641527641ull);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_17 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_18 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_94 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_95 = 0;
}
