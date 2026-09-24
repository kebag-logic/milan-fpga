// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_mmcm_drp_servo.h for the primary calling header

#include "VKL_mmcm_drp_servo__pch.h"

void VKL_mmcm_drp_servo___024root___eval_triggers_vec__ico(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_triggers_vec__ico\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[1U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[1U]) 
                                     | (IData)((IData)(vlSelfRef.__VicoFirstIteration)));
    vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                    (((((((IData)(vlSelfRef.ps_done_i) 
                                                          != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__ps_done_i__0)) 
                                                         << 6U) 
                                                        | ((((IData)(vlSelfRef.mmcm_locked_i) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__mmcm_locked_i__0)) 
                                                            << 5U) 
                                                           | (((IData)(vlSelfRef.drp_rdy_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__drp_rdy_i__0)) 
                                                              << 4U))) 
                                                       | (((((IData)(vlSelfRef.drp_do_i) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__drp_do_i__0)) 
                                                            << 3U) 
                                                           | (((IData)(vlSelfRef.ps_invert_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__ps_invert_i__0)) 
                                                              << 2U)) 
                                                          | ((((IData)(vlSelfRef.auto_repair_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__auto_repair_i__0)) 
                                                              << 1U) 
                                                             | (vlSelfRef.crf_rate_i 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__crf_rate_i__0)))) 
                                                      << 8U) 
                                                     | (((((((IData)(vlSelfRef.crf_locked_i) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__crf_locked_i__0)) 
                                                            << 3U) 
                                                           | (((IData)(vlSelfRef.crf_src_idx_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__crf_src_idx_i__0)) 
                                                              << 2U)) 
                                                          | ((((IData)(vlSelfRef.clk_src_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_src_i__0)) 
                                                              << 1U) 
                                                             | (vlSelfRef.ptp_now_i 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__ptp_now_i__0))) 
                                                         << 4U) 
                                                        | (((((IData)(vlSelfRef.ps_clk_i) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__ps_clk_i__0)) 
                                                             << 3U) 
                                                            | (((IData)(vlSelfRef.clk_audio_i) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__0)) 
                                                               << 2U)) 
                                                           | ((((IData)(vlSelfRef.rst_n) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0)) 
                                                               << 1U) 
                                                              | ((IData)(vlSelfRef.clk_i) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_i__0))))))));
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
    }
}

bool VKL_mmcm_drp_servo___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___trigger_anySet__ico\n"); );
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

