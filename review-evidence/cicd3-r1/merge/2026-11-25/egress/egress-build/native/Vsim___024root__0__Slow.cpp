// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_sim___eval_static__TOP__sim(Vsim_sim* vlSelf);

VL_ATTR_COLD void Vsim___024root___eval_static(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_static\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vsim_sim___eval_static__TOP__sim((&vlSymsp->TOP__sim));
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
    vlSelfRef.__Vtrigprevexpr___TOP__sys_clk__1 = vlSelfRef.sys_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__litex_reset__0 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__litex_reset;
    vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1__0 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1;
    vlSelfRef.__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1__0 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1;
    vlSelfRef.__Vtrigprevexpr_h8ac6c1f5__1 = (0x40U 
                                              != (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_holder_counter));
}

VL_ATTR_COLD void Vsim_sim___eval_initial__TOP__sim(Vsim_sim* vlSelf);

VL_ATTR_COLD void Vsim___024root___eval_initial(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_initial\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vsim_sim___eval_initial__TOP__sim((&vlSymsp->TOP__sim));
}

VL_ATTR_COLD void Vsim___024root___eval_final(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_final\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsim___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vsim___024root___eval_phase__stl(Vsim___024root* vlSelf);

VL_ATTR_COLD void Vsim___024root___eval_settle(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_settle\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vsim___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("$VALIDATION_STORAGE/cicd3-candidate-0923/egress/egress-build/gateware/sim.v", 23, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vsim___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vsim___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsim___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vsim___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vsim___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__0(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__1(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__2(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__3(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__4(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__5(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__6(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__7(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__8(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__9(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__10(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__41(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__42(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__43(Vsim_sim* vlSelf);
void Vsim_sim___nba_sequent__TOP__sim__44(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__15(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__16(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__17(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9(Vsim_VexiiRiscv* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__18(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__19(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__20(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__21(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__22(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__23(Vsim_sim* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf);
VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10(Vsim_VexiiRiscv* vlSelf);

VL_ATTR_COLD void Vsim___024root___eval_stl(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_stl\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        {
            // Inlined CFunc: _stl_sequent__TOP__0
            vlSelfRef.mbx_host_ack = vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__ack_r;
            vlSelfRef.serial_source_valid = vlSymsp->TOP__sim.__PVT__soc_tx_fifo_readable;
            vlSelfRef.serial_sink_ready = (0x10U != (IData)(vlSymsp->TOP__sim.__PVT__soc_rx_fifo_level0));
            vlSelfRef.serial_source_data = (0x000000ffU 
                                            & (IData)(vlSymsp->TOP__sim.__PVT__storage_1_dat1));
            vlSelfRef.mbx_tx_if = (1U & (vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r 
                                         >> 0x00000010U));
            vlSelfRef.mbx_tx_ch = vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
            vlSelfRef.mbx_ms_tick = vlSymsp->TOP__sim.__PVT__add_devices_stimulusmailbox_ms_tick;
            vlSelfRef.flash_cs = vlSymsp->TOP__sim.__PVT__flashboundary_cs;
            vlSelfRef.mbx_tx_data = (0x000000ffU & 
                                     (vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__pw_r 
                                      >> ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r) 
                                          << 3U)));
            vlSelfRef.flash_rx_ready = (1U & (~ ((IData)(vlSymsp->TOP__sim.__PVT__add_devices_rx_pipe_valid_source_valid) 
                                                 & (IData)(vlSymsp->TOP__sim.__PVT__add_devices_rx_pipe_ready_valid))));
            vlSelfRef.mbx_tx_valid = (6U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__st_r));
            vlSelfRef.mbx_rx_ready = ((0U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                                      & (4U > (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r)));
            vlSelfRef.mbx_host_rdata = ((8U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                         ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r
                                         : ((4U & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                             ? ((2U 
                                                 & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                 ? 
                                                ((1U 
                                                  & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                  ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r
                                                  : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__srp_rx_rdata_w)
                                                 : 
                                                ((1U 
                                                  & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                  ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__maap_rx_rdata_w
                                                  : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__aecp_rx_rdata_w))
                                             : ((2U 
                                                 & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                 ? 
                                                ((1U 
                                                  & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                  ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__acmp_rx_rdata_w
                                                  : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__adp_rx_rdata_w)
                                                 : 
                                                ((1U 
                                                  & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__rsel_r))
                                                  ? vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__evt_rdata_w
                                                  : vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__reg_rdata_r))));
            vlSelfRef.mbx_tx_last = ((IData)(vlSelfRef.mbx_tx_valid) 
                                     & (1U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx__DOT__u_tx__DOT__left_r)));
        }
        Vsim_sim___stl_sequent__TOP__sim__0((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__1((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__2((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__3((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__4((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__5((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__6((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__7((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__8((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__9((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__10((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__41((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__42((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__43((&vlSymsp->TOP__sim));
        Vsim_sim___nba_sequent__TOP__sim__44((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__15((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__16((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__17((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
        {
            // Inlined CFunc: _stl_sequent__TOP__1
            vlSelfRef.flash_tx_valid = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_valid;
            vlSelfRef.flash_tx_data = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_data;
            vlSelfRef.flash_tx_len = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_len;
            vlSelfRef.flash_tx_width = vlSymsp->TOP__sim.__PVT__add_devices_tx_pipe_ready_source_payload_width;
            vlSelfRef.mbx_host_we = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma8;
        }
        Vsim_sim___stl_sequent__TOP__sim__18((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__19((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__20((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__21((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__22((&vlSymsp->TOP__sim));
        Vsim_sim___stl_sequent__TOP__sim__23((&vlSymsp->TOP__sim));
        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952));
        {
            // Inlined CFunc: _stl_sequent__TOP__2
            vlSelfRef.mbx_host_wdata = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma10;
            vlSelfRef.mbx_host_addr = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma9;
            vlSelfRef.mbx_host_req = vlSymsp->TOP__sim.__PVT__add_devices_ctrlmailboxdma7;
        }
        Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10((&vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core));
    }
}

VL_ATTR_COLD bool Vsim___024root___eval_phase__stl(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___eval_phase__stl\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vsim___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vsim___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vsim___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vsim___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsim___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vsim___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( audio_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( audio_tdm_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( flash_rx_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( flash_rx_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( flash_tx_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( mbx_amap_wr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( mbx_asp_chg)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( mbx_avb_chg)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( mbx_domain)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( mbx_gm_change)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( mbx_gm_id)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( mbx_link_up)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( mbx_rx_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( mbx_rx_if)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( mbx_rx_last)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @( mbx_rx_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000010U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 16 is active: @( mbx_tx_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000011U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 17 is active: @( milan_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000012U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 18 is active: @( serial_sink_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000013U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 19 is active: @( serial_sink_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000014U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 20 is active: @( serial_source_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000015U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 21 is active: @( sim_trace)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000016U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 22 is active: @( sys_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000017U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 23 is active: @( sys_reset)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vsim___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsim___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vsim___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge sys_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.litex_reset)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(posedge sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.cpuResetCtrl_fiber_aggregator_asyncBuffers_0.buffers_1)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(posedge sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.cpuResetCtrl_fiber_buffer.buffers_1)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @(posedge (7'h40 != sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.cpuResetCtrl_fiber_holder_counter))\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vsim___024root___ctor_var_reset(Vsim___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsim___024root___ctor_var_reset\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->audio_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12462280889005755289ull);
    vlSelf->audio_tdm_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5413948399227823105ull);
    vlSelf->flash_cs = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7255794963022757664ull);
    vlSelf->flash_rx_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8802421814854729555ull);
    vlSelf->flash_rx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423837276700678229ull);
    vlSelf->flash_rx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17789749695252465462ull);
    vlSelf->flash_tx_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4182198138983956969ull);
    vlSelf->flash_tx_len = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3197588221592898328ull);
    vlSelf->flash_tx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13059070663017614748ull);
    vlSelf->flash_tx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17534642262895807053ull);
    vlSelf->flash_tx_width = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 669027698148927646ull);
    vlSelf->mbx_amap_wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13173040641504320749ull);
    vlSelf->mbx_asp_chg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9389837737349363835ull);
    vlSelf->mbx_avb_chg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1414334382951439449ull);
    vlSelf->mbx_domain = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13232456389494613888ull);
    vlSelf->mbx_gm_change = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10675885280483565098ull);
    vlSelf->mbx_gm_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5324599952719613123ull);
    vlSelf->mbx_host_ack = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15395814796466849453ull);
    vlSelf->mbx_host_addr = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 5590183630757749138ull);
    vlSelf->mbx_host_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8469723683417989429ull);
    vlSelf->mbx_host_req = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6052294283063882772ull);
    vlSelf->mbx_host_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7110123708436204860ull);
    vlSelf->mbx_host_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13776551202371385470ull);
    vlSelf->mbx_link_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3557674121578675774ull);
    vlSelf->mbx_ms_tick = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16892885806497512599ull);
    vlSelf->mbx_rx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15363302603865357597ull);
    vlSelf->mbx_rx_if = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1366435488215255091ull);
    vlSelf->mbx_rx_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4510311912441291199ull);
    vlSelf->mbx_rx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13693448134670629485ull);
    vlSelf->mbx_rx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10323207466166538961ull);
    vlSelf->mbx_tx_ch = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5923475415192670401ull);
    vlSelf->mbx_tx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11974658817752159988ull);
    vlSelf->mbx_tx_if = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2154894095737347039ull);
    vlSelf->mbx_tx_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13654315388401743911ull);
    vlSelf->mbx_tx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17679267980591550443ull);
    vlSelf->mbx_tx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13206040831982127523ull);
    vlSelf->milan_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16387643398324370288ull);
    vlSelf->serial_sink_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9573462725403686387ull);
    vlSelf->serial_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3758950120267853273ull);
    vlSelf->serial_sink_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13511602996822676087ull);
    vlSelf->serial_source_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17344215306608104219ull);
    vlSelf->serial_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9973345444914751179ull);
    vlSelf->serial_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18327467128597415915ull);
    vlSelf->sim_trace = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16134794833742535666ull);
    vlSelf->sys_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7302336598091101382ull);
    vlSelf->sys_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 763759673302712755ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__audio_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__audio_tdm_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__flash_rx_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__flash_rx_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__flash_tx_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_amap_wr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_asp_chg__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_avb_chg__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_domain__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_gm_change__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_gm_id__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_link_up__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_rx_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_rx_if__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_rx_last__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_rx_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mbx_tx_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__milan_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__serial_sink_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__serial_sink_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__serial_source_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sim_trace__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sys_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sys_reset__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__sys_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__litex_reset__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1__0 = 0;
    vlSelf->__Vtrigprevexpr_h8ac6c1f5__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
