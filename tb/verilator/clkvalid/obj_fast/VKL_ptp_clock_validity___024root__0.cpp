// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_ptp_clock_validity.h for the primary calling header

#include "VKL_ptp_clock_validity__pch.h"

bool VKL_ptp_clock_validity___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___trigger_anySet__act\n"); );
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

void VKL_ptp_clock_validity___024root___nba_sequent__TOP__0(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___nba_sequent__TOP__0\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ __Vdly__KL_ptp_clock_validity__DOT__qdiv_r;
    __Vdly__KL_ptp_clock_validity__DOT__qdiv_r = 0;
    SData/*11:0*/ __Vdly__KL_ptp_clock_validity__DOT__lease_r;
    __Vdly__KL_ptp_clock_validity__DOT__lease_r = 0;
    CData/*1:0*/ __Vdly__KL_ptp_clock_validity__DOT__hold_r;
    __Vdly__KL_ptp_clock_validity__DOT__hold_r = 0;
    CData/*0:0*/ __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r;
    __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r = 0;
    CData/*1:0*/ __Vdly__KL_ptp_clock_validity__DOT__ival_r;
    __Vdly__KL_ptp_clock_validity__DOT__ival_r = 0;
    // Body
    __Vdly__KL_ptp_clock_validity__DOT__qdiv_r = vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r;
    __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r = vlSelfRef.KL_ptp_clock_validity__DOT__tu_seen_r;
    __Vdly__KL_ptp_clock_validity__DOT__ival_r = vlSelfRef.KL_ptp_clock_validity__DOT__ival_r;
    __Vdly__KL_ptp_clock_validity__DOT__lease_r = vlSelfRef.KL_ptp_clock_validity__DOT__lease_r;
    __Vdly__KL_ptp_clock_validity__DOT__hold_r = vlSelfRef.KL_ptp_clock_validity__DOT__hold_r;
    if (vlSelfRef.rst_n) {
        if (vlSelfRef.ts_uncertain_o) {
            __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r = 1U;
        }
        if ((7U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r))) {
            __Vdly__KL_ptp_clock_validity__DOT__qdiv_r = 0U;
            __Vdly__KL_ptp_clock_validity__DOT__ival_r 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__ival_r)));
            if ((3U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__ival_r))) {
                if (((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__tu_seen_r) 
                     | (IData)(vlSelfRef.ts_uncertain_o))) {
                    vlSelfRef.KL_ptp_clock_validity__DOT__tu_ivals_r 
                        = ((IData)(1U) + vlSelfRef.KL_ptp_clock_validity__DOT__tu_ivals_r);
                }
                __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r = 0U;
            }
        } else {
            __Vdly__KL_ptp_clock_validity__DOT__qdiv_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r)));
        }
        if (((IData)(vlSelfRef.phc_load_p_i) | ((IData)(vlSelfRef.phc_adj_p_i) 
                                                | ((IData)(vlSelfRef.sw_disc_p_i) 
                                                   | (vlSelfRef.gm_id_i 
                                                      != vlSelfRef.KL_ptp_clock_validity__DOT__gm_r))))) {
            __Vdly__KL_ptp_clock_validity__DOT__hold_r = 2U;
        } else if (((7U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r)) 
                    & (0U != (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r)))) {
            __Vdly__KL_ptp_clock_validity__DOT__hold_r 
                = (3U & ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r) 
                         - (IData)(1U)));
        }
        if (vlSelfRef.sw_wr_p_i) {
            vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r 
                = ((IData)(vlSelfRef.sw_sync_ok_i) 
                   & (0U != (IData)(vlSelfRef.sw_wdog_q_i)));
            __Vdly__KL_ptp_clock_validity__DOT__lease_r 
                = vlSelfRef.sw_wdog_q_i;
            vlSelfRef.KL_ptp_clock_validity__DOT__no_lease_r 
                = (1U & (~ (0U != (IData)(vlSelfRef.sw_wdog_q_i))));
        } else if (((7U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r)) 
                    & (0U != (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__lease_r)))) {
            __Vdly__KL_ptp_clock_validity__DOT__lease_r 
                = (0x00000fffU & ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__lease_r) 
                                  - (IData)(1U)));
            if ((1U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__lease_r))) {
                vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r = 0U;
                vlSelfRef.KL_ptp_clock_validity__DOT__no_lease_r = 1U;
            }
        }
        vlSelfRef.KL_ptp_clock_validity__DOT__gm_r 
            = vlSelfRef.gm_id_i;
    } else {
        __Vdly__KL_ptp_clock_validity__DOT__qdiv_r = 0U;
        __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r = 0U;
        vlSelfRef.KL_ptp_clock_validity__DOT__tu_ivals_r = 0U;
        __Vdly__KL_ptp_clock_validity__DOT__ival_r = 0U;
        __Vdly__KL_ptp_clock_validity__DOT__hold_r = 0U;
        vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r = 0U;
        __Vdly__KL_ptp_clock_validity__DOT__lease_r = 0U;
        vlSelfRef.KL_ptp_clock_validity__DOT__no_lease_r = 1U;
        vlSelfRef.KL_ptp_clock_validity__DOT__gm_r = 0ULL;
    }
    vlSelfRef.KL_ptp_clock_validity__DOT__tu_seen_r 
        = __Vdly__KL_ptp_clock_validity__DOT__tu_seen_r;
    vlSelfRef.KL_ptp_clock_validity__DOT__ival_r = __Vdly__KL_ptp_clock_validity__DOT__ival_r;
    vlSelfRef.KL_ptp_clock_validity__DOT__hold_r = __Vdly__KL_ptp_clock_validity__DOT__hold_r;
    vlSelfRef.KL_ptp_clock_validity__DOT__qdiv_r = __Vdly__KL_ptp_clock_validity__DOT__qdiv_r;
    vlSelfRef.KL_ptp_clock_validity__DOT__lease_r = __Vdly__KL_ptp_clock_validity__DOT__lease_r;
    vlSelfRef.tu_ivals_o = vlSelfRef.KL_ptp_clock_validity__DOT__tu_ivals_r;
    vlSelfRef.ts_uncertain_o = (1U & (~ ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r) 
                                         & (0U == (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r)))));
    vlSelfRef.stat_o = (((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__lease_r) 
                         << 4U) | ((((0U != (IData)(vlSelfRef.KL_ptp_clock_validity__DOT__hold_r)) 
                                     << 3U) | ((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__no_lease_r) 
                                               << 2U)) 
                                   | (((IData)(vlSelfRef.KL_ptp_clock_validity__DOT__sync_ok_r) 
                                       << 1U) | (IData)(vlSelfRef.ts_uncertain_o))));
}

