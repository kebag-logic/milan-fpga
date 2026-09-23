// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmedia_grid_align_wrap.h for the primary calling header

#include "Vmedia_grid_align_wrap__pch.h"

bool Vmedia_grid_align_wrap___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___trigger_anySet__ico\n"); );
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
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vmedia_grid_align_wrap___024root___eval_phase__ico(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_phase__ico\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__ico
        vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                        (((((IData)(vlSelfRef.frame_ev_i) 
                                                            != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__frame_ev_i__0)) 
                                                           << 3U) 
                                                          | (((IData)(vlSelfRef.sel_i) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__sel_i__0)) 
                                                             << 2U)) 
                                                         | ((((IData)(vlSelfRef.rst_n) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0)) 
                                                             << 1U) 
                                                            | ((IData)(vlSelfRef.clk) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))))));
        vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
        vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
        vlSelfRef.__Vtrigprevexpr___TOP__sel_i__0 = vlSelfRef.sel_i;
        vlSelfRef.__Vtrigprevexpr___TOP__frame_ev_i__0 
            = vlSelfRef.frame_ev_i;
        if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VicoDidInit)))))) {
            vlSelfRef.__VicoDidInit = 1U;
            vlSelfRef.__VicoTriggered[0U] = (1ULL | vlSelfRef.__VicoTriggered[0U]);
            vlSelfRef.__VicoTriggered[0U] = (2ULL | vlSelfRef.__VicoTriggered[0U]);
            vlSelfRef.__VicoTriggered[0U] = (4ULL | vlSelfRef.__VicoTriggered[0U]);
            vlSelfRef.__VicoTriggered[0U] = (8ULL | vlSelfRef.__VicoTriggered[0U]);
        }
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmedia_grid_align_wrap___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vmedia_grid_align_wrap___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        {
            // Inlined CFunc: _eval_ico
            if ((8ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_sequent__TOP__0
                    vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_pair_valid_i 
                        = vlSelfRef.frame_ev_i;
                }
            }
            if ((4ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_sequent__TOP__1
                    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w 
                        = ((- VL_SHIFTRS_III(32,32,32, 
                                             VL_MULS_III(32, (IData)(0x00000064U), 
                                                         VL_EXTENDS_II(32,16, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_w))), 4U)) 
                           & (- (IData)((IData)(vlSelfRef.sel_i))));
                }
            }
        }
    }
    return (__VicoExecute);
}

bool Vmedia_grid_align_wrap___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___trigger_anySet__act\n"); );
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

