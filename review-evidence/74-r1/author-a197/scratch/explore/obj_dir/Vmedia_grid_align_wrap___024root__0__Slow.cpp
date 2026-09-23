// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmedia_grid_align_wrap.h for the primary calling header

#include "Vmedia_grid_align_wrap__pch.h"

VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___eval_static(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_static\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__sel_i__0 = vlSelfRef.sel_i;
    vlSelfRef.__Vtrigprevexpr___TOP__frame_ev_i__0 
        = vlSelfRef.frame_ev_i;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
}

VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___eval_initial(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_initial\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___eval_final(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_final\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vmedia_grid_align_wrap___024root___eval_phase__stl(Vmedia_grid_align_wrap___024root* vlSelf);

VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___eval_settle(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_settle\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vmedia_grid_align_wrap___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("media_grid_align_wrap.sv", 13, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vmedia_grid_align_wrap___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vmedia_grid_align_wrap___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vmedia_grid_align_wrap___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vmedia_grid_align_wrap___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD bool Vmedia_grid_align_wrap___024root___eval_phase__stl(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___eval_phase__stl\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vmedia_grid_align_wrap___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vmedia_grid_align_wrap___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                {
                    // Inlined CFunc: _stl_sequent__TOP__0
                    IData/*31:0*/ __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w;
                    __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w = 0;
                    IData/*31:0*/ __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__diff_w;
                    __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__diff_w = 0;
                    vlSelfRef.u_o = vlSelfRef.media_grid_align_wrap__DOT__u_w;
                    vlSelfRef.media_grid_align_wrap__DOT__u_junction__DOT__tdm_pair_valid_i 
                        = vlSelfRef.frame_ev_i;
                    vlSelfRef.err_cyc_o = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r;
                    vlSelfRef.engaged_o = vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__engaged_r;
                    vlSelfRef.phase_o = vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r;
                    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w 
                        = ((- VL_SHIFTRS_III(32,32,32, 
                                             VL_MULS_III(32, (IData)(0x00000064U), 
                                                         VL_EXTENDS_II(32,16, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_w))), 4U)) 
                           & (- (IData)((IData)(vlSelfRef.sel_i))));
                    vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__sum_w 
                        = (0x0003ffffU & ((IData)(0x00003e80U) 
                                          + (vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__trim_r 
                                             + VL_EXTENDS_II(18,17, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_nco__DOT__frac_r)))));
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w 
                        = (0x00001fffU & (((0x1045U 
                                            == (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r))
                                            ? (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r)
                                            : ((IData)(1U) 
                                               + (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_r))) 
                                          & (- (IData)(
                                                       (1U 
                                                        & (~ (IData)(vlSelfRef.tick_o)))))));
                    __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w 
                        = ((VL_EXTENDS_II(32,14, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__tst_next_w)) 
                            - VL_EXTENDS_II(32,14, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__ref_r))) 
                           + VL_MULS_III(32, (IData)(0x00000823U), 
                                         VL_EXTENDS_II(32,5, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r))));
                    __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__diff_w 
                        = (__Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w 
                           - VL_EXTENDS_II(32,16, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_r)));
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w 
                        = (VL_LTS_III(32, 0x00000411U, __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__diff_w) 
                           & VL_LTS_III(5, 0x18U, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r)));
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_up_w 
                        = (VL_GTS_III(32, 0xfffffbefU, __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__diff_w) 
                           & VL_GTS_III(5, 8U, (IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__slip_r)));
                    vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__err_w 
                        = ((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w)
                            ? (__Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w 
                               - (IData)(0x00000823U))
                            : ((IData)(vlSelfRef.media_grid_align_wrap__DOT__u_align__DOT__fold_up_w)
                                ? ((IData)(0x00000823U) 
                                   + __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w)
                                : __Vinline_0__eval_stl___Vinline_0__stl_sequent__TOP__0_media_grid_align_wrap__DOT__u_align__DOT__base_w));
                }
            }
        }
    }
    return (__VstlExecute);
}

bool Vmedia_grid_align_wrap___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vmedia_grid_align_wrap___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( sel_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( frame_ev_i)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vmedia_grid_align_wrap___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vmedia_grid_align_wrap___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmedia_grid_align_wrap___024root___ctor_var_reset(Vmedia_grid_align_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmedia_grid_align_wrap___024root___ctor_var_reset\n"); );
    Vmedia_grid_align_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->sel_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11903990011214037275ull);
    vlSelf->frame_ev_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14543946671972106668ull);
    vlSelf->tick_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14315340593729067097ull);
    vlSelf->u_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7051498633859270746ull);
    vlSelf->engaged_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11426162202965069449ull);
    vlSelf->err_cyc_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2395410343513130833ull);
    vlSelf->phase_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8497504459728193158ull);
    vlSelf->tdm_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 137734022982063467ull);
    vlSelf->tdm_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17055591806186248809ull);
    vlSelf->media_grid_align_wrap__DOT__u_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4963353638063800258ull);
    vlSelf->media_grid_align_wrap__DOT__u_junction__DOT__tdm_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4226044559576398516ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15725317665206148579ull);
    }
    vlSelf->media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2009374532527140347ull);
    vlSelf->media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12216136003343098940ull);
    vlSelf->media_grid_align_wrap__DOT__u_nco__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3266986486336485828ull);
    vlSelf->media_grid_align_wrap__DOT__u_nco__DOT__frac_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2342492415264900870ull);
    vlSelf->media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17173725969762752870ull);
    vlSelf->media_grid_align_wrap__DOT__u_nco__DOT__trim_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 2483131991476819731ull);
    vlSelf->media_grid_align_wrap__DOT__u_nco__DOT__sum_w = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 4387899439449491381ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__tst_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 17972168417588695781ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__ref_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 5079879351148692001ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__slip_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12371573299980098667ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__quiet_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 310686999609389542ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__engaged_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 727048501107375698ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__tst_next_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 6962553336512275197ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__err_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2487865073629395970ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 908468245796543501ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9484351483905071963ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__fold_up_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1586596040632687611ull);
    vlSelf->media_grid_align_wrap__DOT__u_align__DOT__err_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13160665319059153585ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__sel_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__frame_ev_i__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
