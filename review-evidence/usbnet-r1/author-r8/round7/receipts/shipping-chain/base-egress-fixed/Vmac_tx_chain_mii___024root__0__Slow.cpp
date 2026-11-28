// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmac_tx_chain_mii.h for the primary calling header

#include "Vmac_tx_chain_mii__pch.h"

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_static(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_static\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.mac_tx_chain_mii__DOT__eth_tx_rst = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__macsys_rst = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__macdp_rst = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_en = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_data = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg = 0xffffffffU;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt = 3U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_last = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_last_be = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_readable = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[0U] = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[1U] = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl0_rst1 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl2_rst1 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl3_rst1 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl4_rst1 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl00 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl01 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl10 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl60 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl61 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl70 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71 = 0U;
    }
    vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__0 = vlSelfRef.__VprimaryPorts.sys_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__sys_rst__0 = vlSelfRef.__VprimaryPorts.sys_rst;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__0 = vlSelfRef.__VprimaryPorts.dp_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_rst__0 = vlSelfRef.__VprimaryPorts.dp_rst;
    vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__0 
        = vlSelfRef.__VprimaryPorts.eth_tx_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__eth_rx_clk__0 
        = vlSelfRef.__VprimaryPorts.eth_rx_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__eth_phy_rst__0 
        = vlSelfRef.__VprimaryPorts.eth_phy_rst;
    vlSelfRef.__Vtrigprevexpr___TOP__reinit__0 = vlSelfRef.__VprimaryPorts.reinit;
    vlSelfRef.__Vtrigprevexpr___TOP__eth_rst__0 = vlSelfRef.__VprimaryPorts.eth_rst;
    vlSelfRef.__Vtrigprevexpr___TOP__loopback__0 = vlSelfRef.__VprimaryPorts.loopback;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_tdata__0 = vlSelfRef.__VprimaryPorts.dp_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_tkeep__0 = vlSelfRef.__VprimaryPorts.dp_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_tvalid__0 = vlSelfRef.__VprimaryPorts.dp_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_tlast__0 = vlSelfRef.__VprimaryPorts.dp_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__1 
        = vlSelfRef.__VprimaryPorts.eth_tx_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__1 = vlSelfRef.__VprimaryPorts.dp_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1 = vlSelfRef.__VprimaryPorts.sys_clk;
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_initial(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_initial\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_initial__TOP
        vlSelfRef.__VprimaryPorts.gmii_tx_er = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vmac_tx_chain_mii___024root___trigger_anySet__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &in);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___stl_comb__TOP__0(Vmac_tx_chain_mii___024root* vlSelf);

