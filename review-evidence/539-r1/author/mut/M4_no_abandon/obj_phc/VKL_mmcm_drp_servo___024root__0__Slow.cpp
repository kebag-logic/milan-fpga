// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_mmcm_drp_servo.h for the primary calling header

#include "VKL_mmcm_drp_servo__pch.h"

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___eval_static(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_static\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk_i__0 = vlSelfRef.clk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__0 
        = vlSelfRef.clk_audio_i;
    vlSelfRef.__Vtrigprevexpr___TOP__ps_clk_i__0 = vlSelfRef.ps_clk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__ptp_now_i__0 = vlSelfRef.ptp_now_i;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_src_i__0 = vlSelfRef.clk_src_i;
    vlSelfRef.__Vtrigprevexpr___TOP__crf_src_idx_i__0 
        = vlSelfRef.crf_src_idx_i;
    vlSelfRef.__Vtrigprevexpr___TOP__crf_locked_i__0 
        = vlSelfRef.crf_locked_i;
    vlSelfRef.__Vtrigprevexpr___TOP__crf_rate_i__0 
        = vlSelfRef.crf_rate_i;
    vlSelfRef.__Vtrigprevexpr___TOP__auto_repair_i__0 
        = vlSelfRef.auto_repair_i;
    vlSelfRef.__Vtrigprevexpr___TOP__ps_invert_i__0 
        = vlSelfRef.ps_invert_i;
    vlSelfRef.__Vtrigprevexpr___TOP__drp_do_i__0 = vlSelfRef.drp_do_i;
    vlSelfRef.__Vtrigprevexpr___TOP__drp_rdy_i__0 = vlSelfRef.drp_rdy_i;
    vlSelfRef.__Vtrigprevexpr___TOP__mmcm_locked_i__0 
        = vlSelfRef.mmcm_locked_i;
    vlSelfRef.__Vtrigprevexpr___TOP__ps_done_i__0 = vlSelfRef.ps_done_i;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_audio_i__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_i__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__ps_clk_i__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk__0 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk;
}

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___eval_initial(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_initial\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___eval_final(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_final\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VKL_mmcm_drp_servo___024root___eval_phase__stl(VKL_mmcm_drp_servo___024root* vlSelf);

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___eval_settle(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_settle\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            VKL_mmcm_drp_servo___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("$MANAGEMENT/2026-09-23/539-a227/mut/M4_no_abandon/KL_mmcm_drp_servo.sv", 198, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = VKL_mmcm_drp_servo___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool VKL_mmcm_drp_servo___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(VKL_mmcm_drp_servo___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool VKL_mmcm_drp_servo___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___stl_sequent__TOP__0(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___stl_sequent__TOP__0\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_now_i = vlSelfRef.ptp_now_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i 
        = vlSelfRef.crf_locked_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__crf_rate_i = vlSelfRef.crf_rate_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__auto_repair_i 
        = vlSelfRef.auto_repair_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_invert_i = vlSelfRef.ps_invert_i;
    vlSelfRef.drp_addr_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o;
    vlSelfRef.drp_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o;
    vlSelfRef.drp_we_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o;
    vlSelfRef.drp_di_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o;
    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_do_i = vlSelfRef.drp_do_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_rdy_i = vlSelfRef.drp_rdy_i;
    vlSelfRef.mmcm_rst_o = vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o;
    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_i 
        = vlSelfRef.mmcm_locked_i;
    vlSelfRef.ps_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o;
    vlSelfRef.ps_incdec_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_incdec_o;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_done_i = vlSelfRef.ps_done_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r;
    if (vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r) {
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w = 0x0080U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w = 0x7fffU;
    } else {
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w = 0x0595U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w = 0xefffU;
    }
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__hs_data_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge 
        = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync) 
                                    >> 1U))));
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__tick_a_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__step_hit_w = 
        ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_jump_r) 
         & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r));
    vlSelfRef.KL_mmcm_drp_servo__DOT__guard_hit_w = 
        ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r) 
         & ((4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r)) 
            & (VL_LTS_III(32, 0x00080000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r) 
               | VL_GTS_III(32, 0xfff80000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r))));
    vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i = vlSelfRef.clk_audio_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i = vlSelfRef.ps_clk_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w = (1U 
                                                  & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__arst_sync_r) 
                                                     >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w = (1U 
                                                   & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_sync_r) 
                                                      >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv 
        = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync) 
                                    >> 1U))));
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse 
        = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync) 
                                    >> 1U))));
    vlSelfRef.KL_mmcm_drp_servo__DOT__clk_src_i = vlSelfRef.clk_src_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__crf_src_idx_i 
        = vlSelfRef.crf_src_idx_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i = vlSelfRef.clk_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w 
        = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r) 
                 >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w = 
        (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r) 
               >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_s_w 
        = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r) 
                 >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__trim_w = (0x0000ffffU 
                                                & VL_SHIFTRS_III(24,24,32, vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r, 5U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w;
    vlSelfRef.KL_mmcm_drp_servo__DOT__hs_rcv_w = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cmd_w = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req;
    vlSelfRef.KL_mmcm_drp_servo__DOT__tick_p_w = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse;
    vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w = 
        ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__clk_src_i) 
         == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__crf_src_idx_i));
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n;
    vlSelfRef.KL_mmcm_drp_servo__DOT__status_o = (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__trim_w) 
                                                   << 0x00000010U) 
                                                  | ((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__disc_cnt_r) 
                                                       << 0x0000000aU) 
                                                      | ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__drp_fault_r) 
                                                         << 8U)) 
                                                     | ((((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_s_w) 
                                                            << 3U) 
                                                           | (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w) 
                                                               | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r)) 
                                                              << 2U)) 
                                                          | (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w) 
                                                              << 1U) 
                                                             | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__mismatch_r))) 
                                                         << 4U) 
                                                        | (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r) 
                                                            << 3U) 
                                                           | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)))));
    vlSelfRef.status_o = vlSelfRef.KL_mmcm_drp_servo__DOT__status_o;
}

