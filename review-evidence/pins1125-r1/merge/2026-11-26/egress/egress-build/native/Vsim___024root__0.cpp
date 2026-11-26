// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim___024root___eval_triggers_vec__ico(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_triggers_vec__ico\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                    ((((((((IData)(vlSelfRef.sys_reset) 
                                                           != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_reset__0)) 
                                                          << 3U) 
                                                         | (((IData)(vlSelfRef.sys_clk) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__0)) 
                                                            << 2U)) 
                                                        | ((((IData)(vlSelfRef.sim_trace) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sim_trace__0)) 
                                                            << 1U) 
                                                           | ((IData)(vlSelfRef.serial_source_ready) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__serial_source_ready__0)))) 
                                                       << 0x00000014U) 
                                                      | ((((((IData)(vlSelfRef.serial_sink_valid) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__serial_sink_valid__0)) 
                                                            << 3U) 
                                                           | (((IData)(vlSelfRef.serial_sink_data) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__serial_sink_data__0)) 
                                                              << 2U)) 
                                                          | ((((IData)(vlSelfRef.milan_clk) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__milan_clk__0)) 
                                                              << 1U) 
                                                             | ((IData)(vlSelfRef.mbx_tx_ready) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_tx_ready__0)))) 
                                                         << 0x00000010U)) 
                                                     | ((((((((IData)(vlSelfRef.mbx_rx_valid) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_valid__0)) 
                                                             << 3U) 
                                                            | (((IData)(vlSelfRef.mbx_rx_last) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_last__0)) 
                                                               << 2U)) 
                                                           | ((((IData)(vlSelfRef.mbx_rx_if) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_if__0)) 
                                                               << 1U) 
                                                              | ((IData)(vlSelfRef.mbx_rx_data) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_data__0)))) 
                                                          << 0x0000000cU) 
                                                         | ((((((IData)(vlSelfRef.mbx_link_up) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_link_up__0)) 
                                                               << 3U) 
                                                              | ((vlSelfRef.mbx_gm_id 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__mbx_gm_id__0) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.mbx_gm_change) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_gm_change__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.mbx_domain) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_domain__0)))) 
                                                            << 8U)) 
                                                        | (((((((IData)(vlSelfRef.mbx_avb_chg) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_avb_chg__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.mbx_asp_chg) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_asp_chg__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.mbx_amap_wr) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mbx_amap_wr__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.flash_tx_ready) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__flash_tx_ready__0)))) 
                                                            << 4U) 
                                                           | (((((IData)(vlSelfRef.flash_rx_valid) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__flash_rx_valid__0)) 
                                                                << 3U) 
                                                               | ((vlSelfRef.flash_rx_data 
                                                                   != vlSelfRef.__Vtrigprevexpr___TOP__flash_rx_data__0) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.audio_tdm_clk) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__audio_tdm_clk__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.audio_clk) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__audio_clk__0)))))))));
    vlSelfRef.__Vtrigprevexpr___TOP__audio_clk__0 = vlSelfRef.audio_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__audio_tdm_clk__0 
        = vlSelfRef.audio_tdm_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__flash_rx_data__0 
        = vlSelfRef.flash_rx_data;
    vlSelfRef.__Vtrigprevexpr___TOP__flash_rx_valid__0 
        = vlSelfRef.flash_rx_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__flash_tx_ready__0 
        = vlSelfRef.flash_tx_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_amap_wr__0 
        = vlSelfRef.mbx_amap_wr;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_asp_chg__0 
        = vlSelfRef.mbx_asp_chg;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_avb_chg__0 
        = vlSelfRef.mbx_avb_chg;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_domain__0 
        = vlSelfRef.mbx_domain;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_gm_change__0 
        = vlSelfRef.mbx_gm_change;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_gm_id__0 = vlSelfRef.mbx_gm_id;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_link_up__0 
        = vlSelfRef.mbx_link_up;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_data__0 
        = vlSelfRef.mbx_rx_data;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_if__0 = vlSelfRef.mbx_rx_if;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_last__0 
        = vlSelfRef.mbx_rx_last;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_rx_valid__0 
        = vlSelfRef.mbx_rx_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__mbx_tx_ready__0 
        = vlSelfRef.mbx_tx_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__milan_clk__0 = vlSelfRef.milan_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__serial_sink_data__0 
        = vlSelfRef.serial_sink_data;
    vlSelfRef.__Vtrigprevexpr___TOP__serial_sink_valid__0 
        = vlSelfRef.serial_sink_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__serial_source_ready__0 
        = vlSelfRef.serial_source_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__sim_trace__0 = vlSelfRef.sim_trace;
    vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__0 = vlSelfRef.sys_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__sys_reset__0 = vlSelfRef.sys_reset;
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
    }
}

