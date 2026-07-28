// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.milan_datapath__DOT__aaf_final_mux__DOT__active) 
                        & ((~ (IData)(vlSymsp->TOP.milan_datapath__DOT__aaf_final_mux__DOT__gsel)) 
                           & (IData)(vlSymsp->TOP.milan_datapath__DOT__dpaaf_tready)));
}

extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0;

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlWide<10>/*319:0*/ __Vtemp_4;
    // Body
    vlSelfRef.tvalid = ((4U >= Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                         [vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__queue_grant]) 
                        & ((0U != (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__queue_grant)) 
                           & (((((4U & ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                        << 1U)) | (
                                                   (2U 
                                                    & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg)) 
                                                   | (1U 
                                                      & ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                                         >> 1U)))) 
                                << 2U) | ((2U & (IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg)) 
                                          | (1U & ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U)))) 
                              >> Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                              [vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__queue_grant])));
    vlSelfRef.tkeep = (0x000000ffU & ((IData)(((((QData)((IData)(
                                                                 (0x000000ffU 
                                                                  & vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U]))) 
                                                 << 0x00000020U) 
                                                | (QData)((IData)(
                                                                  ((((0x0000ff00U 
                                                                      & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                                                         << 8U)) 
                                                                     | (0x000000ffU 
                                                                        & vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U])) 
                                                                    << 0x00000010U) 
                                                                   | ((0x0000ff00U 
                                                                       & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                                                          << 8U)) 
                                                                      | (0x000000ffU 
                                                                         & vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U])))))) 
                                               >> (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_87))) 
                                      & (- (IData)(
                                                   (0x27U 
                                                    >= (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_87))))));
    __Vtemp_4[0U] = (IData)((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                              << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))));
    __Vtemp_4[1U] = (IData)(((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))) 
                             >> 0x00000020U));
    __Vtemp_4[2U] = (IData)((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                              << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))));
    __Vtemp_4[3U] = (IData)(((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))) 
                             >> 0x00000020U));
    __Vtemp_4[4U] = (IData)((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                              << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))));
    __Vtemp_4[5U] = (IData)(((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))) 
                             >> 0x00000020U));
    __Vtemp_4[6U] = (IData)((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                              << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))));
    __Vtemp_4[7U] = (IData)(((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))) 
                             >> 0x00000020U));
    __Vtemp_4[8U] = (IData)((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                              << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))));
    __Vtemp_4[9U] = (IData)(((((QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U]))) 
                             >> 0x00000020U));
    vlSelfRef.tdata = ((((QData)((IData)(__Vtemp_4[
                                         (((IData)(0x0000003fU) 
                                           + (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88)) 
                                          >> 5U)])) 
                         << ((0U == (0x0000001fU & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88)))
                              ? 0x00000020U : ((IData)(0x00000040U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88))))) 
                        | (((0U == (0x0000001fU & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88)))
                             ? 0ULL : ((QData)((IData)(__Vtemp_4
                                                       [
                                                       (((IData)(0x0000001fU) 
                                                         + (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88)) 
                                                        >> 5U)])) 
                                       << ((IData)(0x00000020U) 
                                           - (0x0000001fU 
                                              & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88))))) 
                           | ((QData)((IData)(__Vtemp_4
                                              [((IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88) 
                                                >> 5U)])) 
                              >> (0x0000001fU & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88))))) 
                       & (- (QData)((IData)((0x013fU 
                                             >= (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_88))))));
    vlSelfRef.tlast = ((4U >= Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                        [vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__queue_grant]) 
                       & (((((4U & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                    >> 6U)) | ((2U 
                                                & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                                   >> 7U)) 
                                               | (1U 
                                                  & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                                     >> 8U)))) 
                            << 2U) | ((2U & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                             >> 7U)) 
                                      | (1U & (vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                               >> 8U)))) 
                          >> Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                          [vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__queue_grant]));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__rd_ptr_reg)));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__rd_ptr_reg)));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((2U == (IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__axis_tx_rx_ts_switch_rr__DOT__state)) 
                        & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo.tready));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((1U == (IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__axis_tx_rx_ts_switch_rr__DOT__state)) 
                        & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo.tready));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__rd_ptr_reg)));
}

void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg) 
                        & (IData)(vlSymsp->TOP.__VdfgRegularize_h6e95ff9d_0_97));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96 = ((vlSymsp->TOP.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                                  >> 8U) 
                                                 & (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.__VdfgRegularize_h6e95ff9d_0_18));
}
