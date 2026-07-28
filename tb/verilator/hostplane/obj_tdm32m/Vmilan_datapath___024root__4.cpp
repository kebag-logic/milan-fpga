// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___nba_sequent__TOP__4(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__4\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*8:0*/ __Vdly__milan_datapath__DOT__zf_adiv_r;
    __Vdly__milan_datapath__DOT__zf_adiv_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r = 0;
    IData/*31:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r = 0;
    CData/*5:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r = 0;
    IData/*31:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r = 0;
    SData/*15:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r = 0;
    SData/*14:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r = 0;
    CData/*6:0*/ __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r;
    __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r = 0;
    CData/*5:0*/ __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r;
    __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r = 0;
    // Body
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r 
        = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r 
        = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r;
    __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r 
        = vlSelfRef.milan_datapath__DOT__tone_gen__DOT__cnt_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r 
        = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r;
    __Vdly__milan_datapath__DOT__zf_adiv_r = vlSelfRef.milan_datapath__DOT__zf_adiv_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r;
    __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r 
        = vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r;
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r))) {
        if (vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r) {
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__src_level 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__src_level)));
        }
        if ((0x5fffU == (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r))) {
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r = 1U;
        } else {
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r 
                = (0x00007fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r)));
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r = 0U;
        }
    } else {
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__src_level = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r = 0U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r))) {
        if (vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_p_r) {
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__src_level 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__src_level)));
        }
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_p_r = 0U;
        __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r)));
        if ((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r))) {
            if ((0x5fU == (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r))) {
                __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r = 0U;
                vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_p_r = 1U;
            } else {
                __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r)));
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__src_level = 0U;
        __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r = 0U;
        __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_p_r = 0U;
    }
    if (vlSelfRef.axis_resetn) {
        __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__tone_gen__DOT__cnt_r)));
        if (vlSelfRef.milan_datapath__DOT__zf_apulse_r) {
            vlSelfRef.milan_datapath__DOT__zf_tick_cdc__DOT__src_level 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__zf_tick_cdc__DOT__src_level)));
        }
        if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl)) {
            if ((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__tone_gen__DOT__cnt_r))) {
                __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r 
                    = ((0x2fU == (IData)(vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r))
                        ? 0U : (0x0000003fU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r))));
                vlSelfRef.milan_datapath__DOT__tone_smp 
                    = (0x00ffffffU & VL_SHIFTRS_III(24,24,3, 
                                                    ((0x2fU 
                                                      >= (IData)(vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r))
                                                      ? vlSelfRef.milan_datapath__DOT__tone_gen__DOT__TONE_TAB_C
                                                     [vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r]
                                                      : 0U), 
                                                    (7U 
                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl 
                                                        >> 1U))));
            }
        } else {
            __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r = 0U;
            vlSelfRef.milan_datapath__DOT__tone_smp = 0U;
        }
        __Vdly__milan_datapath__DOT__zf_adiv_r = (0x000001ffU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.milan_datapath__DOT__zf_adiv_r)));
        vlSelfRef.milan_datapath__DOT__zf_apulse_r 
            = (0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__zf_adiv_r));
    } else {
        __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__zf_tick_cdc__DOT__src_level = 0U;
        __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__tone_smp = 0U;
        __Vdly__milan_datapath__DOT__zf_adiv_r = 0U;
        vlSelfRef.milan_datapath__DOT__zf_apulse_r = 0U;
    }
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r 
        = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r) 
                  << 1U)) | (IData)(vlSelfRef.axis_resetn));
    __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r 
        = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r) 
                  << 1U)) | (IData)(vlSelfRef.axis_resetn));
    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r 
        = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r) 
                  << 1U)) | (IData)(vlSelfRef.axis_resetn));
    vlSelfRef.i2s_dac_sclk_o = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r) 
                                       >> 1U)) && (1U 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r) 
                                                      >> 2U)));
    vlSelfRef.i2s_dac_mclk_o = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r) 
                                       >> 1U)) && (1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r)));
    vlSelfRef.i2s_dac_lrck_o = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r) 
                                       >> 1U)) && (1U 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r) 
                                                      >> 8U)));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r))) {
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__src_level));
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r)));
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync) 
                                      >> 1U))))) {
            __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r 
                = (((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w))
                    ? 1U : 0U);
        } else if (((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w))) {
            __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r 
                = (0x0000ffffU & ((0x0000ffffU == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r))
                                   ? (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r)
                                   : ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r))));
        }
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r;
        vlSelfRef.milan_datapath__DOT__tone_gen__DOT__cnt_r 
            = __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r;
        vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r 
            = __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r;
        if ((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r))) {
            __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                = ((IData)((vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w 
                            >> 0x18U)) << 8U);
            __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r = 0U;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r 
                = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r;
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r 
                = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r;
            vlSelfRef.milan_datapath__DOT__zf_adiv_r 
                = __Vdly__milan_datapath__DOT__zf_adiv_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r 
                = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w));
        } else {
            if ((7U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r)))) {
                __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r 
                    = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r)));
                if ((0x20U > (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r))) {
                    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
                        = ((vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
                            << 1U) | (IData)(vlSelfRef.i2s_dac_sdin_o));
                }
                if ((0x20U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r))) {
                    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_frame_a_r 
                        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
                    vlSelfRef.i2s_dac_sdin_o = (1U 
                                                & (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r 
                                                   >> 0x17U));
                    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                        = (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r 
                           << 9U);
                } else {
                    vlSelfRef.i2s_dac_sdin_o = (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                                                >> 0x1fU);
                    __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                        = (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                           << 1U);
                }
            }
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
                = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r 
                = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r;
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r 
                = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r 
                = __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r;
            vlSelfRef.milan_datapath__DOT__zf_adiv_r 
                = __Vdly__milan_datapath__DOT__zf_adiv_r;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w)))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r
                [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r))];
        }
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r = 0U;
        if ((0x01ffU == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w)))) {
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r = 1U;
            }
        }
    } else {
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync = 0U;
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r = 0U;
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r;
        vlSelfRef.milan_datapath__DOT__tone_gen__DOT__cnt_r 
            = __Vdly__milan_datapath__DOT__tone_gen__DOT__cnt_r;
        vlSelfRef.milan_datapath__DOT__tone_gen__DOT__idx_r 
            = __Vdly__milan_datapath__DOT__tone_gen__DOT__idx_r;
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r = 0U;
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_frame_a_r = 0U;
        __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r = 0U;
        vlSelfRef.i2s_dac_sdin_o = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r 
            = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r 
            = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r 
            = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__adiv_r 
            = __Vdly__milan_datapath__DOT__crf_tx__DOT__adiv_r;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r 
            = __Vdly__milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__arst_n_r 
            = __Vdly__milan_datapath__DOT__crf_tx__DOT__arst_n_r;
        vlSelfRef.milan_datapath__DOT__zf_adiv_r = __Vdly__milan_datapath__DOT__zf_adiv_r;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r 
        = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w 
        = ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r) 
                     >> 1U))) || ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n) 
                                  == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r2_r)));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r))) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r2_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r1_r;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r1_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_r;
    } else {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r2_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r1_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n 
        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r) 
                          + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n) 
           ^ ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n) 
              >> 1U));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r 
        = __Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r;
}

void Vmilan_datapath___024root___nba_sequent__TOP__5(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__5\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r = 0;
    SData/*13:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 0;
    CData/*7:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync = 0;
    // Body
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r;
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r 
        = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r))) {
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_tog));
        vlSelfRef.o_mmcm_ps_en = 0U;
        if (vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r) {
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r = 1U;
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r))) {
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r));
            if (vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r) {
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r 
                    = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r) 
                             >> 0x0eU));
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r 
                    = (0x00003fffU & (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r));
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r 
                    = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r;
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r))) {
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r = 1U;
            vlSelfRef.o_mmcm_ps_en = 1U;
            vlSelfRef.o_mmcm_ps_incdec = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r;
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r = 0xffU;
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 2U;
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r))) {
            if (vlSelfRef.i_mmcm_ps_done) {
                if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r))) {
                    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 0U;
                } else {
                    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r 
                        = (0x00003fffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r) 
                                          - (IData)(1U)));
                    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 1U;
                }
            } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r))) {
                vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r = 1U;
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 0U;
            } else {
                __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r 
                    = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r) 
                                      - (IData)(1U)));
            }
        } else {
            __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r) {
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r 
                = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_out_r;
        }
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync) 
                                      >> 1U))))) {
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_tog 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_tog)));
            vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_out_r 
                = vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__data_hold;
        }
    } else {
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_tog = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = 0U;
        vlSelfRef.o_mmcm_ps_en = 0U;
        vlSelfRef.o_mmcm_ps_incdec = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r = 0U;
        __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_out_r = 0U;
    }
    __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r 
        = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r) 
                  << 1U)) | (IData)(vlSelfRef.axis_resetn));
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r 
        = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r) 
                  >> 1U)) && (1U & VL_REDXOR_32((3U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync) 
                                                    >> 1U)))));
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync;
    vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r 
        = __Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r;
}

void Vmilan_datapath___024root___nba_sequent__TOP__6(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__6\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s;
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s;
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s;
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s = 0;
    VlWide<3>/*95:0*/ __Vtemp_3;
    VlWide<3>/*95:0*/ __Vtemp_4;
    VlWide<3>/*95:0*/ __Vtemp_5;
    VlWide<3>/*95:0*/ __Vtemp_6;
    VlWide<3>/*95:0*/ __Vtemp_9;
    VlWide<3>/*95:0*/ __Vtemp_10;
    VlWide<3>/*95:0*/ __Vtemp_11;
    // Body
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s;
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s;
    __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s;
    vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U];
    vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U];
    vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U] 
        = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U];
    if (vlSelfRef.gtx_resetn) {
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_tgl));
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_tgl));
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl));
        if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot_valid) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl_ts 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl_ts)));
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_val_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot;
        }
        if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_pulse_q) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
                = ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap) 
                   << 0x00000018U);
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
                = (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap) 
                    >> 8U) | ((IData)((vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap 
                                       >> 0x00000020U)) 
                              << 0x00000018U));
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U] 
                = ((IData)((vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap 
                            >> 0x00000020U)) >> 8U);
        } else {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U];
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U];
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U];
            if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_sync) {
                VL_EXTENDS_WQ(88,33, __Vtemp_3, (QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_sync)));
                VL_EXTENDS_WI(88,32, __Vtemp_4, vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_sync);
                VL_ADD_W(3, __Vtemp_5, __Vtemp_3, __Vtemp_4);
                VL_ADD_W(3, __Vtemp_6, vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next, __Vtemp_5);
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                    = __Vtemp_6[0U];
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                    = __Vtemp_6[1U];
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                    = (0x00ffffffU & __Vtemp_6[2U]);
            }
            if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_pulse_q) {
                VL_EXTENDS_WQ(88,64, __Vtemp_9, vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__offset_cap);
                VL_SHIFTL_WWI(88,88,32, __Vtemp_10, __Vtemp_9, 0x00000018U);
                VL_ADD_W(3, __Vtemp_11, vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next, __Vtemp_10);
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U] 
                    = __Vtemp_11[0U];
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U] 
                    = __Vtemp_11[1U];
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U] 
                    = (0x00ffffffU & __Vtemp_11[2U]);
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[1U];
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U] 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next[2U];
        }
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_sync 
            = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_meta;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_sync 
            = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_meta;
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s) 
                                      >> 1U))))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_twhi)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_twlo)));
        }
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s) 
                                      >> 1U))))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__offset_cap 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_ofhi)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_oflo)));
        }
        if ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s) 
                                      >> 1U))))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U])) 
                    << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U])) 
                                        << 8U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U])) 
                                                  >> 0x00000018U)));
        }
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_meta 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_incr;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_meta 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj;
    } else {
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s = 0U;
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s = 0U;
        __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl_ts = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_val_ts = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_sync = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_sync = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__offset_cap = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_meta = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_meta = 0U;
    }
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_pulse_q 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & VL_REDXOR_32(
                                                               (3U 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s) 
                                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_pulse_q 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & VL_REDXOR_32(
                                                               (3U 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s) 
                                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_sync 
        = ((IData)(vlSelfRef.gtx_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_meta));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot_valid 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & VL_REDXOR_32(
                                                               (3U 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s) 
                                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s 
        = __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s 
        = __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s 
        = __Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_meta 
        = ((IData)(vlSelfRef.gtx_resetn) && (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_ctrl));
}

void Vmilan_datapath___024root___nba_sequent__TOP__7(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__7\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r = 0;
    SData/*9:0*/ __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r = 0;
    IData/*30:0*/ __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r = 0;
    QData/*51:0*/ __VdlyVal__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0;
    __VdlyVal__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0;
    __VdlyDim0__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0;
    __VdlySet__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    // Body
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r 
        = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
        = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r 
        = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r;
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r 
        = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r;
    __VdlySet__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0U;
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__mdiv_r 
        = (IData)((((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r) 
                    >> 1U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__mdiv_r))));
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r 
        = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r) 
                  >> 1U)) && ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__tick_w))) 
                              && (1U & ((IData)(1U) 
                                        + (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r)))));
    __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r 
        = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r) 
                  << 1U)) | (IData)(vlSelfRef.axis_resetn));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r))) {
        if (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w) {
            __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
                = ((0x7ffffffeU & (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
                                   << 1U)) | (IData)(vlSelfRef.tdm_data_i));
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r)))) {
            vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r)));
        }
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r 
            = __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r;
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_full_w)))) {
            __VdlyVal__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_slot_r)) 
                    << 0x00000030U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_l_r)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_r_r))));
            __VdlyDim0__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r));
            __VdlySet__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 1U;
        }
    } else {
        __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r 
            = __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r;
    }
    if (__VdlySet__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r[__VdlyDim0__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0] 
            = __VdlyVal__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r))) {
        if (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w) {
            if ((0x03ffU == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r))) {
                __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r = 0U;
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fsync_r = 1U;
            } else {
                __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r 
                    = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r)));
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fsync_r = 0U;
            }
            vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__startp_r 
                = (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r));
        }
    } else {
        __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fsync_r = 1U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__startp_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r 
        = __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r;
    vlSelfRef.i2s_mclk_o = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__mdiv_r;
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__tick_w 
        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r)));
    vlSelfRef.tdm_bclk_o = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r;
    vlSelfRef.tdm_fsync_o = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fsync_r;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r))) {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w) {
            if ((0x1fU == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__ebit_w))) {
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bit_r = 0U;
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__slot_r 
                    = (0x0000001fU & ((0x1fU == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w))
                                       ? 0U : ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w))));
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w))) {
                    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_slot_r 
                        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w) 
                                          >> 1U));
                    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_r_r 
                        = (0x00ffffffU & (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
                                          >> 7U));
                    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_l_r 
                        = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__lhold_r;
                    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r 
                        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_full_w)));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bit_r 
                    = (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__ebit_w)));
                vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__slot_r 
                    = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w));
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bit_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_r_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_l_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_full_w 
        = ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r) 
                  >> 1U)) && ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n) 
                              == ((0x0000000cU & ((~ 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r) 
                                                    >> 2U)) 
                                                  << 2U)) 
                                  | (3U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r)))));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r))) {
        if (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w) {
            if ((0x1fU == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__ebit_w))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w)))) {
                    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__lhold_r 
                        = (0x00ffffffU & (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
                                          >> 7U));
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w1_r;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w1_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_r;
    } else {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__lhold_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w1_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r 
        = __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r;
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__slot_r) 
           & (- (IData)((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__startp_r))))));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__ebit_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bit_r) 
           & (- (IData)((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__startp_r))))));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r))));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r) 
                          + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_full_w)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r))));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n) 
           ^ ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n) 
              >> 1U));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r 
        = __Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r;
}

