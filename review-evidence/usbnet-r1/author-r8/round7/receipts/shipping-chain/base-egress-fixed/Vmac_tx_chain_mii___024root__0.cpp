// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmac_tx_chain_mii.h for the primary calling header

#include "Vmac_tx_chain_mii__pch.h"

void Vmac_tx_chain_mii___024root___eval_sample(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_sample\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG
bool Vmac_tx_chain_mii___024root___trigger_anySet__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &in);

bool Vmac_tx_chain_mii___024root___eval_ico(Vmac_tx_chain_mii___024root* vlSelf, ::CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_ico\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VicoExecute;
    // Body
    vlSelfRef.__VicoTriggered[1U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[1U]) 
                                     | (::IData)((::IData)(firstIteration)));
    {
        // Inlined CFunc: _eval_triggers_vec__ico
        vlSelfRef.__VicoTriggered[0U] = (::QData)((::IData)(
                                                            (((((((::IData)(vlSelfRef.__VprimaryPorts.dp_tlast) 
                                                                  != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_tlast__0)) 
                                                                 << 5U) 
                                                                | (((::IData)(vlSelfRef.__VprimaryPorts.dp_tvalid) 
                                                                    != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_tvalid__0)) 
                                                                   << 4U)) 
                                                               | (((((::IData)(vlSelfRef.__VprimaryPorts.dp_tkeep) 
                                                                     != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_tkeep__0)) 
                                                                    << 3U) 
                                                                   | ((vlSelfRef.__VprimaryPorts.dp_tdata 
                                                                       != vlSelfRef.__Vtrigprevexpr___TOP__dp_tdata__0) 
                                                                      << 2U)) 
                                                                  | ((((::IData)(vlSelfRef.__VprimaryPorts.loopback) 
                                                                       != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__loopback__0)) 
                                                                      << 1U) 
                                                                     | ((::IData)(vlSelfRef.__VprimaryPorts.eth_rst) 
                                                                        != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__eth_rst__0))))) 
                                                              << 8U) 
                                                             | (((((((::IData)(vlSelfRef.__VprimaryPorts.reinit) 
                                                                     != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__reinit__0)) 
                                                                    << 3U) 
                                                                   | (((::IData)(vlSelfRef.__VprimaryPorts.eth_phy_rst) 
                                                                       != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__eth_phy_rst__0)) 
                                                                      << 2U)) 
                                                                  | ((((::IData)(vlSelfRef.__VprimaryPorts.eth_rx_clk) 
                                                                       != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__eth_rx_clk__0)) 
                                                                      << 1U) 
                                                                     | ((::IData)(vlSelfRef.__VprimaryPorts.eth_tx_clk) 
                                                                        != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__0)))) 
                                                                 << 4U) 
                                                                | (((((::IData)(vlSelfRef.__VprimaryPorts.dp_rst) 
                                                                      != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_rst__0)) 
                                                                     << 3U) 
                                                                    | (((::IData)(vlSelfRef.__VprimaryPorts.dp_clk) 
                                                                        != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__0)) 
                                                                       << 2U)) 
                                                                   | ((((::IData)(vlSelfRef.__VprimaryPorts.sys_rst) 
                                                                        != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_rst__0)) 
                                                                       << 1U) 
                                                                      | ((::IData)(vlSelfRef.__VprimaryPorts.sys_clk) 
                                                                         != (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__0))))))));
        vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__0 
            = vlSelfRef.__VprimaryPorts.sys_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__sys_rst__0 
            = vlSelfRef.__VprimaryPorts.sys_rst;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__0 
            = vlSelfRef.__VprimaryPorts.dp_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_rst__0 
            = vlSelfRef.__VprimaryPorts.dp_rst;
        vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__0 
            = vlSelfRef.__VprimaryPorts.eth_tx_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__eth_rx_clk__0 
            = vlSelfRef.__VprimaryPorts.eth_rx_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__eth_phy_rst__0 
            = vlSelfRef.__VprimaryPorts.eth_phy_rst;
        vlSelfRef.__Vtrigprevexpr___TOP__reinit__0 
            = vlSelfRef.__VprimaryPorts.reinit;
        vlSelfRef.__Vtrigprevexpr___TOP__eth_rst__0 
            = vlSelfRef.__VprimaryPorts.eth_rst;
        vlSelfRef.__Vtrigprevexpr___TOP__loopback__0 
            = vlSelfRef.__VprimaryPorts.loopback;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_tdata__0 
            = vlSelfRef.__VprimaryPorts.dp_tdata;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_tkeep__0 
            = vlSelfRef.__VprimaryPorts.dp_tkeep;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_tvalid__0 
            = vlSelfRef.__VprimaryPorts.dp_tvalid;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_tlast__0 
            = vlSelfRef.__VprimaryPorts.dp_tlast;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmac_tx_chain_mii___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vmac_tx_chain_mii___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        {
            // Inlined CFunc: _eval_body__ico
            if ((((0x0000000000000200ULL & vlSelfRef.__VicoTriggered[0U])) != 0ULL)) {
                {
                    // Inlined CFunc: _ico_comb__TOP__0
                    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid 
                        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
                           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable));
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready 
                        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
                           & ((0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)) 
                              & (9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0))));
                    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid 
                        = ((9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)) 
                           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid));
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary 
                        = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary) 
                                          + ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable) 
                                             & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable)) 
                                                | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready)))));
                }
            }
            if ((((0x0000000000001000ULL & vlSelfRef.__VicoTriggered[0U])) != 0ULL)) {
                {
                    // Inlined CFunc: _ico_comb__TOP__1
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce 
                        = ((::IData)(vlSelfRef.__VprimaryPorts.dp_tvalid) 
                           & (::IData)(vlSelfRef.__VprimaryPorts.dp_tready));
                    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary 
                        = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary) 
                                          + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce)));
                }
            }
        }
    }
    return (__VicoExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG
void Vmac_tx_chain_mii___024root___trigger_orInto__act_vec_vec(::VlUnpacked<::QData/*63:0*/, 1> &out, const ::VlUnpacked<::QData/*63:0*/, 1> &in);

bool Vmac_tx_chain_mii___024root___eval_act(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_act\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (::QData)((::IData)(
                                                            ((((::IData)(vlSelfRef.__VprimaryPorts.sys_clk) 
                                                               & (~ (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1))) 
                                                              << 2U) 
                                                             | ((((::IData)(vlSelfRef.__VprimaryPorts.dp_clk) 
                                                                  & (~ (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__1))) 
                                                                 << 1U) 
                                                                | ((::IData)(vlSelfRef.__VprimaryPorts.eth_tx_clk) 
                                                                   & (~ (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__1)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__eth_tx_clk__1 
            = vlSelfRef.__VprimaryPorts.eth_tx_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__dp_clk__1 
            = vlSelfRef.__VprimaryPorts.dp_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1 
            = vlSelfRef.__VprimaryPorts.sys_clk;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmac_tx_chain_mii___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vmac_tx_chain_mii___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

bool Vmac_tx_chain_mii___024root___eval_inact(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_inact\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

bool Vmac_tx_chain_mii___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in);
void Vmac_tx_chain_mii___024root___eval_body__nba(Vmac_tx_chain_mii___024root* vlSelf);
void Vmac_tx_chain_mii___024root___trigger_clear__act(::VlUnpacked<::QData/*63:0*/, 1> &out);

bool Vmac_tx_chain_mii___024root___eval_nba(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_nba\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vmac_tx_chain_mii___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vmac_tx_chain_mii___024root___eval_body__nba(vlSelf);
        Vmac_tx_chain_mii___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

bool Vmac_tx_chain_mii___024root___eval_obs(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_obs\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

bool Vmac_tx_chain_mii___024root___eval_react(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_react\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

void Vmac_tx_chain_mii___024root___eval_postponed(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_postponed\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

bool Vmac_tx_chain_mii___024root___trigger_anySet__ico(const ::VlUnpacked<::QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___trigger_anySet__ico\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((::IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

bool Vmac_tx_chain_mii___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___trigger_anySet__act\n"); );
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

void Vmac_tx_chain_mii___024root___nba_sequent__TOP__0(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___nba_sequent__TOP__0\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::SData/*8:0*/ __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32 = 0;
    ::SData/*8:0*/ __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33 = 0;
    ::SData/*9:0*/ __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34 = 0;
    ::CData/*3:0*/ __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36 = 0;
    ::CData/*0:0*/ __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38;
    __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38 = 0;
    ::VlWide<3>/*81:0*/ __Vdly_Val__mac_tx_chain_mii__DOT__storage_62;
    VL_ZERO_W(82, __Vdly_Val__mac_tx_chain_mii__DOT__storage_62);
    ::CData/*4:0*/ __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63;
    __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63 = 0;
    ::CData/*0:0*/ __Vdly_Set__mac_tx_chain_mii__DOT__storage_64;
    __Vdly_Set__mac_tx_chain_mii__DOT__storage_64 = 0;
    ::VlWide<3>/*81:0*/ __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65;
    VL_ZERO_W(82, __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65);
    ::SData/*8:0*/ __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66;
    __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66 = 0;
    ::CData/*0:0*/ __Vdly_Set__mac_tx_chain_mii__DOT__storage_3_67;
    __Vdly_Set__mac_tx_chain_mii__DOT__storage_3_67 = 0;
    // Body
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33 
        = vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32 
        = vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce;
    __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34 
        = vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0;
    __Vdly_Set__mac_tx_chain_mii__DOT__storage_3_67 = 0U;
    __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36 
        = vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0;
    __Vdly_Set__mac_tx_chain_mii__DOT__storage_64 = 0U;
    if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid) 
         & (0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)))) {
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32 
            = (0x000001ffU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce)));
        if ((1U & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_syncfifo_re)))) {
            __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34 
                = (0x000003ffU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)));
        }
    } else if (vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_syncfifo_re) {
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34 
            = (0x000003ffU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0) 
                              - (::IData)(1U)));
    }
    if (((0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)) 
         & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid))) {
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[0U] 
            = (::IData)((((::QData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[1U])) 
                          << 0x00000020U) | (::QData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[0U]))));
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[1U] 
            = (::IData)(((((::QData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[1U])) 
                           << 0x00000020U) | (::QData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[0U]))) 
                         >> 0x00000020U));
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[2U] 
            = (0x0003ffffU & ((0x00020000U & (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
                                              << 8U)) 
                              | (0x000000ffU & (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
                                                & ((~ 
                                                    (0x0000007fU 
                                                     & (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
                                                        >> 1U))) 
                                                   & (- (::IData)(
                                                                  (1U 
                                                                   & (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
                                                                      >> 9U)))))))));
        __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66 
            = vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce;
        __Vdly_Set__mac_tx_chain_mii__DOT__storage_3_67 = 1U;
    }
    if ((((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid) 
          & ((0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)) 
             & (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
                >> 9U))) & (9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)))) {
        if ((1U & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re)))) {
            __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36 
                = (0x0000000fU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)));
        }
    } else if (vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re) {
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36 
            = (0x0000000fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0) 
                              - (::IData)(1U)));
    }
    if ((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready) 
               | (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable))))) {
        __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[0U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[0U];
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[1U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[1U];
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_dout[2U] 
            = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__memdat_6) 
                << 8U) | vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[2U]);
    }
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce) {
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[0U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[0U];
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[1U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[1U];
        __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[2U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[2U];
        __Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63 
            = (0x0000001fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_binary));
        __Vdly_Set__mac_tx_chain_mii__DOT__storage_64 = 1U;
    }
    if (vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_syncfifo_re) {
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33 
            = (0x000001ffU & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume)));
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_readable = 1U;
        vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[0U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__storage_3
            [vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume][0U];
        vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[1U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__storage_3
            [vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume][1U];
        vlSelfRef.mac_tx_chain_mii__DOT__memdat_2[2U] 
            = vlSelfRef.mac_tx_chain_mii__DOT__storage_3
            [vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume][2U];
    } else if (vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce) {
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_readable = 0U;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary;
    if (vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re) {
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable = 1U;
    } else if (vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_source_ready) {
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable = 0U;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl61 
        = vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl60;
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11 
        = vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl10;
    if (vlSelfRef.mac_tx_chain_mii__DOT__macsys_rst) {
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33 = 0U;
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce 
            = __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32;
        __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38 = 0U;
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0 
            = __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34;
        __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36 = 0U;
    } else {
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce 
            = __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_produce_32;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0 
            = __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0_34;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0 
        = __Vdly__mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0_36;
    if (__Vdly_Set__mac_tx_chain_mii__DOT__storage_64) {
        vlSelfRef.mac_tx_chain_mii__DOT__storage[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63][0U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[0U];
        vlSelfRef.mac_tx_chain_mii__DOT__storage[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63][1U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[1U];
        vlSelfRef.mac_tx_chain_mii__DOT__storage[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_63][2U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_62[2U];
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_binary 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_next_binary;
    if (vlSelfRef.mac_tx_chain_mii__DOT__macsys_rst) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_readable = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_binary = 0U;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl60 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q;
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl10 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready 
        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
           & ((0x0200U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_level0)) 
              & (9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable 
        = __Vdly__mac_tx_chain_mii__DOT__tx_dp_cdc_readable_38;
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume 
        = __Vdly__mac_tx_chain_mii__DOT__packetfifo_payload_fifo_consume_33;
    if (__Vdly_Set__mac_tx_chain_mii__DOT__storage_3_67) {
        vlSelfRef.mac_tx_chain_mii__DOT__storage_3[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66][0U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[0U];
        vlSelfRef.mac_tx_chain_mii__DOT__storage_3[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66][1U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[1U];
        vlSelfRef.mac_tx_chain_mii__DOT__storage_3[__Vdly_Dim0__mac_tx_chain_mii__DOT__storage_3_66][2U] 
            = __Vdly_Val__mac_tx_chain_mii__DOT__storage_3_65[2U];
    }
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid 
        = ((~ (::IData)(vlSelfRef.__VprimaryPorts.loopback)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable));
    vlSelfRef.mac_tx_chain_mii__DOT__memdat_6 = vlSelfRef.mac_tx_chain_mii__DOT__storage_6
        [(0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary))];
    vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[0U] = vlSelfRef.mac_tx_chain_mii__DOT__storage_5
        [(0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary))][0U];
    vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[1U] = vlSelfRef.mac_tx_chain_mii__DOT__storage_5
        [(0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary))][1U];
    vlSelfRef.mac_tx_chain_mii__DOT__memdat_5[2U] = vlSelfRef.mac_tx_chain_mii__DOT__storage_5
        [(0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary))][2U];
    vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_payload_fifo_sink_valid 
        = ((9U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_sink_sink_valid));
}

void Vmac_tx_chain_mii___024root___nba_sequent__TOP__2(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___nba_sequent__TOP__2\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
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
    ::CData/*0:0*/ __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2;
    __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2 = 0;
    ::CData/*1:0*/ __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14;
    __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14 = 0;
    ::CData/*1:0*/ __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16;
    __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16 = 0;
    ::CData/*0:0*/ __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18;
    __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18 = 0;
    ::CData/*2:0*/ __Vdly__mac_tx_chain_mii__DOT__tx_preamble_count_23;
    __Vdly__mac_tx_chain_mii__DOT__tx_preamble_count_23 = 0;
    // Body
    __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2 
        = vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux;
    __Vdly__mac_tx_chain_mii__DOT__tx_preamble_count_23 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count;
    __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14 = vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt;
    __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid;
    __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16 
        = vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state;
    if (vlSelfRef.__VprimaryPorts.phy_sink_valid) {
        __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2 
            = ((1U & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux))) 
               && (1U & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux))));
    }
    if (vlSelfRef.mac_tx_chain_mii__DOT__eth_tx_rst) {
        __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2 = 0U;
    }
    if (((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
          ? ((::IData)(vlSelfRef.__Vdfg_Regularize_1579) 
             & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready))
          : (2U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)))) {
        __Vdly__mac_tx_chain_mii__DOT__tx_preamble_count_23 
            = (7U & ((- (::IData)((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)))) 
                     & ((- (::IData)((::IData)(vlSelfRef.__Vdfg_Regularize_1579))) 
                        & (((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count)) 
                           & (- (::IData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready)))))));
    }
    if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid) 
         & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_ready))) {
        if (vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop) {
            if (vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last) {
                vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop = 0U;
            }
        } else if (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end) 
                    & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last)))) {
            vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop = 1U;
        }
        vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux 
            = ((7U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))
                ? 0U : (7U & ((::IData)(1U) + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux))));
    }
    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
            ? ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready)
                ? ((7U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count))
                    ? 2U : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
                : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
            : ((2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))
                ? ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state) 
                   & (- (::IData)((1U & (~ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid) 
                                            & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_sink_ready) 
                                               & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_last))))))))
                : ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid)
                    ? 1U : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))));
    vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_en = vlSelfRef.__VprimaryPorts.phy_sink_valid;
    vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_data = 
        (0x0000000fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux)
                         ? ((::IData)(vlSelfRef.__VprimaryPorts.phy_sink_data) 
                            >> 4U) : (::IData)(vlSelfRef.__VprimaryPorts.phy_sink_data)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_binary 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary;
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value_ce) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter_clockdomainsrenamer0_next_value;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl01 
        = vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl00;
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value_ce) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_gap_counter_clockdomainsrenamer3_next_value;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__memadr_1 = (0x0000001fU 
                                                 & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary));
    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state 
        = vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_next_state;
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reset) {
        __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14 = 3U;
    } else if (((::IData)(vlSelfRef.__Vdfg_Regularize_1582) 
                & (0U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt)))) {
        __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14 
            = (3U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt) 
                     - (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_ready)));
    }
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet 
            = ((- (::IData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0))) 
               & ((~ (((((((((::IData)(vlSelfRef.__Vdfg_Regularize_1571) 
                             << 3U) | (4U & ((::IData)(vlSelfRef.__Vdfg_Regularize_1569) 
                                             << 2U))) 
                           | ((2U & (::IData)(vlSelfRef.__Vdfg_Regularize_1569)) 
                              | (::IData)(vlSelfRef.__Vdfg_Regularize_1567))) 
                          << 0x0000000cU) | ((((2U 
                                                & ((::IData)(vlSelfRef.__Vdfg_Regularize_1565) 
                                                   << 1U)) 
                                               | (1U 
                                                  & ((::IData)(vlSelfRef.__Vdfg_Regularize_1565) 
                                                     >> 1U))) 
                                              << 0x0000000aU) 
                                             | (((::IData)(vlSelfRef.__Vdfg_Regularize_1602) 
                                                 << 9U) 
                                                | (0x00000100U 
                                                   & ((::IData)(vlSelfRef.__Vdfg_Regularize_1564) 
                                                      << 8U))))) 
                        | (((((2U & (::IData)(vlSelfRef.__Vdfg_Regularize_1564)) 
                              | (::IData)(vlSelfRef.__Vdfg_Regularize_1600)) 
                             << 6U) | (((2U & ((::IData)(vlSelfRef.__Vdfg_Regularize_1556) 
                                               << 1U)) 
                                        | (1U & ((::IData)(vlSelfRef.__Vdfg_Regularize_1556) 
                                                 >> 1U))) 
                                       << 4U)) | ((
                                                   ((2U 
                                                     & ((::IData)(vlSelfRef.__Vdfg_Regularize_1556) 
                                                        >> 1U)) 
                                                    | (::IData)(vlSelfRef.__Vdfg_Regularize_1599)) 
                                                   << 2U) 
                                                  | (((::IData)(vlSelfRef.__Vdfg_Regularize_1598) 
                                                      << 1U) 
                                                     | (::IData)(vlSelfRef.__Vdfg_Regularize_1597))))) 
                       << 0x00000010U) | (((((((::IData)(vlSelfRef.__Vdfg_Regularize_1596) 
                                               << 3U) 
                                              | ((::IData)(vlSelfRef.__Vdfg_Regularize_1595) 
                                                 << 2U)) 
                                             | (((::IData)(vlSelfRef.__Vdfg_Regularize_1594) 
                                                 << 1U) 
                                                | (::IData)(vlSelfRef.__Vdfg_Regularize_1593))) 
                                            << 0x0000000cU) 
                                           | ((((2U 
                                                 & ((::IData)(vlSelfRef.__Vdfg_Regularize_1562) 
                                                    << 1U)) 
                                                | (1U 
                                                   & ((::IData)(vlSelfRef.__Vdfg_Regularize_1562) 
                                                      >> 1U))) 
                                               << 0x0000000aU) 
                                              | (((2U 
                                                   & ((::IData)(vlSelfRef.__Vdfg_Regularize_1572) 
                                                      << 1U)) 
                                                  | (1U 
                                                     & ((::IData)(vlSelfRef.__Vdfg_Regularize_1572) 
                                                        >> 1U))) 
                                                 << 8U))) 
                                          | ((((((::IData)(vlSelfRef.__Vdfg_Regularize_1590) 
                                                 << 3U) 
                                                | ((::IData)(vlSelfRef.__Vdfg_Regularize_1589) 
                                                   << 2U)) 
                                               | (((::IData)(vlSelfRef.__Vdfg_Regularize_1588) 
                                                   << 1U) 
                                                  | (::IData)(vlSelfRef.__Vdfg_Regularize_1587))) 
                                              << 4U) 
                                             | ((((::IData)(vlSelfRef.__Vdfg_Regularize_1586) 
                                                  << 3U) 
                                                 | ((::IData)(vlSelfRef.__Vdfg_Regularize_1585) 
                                                    << 2U)) 
                                                | (((::IData)(vlSelfRef.__Vdfg_Regularize_1584) 
                                                    << 1U) 
                                                   | (::IData)(vlSelfRef.__Vdfg_Regularize_1583))))))) 
                  & (- (::IData)((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_last_be)))));
    }
    if ((1U & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)) 
               | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_sink_ready)))) {
        __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_valid;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_last 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_last;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data 
            = (0x000000ffU & ((- (::IData)((1U & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state))))) 
                              & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
                                 & (- (::IData)((1U 
                                                 & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state))))))));
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_last_be 
            = vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_payload_last_be;
    }
    if (((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
         & (::IData)(vlSelfRef.__Vdfg_Regularize_1578))) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
            = (((((((((::IData)(vlSelfRef.__Vdfg_Regularize_1583) 
                      << 3U) | ((::IData)(vlSelfRef.__Vdfg_Regularize_1584) 
                                << 2U)) | (((::IData)(vlSelfRef.__Vdfg_Regularize_1585) 
                                            << 1U) 
                                           | (::IData)(vlSelfRef.__Vdfg_Regularize_1586))) 
                   << 0x0000000cU) | (((((::IData)(vlSelfRef.__Vdfg_Regularize_1587) 
                                         << 3U) | ((::IData)(vlSelfRef.__Vdfg_Regularize_1588) 
                                                   << 2U)) 
                                       | (((::IData)(vlSelfRef.__Vdfg_Regularize_1589) 
                                           << 1U) | (::IData)(vlSelfRef.__Vdfg_Regularize_1590))) 
                                      << 8U)) | ((((::IData)(vlSelfRef.__Vdfg_Regularize_1572) 
                                                   << 6U) 
                                                  | ((::IData)(vlSelfRef.__Vdfg_Regularize_1562) 
                                                     << 4U)) 
                                                 | ((((::IData)(vlSelfRef.__Vdfg_Regularize_1593) 
                                                      << 3U) 
                                                     | ((::IData)(vlSelfRef.__Vdfg_Regularize_1594) 
                                                        << 2U)) 
                                                    | (((::IData)(vlSelfRef.__Vdfg_Regularize_1595) 
                                                        << 1U) 
                                                       | (::IData)(vlSelfRef.__Vdfg_Regularize_1596))))) 
                << 0x00000010U) | ((((((::IData)(vlSelfRef.__Vdfg_Regularize_1597) 
                                       << 6U) | (((::IData)(vlSelfRef.__Vdfg_Regularize_1598) 
                                                  << 5U) 
                                                 | ((::IData)(vlSelfRef.__Vdfg_Regularize_1599) 
                                                    << 4U))) 
                                     | (((::IData)(vlSelfRef.__Vdfg_Regularize_1556) 
                                         << 1U) | (::IData)(vlSelfRef.__Vdfg_Regularize_1600))) 
                                    << 9U) | ((((::IData)(vlSelfRef.__Vdfg_Regularize_1564) 
                                                << 7U) 
                                               | (((::IData)(vlSelfRef.__Vdfg_Regularize_1602) 
                                                   << 6U) 
                                                  | ((::IData)(vlSelfRef.__Vdfg_Regularize_1565) 
                                                     << 4U))) 
                                              | (((::IData)(vlSelfRef.__Vdfg_Regularize_1567) 
                                                  << 3U) 
                                                 | (((::IData)(vlSelfRef.__Vdfg_Regularize_1569) 
                                                     << 1U) 
                                                    | (::IData)(vlSelfRef.__Vdfg_Regularize_1571))))));
    }
    if (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reset) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg = 0xffffffffU;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q 
        = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary) 
            >> 1U) ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_next_binary));
    vlSelfRef.mac_tx_chain_mii__DOT__macdp_rst = (((::IData)(vlSelfRef.__VprimaryPorts.dp_rst) 
                                                   | (::IData)(vlSelfRef.__VprimaryPorts.reinit)) 
                                                  | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl3_rst1));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count 
        = __Vdly__mac_tx_chain_mii__DOT__tx_preamble_count_23;
    if (vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop = 0U;
        __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14 = 3U;
    }
    __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
            ? ((::IData)(vlSelfRef.__Vdfg_Regularize_1581)
                ? 2U : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
            : ((2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
                ? ((0U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt))
                    ? ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state) 
                       & (- (::IData)((1U & (~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_ready))))))
                    : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
                : ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)
                    ? 1U : (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt = __Vdly__mac_tx_chain_mii__DOT__tx_crc_cnt_14;
    vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux 
        = __Vdly__mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux_2;
    if (vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux = 0U;
        __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18 = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state = 0U;
        __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16 = 0U;
    }
    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state 
        = __Vdly__mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state_16;
    vlSelfRef.__Vdfg_Regularize_1579 = (7U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_preamble_count));
    vlSelfRef.__VprimaryPorts.gmii_tx_en = vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_en;
    vlSelfRef.__VprimaryPorts.gmii_tx_data = vlSelfRef.mac_tx_chain_mii__DOT__pads_tx_data;
    vlSelfRef.__VprimaryPorts.phy_sink_ready = vlSelfRef.mac_tx_chain_mii__DOT__liteethphymiitx_converter_mux;
    vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl00 
        = vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reset = 
        (1U & (~ ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
                  | (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)))));
    vlSelfRef.__Vdfg_Regularize_1582 = ((1U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
                                        & (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)));
    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state 
        = vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_next_state;
    vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state 
        = vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_next_state;
    if (vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1) {
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q_binary = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_counter = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg = 0xffffffffU;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_last_be = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpaddinginserter_state = 0U;
        vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state = 0U;
    }
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
    __Vdfg_Regularize_1603 = (3U & ((- (::IData)((1U 
                                                  & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                                     >> 1U)))) 
                                    ^ (- (::IData)(
                                                   (1U 
                                                    & (vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                                       >> 0x0000001eU))))));
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
    __Vdfg_Regularize_1555 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001cU) 
                                    ^ ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data) 
                                       >> 3U)));
    __Vdfg_Regularize_1539 = (1U & ((vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_reg 
                                     >> 0x0000001fU) 
                                    ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_payload_data)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter1_q) 
           != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl01));
    vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl3_rst1 
        = ((::IData)(vlSelfRef.__VprimaryPorts.dp_rst) 
           | (::IData)(vlSelfRef.__VprimaryPorts.reinit));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid 
        = __Vdly__mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid_18;
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_last 
        = ((0U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_cnt)) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_1582));
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
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_source_valid 
        = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_drop)) 
           & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_source_source_valid));
    mac_tx_chain_mii__DOT__tx_preamble_source_last 
        = ((2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
           & ((1U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
              & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_last)));
    vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1 
        = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__eth_tx_rst) 
            | (::IData)(vlSelfRef.__VprimaryPorts.eth_rst)) 
           | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl4_rst1));
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
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state))
            ? (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)
            : (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)));
    mac_tx_chain_mii__DOT__tx_preamble_source_valid 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state)) 
           | ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_source_valid) 
              & (2U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacpreambleinserter_state))));
    vlSelfRef.__VprimaryPorts.phy_sink_last = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state)) 
                                               & (::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_last));
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
    vlSelfRef.__VprimaryPorts.phy_sink_valid = ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmacgap_state)) 
                                                & (::IData)(mac_tx_chain_mii__DOT__tx_preamble_source_valid));
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
    vlSelfRef.__VprimaryPorts.maceth_tx_rst = vlSelfRef.mac_tx_chain_mii__DOT__maceth_tx_rst_1;
    vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl4_rst1 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__eth_tx_rst) 
           | (::IData)(vlSelfRef.__VprimaryPorts.eth_rst));
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
    vlSelfRef.mac_tx_chain_mii__DOT__eth_tx_rst = ((::IData)(vlSelfRef.__VprimaryPorts.eth_phy_rst) 
                                                   | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl0_rst1));
    vlSelfRef.__Vdfg_Regularize_1581 = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_last) 
                                        & (::IData)(vlSelfRef.__Vdfg_Regularize_1578));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_padding_source_ready 
        = (1U & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_pipe_valid_source_valid)) 
                 | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_sink_ready)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 
        = ((1U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_bufferizeendpoints_state)) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_1581));
    vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl0_rst1 
        = vlSelfRef.__VprimaryPorts.eth_phy_rst;
}