VL_ATTR_COLD bool Vmac_tx_chain_mii___024root___eval_stl(Vmac_tx_chain_mii___024root* vlSelf, ::CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_stl\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VstlExecute;
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (::IData)((::IData)(firstIteration)));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmac_tx_chain_mii___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vmac_tx_chain_mii___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_body__stl
            if ((((1ULL & vlSelfRef.__VstlTriggered[0U])) != 0ULL)) {
                Vmac_tx_chain_mii___024root___stl_comb__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__stl(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__stl\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vmac_tx_chain_mii___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__ico(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__ico\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vmac_tx_chain_mii___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__act(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__act\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vmac_tx_chain_mii___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__nba(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__nba\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vmac_tx_chain_mii___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__obs(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__obs\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__react(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_dump_triggers__react\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_final(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_final\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (::IData)(Vmac_tx_chain_mii___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vmac_tx_chain_mii___024root___trigger_anySet__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___trigger_anySet__stl\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((::IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___stl_comb__TOP__0(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___stl_comb__TOP__0\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_cdc_source_source_last;
    mac_tx_chain_mii__DOT__tx_cdc_source_source_last = 0;
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_converter_source_last;
    mac_tx_chain_mii__DOT__tx_converter_source_last = 0;
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be;
    mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be = 0;
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last;
    mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last = 0;
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_preamble_source_valid;
    mac_tx_chain_mii__DOT__tx_preamble_source_valid = 0;
    ::CData/*0:0*/ mac_tx_chain_mii__DOT__tx_preamble_source_last;
    mac_tx_chain_mii__DOT__tx_preamble_source_last = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1539;
    __Vdfg_Regularize_1539 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1540;
    __Vdfg_Regularize_1540 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1542;
    __Vdfg_Regularize_1542 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1543;
    __Vdfg_Regularize_1543 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1544;
    __Vdfg_Regularize_1544 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1545;
    __Vdfg_Regularize_1545 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1546;
    __Vdfg_Regularize_1546 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1555;
    __Vdfg_Regularize_1555 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1557;
    __Vdfg_Regularize_1557 = 0;
    ::CData/*1:0*/ __Vdfg_Regularize_1563;
    __Vdfg_Regularize_1563 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1566;
    __Vdfg_Regularize_1566 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1568;
    __Vdfg_Regularize_1568 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1570;
    __Vdfg_Regularize_1570 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1591;
    __Vdfg_Regularize_1591 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1592;
    __Vdfg_Regularize_1592 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1601;
    __Vdfg_Regularize_1601 = 0;
    ::CData/*1:0*/ __Vdfg_Regularize_1603;
    __Vdfg_Regularize_1603 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1604;
    __Vdfg_Regularize_1604 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_1605;
    __Vdfg_Regularize_1605 = 0;
    // Body
    vlSelfRef.__VprimaryPorts.maceth_tx_rst = vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1;
    vlSelfRef.__VprimaryPorts.gmii_tx_en = vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_en;
    vlSelfRef.__VprimaryPorts.gmii_tx_data = vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_data;
    vlSelfRef.__VprimaryPorts.phy_sink_ready = vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reset = 
        (1U & (~ ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
                  | (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)))));
    vlSelfRef.__Vdfg_Regularize_1579 = (7U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count));
    vlSelfRef.__Vdfg_Regularize_1562 = (3U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                               >> 0x0000000cU) 
                                              ^ (((2U 
                                                   & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                      >> 1U)) 
                                                  | (1U 
                                                     & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                        >> 3U))) 
                                                 ^ 
                                                 (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x0000001cU))));
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid 
        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable));
    vlSelfRef.__VprimaryPorts.phy_sink_data = (0x000000ffU 
                                               & (((1U 
                                                    == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
                                                    ? 
                                                   ((4U 
                                                     & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count))
                                                     ? 
                                                    ((2U 
                                                      & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count))
                                                      ? 
                                                     ((1U 
                                                       & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count))
                                                       ? 0xd5U
                                                       : 0x55U)
                                                      : 0x55U)
                                                     : 0x55U)
                                                    : 
                                                   ((1U 
                                                     == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
                                                     ? (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data)
                                                     : 
                                                    (((0U 
                                                       == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt))
                                                       ? 
                                                      (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet 
                                                       >> 0x00000018U)
                                                       : 
                                                      ((1U 
                                                        == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt))
                                                        ? 
                                                       (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet 
                                                        >> 0x00000010U)
                                                        : 
                                                       ((2U 
                                                         == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt))
                                                         ? 
                                                        (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet 
                                                         >> 8U)
                                                         : vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet))) 
                                                     & (- (::IData)(
                                                                    (2U 
                                                                     == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))))))) 
                                                  & (- (::IData)(
                                                                 (1U 
                                                                  & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state)))))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q) 
           != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl61));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready 
        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
           & ((0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)) 
              & (9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0))));
    vlSelfRef.__VprimaryPorts.dp_tready = (((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q) 
                                                   >> 4U)) 
                                            == (1U 
                                                & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71) 
                                                   >> 4U))) 
                                           | (((1U 
                                                & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q) 
                                                   >> 3U)) 
                                               == (1U 
                                                   & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71) 
                                                      >> 3U))) 
                                              | ((7U 
                                                  & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q)) 
                                                 != 
                                                 (7U 
                                                  & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71)))));
    __Vdfg_Regularize_1603 = (3U & ((- (::IData)((1U 
                                                  & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                     >> 1U)))) 
                                    ^ (- (::IData)(
                                                   (1U 
                                                    & (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                       >> 0x0000001eU))))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable) 
           & (((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q) 
                      >> 5U)) == (1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11) 
                                        >> 5U))) | 
              (((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q) 
                       >> 4U)) == (1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11) 
                                         >> 4U))) | 
               ((0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q)) 
                != (0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11))))));
    __Vdfg_Regularize_1604 = (1U & (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                     >> 5U) ^ VL_REDXOR_32(
                                                           (0x06000000U 
                                                            & vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg))));
    __Vdfg_Regularize_1563 = (3U & ((- (::IData)((1U 
                                                  & (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                     >> 0x00000018U)))) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 5U)));
    __Vdfg_Regularize_1568 = (1U & (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                     >> 4U) ^ VL_REDXOR_32(
                                                           (0x0c000000U 
                                                            & vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg))));
    __Vdfg_Regularize_1542 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001aU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 5U)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q) 
           != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl01));
    __Vdfg_Regularize_1543 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001bU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 4U)));
    __Vdfg_Regularize_1545 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001eU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 1U)));
    __Vdfg_Regularize_1544 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001dU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 2U)));
    mac_tx_chain_mii__DOT__tx_cdc_source_source_last 
        = (1U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                 [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                 >> 0x00000011U));
    __Vdfg_Regularize_1555 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001cU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 3U)));
    __Vdfg_Regularize_1539 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001fU) 
                                    ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data)));
    vlSelfRef.__Vdfg_Regularize_1582 = ((1U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
                                        & (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data 
        = ((4U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
            ? ((2U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                ? ((1U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                    ? ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 6U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 1U)) 
                                                  | (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                     [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][1U] 
                                                     >> 0x00000018U)))
                    : ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 5U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 2U)) 
                                                  | (0x000000ffU 
                                                     & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                        [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][1U] 
                                                        >> 0x00000010U)))))
                : ((1U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                    ? ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 4U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 3U)) 
                                                  | (0x000000ffU 
                                                     & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                        [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][1U] 
                                                        >> 8U))))
                    : ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 3U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 4U)) 
                                                  | (0x000000ffU 
                                                     & vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                     [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][1U])))))
            : ((2U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                ? ((1U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                    ? ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 2U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 5U)) 
                                                  | (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                     [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][0U] 
                                                     >> 0x00000018U)))
                    : ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       >> 1U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 6U)) 
                                                  | (0x000000ffU 
                                                     & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                        [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][0U] 
                                                        >> 0x00000010U)))))
                : ((1U & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                    ? ((0x00000200U & vlSelfRef.mac_tx_chain_mii__DOT__storage
                        [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U]) 
                       | ((0x00000100U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                          [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                          << 7U)) | 
                          (0x000000ffU & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                          [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][0U] 
                                          >> 8U))))
                    : ((0x00000200U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                       [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                       << 1U)) | ((0x00000100U 
                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                      [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                                                      << 8U)) 
                                                  | (0x000000ffU 
                                                     & vlSelfRef.mac_tx_chain_mii__DOT__storage
                                                     [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][0U]))))));
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid 
        = ((9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary 
        = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary) 
                          + ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable) 
                             & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable)) 
                                | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready)))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce 
        = ((::IData)(vlSelfRef.__VprimaryPorts.dp_tvalid) 
           & (::IData)(vlSelfRef.__VprimaryPorts.dp_tready));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_next_binary 
        = (0x0000003fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_binary) 
                          + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce)));
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_syncfifo_re 
        = (((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_readable)) 
            | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce)) 
           & (0U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)));
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_source_ready 
        = ((vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[2U] 
            >> 0x00000011U) & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_source_valid 
        = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid));
    vlSelfRef.__Vdfg_Regularize_1589 = (1U & ((::IData)(__Vdfg_Regularize_1543) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x00000011U) 
                                                 ^ (::IData)(__Vdfg_Regularize_1542))));
    __Vdfg_Regularize_1591 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x00000018U) 
                                    ^ (::IData)(__Vdfg_Regularize_1545)));
    vlSelfRef.__Vdfg_Regularize_1583 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                               >> 0x00000017U) 
                                              ^ (::IData)(__Vdfg_Regularize_1544)));
    __Vdfg_Regularize_1557 = ((::IData)(__Vdfg_Regularize_1545) 
                              ^ (::IData)(__Vdfg_Regularize_1544));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last 
        = ((::IData)(mac_tx_chain_mii__DOT__tx_cdc_source_source_last) 
           & (7U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux)));
    __Vdfg_Regularize_1546 = ((::IData)(__Vdfg_Regularize_1544) 
                              ^ (::IData)(__Vdfg_Regularize_1555));
    __Vdfg_Regularize_1540 = ((::IData)(__Vdfg_Regularize_1555) 
                              ^ (::IData)(__Vdfg_Regularize_1543));
    vlSelfRef.__Vdfg_Regularize_1584 = (1U & ((::IData)(__Vdfg_Regularize_1539) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x00000016U) 
                                                 ^ (::IData)(__Vdfg_Regularize_1555))));
    vlSelfRef.__Vdfg_Regularize_1593 = (1U & ((::IData)(__Vdfg_Regularize_1539) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x0000000bU) 
                                                 ^ (::IData)(__Vdfg_Regularize_1543))));
    vlSelfRef.__Vdfg_Regularize_1585 = (1U & ((::IData)(__Vdfg_Regularize_1539) 
                                              ^ ((::IData)(__Vdfg_Regularize_1545) 
                                                 ^ 
                                                 ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                   >> 0x00000015U) 
                                                  ^ (::IData)(__Vdfg_Regularize_1543)))));
    vlSelfRef.__Vdfg_Regularize_1594 = (1U & ((::IData)(__Vdfg_Regularize_1539) 
                                              ^ ((::IData)(__Vdfg_Regularize_1545) 
                                                 ^ 
                                                 ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                   >> 0x0000000aU) 
                                                  ^ (::IData)(__Vdfg_Regularize_1542)))));
    __Vdfg_Regularize_1601 = ((::IData)(__Vdfg_Regularize_1539) 
                              ^ (::IData)(__Vdfg_Regularize_1544));
    __Vdfg_Regularize_1570 = (1U & ((::IData)(__Vdfg_Regularize_1604) 
                                    ^ (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                        >> 6U) ^ (::IData)(__Vdfg_Regularize_1539))));
    __Vdfg_Regularize_1566 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x00000019U) 
                                    ^ (::IData)(__Vdfg_Regularize_1539)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_last 
        = ((0U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt)) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_1582));
    mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be 
        = (1U & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state)) 
                 & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
                    >> 8U)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end 
        = ((::IData)(mac_tx_chain_mii__DOT__tx_cdc_source_source_last) 
           & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
              >> 8U));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
            ? (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)
            : (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)));
    mac_tx_chain_mii__DOT__tx_preamble_source_valid 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
           | ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid) 
              & (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary 
        = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary) 
                          + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce)));
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re 
        = (((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable)) 
            | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_source_ready)) 
           & (0U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)));
    vlSelfRef.__Vdfg_Regularize_1571 = (::IData)((((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                   >> 7U) 
                                                  ^ (::IData)(__Vdfg_Regularize_1591)));
    __Vdfg_Regularize_1592 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x00000019U) 
                                    ^ (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                        >> 6U) ^ (::IData)(__Vdfg_Regularize_1591))));
    vlSelfRef.__Vdfg_Regularize_1586 = (1U & ((::IData)(__Vdfg_Regularize_1557) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x00000014U) 
                                                 ^ (::IData)(__Vdfg_Regularize_1542))));
    vlSelfRef.__Vdfg_Regularize_1595 = (1U & (((::IData)(__Vdfg_Regularize_1557) 
                                               ^ VL_REDXOR_32(
                                                              (0x02000200U 
                                                               & vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg))) 
                                              ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                 >> 6U)));
    vlSelfRef.__Vdfg_Regularize_1596 = (1U & (((::IData)(__Vdfg_Regularize_1546) 
                                               ^ VL_REDXOR_32(
                                                              (0x01000100U 
                                                               & vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg))) 
                                              ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                 >> 7U)));
    vlSelfRef.__Vdfg_Regularize_1600 = (1U & ((::IData)(__Vdfg_Regularize_1546) 
                                              ^ ((::IData)(__Vdfg_Regularize_1604) 
                                                 ^ 
                                                 (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                   >> 6U) 
                                                  ^ 
                                                  (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                   >> 1U)))));
    vlSelfRef.__Vdfg_Regularize_1598 = (1U & ((::IData)(__Vdfg_Regularize_1539) 
                                              ^ ((::IData)(__Vdfg_Regularize_1545) 
                                                 ^ 
                                                 ((::IData)(__Vdfg_Regularize_1540) 
                                                  ^ 
                                                  ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                    >> 6U) 
                                                   ^ (::IData)(__Vdfg_Regularize_1542))))));
    vlSelfRef.__Vdfg_Regularize_1597 = (1U & ((::IData)(__Vdfg_Regularize_1601) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 7U) 
                                                 ^ (::IData)(__Vdfg_Regularize_1540))));
    vlSelfRef.__Vdfg_Regularize_1564 = (3U & ((- (::IData)(
                                                           (1U 
                                                            & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                               >> 7U)))) 
                                              ^ (((2U 
                                                   & (((::IData)(__Vdfg_Regularize_1540) 
                                                       ^ 
                                                       ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                         >> 0x00000019U) 
                                                        ^ vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg)) 
                                                      << 1U)) 
                                                  | ((::IData)(__Vdfg_Regularize_1601) 
                                                     ^ (::IData)(__Vdfg_Regularize_1568))) 
                                                 ^ (::IData)(__Vdfg_Regularize_1563))));
    vlSelfRef.__Vdfg_Regularize_1590 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                               >> 0x00000010U) 
                                              ^ (::IData)(__Vdfg_Regularize_1570)));
    vlSelfRef.__Vdfg_Regularize_1602 = ((::IData)(__Vdfg_Regularize_1557) 
                                        ^ ((::IData)(__Vdfg_Regularize_1555) 
                                           ^ (::IData)(__Vdfg_Regularize_1570)));
    vlSelfRef.__Vdfg_Regularize_1565 = (3U & ((- (::IData)(
                                                           (1U 
                                                            & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                               >> 7U)))) 
                                              ^ ((::IData)(__Vdfg_Regularize_1563) 
                                                 ^ 
                                                 (((((::IData)(__Vdfg_Regularize_1546) 
                                                     ^ 
                                                     ((::IData)(__Vdfg_Regularize_1543) 
                                                      ^ (::IData)(__Vdfg_Regularize_1566))) 
                                                    << 1U) 
                                                   | (1U 
                                                      & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                          >> 0x0000001aU) 
                                                         ^ (::IData)(__Vdfg_Regularize_1540)))) 
                                                  ^ (::IData)(__Vdfg_Regularize_1603)))));
    vlSelfRef.__Vdfg_Regularize_1567 = (1U & (((::IData)(__Vdfg_Regularize_1568) 
                                               ^ VL_REDXOR_8(
                                                             (0x60U 
                                                              & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data)))) 
                                              ^ (::IData)(__Vdfg_Regularize_1566)));
    __Vdfg_Regularize_1605 = (1U & (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                     >> 6U) ^ (::IData)(__Vdfg_Regularize_1566)));
    mac_tx_chain_mii__DOT__tx_preamble_source_last 
        = ((2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
           & ((1U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
              & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_last)));
    mac_tx_chain_mii__DOT__tx_converter_source_last 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end) 
           | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last));
    vlSelfRef.__VprimaryPorts.phy_sink_valid = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state)) 
                                                & (::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_valid));
    vlSelfRef.__Vdfg_Regularize_1588 = (1U & ((::IData)(__Vdfg_Regularize_1540) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x00000012U) 
                                                 ^ (::IData)(vlSelfRef.__Vdfg_Regularize_1571))));
    vlSelfRef.__Vdfg_Regularize_1572 = (3U & ((- (::IData)(
                                                           (1U 
                                                            & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                               >> 7U)))) 
                                              ^ ((((::IData)(__Vdfg_Regularize_1592) 
                                                   << 1U) 
                                                  | (1U 
                                                     & (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                        >> 0x00000018U))) 
                                                 ^ 
                                                 (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x0000000eU))));
    vlSelfRef.__Vdfg_Regularize_1556 = (7U & (((4U 
                                                & (((::IData)(__Vdfg_Regularize_1546) 
                                                    ^ 
                                                    ((::IData)(__Vdfg_Regularize_1542) 
                                                     ^ 
                                                     ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                       >> 4U) 
                                                      ^ (::IData)(__Vdfg_Regularize_1592)))) 
                                                   << 2U)) 
                                               | (((2U 
                                                    & (((::IData)(__Vdfg_Regularize_1540) 
                                                        ^ 
                                                        VL_REDXOR_32(
                                                                     (0x02000008U 
                                                                      & vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg))) 
                                                       << 1U)) 
                                                   | (1U 
                                                      & ((::IData)(__Vdfg_Regularize_1544) 
                                                         ^ 
                                                         ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                           >> 2U) 
                                                          ^ (::IData)(__Vdfg_Regularize_1568))))) 
                                                  ^ (::IData)(__Vdfg_Regularize_1563))) 
                                              ^ (- (::IData)(
                                                             (1U 
                                                              & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                                 >> 7U))))));
    vlSelfRef.__Vdfg_Regularize_1599 = (1U & ((::IData)(__Vdfg_Regularize_1557) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 5U) 
                                                 ^ (::IData)(vlSelfRef.__Vdfg_Regularize_1567))));
    vlSelfRef.__Vdfg_Regularize_1587 = (1U & ((::IData)(__Vdfg_Regularize_1546) 
                                              ^ ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                  >> 0x00000013U) 
                                                 ^ (::IData)(__Vdfg_Regularize_1605))));
    vlSelfRef.__Vdfg_Regularize_1569 = (3U & ((- (::IData)(
                                                           (1U 
                                                            & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                               >> 7U)))) 
                                              ^ ((- (::IData)(
                                                              (1U 
                                                               & (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                                  >> 0x00000018U)))) 
                                                 ^ 
                                                 ((((::IData)(__Vdfg_Regularize_1570) 
                                                    << 1U) 
                                                   | (::IData)(__Vdfg_Regularize_1605)) 
                                                  ^ (::IData)(__Vdfg_Regularize_1603)))));
    vlSelfRef.__VprimaryPorts.phy_sink_last = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state)) 
                                               & (::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_last));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready = 0U;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value = 0U;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value_ce = 0U;
    if (vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state) {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state = 1U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value 
            = (0x0000000fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter) 
                              - (::IData)(1U)));
        vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value_ce = 1U;
        if ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter))) {
            vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state = 0U;
        }
    } else {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready 
            = vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux;
        if ((((::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_valid) 
              & (::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_last)) 
             & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready))) {
            vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value = 0x0cU;
            vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value_ce = 1U;
            vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state = 1U;
        }
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_ready 
        = ((1U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
           & ((2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
               ? (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready)
               : (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_sink_ready 
        = (1U & ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
                  ? (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_ready)
                  : (~ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid) 
                        | (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))))));
    vlSelfRef.__Vdfg_Regularize_1578 = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid) 
                                        & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_ready));
    vlSelfRef.__Vdfg_Regularize_1581 = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_last) 
                                        & (::IData)(vlSelfRef.__Vdfg_Regularize_1578));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_ready 
        = (1U & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)) 
                 | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_sink_ready)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_1581));
    mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last = 0U;
    if (vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state) {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state = 1U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_last_be_last_handler_sink_ready = 1U;
        if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_source_valid) 
             & (::IData)(mac_tx_chain_mii__DOT__tx_converter_source_last))) {
            vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state = 0U;
        }
    } else {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_last_be_last_handler_sink_ready 
            = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state)) 
               & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_ready));
        mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last 
            = (1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
                     >> 8U));
        if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_source_valid) 
             & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_last_be_last_handler_sink_ready))) {
            if (((::IData)(mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last) 
                 & (~ (::IData)(mac_tx_chain_mii__DOT__tx_converter_source_last)))) {
                vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state = 1U;
            }
        }
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_ready 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop) 
           | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_last_be_last_handler_sink_ready));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_last = 0U;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be = 0U;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value = 0U;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = 0U;
    if (vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state) {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state = 1U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_valid = 1U;
        if ((0x003bU <= (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter))) {
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be = 1U;
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_last = 1U;
        }
        if (vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_ready) {
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value 
                = (0x0000ffffU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter)));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = 1U;
            if ((0x003bU <= (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter))) {
                vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value = 0U;
                vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = 1U;
                vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state = 0U;
            }
        }
    } else {
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_valid 
            = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state)) 
               & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_source_valid));
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_last 
            = mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be 
            = mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be;
        if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_valid) 
             & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_ready))) {
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value 
                = (0x0000ffffU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter)));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = 1U;
            if (mac_tx_chain_mii__DOT__tx_last_be_last_handler_source_last) {
                if ((0x003bU <= (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter))) {
                    if (((0x003bU == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter)) 
                         & (1U > (::IData)(mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be)))) {
                        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be = 1U;
                    } else {
                        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value = 0U;
                        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = 1U;
                    }
                } else {
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_last = 0U;
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be = 0U;
                    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state = 1U;
                }
            }
        }
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary 
        = (0x0000003fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_binary) 
                          + ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid) 
                             & ((7U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux)) 
                                & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_ready)))));
}

