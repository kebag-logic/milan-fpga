// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

VL_ATTR_COLD void Vptp_ts_top___024root___eval_static(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_static\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mark_frame_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mark_frame_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mark_frame_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet = 1U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet = 1U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged = 0U;
        const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
        VL_SCOPED_RAND_RESET_W(88, vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next, __VscopeHash, 9939359461207149327ull);
    }
    vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__0 = vlSelfRef.gtx_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__gtx_resetn__0 
        = vlSelfRef.gtx_resetn;
    vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__0 = vlSelfRef.axis_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__0 
        = vlSelfRef.axis_resetn;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_enable__0 
        = vlSelfRef.i_ptp_enable;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_incr__0 
        = vlSelfRef.i_ptp_incr;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_adj__0 = vlSelfRef.i_ptp_adj;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_tod_wr__0 
        = vlSelfRef.i_ptp_tod_wr;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_offset__0 
        = vlSelfRef.i_ptp_offset;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_load__0 
        = vlSelfRef.i_ptp_cmd_load;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_adjust__0 
        = vlSelfRef.i_ptp_cmd_adjust;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_snapshot__0 
        = vlSelfRef.i_ptp_cmd_snapshot;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_ingress_lat__0 
        = vlSelfRef.i_ptp_ingress_lat;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_egress_lat__0 
        = vlSelfRef.i_ptp_egress_lat;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tdata__0 
        = vlSelfRef.s_axis_tx_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0 
        = vlSelfRef.s_axis_tx_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tlast__0 
        = vlSelfRef.s_axis_tx_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0 
        = vlSelfRef.s_axis_tx_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_tx_tready__0 
        = vlSelfRef.m_axis_tx_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tdata__0 
        = vlSelfRef.s_axis_rx_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tvalid__0 
        = vlSelfRef.s_axis_rx_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tlast__0 
        = vlSelfRef.s_axis_rx_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tkeep__0 
        = vlSelfRef.s_axis_rx_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_rx_tready__0 
        = vlSelfRef.m_axis_rx_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__ts_m_axis_tready__0 
        = vlSelfRef.ts_m_axis_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__1 = vlSelfRef.axis_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1 = vlSelfRef.gtx_clk;
}

VL_ATTR_COLD void Vptp_ts_top___024root___eval_initial(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_initial\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vptp_ts_top___024root___eval_final(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_final\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vptp_ts_top___024root___eval_phase__stl(Vptp_ts_top___024root* vlSelf);

VL_ATTR_COLD void Vptp_ts_top___024root___eval_settle(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_settle\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vptp_ts_top___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv", 31, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vptp_ts_top___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vptp_ts_top___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vptp_ts_top___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vptp_ts_top___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

VL_ATTR_COLD void Vptp_ts_top___024root___stl_sequent__TOP__0(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___stl_sequent__TOP__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.o_ptp_now = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U])) 
                            << 0x00000028U) | (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U])) 
                                                << 8U) 
                                               | ((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U])) 
                                                  >> 0x00000018U)));
    vlSelfRef.o_ptp_tod_rd = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg;
    vlSelfRef.o_ptp_tod_rd_valid = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg;
    vlSelfRef.o_tx_ts_ready = vlSelfRef.ptp_ts_top__DOT__tx_ts_ready_r;
    vlSelfRef.m_axis_tx_tdata = vlSelfRef.s_axis_tx_tdata;
    vlSelfRef.s_axis_tx_tready = vlSelfRef.m_axis_tx_tready;
    vlSelfRef.m_axis_tx_tvalid = vlSelfRef.s_axis_tx_tvalid;
    vlSelfRef.m_axis_tx_tlast = vlSelfRef.s_axis_tx_tlast;
    vlSelfRef.m_axis_tx_tkeep = vlSelfRef.s_axis_tx_tkeep;
    vlSelfRef.m_axis_rx_tdata = vlSelfRef.s_axis_rx_tdata;
    vlSelfRef.s_axis_rx_tready = vlSelfRef.m_axis_rx_tready;
    vlSelfRef.m_axis_rx_tvalid = vlSelfRef.s_axis_rx_tvalid;
    vlSelfRef.m_axis_rx_tlast = vlSelfRef.s_axis_rx_tlast;
    vlSelfRef.m_axis_rx_tkeep = vlSelfRef.s_axis_rx_tkeep;
    vlSelfRef.ts_m_axis_tdata = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                  << 0x00000020U) | (QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][0U])));
    vlSelfRef.ts_m_axis_tlast = (1U & (vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                       >> 8U));
    vlSelfRef.ts_m_axis_tkeep = (0x000000ffU & vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][2U]);
    vlSelfRef.ts_m_axis_tvalid = (1U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U));
    vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid = 0U;
    vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata = 0ULL;
    vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep = 0U;
    vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast = 0U;
    if ((1U == (IData)(vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state))) {
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid 
            = (1U & ((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata 
            = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep 
            = (0x000000ffU & vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U]);
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast 
            = (1U & (vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                     >> 8U));
    } else if ((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state))) {
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid 
            = (1U & ((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata 
            = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep 
            = (0x000000ffU & vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U]);
        vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast 
            = (1U & (vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                     >> 8U));
    }
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc 
        = ((IData)(vlSelfRef.s_axis_tx_tvalid) & (IData)(vlSelfRef.m_axis_tx_tready));
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc 
        = ((IData)(vlSelfRef.s_axis_rx_tvalid) & (IData)(vlSelfRef.m_axis_rx_tready));
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push 
        = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc) 
                & (IData)(vlSelfRef.s_axis_tx_tlast)) 
               & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match)) 
             & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)));
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push 
        = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc) 
                & (IData)(vlSelfRef.s_axis_rx_tlast)) 
               & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match)) 
             & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf);

