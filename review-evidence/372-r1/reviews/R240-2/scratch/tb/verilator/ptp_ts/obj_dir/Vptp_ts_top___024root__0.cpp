// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

void Vptp_ts_top___024root___eval_triggers_vec__ico(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_triggers_vec__ico\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                    (((((IData)(vlSelfRef.ts_m_axis_tready) 
                                                        != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__ts_m_axis_tready__0)) 
                                                       << 0x00000018U) 
                                                      | (((((((IData)(vlSelfRef.m_axis_rx_tready) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_rx_tready__0)) 
                                                             << 3U) 
                                                            | (((IData)(vlSelfRef.s_axis_rx_tkeep) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tkeep__0)) 
                                                               << 2U)) 
                                                           | ((((IData)(vlSelfRef.s_axis_rx_tlast) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tlast__0)) 
                                                               << 1U) 
                                                              | ((IData)(vlSelfRef.s_axis_rx_tvalid) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tvalid__0)))) 
                                                          << 0x00000014U) 
                                                         | (((((vlSelfRef.s_axis_rx_tdata 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__s_axis_rx_tdata__0) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.m_axis_tx_tready) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_tx_tready__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.s_axis_tx_tkeep) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.s_axis_tx_tlast) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tlast__0)))) 
                                                            << 0x00000010U))) 
                                                     | ((((((((IData)(vlSelfRef.s_axis_tx_tvalid) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0)) 
                                                             << 3U) 
                                                            | ((vlSelfRef.s_axis_tx_tdata 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tdata__0) 
                                                               << 2U)) 
                                                           | (((vlSelfRef.i_ptp_egress_lat 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_egress_lat__0) 
                                                               << 1U) 
                                                              | (vlSelfRef.i_ptp_ingress_lat 
                                                                 != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_ingress_lat__0))) 
                                                          << 0x0000000cU) 
                                                         | ((((((IData)(vlSelfRef.i_ptp_cmd_snapshot) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_snapshot__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.i_ptp_cmd_adjust) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_adjust__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.i_ptp_cmd_load) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_cmd_load__0)) 
                                                                 << 1U) 
                                                                | (vlSelfRef.i_ptp_offset 
                                                                   != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_offset__0))) 
                                                            << 8U)) 
                                                        | ((((((vlSelfRef.i_ptp_tod_wr 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_tod_wr__0) 
                                                               << 3U) 
                                                              | ((vlSelfRef.i_ptp_adj 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_adj__0) 
                                                                 << 2U)) 
                                                             | (((vlSelfRef.i_ptp_incr 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_incr__0) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.i_ptp_enable) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ptp_enable__0)))) 
                                                            << 4U) 
                                                           | (((((IData)(vlSelfRef.axis_resetn) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__0)) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.axis_clk) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.gtx_resetn) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_resetn__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.gtx_clk) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__0)))))))));
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
    if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VicoDidInit)))))) {
        vlSelfRef.__VicoDidInit = 1U;
        vlSelfRef.__VicoTriggered[0U] = (1ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (2ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (4ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (8ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000010ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000020ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000040ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000080ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000100ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000200ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000400ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000800ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000001000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000002000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000004000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000008000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000010000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000020000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000040000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000080000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000100000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000200000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000400000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000800000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000001000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
    }
}

bool Vptp_ts_top___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

void Vptp_ts_top___024root___eval_ico(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_ico\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x0000000000004000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__0
            vlSelfRef.m_axis_tx_tdata = vlSelfRef.s_axis_tx_tdata;
        }
    }
    if ((0x0000000000040000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__1
            vlSelfRef.s_axis_tx_tready = vlSelfRef.m_axis_tx_tready;
        }
    }
    if ((0x0000000000008000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__2
            vlSelfRef.m_axis_tx_tvalid = vlSelfRef.s_axis_tx_tvalid;
        }
    }
    if ((0x0000000000010000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__3
            vlSelfRef.m_axis_tx_tlast = vlSelfRef.s_axis_tx_tlast;
        }
    }
    if ((0x0000000000020000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__4
            vlSelfRef.m_axis_tx_tkeep = vlSelfRef.s_axis_tx_tkeep;
        }
    }
    if ((0x0000000000080000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__5
            vlSelfRef.m_axis_rx_tdata = vlSelfRef.s_axis_rx_tdata;
        }
    }
    if ((0x0000000000800000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__6
            vlSelfRef.s_axis_rx_tready = vlSelfRef.m_axis_rx_tready;
        }
    }
    if ((0x0000000000100000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__7
            vlSelfRef.m_axis_rx_tvalid = vlSelfRef.s_axis_rx_tvalid;
        }
    }
    if ((0x0000000000200000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__8
            vlSelfRef.m_axis_rx_tlast = vlSelfRef.s_axis_rx_tlast;
        }
    }
    if ((0x0000000000400000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__9
            vlSelfRef.m_axis_rx_tkeep = vlSelfRef.s_axis_rx_tkeep;
        }
    }
    if ((0x0000000000048000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__0
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc 
                = ((IData)(vlSelfRef.s_axis_tx_tvalid) 
                   & (IData)(vlSelfRef.m_axis_tx_tready));
        }
    }
    if ((0x0000000000900000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__1
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc 
                = ((IData)(vlSelfRef.s_axis_rx_tvalid) 
                   & (IData)(vlSelfRef.m_axis_rx_tready));
        }
    }
    if ((0x0000000000058000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__2
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push 
                = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc) 
                        & (IData)(vlSelfRef.s_axis_tx_tlast)) 
                       & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid)) 
                      & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match)) 
                     & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid)) 
                    & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type)))) 
                   & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)));
        }
    }
    if ((0x0000000000b00000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__3
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push 
                = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc) 
                        & (IData)(vlSelfRef.s_axis_rx_tlast)) 
                       & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid)) 
                      & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match)) 
                     & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid)) 
                    & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type)))) 
                   & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)));
        }
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vptp_ts_top___024root___eval_phase__ico(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_phase__ico\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vptp_ts_top___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vptp_ts_top___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vptp_ts_top___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        Vptp_ts_top___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

bool Vptp_ts_top___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___trigger_anySet__act\n"); );
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

void Vptp_ts_top___024root___nba_sequent__TOP__0(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___nba_sequent__TOP__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s;
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s = 0;
    CData/*2:0*/ __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s;
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s = 0;
    VlWide<3>/*95:0*/ __Vtemp_3;
    VlWide<3>/*95:0*/ __Vtemp_4;
    VlWide<3>/*95:0*/ __Vtemp_5;
    VlWide<3>/*95:0*/ __Vtemp_6;
    VlWide<3>/*95:0*/ __Vtemp_9;
    VlWide<3>/*95:0*/ __Vtemp_10;
    VlWide<3>/*95:0*/ __Vtemp_11;
    // Body
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s 
        = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_s;
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_s;
    vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s 
        = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_s;
    vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts 
        = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts;
    vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[0U] 
        = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U];
    vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[1U] 
        = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U];
    vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[2U] 
        = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U];
    if (vlSelfRef.gtx_resetn) {
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s 
            = ((6U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_s) 
                      << 1U)) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_tgl));
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s 
            = ((6U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_s) 
                      << 1U)) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl));
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s 
            = ((6U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_s) 
                      << 1U)) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl));
        if (vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot_valid) {
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts 
                = (1U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts)));
        }
        if (vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_pulse_q) {
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[0U] 
                = ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap) 
                   << 0x00000018U);
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[1U] 
                = (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap) 
                    >> 8U) | ((IData)((vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap 
                                       >> 0x00000020U)) 
                              << 0x00000018U));
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[2U] 
                = ((IData)((vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap 
                            >> 0x00000020U)) >> 8U);
        } else {
            vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U];
            vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U];
            vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U];
            if (vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__en_sync) {
                VL_EXTENDS_WQ(88,33, __Vtemp_3, (QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_sync)));
                VL_EXTENDS_WI(88,32, __Vtemp_4, vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_sync);
                VL_ADD_W(3, __Vtemp_5, __Vtemp_3, __Vtemp_4);
                VL_ADD_W(3, __Vtemp_6, vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next, __Vtemp_5);
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                    = __Vtemp_6[0U];
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                    = __Vtemp_6[1U];
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                    = (0x00ffffffU & __Vtemp_6[2U]);
            }
            if (vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_pulse_q) {
                VL_EXTENDS_WQ(88,64, __Vtemp_9, vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__offset_cap);
                VL_SHIFTL_WWI(88,88,32, __Vtemp_10, __Vtemp_9, 0x00000018U);
                VL_ADD_W(3, __Vtemp_11, vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next, __Vtemp_10);
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                    = __Vtemp_11[0U];
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                    = __Vtemp_11[1U];
                vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                    = (0x00ffffffU & __Vtemp_11[2U]);
            }
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[0U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U];
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[1U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U];
            vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[2U] 
                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U];
        }
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_s) 
                                      >> 1U))))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap 
                = vlSelfRef.i_ptp_tod_wr;
        }
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_s) 
                                      >> 1U))))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__offset_cap 
                = vlSelfRef.i_ptp_offset;
        }
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_sync 
            = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_meta;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_sync 
            = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_meta;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_meta 
            = vlSelfRef.i_ptp_incr;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_meta 
            = vlSelfRef.i_ptp_adj;
    } else {
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s = 0U;
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s = 0U;
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts = 0U;
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[0U] = 0U;
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[1U] = 0U;
        vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[2U] = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap = 0ULL;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__offset_cap = 0ULL;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_sync = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_sync = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__incr_meta = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_meta = 0U;
    }
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_pulse_q 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & VL_REDXOR_32(
                                                               (3U 
                                                                & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_s) 
                                                                   >> 1U)))));
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_pulse_q 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & VL_REDXOR_32(
                                                               (3U 
                                                                & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_s) 
                                                                   >> 1U)))));
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__en_sync 
        = ((IData)(vlSelfRef.gtx_resetn) && (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__en_meta));
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_s 
        = __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__load_s;
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_s 
        = __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__adj_s;
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__en_meta 
        = ((IData)(vlSelfRef.gtx_resetn) && (IData)(vlSelfRef.i_ptp_enable));
}