void Vmedia_grid_align_wrap___024root___nba_sequent__TOP__0(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___nba_sequent__TOP__0\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ media_grid_align_wrap__DOT__u_align__DOT__base_w;
    media_grid_align_wrap__DOT__u_align__DOT__base_w = 0;
    IData/*31:0*/ media_grid_align_wrap__DOT__u_align__DOT__diff_w;
    media_grid_align_wrap__DOT__u_align__DOT__diff_w = 0;
    IData/*31:0*/ __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__Vfuncout;
    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v;
    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v = 0;
    SData/*15:0*/ __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__Vfuncout;
    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v;
    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v = 0;
    SData/*11:0*/ __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r;
    __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r = 0;
    SData/*13:0*/ __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r = 0;
    CData/*4:0*/ __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r = 0;
    IData/*31:0*/ __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r = 0;
    SData/*15:0*/ __Vdly__media_grid_align_wrap__DOT__u_w;
    __Vdly__media_grid_align_wrap__DOT__u_w = 0;
    CData/*0:0*/ __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v0;
    __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v1;
    __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v1 = 0;
    // Body
    __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v0 = 0U;
    __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v1 = 0U;
    __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r 
        = vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__cnt_r;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r 
        = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r 
        = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__acc_r;
    __Vdly__media_grid_align_wrap__DOT__u_w = vlSelfRef.media_grid_align_wrap__DOT__u_w;
    __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r 
        = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r;
    if (vlSelfRef.rst_n) {
        if (vlSelfRef.frame_ev_i) {
            __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v0 = 1U;
        }
        if ((2U == (((IData)(vlSelfRef.frame_ev_i) 
                     << 1U) | (IData)(vlSelfRef.tick_o)))) {
            if (((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r) 
                 & (0xffffU != (IData)(vlSelfRef.tdm_skip_cnt_o)))) {
                vlSelfRef.tdm_skip_cnt_o = (0x0000ffffU 
                                            & ((IData)(1U) 
                                               + (IData)(vlSelfRef.tdm_skip_cnt_o)));
            }
            vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r = 1U;
            vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r = 1U;
        } else {
            if ((1U == (((IData)(vlSelfRef.frame_ev_i) 
                         << 1U) | (IData)(vlSelfRef.tick_o)))) {
                if ((((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r) 
                      & (~ (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r))) 
                     & (0xffffU != (IData)(vlSelfRef.tdm_dup_cnt_o)))) {
                    vlSelfRef.tdm_dup_cnt_o = (0x0000ffffU 
                                               & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tdm_dup_cnt_o)));
                }
                vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r = 0U;
            } else if ((3U == (((IData)(vlSelfRef.frame_ev_i) 
                                << 1U) | (IData)(vlSelfRef.tick_o)))) {
                vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r = 0U;
            }
            if ((1U != (((IData)(vlSelfRef.frame_ev_i) 
                         << 1U) | (IData)(vlSelfRef.tick_o)))) {
                if ((3U == (((IData)(vlSelfRef.frame_ev_i) 
                             << 1U) | (IData)(vlSelfRef.tick_o)))) {
                    vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r = 1U;
                }
            }
        }
        vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_r 
            = (VL_LTS_III(32, 0x00007d00U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w)
                ? 0x00007d00U : (VL_GTS_III(32, 0xffff8300U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w)
                                  ? 0x00038300U : (0x0003ffffU 
                                                   & vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w)));
        if (vlSelfRef.sel_i) {
            if ((1U & ((~ (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r)) 
                       | (0x208cU <= (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r))))) {
                __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.frame_ev_i)
                        ? 0U : (0x00003fffU & ((0x208cU 
                                                <= (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r))
                                                ? (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r)
                                                : ((IData)(1U) 
                                                   + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r)))));
                if (vlSelfRef.frame_ev_i) {
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__ref_r 
                        = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w;
                }
                vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r 
                    = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w;
                __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r = 0U;
                vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r 
                    = vlSelfRef.frame_ev_i;
                vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r = 0U;
                __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r = 0U;
                __Vdly__media_grid_align_wrap__DOT__u_w = 0U;
            } else {
                __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.frame_ev_i)
                        ? 0U : (0x00003fffU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r))));
                if (vlSelfRef.frame_ev_i) {
                    if (vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w) {
                        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r 
                            = (0x0000001fU & ((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r) 
                                              - (IData)(1U)));
                    } else if (vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_up_w) {
                        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r)));
                    }
                    if ((1U & (~ (((0xf380U == (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_w)) 
                                   & VL_LTS_III(32, 0U, vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w)) 
                                  | ((0x0c80U == (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_w)) 
                                     & VL_GTS_III(32, 0U, vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w)))))) {
                        __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v 
                            = (vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__acc_r 
                               + vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w);
                        __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__Vfuncout 
                            = (VL_LTS_III(32, 0x00c80000U, __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v)
                                ? 0x00c80000U : (VL_GTS_III(32, 0xff380000U, __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v)
                                                  ? 0xff380000U
                                                  : __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__v));
                        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r 
                            = __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_acc__6__Vfuncout;
                    }
                    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v 
                        = (VL_MULS_III(32, (IData)(0xffffffffU), 
                                       (vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w 
                                        << 2U)) - VL_SHIFTRS_III(32,32,32, vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__acc_r, 0x0000000cU));
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r 
                        = (0x0000ffffU & vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w);
                    __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__Vfuncout 
                        = (VL_LTS_III(32, 0x00000c80U, __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v)
                            ? 0x00000c80U : (VL_GTS_III(32, 0xfffff380U, __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v)
                                              ? 0x0000f380U
                                              : (0x0000ffffU 
                                                 & __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__v)));
                    __Vdly__media_grid_align_wrap__DOT__u_w 
                        = __Vfunc_media_grid_align_wrap__DOT__u_align__DOT__clamp_u__7__Vfuncout;
                }
                vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r 
                    = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w;
            }
        } else {
            __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r = 0U;
            vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r 
                = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w;
            __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r = 0U;
            vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r = 0U;
            vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r = 0U;
            __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r = 0U;
            __Vdly__media_grid_align_wrap__DOT__u_w = 0U;
        }
        if (((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__cnt_r) 
             == ((VL_LTES_III(18, 0x0000bb80U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w)
                   ? 0x00000823U : 0x00000822U) - (1U 
                                                   & (- (IData)(
                                                                VL_GTS_III(18, 0U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w))))))) {
            __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r = 0U;
            vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r 
                = (0x0000ffffU & (VL_LTES_III(18, 0x0000bb80U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w)
                                   ? (vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w 
                                      - (IData)(0xbb80U))
                                   : (VL_GTS_III(18, 0U, vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w)
                                       ? ((IData)(0xbb80U) 
                                          + vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w)
                                       : vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w)));
            vlSelfRef.tick_o = 1U;
        } else {
            __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r 
                = (0x00000fffU & ((IData)(1U) + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__cnt_r)));
            vlSelfRef.tick_o = 0U;
        }
    } else {
        __VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v1 = 1U;
        vlSelfRef.tdm_dup_cnt_o = 0U;
        vlSelfRef.tdm_skip_cnt_o = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_r = 0U;
        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__ref_r = 0U;
        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r = 0U;
        __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r = 0U;
        __Vdly__media_grid_align_wrap__DOT__u_w = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r = 0U;
        __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r = 0U;
        vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r = 0U;
        vlSelfRef.tick_o = 0U;
    }
    if (__VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v0) {
        vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r[0U] = 0ULL;
    }
    if (__VdlySet__media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r__v1) {
        vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r[0U] = 0ULL;
    }
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__quiet_r 
        = __Vdly__media_grid_align_wrap__DOT__u_align__DOT__quiet_r;
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__acc_r 
        = __Vdly__media_grid_align_wrap__DOT__u_align__DOT__acc_r;
    vlSelfRef.media_grid_align_wrap__DOT__u_w = __Vdly__media_grid_align_wrap__DOT__u_w;
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r 
        = __Vdly__media_grid_align_wrap__DOT__u_align__DOT__slip_r;
    vlSelfRef.engaged_o = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r;
    vlSelfRef.u_o = vlSelfRef.media_grid_align_wrap__DOT__u_w;
    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w 
        = ((- VL_SHIFTRS_III(32,32,32, VL_MULS_III(32, (IData)(0x00000064U), 
                                                   VL_EXTENDS_II(32,16, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_w))), 4U)) 
           & (- (IData)((IData)(vlSelfRef.sel_i))));
    vlSelfRef.err_cyc_o = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r;
    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__cnt_r 
        = __Vdly__media_grid_align_wrap__DOT__u_nco__DOT__cnt_r;
    vlSelfRef.phase_o = vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r;
    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w 
        = (0x0003ffffU & ((IData)(0x00003e80U) + (vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_r 
                                                  + 
                                                  VL_EXTENDS_II(18,17, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r)))));
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w 
        = (0x00001fffU & (((0x1045U == (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r))
                            ? (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r)
                            : ((IData)(1U) + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r))) 
                          & (- (IData)((1U & (~ (IData)(vlSelfRef.tick_o)))))));
    media_grid_align_wrap__DOT__u_align__DOT__base_w 
        = ((VL_EXTENDS_II(32,14, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w)) 
            - VL_EXTENDS_II(32,14, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__ref_r))) 
           + VL_MULS_III(32, (IData)(0x00000823U), 
                         VL_EXTENDS_II(32,5, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r))));
    media_grid_align_wrap__DOT__u_align__DOT__diff_w 
        = (media_grid_align_wrap__DOT__u_align__DOT__base_w 
           - VL_EXTENDS_II(32,16, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r)));
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w 
        = (VL_LTS_III(32, 0x00000411U, media_grid_align_wrap__DOT__u_align__DOT__diff_w) 
           & VL_LTS_III(5, 0x18U, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r)));
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_up_w 
        = (VL_GTS_III(32, 0xfffffbefU, media_grid_align_wrap__DOT__u_align__DOT__diff_w) 
           & VL_GTS_III(5, 8U, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r)));
    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w 
        = ((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w)
            ? (media_grid_align_wrap__DOT__u_align__DOT__base_w 
               - (IData)(0x00000823U)) : ((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_up_w)
                                           ? ((IData)(0x00000823U) 
                                              + media_grid_align_wrap__DOT__u_align__DOT__base_w)
                                           : media_grid_align_wrap__DOT__u_align__DOT__base_w));
}

