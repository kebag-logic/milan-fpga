// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#include "Vaxis_mux_rr_2in_1out__pch.h"

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___eval_static(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_static\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__s0_tdata__0 = vlSelfRef.s0_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s0_tvalid__0 = vlSelfRef.s0_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s0_tlast__0 = vlSelfRef.s0_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__s0_tkeep__0 = vlSelfRef.s0_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__s1_tdata__0 = vlSelfRef.s1_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s1_tvalid__0 = vlSelfRef.s1_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s1_tlast__0 = vlSelfRef.s1_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__s1_tkeep__0 = vlSelfRef.s1_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__m_tready__0 = vlSelfRef.m_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
}

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___eval_initial(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_initial\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___eval_final(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_final\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vaxis_mux_rr_2in_1out___024root___eval_phase__stl(Vaxis_mux_rr_2in_1out___024root* vlSelf);

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___eval_settle(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_settle\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vaxis_mux_rr_2in_1out___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/hdl/common/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vaxis_mux_rr_2in_1out___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vaxis_mux_rr_2in_1out___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD bool Vaxis_mux_rr_2in_1out___024root___eval_phase__stl(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_phase__stl\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vaxis_mux_rr_2in_1out___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vaxis_mux_rr_2in_1out___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                {
                    // Inlined CFunc: _stl_sequent__TOP__0
                    vlSelfRef.s0_tready = ((IData)(vlSelfRef.m_tready) 
                                           & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
                    vlSelfRef.s1_tready = ((IData)(vlSelfRef.m_tready) 
                                           & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
                    vlSelfRef.m_tvalid = 0U;
                    vlSelfRef.m_tdata = 0ULL;
                    vlSelfRef.m_tkeep = 0U;
                    vlSelfRef.m_tlast = 0U;
                    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tvalid = vlSelfRef.s0_tvalid;
                        vlSelfRef.m_tdata = vlSelfRef.s0_tdata;
                        vlSelfRef.m_tkeep = vlSelfRef.s0_tkeep;
                        vlSelfRef.m_tlast = vlSelfRef.s0_tlast;
                    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tvalid = vlSelfRef.s1_tvalid;
                        vlSelfRef.m_tdata = vlSelfRef.s1_tdata;
                        vlSelfRef.m_tkeep = vlSelfRef.s1_tkeep;
                        vlSelfRef.m_tlast = vlSelfRef.s1_tlast;
                    }
                }
            }
        }
    }
    return (__VstlExecute);
}

bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vaxis_mux_rr_2in_1out___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( s0_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( s0_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( s0_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( s0_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( s1_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( s1_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( s1_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( s1_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( m_tready)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vaxis_mux_rr_2in_1out___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___ctor_var_reset(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___ctor_var_reset\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->s0_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10038523908176215039ull);
    vlSelf->s0_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10737655094133076506ull);
    vlSelf->s0_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5190480379160582775ull);
    vlSelf->s0_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9729448994020064200ull);
    vlSelf->s0_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9527560413845868703ull);
    vlSelf->s1_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6968326553760251947ull);
    vlSelf->s1_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7191469954384529373ull);
    vlSelf->s1_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1022631443850173021ull);
    vlSelf->s1_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14113428674425293274ull);
    vlSelf->s1_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4529824278714078222ull);
    vlSelf->m_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16534874751520676056ull);
    vlSelf->m_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6330821876457450032ull);
    vlSelf->m_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15425253223298272161ull);
    vlSelf->m_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9494342378649836147ull);
    vlSelf->m_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15983276138172624764ull);
    vlSelf->axis_mux_rr_2in_1out__DOT__state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18426771534712868549ull);
    vlSelf->axis_mux_rr_2in_1out__DOT__last_served = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13190672391043364691ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s0_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s0_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s0_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s0_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s1_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s1_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s1_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s1_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_tready__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