void Vmac_tx_chain_mii___024root___nba_comb__TOP__0(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___nba_comb__TOP__0\n"); );
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
    // Body
    mac_tx_chain_mii__DOT__tx_cdc_source_source_last 
        = (1U & (vlSelfRef.mac_tx_chain_mii__DOT__storage
                 [vlSelfRef.mac_tx_chain_mii__DOT__memadr_1][2U] 
                 >> 0x00000011U));
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
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last 
        = ((::IData)(mac_tx_chain_mii__DOT__tx_cdc_source_source_last) 
           & (7U == (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_mux)));
    vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end 
        = ((::IData)(mac_tx_chain_mii__DOT__tx_cdc_source_source_last) 
           & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
              >> 8U));
    mac_tx_chain_mii__DOT__tx_last_be_source_source_payload_last_be 
        = (1U & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__txdatapath_liteethmactxlastbe_state)) 
                 & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_payload_data) 
                    >> 8U)));
    mac_tx_chain_mii__DOT__tx_converter_source_last 
        = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_last_be_packet_end) 
           | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_converter_converter_source_last));
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

void Vmac_tx_chain_mii___024root___eval_body__nba(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_body__nba\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((((4ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        Vmac_tx_chain_mii___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((((2ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        {
            // Inlined CFunc: _nba_sequent__TOP__1
            ::VlWide<3>/*71:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56;
            VL_ZERO_W(72, __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56);
            ::CData/*3:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57 = 0;
            ::CData/*0:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_5_58;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_5_58 = 0;
            ::CData/*1:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_6_59;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_6_59 = 0;
            ::CData/*3:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_6_60;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_6_60 = 0;
            ::CData/*0:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_6_61;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_6_61 = 0;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_6_61 = 0U;
            __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_5_58 = 0U;
            if (vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce) {
                __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_6_59 
                    = ((::IData)(vlSelfRef.__VprimaryPorts.dp_tlast) 
                       << 1U);
                __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_6_60 
                    = (0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary));
                __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_6_61 = 1U;
                __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[0U] 
                    = (::IData)(vlSelfRef.__VprimaryPorts.dp_tdata);
                __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[1U] 
                    = (::IData)((vlSelfRef.__VprimaryPorts.dp_tdata 
                                 >> 0x00000020U));
                __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[2U] 
                    = vlSelfRef.__VprimaryPorts.dp_tkeep;
                __Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57 
                    = (0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary));
                __Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_5_58 = 1U;
            }
            vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71 
                = vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl70;
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q 
                = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary) 
                    >> 1U) ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary));
            if (__Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_6_61) {
                vlSelfRef.mac_tx_chain_mii__DOT__storage_6[__Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_6_60] 
                    = __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_6_59;
            }
            if (__Vinline_0__nba_sequent__TOP__1___Vdly_Set__mac_tx_chain_mii__DOT__storage_5_58) {
                vlSelfRef.mac_tx_chain_mii__DOT__storage_5[__Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57][0U] 
                    = __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[0U];
                vlSelfRef.mac_tx_chain_mii__DOT__storage_5[__Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57][1U] 
                    = __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[1U];
                vlSelfRef.mac_tx_chain_mii__DOT__storage_5[__Vinline_0__nba_sequent__TOP__1___Vdly_Dim0__mac_tx_chain_mii__DOT__storage_5_57][2U] 
                    = __Vinline_0__nba_sequent__TOP__1___Vdly_Val__mac_tx_chain_mii__DOT__storage_5_56[2U];
            }
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary 
                = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary;
            if (vlSelfRef.mac_tx_chain_mii__DOT__macdp_rst) {
                vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q = 0U;
                vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary = 0U;
            }
            vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl70 
                = vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q;
            vlSelfRef.__VprimaryPorts.dp_tready = (
                                                   ((1U 
                                                     & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q) 
                                                        >> 4U)) 
                                                    == 
                                                    (1U 
                                                     & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71) 
                                                        >> 4U))) 
                                                   | (((1U 
                                                        & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q) 
                                                           >> 3U)) 
                                                       == 
                                                       (1U 
                                                        & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71) 
                                                           >> 3U))) 
                                                      | ((7U 
                                                          & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q)) 
                                                         != 
                                                         (7U 
                                                          & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl71)))));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce 
                = ((::IData)(vlSelfRef.__VprimaryPorts.dp_tvalid) 
                   & (::IData)(vlSelfRef.__VprimaryPorts.dp_tready));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_next_binary 
                = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_q_binary) 
                                  + (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter0_ce)));
        }
    }
    if ((((1ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        Vmac_tx_chain_mii___024root___nba_sequent__TOP__2(vlSelf);
    }
    if ((((4ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        {
            // Inlined CFunc: _nba_sequent__TOP__3
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q 
                = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary) 
                    >> 1U) ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q 
                = (((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_next_binary) 
                    >> 1U) ^ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q_next_binary));
            if (vlSelfRef.mac_tx_chain_mii__DOT__macsys_rst) {
                vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q = 0U;
                vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q = 0U;
            }
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable 
                = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q) 
                   != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl61));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_ce 
                = ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable) 
                   & (((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q) 
                              >> 5U)) == (1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11) 
                                                >> 5U))) 
                      | (((1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q) 
                                 >> 4U)) == (1U & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11) 
                                                   >> 4U))) 
                         | ((0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_cdc_cdc_graycounter0_q)) 
                            != (0x0000000fU & (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__multiregimpl11))))));
            vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_next_binary 
                = (0x0000001fU & ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_graycounter1_q_binary) 
                                  + ((::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_asyncfifo_readable) 
                                     & ((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_cdc_readable)) 
                                        | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__tx_dp_source_source_ready)))));
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
            vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_syncfifo_re 
                = (((~ (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_readable)) 
                    | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_source_ready)) 
                   & (0U != (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__packetfifo_param_fifo_level0)));
        }
    }
    if ((((5ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        Vmac_tx_chain_mii___024root___nba_comb__TOP__0(vlSelf);
    }
    if ((((1ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
        {
            // Inlined CFunc: _nba_sequent__TOP__4
            vlSelfRef.mac_tx_chain_mii__DOT__macsys_rst 
                = (((::IData)(vlSelfRef.__VprimaryPorts.sys_rst) 
                    | (::IData)(vlSelfRef.__VprimaryPorts.reinit)) 
                   | (::IData)(vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl2_rst1));
            vlSelfRef.mac_tx_chain_mii__DOT__simasyncresetsynchronizerimpl2_rst1 
                = ((::IData)(vlSelfRef.__VprimaryPorts.sys_rst) 
                   | (::IData)(vlSelfRef.__VprimaryPorts.reinit));
        }
    }
}

void Vmac_tx_chain_mii___024root___trigger_orInto__act_vec_vec(::VlUnpacked<::QData/*63:0*/, 1> &out, const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((::IData)(1U) + n);
    } while ((0U >= n));
}

void Vmac_tx_chain_mii___024root___trigger_clear__act(::VlUnpacked<::QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___trigger_clear__act\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((::IData)(1U) + n);
    } while ((1U > n));
}

#ifdef VL_DEBUG
void Vmac_tx_chain_mii___024root___eval_debug_assertions(Vmac_tx_chain_mii___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmac_tx_chain_mii___024root___eval_debug_assertions\n"); );
    Vmac_tx_chain_mii__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.sys_clk 
                      & 0xfeU)))) {
        Verilated::overWidthError("sys_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.sys_rst 
                      & 0xfeU)))) {
        Verilated::overWidthError("sys_rst");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.dp_clk 
                      & 0xfeU)))) {
        Verilated::overWidthError("dp_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.dp_rst 
                      & 0xfeU)))) {
        Verilated::overWidthError("dp_rst");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.eth_tx_clk 
                      & 0xfeU)))) {
        Verilated::overWidthError("eth_tx_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.eth_rx_clk 
                      & 0xfeU)))) {
        Verilated::overWidthError("eth_rx_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.eth_phy_rst 
                      & 0xfeU)))) {
        Verilated::overWidthError("eth_phy_rst");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.reinit 
                      & 0xfeU)))) {
        Verilated::overWidthError("reinit");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.eth_rst 
                      & 0xfeU)))) {
        Verilated::overWidthError("eth_rst");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.loopback 
                      & 0xfeU)))) {
        Verilated::overWidthError("loopback");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.dp_tvalid 
                      & 0xfeU)))) {
        Verilated::overWidthError("dp_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.__VprimaryPorts.dp_tlast 
                      & 0xfeU)))) {
        Verilated::overWidthError("dp_tlast");
    }
}
#endif  // VL_DEBUG