void Vmedia_grid_align_wrap___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vmedia_grid_align_wrap___024root___eval_phase__act(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_phase__act\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((IData)(vlSelfRef.clk) 
                                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__1)))));
        vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmedia_grid_align_wrap___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vmedia_grid_align_wrap___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vmedia_grid_align_wrap___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vmedia_grid_align_wrap___024root___eval_phase__nba(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_phase__nba\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vmedia_grid_align_wrap___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vmedia_grid_align_wrap___024root___nba_sequent__TOP__0(vlSelf);
            }
        }
        Vmedia_grid_align_wrap___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vmedia_grid_align_wrap___024root___eval(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vmedia_grid_align_wrap___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("media_grid_align_wrap.sv", 15, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vmedia_grid_align_wrap___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vmedia_grid_align_wrap___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("media_grid_align_wrap.sv", 15, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vmedia_grid_align_wrap___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("media_grid_align_wrap.sv", 15, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vmedia_grid_align_wrap___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vmedia_grid_align_wrap___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vmedia_grid_align_wrap___024root___eval_debug_assertions(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_debug_assertions\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.sel_i & 0xfeU)))) {
        Verilated::overWidthError("sel_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.frame_ev_i & 0xfeU)))) {
        Verilated::overWidthError("frame_ev_i");
    }
}
#endif  // VL_DEBUG
