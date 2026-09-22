// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#include "Vaxis_mux_rr_2in_1out__pch.h"

void Vaxis_mux_rr_2in_1out___024root___eval_triggers_vec__ico(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_triggers_vec__ico\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                    (((((IData)(vlSelfRef.m_tready) 
                                                        != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_tready__0)) 
                                                       << 0x0000000aU) 
                                                      | ((((IData)(vlSelfRef.s1_tkeep) 
                                                           != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s1_tkeep__0)) 
                                                          << 9U) 
                                                         | (((IData)(vlSelfRef.s1_tlast) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s1_tlast__0)) 
                                                            << 8U))) 
                                                     | (((((((IData)(vlSelfRef.s1_tvalid) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s1_tvalid__0)) 
                                                            << 3U) 
                                                           | ((vlSelfRef.s1_tdata 
                                                               != vlSelfRef.__Vtrigprevexpr___TOP__s1_tdata__0) 
                                                              << 2U)) 
                                                          | ((((IData)(vlSelfRef.s0_tkeep) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s0_tkeep__0)) 
                                                              << 1U) 
                                                             | ((IData)(vlSelfRef.s0_tlast) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s0_tlast__0)))) 
                                                         << 4U) 
                                                        | (((((IData)(vlSelfRef.s0_tvalid) 
                                                              != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s0_tvalid__0)) 
                                                             << 3U) 
                                                            | ((vlSelfRef.s0_tdata 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__s0_tdata__0) 
                                                               << 2U)) 
                                                           | ((((IData)(vlSelfRef.rst_n) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0)) 
                                                               << 1U) 
                                                              | ((IData)(vlSelfRef.clk) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))))))));
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
    }
}

bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___trigger_anySet__ico\n"); );
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
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vaxis_mux_rr_2in_1out___024root___eval_phase__ico(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_phase__ico\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vaxis_mux_rr_2in_1out___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vaxis_mux_rr_2in_1out___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        {
            // Inlined CFunc: _eval_ico
            if ((0x0000000000000400ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_sequent__TOP__0
                    vlSelfRef.s0_tready = ((IData)(vlSelfRef.m_tready) 
                                           & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
                    vlSelfRef.s1_tready = ((IData)(vlSelfRef.m_tready) 
                                           & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
                }
            }
            if ((0x0000000000000088ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__0
                    vlSelfRef.m_tvalid = 0U;
                    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tvalid = vlSelfRef.s0_tvalid;
                    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tvalid = vlSelfRef.s1_tvalid;
                    }
                }
            }
            if ((0x0000000000000044ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__1
                    vlSelfRef.m_tdata = 0ULL;
                    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tdata = vlSelfRef.s0_tdata;
                    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tdata = vlSelfRef.s1_tdata;
                    }
                }
            }
            if ((0x0000000000000220ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__2
                    vlSelfRef.m_tkeep = 0U;
                    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tkeep = vlSelfRef.s0_tkeep;
                    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tkeep = vlSelfRef.s1_tkeep;
                    }
                }
            }
            if ((0x0000000000000110ULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__3
                    vlSelfRef.m_tlast = 0U;
                    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tlast = vlSelfRef.s0_tlast;
                    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                        vlSelfRef.m_tlast = vlSelfRef.s1_tlast;
                    }
                }
            }
        }
    }
    return (__VicoExecute);
}

bool Vaxis_mux_rr_2in_1out___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___trigger_anySet__act\n"); );
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

void Vaxis_mux_rr_2in_1out___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vaxis_mux_rr_2in_1out___024root___eval_phase__act(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_phase__act\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vaxis_mux_rr_2in_1out___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vaxis_mux_rr_2in_1out___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

extern const VlUnpacked<CData/*1:0*/, 256> Vaxis_mux_rr_2in_1out__ConstPool__TABLE_hd45f40b9_0;

bool Vaxis_mux_rr_2in_1out___024root___eval_phase__nba(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_phase__nba\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vaxis_mux_rr_2in_1out___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _nba_sequent__TOP__0
                    CData/*1:0*/ __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state = 0;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state 
                        = vlSelfRef.axis_mux_rr_2in_1out__DOT__state;
                    if (vlSelfRef.rst_n) {
                        __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state 
                            = Vaxis_mux_rr_2in_1out__ConstPool__TABLE_hd45f40b9_0
                            [((((((IData)(vlSelfRef.s1_tlast) 
                                  << 3U) | ((IData)(vlSelfRef.m_tready) 
                                            << 2U)) 
                                | (((IData)(vlSelfRef.s0_tlast) 
                                    << 1U) | (IData)(vlSelfRef.s1_tvalid))) 
                               << 4U) | (((IData)(vlSelfRef.s0_tvalid) 
                                          << 3U) | 
                                         (((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served) 
                                           << 2U) | (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))))];
                        if (((((IData)(vlSelfRef.s0_tready) 
                               & (IData)(vlSelfRef.s0_tvalid)) 
                              & (IData)(vlSelfRef.s0_tlast)) 
                             | (((IData)(vlSelfRef.s1_tready) 
                                 & (IData)(vlSelfRef.s1_tvalid)) 
                                & (IData)(vlSelfRef.s1_tlast)))) {
                            vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served 
                                = (1U != (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state));
                        }
                    } else {
                        __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state = 0U;
                        vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served = 0U;
                    }
                    vlSelfRef.axis_mux_rr_2in_1out__DOT__state 
                        = __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__0___Vdly__axis_mux_rr_2in_1out__DOT__state;
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
        Vaxis_mux_rr_2in_1out___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vaxis_mux_rr_2in_1out___024root___eval(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/hdl/common/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vaxis_mux_rr_2in_1out___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/hdl/common/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/hdl/common/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vaxis_mux_rr_2in_1out___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vaxis_mux_rr_2in_1out___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vaxis_mux_rr_2in_1out___024root___eval_debug_assertions(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_debug_assertions\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.s0_tvalid & 0xfeU)))) {
        Verilated::overWidthError("s0_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s0_tlast & 0xfeU)))) {
        Verilated::overWidthError("s0_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.s1_tvalid & 0xfeU)))) {
        Verilated::overWidthError("s1_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s1_tlast & 0xfeU)))) {
        Verilated::overWidthError("s1_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_tready & 0xfeU)))) {
        Verilated::overWidthError("m_tready");
    }
}
#endif  // VL_DEBUG