extern const VlUnpacked<CData/*1:0*/, 256> Vptp_ts_top__ConstPool__TABLE_hd45f40b9_0;

void Vptp_ts_top___024root___nba_sequent__TOP__1(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___nba_sequent__TOP__1\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg;
    __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg;
    __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg;
    __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state;
    __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state = 0;
    CData/*6:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl = 0;
    QData/*63:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts = 0;
    SData/*15:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq = 0;
    CData/*3:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt = 0;
    CData/*0:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 0;
    CData/*6:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl = 0;
    QData/*63:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts = 0;
    SData/*15:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq = 0;
    CData/*3:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt = 0;
    CData/*0:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = 0;
    CData/*1:0*/ __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 0;
    CData/*2:0*/ __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s;
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0);
    CData/*0:0*/ __VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0;
    __VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0);
    CData/*0:0*/ __VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0;
    __VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0);
    CData/*0:0*/ __VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0;
    __VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VlWide<3>/*72:0*/ __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1;
    VL_ZERO_W(73, __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1);
    CData/*0:0*/ __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    // Body
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0 = 0U;
    __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg 
        = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg;
    __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s 
        = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s;
    __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state 
        = vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1 = 0U;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r;
    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r;
    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state 
        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0 = 0U;
    __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg 
        = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0 = 0U;
    __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg 
        = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg;
    __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0U;
    __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0U;
    if (vlSelfRef.ts_m_axis_tready) {
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.ts_m_axis_tready) | (0U 
                                                != 
                                                (1U 
                                                 & ((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg)) 
                                                    >> 1U))))) {
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[0U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][0U];
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[1U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][1U];
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[2U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][2U];
        __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.ts_m_axis_tready) | (0U 
                                                != 
                                                (3U 
                                                 & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[0U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg))][0U];
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[1U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg))][1U];
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[2U] 
            = vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg))][2U];
        __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1 = 1U;
        if (((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg) 
             != (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_commit_reg))) {
            vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg)));
            __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg));
        }
    }
    if (vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered.tready) {
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered.tready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[0U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][0U];
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[1U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][1U];
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[2U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][2U];
        __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered.tready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[0U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg))][0U];
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[1U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg))][1U];
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[2U] 
            = vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg))][2U];
        __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 1U;
        if (((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg) 
             != (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_commit_reg))) {
            vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg)));
            __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
        }
    }
    if (vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered.tready) {
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered.tready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[0U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][0U];
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[1U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][1U];
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[2U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][2U];
        __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered.tready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[0U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg))][0U];
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[1U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg))][1U];
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[2U] 
            = vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem
            [(1U & (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg))][2U];
        __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 1U;
        if (((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg) 
             != (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_commit_reg))) {
            vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg)));
            __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg));
        }
    }
    vlSelfRef.ptp_ts_top__DOT__tx_ts_ready_r = ((IData)(vlSelfRef.axis_resetn) 
                                                & (((0U 
                                                     != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state)) 
                                                    & (IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx.tready)) 
                                                   & (2U 
                                                      == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))));
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg = 0U;
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg = 0U;
    }
    vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (__VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[0U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg__v1[2U];
    }
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.i_ptp_cmd_load) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_tgl 
                = (1U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_tgl)));
        }
        if (vlSelfRef.i_ptp_cmd_adjust) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl 
                = (1U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl)));
        }
        if (vlSelfRef.i_ptp_cmd_snapshot) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl 
                = (1U & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl)));
        }
        if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc) {
            if (vlSelfRef.s_axis_rx_tlast) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter = 0U;
            } else if ((0x30U >= (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter))) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter 
                    = (0x0000007fU & ((IData)(8U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)));
            }
        }
        if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc) {
            if (vlSelfRef.s_axis_tx_tlast) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter = 0U;
            } else if ((0x30U >= (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter))) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter 
                    = (0x0000007fU & ((IData)(8U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)));
            }
        }
        __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state 
            = Vptp_ts_top__ConstPool__TABLE_hd45f40b9_0
            [(((((2U & (vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                        >> 7U)) | (IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo.tready)) 
                << 6U) | (((2U & (vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                  >> 7U)) | (1U & ((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U))) 
                          << 4U)) | ((8U & ((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                            << 2U)) 
                                     | (((IData)(vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served) 
                                         << 2U) | (IData)(vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state))))];
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s 
            = ((6U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s) 
                      << 1U)) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts));
        if ((1U & VL_REDXOR_4((6U & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s))))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg = 1U;
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg 
                = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_val_ts;
        } else {
            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg = 0U;
        }
    } else {
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__load_tgl = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter = 0U;
        __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg = 0ULL;
        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg = 0U;
    }
    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s 
        = __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s;
    vlSelfRef.ts_m_axis_tvalid = (1U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U));
    vlSelfRef.ts_m_axis_tdata = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                  << 0x00000020U) | (QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][0U])));
    vlSelfRef.ts_m_axis_tlast = (1U & (vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                       >> 8U));
    vlSelfRef.ts_m_axis_tkeep = (0x000000ffU & vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg[1U][2U]);
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo.tready) 
         & (IData)(vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid))) {
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[0U] 
            = (IData)(vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata);
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[1U] 
            = (IData)((vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata 
                       >> 0x00000020U));
        __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[2U] 
            = ((((IData)(vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast) 
                 | (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mark_frame_reg)) 
                << 8U) | (IData)(vlSelfRef.ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep));
        __VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0 
            = (1U & (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg));
        __VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg)));
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_commit_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg)));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_rx.tready) 
         & (0U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state)))) {
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[0U] 
            = (IData)(((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))
                        ? (QData)((IData)((2U | (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq) 
                                                  << 8U) 
                                                 | ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt) 
                                                    << 4U)))))
                        : vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts));
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[1U] 
            = (IData)((((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))
                         ? (QData)((IData)((2U | (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq) 
                                                   << 8U) 
                                                  | ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt) 
                                                     << 4U)))))
                         : vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts) 
                       >> 0x00000020U));
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[2U] 
            = ((0x00000100U & __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[2U]) 
               | (0x000000ffU & (7U | (- (IData)((2U 
                                                  != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state)))))));
        __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[2U] 
            = ((0x000000ffU & __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[2U]) 
               | (0x000001ffU & (((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mark_frame_reg) 
                                  | (2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))) 
                                 << 8U)));
        __VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0 
            = (1U & (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg));
        __VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg)));
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_commit_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg)));
    }
    if (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx.tready) 
         & (0U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state)))) {
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[0U] 
            = (IData)(((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))
                        ? (QData)((IData)((3U | (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq) 
                                                  << 8U) 
                                                 | ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt) 
                                                    << 4U)))))
                        : vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts));
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[1U] 
            = (IData)((((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))
                         ? (QData)((IData)((3U | (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq) 
                                                   << 8U) 
                                                  | ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt) 
                                                     << 4U)))))
                         : vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts) 
                       >> 0x00000020U));
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[2U] 
            = ((0x00000100U & __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[2U]) 
               | (0x000000ffU & (7U | (- (IData)((2U 
                                                  != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state)))))));
        __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[2U] 
            = ((0x000000ffU & __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[2U]) 
               | (0x000001ffU & (((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mark_frame_reg) 
                                  | (2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))) 
                                 << 8U)));
        __VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0 
            = (1U & (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg));
        __VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0 = 1U;
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg)));
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_commit_reg 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg)));
    }
    if (vlSelfRef.axis_resetn) {
        if (((((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered.tready) 
               & ((IData)(vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)) & (vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                             >> 8U)) | (((IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered.tready) 
                                         & ((IData)(vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg) 
                                            >> 1U)) 
                                        & (vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                                           >> 8U)))) {
            vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served 
                = (1U != (IData)(vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state));
        }
        __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = 0U;
        if ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))) {
            if ((0U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt;
                __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = 1U;
                __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))) {
            if (vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_rx.tready) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 2U;
            }
        } else if ((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state))) {
            if (vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_rx.tready) {
                if ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl))) {
                    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 0U;
                } else {
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts;
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq;
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt;
                    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = 1U;
                    __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 1U;
                }
            }
        } else {
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 0U;
        }
        __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = 0U;
        if ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))) {
            if ((0U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt 
                    = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt;
                __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = 1U;
                __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))) {
            if (vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx.tready) {
                __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 2U;
            }
        } else if ((2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state))) {
            if (vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx.tready) {
                if ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl))) {
                    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 0U;
                } else {
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts;
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq;
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt 
                        = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt;
                    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = 1U;
                    __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 1U;
                }
            }
        } else {
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 0U;
        }
        if ((2U == (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push) 
                     << 1U) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r)))) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)));
        } else if ((1U == (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push) 
                            << 1U) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r)))) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl 
                = (3U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl) 
                         - (IData)(1U)));
        }
        if (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push) 
             & ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)) 
                | ((1U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)) 
                   & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r))))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_sop;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type;
        } else if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_sop;
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id;
            __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type;
        } else if (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r) 
                    & (2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt;
        }
        if ((2U == (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push) 
                     << 1U) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r)))) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)));
        } else if ((1U == (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push) 
                            << 1U) | (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r)))) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl 
                = (3U & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl) 
                         - (IData)(1U)));
        }
        if (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push) 
             & ((0U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)) 
                | ((1U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)) 
                   & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r))))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_sop;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type;
        } else if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push) {
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_sop;
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id;
            __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type;
        } else if (((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r) 
                    & (2U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)))) {
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq;
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt 
                = vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt;
        }
        if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc) {
            if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_sop 
                    = (vlSelfRef.o_ptp_now - (QData)((IData)(vlSelfRef.i_ptp_ingress_lat)));
            }
            if (((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                if ((0x8100U != ((0x0000ff00U & ((IData)(
                                                         (vlSelfRef.s_axis_rx_tdata 
                                                          >> 0x00000020U)) 
                                                 << 8U)) 
                                 | (0x000000ffU & (IData)(
                                                          (vlSelfRef.s_axis_rx_tdata 
                                                           >> 0x00000028U)))))) {
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match 
                        = (0x88f7U == ((0x0000ff00U 
                                        & ((IData)(
                                                   (vlSelfRef.s_axis_rx_tdata 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                                       | (0x000000ffU 
                                          & (IData)(
                                                    (vlSelfRef.s_axis_rx_tdata 
                                                     >> 0x00000028U)))));
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type 
                        = (0x0000000fU & (IData)((vlSelfRef.s_axis_rx_tdata 
                                                  >> 0x00000030U)));
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged)) 
                 & (0x10U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match 
                    = (0x88f7U == ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_rx_tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_rx_tdata 
                                                             >> 8U)))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type 
                    = (0x0000000fU & (IData)((vlSelfRef.s_axis_rx_tdata 
                                              >> 0x00000010U)));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged))) 
                 & (0x28U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)((vlSelfRef.s_axis_rx_tdata 
                                                >> 0x00000020U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_rx_tdata 
                                                             >> 0x00000028U))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged)) 
                 & (0x30U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_rx_tdata) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_rx_tdata 
                                                             >> 8U))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 1U;
            }
            if (((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged 
                    = (0x8100U == ((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.s_axis_rx_tdata 
                                                            >> 0x00000020U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_rx_tdata 
                                                             >> 0x00000028U)))));
            }
            if (vlSelfRef.s_axis_rx_tlast) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged = 0U;
            }
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet 
                = vlSelfRef.s_axis_rx_tlast;
        }
        if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc) {
            if (vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_sop 
                    = (vlSelfRef.o_ptp_now + (QData)((IData)(vlSelfRef.i_ptp_egress_lat)));
            }
            if (((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                if ((0x8100U != ((0x0000ff00U & ((IData)(
                                                         (vlSelfRef.s_axis_tx_tdata 
                                                          >> 0x00000020U)) 
                                                 << 8U)) 
                                 | (0x000000ffU & (IData)(
                                                          (vlSelfRef.s_axis_tx_tdata 
                                                           >> 0x00000028U)))))) {
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match 
                        = (0x88f7U == ((0x0000ff00U 
                                        & ((IData)(
                                                   (vlSelfRef.s_axis_tx_tdata 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                                       | (0x000000ffU 
                                          & (IData)(
                                                    (vlSelfRef.s_axis_tx_tdata 
                                                     >> 0x00000028U)))));
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type 
                        = (0x0000000fU & (IData)((vlSelfRef.s_axis_tx_tdata 
                                                  >> 0x00000030U)));
                    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged)) 
                 & (0x10U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match 
                    = (0x88f7U == ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_tx_tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_tx_tdata 
                                                             >> 8U)))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type 
                    = (0x0000000fU & (IData)((vlSelfRef.s_axis_tx_tdata 
                                              >> 0x00000010U)));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged))) 
                 & (0x28U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)((vlSelfRef.s_axis_tx_tdata 
                                                >> 0x00000020U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_tx_tdata 
                                                             >> 0x00000028U))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged)) 
                 & (0x30U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_tx_tdata) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_tx_tdata 
                                                             >> 8U))));
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 1U;
            }
            if (((~ (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged 
                    = (0x8100U == ((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.s_axis_tx_tdata 
                                                            >> 0x00000020U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_tx_tdata 
                                                             >> 0x00000028U)))));
            }
            if (vlSelfRef.s_axis_tx_tlast) {
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 0U;
                vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged = 0U;
            }
            vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet 
                = vlSelfRef.s_axis_tx_tlast;
        }
    } else {
        vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl = 0U;
        __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged = 0U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet = 1U;
        vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet = 1U;
    }
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg = 0U;
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg = 0U;
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0U;
        __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_commit_reg = 0U;
        __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_commit_reg = 0U;
        __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mark_frame_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mark_frame_reg = 0U;
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mark_frame_reg = 0U;
    }
    vlSelfRef.o_tx_ts_ready = vlSelfRef.ptp_ts_top__DOT__tx_ts_ready_r;
    vlSelfRef.o_ptp_tod_rd_valid = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg;
    vlSelfRef.o_ptp_tod_rd = vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg;
    vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (__VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[0U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1[2U];
    }
    if (__VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[1U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (__VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][0U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][1U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[0U][2U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1[2U];
    }
    vlSelfRef.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state 
        = __Vdly__ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state;
    if (__VdlySet__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0) {
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0][0U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0][1U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0][2U] 
            = __VdlyVal__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem__v0[2U];
    }
    vlSelfRef.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg 
        = __Vdly__ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg;
    if (__VdlySet__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0) {
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0][0U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0][1U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0][2U] 
            = __VdlyVal__ptp_ts_top__DOT__rx_ts_buffer__DOT__mem__v0[2U];
    }
    vlSelfRef.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg 
        = __Vdly__ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg;
    if (__VdlySet__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0) {
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0][0U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[0U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0][1U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[1U];
        vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__mem[__VdlyDim0__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0][2U] 
            = __VdlyVal__ptp_ts_top__DOT__tx_ts_buffer__DOT__mem__v0[2U];
    }
    vlSelfRef.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg 
        = __Vdly__ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg;
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
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push 
        = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc) 
                & (IData)(vlSelfRef.s_axis_rx_tlast)) 
               & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match)) 
             & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl)));
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push 
        = (((((((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc) 
                & (IData)(vlSelfRef.s_axis_tx_tlast)) 
               & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match)) 
             & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl)));
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter;
    vlSelfRef.ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter 
        = __Vdly__ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter;
}