extern const VlUnpacked<CData/*3:0*/, 512> Vmilan_datapath__ConstPool__TABLE_hc68454f1_0;
extern const VlWide<10>/*319:0*/ Vmilan_datapath__ConstPool__CONST_h8a04c6be_0;
extern const VlWide<30>/*959:0*/ Vmilan_datapath__ConstPool__CONST_h99b8ac36_0;
extern const VlUnpacked<IData/*16:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h441640be_0;
extern const VlUnpacked<CData/*4:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h91c136a7_0;
extern const VlUnpacked<CData/*1:0*/, 128> Vmilan_datapath__ConstPool__TABLE_h3d59c2d6_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vmilan_datapath__ConstPool__TABLE_hbb7d8a2c_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vmilan_datapath__ConstPool__TABLE_hec53cc74_0;

void Vmilan_datapath___024root___nba_sequent__TOP__8(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__8\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m = 0;
    SData/*14:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m = 0;
    CData/*6:0*/ __Vtableidx3;
    __Vtableidx3 = 0;
    IData/*29:0*/ __VdfgRegularize_h6e95ff9d_0_23;
    __VdfgRegularize_h6e95ff9d_0_23 = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp_listener_reg;
    __Vdly__milan_datapath__DOT__lwsrp_listener_reg = 0;
    SData/*9:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 0;
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = 0;
    SData/*9:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0;
    SData/*9:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__lwsrp_stream_gate;
    __Vdly__milan_datapath__DOT__lwsrp_stream_gate = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 0;
    SData/*10:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r = 0;
    CData/*4:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r = 0;
    VlWide<5>/*149:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r;
    VL_ZERO_W(150, __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r);
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r = 0;
    VlWide<5>/*149:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r;
    VL_ZERO_W(150, __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r);
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r = 0;
    CData/*2:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 0;
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w = 0;
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w = 0;
    SData/*14:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r = 0;
    IData/*16:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r = 0;
    CData/*7:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r = 0;
    SData/*13:0*/ __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r;
    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = 0;
    QData/*63:0*/ __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r;
    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r = 0;
    IData/*16:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r = 0;
    SData/*8:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r = 0;
    SData/*15:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r = 0;
    QData/*63:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r = 0;
    CData/*7:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r = 0;
    IData/*19:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0;
    IData/*23:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = 0;
    IData/*23:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = 0;
    IData/*23:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = 0;
    IData/*23:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = 0;
    CData/*0:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0;
    QData/*43:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0;
    IData/*23:0*/ __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r = 0;
    SData/*15:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r = 0;
    CData/*1:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 0;
    CData/*3:0*/ __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 = 0;
    CData/*3:0*/ __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0;
    __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v1;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v1 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 = 0;
    CData/*3:0*/ __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0;
    __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v1;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v1 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 = 0;
    CData/*3:0*/ __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0;
    __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v1;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v1 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v2;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v2 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v1;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v1 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v6;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v6 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v2;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v2 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v10;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v10 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v3;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v3 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v14;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v14 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v4;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v4 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v18;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v18 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v5;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v5 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v22;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v22 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v6;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v6 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v26;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v26 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v7;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v7 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v30;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v30 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33 = 0;
    IData/*29:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v8;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v8 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v34;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v34 = 0;
    CData/*4:0*/ __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35;
    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v36;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v36 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v9;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v9 = 0;
    QData/*47:0*/ __VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0;
    __VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0;
    __VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    CData/*0:0*/ __VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0;
    __VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    VlWide<14>/*447:0*/ __Vtemp_8;
    VlWide<4>/*127:0*/ __Vtemp_9;
    VlWide<5>/*159:0*/ __Vtemp_11;
    VlWide<5>/*159:0*/ __Vtemp_13;
    // Body
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_timers__DOT__ms_ctr_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_timers__DOT__ms_ctr_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r 
        = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hidx_r;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v1 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v1 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__state_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__state_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r;
    __VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__src_mac_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__src_mac_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__req_valid_w 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__req_valid_w;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lane_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lane_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
    __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
        = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r;
    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r;
    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__tout_r 
        = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__tout_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__settle_r 
        = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__settle_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__have_seq_r 
        = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__have_seq_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hfill_r 
        = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hfill_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__crf_locked_w 
        = vlSelfRef.milan_datapath__DOT__crf_locked_w;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v2 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v6 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v10 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v14 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v18 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v22 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v26 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v30 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v34 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v36 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v9 = 0U;
    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
        = vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cap_par_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cap_par_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ecap_par_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ecap_par_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__vbase_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__vbase_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__pack_idx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__pack_idx_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__dom_a_evt_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__dom_a_evt_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_class_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_class_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_prio_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_prio_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_vid_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_vid_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tfail_code_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tfail_code_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__hdr_idx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__hdr_idx_r;
    __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r 
        = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__frame_pend_r;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 = 0U;
    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v1 = 0U;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_failed 
        = vlSelfRef.milan_datapath__DOT__lwsrp_ta_failed;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_registered 
        = vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r;
    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r;
    __Vdly__milan_datapath__DOT__lwsrp_listener_reg 
        = vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U];
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r;
    __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__req_pop_w 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__req_pop_w;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pop_pend_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pop_pend_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_rl_ms_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_rl_ms_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_dirty_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_dirty_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkup_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkup_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkdn_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkdn_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_gmchg_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_gmchg_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw3_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw3_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_status_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_status_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_reject_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_reject_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__discard_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__discard_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_ph_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_ph_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_done_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_done_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_n_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_n_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bidx_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bidx_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_rlen_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_rlen_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__status_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__status_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bslh_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bslh_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bcdl_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bcdl_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cdl_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cdl_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_frame_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_frame_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__sysuid_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__sysuid_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__started_in_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__started_in_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend2_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend2_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend3_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend3_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_dlen_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_dlen_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_len_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_len_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsc_lo_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsc_lo_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsch_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsch_r;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v0 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v5 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v6 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v7 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v9 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v10 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v1 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v2 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v3 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v4 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ptr_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ptr_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ph_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ph_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cwld_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cwld_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bscan_ph_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bscan_ph_r;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v0 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v1 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v2 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v3 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cap_done_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cap_done_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw1_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw1_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend4_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend4_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[0U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[0U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[1U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[1U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[2U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[2U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[3U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[3U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[4U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[4U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[5U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[5U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[6U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[6U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[7U] 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q[7U];
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_cnt_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_cnt_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fi_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fi_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_base_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_base_q;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v0 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v1 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v2 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v3 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__batch_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__batch_q;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__state_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__state_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__vu_q 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__vu_q;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v4 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v5 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v18 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v44 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v45 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v46 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v50 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v52 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v57 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v61 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v62 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v65 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v66 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v68 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v71 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v75 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v76 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v77 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v80 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v81 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v82 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v86 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v87 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v88 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v100 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v101 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v104 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v108 = 0U;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q__v43 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v59 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v60 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v82 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v90 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v91 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v92 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v93 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v94 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v95 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v96 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v97 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v98 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v99 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v100 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v101 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v106 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v107 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v108 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v109 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v110 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v111 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v112 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v113 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v114 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v115 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v116 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v117 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v122 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v123 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v124 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v125 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v126 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v127 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v128 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v129 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v130 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v131 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v132 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v133 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v0 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v17 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v34 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v35 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v36 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v37 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v38 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v39 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v40 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v41 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v42 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v43 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v44 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v47 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v48 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v49 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v51 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v52 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v54 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v57 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v58 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v61 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v62 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v63 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v64 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v65 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v66 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v67 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v68 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v70 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v71 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v72 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v73 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v74 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v75 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v76 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v77 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v79 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v80 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v81 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v83 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v84 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v85 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v86 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v87 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v88 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v89 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v102 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v103 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v104 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v105 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v118 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v119 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v120 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v121 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q__v18 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v49 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v51 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v56 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v67 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v91 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v8 = 0U;
    vlSelfRef.__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v134 = 0U;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_pend_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r;
    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r;
    vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__pres_offset_r 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__pres_offset_r;
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxv_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.m_axis_rx_tvalid));
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__lwsrp_ctx_oor_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxv_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.m_axis_rx_tvalid));
    vlSelfRef.milan_datapath__DOT__crf_srp_own_r = 
        ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__crf_srp_svc_w));
    vlSelfRef.milan_datapath__DOT__acmp_tbl_gnt_w = 
        ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_tbl_ok));
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit) {
            if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok) {
                vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hidx_r)));
                vlSelfRef.milan_datapath__DOT__crf_pducnt_w 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__crf_pducnt_w)));
                vlSelfRef.milan_datapath__DOT__crf_delta_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_crf_ts) 
                       - ((vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
                           << 8U) | (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
                                     >> 0x00000018U)));
            }
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok)))) {
                vlSelfRef.milan_datapath__DOT__crf_fmterr_w 
                    = (0x000000ffU & ((0x000000ffU 
                                       == (IData)(vlSelfRef.milan_datapath__DOT__crf_fmterr_w))
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__crf_fmterr_w)
                                       : ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__crf_fmterr_w))));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__svc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_we_i)) 
             & (0U != (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i)))) {
            if ((0x0eU >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                          - (IData)(1U))))) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 
                    = vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_interval_i;
                __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 
                    = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 
                    = vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_max_frame_i;
                __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 
                    = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0 = 1U;
            }
        }
        if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp_idle_slope 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_nx_w;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__grant_r 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w;
            vlSelfRef.milan_datapath__DOT__lwsrp_over_limit 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__refuse_w));
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r = 0U;
        } else {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r 
                = (0x3fffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__fit_w)
                                   ? vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cand_w
                                   : vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r));
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_r 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_r 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_nx_w;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__refuse_w));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_active)) 
             & ((8U != (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r)) 
                | (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w)))) {
            __VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in)));
            __VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r;
            __VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 1U;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r)));
        }
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r 
            = (0x0000000fU & (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r) 
                               + ((((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc) 
                                    & (IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_active)) 
                                   & ((8U != (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r)) 
                                      | (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w)))
                                   ? 1U : 0U)) - ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w)
                                                   ? 1U
                                                   : 0U)));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__lfsr_r 
            = ((0x0000fffeU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__lfsr_r) 
                               << 1U)) | (1U & VL_REDXOR_16(
                                                            (0xb400U 
                                                             & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__lfsr_r)))));
        if (vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r) {
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gap_r))) {
                vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r = 0U;
            } else {
                vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gap_r 
                    = (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gap_r) 
                                      - (IData)(1U)));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast))) {
            vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r = 1U;
            vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gap_r = 0x01ffU;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__tick_1khz_w))) {
            if ((0U == vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r)) {
                __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = 0U;
                __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r = 0ULL;
            } else {
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r 
                    = (0x0001ffffU & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r 
                                      - (IData)(1U)));
            }
        }
        if ((((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[0U] 
               & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__val_msgtype_w))) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__w_block_locked))) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__w_lock_denied)))) {
            if ((1U == (0x00007fffU & ((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U] 
                                        << 0x0000000eU) 
                                       | (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U] 
                                          >> 0x00000012U))))) {
                if ((0x00020000U & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U])) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r) 
                         & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[4U])) 
                              << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[3U])) 
                                                  << 0x0000000eU) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U])) 
                                                    >> 0x00000012U))) 
                            == vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r))) {
                        __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = 0U;
                        __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r = 0ULL;
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r = 0U;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r) {
                    if (((((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[4U])) 
                           << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[3U])) 
                                               << 0x0000000eU) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U])) 
                                                 >> 0x00000012U))) 
                         == vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r)) {
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r = 0x0000ea60U;
                    }
                } else {
                    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = 1U;
                    __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[4U])) 
                            << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[3U])) 
                                                << 0x0000000eU) 
                                               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U])) 
                                                  >> 0x00000012U)));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r = 0x0000ea60U;
                }
            }
            if ((1U != (0x00007fffU & ((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U] 
                                        << 0x0000000eU) 
                                       | (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U] 
                                          >> 0x00000012U))))) {
                if ((6U == (0x00007fffU & ((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[2U] 
                                            << 0x0000000eU) 
                                           | (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U] 
                                              >> 0x00000012U))))) {
                    if ((1U > (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U] 
                                              >> 1U)))) {
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r 
                            = (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__hdr_w[1U] 
                                              >> 1U));
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r 
            = __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r 
            = __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r;
        if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__dom_class_a_w) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__dom_match_w)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 1U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = 0x4e20U;
            } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__dom_match_w) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = 0U;
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r 
                    = (0x00007fffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r) 
                                      - (IData)(1U)));
                if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 0U;
                }
            }
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U])))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                        = ((0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]) 
                           | (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                             - (IData)(1U))));
                    if ((1U == (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7ffeU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                         & (0U == (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U])))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                            = (0x0258U | (0xfffffc00U 
                                          & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                    }
                }
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                        } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0x0258U | (0xfffffc00U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                        }
                    }
                } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7ffeU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7ffeU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                    = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
            }
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                              >> 0x0000000aU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                        = ((0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]) 
                           | (0x000ffc00U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                << 0x00000016U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                  >> 0x0000000aU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000aU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                               >> 0x0000000aU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7ffdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 1U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                              >> 0x0000000aU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                            = (0x00096000U | (0xfff003ffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                    }
                }
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                        } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0x00096000U | (0xfff003ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                        }
                    }
                } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7ffdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7ffdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                    = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
            }
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                              >> 0x00000014U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                        = ((0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]) 
                           | (0x3ff00000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                << 0x0000000cU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                  >> 0x00000014U)) 
                                              - (IData)(1U)) 
                                             << 0x00000014U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                               >> 0x00000014U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7ffbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 2U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                              >> 0x00000014U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                            = (0x25800000U | (0xc00fffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                    }
                }
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                        } else if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0x25800000U | (0xc00fffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]));
                        }
                    }
                } else if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7ffbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7ffbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                    = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
            }
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                               << 2U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                 >> 0x0000001eU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                        = ((0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                 << 2U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                           >> 0x0000001eU)) 
                               - (IData)(1U)) << 0x0000001eU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                        = ((0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]) 
                           | (0x000000ffU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                << 2U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                  >> 0x0000001eU)) 
                                              - (IData)(1U)) 
                                             >> 2U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                << 2U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                  >> 0x0000001eU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7ff7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 3U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                               << 2U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                                 >> 0x0000001eU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                            = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                            = (0x00000096U | (0xffffff00U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                    }
                }
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
                        } else if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0x00000096U | (0xffffff00U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                        }
                    }
                } else if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7ff7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7ff7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
                    = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                    = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
            }
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                              >> 8U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                        = ((0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]) 
                           | (0x0003ff00U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                << 0x00000018U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                  >> 8U)) 
                                              - (IData)(1U)) 
                                             << 8U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                               >> 8U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7fefU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 4U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                              >> 8U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                            = (0x00025800U | (0xfffc00ffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                    }
                }
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
                        } else if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0x00025800U | (0xfffc00ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                        }
                    }
                } else if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7fefU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7fefU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                    = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
            }
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                              >> 0x00000012U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                        = ((0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]) 
                           | (0x0ffc0000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                << 0x0000000eU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                  >> 0x00000012U)) 
                                              - (IData)(1U)) 
                                             << 0x00000012U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                               >> 0x00000012U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7fdfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 5U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                              >> 0x00000012U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                            = (0x09600000U | (0xf003ffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                    }
                }
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
                        } else if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0x09600000U | (0xf003ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                        }
                    }
                } else if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7fdfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7fdfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                    = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
            }
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                 >> 0x0000001cU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                        = ((0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                 << 4U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                           >> 0x0000001cU)) 
                               - (IData)(1U)) << 0x0000001cU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                        = ((0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]) 
                           | (0x0000003fU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                  >> 0x0000001cU)) 
                                              - (IData)(1U)) 
                                             >> 4U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                  >> 0x0000001cU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7fbfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 6U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                                 >> 0x0000001cU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                            = (0x80000000U | (0x0fffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                            = (0x00000025U | (0xffffffc0U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                    }
                }
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
                        } else if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                                = (0x80000000U | (0x0fffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0x00000025U | (0xffffffc0U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                        }
                    }
                } else if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7fbfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7fbfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
                    = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                    = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
            }
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                              >> 6U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                        = ((0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]) 
                           | (0x0000ffc0U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                << 0x0000001aU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                  >> 6U)) 
                                              - (IData)(1U)) 
                                             << 6U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                               >> 6U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7f7fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 7U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                              >> 6U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                            = (0x00009600U | (0xffff003fU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                    }
                }
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
                        } else if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0x00009600U | (0xffff003fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                        }
                    }
                } else if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7f7fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7f7fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                    = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
            }
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                              >> 0x00000010U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                        = ((0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]) 
                           | (0x03ff0000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                << 0x00000010U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                  >> 0x00000010U)) 
                                              - (IData)(1U)) 
                                             << 0x00000010U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                               >> 0x00000010U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7effU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 8U) & (0U == (0x000003ffU 
                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                              >> 0x00000010U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                            = (0x02580000U | (0xfc00ffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                    }
                }
                if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
                        } else if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0x02580000U | (0xfc00ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                        }
                    }
                } else if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7effU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7effU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                    = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
            }
            if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                               << 6U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                 >> 0x0000001aU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                        = ((0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                 << 6U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                           >> 0x0000001aU)) 
                               - (IData)(1U)) << 0x0000001aU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                        = ((0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]) 
                           | (0x0000000fU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                << 6U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                  >> 0x0000001aU)) 
                                              - (IData)(1U)) 
                                             >> 6U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                << 6U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                  >> 0x0000001aU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7dffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 9U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                               << 6U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                                 >> 0x0000001aU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                            = (0x60000000U | (0x03ffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                            = (9U | (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                    }
                }
                if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000200U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
                        } else if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                                = (0x60000000U | (0x03ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (9U | (0xfffffff0U 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                        }
                    }
                } else if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000200U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7dffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7dffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
                    = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                    = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
            }
            if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                              >> 4U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                        = ((0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]) 
                           | (0x00003ff0U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                << 0x0000001cU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                  >> 4U)) 
                                              - (IData)(1U)) 
                                             << 4U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                               >> 4U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x7bffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 0x0aU) & (0U == (0x000003ffU 
                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                 >> 4U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                            = (0x00002580U | (0xffffc00fU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                    }
                }
                if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000400U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
                        } else if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0x00002580U | (0xffffc00fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                        }
                    }
                } else if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000400U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x7bffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x7bffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                    = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
            }
            if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                              >> 0x0000000eU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                        = ((0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]) 
                           | (0x00ffc000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                << 0x00000012U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                  >> 0x0000000eU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000eU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                               >> 0x0000000eU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x77ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 0x0bU) & (0U == (0x000003ffU 
                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                 >> 0x0000000eU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                            = (0x00960000U | (0xff003fffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                    }
                }
                if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00000800U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
                        } else if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0x00960000U | (0xff003fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                        }
                    }
                } else if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00000800U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x77ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x77ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                    = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
            }
            if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                               << 8U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                 >> 0x00000018U)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                        = ((0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                 << 8U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                           >> 0x00000018U)) 
                               - (IData)(1U)) << 0x00000018U));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                        = ((0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]) 
                           | (3U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                       << 8U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                 >> 0x00000018U)) 
                                     - (IData)(1U)) 
                                    >> 8U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                << 8U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                  >> 0x00000018U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x6fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 0x0cU) & (0U == (0x000003ffU 
                                              & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                  << 8U) 
                                                 | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                                    >> 0x00000018U)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                            = (0x58000000U | (0x00ffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                            = (2U | (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                    }
                }
                if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00001000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
                        } else if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                                = (0x58000000U | (0x00ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (2U | (0x003ffffcU 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                        }
                    }
                } else if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00001000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x6fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x6fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
                    = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                    = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
            }
            if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                              >> 2U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                        = ((0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]) 
                           | (0x00000ffcU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                << 0x0000001eU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                  >> 2U)) 
                                              - (IData)(1U)) 
                                             << 2U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                               >> 2U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x5fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 0x0dU) & (0U == (0x000003ffU 
                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                 >> 2U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                            = (0x00000960U | (0x003ff003U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                    }
                }
                if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00002000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
                        } else if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (0x00000960U | (0x003ff003U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                        }
                    }
                } else if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00002000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x5fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x5fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                    = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
            }
            if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                              >> 0x0000000cU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                        = ((0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]) 
                           | (0x003ff000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                << 0x00000014U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                  >> 0x0000000cU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000cU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                               >> 0x0000000cU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                            = (0x3fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)) 
                          >> 0x0eU) & (0U == (0x000003ffU 
                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                                 >> 0x0000000cU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                            = (0x00258000U | (0x00000fffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                    }
                }
                if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                                = (0x00004000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
                        } else if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                                = (0x00258000U | (0x00000fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]));
                        }
                    }
                } else if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x00004000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                } else if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                        = (0x3fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
                    = (0x3fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r));
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
                    = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U]);
            }
        } else {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] = 0U;
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r;
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__overflow_reg) {
            vlSelfRef.milan_datapath__DOT__lwsrp_rx_drops 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_rx_drops)));
        }
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q2_r))) {
            __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 
                = ((0x0000000000004189ULL < vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__iv_bytes_r)
                    ? 0x3fffffffU : (0x3fffffffU & 
                                     ((IData)(0x0000fa00U) 
                                      * (0x00007fffU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__iv_bytes_r)))));
            __VdlyDim0__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q2_r;
            __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT____Vcellinp__ta_registrar__enable_i) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                 & (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r 
                    = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r) 
                                      - (IData)(1U)));
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_failed = 0U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_failed) 
                     & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0x0258U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_tfail_p) {
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__w_join_evt) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_failed = 1U;
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0U;
                } else if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_evt)) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_failed))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0x0258U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                 & (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r 
                    = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r) 
                                      - (IData)(1U)));
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_registered = 0U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered) 
                     & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0x0258U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_tadv_p) {
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__w_join_evt) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_registered = 1U;
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0U;
                } else if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_evt)) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0x0258U;
                }
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_failed = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_registered = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U];
        if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__evt_cmd_w) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__cmd_cnt_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__cmd_cnt_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__evt_resp_w) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__resp_cnt_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__resp_cnt_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__pres_wr_p_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__pres_offset_r 
                = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__pres_wr_val_w;
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r;
        vlSelfRef.milan_datapath__DOT__pcm_lpf_tvalid = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_active)))) {
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in;
        }
        if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w) {
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 1U;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0U;
            __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0ULL;
        } else if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                 & (5U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))) {
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)));
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                    = (0x00000fffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w)
                                                 ? 
                                                (- 
                                                 VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))
                                                 : 
                                                VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w)));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                        & (0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))) {
                vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                    = (((QData)((IData)(((0x00ff0000U 
                                          & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w 
                                             << 0x00000010U)) 
                                         | ((0x0000ff00U 
                                             & vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w) 
                                            | (0x000000ffU 
                                               & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w 
                                                  >> 0x10U)))))) 
                        << 0x00000020U) | (QData)((IData)(
                                                          ((0x00ff0000U 
                                                            & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
                                                               << 0x00000010U)) 
                                                           | ((0x0000ff00U 
                                                               & vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r) 
                                                              | (0x000000ffU 
                                                                 & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
                                                                    >> 0x10U)))))));
                vlSelfRef.milan_datapath__DOT__pcm_lpf_tvalid = 1U;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0U;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r;
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w;
            } else {
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                    = (0x00000fffffffffffULL & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                                                + ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w)
                                                    ? 
                                                   (- 
                                                    VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))
                                                    : 
                                                   VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))));
                __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r;
        if ((((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_want_w) 
              != (IData)(vlSelfRef.milan_datapath__DOT__crf_srp_last_r)) 
             | ((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_want_w) 
                & ((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                    != vlSelfRef.milan_datapath__DOT__crf_srp_sid_r) 
                   | (vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                      != vlSelfRef.milan_datapath__DOT__crf_srp_dmac_r))))) {
            vlSelfRef.milan_datapath__DOT__crf_srp_req_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__crf_srp_svc_w) {
            vlSelfRef.milan_datapath__DOT__crf_srp_val_r 
                = vlSelfRef.milan_datapath__DOT__crf_srp_want_w;
            vlSelfRef.milan_datapath__DOT__crf_srp_req_r = 0U;
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[0U];
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0 = 1U;
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v2 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01feU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01feU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v1 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[1U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v6 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01fdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01fdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v2 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[2U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v10 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01fbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01fbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v3 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[3U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v14 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01f7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01f7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v4 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[4U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v18 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01efU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01efU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v5 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[5U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v22 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01dfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01dfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v6 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[6U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v26 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x01bfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x01bfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v7 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[7U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v30 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x017fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x017fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r))) {
                if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U])) {
                    __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U]) 
                                          - (IData)(1U)));
                    __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32 = 1U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                        = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
                }
            } else {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33 = 1U;
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v8 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[8U];
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
        } else {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate))) {
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v34 = 1U;
            } else if ((0U != vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U])) {
                __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U]) 
                                      - (IData)(1U)));
                __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35 = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
                    = (0x00ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
            }
            __Vdly__milan_datapath__DOT__lwsrp_stream_gate 
                = (0x00ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp_stream_gate));
        }
        vlSelfRef.milan_datapath__DOT__lwsrp_slope_en 
            = (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r));
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r = 0U;
        __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v1 = 1U;
        __VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__lfsr_r = 0xace1U;
        vlSelfRef.milan_datapath__DOT__crf_pducnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__crf_fmterr_w = 0U;
        vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gap_r = 0U;
        vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r = 0U;
        __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r = 0ULL;
        __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r 
            = __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r 
            = __Vdly__milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r;
        vlSelfRef.milan_datapath__DOT__lwsrp_rx_drops = 0U;
        __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_failed = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r;
        vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp_ta_registered = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[0U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[1U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[2U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[3U];
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U] 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r[4U];
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__cmd_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__resp_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aecp_listener__DOT__pres_offset_r = 0x001e8480U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_idle_slope = 0U;
        vlSelfRef.milan_datapath__DOT__crf_delta_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__grant_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_over_limit = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r;
        vlSelfRef.milan_datapath__DOT__crf_srp_val_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0ULL;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r = 0U;
        __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata = 0ULL;
        vlSelfRef.milan_datapath__DOT__pcm_lpf_tvalid = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
            = __Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_srp_req_r = 0U;
        __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v36 = 1U;
        __Vdly__milan_datapath__DOT__lwsrp_stream_gate = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_slope_en = 0U;
        __VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v9 = 1U;
    }
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r;
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[__VdlyDim0__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v0;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r__v1) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[8U] = 0U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[0U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[1U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v1;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[2U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v2;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[3U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v3;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[4U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v4;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[5U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v5;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[6U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v6;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[7U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v7;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[8U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v8;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v0;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v2) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v3;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v4;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v5) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v6) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v7;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v8;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v9) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v10) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v11;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v12;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v13) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v14) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v15;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v16;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v17) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v18) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v19;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v20;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v21) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v22) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v23;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v24;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v25) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v26) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v27;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v28;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v29) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v30) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v31;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v32;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v33) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v34) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U] = 0x10U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v35;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r__v36) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[0U] = 0U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r__v9) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[8U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate 
        = __Vdly__milan_datapath__DOT__lwsrp_stream_gate;
    if (vlSelfRef.axis_resetn) {
        if ((1U & (((VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__sync) 
                                         >> 1U))) & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__frame_pend_r))) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r))))) {
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U])) 
                     << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U])) 
                                         << 8U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U])) 
                                                   >> 0x00000018U))) 
                   + (QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__pres_offset_r)));
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__tu_r 
                = vlSelfRef.milan_datapath__DOT__clkv_tu_w;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vln_r 
                = vlSelfRef.milan_datapath__DOT__crft_class_a_w;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vpcp_r = 3U;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vvid_r 
                = (0x00000fffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid);
            __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r = 1U;
        }
        if ((1U & (~ vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl))) {
            __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) {
            if (vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active) 
                     & ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready)))) {
                    if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r))) {
                        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__seq_r 
                            = (0x000000ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__seq_r)));
                        vlSelfRef.milan_datapath__DOT__crft_count_w 
                            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__crft_count_w);
                        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r = 0U;
                        __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r = 0U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r)));
                    }
                }
            } else {
                vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r = 0U;
            }
        } else if (vlSelfRef.milan_datapath__DOT__crf_tx__DOT__frame_pend_r) {
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r = 0U;
            vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__frame_pend_r 
            = __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r;
        if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) {
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__svc_w) {
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i))) {
                    vlSelfRef.milan_datapath__DOT__srp_ctx_rd_sid_w 
                        = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                             [(((IData)(0x0000003fU) 
                                                + ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                   << 6U)) 
                                               >> 5U)])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                               [
                                                               (0x07fffffeU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                   << 1U))]))) 
                           & (- (QData)((IData)((0x03bfU 
                                                 >= 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                  << 6U))))));
                    vlSelfRef.milan_datapath__DOT__srp_ctx_rd_stat_w 
                        = (((((((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                   >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))) 
                               << 3U) | (((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                             >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))) 
                                         << 2U)) | 
                             ((((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r) 
                                   >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))) 
                               << 1U) | ((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                            >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))))) 
                            << 0x0000000cU) | ((((0x0eU 
                                                  >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w) 
                                                    >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))) 
                                                << 0x0000000bU) 
                                               | ((((0x0eU 
                                                     >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w)) 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r) 
                                                       >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w))) 
                                                   << 0x0000000aU) 
                                                  | ((0x00000300U 
                                                      & (((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                           >> 
                                                           ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                            << 1U)) 
                                                          & (- (IData)(
                                                                       (0x1dU 
                                                                        >= 
                                                                        ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                         << 1U))))) 
                                                         << 8U)) 
                                                     | (0x000000ffU 
                                                        & ((((0U 
                                                              == 
                                                              (0x0000001fU 
                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                  << 3U)))
                                                              ? 0U
                                                              : 
                                                             (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r
                                                              [
                                                              (((IData)(7U) 
                                                                + 
                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                 << 3U)) 
                                                               >> 5U)] 
                                                              << 
                                                              ((IData)(0x00000020U) 
                                                               - 
                                                               (0x0000001fU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                   << 3U))))) 
                                                            | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r
                                                               [
                                                               (0x07ffffffU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                   >> 2U))] 
                                                               >> 
                                                               (0x0000001fU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                   << 3U)))) 
                                                           & (- (IData)(
                                                                        (0x77U 
                                                                         >= 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w) 
                                                                          << 3U))))))))));
                } else {
                    vlSelfRef.milan_datapath__DOT__srp_ctx_rd_sid_w 
                        = (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                           << 0x00000010U);
                    vlSelfRef.milan_datapath__DOT__srp_ctx_rd_stat_w 
                        = ((((3U == (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                             << 0x0000000fU) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared) 
                                                 << 0x0000000dU) 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg) 
                                                   << 0x0000000cU))) 
                           | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready) 
                               << 0x0000000bU) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tfail_valid) 
                                                   << 0x0000000aU) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl) 
                                                      << 8U) 
                                                     | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tfail_code)))));
                }
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r)))) {
            if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r))) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r = 1U;
            } else {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp 
            = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_pend_r;
        if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r) 
             & (3U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp)))) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp)));
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__start 
            = (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r))) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r) 
                  | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r) 
                     | ((IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r) 
                           | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_now) 
                              | ((0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_pend_r)) 
                                 | (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_fail_r) 
                                     != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_failed)) 
                                    | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_reg_r) 
                                       != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered))))))))));
        if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__start) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r = 1U;
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r = 0U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_ms_r 
                = (0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_1s_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_adp_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_now));
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp))) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp 
                    = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp) 
                             - (IData)(1U)));
            }
        } else if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_reg_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_reg_r)) 
                       | (0x01ffU & (((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)) 
                                      && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered) 
                                                >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)))) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))));
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_fail_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_fail_r)) 
                       | (0x01ffU & (((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)) 
                                      && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_failed) 
                                                >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)))) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))));
            }
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_probe_set_w) {
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))) {
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
                        = ((IData)(__Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))));
                }
            }
            if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r = 0U;
            } else {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_pend_r 
            = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__mp;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s) 
                | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r)) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__start)));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_now) 
                | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r)) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sweep_seq__DOT__start)));
        if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_cap_hs) {
            if ((9U <= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 1U;
            }
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r) 
                              >> 2U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r)))) {
                            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r 
                                = ((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                             >> 8U))));
                            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_vlan_r 
                                = ((0x00000f00U & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                            >> 0x10U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                             >> 0x18U))));
                        }
                    }
                }
            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r 
                            = ((0x0000ffff00000000ULL 
                                & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r) 
                               | (IData)((IData)(((
                                                   ((0x0000ff00U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                        << 8U)) 
                                                    | (0x000000ffU 
                                                       & (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                  >> 8U)))) 
                                                   << 0x00000010U) 
                                                  | ((0x0000ff00U 
                                                      & ((IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                  >> 0x10U)) 
                                                         << 8U)) 
                                                     | (0x000000ffU 
                                                        & (IData)(
                                                                  (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                   >> 0x18U))))))));
                    } else {
                        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r 
                            = (((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                << 8U)) 
                                | (0x000000ffU & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                          >> 8U)))) 
                               == (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id)));
                        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r 
                            = ((0x0000ff00U & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                        >> 0x10U)) 
                                               << 8U)) 
                               | (0x000000ffU & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                         >> 0x18U))));
                        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r 
                            = ((0x0000ff00U & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                        >> 0x20U)) 
                                               << 8U)) 
                               | (0x000000ffU & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                         >> 0x28U))));
                        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r 
                            = ((0x00000000ffffffffULL 
                                & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r) 
                               | ((QData)((IData)((
                                                   (0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x30U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                 >> 0x38U)))))) 
                                  << 0x00000020U));
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                        = ((0xffffffffffff0000ULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r) 
                           | (IData)((IData)(((0x0000ff00U 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                  << 8U)) 
                                              | (0x000000ffU 
                                                 & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                            >> 8U)))))));
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r 
                        = ((((QData)((IData)(((((0x0000ff00U 
                                                 & ((IData)(
                                                            (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                             >> 0x10U)) 
                                                    << 8U)) 
                                                | (0x000000ffU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                              >> 0x18U)))) 
                                               << 0x00000010U) 
                                              | ((0x0000ff00U 
                                                  & ((IData)(
                                                             (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                              >> 0x20U)) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                               >> 0x28U))))))) 
                             << 0x00000010U) | (QData)((IData)(
                                                               ((0x0000ff00U 
                                                                 & ((IData)(
                                                                            (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                             >> 0x30U)) 
                                                                    << 8U)) 
                                                                | (0x000000ffU 
                                                                   & (IData)(
                                                                             (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                              >> 0x38U))))))) 
                           == (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                               >> 0x10U));
                } else {
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r 
                        = ((0xffffffffffff0000ULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r) 
                           | (IData)((IData)(((0x0000ff00U 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                  << 8U)) 
                                              | (0x000000ffU 
                                                 & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                            >> 8U)))))));
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                        = ((0x000000000000ffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r) 
                           | (((QData)((IData)(((((0x0000ff00U 
                                                   & ((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                               >> 0x10U)) 
                                                      << 8U)) 
                                                  | (0x000000ffU 
                                                     & (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x18U)))) 
                                                 << 0x00000010U) 
                                                | ((0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x20U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                 >> 0x28U))))))) 
                               << 0x00000020U) | ((QData)((IData)(
                                                                  ((0x0000ff00U 
                                                                    & ((IData)(
                                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x30U)) 
                                                                       << 8U)) 
                                                                   | (0x000000ffU 
                                                                      & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x38U)))))) 
                                                  << 0x00000010U)));
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
                        = ((0xffffffffffff0000ULL & __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r) 
                           | (IData)((IData)(((0x0000ff00U 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                  << 8U)) 
                                              | (0x000000ffU 
                                                 & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                            >> 8U)))))));
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r 
                        = ((0x000000000000ffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r) 
                           | (((QData)((IData)(((((0x0000ff00U 
                                                   & ((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                               >> 0x10U)) 
                                                      << 8U)) 
                                                  | (0x000000ffU 
                                                     & (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x18U)))) 
                                                 << 0x00000010U) 
                                                | ((0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x20U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                 >> 0x28U))))))) 
                               << 0x00000020U) | ((QData)((IData)(
                                                                  ((0x0000ff00U 
                                                                    & ((IData)(
                                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x30U)) 
                                                                       << 8U)) 
                                                                   | (0x000000ffU 
                                                                      & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x38U)))))) 
                                                  << 0x00000010U)));
                } else {
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_status_r 
                        = (0x0000001fU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                  >> 3U)));
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
                        = ((0x000000000000ffffULL & __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r) 
                           | (((QData)((IData)(((((0x0000ff00U 
                                                   & ((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                               >> 0x10U)) 
                                                      << 8U)) 
                                                  | (0x000000ffU 
                                                     & (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x18U)))) 
                                                 << 0x00000010U) 
                                                | ((0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                >> 0x20U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                 >> 0x28U))))))) 
                               << 0x00000020U) | ((QData)((IData)(
                                                                  ((0x0000ff00U 
                                                                    & ((IData)(
                                                                               (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x30U)) 
                                                                       << 8U)) 
                                                                   | (0x000000ffU 
                                                                      & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x38U)))))) 
                                                  << 0x00000010U)));
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r 
                    = (0x22f0U == ((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                            >> 0x20U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                             >> 0x28U)))));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                              >> 0x30U)));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r 
                    = (0U == (0x0000000fU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                     >> 0x3cU))));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r 
                    = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                              >> 0x38U)));
            } else {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r 
                    = (0x000091e0f0010000ULL == (((QData)((IData)(
                                                                  ((((0x0000ff00U 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r) 
                                                                         << 8U)) 
                                                                     | (0x000000ffU 
                                                                        & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 8U)))) 
                                                                    << 0x00000010U) 
                                                                   | ((0x0000ff00U 
                                                                       & ((IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x10U)) 
                                                                          << 8U)) 
                                                                      | (0x000000ffU 
                                                                         & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x18U))))))) 
                                                  << 0x00000010U) 
                                                 | (QData)((IData)(
                                                                   ((0x0000ff00U 
                                                                     & ((IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x20U)) 
                                                                        << 8U)) 
                                                                    | (0x000000ffU 
                                                                       & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
                                                                                >> 0x28U))))))));
            }
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 0U;
            }
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r 
                = ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))
                    ? 0x0000000aU : (0x0000000fU & 
                                     ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r))));
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxl_r) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r 
                    = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxk_r) 
                          >> 5U));
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) {
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 1U;
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[0U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][0U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[1U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][1U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][2U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][3U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[4U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][4U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[5U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][5U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[6U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][6U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][7U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][8U];
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                        [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                          & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][9U];
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_luid_idx;
                }
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_len_ok_r 
                    = ((4U <= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r)) 
                       | ((3U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r)) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxk_r) 
                             >> 1U)));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = 0U;
            }
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__active) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tready)))) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r = 0U;
                if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
                    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) {
                        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)));
                    }
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 0U;
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = 0U;
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 0U;
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0U;
                } else {
                    __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r)));
                }
            } else if ((0x000fffffU == vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r)) {
                vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge 
                    = (0x000000ffU & ((0x000000ffU 
                                       == (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge))
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge)
                                       : ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge))));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 0U;
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r = 0U;
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = 0U;
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 0U;
            } else {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r 
                    = (0x000fffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r));
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_classify_r 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_classify_r)));
            if ((0xfcU == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_fc_r 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_fc_r)));
                if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_acmp_base) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_is_lstn_cmd))) {
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_basehit_r 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_basehit_r)));
                }
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_flags_r 
                    = ((((((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r) 
                           << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r) 
                                     << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r))) 
                        << 4U) | ((((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r) 
                                    << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r) 
                                              << 2U)) 
                                  | (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r) 
                                      << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_is_lstn_cmd))));
            }
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_seen) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_eid_r 
                    = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r;
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_avail_r 
                    = (0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r));
            }
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstn_hit) {
                vlSelfRef.milan_datapath__DOT__acmpl_cmd_count 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmpl_cmd_count)));
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 2U;
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_msg_r 
                    = (1U | (0x0000000eU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r)));
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_status_r 
                    = ((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r))
                        ? 0U : 1U);
                if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_set_w) {
                    if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r))) {
                        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
                            = ((IData)(__Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r) 
                               | (0x01ffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r))));
                    }
                }
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r 
                    = (3U & (0xaaa98aaaU >> ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r) 
                                             << 1U)));
            } else {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 0U;
            }
        } else if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok) {
            if ((8U >= Vmilan_datapath__ConstPool__TABLE_hc68454f1_0
                 [vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r])) {
                __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
                    = ((~ ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_hc68454f1_0
                           [vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r])) 
                       & (IData)(__Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r));
            }
            vlSelfRef.milan_datapath__DOT__acmpl_probe_count 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmpl_probe_count)));
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0U;
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 3U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[0U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][0U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[1U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][1U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][2U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][3U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[4U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][4U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[5U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][5U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[6U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][6U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][7U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][8U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][9U];
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r 
                = Vmilan_datapath__ConstPool__TABLE_hc68454f1_0
                [vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r];
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__sweep_seq__DOT__start 
            = ((~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_active_r)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__s1_pend_r) 
                  | (IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s)));
        if (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__sweep_seq__DOT__start) {
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_active_r = 1U;
            __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_swp_run) {
            if (((((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r)) 
                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v) 
                             >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r)))) 
                  & (0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tmr_rd_w))) 
                 & (~ ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r)) 
                       && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_lobs_v_w) 
                                 >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r))))))) {
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r))) {
                    vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v));
                }
            }
            if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_active_r = 0U;
            } else {
                __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__s1_pend_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s) 
                | (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__s1_pend_r)) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__sweep_seq__DOT__start)));
        if (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_cap_hs) {
            if ((9U <= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__ovfl_r = 1U;
            }
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__ovfl_r = 0U;
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r)))) {
                            __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r 
                                = ((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                            >> 0x10U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                             >> 0x18U))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tk_lo_ok_r 
                            = (((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r) 
                                                << 8U)) 
                                | (0x000000ffU & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                          >> 8U)))) 
                               == (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id)));
                    } else {
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tk_hi_ok_r 
                            = ((((QData)((IData)(((
                                                   ((0x0000ff00U 
                                                     & ((IData)(
                                                                (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                 >> 0x10U)) 
                                                        << 8U)) 
                                                    | (0x000000ffU 
                                                       & (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                  >> 0x18U)))) 
                                                   << 0x00000010U) 
                                                  | ((0x0000ff00U 
                                                      & ((IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                  >> 0x20U)) 
                                                         << 8U)) 
                                                     | (0x000000ffU 
                                                        & (IData)(
                                                                  (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                   >> 0x28U))))))) 
                                 << 0x00000010U) | (QData)((IData)(
                                                                   ((0x0000ff00U 
                                                                     & ((IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                                >> 0x30U)) 
                                                                        << 8U)) 
                                                                    | (0x000000ffU 
                                                                       & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                                >> 0x38U))))))) 
                               == (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                   >> 0x10U));
                    }
                } else if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r) 
                                     >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))) {
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__hdr_ok_r 
                            = (IData)(((0x00fc000000000000ULL 
                                        == (0xf0ff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r)) 
                                       & (0x22f0U == 
                                          ((0x0000ff00U 
                                            & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                        >> 0x20U)) 
                                               << 8U)) 
                                           | (0x000000ffU 
                                              & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                         >> 0x28U)))))));
                        __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r 
                            = (0x0000000fU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                      >> 0x38U)));
                    } else {
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__dst_ok_r 
                            = (0x000091e0f0010000ULL 
                               == (((QData)((IData)(
                                                    ((((0x0000ff00U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r) 
                                                           << 8U)) 
                                                       | (0x000000ffU 
                                                          & (IData)(
                                                                    (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                     >> 8U)))) 
                                                      << 0x00000010U) 
                                                     | ((0x0000ff00U 
                                                         & ((IData)(
                                                                    (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                     >> 0x10U)) 
                                                            << 8U)) 
                                                        | (0x000000ffU 
                                                           & (IData)(
                                                                     (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                      >> 0x18U))))))) 
                                    << 0x00000010U) 
                                   | (QData)((IData)(
                                                     ((0x0000ff00U 
                                                       & ((IData)(
                                                                  (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                   >> 0x20U)) 
                                                          << 8U)) 
                                                      | (0x000000ffU 
                                                         & (IData)(
                                                                   (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
                                                                    >> 0x28U))))))));
                    }
                }
            }
            __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r 
                = ((9U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))
                    ? 9U : (0x0000000fU & ((IData)(1U) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r))));
            if (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxl_r) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))) {
                    __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 1U;
                }
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__len_ok_r 
                    = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxk_r) 
                          >> 5U));
                __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r = 0U;
            }
        }
        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))) {
                if (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_hit) {
                    vlSelfRef.milan_datapath__DOT__acmp_cmd_count 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__acmp_cmd_count)));
                    __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 2U;
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_msg_r 
                        = (1U | (0x0000000eU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r)));
                    __Vtemp_8[0U] = (IData)(vlSelfRef.milan_datapath__DOT__eff_aaf_dmac);
                    __Vtemp_8[1U] = (((IData)((0x0000ffffffffffffULL 
                                               & (1ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      << 0x00000010U) 
                                     | (IData)((vlSelfRef.milan_datapath__DOT__eff_aaf_dmac 
                                                >> 0x00000020U)));
                    __Vtemp_8[2U] = (((IData)((0x0000ffffffffffffULL 
                                               & (1ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      >> 0x00000010U) 
                                     | ((IData)(((0x0000ffffffffffffULL 
                                                  & (1ULL 
                                                     + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                 >> 0x00000020U)) 
                                        << 0x00000010U));
                    __Vtemp_8[3U] = (IData)((0x0000ffffffffffffULL 
                                             & (2ULL 
                                                + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)));
                    __Vtemp_8[4U] = (((IData)((0x0000ffffffffffffULL 
                                               & (3ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      << 0x00000010U) 
                                     | (IData)(((0x0000ffffffffffffULL 
                                                 & (2ULL 
                                                    + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                >> 0x00000020U)));
                    __Vtemp_8[5U] = (((IData)((0x0000ffffffffffffULL 
                                               & (3ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      >> 0x00000010U) 
                                     | ((IData)(((0x0000ffffffffffffULL 
                                                  & (3ULL 
                                                     + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                 >> 0x00000020U)) 
                                        << 0x00000010U));
                    __Vtemp_8[6U] = (IData)((0x0000ffffffffffffULL 
                                             & (4ULL 
                                                + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)));
                    __Vtemp_8[7U] = (((IData)((0x0000ffffffffffffULL 
                                               & (5ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      << 0x00000010U) 
                                     | (IData)(((0x0000ffffffffffffULL 
                                                 & (4ULL 
                                                    + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                >> 0x00000020U)));
                    __Vtemp_8[8U] = (((IData)((0x0000ffffffffffffULL 
                                               & (5ULL 
                                                  + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                      >> 0x00000010U) 
                                     | ((IData)(((0x0000ffffffffffffULL 
                                                  & (5ULL 
                                                     + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                 >> 0x00000020U)) 
                                        << 0x00000010U));
                    __Vtemp_8[9U] = (IData)((0x0000ffffffffffffULL 
                                             & (6ULL 
                                                + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)));
                    __Vtemp_8[10U] = (((IData)((0x0000ffffffffffffULL 
                                                & (7ULL 
                                                   + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                       << 0x00000010U) 
                                      | (IData)(((0x0000ffffffffffffULL 
                                                  & (6ULL 
                                                     + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                 >> 0x00000020U)));
                    __Vtemp_8[11U] = (((IData)((0x0000ffffffffffffULL 
                                                & (7ULL 
                                                   + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac))) 
                                       >> 0x00000010U) 
                                      | ((IData)(((0x0000ffffffffffffULL 
                                                   & (7ULL 
                                                      + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                  >> 0x00000020U)) 
                                         << 0x00000010U));
                    __Vtemp_8[12U] = (((0x0000ffffU 
                                        & (IData)((0x0000ffffffffffffULL 
                                                   & (8ULL 
                                                      + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)))) 
                                       | ((IData)((
                                                   (0x0000ffffffffffffULL 
                                                    & (7ULL 
                                                       + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                   >> 0x00000020U)) 
                                          >> 0x00000010U)) 
                                      | (0xffff0000U 
                                         & (IData)(
                                                   (0x0000ffffffffffffULL 
                                                    & (8ULL 
                                                       + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)))));
                    __Vtemp_8[13U] = (0x0000ffffU & (IData)(
                                                            ((0x0000ffffffffffffULL 
                                                              & (8ULL 
                                                                 + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)) 
                                                             >> 0x00000020U)));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                        = ((0x01afU >= (0x000001ffU 
                                        & ((IData)(0x00000030U) 
                                           * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))
                            ? (0x0000ffffffffffffULL 
                               & (((QData)((IData)(__Vtemp_8
                                                   [
                                                   (((IData)(0x0000002fU) 
                                                     + 
                                                     (0x000001ffU 
                                                      & ((IData)(0x00000030U) 
                                                         * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))) 
                                                    >> 5U)])) 
                                   << ((0U == (0x0000001fU 
                                               & ((IData)(0x00000030U) 
                                                  * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))
                                        ? 0x00000020U
                                        : ((IData)(0x00000040U) 
                                           - (0x0000001fU 
                                              & ((IData)(0x00000030U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))))) 
                                  | (((0U == (0x0000001fU 
                                              & ((IData)(0x00000030U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))
                                       ? 0ULL : ((QData)((IData)(__Vtemp_8
                                                                 [
                                                                 (((IData)(0x0000001fU) 
                                                                   + 
                                                                   (0x000001ffU 
                                                                    & ((IData)(0x00000030U) 
                                                                       * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))) 
                                                                  >> 5U)])) 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & ((IData)(0x00000030U) 
                                                      * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))))) 
                                     | ((QData)((IData)(__Vtemp_8
                                                        [
                                                        (0x0000000fU 
                                                         & (((IData)(0x00000030U) 
                                                             * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)) 
                                                            >> 5U))])) 
                                        >> (0x0000001fU 
                                            & ((IData)(0x00000030U) 
                                               * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))))))
                            : 0ULL);
                    __Vtemp_9[0U] = (IData)((((QData)((IData)(
                                                              (0x00ffffffU 
                                                               & ((0x00fff000U 
                                                                   & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                      >> 4U)) 
                                                                  | (0x00000fffU 
                                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        >> 0x00000010U)))))) 
                                              << 0x00000024U) 
                                             | (0x0000000fffffffffULL 
                                                & (((QData)((IData)(
                                                                    (0x00000fffU 
                                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        >> 0x00000010U)))) 
                                                    << 0x00000018U) 
                                                   | (((QData)((IData)(
                                                                       (0x00000fffU 
                                                                        & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                           >> 0x00000010U)))) 
                                                       << 0x0000000cU) 
                                                      | (QData)((IData)(
                                                                        (0x00000fffU 
                                                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                            >> 0x00000010U)))))))));
                    __Vtemp_9[1U] = (((IData)((((QData)((IData)(
                                                                (0x00ffffffU 
                                                                 & ((0x00fff000U 
                                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        >> 4U)) 
                                                                    | (0x00000fffU 
                                                                       & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                          >> 0x00000010U)))))) 
                                                << 0x00000018U) 
                                               | (QData)((IData)(
                                                                 (0x00ffffffU 
                                                                  & ((0x00fff000U 
                                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                         >> 4U)) 
                                                                     | (0x00000fffU 
                                                                        & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                           >> 0x00000010U)))))))) 
                                      << 0x0000001cU) 
                                     | (IData)(((((QData)((IData)(
                                                                  (0x00ffffffU 
                                                                   & ((0x00fff000U 
                                                                       & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                          >> 4U)) 
                                                                      | (0x00000fffU 
                                                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                            >> 0x00000010U)))))) 
                                                  << 0x00000024U) 
                                                 | (0x0000000fffffffffULL 
                                                    & (((QData)((IData)(
                                                                        (0x00000fffU 
                                                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                            >> 0x00000010U)))) 
                                                        << 0x00000018U) 
                                                       | (((QData)((IData)(
                                                                           (0x00000fffU 
                                                                            & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                               >> 0x00000010U)))) 
                                                           << 0x0000000cU) 
                                                          | (QData)((IData)(
                                                                            (0x00000fffU 
                                                                             & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                >> 0x00000010U)))))))) 
                                                >> 0x00000020U)));
                    __Vtemp_9[2U] = (((IData)((((QData)((IData)(
                                                                (0x00ffffffU 
                                                                 & ((0x00fff000U 
                                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        >> 4U)) 
                                                                    | (0x00000fffU 
                                                                       & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                          >> 0x00000010U)))))) 
                                                << 0x00000018U) 
                                               | (QData)((IData)(
                                                                 (0x00ffffffU 
                                                                  & ((0x00fff000U 
                                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                         >> 4U)) 
                                                                     | (0x00000fffU 
                                                                        & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                           >> 0x00000010U)))))))) 
                                      >> 4U) | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (0x00ffffffU 
                                                                            & ((0x00fff000U 
                                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                >> 4U)) 
                                                                               | (0x00000fffU 
                                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                >> 0x00000010U)))))) 
                                                           << 0x00000018U) 
                                                          | (QData)((IData)(
                                                                            (0x00ffffffU 
                                                                             & ((0x00fff000U 
                                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                >> 4U)) 
                                                                                | (0x00000fffU 
                                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                >> 0x00000010U))))))) 
                                                         >> 0x00000020U)) 
                                                << 0x0000001cU));
                    __Vtemp_9[3U] = ((IData)(((((QData)((IData)(
                                                                (0x00ffffffU 
                                                                 & ((0x00fff000U 
                                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        >> 4U)) 
                                                                    | (0x00000fffU 
                                                                       & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                          >> 0x00000010U)))))) 
                                                << 0x00000018U) 
                                               | (QData)((IData)(
                                                                 (0x00ffffffU 
                                                                  & ((0x00fff000U 
                                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                         >> 4U)) 
                                                                     | (0x00000fffU 
                                                                        & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                           >> 0x00000010U))))))) 
                                              >> 0x00000020U)) 
                                     >> 4U);
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_vid_r 
                        = ((0x6bU >= (0x0000007fU & 
                                      ((IData)(0x0000000cU) 
                                       * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))
                            ? (0x00000fffU & (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & ((IData)(0x0000000cU) 
                                                    * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))
                                                ? 0U
                                                : (__Vtemp_9
                                                   [
                                                   (((IData)(0x0000000bU) 
                                                     + 
                                                     (0x0000007fU 
                                                      & ((IData)(0x0000000cU) 
                                                         * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & ((IData)(0x0000000cU) 
                                                        * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)))))) 
                                              | (__Vtemp_9
                                                 [(3U 
                                                   & (((IData)(0x0000000cU) 
                                                       * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))))))
                            : 0U);
                    __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r = 0U;
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = 0U;
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r = 0U;
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r))) {
                        if ((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r))) {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 0U;
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = 2U;
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r = 0x000aU;
                            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))) {
                                vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v 
                                    = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v) 
                                       | (0x01ffU & 
                                          ((IData)(1U) 
                                           << (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx))));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 2U;
                        }
                    } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r))) {
                        if ((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r))) {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 0U;
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = 1U;
                        } else {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 2U;
                        }
                    } else if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r))) {
                        if ((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r))) {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 0U;
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = 2U;
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r = 0x004aU;
                        } else {
                            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 2U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 0x1fU;
                    }
                } else {
                    __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 0U;
                }
            } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__active) 
                     & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__gsel) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tready)))) {
                    if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
                        vlSelfRef.milan_datapath__DOT__acmp_resp_count 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__acmp_resp_count)));
                        __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 0U;
                        __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r = 0U;
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__ovfl_r = 0U;
                        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__len_ok_r = 0U;
                    } else {
                        __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r)));
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 0U;
            }
        }
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r;
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r 
                = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r))
                    ? 0U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r))));
        }
        if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__enable_q)) 
                   & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = 1U;
            if ((2U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 1U;
            }
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 1U;
            }
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
        }
        if (((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_q)) 
             & (3U == (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                    & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r)) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_q))))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
        }
        if (((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
              & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared)) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered) 
                ^ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_ready_q)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
        }
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r))) 
                | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
        }
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
        }
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_fastjoin_w))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
        }
        if ((IData)((((1U == (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_q)) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r = 1U;
        }
        if ((((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_q)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r = 1U;
        }
        if (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__enable_q))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r = 1U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 0U;
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r))) {
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r 
                    = vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r 
                    = vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r = 5U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r = 5U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r = 5U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 1U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r = 5U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r = 5U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 1U;
            } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r = 5U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 1U;
            } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r 
                    = (IData)((3U == (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r 
                    = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                             & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r)));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r)
                        ? 0U : 1U);
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r)
                        ? 0U : 1U);
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r)
                        ? 0U : 1U);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 1U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = 0U;
                if ((IData)((3U == (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 0U;
                    vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared = 1U;
                }
                if ((1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 0U;
                    vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared = 1U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r) {
                if ((5U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r)
                            ? 0U : 1U);
                }
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 1U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = 0U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 0U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tready)))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                     == (0x0000000fU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w)
                                          ? 0x0bU : 8U) 
                                        - (IData)(1U))))) {
                    vlSelfRef.milan_datapath__DOT__lwsrp_tx_count 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_count)));
                    if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r = 1U;
                    }
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r = 7U;
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 2U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r 
                = (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r) 
                                  - (IData)(1U)));
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 0U;
            }
        } else {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 0U;
        }
    } else {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__crft_count_w = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r = 0ULL;
        __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__tu_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vln_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vpcp_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vvid_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__frame_pend_r 
            = __Vdly__milan_datapath__DOT__crf_tx__DOT__frame_pend_r;
        vlSelfRef.milan_datapath__DOT__srp_ctx_rd_sid_w = 0ULL;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmpl_cmd_count = 0U;
        vlSelfRef.milan_datapath__DOT__acmpl_probe_count = 0U;
        vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_classify_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_fc_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_basehit_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_len_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_status_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r = 0ULL;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_vlan_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r = 2U;
        VL_ASSIGN_W(317, vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r, Vmilan_datapath__ConstPool__CONST_h8a04c6be_0);
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_ms_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_1s_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_adp_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_avail_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_reg_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_fail_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_flags_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r 
            = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r;
        vlSelfRef.milan_datapath__DOT__srp_ctx_rd_stat_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r 
            = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_cmd_count = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_resp_count = 0U;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__ovfl_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__len_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__dst_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__hdr_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tk_hi_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tk_lo_ok_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_vid_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_active_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__s1_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__wbeat_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__wbeat_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__swp_idx_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__msg_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__msg_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__tuid_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__beat_r;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r 
            = __Vdly__milan_datapath__DOT__acmp_responder__DOT__st_r;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_tx_count = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r = 1U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_lstn_declared = 0U;
    }
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r;
    __VdfgRegularize_h6e95ff9d_0_23 = (0x3fffffffU 
                                       & ((IData)((0x00000fffffffffffULL 
                                                   & VL_SHIFTRS_QQI(44,44,32, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r, 0x0000000eU))) 
                                          + (1U & (- (IData)(
                                                             (1U 
                                                              & (IData)(
                                                                        (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                                                                         >> 0x0000000dU))))))));
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
           | ((4U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
              | ((8U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
                 | (9U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cand_w 
        = (0x7fffffffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r
                           [vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r] 
                           & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))))) 
                          + vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_nx_w 
        = (0x7fffffffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_r 
                          + (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r
                             [vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r] 
                             & (- (IData)(((8U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r)) 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r) 
                                              >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstnr_us 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_luid_idx 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r) 
                          & (- (IData)((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_is_lstn_cmd 
        = ((6U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r)) 
           | ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r)) 
              | (0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid 
        = (((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)) 
            & ((0x01feU >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)) 
               & (0ULL != vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r)))
            ? vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r
            : (((QData)((IData)((0x00ffffffU & (IData)(
                                                       (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                                                        >> 0x00000028U))))) 
                << 0x00000028U) | (((QData)((IData)(
                                                    (0x00ffffffU 
                                                     & ((0xfffeU 
                                                         == 
                                                         (0x0000ffffU 
                                                          & (IData)(
                                                                    (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                                                                     >> 0x00000018U))))
                                                         ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r)
                                                         : (IData)(
                                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                                                                    >> 0x00000010U)))))) 
                                    << 0x00000010U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r)))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_sm_en 
        = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)) 
           & (1U >> (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
        = (0x0000ffffffffffffULL & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                     ? vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r
                                     : ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U])) 
                                          << 0x00000020U) 
                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[6U]))) 
                                        & (- (QData)((IData)(
                                                             ((0U 
                                                               != 
                                                               (7U 
                                                                & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                                   >> 0x0000001aU))) 
                                                              & (2U 
                                                                 == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r)))))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_flags_match 
        = ((0U != (8U & (((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                           << 4U) | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                     >> 0x0000001cU)) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r)))) 
           | (0U == (8U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r) 
                           | ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                               << 4U) | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                         >> 0x0000001cU))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_same_talker 
        = ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
            == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U])) 
                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U])))) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r) 
              == (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                 >> 0x0000000cU))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxv_r));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxl_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.s_axis_mac_rx_tlast));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) 
           & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxv_r) 
                  | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r) 
                     | (0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r))))) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
           | (3U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r) 
                          & (- (IData)((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r))))));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxl_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.s_axis_mac_rx_tlast));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_cap_hs 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxv_r) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r)) 
              | (1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_ready_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__enable_q 
        = ((IData)(vlSelfRef.axis_resetn) && (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     (3U 
                                                      == 
                                                      (3U 
                                                       & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_q 
        = ((IData)(vlSelfRef.axis_resetn) && (1U & 
                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r))));
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__acmp_rest_ack_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_pend) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_sm_ok)))) {
            vlSelfRef.milan_datapath__DOT__acmp_rest_status_w = 2U;
            vlSelfRef.milan_datapath__DOT__acmp_rest_ack_w = 1U;
        } else if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok) {
            vlSelfRef.milan_datapath__DOT__acmp_rest_status_w 
                = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16)
                    ? 0U : 1U);
            vlSelfRef.milan_datapath__DOT__acmp_rest_ack_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__srp_ctx_gnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_discover_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_tbl_ok) {
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[0U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][0U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[1U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][1U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[2U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][2U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[3U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][3U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[4U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][4U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[5U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][5U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[6U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][6U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[7U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][7U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[8U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][8U];
            vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o[9U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][9U];
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q2_r 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r;
        __Vtemp_11[0U] = (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[7U]) 
                           << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec 
                                              >> 0x00000010U));
        __Vtemp_11[1U] = (IData)((((QData)((IData)(
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[11U]) 
                                                     << 0x00000010U) 
                                                    | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[10U]))) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[9U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[8U])))));
        __Vtemp_11[2U] = (IData)(((((QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[11U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[10U]))) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[9U]) 
                                                       << 0x00000010U) 
                                                      | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[8U])))) 
                                  >> 0x00000020U));
        __Vtemp_11[3U] = (IData)((((QData)((IData)(
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[14U]) 
                                                     << 0x00000010U) 
                                                    | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[13U]))) 
                                   << 0x00000010U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[12U]))));
        __Vtemp_11[4U] = (IData)(((((QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[14U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[13U]))) 
                                    << 0x00000010U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[12U]))) 
                                  >> 0x00000020U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__iv_bytes_r 
            = (0x00000001ffffffffULL & ((QData)((IData)(
                                                        ((0x8fU 
                                                          >= 
                                                          (0x000000ffU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                              << 4U)))
                                                          ? 
                                                         (0x0000ffffU 
                                                          & (((0U 
                                                               == 
                                                               (0x0000001fU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                                   << 4U)))
                                                               ? 0U
                                                               : 
                                                              (__Vtemp_11
                                                               [
                                                               (((IData)(0x0000000fU) 
                                                                 + 
                                                                 (0x000000ffU 
                                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                                     << 4U))) 
                                                                >> 5U)] 
                                                               << 
                                                               ((IData)(0x00000020U) 
                                                                - 
                                                                (0x0000001fU 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                                    << 4U))))) 
                                                             | (__Vtemp_11
                                                                [
                                                                (7U 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                                    >> 1U))] 
                                                                >> 
                                                                (0x0000001fU 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r) 
                                                                    << 4U)))))
                                                          : 0U))) 
                                        * (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__frame_bytes_r))));
        if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w) {
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r 
                = (0x00ffffffU & (IData)((vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r
                                          [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r] 
                                          >> 0x00000018U)));
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r 
                = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r
                                         [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r]));
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__crf_srp_svc_w) {
            vlSelfRef.milan_datapath__DOT__crf_srp_last_r 
                = vlSelfRef.milan_datapath__DOT__crf_srp_want_w;
            vlSelfRef.milan_datapath__DOT__crf_srp_dmac_r 
                = vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w;
            vlSelfRef.milan_datapath__DOT__crf_srp_sid_r 
                = vlSelfRef.milan_datapath__DOT__eff_crft_sid_w;
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxk_r 
            = vlSelfRef.s_axis_mac_rx_tkeep;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r = 0U;
        if ((0x0001869fU == vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r)) {
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r = 1U;
        } else {
            __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r));
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r 
            = vlSelfRef.s_axis_mac_rx_tdata;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxk_r 
            = vlSelfRef.s_axis_mac_rx_tkeep;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r 
            = vlSelfRef.s_axis_mac_rx_tdata;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_fastjoin_w = 0U;
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r 
                = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r))
                    ? 0U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r))));
        }
        if (((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
              & (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) 
             & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w) 
                  & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r))) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p)) 
                | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 1U;
        }
        if ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
             & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r)) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r)) 
                != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__ready_q_r)))) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_done_w) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w)));
            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w)));
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r 
                = (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r) 
                    | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w))) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w)));
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__ready_q_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w) 
                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r));
        if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__kill_pend_r) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__kill_pend_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxv_r) {
            if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxl_r) {
                if ((vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl 
                     & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r))) {
                    vlSelfRef.milan_datapath__DOT__aecp_discover_p = 1U;
                }
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r) 
                          >> 2U)))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r))) {
                        if (((((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__is_avtp_r) 
                               & (0xfaU == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__subtype_r))) 
                              & (2U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__msgtype_r))) 
                             & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxk_r) 
                                >> 1U))) {
                            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r 
                                = ((0ULL == ((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__tgt_hi_r 
                                              << 0x00000010U) 
                                             | (QData)((IData)(
                                                               ((0x0000ff00U 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r) 
                                                                    << 8U)) 
                                                                | (0x000000ffU 
                                                                   & (IData)(
                                                                             (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                              >> 8U)))))))) 
                                   | (((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__tgt_hi_r 
                                        << 0x00000010U) 
                                       | (QData)((IData)(
                                                         ((0x0000ff00U 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r) 
                                                              << 8U)) 
                                                          | (0x000000ffU 
                                                             & (IData)(
                                                                       (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                        >> 8U))))))) 
                                      == vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__tgt_hi_r 
                            = (((QData)((IData)((((
                                                   (0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                >> 0x10U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                 >> 0x18U)))) 
                                                  << 0x00000010U) 
                                                 | ((0x0000ff00U 
                                                     & ((IData)(
                                                                (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                 >> 0x20U)) 
                                                        << 8U)) 
                                                    | (0x000000ffU 
                                                       & (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                  >> 0x28U))))))) 
                                << 0x00000010U) | (QData)((IData)(
                                                                  ((0x0000ff00U 
                                                                    & ((IData)(
                                                                               (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                                >> 0x30U)) 
                                                                       << 8U)) 
                                                                   | (0x000000ffU 
                                                                      & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                                >> 0x38U)))))));
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r))) {
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__is_avtp_r 
                        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_b1_avtp;
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__subtype_r 
                        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                  >> 0x30U)));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__msgtype_r 
                        = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                  >> 0x00000038U)));
                    if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxl_r)) 
                          & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__pushing_r)) 
                         & (~ (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_b1_avtp) 
                                & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__dst_ok_r)) 
                               & (0x00fb000000000000ULL 
                                  == (0x00ff000000000000ULL 
                                      & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r)))))) {
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__drop_rest_r = 1U;
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__kill_pend_r = 1U;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__pushing_r 
                        = (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl);
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__dst_ok_r 
                        = ((((QData)((IData)(((((0x0000ff00U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r) 
                                                    << 8U)) 
                                                | (0x000000ffU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                              >> 8U)))) 
                                               << 0x00000010U) 
                                              | ((0x0000ff00U 
                                                  & ((IData)(
                                                             (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                              >> 0x10U)) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                               >> 0x18U))))))) 
                             << 0x00000010U) | (QData)((IData)(
                                                               ((0x0000ff00U 
                                                                 & ((IData)(
                                                                            (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                             >> 0x20U)) 
                                                                    << 8U)) 
                                                                | (0x000000ffU 
                                                                   & (IData)(
                                                                             (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r 
                                                                              >> 0x28U))))))) 
                           == vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w);
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r = 0U;
                }
            }
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r 
                = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r))
                    ? 4U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r))));
            if (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxl_r) {
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r = 0U;
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__pushing_r = 0U;
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__drop_rest_r = 0U;
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r = 0U;
            }
        }
        __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r 
            = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r))
                ? 0U : (0x0000000fU & ((IData)(1U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r))));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r;
        __Vtemp_13[0U] = (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[7U]) 
                           << 0x00000010U) | (0x0000ffffU 
                                              & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec));
        __Vtemp_13[1U] = (IData)((((QData)((IData)(
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[11U]) 
                                                     << 0x00000010U) 
                                                    | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[10U]))) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[9U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[8U])))));
        __Vtemp_13[2U] = (IData)(((((QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[11U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[10U]))) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[9U]) 
                                                       << 0x00000010U) 
                                                      | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[8U])))) 
                                  >> 0x00000020U));
        __Vtemp_13[3U] = (IData)((((QData)((IData)(
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[14U]) 
                                                     << 0x00000010U) 
                                                    | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[13U]))) 
                                   << 0x00000010U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[12U]))));
        __Vtemp_13[4U] = (IData)(((((QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[14U]) 
                                                      << 0x00000010U) 
                                                     | vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[13U]))) 
                                    << 0x00000010U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[12U]))) 
                                  >> 0x00000020U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__frame_bytes_r 
            = (0x0001ffffU & ((IData)(0x0000002aU) 
                              + ((0x8fU >= (0x000000ffU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                               << 4U)))
                                  ? (0x0000ffffU & 
                                     (((0U == (0x0000001fU 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                                  << 4U)))
                                        ? 0U : (__Vtemp_13
                                                [(((IData)(0x0000000fU) 
                                                   + 
                                                   (0x000000ffU 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                                       << 4U))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                                     << 4U))))) 
                                      | (__Vtemp_13
                                         [(7U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                                 >> 1U))] 
                                         >> (0x0000001fU 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r) 
                                                << 4U)))))
                                  : 0U)));
        if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w))) {
                vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r)) 
                       | (0x01ffU & ((1U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] 
                                            >> 0x00000019U)) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w))));
            }
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) {
            if ((0xc7U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r)));
            }
            if ((0x270fU == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r = 0U;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w = 1U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r 
                    = (0x00003fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_done_w = 0U;
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 0U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r 
                        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r) 
                                          - (IData)(1U)));
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w = 0U;
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w = 0U;
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 0U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
                     & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tready)))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r = 0U;
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r = 0ULL;
                    if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_count_o 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_count_o)));
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_done_w = 1U;
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r = 7U;
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 6U;
                    } else {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 4U;
                    }
                }
            } else if (((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r)) 
                        & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 2U;
            } else {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r 
                    = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r)));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r 
                    = (((~ (0x00000000000000ffULL << 
                            (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r) 
                                            << 3U)))) 
                        & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w)) 
                          << (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r) 
                                             << 3U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__need_load = 0U;
                if (((7U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r)) 
                     | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_end_w))) {
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r 
                        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_end_w;
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 5U;
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r)));
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_end_w) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 8U;
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec 
                                = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))
                                    ? 8U : 7U);
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from 
                                = (0x0000000fU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)));
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m 
                                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r;
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0fU;
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 0x0eU) & (0x0eU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0eU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 0x0dU) & (0x0dU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0dU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 0x0cU) & (0x0cU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0cU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 0x0bU) & (0x0bU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0bU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 0x0aU) & (0x0aU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0x0aU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 9U) & (9U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 9U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 8U) & (8U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 8U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 7U) & (7U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 7U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 6U) & (6U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 6U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 5U) & (5U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 5U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 4U) & (4U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 4U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 3U) & (3U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 3U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 2U) & (2U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 2U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                  >> 1U) & (1U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 1U;
                            }
                            if (((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__m) 
                                 & (0U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout = 0U;
                            }
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                                = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__36__Vfuncout;
                            if ((0x0fU != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow))) {
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 5U;
                            } else {
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 6U;
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 5U;
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m 
                                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r;
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0fU;
                            if ((0x00004000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0eU;
                            }
                            if ((0x00002000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0dU;
                            }
                            if ((0x00001000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0cU;
                            }
                            if ((0x00000800U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0bU;
                            }
                            if ((0x00000400U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0x0aU;
                            }
                            if ((0x00000200U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 9U;
                            }
                            if ((0x00000100U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 8U;
                            }
                            if ((0x00000080U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 7U;
                            }
                            if ((0x00000040U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 6U;
                            }
                            if ((0x00000020U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 5U;
                            }
                            if ((0x00000010U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 4U;
                            }
                            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 3U;
                            }
                            if ((4U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 2U;
                            }
                            if ((2U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 1U;
                            }
                            if ((1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__m))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout = 0U;
                            }
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                                = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__37__Vfuncout;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec 
                                = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r))
                                    ? 4U : 7U);
                        } else {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from 
                                = (0x0000000fU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)));
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m 
                                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r;
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0fU;
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 0x0eU) & (0x0eU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0eU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 0x0dU) & (0x0dU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0dU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 0x0cU) & (0x0cU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0cU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 0x0bU) & (0x0bU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0bU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 0x0aU) & (0x0aU 
                                               >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0x0aU;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 9U) & (9U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 9U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 8U) & (8U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 8U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 7U) & (7U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 7U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 6U) & (6U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 6U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 5U) & (5U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 5U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 4U) & (4U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 4U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 3U) & (3U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 3U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 2U) & (2U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 2U;
                            }
                            if ((((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                  >> 1U) & (1U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 1U;
                            }
                            if (((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__m) 
                                 & (0U >= (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__from)))) {
                                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout = 0U;
                            }
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                                = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__38__Vfuncout;
                            if ((0x0fU != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow))) {
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 2U;
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__need_load = 1U;
                            } else {
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 3U;
                                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec = 2U;
                        __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m 
                            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r;
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__need_load = 1U;
                        __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0fU;
                        if ((0x00004000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0eU;
                        }
                        if ((0x00002000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0dU;
                        }
                        if ((0x00001000U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0cU;
                        }
                        if ((0x00000800U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0bU;
                        }
                        if ((0x00000400U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0x0aU;
                        }
                        if ((0x00000200U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 9U;
                        }
                        if ((0x00000100U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 8U;
                        }
                        if ((0x00000080U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 7U;
                        }
                        if ((0x00000040U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 6U;
                        }
                        if ((0x00000020U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 5U;
                        }
                        if ((0x00000010U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 4U;
                        }
                        if ((8U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 3U;
                        }
                        if ((4U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 2U;
                        }
                        if ((2U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 1U;
                        }
                        if ((1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__m))) {
                            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout = 0U;
                        }
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow 
                            = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__find_row__39__Vfuncout;
                    } else {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec 
                            = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r))
                                ? 1U : ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r))
                                         ? 4U : 7U));
                    }
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r = 0U;
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r 
                        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nsec;
                    vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r 
                        = ((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow))
                            ? (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)
                            : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__nrow));
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r 
                        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__need_load)) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r));
                } else {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r 
                        = (0x0000001fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r)));
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rec_data_w[0U];
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rec_data_w[1U];
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rec_data_w[2U];
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rec_data_w[3U];
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r = 1U;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 4U;
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))) {
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r))) {
                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 1U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 2U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 3U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 4U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 5U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 6U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 7U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 8U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 9U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 0x0aU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 0x0bU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 0x0cU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 0x0dU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__42__m) 
                                               >> 0x0eU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_1 
                    = (0x000003ffU & ((IData)(6U) + 
                                      ((IData)(0x001cU) 
                                       * (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_0__popcnt))));
            } else {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_1 = 0U;
            }
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r;
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r;
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r))) {
                __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r;
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 1U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 2U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 3U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 4U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 5U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 6U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 7U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 8U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 9U))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 0x0aU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 0x0bU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 0x0cU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 0x0dU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt 
                    = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt) 
                                      + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__43__m) 
                                               >> 0x0eU))));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_3 
                    = (0x000003ffU & ((IData)(6U) + 
                                      ((IData)(0x000cU) 
                                       * (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCall_2__popcnt))));
            } else {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_3 = 0U;
            }
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r = 0U;
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (1U & (IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__latch_b__DOT__core 
                = (0x000003ffU & ((IData)(0x0011U) 
                                  + ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_1) 
                                     + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT____VlemCond_3))));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 4U;
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 1U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 1U))));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_len_r 
                = ((0x003cU > (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__latch_b__DOT__core))
                    ? 0x003cU : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ctx_tx_S__DOT__latch_b__DOT__core));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 2U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 2U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 3U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 3U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 4U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 4U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 5U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 5U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 6U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 6U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 7U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 7U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 8U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 8U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 9U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 9U))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 0x0aU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 0x0aU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 0x0bU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 0x0bU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 0x0cU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 0x0cU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 0x0dU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 0x0dU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__m) 
                                           >> 0x0eU))));
            __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout 
                = (0x0000001fU & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout) 
                                  + (1U & ((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__m) 
                                           >> 0x0eU))));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nt_r 
                = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__40__Vfuncout;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nl_r 
                = __Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__popcnt__41__Vfuncout;
        } else if ((((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w)) 
                     | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                        & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r)) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r) 
                              | (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w)))))) 
                    & (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w)))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 1U;
        }
        if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U])))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                        = ((0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]) 
                           | (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                             - (IData)(1U))));
                    if ((1U == (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7ffeU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ffffffcU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                         & (0U == (0x000003ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U])))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                            = (0x0258U | (0xfffffc00U 
                                          & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                    }
                }
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                                = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                        }
                    }
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x0258U | (0xfffffc00U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                } else {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                            = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                    }
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (1U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffffcU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffffcU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                    & (0U == (0x000003ffU 
                                              & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U])))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x0258U | (0xfffffc00U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7ffeU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ffffffcU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                    = (0xfffffc00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
            }
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                              >> 0x0000000aU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                        = ((0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]) 
                           | (0x000ffc00U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                << 0x00000016U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                  >> 0x0000000aU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000aU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                               >> 0x0000000aU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7ffdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 1U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ffffff3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 1U) & (0U == (0x000ffc00U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                            = (0x00096000U | (0xfff003ffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                    }
                }
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                                = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 8U));
                        }
                    }
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x00096000U | (0xfff003ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                } else {
                    if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                            = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 8U));
                    }
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (2U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffff3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0000000cU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffff3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0000000cU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 1U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                   >> 0x0000000aU))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x00096000U | (0xfff003ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7ffdU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ffffff3U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                    = (0xfff003ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
            }
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                              >> 0x00000014U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                        = ((0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]) 
                           | (0x3ff00000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                << 0x0000000cU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                  >> 0x00000014U)) 
                                              - (IData)(1U)) 
                                             << 0x00000014U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                               >> 0x00000014U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7ffbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 2U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3fffffcfU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 2U) & (0U == (0x3ff00000U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                            = (0x25800000U | (0xc00fffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                    }
                }
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                                = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000010U));
                        }
                    }
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x25800000U | (0xc00fffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                } else {
                    if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                            = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000010U));
                    }
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (4U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffffcfU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000030U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffffcfU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000030U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 2U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                   >> 0x00000014U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x25800000U | (0xc00fffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7ffbU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3fffffcfU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                    = (0xc00fffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
            }
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                               << 2U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                 >> 0x0000001eU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                        = ((0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                 << 2U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                           >> 0x0000001eU)) 
                               - (IData)(1U)) << 0x0000001eU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                        = ((0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]) 
                           | (0x000000ffU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                << 2U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                  >> 0x0000001eU)) 
                                              - (IData)(1U)) 
                                             >> 2U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                << 2U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                  >> 0x0000001eU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7ff7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 3U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3fffff3fU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                          >> 3U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                               << 2U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                 >> 0x0000001eU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                            = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                            = (0x00000096U | (0xffffff00U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                    }
                }
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000018U));
                        }
                    }
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x00000096U | (0xffffff00U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                } else {
                    if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] 
                            = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000018U));
                    }
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (8U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffff3fU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x000000c0U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffff3fU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x000000c0U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 3U) & (0U == 
                                               (0x000003ffU 
                                                & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                    << 2U) 
                                                   | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                                      >> 0x0000001eU)))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                                = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x00000096U | (0xffffff00U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7ff7U & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3fffff3fU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
                    = (0x3fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                    = (0xffffff00U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
            }
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                              >> 8U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                        = ((0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]) 
                           | (0x0003ff00U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                << 0x00000018U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                  >> 8U)) 
                                              - (IData)(1U)) 
                                             << 8U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                               >> 8U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7fefU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 4U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ffffcffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 4U) & (0U == (0x0003ff00U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                            = (0x00025800U | (0xfffc00ffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                    }
                }
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                                = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                        }
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x00025800U | (0xfffc00ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                } else {
                    if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                            = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000010U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffcffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000300U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffffcffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000300U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 4U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                   >> 8U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x00025800U | (0xfffc00ffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7fefU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ffffcffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                    = (0xfffc00ffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
            }
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                              >> 0x00000012U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                        = ((0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]) 
                           | (0x0ffc0000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                << 0x0000000eU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                  >> 0x00000012U)) 
                                              - (IData)(1U)) 
                                             << 0x00000012U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                               >> 0x00000012U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7fdfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 5U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ffff3ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 5U) & (0U == (0x0ffc0000U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                            = (0x09600000U | (0xf003ffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                    }
                }
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                                = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 8U));
                        }
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x09600000U | (0xf003ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                } else {
                    if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                            = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 8U));
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000020U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffff3ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000c00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffff3ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00000c00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 5U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                   >> 0x00000012U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x09600000U | (0xf003ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7fdfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ffff3ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                    = (0xf003ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
            }
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                 >> 0x0000001cU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                        = ((0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                 << 4U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                           >> 0x0000001cU)) 
                               - (IData)(1U)) << 0x0000001cU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                        = ((0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]) 
                           | (0x0000003fU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                  >> 0x0000001cU)) 
                                              - (IData)(1U)) 
                                             >> 4U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                  >> 0x0000001cU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7fbfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 6U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3fffcfffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                          >> 6U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                 >> 0x0000001cU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                            = (0x80000000U | (0x0fffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                            = (0x00000025U | (0xffffffc0U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                    }
                }
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                                = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000010U));
                        }
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x80000000U | (0x0fffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x00000025U | (0xffffffc0U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                } else {
                    if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                            = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000010U));
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000040U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffcfffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00003000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fffcfffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00003000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 6U) & (0U == 
                                               (0x000003ffU 
                                                & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                                      >> 0x0000001cU)))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                                = (0x80000000U | (0x0fffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x00000025U | (0xffffffc0U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7fbfU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3fffcfffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
                    = (0x0fffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                    = (0xffffffc0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
            }
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                              >> 6U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                        = ((0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]) 
                           | (0x0000ffc0U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                << 0x0000001aU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                  >> 6U)) 
                                              - (IData)(1U)) 
                                             << 6U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                               >> 6U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7f7fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 7U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3fff3fffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 7U) & (0U == (0x0000ffc0U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                            = (0x00009600U | (0xffff003fU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                    }
                }
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000018U));
                        }
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x00009600U | (0xffff003fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                } else {
                    if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] 
                            = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000018U));
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000080U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fff3fffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0000c000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fff3fffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0000c000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 7U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                   >> 6U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x00009600U | (0xffff003fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7f7fU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3fff3fffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                    = (0xffff003fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
            }
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                              >> 0x00000010U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                        = ((0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]) 
                           | (0x03ff0000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                << 0x00000010U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                  >> 0x00000010U)) 
                                              - (IData)(1U)) 
                                             << 0x00000010U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                               >> 0x00000010U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7effU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 8U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ffcffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 8U) & (0U == (0x03ff0000U 
                                                   & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                            = (0x02580000U | (0xfc00ffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                    }
                }
                if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                                = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                        }
                    }
                    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x02580000U | (0xfc00ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                } else {
                    if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                            = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w));
                    }
                    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000100U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffcffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00030000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ffcffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00030000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 8U) & (0U == 
                                               (0x000003ffU 
                                                & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                   >> 0x00000010U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x02580000U | (0xfc00ffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7effU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ffcffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                    = (0xfc00ffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
            }
            if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                               << 6U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                 >> 0x0000001aU)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                        = ((0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                 << 6U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                           >> 0x0000001aU)) 
                               - (IData)(1U)) << 0x0000001aU));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                        = ((0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]) 
                           | (0x0000000fU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                << 6U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                  >> 0x0000001aU)) 
                                              - (IData)(1U)) 
                                             >> 6U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                << 6U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                  >> 0x0000001aU))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7dffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 9U)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3ff3ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                          >> 9U) & (0U == (0x000003ffU 
                                           & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                               << 6U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                 >> 0x0000001aU)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                            = (0x60000000U | (0x03ffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                            = (9U | (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                    }
                }
                if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                                = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 8U));
                        }
                    }
                    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000200U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x60000000U | (0x03ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (9U | (0xfffffff0U 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                } else {
                    if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                            = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 8U));
                    }
                    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000200U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ff3ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x000c0000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000200U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3ff3ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x000c0000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 9U) & (0U == 
                                               (0x000003ffU 
                                                & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                    << 6U) 
                                                   | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                                      >> 0x0000001aU)))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                                = (0x60000000U | (0x03ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (9U | (0xfffffff0U 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7dffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3ff3ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
                    = (0x03ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                    = (0xfffffff0U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
            }
            if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                              >> 4U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                        = ((0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]) 
                           | (0x00003ff0U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                << 0x0000001cU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                  >> 4U)) 
                                              - (IData)(1U)) 
                                             << 4U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                               >> 4U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x7bffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 0x0aU)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3fcfffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 0x0000000aU) & 
                                 (0U == (0x00003ff0U 
                                         & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                            = (0x00002580U | (0xffffc00fU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                    }
                }
                if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                                = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000010U));
                        }
                    }
                    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000400U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00002580U | (0xffffc00fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                } else {
                    if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                            = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000010U));
                    }
                    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000400U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fcfffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00300000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000400U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3fcfffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00300000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 0x0aU) & (0U 
                                                  == 
                                                  (0x000003ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                      >> 4U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00002580U | (0xffffc00fU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x7bffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3fcfffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                    = (0xffffc00fU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
            }
            if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                              >> 0x0000000eU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                        = ((0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]) 
                           | (0x00ffc000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                << 0x00000012U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                  >> 0x0000000eU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000eU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                               >> 0x0000000eU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x77ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 0x0bU)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3f3fffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 0x0000000bU) & 
                                 (0U == (0x00ffc000U 
                                         & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                            = (0x00960000U | (0xff003fffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                    }
                }
                if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                      << 0x00000018U));
                        }
                    }
                    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000800U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00960000U | (0xff003fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                } else {
                    if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] 
                            = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                  << 0x00000018U));
                    }
                    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00000800U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3f3fffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00c00000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if ((0x00000800U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3f3fffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x00c00000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 0x0bU) & (0U 
                                                  == 
                                                  (0x000003ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                      >> 0x0000000eU))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00960000U | (0xff003fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x77ffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3f3fffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                    = (0xff003fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
            }
            if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                               << 8U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                 >> 0x00000018U)))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                        = ((0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]) 
                           | ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                 << 8U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                           >> 0x00000018U)) 
                               - (IData)(1U)) << 0x00000018U));
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                        = ((0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]) 
                           | (3U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                       << 8U) | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                 >> 0x00000018U)) 
                                     - (IData)(1U)) 
                                    >> 8U)));
                    if ((1U == (0x000003ffU & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                << 8U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                  >> 0x00000018U))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x6fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 0x0cU)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x3cffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                          >> 0x0cU) & (0U == (0x000003ffU 
                                              & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                  << 8U) 
                                                 | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                    >> 0x00000018U)))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                            = (0x58000000U | (0x00ffffffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                            = (2U | (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                    }
                }
                if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                                = ((0x00ffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                                   | (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w)));
                        }
                    }
                    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00001000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x58000000U | (0x00ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (2U | (0x003ffffcU 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                } else {
                    if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                            = ((0x00ffff00U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                               | (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w)));
                    }
                    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00001000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3cffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x03000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00001000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x3cffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x03000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 0x0cU) & (0U 
                                                  == 
                                                  (0x000003ffU 
                                                   & ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                       << 8U) 
                                                      | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                                         >> 0x00000018U)))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                                = (0x58000000U | (0x00ffffffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (2U | (0x003ffffcU 
                                         & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x6fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x3cffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
                    = (0x00ffffffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U]);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                    = (0x003ffffcU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
            }
            if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                              >> 2U))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                        = ((0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]) 
                           | (0x00000ffcU & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                << 0x0000001eU) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                  >> 2U)) 
                                              - (IData)(1U)) 
                                             << 2U)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                               >> 2U)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x5fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 0x0dU)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x33ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 0x0000000dU) & 
                                 (0U == (0x00000ffcU 
                                         & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                            = (0x00000960U | (0x003ff003U 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                    }
                }
                if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                                = ((0x00ff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                                   | (0x00ffffffU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                       << 8U)));
                        }
                    }
                    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00002000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00000960U | (0x003ff003U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                } else {
                    if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                            = ((0x00ff00ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                               | (0x00ffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                                 << 8U)));
                    }
                    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00002000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x33ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0c000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00002000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x33ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x0c000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 0x0dU) & (0U 
                                                  == 
                                                  (0x000003ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                      >> 2U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00000960U | (0x003ff003U 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x5fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x33ffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                    = (0x003ff003U & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
            }
            if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                     & (0U != (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                              >> 0x0000000cU))))) {
                    __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                        = ((0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]) 
                           | (0x003ff000U & ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                << 0x00000014U) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                  >> 0x0000000cU)) 
                                              - (IData)(1U)) 
                                             << 0x0000000cU)));
                    if ((1U == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                               >> 0x0000000cU)))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                            = (0x3fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                      >> 0x0eU)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = (0x0fffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                  >> 0x0000000eU) & 
                                 (0U == (0x003ff000U 
                                         & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]))))) {
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                            = (0x00258000U | (0x00000fffU 
                                              & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                    }
                }
                if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))) {
                    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w))) {
                        if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                                = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                                   | (0x00ffffffU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                       << 0x00000010U)));
                        }
                    }
                    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w))) {
                        if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00004000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00258000U | (0x00000fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                } else {
                    if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w)))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] 
                            = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U]) 
                               | (0x00ffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w) 
                                                 << 0x00000010U)));
                    }
                    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w))) {
                        if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                                = (0x00004000U | (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x0fffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x30000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if ((0x00004000U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                = ((0x0fffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r) 
                                   | (0x30000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__e_par_w));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
                        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)) 
                                     >> 0x0eU) & (0U 
                                                  == 
                                                  (0x000003ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                                      >> 0x0000000cU))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                                = (0x00258000U | (0x00000fffU 
                                                  & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]));
                        }
                    }
                }
            } else {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
                    = (0x3fffU & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r));
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                    = (0x0fffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r);
                __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
                    = (0x00000fffU & __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U]);
            }
            if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__svc_w) {
                vlSelfRef.milan_datapath__DOT__srp_ctx_gnt_w = 1U;
                if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_we_i) 
                     & (0U != (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i)))) {
                    if (vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_valid_i) {
                        if ((0x03bfU >= (0x000003c0U 
                                         & (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                             - (IData)(1U)) 
                                            << 6U)))) {
                            VL_ASSIGNSEL_WQ(960, 64, 
                                            (0x000003c0U 
                                             & (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                 - (IData)(1U)) 
                                                << 6U)), vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r, 
                                            ((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_gnt_w)
                                              ? vlSelfRef.milan_datapath__DOT__eff_crft_sid_w
                                              : vlSelfRef.milan_datapath__DOT__csr__DOT__srp_wr_sid_r));
                        }
                        if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_dir_i) 
                             & (~ ((0x0eU >= (0x0000000fU 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                 - (IData)(1U)))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                             >> (0x0000000fU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                    - (IData)(1U))))))))) {
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_fastjoin_w = 1U;
                        }
                        if ((0x0eU >= (0x0000000fU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                          - (IData)(1U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w 
                                = (((~ ((IData)(1U) 
                                        << (0x0000000fU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                               - (IData)(1U))))) 
                                    & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w)) 
                                   | (0x7fffU & ((1U 
                                                  & (((0x0eU 
                                                       >= 
                                                       (0x0000000fU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                           - (IData)(1U)))) 
                                                      && (1U 
                                                          & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w) 
                                                             >> 
                                                             (0x0000000fU 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                                 - (IData)(1U)))))) 
                                                     | (~ 
                                                        ((0x0eU 
                                                          >= 
                                                          (0x0000000fU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                              - (IData)(1U)))) 
                                                         && (1U 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                                >> 
                                                                (0x0000000fU 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                                    - (IData)(1U))))))))) 
                                                 << 
                                                 (0x0000000fU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                     - (IData)(1U))))));
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w 
                                = ((~ ((IData)(1U) 
                                       << (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                              - (IData)(1U))))) 
                                   & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r 
                                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                   | (0x7fffU & ((IData)(1U) 
                                                 << 
                                                 (0x0000000fU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                     - (IData)(1U))))));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r 
                                = (((~ ((IData)(1U) 
                                        << (0x0000000fU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                               - (IData)(1U))))) 
                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r)) 
                                   | (0x7fffU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_dir_i) 
                                                 << 
                                                 (0x0000000fU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                     - (IData)(1U))))));
                        }
                        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 1U;
                    } else {
                        if (((0x0eU >= (0x0000000fU 
                                        & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                           - (IData)(1U)))) 
                             && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r) 
                                       >> (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                              - (IData)(1U))))))) {
                            if ((0x0eU >= (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                              - (IData)(1U))))) {
                                __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w 
                                    = ((IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
                                       | (0x7fffU & 
                                          ((IData)(1U) 
                                           << (0x0000000fU 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                  - (IData)(1U))))));
                            }
                        }
                        if ((0x0eU >= (0x0000000fU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                          - (IData)(1U))))) {
                            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w 
                                = ((~ ((IData)(1U) 
                                       << (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                              - (IData)(1U))))) 
                                   & (IData)(__Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w));
                            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r 
                                = ((~ ((IData)(1U) 
                                       << (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                              - (IData)(1U))))) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r));
                        }
                    }
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_p) 
                 & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt)) 
                    | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt)) 
                       | (3U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt)))))) {
                __Vdly__milan_datapath__DOT__lwsrp_listener_reg = 1U;
                vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_decl;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0U;
            } else if ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_p) 
                         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg))) {
                vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_decl;
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0U;
            } else if ((((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_p) 
                           & (5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt))) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p)) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg)) 
                        & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0x0258U;
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w) 
                        & (0U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r)))) {
                __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r 
                    = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r) 
                                      - (IData)(1U)));
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r))) {
                    __Vdly__milan_datapath__DOT__lwsrp_listener_reg = 0U;
                    vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl = 0U;
                }
            }
        } else {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp_listener_reg = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w = 0U;
            __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r = 0U;
        }
        if (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r)))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w = 0U;
        }
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w = 0U;
        if ((0x0001869fU == vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r)) {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w = 1U;
        } else {
            __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r));
        }
    } else {
        vlSelfRef.milan_datapath__DOT__acmp_rest_status_w = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_rest_ack_w = 0U;
        vlSelfRef.milan_datapath__DOT__srp_ctx_gnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_discover_p = 0U;
        VL_ASSIGN_W(317, vlSelfRef.milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o, Vmilan_datapath__ConstPool__CONST_h8a04c6be_0);
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q2_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__iv_bytes_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_srp_last_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_srp_dmac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__crf_srp_sid_r = 0ULL;
        VL_ASSIGN_W(960, vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r, Vmilan_datapath__ConstPool__CONST_h99b8ac36_0);
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxk_r = 0U;
        __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r[3U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp_listener_reg = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxk_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rxd_r = 0ULL;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_fastjoin_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__ready_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__kill_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__pushing_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__drop_rest_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__dst_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__subtype_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__msgtype_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__is_avtp_r = 0U;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__tgt_hi_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__frame_bytes_r = 0U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__join_tick_w = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_count_o = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r = 0ULL;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nt_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nl_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_len_r = 0x003cU;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx_done_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w = 0U;
        __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tick_1khz_w = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r = 0U;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[__VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v0;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_intv_r__v1) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_intv_r[14U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w 
        = (VL_LTS_III(30, 0x007fffffU, __VdfgRegularize_h6e95ff9d_0_23)
            ? 0x007fffffU : (VL_GTS_III(30, 0x3f800000U, __VdfgRegularize_h6e95ff9d_0_23)
                              ? 0x00800000U : (0x00ffffffU 
                                               & __VdfgRegularize_h6e95ff9d_0_23)));
    if (__VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r[__VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0] 
            = __VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                    | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r)))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_cap_hs 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
            | (1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r 
        = __Vdly__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r;
    vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg 
        = __Vdly__milan_datapath__DOT__lwsrp_listener_reg;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U] 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[0U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U] 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[1U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U] 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[2U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U] 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[3U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U] 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r[4U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full_w));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w 
        = (0x000001ffffffffffULL & VL_MULS_QQQ(41, 
                                               (0x000001ffffffffffULL 
                                                & VL_EXTENDS_QI(41,17, Vmilan_datapath__ConstPool__TABLE_h441640be_0
                                                                [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r])), 
                                               (0x000001ffffffffffULL 
                                                & VL_EXTENDS_QI(41,24, 
                                                                ((0U 
                                                                  == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                  ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r
                                                                  : 
                                                                 ((1U 
                                                                   == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                   ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r
                                                                   : 
                                                                  ((2U 
                                                                    == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                    ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r
                                                                    : 
                                                                   ((3U 
                                                                     == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                     ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r
                                                                     : 
                                                                    ((4U 
                                                                      == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                      ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r
                                                                      : 
                                                                     ((5U 
                                                                       == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                       ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r
                                                                       : 
                                                                      ((6U 
                                                                        == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                        ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r
                                                                        : 
                                                                       ((7U 
                                                                         == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                         ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r
                                                                         : 
                                                                        ((8U 
                                                                          == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                          ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r
                                                                          : vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r)))))))))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxl_r) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg) 
           & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)) 
              | (3U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r;
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[__VdlyDim0__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0] 
            = __VdlyVal__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v0;
    }
    if (__VdlySet__milan_datapath__DOT__lwsrp__DOT__gate_maxf_r__v1) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[14U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run 
        = ((~ ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
               | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_fresh_w 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__row_fresh_w;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__row_lv_w;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_end_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r) 
           == (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_len_r) 
                              - (IData)(1U))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_end_w 
        = ((8U != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r) 
              == (0x0000001fU & ((IData)(Vmilan_datapath__ConstPool__TABLE_h91c136a7_0
                                         [vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r]) 
                                 - (IData)(1U)))));
    __Vtableidx3 = ((((((5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r)) 
                        << 3U) | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r)) 
                                  << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tlast) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tready))) 
                     << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid) 
                                << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
                                           << 1U) | (IData)(vlSelfRef.axis_resetn))));
    if ((1U & Vmilan_datapath__ConstPool__TABLE_h3d59c2d6_0
         [__Vtableidx3])) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r 
            = Vmilan_datapath__ConstPool__TABLE_hbb7d8a2c_0
            [__Vtableidx3];
    }
    if ((2U & Vmilan_datapath__ConstPool__TABLE_h3d59c2d6_0
         [__Vtableidx3])) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r 
            = Vmilan_datapath__ConstPool__TABLE_hec53cc74_0
            [__Vtableidx3];
    }
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r 
        = __Vdly__milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r;
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41 = (1U 
                                                 & ((0x00000080U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 7U)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 7U) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x0000000eU))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x0000000eU)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42 = (1U 
                                                 & ((0x00000100U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 8U)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 8U) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x00000010U))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x00000010U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43 = (1U 
                                                 & ((0x00000200U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 9U)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 9U) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x00000012U))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x00000012U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44 = (1U 
                                                 & ((0x00000400U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 0x0000000aU)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 0x0000000aU) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x00000014U))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x00000014U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45 = (1U 
                                                 & ((0x00000800U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 0x0000000bU)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 0x0000000bU) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x00000016U))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x00000016U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46 = (1U 
                                                 & ((0x00001000U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 0x0000000cU)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 0x0000000cU) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x00000018U))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x00000018U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47 = (1U 
                                                 & ((0x00002000U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 0x0000000dU)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 0x0000000dU) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x0000001aU))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x0000001aU)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48 = (1U 
                                                 & ((0x00004000U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 0x0000000eU)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 0x0000000eU) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x0000001cU))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x0000001cU)))))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
              == (0x0000000fU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w)
                                   ? 0x0bU : 8U) - (IData)(1U)))));
    vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)
               ? (5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r))
               : (1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
                << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47) 
                          << 2U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46) 
                                      << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45))) 
             << 0x0000000bU) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44) 
                                   << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43) 
                                             << 2U)) 
                                 | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42) 
                                     << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41))) 
                                << 7U)) | (((((2U & 
                                               (((0x00000040U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                  ? 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                  >> 6U)
                                                  : 
                                                 (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                   >> 6U) 
                                                  & ((2U 
                                                      == 
                                                      (3U 
                                                       & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                          >> 0x0000000cU))) 
                                                     | (3U 
                                                        == 
                                                        (3U 
                                                         & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                            >> 0x0000000cU)))))) 
                                                << 1U)) 
                                              | (1U 
                                                 & ((0x00000020U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 5U)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 5U) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x0000000aU))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x0000000aU)))))))) 
                                             << 5U) 
                                            | (((2U 
                                                 & (((0x00000010U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                      ? 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 4U)
                                                      : 
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 4U) 
                                                      & ((2U 
                                                          == 
                                                          (3U 
                                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                              >> 8U))) 
                                                         | (3U 
                                                            == 
                                                            (3U 
                                                             & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                >> 8U)))))) 
                                                    << 1U)) 
                                                | (1U 
                                                   & ((8U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                       ? 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 3U)
                                                       : 
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        >> 3U) 
                                                       & ((2U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 6U))) 
                                                          | (3U 
                                                             == 
                                                             (3U 
                                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                 >> 6U)))))))) 
                                               << 3U)) 
                                           | ((4U & 
                                               (((4U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                  ? 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                  >> 2U)
                                                  : 
                                                 (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                   >> 2U) 
                                                  & ((2U 
                                                      == 
                                                      (3U 
                                                       & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                          >> 4U))) 
                                                     | (3U 
                                                        == 
                                                        (3U 
                                                         & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                            >> 4U)))))) 
                                                << 2U)) 
                                              | ((2U 
                                                  & (((2U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                       ? 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 1U)
                                                       : 
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        >> 1U) 
                                                       & ((2U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 2U))) 
                                                          | (3U 
                                                             == 
                                                             (3U 
                                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                 >> 2U)))))) 
                                                     << 1U)) 
                                                 | (1U 
                                                    & ((1U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                        ? (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)
                                                        : 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        & ((2U 
                                                            == 
                                                            (3U 
                                                             & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r)) 
                                                           | (3U 
                                                              == 
                                                              (3U 
                                                               & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r))))))))));
    vlSelfRef.milan_datapath__DOT__lwsrp_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)
             ? ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r) 
                & (5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r)))
             : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w)));
}