void VKL_mmcm_drp_servo___024root___eval_ico(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_ico\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x0000000000000010ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__0
            vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_now_i 
                = vlSelfRef.ptp_now_i;
        }
    }
    if ((0x0000000000000080ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__1
            vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i 
                = vlSelfRef.crf_locked_i;
        }
    }
    if ((0x0000000000000100ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__2
            vlSelfRef.KL_mmcm_drp_servo__DOT__crf_rate_i 
                = vlSelfRef.crf_rate_i;
        }
    }
    if ((0x0000000000000200ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__3
            vlSelfRef.KL_mmcm_drp_servo__DOT__auto_repair_i 
                = vlSelfRef.auto_repair_i;
        }
    }
    if ((0x0000000000000400ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__4
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_invert_i 
                = vlSelfRef.ps_invert_i;
        }
    }
    if ((1ULL & vlSelfRef.__VicoTriggered[1U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__5
            vlSelfRef.drp_addr_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o;
            vlSelfRef.drp_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o;
            vlSelfRef.drp_we_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o;
            vlSelfRef.drp_di_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o;
            vlSelfRef.mmcm_rst_o = vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o;
            vlSelfRef.ps_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o;
            vlSelfRef.ps_incdec_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_incdec_o;
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
            vlSelfRef.KL_mmcm_drp_servo__DOT__step_hit_w 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_jump_r) 
                   & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r));
            vlSelfRef.KL_mmcm_drp_servo__DOT__guard_hit_w 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r) 
                   & ((4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r)) 
                      & (VL_LTS_III(32, 0x00080000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r) 
                         | VL_GTS_III(32, 0xfff80000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r))));
            vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__arst_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_sync_r) 
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
            vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_s_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__trim_w 
                = (0x0000ffffU & VL_SHIFTRS_III(24,24,32, vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r, 5U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w;
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w;
            vlSelfRef.KL_mmcm_drp_servo__DOT__hs_rcv_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cmd_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req;
            vlSelfRef.KL_mmcm_drp_servo__DOT__tick_p_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse;
            vlSelfRef.KL_mmcm_drp_servo__DOT__status_o 
                = (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__trim_w) 
                    << 0x00000010U) | ((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__disc_cnt_r) 
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
                                           << 4U) | 
                                          (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r) 
                                            << 3U) 
                                           | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)))));
            vlSelfRef.status_o = vlSelfRef.KL_mmcm_drp_servo__DOT__status_o;
        }
    }
    if ((0x0000000000000800ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__6
            vlSelfRef.KL_mmcm_drp_servo__DOT__drp_do_i 
                = vlSelfRef.drp_do_i;
        }
    }
    if ((0x0000000000001000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__7
            vlSelfRef.KL_mmcm_drp_servo__DOT__drp_rdy_i 
                = vlSelfRef.drp_rdy_i;
        }
    }
    if ((0x0000000000002000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__8
            vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_i 
                = vlSelfRef.mmcm_locked_i;
        }
    }
    if ((0x0000000000004000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__9
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_done_i 
                = vlSelfRef.ps_done_i;
        }
    }
    if ((4ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__10
            vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i 
                = vlSelfRef.clk_audio_i;
        }
    }
    if ((8ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__11
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i 
                = vlSelfRef.ps_clk_i;
        }
    }
    if ((0x0000000000000020ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__12
            vlSelfRef.KL_mmcm_drp_servo__DOT__clk_src_i 
                = vlSelfRef.clk_src_i;
        }
    }
    if ((0x0000000000000040ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__13
            vlSelfRef.KL_mmcm_drp_servo__DOT__crf_src_idx_i 
                = vlSelfRef.crf_src_idx_i;
        }
    }
    if ((1ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__14
            vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i 
                = vlSelfRef.clk_i;
        }
    }
    if ((2ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__15
            vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n 
                = vlSelfRef.rst_n;
        }
    }
    if (((1ULL & vlSelfRef.__VicoTriggered[1U]) | (4ULL 
                                                   & vlSelfRef.__VicoTriggered[0U]))) {
        {
            // Inlined CFunc: _ico_comb__TOP__0
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i;
        }
    }
    if (((1ULL & vlSelfRef.__VicoTriggered[1U]) | (8ULL 
                                                   & vlSelfRef.__VicoTriggered[0U]))) {
        {
            // Inlined CFunc: _ico_comb__TOP__1
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i;
        }
    }
    if (((1ULL & vlSelfRef.__VicoTriggered[1U]) | (0x0000000000000060ULL 
                                                   & vlSelfRef.__VicoTriggered[0U]))) {
        {
            // Inlined CFunc: _ico_comb__TOP__2
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__clk_src_i) 
                   == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__crf_src_idx_i));
        }
    }
    if ((1ULL & (vlSelfRef.__VicoTriggered[1U] | vlSelfRef.__VicoTriggered[0U]))) {
        {
            // Inlined CFunc: _ico_comb__TOP__3
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i;
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i;
        }
    }
    if (((1ULL & vlSelfRef.__VicoTriggered[1U]) | (2ULL 
                                                   & vlSelfRef.__VicoTriggered[0U]))) {
        {
            // Inlined CFunc: _ico_comb__TOP__4
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n;
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n;
        }
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool VKL_mmcm_drp_servo___024root___eval_phase__ico(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_phase__ico\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    VKL_mmcm_drp_servo___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VKL_mmcm_drp_servo___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = VKL_mmcm_drp_servo___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        VKL_mmcm_drp_servo___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

bool VKL_mmcm_drp_servo___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___trigger_anySet__act\n"); );
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

void VKL_mmcm_drp_servo___024root___nba_sequent__TOP__6(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___nba_sequent__TOP__6\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*23:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__Vfuncout;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v = 0;
    IData/*31:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v = 0;
    IData/*23:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__Vfuncout;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v = 0;
    IData/*31:0*/ __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v;
    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r;
    __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r = 0;
    IData/*31:0*/ __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r;
    __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r = 0;
    CData/*2:0*/ __Vdly__KL_mmcm_drp_servo__DOT__state_r;
    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0;
    CData/*1:0*/ __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r;
    __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 0;
    CData/*2:0*/ __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = 0;
    CData/*3:0*/ __Vdly__KL_mmcm_drp_servo__DOT__dstate_r;
    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0;
    IData/*23:0*/ __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r;
    __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r = 0;
    IData/*23:0*/ __Vdly__KL_mmcm_drp_servo__DOT__integ_r;
    __Vdly__KL_mmcm_drp_servo__DOT__integ_r = 0;
    IData/*31:0*/ __Vdly__KL_mmcm_drp_servo__DOT__acc_r;
    __Vdly__KL_mmcm_drp_servo__DOT__acc_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r;
    __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0;
    CData/*1:0*/ __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r;
    __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0;
    CData/*5:0*/ __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r;
    __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r;
    __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r;
    __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__repairing_r;
    __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = 0;
    SData/*9:0*/ __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r = 0;
    QData/*63:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r = 0;
    IData/*31:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r = 0;
    CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r = 0;
    CData/*2:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 0;
    // Body
    __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r = vlSelfRef.KL_mmcm_drp_servo__DOT__u_gain_r;
    __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = vlSelfRef.KL_mmcm_drp_servo__DOT__win_skip_r;
    __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r;
    __Vdly__KL_mmcm_drp_servo__DOT__integ_r = vlSelfRef.KL_mmcm_drp_servo__DOT__integ_r;
    __Vdly__KL_mmcm_drp_servo__DOT__acc_r = vlSelfRef.KL_mmcm_drp_servo__DOT__acc_r;
    __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = vlSelfRef.KL_mmcm_drp_servo__DOT__disc_run_r;
    __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_hold_r;
    __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_pass_r;
    __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = vlSelfRef.KL_mmcm_drp_servo__DOT__repairing_r;
    __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r = vlSelfRef.KL_mmcm_drp_servo__DOT__tick_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_d_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_rate_r;
    __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r;
    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r;
    __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r;
    __Vdly__KL_mmcm_drp_servo__DOT__state_r = vlSelfRef.KL_mmcm_drp_servo__DOT__state_r;
    __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r = vlSelfRef.KL_mmcm_drp_servo__DOT__disc_cnt_r;
    __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r = vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r;
    __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r = vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r;
    if (vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n) {
        vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r 
            = ((2U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_i));
        vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r 
            = ((2U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_ps_r));
        vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r 
            = ((2U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_ps_r));
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o = 0U;
        if (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r) 
             & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__hs_rcv_w))) {
            __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r = 0U;
        }
        __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r = 
            ((IData)(0x0000003bU) * VL_EXTENDS_II(32,24, vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r));
        if ((4U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
            if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
                if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
                    if ((1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w)))) {
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w) {
                    if (vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i) {
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                        __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 2U;
                        __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = 0U;
                    }
                } else {
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
                }
            } else if (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i) {
                    if (((3U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
                         & (4U <= (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r)))) {
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 4U;
                    } else if (((4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
                                & (0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r)))) {
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                    }
                } else {
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 5U;
                }
            } else {
                __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
            }
        } else if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
            if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w) {
                    if (vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i) {
                        if (((3U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
                             & (4U <= (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r)))) {
                            __Vdly__KL_mmcm_drp_servo__DOT__state_r = 4U;
                        } else if (((4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
                                    & (0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r)))) {
                            __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                        }
                    } else {
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 5U;
                    }
                } else {
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
                }
            } else if ((1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w)))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) {
            if ((1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w)))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
            }
        } else {
            __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__integ_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__acc_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r = 0U;
            vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r = 0U;
            vlSelfRef.KL_mmcm_drp_servo__DOT__mismatch_r = 0U;
            vlSelfRef.KL_mmcm_drp_servo__DOT__drp_fault_r = 0U;
            vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
            __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 0U;
            if (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_sel_w) 
                 & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__crf_locked_i))) {
                __Vdly__KL_mmcm_drp_servo__DOT__state_r = 1U;
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 1U;
                __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r = 1U;
                __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = 0U;
            }
        }
        if ((((3U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
              | (4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r))) 
             | (5U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)))) {
            const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 13121607036966620062ull);
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12773466568752013915ull);
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__tick_p_w) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r) {
                    if ((0x01ffU == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__tick_cnt_r))) {
                        __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r = 0U;
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r 
                            = (vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_q_r 
                               - vlSelfRef.KL_mmcm_drp_servo__DOT__win_start_r);
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r 
                            = vlSelfRef.KL_mmcm_drp_servo__DOT__crf_rate_i;
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r 
                            = ((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_skip_r)) 
                               & (5U != (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)));
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 1U;
                        if ((0U != (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_skip_r))) {
                            __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r 
                                = (3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_skip_r) 
                                         - (IData)(1U)));
                        }
                        vlSelfRef.KL_mmcm_drp_servo__DOT__win_start_r 
                            = vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_q_r;
                    } else {
                        __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r 
                            = (0x000003ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__tick_cnt_r)));
                    }
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__win_start_r 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_q_r;
                    __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r = 0U;
                }
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v 
                = (0x0000007fU & (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__disc_cnt_r) 
                                   + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__guard_hit_w)) 
                                  + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__step_hit_w)));
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17599087223149111973ull);
            if ((4U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                    if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                        if (vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r) {
                            __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r 
                                = (0x00ffffffU & (VL_LTS_III(32, 0x0000c800U, vlSelfRef.KL_mmcm_drp_servo__DOT__pp_du_r)
                                                   ? 
                                                  ((IData)(0x0000c800U) 
                                                   + vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r)
                                                   : 
                                                  (VL_GTS_III(32, 0xffff3800U, vlSelfRef.KL_mmcm_drp_servo__DOT__pp_du_r)
                                                    ? 
                                                   (vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r 
                                                    - (IData)(0x0000c800U))
                                                    : vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ut_r)));
                            if (vlSelfRef.KL_mmcm_drp_servo__DOT__pp_thr_r) {
                                if ((4U != (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r))) {
                                    __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r 
                                        = (7U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r)));
                                }
                            } else {
                                __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = 0U;
                            }
                            __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0U;
                            __Vdly__KL_mmcm_drp_servo__DOT__integ_r 
                                = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ig_r;
                        }
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 0U;
                    } else {
                        __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v 
                            = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_un_r;
                        __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v 
                            = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_un_r;
                        __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__Vfuncout 
                            = (VL_LTS_III(32, 0x00019000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v)
                                ? 0x00019000U : (VL_GTS_III(32, 0xfffe7000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v)
                                                  ? 0x00fe7000U
                                                  : 
                                                 (0x00ffffffU 
                                                  & __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__v)));
                        vlSelfRef.KL_mmcm_drp_servo__DOT____VlemCall_1__clamp_u 
                            = (VL_LTS_III(32, 0x00019000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v)
                                ? 0x00019000U : (VL_GTS_III(32, 0xfffe7000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v)
                                                  ? 0x00fe7000U
                                                  : 
                                                 (0x00ffffffU 
                                                  & __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__1__v)));
                        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ut_r 
                            = __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__0__Vfuncout;
                        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_du_r 
                            = (VL_EXTENDS_II(32,24, vlSelfRef.KL_mmcm_drp_servo__DOT____VlemCall_1__clamp_u) 
                               - VL_EXTENDS_II(32,24, vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r));
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 7U;
                    }
                } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_isum_r;
                    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__pp_isum_r;
                    __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__Vfuncout 
                        = (VL_LTS_III(32, 0x00019000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v)
                            ? 0x00019000U : (VL_GTS_III(32, 0xfffe7000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v)
                                              ? 0x00fe7000U
                                              : (0x00ffffffU 
                                                 & __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__v)));
                    vlSelfRef.KL_mmcm_drp_servo__DOT____VlemCall_0__clamp_u 
                        = (VL_LTS_III(32, 0x00019000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v)
                            ? 0x00019000U : (VL_GTS_III(32, 0xfffe7000U, __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v)
                                              ? 0x00fe7000U
                                              : (0x00ffffffU 
                                                 & __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__3__v)));
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ig_r 
                        = __Vfunc_KL_mmcm_drp_servo__DOT__clamp_u__2__Vfuncout;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_un_r 
                        = (VL_EXTENDS_II(32,24, vlSelfRef.KL_mmcm_drp_servo__DOT____VlemCall_0__clamp_u) 
                           + VL_SHIFTRS_III(32,32,32, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r, 2U));
                    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 6U;
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_isum_r 
                        = (VL_EXTENDS_II(32,24, vlSelfRef.KL_mmcm_drp_servo__DOT__integ_r) 
                           + VL_SHIFTRS_III(32,32,32, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r, 1U));
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_thr_r 
                        = (VL_GTS_III(32, 0x00000400U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r) 
                           & VL_LTS_III(32, 0xfffffc00U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r));
                    if (vlSelfRef.KL_mmcm_drp_servo__DOT__guard_hit_w) {
                        __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r = 0U;
                        if ((3U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__disc_run_r))) {
                            __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
                            __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0U;
                        } else {
                            __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__disc_run_r)));
                        }
                    }
                    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 5U;
                }
            } else if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r 
                        = (vlSelfRef.KL_mmcm_drp_servo__DOT__pp_locerr_r 
                           - vlSelfRef.KL_mmcm_drp_servo__DOT__pp_rate_r);
                    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 4U;
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_locerr_r 
                        = (VL_LTS_IQQ(64, 0x0000000000100000ULL, vlSelfRef.KL_mmcm_drp_servo__DOT__pp_spann_r)
                            ? 0x00100000U : (VL_GTS_IQQ(64, 0xfffffffffff00000ULL, vlSelfRef.KL_mmcm_drp_servo__DOT__pp_spann_r)
                                              ? 0xfff00000U
                                              : (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_spann_r)));
                    __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 3U;
                }
            } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__pp_spann_r 
                    = (vlSelfRef.KL_mmcm_drp_servo__DOT__pp_d_r 
                       - 0x000000001e848000ULL);
                __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 2U;
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__acc_r;
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__step_hit_w) {
                __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0U;
                if ((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r))) {
                    __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r = 0U;
                }
            }
            if (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__tick_p_w) 
                 & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_hold_r)))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v 
                    = (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v 
                       + vlSelfRef.KL_mmcm_drp_servo__DOT__u_gain_r);
            }
            __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r 
                = ((0x3fU < (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v))
                    ? 0x0000003fU : (0x0000003fU & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v)));
            if ((1U & (((~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r)) 
                        & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w))) 
                       & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_hold_r))))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v 
                    = VL_SHIFTRS_III(32,32,32, vlSelfRef.KL_mmcm_drp_servo__DOT__acc_r, 9U);
                if (VL_LTS_III(32, 0x00003fffU, vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v)) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v = 0x00003fffU;
                }
                if (VL_GTS_III(32, 0xffffc001U, vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v)) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v = 0xffffc001U;
                }
                if ((0U != vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v)) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__hs_data_r 
                        = (VL_LTS_III(32, 0U, vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v)
                            ? (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_invert_i) 
                                << 0x0000000eU) | (0x00003fffU 
                                                   & vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v))
                            : ((0x00004000U & ((~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_invert_i)) 
                                               << 0x0000000eU)) 
                               | (0x00003fffU & (- vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v))));
                    __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r = 1U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v 
                        = (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v 
                           - (vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v 
                              << 9U));
                }
            }
            __Vdly__KL_mmcm_drp_servo__DOT__acc_r = vlSelfRef.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v;
        } else {
            __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 0U;
        }
        if ((8U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
            if ((4U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
            } else if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w) {
                    __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 0U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                    __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 1U;
                } else if ((0U == vlSelfRef.KL_mmcm_drp_servo__DOT__relock_r)) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_fault_r = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 0U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                    __Vdly__KL_mmcm_drp_servo__DOT__state_r = 6U;
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__relock_r 
                        = (0x0003ffffU & (vlSelfRef.KL_mmcm_drp_servo__DOT__relock_r 
                                          - (IData)(1U)));
                }
            } else if (vlSelfRef.KL_mmcm_drp_servo__DOT__drp_rdy_i) {
                __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 0U;
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 1U;
            }
        } else if ((4U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
            if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o = 0x28U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o = 0xffffU;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o = 1U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 8U;
                } else if ((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rst_settle_r))) {
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 7U;
                } else {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__rst_settle_r 
                        = (0x0000000fU & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rst_settle_r) 
                                          - (IData)(1U)));
                }
            } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                if ((1U & ((~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w)) 
                           & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r))))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 1U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__rst_settle_r = 0x0fU;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 6U;
                }
            } else if (vlSelfRef.KL_mmcm_drp_servo__DOT__drp_rdy_i) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__relock_r = 0x00020000U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 9U;
                } else {
                    __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 1U;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
            if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o 
                    = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r)
                        ? 9U : 8U);
                vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o 
                    = (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rd_val_r) 
                        & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w))) 
                       | ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w) 
                          & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w)));
                vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o = 1U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o = 1U;
                __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 4U;
            } else if (vlSelfRef.KL_mmcm_drp_servo__DOT__drp_rdy_i) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__rd_val_r 
                    = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_do_i;
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__repairing_r) {
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 3U;
                } else if (vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r) {
                    if (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__drp_pass_r) 
                         & (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__drp_do_i) 
                             & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w)) 
                            == ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w) 
                                & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w))))) {
                        __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
                        vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r = 1U;
                        __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                        __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 1U;
                    } else {
                        vlSelfRef.KL_mmcm_drp_servo__DOT__mismatch_r = 1U;
                        if (vlSelfRef.KL_mmcm_drp_servo__DOT__auto_repair_i) {
                            __Vdly__KL_mmcm_drp_servo__DOT__state_r = 2U;
                            __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 1U;
                            __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 5U;
                        } else {
                            __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
                            __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
                            __Vdly__KL_mmcm_drp_servo__DOT__state_r = 3U;
                            __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 1U;
                        }
                    }
                } else {
                    __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 1U;
                    __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 1U;
                }
                if ((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__drp_do_i) 
                      & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w)) 
                     != ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w) 
                         & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w)))) {
                    __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r = 0U;
                }
            }
        } else if ((1U & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r))) {
            vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r)
                    ? 9U : 8U);
            vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o = 1U;
            __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 2U;
        }
        if (((2U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
             & (5U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r)))) {
            __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = 1U;
        }
        if (((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)) 
             | (3U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__state_r)))) {
            __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = 0U;
        }
        vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_jump_r 
            = (0x00001000U < ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_now_i) 
                              - (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_q_r)));
    } else {
        vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__integ_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__acc_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__repairing_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__state_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__dstate_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__win_start_r = 0ULL;
        vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__hs_data_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__rd_val_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__verified_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__mismatch_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__drp_fault_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__relock_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__rst_settle_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r = 0ULL;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_spann_r = 0ULL;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_locerr_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_isum_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_thr_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ig_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_un_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_ut_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__pp_du_r = 0U;
        __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r = 0U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_jump_r = 0U;
    }
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_gain_r = __Vdly__KL_mmcm_drp_servo__DOT__u_gain_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__win_skip_r = __Vdly__KL_mmcm_drp_servo__DOT__win_skip_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__lock_cnt_r = __Vdly__KL_mmcm_drp_servo__DOT__lock_cnt_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__dstate_r = __Vdly__KL_mmcm_drp_servo__DOT__dstate_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__integ_r = __Vdly__KL_mmcm_drp_servo__DOT__integ_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__acc_r = __Vdly__KL_mmcm_drp_servo__DOT__acc_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__disc_run_r = __Vdly__KL_mmcm_drp_servo__DOT__disc_run_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_hold_r = __Vdly__KL_mmcm_drp_servo__DOT__ps_hold_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__drp_pass_r = __Vdly__KL_mmcm_drp_servo__DOT__drp_pass_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__repairing_r = __Vdly__KL_mmcm_drp_servo__DOT__repairing_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__tick_cnt_r = __Vdly__KL_mmcm_drp_servo__DOT__tick_cnt_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_d_r = __Vdly__KL_mmcm_drp_servo__DOT__pp_d_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_rate_r = __Vdly__KL_mmcm_drp_servo__DOT__pp_rate_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r = __Vdly__KL_mmcm_drp_servo__DOT__win_valid_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r = __Vdly__KL_mmcm_drp_servo__DOT__pp_run_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r = __Vdly__KL_mmcm_drp_servo__DOT__pp_seq_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r = __Vdly__KL_mmcm_drp_servo__DOT__rd_second_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__state_r = __Vdly__KL_mmcm_drp_servo__DOT__state_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__disc_cnt_r = __Vdly__KL_mmcm_drp_servo__DOT__disc_cnt_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r = __Vdly__KL_mmcm_drp_servo__DOT__hs_send_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r = __Vdly__KL_mmcm_drp_servo__DOT__u_cmd_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w 
        = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__locked_sync_r) 
                 >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_s_w = 
        (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psbusy_sync_r) 
               >> 1U));
    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_s_w 
        = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psfault_sync_r) 
                 >> 1U));
    vlSelfRef.drp_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_en_o;
    vlSelfRef.drp_we_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_we_o;
    vlSelfRef.mmcm_rst_o = vlSelfRef.KL_mmcm_drp_servo__DOT__mmcm_rst_o;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__hs_data_r;
    vlSelfRef.drp_addr_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_addr_o;
    vlSelfRef.drp_di_o = vlSelfRef.KL_mmcm_drp_servo__DOT__drp_di_o;
    vlSelfRef.KL_mmcm_drp_servo__DOT__step_hit_w = 
        ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_jump_r) 
         & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__win_valid_r));
    vlSelfRef.KL_mmcm_drp_servo__DOT__guard_hit_w = 
        ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_run_r) 
         & ((4U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pp_seq_r)) 
            & (VL_LTS_III(32, 0x00080000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r) 
               | VL_GTS_III(32, 0xfff80000U, vlSelfRef.KL_mmcm_drp_servo__DOT__ew_r))));
    if (vlSelfRef.KL_mmcm_drp_servo__DOT__rd_second_r) {
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w = 0x0080U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w = 0x7fffU;
    } else {
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_val_w = 0x0595U;
        vlSelfRef.KL_mmcm_drp_servo__DOT__exp_mask_w = 0xefffU;
    }
    vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_q_r = vlSelfRef.KL_mmcm_drp_servo__DOT__ptp_now_i;
    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send 
        = vlSelfRef.KL_mmcm_drp_servo__DOT__hs_send_r;
    vlSelfRef.KL_mmcm_drp_servo__DOT__trim_w = (0x0000ffffU 
                                                & VL_SHIFTRS_III(24,24,32, vlSelfRef.KL_mmcm_drp_servo__DOT__u_cmd_r, 5U));
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

void VKL_mmcm_drp_servo___024root___eval_nba(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_nba\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x0000000000000020ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__0
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level;
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse) {
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level 
                        = (1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level)));
                }
            } else {
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level = 0U;
            }
        }
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__1
            SData/*14:0*/ __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r;
            __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r = 0;
            __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__tick_div_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__arst_sync_r 
                = ((2U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__arst_sync_r) 
                          << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n));
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w) {
                if ((0x5fffU == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__tick_div_r))) {
                    __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r = 0U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__tick_a_r = 1U;
                } else {
                    __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r 
                        = (0x00007fffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__tick_div_r)));
                    vlSelfRef.KL_mmcm_drp_servo__DOT__tick_a_r = 0U;
                }
            } else {
                __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__tick_a_r = 0U;
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__tick_div_r 
                = __Vinline_0__nba_sequent__TOP__1___Vdly__KL_mmcm_drp_servo__DOT__tick_div_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__arst_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__tick_a_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__arst_n_w;
        }
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__2
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog;
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n) {
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge) {
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog 
                        = (1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog)));
                    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold;
                }
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync 
                    = ((6U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync) 
                              << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog));
            } else {
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r = 0U;
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n) 
                   && (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge 
                = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync) 
                                            >> 1U))));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r;
        }
    }
    if ((0x0000000000000040ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__3
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n)
                    ? ((6U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync) 
                              << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level))
                    : 0U);
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse 
                = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync) 
                                            >> 1U))));
        }
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__4
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync 
                    = ((6U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync) 
                              << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog));
                if (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send) 
                     & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send_d)))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog 
                        = (1U & (~ (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog)));
                    vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in;
                }
            } else {
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold = 0U;
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv 
                = (1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync) 
                                            >> 1U))));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send_d 
                = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n) 
                   && (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send));
        }
    }
    if ((4ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__5
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__pend_v_r;
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_dir_r;
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cnt_r;
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__pstate_r;
            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_wd_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_sync_r 
                = ((2U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_sync_r) 
                          << 1U)) | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__rst_n));
        }
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
        VKL_mmcm_drp_servo___024root___nba_sequent__TOP__6(vlSelf);
    }
    if ((0x0000000000000020ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__7
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level;
        }
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__8
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog;
        }
    }
    if ((4ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__9
            if (vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w) {
                vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o = 0U;
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w) {
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r = 1U;
                }
                if ((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pstate_r))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_ps_r 
                        = ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pend_v_r) 
                           | (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w));
                    if (vlSelfRef.KL_mmcm_drp_servo__DOT__pend_v_r) {
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r 
                            = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pend_r) 
                                     >> 0x0eU));
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r 
                            = (0x00003fffU & (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pend_r));
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r 
                            = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w;
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 1U;
                    }
                } else if ((1U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pstate_r))) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_ps_r = 1U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o = 1U;
                    vlSelfRef.KL_mmcm_drp_servo__DOT__ps_incdec_o 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_dir_r;
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r = 0xffU;
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 2U;
                } else if ((2U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__pstate_r))) {
                    if (vlSelfRef.KL_mmcm_drp_servo__DOT__ps_done_i) {
                        if ((1U >= (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cnt_r))) {
                            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 0U;
                        } else {
                            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r 
                                = (0x00003fffU & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cnt_r) 
                                                  - (IData)(1U)));
                            vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 1U;
                        }
                    } else if ((0U == (IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_wd_r))) {
                        vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_ps_r = 1U;
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r 
                            = (0x000000ffU & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_wd_r) 
                                              - (IData)(1U)));
                    }
                } else {
                    vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 0U;
                }
                if (vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w) {
                    vlSelfRef.KL_mmcm_drp_servo__DOT__pend_r 
                        = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cmd_w;
                }
            } else {
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r = 0U;
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__ps_incdec_o = 0U;
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r = 0U;
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__ps_busy_ps_r = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__ps_fault_ps_r = 0U;
                vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r = 0U;
                vlSelfRef.KL_mmcm_drp_servo__DOT__pend_r = 0U;
            }
            vlSelfRef.KL_mmcm_drp_servo__DOT__pend_v_r 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pend_v_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_dir_r 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cnt_r 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__pstate_r 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__pstate_r;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_wd_r 
                = vlSelfRef.__Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r;
            vlSelfRef.ps_en_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_en_o;
            vlSelfRef.ps_incdec_o = vlSelfRef.KL_mmcm_drp_servo__DOT__ps_incdec_o;
            vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w 
                = (1U & ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_sync_r) 
                         >> 1U));
            vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__psrst_n_w;
        }
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__10
            vlSelfRef.KL_mmcm_drp_servo__DOT__hs_rcv_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv;
        }
    }
    if ((0x0000000000000040ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__11
            vlSelfRef.KL_mmcm_drp_servo__DOT__tick_p_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse;
        }
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__12
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_cmd_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out;
            vlSelfRef.KL_mmcm_drp_servo__DOT__ps_req_w 
                = vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req;
        }
    }
}

