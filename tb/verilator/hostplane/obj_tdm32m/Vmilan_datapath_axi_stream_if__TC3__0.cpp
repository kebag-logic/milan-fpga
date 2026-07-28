// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath_axi_stream_if__TC3___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0(Vmilan_datapath_axi_stream_if__TC3* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if__TC3___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tdest = (7U & vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem
                       [(0x0000001fU & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_rd))]);
    vlSelfRef.tvalid = (((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg) 
                         >> 1U) & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_99));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19 = ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg) 
                                                 & (IData)(vlSelfRef.tvalid));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19) {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18 = 
            (1U & (~ (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_reg)));
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96 = 
            ((~ (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                 >> 8U)) & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg));
    } else {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18 = 0U;
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96 = vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18)
                                                  ? 
                                                 (5U 
                                                  <= (IData)(vlSelfRef.tdest))
                                                  : (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__drop_reg));
}