VL_ATTR_COLD bool Vptp_ts_top___024root___eval_phase__stl(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_phase__stl\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[0U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vptp_ts_top___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vptp_ts_top___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vptp_ts_top___024root___stl_sequent__TOP__0(vlSelf);
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_rx));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered));
            }
        }
    }
    return (__VstlExecute);
}

bool Vptp_ts_top___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vptp_ts_top___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( gtx_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( gtx_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( axis_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( i_ptp_enable)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( i_ptp_incr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( i_ptp_adj)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( i_ptp_tod_wr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( i_ptp_offset)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( i_ptp_cmd_load)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( i_ptp_cmd_adjust)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( i_ptp_cmd_snapshot)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( i_ptp_ingress_lat)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( i_ptp_egress_lat)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( s_axis_tx_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @( s_axis_tx_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000010U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 16 is active: @( s_axis_tx_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000011U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 17 is active: @( s_axis_tx_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000012U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 18 is active: @( m_axis_tx_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000013U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 19 is active: @( s_axis_rx_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000014U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 20 is active: @( s_axis_rx_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000015U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 21 is active: @( s_axis_rx_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000016U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 22 is active: @( s_axis_rx_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000017U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 23 is active: @( m_axis_rx_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000018U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 24 is active: @( ts_m_axis_tready)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vptp_ts_top___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vptp_ts_top___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge gtx_clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vptp_ts_top___024root___ctor_var_reset(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___ctor_var_reset\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->gtx_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5173468789992344027ull);
    vlSelf->gtx_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2680759800423739578ull);
    vlSelf->axis_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6077951788264469019ull);
    vlSelf->axis_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13353824713052781882ull);
    vlSelf->i_ptp_enable = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 617811767470941369ull);
    vlSelf->i_ptp_incr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5984934072929749063ull);
    vlSelf->i_ptp_adj = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16217958732550772110ull);
    vlSelf->i_ptp_tod_wr = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9492482942880857687ull);
    vlSelf->i_ptp_offset = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7653796669312421526ull);
    vlSelf->i_ptp_cmd_load = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16740898758829986270ull);
    vlSelf->i_ptp_cmd_adjust = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15217503413610063673ull);
    vlSelf->i_ptp_cmd_snapshot = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 834930734752836857ull);
    vlSelf->i_ptp_ingress_lat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9901933367592091047ull);
    vlSelf->i_ptp_egress_lat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14978227296342037052ull);
    vlSelf->o_ptp_tod_rd = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17890953458571362877ull);
    vlSelf->o_ptp_tod_rd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13852632076858666399ull);
    vlSelf->o_tx_ts_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5242944405000914824ull);
    vlSelf->o_ptp_now = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11465470834979412285ull);
    vlSelf->s_axis_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16415501603384742319ull);
    vlSelf->s_axis_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11371248574670827460ull);
    vlSelf->s_axis_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1739555264497535737ull);
    vlSelf->s_axis_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6321668314625288019ull);
    vlSelf->s_axis_tx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3157636447565749703ull);
    vlSelf->m_axis_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1499661993762382952ull);
    vlSelf->m_axis_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7351300163871840319ull);
    vlSelf->m_axis_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10006263958730874084ull);
    vlSelf->m_axis_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10840558317423350651ull);
    vlSelf->m_axis_tx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13037939374526829503ull);
    vlSelf->s_axis_rx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15179552465365695301ull);
    vlSelf->s_axis_rx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1042852775941457034ull);
    vlSelf->s_axis_rx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 74960513163540353ull);
    vlSelf->s_axis_rx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2402007813527927649ull);
    vlSelf->s_axis_rx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1149992855450969255ull);
    vlSelf->m_axis_rx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 259829326048321033ull);
    vlSelf->m_axis_rx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 48968215238118370ull);
    vlSelf->m_axis_rx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4361656292483556361ull);
    vlSelf->m_axis_rx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3101536001143430368ull);
    vlSelf->m_axis_rx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3749104770080218473ull);
    vlSelf->ts_m_axis_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8627880065411700777ull);
    vlSelf->ts_m_axis_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17968524089391652857ull);
    vlSelf->ts_m_axis_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 102550603530795051ull);
    vlSelf->ts_m_axis_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 388345528443562415ull);
    vlSelf->ts_m_axis_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9729176469426593541ull);
    vlSelf->ptp_ts_top__DOT__tx_ts_ready_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8052852275738517252ull);
    vlSelf->ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep = 0;
    vlSelf->ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast = 0;
    vlSelf->ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid = 0;
    vlSelf->ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata = 0;
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem[__Vi0], __VscopeHash, 1014027823596035281ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 18399109978647920801ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__rx_ts_buffer__DOT__mem[__Vi0], __VscopeHash, 1156538141290228715ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 18222905914980321404ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__tx_ts_buffer__DOT__mem[__Vi0], __VscopeHash, 17115932160352325896ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 4546202230215998477ull);
    }
    vlSelf->ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7116419387560650128ull);
    vlSelf->ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3615295267462141405ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 6239521590224130606ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_sop = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5154768304767153748ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18233816864799245410ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18408730481605698763ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9904424662065677060ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5132869410822097296ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3188206966121943014ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14448004158424067255ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11253733757203581029ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16113283499959507767ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7037916480547808472ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4967881472814897748ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14051724558980646004ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16175866742331702732ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15353389884822779935ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13691884272966866999ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1644428980824715190ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14943944244806688243ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13999378218761904748ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 1641808559353667572ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_sop = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6753243955893880547ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3226486890371739909ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14169298857516683119ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13117524981916043630ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15681175883706383236ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12210693080244243162ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9938238492665855926ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11808166426127387246ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13010802619446312115ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7176862938781126524ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9982304592243685342ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10216732586240426960ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17643881956355937904ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18080153132824103962ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12704728869150803899ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2256203551579711433ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1332911773837510459ull);
    vlSelf->ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10302661986838044500ull);
    VL_SCOPED_RAND_RESET_W(88, vlSelf->ptp_ts_top__DOT__ts_counter__DOT__acc, __VscopeHash, 15026287820270692410ull);
    vlSelf->ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7913476520876313401ull);
    vlSelf->ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13903563612398078058ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__en_meta = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16877727060604190452ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__en_sync = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 851093700376726948ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__incr_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16484831627614683721ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__incr_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14782963166040552370ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__adj_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6297025132565863160ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__adj_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11451682201266429626ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__load_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12894960071370454206ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 140763781419383091ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6414024181257168356ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__load_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11377076549333750407ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__adj_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9216662130965256040ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__snap_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3592094488416495118ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1118543044040180214ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__offset_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8954303945825316453ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__load_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6941226726631279209ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__adj_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8302808738674237486ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__snap_val_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13212368032586035932ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11097070054814858033ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15020665433669172869ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12773244527840421472ull);
    vlSelf->ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7536057825649960057ull);
    VL_ZERO_RESET_W(88, vlSelf->__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc);
    vlSelf->__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s = 0;
    vlSelf->__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_enable__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_incr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_adj__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_tod_wr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_offset__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_cmd_load__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_cmd_adjust__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_cmd_snapshot__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_ingress_lat__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ptp_egress_lat__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_tx_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_rx_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_rx_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_rx_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_rx_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_rx_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ts_m_axis_tready__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