void VKL_ptp_clock_validity___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void VKL_ptp_clock_validity___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool VKL_ptp_clock_validity___024root___eval_phase__act(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_phase__act\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((IData)(vlSelfRef.clk_i) 
                                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_i__0)))));
        vlSelfRef.__Vtrigprevexpr___TOP__clk_i__0 = vlSelfRef.clk_i;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VKL_ptp_clock_validity___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    VKL_ptp_clock_validity___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void VKL_ptp_clock_validity___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool VKL_ptp_clock_validity___024root___eval_phase__nba(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_phase__nba\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = VKL_ptp_clock_validity___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                VKL_ptp_clock_validity___024root___nba_sequent__TOP__0(vlSelf);
            }
        }
        VKL_ptp_clock_validity___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void VKL_ptp_clock_validity___024root___eval(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            VKL_ptp_clock_validity___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv", 98, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                VKL_ptp_clock_validity___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv", 98, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = VKL_ptp_clock_validity___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = VKL_ptp_clock_validity___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void VKL_ptp_clock_validity___024root___eval_debug_assertions(VKL_ptp_clock_validity___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VKL_ptp_clock_validity___024root___eval_debug_assertions\n"); );
    VKL_ptp_clock_validity__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk_i & 0xfeU)))) {
        Verilated::overWidthError("clk_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.sw_wr_p_i & 0xfeU)))) {
        Verilated::overWidthError("sw_wr_p_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.sw_sync_ok_i & 0xfeU)))) {
        Verilated::overWidthError("sw_sync_ok_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.sw_disc_p_i & 0xfeU)))) {
        Verilated::overWidthError("sw_disc_p_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.sw_wdog_q_i & 0xf000U)))) {
        Verilated::overWidthError("sw_wdog_q_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.phc_load_p_i & 0xfeU)))) {
        Verilated::overWidthError("phc_load_p_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.phc_adj_p_i & 0xfeU)))) {
        Verilated::overWidthError("phc_adj_p_i");
    }
}
#endif  // VL_DEBUG