bool Vmac_tx_chain_mii___024root___trigger_anySet__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (::IData)(Vmac_tx_chain_mii___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( sys_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( sys_rst)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( dp_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( dp_rst)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( eth_tx_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( eth_rx_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( eth_phy_rst)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( reinit)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( eth_rst)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( loopback)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( dp_tdata)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( dp_tkeep)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( dp_tvalid)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( dp_tlast)\n");
    }
    if ((1U & (::IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vmac_tx_chain_mii___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (::IData)(Vmac_tx_chain_mii___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge eth_tx_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge dp_clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(posedge sys_clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmac_tx_chain_mii___024root___ctor_var_reset(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___ctor_var_reset\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__VprimaryPorts.sys_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7302336598091101382ull);
    vlSelf->__VprimaryPorts.sys_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10947334754268556250ull);
    vlSelf->__VprimaryPorts.dp_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4650995985143171785ull);
    vlSelf->__VprimaryPorts.dp_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15593781832980121056ull);
    vlSelf->__VprimaryPorts.eth_tx_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17071025718643962146ull);
    vlSelf->__VprimaryPorts.eth_rx_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9405710659758061796ull);
    vlSelf->__VprimaryPorts.eth_phy_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12857751378808463373ull);
    vlSelf->__VprimaryPorts.reinit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9480519976459974295ull);
    vlSelf->__VprimaryPorts.eth_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 552569885826598545ull);
    vlSelf->__VprimaryPorts.loopback = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16500989605875034370ull);
    vlSelf->__VprimaryPorts.dp_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14479072077966796704ull);
    vlSelf->__VprimaryPorts.dp_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16161050012122279814ull);
    vlSelf->__VprimaryPorts.dp_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16795380272023922430ull);
    vlSelf->__VprimaryPorts.dp_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9114185845850022553ull);
    vlSelf->__VprimaryPorts.dp_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13084276106890499742ull);
    vlSelf->__VprimaryPorts.gmii_tx_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8315225809664225203ull);
    vlSelf->__VprimaryPorts.gmii_tx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14777442747820233388ull);
    vlSelf->__VprimaryPorts.gmii_tx_er = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11344467775957395112ull);
    vlSelf->__VprimaryPorts.phy_sink_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2063828136341495479ull);
    vlSelf->__VprimaryPorts.phy_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10996340423232676186ull);
    vlSelf->__VprimaryPorts.phy_sink_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10919506363590101931ull);
    vlSelf->__VprimaryPorts.phy_sink_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9021133576213741080ull);
    vlSelf->__VprimaryPorts.maceth_tx_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10402815415731484650ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_cdc_source_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13187479592393364493ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18113125249958079734ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_next_binary = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 897849692378824325ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3479397930201565083ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_converter_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7476824722306493802ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_converter_converter_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1302112633464660916ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_converter_converter_source_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3406425013727539973ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 9000236457275917480ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7536064032534943581ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_last_be_last_handler_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15635352551044774272ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6943164757230970061ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1593942340789841977ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_source_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7724206888644378212ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10856799070610439721ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16081088833593891458ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5311500226799580142ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17598330804327348862ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_source_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14263274420916555087ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14010670076246004071ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_gap_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13939536745157292050ull);
    vlSelf->mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16441599117233107109ull);
    vlSelf->mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11358354017411131817ull);
    vlSelf->mac_tx_chain_mii__DOT__packetfifo_payload_fifo_syncfifo_re = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13164238008362432090ull);
    vlSelf->mac_tx_chain_mii__DOT__packetfifo_param_fifo_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17285905066977482540ull);
    vlSelf->mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 258281159019826808ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_dp_source_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17609493384244137373ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12288930061705841276ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10839458962489396284ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16992324609569348374ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17842651943130442218ull);
    vlSelf->mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15247019980208113765ull);
    vlSelf->mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12849979839375586994ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8643508934661871415ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13968187726376025061ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16741339035965198223ull);
    vlSelf->mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15346800557855957281ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11157134746865640395ull);
    vlSelf->mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value_ce = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11773446921680440169ull);
    VL_SCOPED_RAND_RESET_W(82, vlSelf->mac_tx_chain_mii__DOT__storage[0], __VscopeHash, 8132024904073932961ull);
    VL_UNPACKED_FILL(vlSelf->mac_tx_chain_mii__DOT__storage.data(), sizeof(vlSelf->mac_tx_chain_mii__DOT__storage[0]), 32);
    vlSelf->mac_tx_chain_mii__DOT__memadr_1 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6492185072351252245ull);
    VL_SCOPED_RAND_RESET_W(82, vlSelf->mac_tx_chain_mii__DOT__storage_3[0], __VscopeHash, 10600070773926725663ull);
    VL_UNPACKED_FILL(vlSelf->mac_tx_chain_mii__DOT__storage_3.data(), sizeof(vlSelf->mac_tx_chain_mii__DOT__storage_3[0]), 512);
    VL_SCOPED_RAND_RESET_W(82, vlSelf->mac_tx_chain_mii__DOT__memdat_2, __VscopeHash, 17011761159416107675ull);
    VL_SCOPED_RAND_RESET_W(72, vlSelf->mac_tx_chain_mii__DOT__storage_5[0], __VscopeHash, 12287547749235059918ull);
    VL_UNPACKED_FILL(vlSelf->mac_tx_chain_mii__DOT__storage_5.data(), sizeof(vlSelf->mac_tx_chain_mii__DOT__storage_5[0]), 16);
    VL_SCOPED_RAND_RESET_W(72, vlSelf->mac_tx_chain_mii__DOT__memdat_5, __VscopeHash, 6539249160283472419ull);
    vlSelf->mac_tx_chain_mii__DOT__storage_6[0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14806835946626244869ull);
    VL_UNPACKED_FILL(vlSelf->mac_tx_chain_mii__DOT__storage_6.data(), sizeof(vlSelf->mac_tx_chain_mii__DOT__storage_6[0]), 16);
    vlSelf->mac_tx_chain_mii__DOT__memdat_6 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11201702723783787165ull);
    vlSelf->__Vdfg_Regularize_1556 = 0;
    vlSelf->__Vdfg_Regularize_1562 = 0;
    vlSelf->__Vdfg_Regularize_1564 = 0;
    vlSelf->__Vdfg_Regularize_1565 = 0;
    vlSelf->__Vdfg_Regularize_1567 = 0;
    vlSelf->__Vdfg_Regularize_1569 = 0;
    vlSelf->__Vdfg_Regularize_1571 = 0;
    vlSelf->__Vdfg_Regularize_1572 = 0;
    vlSelf->__Vdfg_Regularize_1578 = 0;
    vlSelf->__Vdfg_Regularize_1579 = 0;
    vlSelf->__Vdfg_Regularize_1581 = 0;
    vlSelf->__Vdfg_Regularize_1582 = 0;
    vlSelf->__Vdfg_Regularize_1583 = 0;
    vlSelf->__Vdfg_Regularize_1584 = 0;
    vlSelf->__Vdfg_Regularize_1585 = 0;
    vlSelf->__Vdfg_Regularize_1586 = 0;
    vlSelf->__Vdfg_Regularize_1587 = 0;
    vlSelf->__Vdfg_Regularize_1588 = 0;
    vlSelf->__Vdfg_Regularize_1589 = 0;
    vlSelf->__Vdfg_Regularize_1590 = 0;
    vlSelf->__Vdfg_Regularize_1593 = 0;
    vlSelf->__Vdfg_Regularize_1594 = 0;
    vlSelf->__Vdfg_Regularize_1595 = 0;
    vlSelf->__Vdfg_Regularize_1596 = 0;
    vlSelf->__Vdfg_Regularize_1597 = 0;
    vlSelf->__Vdfg_Regularize_1598 = 0;
    vlSelf->__Vdfg_Regularize_1599 = 0;
    vlSelf->__Vdfg_Regularize_1600 = 0;
    vlSelf->__Vdfg_Regularize_1602 = 0;
    vlSelf->__VstlTriggered[0] = 0;
    VL_UNPACKED_FILL(vlSelf->__VstlTriggered.data(), sizeof(vlSelf->__VstlTriggered[0]), 1);
    vlSelf->__VicoTriggered[0] = 0;
    VL_UNPACKED_FILL(vlSelf->__VicoTriggered.data(), sizeof(vlSelf->__VicoTriggered[0]), 2);
    vlSelf->__Vtrigprevexpr___TOP__sys_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sys_rst__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_rst__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__eth_tx_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__eth_rx_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__eth_phy_rst__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__reinit__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__eth_rst__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__loopback__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_tlast__0 = 0;
    vlSelf->__VactTriggered[0] = 0;
    VL_UNPACKED_FILL(vlSelf->__VactTriggered.data(), sizeof(vlSelf->__VactTriggered[0]), 1);
    vlSelf->__Vtrigprevexpr___TOP__eth_tx_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dp_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sys_clk__1 = 0;
    vlSelf->__VnbaTriggered[0] = 0;
    VL_UNPACKED_FILL(vlSelf->__VnbaTriggered.data(), sizeof(vlSelf->__VnbaTriggered[0]), 1);
}
