// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0;

VL_ATTR_COLD void Vmilan_datapath_axi_stream_if___stl_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___stl_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlWide<10>/*319:0*/ __Vtemp_4;
    // Body
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
}

VL_ATTR_COLD void Vmilan_datapath_axi_stream_if___ctor_var_reset(Vmilan_datapath_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vmilan_datapath_axi_stream_if___ctor_var_reset\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__PVT__clk = 0;
    vlSelf->__PVT__rst_n = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6606742779220347250ull);
    vlSelf->tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11580290079671979871ull);
    vlSelf->tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9634498217090403279ull);
    vlSelf->tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17793882294932938261ull);
    vlSelf->tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15675116905018685246ull);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_96 = 0;
}
