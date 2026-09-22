// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsemantics_probe.h for the primary calling header

#include "Vsemantics_probe__pch.h"

VL_ATTR_COLD void Vsemantics_probe___024root___eval_static(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_static\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__valid__0 = vlSelfRef.valid;
    vlSelfRef.__Vtrigprevexpr___TOP__ready__0 = vlSelfRef.ready;
    vlSelfRef.__Vtrigprevexpr___TOP__data__0 = vlSelfRef.data;
    vlSelfRef.__Vtrigprevexpr___TOP__keep__0 = vlSelfRef.keep;
    vlSelfRef.__Vtrigprevexpr___TOP__last__0 = vlSelfRef.last;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
}

VL_ATTR_COLD void Vsemantics_probe___024root___eval_initial(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_initial\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vsemantics_probe___024root___eval_final(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_final\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vsemantics_probe___024root___eval_phase__stl(Vsemantics_probe___024root* vlSelf);

VL_ATTR_COLD void Vsemantics_probe___024root___eval_settle(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_settle\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vsemantics_probe___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 3, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vsemantics_probe___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vsemantics_probe___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vsemantics_probe___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vsemantics_probe___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD bool Vsemantics_probe___024root___eval_phase__stl(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_phase__stl\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vsemantics_probe___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vsemantics_probe___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__0
                    vlSelfRef.semantics_probe__DOT__real_checker__DOT__stalled_w 
                        = ((~ (IData)(vlSelfRef.ready)) 
                           & (IData)(vlSelfRef.valid));
                }
            }
        }
    }
    return (__VstlExecute);
}

bool Vsemantics_probe___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vsemantics_probe___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( keep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( last)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vsemantics_probe___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vsemantics_probe___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vsemantics_probe___024root___ctor_var_reset(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___ctor_var_reset\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4944192500720994163ull);
    vlSelf->ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 898948264233693212ull);
    vlSelf->data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10363016170300574568ull);
    vlSelf->keep = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3640148603251906323ull);
    vlSelf->last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2304216914404789790ull);
    vlSelf->semantics_probe__DOT___Vpast_1_1 = 0;
    vlSelf->semantics_probe__DOT___Vpast_4_1 = 0;
    vlSelf->semantics_probe__DOT___Vpast_5_1 = 0;
    vlSelf->semantics_probe__DOT__real_checker__DOT__stalled_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12926281137872467361ull);
    vlSelf->semantics_probe__DOT__real_checker__DOT___Vpast_1_1 = 0;
    vlSelf->semantics_probe__DOT__real_checker__DOT___Vpast_2_1 = 0;
    vlSelf->semantics_probe__DOT__real_checker__DOT___Vpast_4_1 = 0;
    vlSelf->semantics_probe__DOT__real_checker__DOT___Vpast_6_1 = 0;
    vlSelf->semantics_probe__DOT__real_checker__DOT___Vpast_8_1 = 0;
    vlSelf->__Vsampled_TOP__valid = 0;
    vlSelf->__Vsampled_TOP__ready = 0;
    vlSelf->__Vsampled_TOP__rst_n = 0;
    vlSelf->__Vsampled_TOP__data = 0;
    vlSelf->__Vsampled_TOP__keep = 0;
    vlSelf->__Vsampled_TOP__last = 0;
    vlSelf->__Vsampled_TOP__semantics_probe__DOT__real_checker__DOT__stalled_w = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__keep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__last__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
