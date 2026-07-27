// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_ptp_clock_validity.h for the primary calling header

#include "VKL_ptp_clock_validity__pch.h"

VL_ATTR_COLD void VKL_ptp_clock_validity___024root___eval_static(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_static\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk_i__0 = vlSelfRef.clk_i;
}

VL_ATTR_COLD void VKL_ptp_clock_validity___024root___eval_initial(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_initial\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void VKL_ptp_clock_validity___024root___eval_final(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_final\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_ptp_clock_validity___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VKL_ptp_clock_validity___024root___eval_phase__stl(VKL_ptp_clock_validity___024root* vlSelf);

VL_ATTR_COLD void VKL_ptp_clock_validity___024root___eval_settle(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_settle\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            VKL_ptp_clock_validity___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv", 98, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = VKL_ptp_clock_validity___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool VKL_ptp_clock_validity___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_ptp_clock_validity___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(VKL_ptp_clock_validity___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool VKL_ptp_clock_validity___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD bool VKL_ptp_clock_validity___024root___eval_phase__stl(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_phase__stl\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        VKL_ptp_clock_validity___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = VKL_ptp_clock_validity___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                {
                    // Inlined CFunc: _stl_sequent__TOP__0
                    vlSelfRef.tu_ivals_o = vlSelfRef.KL_ptp_clock_validity__DOT__tu_ivals_r;
                    vlSelfRef.ts_uncertain_o = (1U 
                                                & (~ 
                                                   ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r) 
                                                    & (0U 
                                                       == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r)))));
                    vlSelfRef.stat_o = (((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__lease_r) 
                                         << 4U) | (
                                                   (((0U 
                                                      != (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r)) 
                                                     << 3U) 
                                                    | ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__no_lease_r) 
                                                       << 2U)) 
                                                   | (((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r) 
                                                       << 1U) 
                                                      | (IData)(vlSelfRef.ts_uncertain_o))));
                }
            }
        }
    }
    return (__VstlExecute);
}

bool VKL_ptp_clock_validity___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void VKL_ptp_clock_validity___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(VKL_ptp_clock_validity___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk_i)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VKL_ptp_clock_validity___024root___ctor_var_reset(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___ctor_var_reset\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11908517815223722933ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->sw_wr_p_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3680840686689752600ull);
    vlSelf->sw_sync_ok_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7394878747239620656ull);
    vlSelf->sw_disc_p_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11409691452214315427ull);
    vlSelf->sw_wdog_q_i = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 17442190145774352044ull);
    vlSelf->phc_load_p_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12268614082032072921ull);
    vlSelf->phc_adj_p_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7843756250333684219ull);
    vlSelf->gm_id_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2671297330762035917ull);
    vlSelf->ts_uncertain_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2326070746865574844ull);
    vlSelf->stat_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1729998714009813624ull);
    vlSelf->tu_ivals_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9692184705830658211ull);
    vlSelf->KL_ptp_clock_validity__DOT__qdiv_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16783170439912505277ull);
    vlSelf->KL_ptp_clock_validity__DOT__sync_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2226307336570383175ull);
    vlSelf->KL_ptp_clock_validity__DOT__lease_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 11075128441102064905ull);
    vlSelf->KL_ptp_clock_validity__DOT__no_lease_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8238104748871253732ull);
    vlSelf->KL_ptp_clock_validity__DOT__gm_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2628638661778447420ull);
    vlSelf->KL_ptp_clock_validity__DOT__hold_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15359790677853308226ull);
    vlSelf->KL_ptp_clock_validity__DOT__ival_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6589493104113705892ull);
    vlSelf->KL_ptp_clock_validity__DOT__tu_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6990214613419801647ull);
    vlSelf->KL_ptp_clock_validity__DOT__tu_ivals_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11165548501780168562ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk_i__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