VL_ATTR_COLD bool VKL_mmcm_drp_servo___024root___eval_phase__stl(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_phase__stl\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        VKL_mmcm_drp_servo___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = VKL_mmcm_drp_servo___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                VKL_mmcm_drp_servo___024root___stl_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool VKL_mmcm_drp_servo___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(VKL_mmcm_drp_servo___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( clk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( ps_clk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( ptp_now_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( clk_src_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( crf_src_idx_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( crf_locked_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( crf_rate_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( auto_repair_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( ps_invert_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( drp_do_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( drp_rdy_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( mmcm_locked_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( ps_done_i)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool VKL_mmcm_drp_servo___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(VKL_mmcm_drp_servo___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge KL_mmcm_drp_servo.clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge KL_mmcm_drp_servo.clk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(posedge KL_mmcm_drp_servo.ps_clk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(posedge KL_mmcm_drp_servo.u_batch_hs.src_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @(posedge KL_mmcm_drp_servo.u_batch_hs.dest_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @(posedge KL_mmcm_drp_servo.u_tick_cdc.src_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @(posedge KL_mmcm_drp_servo.u_tick_cdc.dest_clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___ctor_var_reset(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___ctor_var_reset\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11908517815223722933ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->clk_audio_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1594742816405956070ull);
    vlSelf->ps_clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6903185485823679000ull);
    vlSelf->ptp_now_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2491740268308898890ull);
    vlSelf->clk_src_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4001498580928466257ull);
    vlSelf->crf_src_idx_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3577518398826460307ull);
    vlSelf->crf_locked_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14040206426382493256ull);
    vlSelf->crf_rate_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13035929894086438757ull);
    vlSelf->auto_repair_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10125271887046459005ull);
    vlSelf->ps_invert_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18432430532485986975ull);
    vlSelf->drp_addr_o = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 6543859326175383647ull);
    vlSelf->drp_en_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17787691427972621324ull);
    vlSelf->drp_we_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3042216703865485232ull);
    vlSelf->drp_di_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1608035197259999800ull);
    vlSelf->drp_do_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8926835821776595969ull);
    vlSelf->drp_rdy_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13327006151383854192ull);
    vlSelf->mmcm_rst_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7492668421012111420ull);
    vlSelf->mmcm_locked_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1708720758528777508ull);
    vlSelf->ps_en_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11492849575985110287ull);
    vlSelf->ps_incdec_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 604744314129405052ull);
    vlSelf->ps_done_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15940800893055797643ull);
    vlSelf->status_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11259888103469126399ull);
    vlSelf->KL_mmcm_drp_servo__DOT__clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8875516382202177074ull);
    vlSelf->KL_mmcm_drp_servo__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15172833700772332761ull);
    vlSelf->KL_mmcm_drp_servo__DOT__clk_audio_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7747258880222107302ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12709072977707475799ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ptp_now_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9711184958835630945ull);
    vlSelf->KL_mmcm_drp_servo__DOT__clk_src_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7996233406066612626ull);
    vlSelf->KL_mmcm_drp_servo__DOT__crf_src_idx_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2423889043224146596ull);
    vlSelf->KL_mmcm_drp_servo__DOT__crf_locked_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3190835292332805583ull);
    vlSelf->KL_mmcm_drp_servo__DOT__crf_rate_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16295331423025819383ull);
    vlSelf->KL_mmcm_drp_servo__DOT__auto_repair_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14969071184831009973ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_invert_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15671409368417991328ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_addr_o = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9115083716497531983ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_en_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3287520858226350024ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_we_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7439359618185255668ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_di_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16662205989236356894ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_do_i = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12381215437424654570ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_rdy_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15957548013674051566ull);
    vlSelf->KL_mmcm_drp_servo__DOT__mmcm_rst_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12786329505429878659ull);
    vlSelf->KL_mmcm_drp_servo__DOT__mmcm_locked_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4548130350975004224ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_en_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2173758236628673053ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_incdec_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12749270043910111743ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_done_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14564732915250279277ull);
    vlSelf->KL_mmcm_drp_servo__DOT__status_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9026298482424942598ull);
    vlSelf->KL_mmcm_drp_servo__DOT__arst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7438373549885492095ull);
    vlSelf->KL_mmcm_drp_servo__DOT__arst_n_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8268188493329411923ull);
    vlSelf->KL_mmcm_drp_servo__DOT__tick_div_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6848673665305398440ull);
    vlSelf->KL_mmcm_drp_servo__DOT__tick_a_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12567613266977565741ull);
    vlSelf->KL_mmcm_drp_servo__DOT__tick_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15493955024991966149ull);
    vlSelf->KL_mmcm_drp_servo__DOT__locked_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9442504193666720650ull);
    vlSelf->KL_mmcm_drp_servo__DOT__psbusy_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 569621151399616708ull);
    vlSelf->KL_mmcm_drp_servo__DOT__psfault_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7624773985730085952ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_busy_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5876875782864409558ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_fault_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15321321888604368442ull);
    vlSelf->KL_mmcm_drp_servo__DOT__mmcm_locked_s_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8735737864758639657ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_busy_s_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17365746343419135435ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_fault_s_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16539931598706146600ull);
    vlSelf->KL_mmcm_drp_servo__DOT__state_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8961673109474646637ull);
    vlSelf->KL_mmcm_drp_servo__DOT__dstate_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6135536857470354889ull);
    vlSelf->KL_mmcm_drp_servo__DOT__servo_sel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16662652157287648059ull);
    vlSelf->KL_mmcm_drp_servo__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 14821631104439654321ull);
    vlSelf->KL_mmcm_drp_servo__DOT__win_start_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8257888031918994333ull);
    vlSelf->KL_mmcm_drp_servo__DOT__win_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1904583293306700795ull);
    vlSelf->KL_mmcm_drp_servo__DOT__win_skip_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17716824039754164531ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ew_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6748665316009559356ull);
    vlSelf->KL_mmcm_drp_servo__DOT__disc_run_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8335347909800154176ull);
    vlSelf->KL_mmcm_drp_servo__DOT__disc_cnt_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4807606037834097922ull);
    vlSelf->KL_mmcm_drp_servo__DOT__integ_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8942111610789834200ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_cmd_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 4778400480614599360ull);
    vlSelf->KL_mmcm_drp_servo__DOT__lock_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15618043172355272883ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_seq_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8405828721829806121ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_run_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1966383840535602607ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6563144196392625410ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_spann_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9268087427113556556ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_locerr_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2068720028445863052ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_rate_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8002263867771026377ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_isum_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12490272382179665523ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_thr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16740437456058976446ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_ig_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12501262705369926287ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_un_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 43281517754776707ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_ut_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12841091646216654351ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pp_du_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5265733378595073261ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_gain_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6863811042625025457ull);
    vlSelf->KL_mmcm_drp_servo__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4304581553518015144ull);
    vlSelf->KL_mmcm_drp_servo__DOT__hs_send_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1637972342578697689ull);
    vlSelf->KL_mmcm_drp_servo__DOT__hs_data_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14985889868354360444ull);
    vlSelf->KL_mmcm_drp_servo__DOT__hs_rcv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8614257718219642794ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_hold_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9974261787215240860ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3256166833731268056ull);
    vlSelf->KL_mmcm_drp_servo__DOT__rd_second_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5118328151167685567ull);
    vlSelf->KL_mmcm_drp_servo__DOT__repairing_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 614147775786015938ull);
    vlSelf->KL_mmcm_drp_servo__DOT__rd_val_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9726761603271039324ull);
    vlSelf->KL_mmcm_drp_servo__DOT__verified_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16033046975498821150ull);
    vlSelf->KL_mmcm_drp_servo__DOT__mismatch_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12019075211802965800ull);
    vlSelf->KL_mmcm_drp_servo__DOT__drp_fault_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9021356256746476355ull);
    vlSelf->KL_mmcm_drp_servo__DOT__relock_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 6659125747344387915ull);
    vlSelf->KL_mmcm_drp_servo__DOT__rst_settle_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5706029885280604104ull);
    vlSelf->KL_mmcm_drp_servo__DOT__exp_val_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4563230566511728121ull);
    vlSelf->KL_mmcm_drp_servo__DOT__exp_mask_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2863095291222903150ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ptp_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12801651134048900662ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ptp_jump_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12979578047585586434ull);
    vlSelf->KL_mmcm_drp_servo__DOT__guard_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18259592786256774109ull);
    vlSelf->KL_mmcm_drp_servo__DOT__step_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15174482727521278586ull);
    vlSelf->KL_mmcm_drp_servo__DOT__psrst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15080568459425894771ull);
    vlSelf->KL_mmcm_drp_servo__DOT__psrst_n_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14357996641398997776ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_cmd_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 2716922996491716841ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17955890966194512967ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7402063850900189819ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_cnt_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 723722434378518120ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11240275198226489037ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pend_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9836556216861118460ull);
    vlSelf->KL_mmcm_drp_servo__DOT__pend_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1521111792128389727ull);
    vlSelf->KL_mmcm_drp_servo__DOT__ps_wd_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7233788591588907954ull);
    vlSelf->KL_mmcm_drp_servo__DOT__trim_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11399387128655968302ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7142195534004022814ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16473283478679597431ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 5707961912464830185ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8060091464623831511ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7181134435622393857ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1981527480310684944ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14291074731522105985ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 220664082250164327ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17371304959020154607ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send_d = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16651300702798052115ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18005905136253534797ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 18011866772296122678ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14797509441302752063ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11278523712245355388ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11754053943687530032ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7290567171778235399ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7068422347733040870ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1159323135186758477ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12336780895663096717ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16631031566338387807ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3659591650013200166ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1121013750864808692ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16297774699565137638ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 605663415507637300ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14512315978089185163ull);
    vlSelf->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2447372629321147707ull);
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog = 0;
    vlSelf->__Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ps_clk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ptp_now_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_src_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__crf_src_idx_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__crf_locked_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__crf_rate_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__auto_repair_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ps_invert_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__drp_do_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__drp_rdy_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__mmcm_locked_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ps_done_i__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_audio_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__ps_clk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