void VKL_mmcm_drp_servo___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void VKL_mmcm_drp_servo___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool VKL_mmcm_drp_servo___024root___eval_phase__act(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_phase__act\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        (((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk) 
                                                            & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk__0))) 
                                                           << 6U) 
                                                          | ((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk__0))) 
                                                              << 5U) 
                                                             | (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk__0))) 
                                                                << 4U))) 
                                                         | (((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk__0))) 
                                                              << 3U) 
                                                             | (((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__ps_clk_i) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__ps_clk_i__0))) 
                                                                << 2U)) 
                                                            | ((((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__clk_i) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_i__0))) 
                                                                << 1U) 
                                                               | ((IData)(vlSelfRef.KL_mmcm_drp_servo__DOT__clk_audio_i) 
                                                                  & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_audio_i__0))))))));
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
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VKL_mmcm_drp_servo___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    VKL_mmcm_drp_servo___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void VKL_mmcm_drp_servo___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool VKL_mmcm_drp_servo___024root___eval_phase__nba(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_phase__nba\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = VKL_mmcm_drp_servo___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        VKL_mmcm_drp_servo___024root___eval_nba(vlSelf);
        VKL_mmcm_drp_servo___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void VKL_mmcm_drp_servo___024root___eval(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            VKL_mmcm_drp_servo___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("$MANAGEMENT/2026-09-23/539-a227/mut/M4_no_abandon/KL_mmcm_drp_servo.sv", 198, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = VKL_mmcm_drp_servo___024root___eval_phase__ico(vlSelf);
        vlSelfRef.__VicoFirstIteration = 0U;
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            VKL_mmcm_drp_servo___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("$MANAGEMENT/2026-09-23/539-a227/mut/M4_no_abandon/KL_mmcm_drp_servo.sv", 198, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                VKL_mmcm_drp_servo___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("$MANAGEMENT/2026-09-23/539-a227/mut/M4_no_abandon/KL_mmcm_drp_servo.sv", 198, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = VKL_mmcm_drp_servo___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = VKL_mmcm_drp_servo___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void VKL_mmcm_drp_servo___024root___eval_debug_assertions(VKL_mmcm_drp_servo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_mmcm_drp_servo___024root___eval_debug_assertions\n"); );
    VKL_mmcm_drp_servo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk_i & 0xfeU)))) {
        Verilated::overWidthError("clk_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.clk_audio_i & 0xfeU)))) {
        Verilated::overWidthError("clk_audio_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.ps_clk_i & 0xfeU)))) {
        Verilated::overWidthError("ps_clk_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.crf_locked_i & 0xfeU)))) {
        Verilated::overWidthError("crf_locked_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.auto_repair_i & 0xfeU)))) {
        Verilated::overWidthError("auto_repair_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.ps_invert_i & 0xfeU)))) {
        Verilated::overWidthError("ps_invert_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.drp_rdy_i & 0xfeU)))) {
        Verilated::overWidthError("drp_rdy_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.mmcm_locked_i & 0xfeU)))) {
        Verilated::overWidthError("mmcm_locked_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.ps_done_i & 0xfeU)))) {
        Verilated::overWidthError("ps_done_i");
    }
}
#endif  // VL_DEBUG