bool Vsim___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___trigger_anySet__ico\n"); );
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

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsim___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG
void Vsim_sim___ico_sequent__TOP__sim__0(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__1(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__2(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__3(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__4(Vsim_sim* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ico_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__5(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__6(Vsim_sim* vlSelf);
void Vsim_sim___ico_sequent__TOP__sim__7(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__0(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__1(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__2(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__3(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__4(Vsim_sim* vlSelf);
void Vsim_sim___ico_comb__TOP__sim__5(Vsim_sim* vlSelf);

bool Vsim___024root___eval_phase__ico(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_phase__ico\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vsim___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vsim___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vsim___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        {
            // Inlined CFunc: _eval_ico
            if ((0x0000000000004000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__0((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000100000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__1((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000001000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__2((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000008000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__3((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000010000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__4((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000800000ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ico_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
            }
            if ((0x0000000000000800ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_sequent__TOP__sim__5((&vlSymsp->TOP__sim));
                Vsim_sim___ico_sequent__TOP__sim__6((&vlSymsp->TOP__sim));
                Vsim_sim___ico_sequent__TOP__sim__7((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000000c00ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_comb__TOP__sim__0((&vlSymsp->TOP__sim));
                Vsim_sim___ico_comb__TOP__sim__1((&vlSymsp->TOP__sim));
                Vsim_sim___ico_comb__TOP__sim__2((&vlSymsp->TOP__sim));
                Vsim_sim___ico_comb__TOP__sim__3((&vlSymsp->TOP__sim));
                Vsim_sim___ico_comb__TOP__sim__4((&vlSymsp->TOP__sim));
            }
            if ((0x0000000000000900ULL & vlSelfRef.__VicoTriggered[0U])) {
                Vsim_sim___ico_comb__TOP__sim__5((&vlSymsp->TOP__sim));
            }
        }
    }
    return (__VicoExecute);
}

bool Vsim___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___trigger_anySet__act\n"); );
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

void Vsim___024root___nba_sequent__TOP__0(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___nba_sequent__TOP__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.serial_sink_ready = (0x10U != (IData)(vlSymsp->TOP__sim.__PVT__soc_rx_fifo_level0));
    vlSelfRef.serial_source_data = (0x000000ffU & (IData)(vlSymsp->TOP__sim.__PVT__storage_1_dat1));
    vlSelfRef.flash_cs = vlSymsp->TOP__sim.__PVT__flashboundary_cs;
    vlSelfRef.mbx_tx_data = (0x000000ffU & (vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__pw_r 
                                            >> ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r) 
                                                << 3U)));
    vlSelfRef.mbx_tx_if = (1U & (vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r 
                                 >> 0x00000010U));
    vlSelfRef.mbx_tx_ch = vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
    vlSelfRef.mbx_tx_valid = (6U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__st_r));
    vlSelfRef.mbx_ms_tick = vlSymsp->TOP__sim.__PVT__add_devices_stimulusmailbox_ms_tick;
    vlSelfRef.mbx_host_rdata = ((8U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                 ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r
                                 : ((4U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                     ? ((2U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                         ? ((1U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                             ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r
                                             : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__srp_rx_rdata_w)
                                         : ((1U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                             ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__maap_rx_rdata_w
                                             : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__aecp_rx_rdata_w))
                                     : ((2U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                         ? ((1U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                             ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__acmp_rx_rdata_w
                                             : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__adp_rx_rdata_w)
                                         : ((1U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                             ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__evt_rdata_w
                                             : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r))));
    vlSelfRef.mbx_host_ack = vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__ack_r;
    vlSelfRef.serial_source_valid = vlSymsp->TOP__sim.__PVT__soc_tx_fifo_readable;
    vlSelfRef.mbx_rx_ready = ((0U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                              & (4U > (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r)));
    vlSelfRef.flash_rx_ready = (1U & (~ ((IData)(vlSymsp->TOP__sim.__PVT__add_devices_rx_pipe_valid_source_valid) 
                                         & (IData)(vlSymsp->TOP__sim.__PVT__add_devices_rx_pipe_ready_valid))));
    vlSelfRef.flash_tx_valid = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_valid;
    vlSelfRef.flash_tx_data = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_data;
    vlSelfRef.flash_tx_len = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_len;
    vlSelfRef.flash_tx_width = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_width;
    vlSelfRef.mbx_tx_last = ((IData)(vlSelfRef.mbx_tx_valid) 
                             & (1U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__left_r)));
}

void Vsim_sim___nba_sequent__TOP__sim__0(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__1(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__2(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__3(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__4(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__5(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__6(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__7(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__8(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__9(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__10(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__11(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__12(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__13(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__14(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__15(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__16(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__17(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__18(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__19(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__20(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__21(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__22(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__23(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__24(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__25(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__26(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__27(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__28(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__29(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__30(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__31(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__32(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__33(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__34(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__35(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__36(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__37(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__38(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__39(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__40(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__41(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__42(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__43(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__44(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__45(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__46(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__47(Vsim_sim* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_RegFileMem___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga__0(Vsim_RegFileMem* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__11(Vsim_VexiiRiscv* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__48(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__49(Vsim_sim* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__12(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__12(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__13(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__13(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__14(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__15(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__14(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__16(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__15(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__16(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__17(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__18(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__19(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__20(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__21(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__22(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__23(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__24(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__25(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__26(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__27(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__28(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__29(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__30(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__31(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__32(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__33(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__34(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__35(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__36(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__37(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__38(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__39(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__40(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__41(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__42(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__43(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__44(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__45(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__46(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__47(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__48(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__49(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__50(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__51(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__52(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__53(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__54(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__17(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__55(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__18(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__19(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__56(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__50(Vsim_sim* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__20(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__58(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__0(Vsim_sim* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__59(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__21(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__60(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__22(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__1(Vsim_sim* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__2(Vsim_sim* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__3(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__51(Vsim_sim* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__61(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7(Vsim_VexiiRiscv* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__62(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__4(Vsim_sim* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__5(Vsim_sim* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__6(Vsim_sim* vlSelf);
void Vsim_sim___nba_comb__TOP__sim__7(Vsim_sim* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__63(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);

void Vsim___024root___eval_nba(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_nba\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_sim___nba_sequent__TOP__sim__0((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__1((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__2((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__3((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__4((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__5((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__6((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__7((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__8((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__9((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__10((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__11((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__12((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__13((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__14((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__15((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__16((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__17((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__18((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__19((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__20((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__21((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__22((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__23((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__24((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__25((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__26((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__27((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__28((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__29((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__30((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__31((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__32((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__33((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__34((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__35((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__36((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__37((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__38((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__39((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__40((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__41((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__42((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__43((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__44((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__45((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__46((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__47((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_RegFileMem___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga));
        Vsim___024root___nba_sequent__TOP__0(vlSelf);
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__11((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_sim___nba_sequent__TOP__sim__48((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__49((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__12((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__12((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__13((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__13((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__14((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__15((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__14((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__16((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__15((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__16((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__17((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__18((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__19((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__20((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__21((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__22((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__23((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__24((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__25((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__26((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__27((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__28((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__29((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__30((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__31((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__32((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__33((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__34((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__35((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__36((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__37((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__38((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__39((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__40((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__41((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__42((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__43((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__44((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__45((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__46((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__47((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__48((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__49((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__50((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__51((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__52((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__53((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__54((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__17((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__55((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__18((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__19((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__56((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_sim___nba_sequent__TOP__sim__50((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__20((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__58((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_sim___nba_comb__TOP__sim__0((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__59((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__21((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__60((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__22((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
    if ((0x000000000000000bULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_sim___nba_comb__TOP__sim__1((&vlSymsp->TOP__sim));
        Vsim_sim___nba_comb__TOP__sim__2((&vlSymsp->TOP__sim));
        Vsim_sim___nba_comb__TOP__sim__3((&vlSymsp->TOP__sim));
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_sim___nba_sequent__TOP__sim__51((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__61((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        {
            // Inlined CFunc: _nba_sequent__TOP__1
            vlSelfRef.mbx_host_we = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma8;
            vlSelfRef.mbx_host_wdata = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma10;
        }
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((0x0000000000000011ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__62((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
    if ((0x000000000000000bULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_sim___nba_comb__TOP__sim__4((&vlSymsp->TOP__sim));
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_sim___nba_comb__TOP__sim__5((&vlSymsp->TOP__sim));
        Vsim_sim___nba_comb__TOP__sim__6((&vlSymsp->TOP__sim));
        Vsim_sim___nba_comb__TOP__sim__7((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        {
            // Inlined CFunc: _nba_comb__TOP__0
            vlSelfRef.mbx_host_addr = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma9;
            vlSelfRef.mbx_host_req = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma7;
        }
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__63((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
    }
}

void Vsim___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vsim___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vsim___024root___eval_phase__act(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_phase__act\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        CData/*0:0*/ __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_h8ac6c1f5__0;
        __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_h8ac6c1f5__0 = 0;
        __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_h8ac6c1f5__0 
            = (0x40U != (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_holder_counter));
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        (((__Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_h8ac6c1f5__0 
                                                           & (~ (IData)(vlSelfRef.__Vtrigprevexpr_h8ac6c1f5__1))) 
                                                          << 4U) 
                                                         | (((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1__0))) 
                                                              << 3U) 
                                                             | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1__0))) 
                                                                << 2U)) 
                                                            | ((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__litex_reset) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__litex_reset__0))) 
                                                                << 1U) 
                                                               | ((IData)(vlSelfRef.sys_clk) 
                                                                  & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1))))))));
        vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1 
            = vlSelfRef.sys_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__litex_reset__0 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__litex_reset;
        vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1__0 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1;
        vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1__0 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1;
        vlSelfRef.__Vtrigprevexpr_h8ac6c1f5__1 = __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_h8ac6c1f5__0;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vsim___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vsim___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vsim___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vsim___024root___eval_phase__nba(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_phase__nba\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vsim___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vsim___024root___eval_nba(vlSelf);
        Vsim___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vsim___024root___eval(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vsim___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("$VALIDATION_STORAGE/pins1125-candidate-0923/egress/egress-build/gateware/sim.v", 23, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vsim___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vsim___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("$VALIDATION_STORAGE/pins1125-candidate-0923/egress/egress-build/gateware/sim.v", 23, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vsim___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("$VALIDATION_STORAGE/pins1125-candidate-0923/egress/egress-build/gateware/sim.v", 23, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vsim___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vsim___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vsim___024root___eval_debug_assertions(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_debug_assertions\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.audio_clk & 0xfeU)))) {
        Verilated::overWidthError("audio_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.audio_tdm_clk & 0xfeU)))) {
        Verilated::overWidthError("audio_tdm_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.flash_rx_valid & 0xfeU)))) {
        Verilated::overWidthError("flash_rx_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.flash_tx_ready & 0xfeU)))) {
        Verilated::overWidthError("flash_tx_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_amap_wr & 0xfeU)))) {
        Verilated::overWidthError("mbx_amap_wr");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_asp_chg & 0xfeU)))) {
        Verilated::overWidthError("mbx_asp_chg");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_avb_chg & 0xfeU)))) {
        Verilated::overWidthError("mbx_avb_chg");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_gm_change & 0xfeU)))) {
        Verilated::overWidthError("mbx_gm_change");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_link_up & 0xfeU)))) {
        Verilated::overWidthError("mbx_link_up");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_rx_if & 0xfeU)))) {
        Verilated::overWidthError("mbx_rx_if");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_rx_last & 0xfeU)))) {
        Verilated::overWidthError("mbx_rx_last");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_rx_valid & 0xfeU)))) {
        Verilated::overWidthError("mbx_rx_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.mbx_tx_ready & 0xfeU)))) {
        Verilated::overWidthError("mbx_tx_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.milan_clk & 0xfeU)))) {
        Verilated::overWidthError("milan_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.serial_sink_valid & 0xfeU)))) {
        Verilated::overWidthError("serial_sink_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.serial_source_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("serial_source_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.sim_trace & 0xfeU)))) {
        Verilated::overWidthError("sim_trace");
    }
    if (VL_UNLIKELY(((vlSelfRef.sys_clk & 0xfeU)))) {
        Verilated::overWidthError("sys_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.sys_reset & 0xfeU)))) {
        Verilated::overWidthError("sys_reset");
    }
}
#endif  // VL_DEBUG