void Vptp_ts_top___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vptp_ts_top___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vptp_ts_top___024root___eval_phase__act(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_phase__act\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((((IData)(vlSelfRef.gtx_clk) 
                                                           & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1))) 
                                                          << 1U) 
                                                         | ((IData)(vlSelfRef.axis_clk) 
                                                            & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__1))))));
        vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__1 
            = vlSelfRef.axis_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1 
            = vlSelfRef.gtx_clk;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vptp_ts_top___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vptp_ts_top___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vptp_ts_top___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf);
void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf);

bool Vptp_ts_top___024root___eval_phase__nba(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_phase__nba\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vptp_ts_top___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vptp_ts_top___024root___nba_sequent__TOP__0(vlSelf);
            }
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vptp_ts_top___024root___nba_sequent__TOP__1(vlSelf);
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_rx));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_m_axis_tx));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_tx_buffered));
                Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0((&vlSymsp->TOP__ptp_ts_top__DOT__ts_rx_buffered));
            }
            if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _nba_sequent__TOP__2
                    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts 
                        = vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts;
                    if (vlSelfRef.gtx_resetn) {
                        if (vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot_valid) {
                            vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_val_ts 
                                = vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot;
                        }
                        if ((1U & VL_REDXOR_32((3U 
                                                & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_s) 
                                                   >> 1U))))) {
                            vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot 
                                = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U])) 
                                    << 0x00000028U) 
                                   | (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U])) 
                                       << 8U) | ((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U])) 
                                                 >> 0x00000018U)));
                        }
                    } else {
                        vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_val_ts = 0ULL;
                        vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot = 0ULL;
                    }
                    vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot_valid 
                        = ((IData)(vlSelfRef.gtx_resetn) 
                           && (1U & VL_REDXOR_32((3U 
                                                  & ((IData)(vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_s) 
                                                     >> 1U)))));
                    vlSelfRef.ptp_ts_top__DOT__ptp_sync__DOT__snap_s 
                        = vlSelfRef.__Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s;
                    vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U] 
                        = vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[0U];
                    vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U] 
                        = vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[1U];
                    vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U] 
                        = vlSelfRef.__Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc[2U];
                    vlSelfRef.o_ptp_now = (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[2U])) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[1U])) 
                                               << 8U) 
                                              | ((QData)((IData)(vlSelfRef.ptp_ts_top__DOT__ts_counter__DOT__acc[0U])) 
                                                 >> 0x00000018U)));
                }
            }
        }
        Vptp_ts_top___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vptp_ts_top___024root___eval(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vptp_ts_top___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv", 31, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vptp_ts_top___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vptp_ts_top___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv", 31, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vptp_ts_top___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv", 31, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vptp_ts_top___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vptp_ts_top___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vptp_ts_top___024root___eval_debug_assertions(Vptp_ts_top___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vptp_ts_top___024root___eval_debug_assertions\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.gtx_clk & 0xfeU)))) {
        Verilated::overWidthError("gtx_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.gtx_resetn & 0xfeU)))) {
        Verilated::overWidthError("gtx_resetn");
    }
    if (VL_UNLIKELY(((vlSelfRef.axis_clk & 0xfeU)))) {
        Verilated::overWidthError("axis_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.axis_resetn & 0xfeU)))) {
        Verilated::overWidthError("axis_resetn");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ptp_enable & 0xfeU)))) {
        Verilated::overWidthError("i_ptp_enable");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ptp_cmd_load & 0xfeU)))) {
        Verilated::overWidthError("i_ptp_cmd_load");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ptp_cmd_adjust & 0xfeU)))) {
        Verilated::overWidthError("i_ptp_cmd_adjust");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ptp_cmd_snapshot 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_ptp_cmd_snapshot");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_tx_tvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axis_tx_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_tx_tlast & 0xfeU)))) {
        Verilated::overWidthError("s_axis_tx_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_tx_tready & 0xfeU)))) {
        Verilated::overWidthError("m_axis_tx_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_rx_tvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axis_rx_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_rx_tlast & 0xfeU)))) {
        Verilated::overWidthError("s_axis_rx_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_rx_tready & 0xfeU)))) {
        Verilated::overWidthError("m_axis_rx_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.ts_m_axis_tready & 0xfeU)))) {
        Verilated::overWidthError("ts_m_axis_tready");
    }
}
#endif  // VL_DEBUG
