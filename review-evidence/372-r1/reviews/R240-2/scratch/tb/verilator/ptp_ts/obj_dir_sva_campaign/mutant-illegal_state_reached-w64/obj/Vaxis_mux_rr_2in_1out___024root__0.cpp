// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#include "Vaxis_mux_rr_2in_1out__pch.h"

extern "C" void axis_sva_witness(const char* rule_name, svBit nonvacuous);

void Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(const VerilatedScope* __Vscopep, const char* __Vfilenamep, IData/*31:0*/ __Vlineno, const std::string &rule_name, CData/*0:0*/ nonvacuous) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP\n"); );
    // Body
    const char* rule_name__Vcvt;
    rule_name__Vcvt = rule_name.c_str();
    svBit nonvacuous__Vcvt;
    nonvacuous__Vcvt = nonvacuous;
    Verilated::dpiContext(__Vscopep, __Vfilenamep, __Vlineno);
    axis_sva_witness(rule_name__Vcvt, nonvacuous__Vcvt);
}

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

void Vaxis_mux_rr_2in_1out___024root___ico_comb__TOP__9(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___ico_comb__TOP__9\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_ON, 8, 1)) {
        if (((IData)(vlSelfRef.s0_tready) & (IData)(vlSelfRef.s1_tready))) {
            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:162: Assertion failed in %m: s0 and s1 were both given TREADY in the same cycle\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_grants_mutually_exclusive", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 162, "");
            }
        } else if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
            Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000a0U, "ai_grants_mutually_exclusive"s, 
                                                                                ((IData)(vlSelfRef.s0_tready) 
                                                                                | (IData)(vlSelfRef.s1_tready)));
        }
        if ((((IData)(vlSelfRef.s0_tready) == ((1U 
                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                               & (IData)(vlSelfRef.m_tready))) 
             & ((IData)(vlSelfRef.s1_tready) == ((2U 
                                                  == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                 & (IData)(vlSelfRef.m_tready))))) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000a6U, "ai_ready_only_for_owner_and_ready_sink"s, 
                                                                                (((1U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                | (2U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) 
                                                                                & (IData)(vlSelfRef.m_tready)));
            }
        } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
            VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:169: Assertion failed in %m: a source's TREADY is not exactly 'it owns the output and the sink is ready'\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_ready_only_for_owner_and_ready_sink", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 169, "");
        }
        if (((IData)(vlSelfRef.m_tvalid) == (((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                              & (IData)(vlSelfRef.s0_tvalid)) 
                                             | ((2U 
                                                 == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                & (IData)(vlSelfRef.s1_tvalid))))) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000adU, "ai_tvalid_forwarded"s, 
                                                                                (((1U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                & (IData)(vlSelfRef.s0_tvalid)) 
                                                                                | ((2U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                & (IData)(vlSelfRef.s1_tvalid))));
            }
        } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
            VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:176: Assertion failed in %m: m TVALID is not the owning source's TVALID, or is high with no owner\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_tvalid_forwarded", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 176, "");
        }
        if (((IData)(vlSelfRef.m_tvalid) & (IData)(vlSelfRef.m_tready))) {
            if (((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))
                  ? (((vlSelfRef.m_tdata == vlSelfRef.s0_tdata) 
                      & ((IData)(vlSelfRef.m_tkeep) 
                         == (IData)(vlSelfRef.s0_tkeep))) 
                     & ((IData)(vlSelfRef.m_tlast) 
                        == (IData)(vlSelfRef.s0_tlast)))
                  : ((((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                       & (vlSelfRef.m_tdata == vlSelfRef.s1_tdata)) 
                      & ((IData)(vlSelfRef.m_tkeep) 
                         == (IData)(vlSelfRef.s1_tkeep))) 
                     & ((IData)(vlSelfRef.m_tlast) 
                        == (IData)(vlSelfRef.s1_tlast))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000b7U, "ai_payload_forwarded_on_transfer"s, 1U);
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:185: Assertion failed in %m: an accepted m beat does not carry the owning source's TDATA, TKEEP and TLAST\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_payload_forwarded_on_transfer", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 185, "");
            }
        }
    }
}

void Vaxis_mux_rr_2in_1out___024root___eval_ico(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___eval_ico\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x0000000000000044ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__0
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
            // Inlined CFunc: _ico_comb__TOP__1
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
            // Inlined CFunc: _ico_comb__TOP__2
            vlSelfRef.m_tlast = 0U;
            if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                vlSelfRef.m_tlast = vlSelfRef.s0_tlast;
            } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                vlSelfRef.m_tlast = vlSelfRef.s1_tlast;
            }
        }
    }
    if ((0x0000000000000088ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__3
            vlSelfRef.m_tvalid = 0U;
            if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                vlSelfRef.m_tvalid = vlSelfRef.s0_tvalid;
            } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
                vlSelfRef.m_tvalid = vlSelfRef.s1_tvalid;
            }
        }
    }
    if ((0x0000000000000400ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__0
            vlSelfRef.s0_tready = ((IData)(vlSelfRef.m_tready) 
                                   & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
            vlSelfRef.s1_tready = ((IData)(vlSelfRef.m_tready) 
                                   & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
        }
    }
    if ((0x0000000000000488ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__4
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w 
                = ((~ (IData)(vlSelfRef.m_tready)) 
                   & (IData)(vlSelfRef.m_tvalid));
        }
    }
    if ((0x0000000000000408ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__5
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w 
                = ((~ (IData)(vlSelfRef.s0_tready)) 
                   & (IData)(vlSelfRef.s0_tvalid));
        }
    }
    if ((0x0000000000000418ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__6
            vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1 
                = ((IData)(vlSelfRef.s0_tvalid) & ((IData)(vlSelfRef.s0_tlast) 
                                                   & (IData)(vlSelfRef.s0_tready)));
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w 
                = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1)) 
                   & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
        }
    }
    if ((0x0000000000000480ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__7
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w 
                = ((~ (IData)(vlSelfRef.s1_tready)) 
                   & (IData)(vlSelfRef.s1_tvalid));
        }
    }
    if ((0x0000000000000580ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__8
            vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0 
                = ((IData)(vlSelfRef.s1_tvalid) & ((IData)(vlSelfRef.s1_tlast) 
                                                   & (IData)(vlSelfRef.s1_tready)));
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w 
                = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)) 
                   & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
        }
    }
    if ((0x00000000000007fcULL & vlSelfRef.__VicoTriggered[0U])) {
        Vaxis_mux_rr_2in_1out___024root___ico_comb__TOP__9(vlSelf);
    }
    if ((0x0000000000000598ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__10
            vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w 
                = (((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)) 
                   | ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1)));
        }
    }
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
        Vaxis_mux_rr_2in_1out___024root___eval_ico(vlSelf);
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

extern const VlUnpacked<CData/*1:0*/, 256> Vaxis_mux_rr_2in_1out__ConstPool__TABLE_hc1749d7b_0;

void Vaxis_mux_rr_2in_1out___024root___nba_sequent__TOP__0(Vaxis_mux_rr_2in_1out___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxis_mux_rr_2in_1out___024root___nba_sequent__TOP__0\n"); );
    Vaxis_mux_rr_2in_1out__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __Vdly__axis_mux_rr_2in_1out__DOT__state;
    __Vdly__axis_mux_rr_2in_1out__DOT__state = 0;
    // Body
    if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_ON, 1, 1)) {
        if (vlSelfRef.rst_n) {
            if (VL_ONEHOT_I((((0U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
                              << 2U) | (((1U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
                                         << 1U) | (2U 
                                                   == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x0000007bU, "ap_state_legal"s, 1U);
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:125: Assertion failed in %m: the mux state decodes to none, or to more than one, of IDLE, STREAM_0 and STREAM_1\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.ap_state_legal", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 125, "");
            }
        }
        if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_15_1)) 
                   | (0U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state))))) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x00000099U, "ap_reset_releases_owner"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_14_1));
            }
        } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
            VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:155: Assertion failed in %m: an owner survived a reset\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.ap_reset_releases_owner", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 155, "");
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1)) 
                       | (IData)(vlSelfRef.__Vsampled_TOP__m_tvalid)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000045U, "ap_tvalid_held_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:71: Assertion failed in %m: TVALID fell before TREADY took the beat (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tvalid_held_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 71, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_12_1)) 
                       | (0U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x00000091U, "ap_owner_released_after_tlast"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_11_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:147: Assertion failed in %m: the owner kept the output after its TLAST beat was taken\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.ap_owner_released_after_tlast", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 147, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1)) 
                       | (IData)(vlSelfRef.__Vsampled_TOP__s1_tvalid)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000045U, "ap_tvalid_held_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:71: Assertion failed in %m: TVALID fell before TREADY took the beat (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tvalid_held_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 71, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1)) 
                       | (IData)(vlSelfRef.__Vsampled_TOP__s0_tvalid)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000045U, "ap_tvalid_held_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:71: Assertion failed in %m: TVALID fell before TREADY took the beat (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tvalid_held_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 71, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1)) 
                       | (vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_4_1 
                          == vlSelfRef.__Vsampled_TOP__m_tdata)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x0000004bU, "ap_tdata_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:77: Assertion failed in %m: TDATA changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tdata_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 77, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_6_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__m_tkeep))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000051U, "ap_tkeep_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:83: Assertion failed in %m: TKEEP changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tkeep_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 83, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_8_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__m_tlast))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000057U, "ap_tlast_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:89: Assertion failed in %m: TLAST changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tlast_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 89, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1)) 
                       | (vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_4_1 
                          == vlSelfRef.__Vsampled_TOP__s1_tdata)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x0000004bU, "ap_tdata_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:77: Assertion failed in %m: TDATA changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tdata_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 77, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_6_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__s1_tkeep))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000051U, "ap_tkeep_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:83: Assertion failed in %m: TKEEP changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tkeep_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 83, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_8_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__s1_tlast))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000057U, "ap_tlast_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:89: Assertion failed in %m: TLAST changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tlast_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 89, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1)) 
                       | (vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_4_1 
                          == vlSelfRef.__Vsampled_TOP__s0_tdata)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x0000004bU, "ap_tdata_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:77: Assertion failed in %m: TDATA changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tdata_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 77, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_6_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__s0_tkeep))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000051U, "ap_tkeep_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:83: Assertion failed in %m: TKEEP changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tkeep_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 83, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_8_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__s0_tlast))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus), 
                                                                                "../../common/sva/axis_stream_source_sva.sv", 0x00000057U, "ap_tlast_stable_until_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:89: Assertion failed in %m: TLAST changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tlast_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_stream_source_sva.sv", 89, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_8_1)) 
                       | ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_9_1) 
                          == (((1U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
                               << 1U) | (2U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state))))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x0000008aU, "ap_owner_held_until_tlast_handshake"s, (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_7_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:141: Assertion failed in %m: the output changed owner before the owning packet's TLAST beat was taken\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.ap_owner_held_until_tlast_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 141, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_3_1)) 
                       | (((1U != (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
                           | (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_4_1)) 
                          & ((2U != (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
                             | (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_5_1)))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x00000082U, "ap_grant_only_to_requester"s, 
                                                                                ((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_2_1) 
                                                                                & ((1U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                | (2U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)))));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:133: Assertion failed in %m: the arbiter granted the output to a source that was not offering a beat\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.ap_grant_only_to_requester", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 133, "");
            }
        }
    }
    __Vdly__axis_mux_rr_2in_1out__DOT__state = vlSelfRef.axis_mux_rr_2in_1out__DOT__state;
    if (vlSelfRef.rst_n) {
        __Vdly__axis_mux_rr_2in_1out__DOT__state = Vaxis_mux_rr_2in_1out__ConstPool__TABLE_hc1749d7b_0
            [((((((IData)(vlSelfRef.s1_tlast) << 3U) 
                 | ((IData)(vlSelfRef.m_tready) << 2U)) 
                | (((IData)(vlSelfRef.s0_tlast) << 1U) 
                   | (IData)(vlSelfRef.s1_tvalid))) 
               << 4U) | (((IData)(vlSelfRef.s0_tvalid) 
                          << 3U) | (((IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served) 
                                     << 2U) | (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))))];
        if (((((IData)(vlSelfRef.s0_tready) & (IData)(vlSelfRef.s0_tvalid)) 
              & (IData)(vlSelfRef.s0_tlast)) | (((IData)(vlSelfRef.s1_tready) 
                                                 & (IData)(vlSelfRef.s1_tvalid)) 
                                                & (IData)(vlSelfRef.s1_tlast)))) {
            vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served 
                = (1U != (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state));
        }
    } else {
        __Vdly__axis_mux_rr_2in_1out__DOT__state = 0U;
        vlSelfRef.axis_mux_rr_2in_1out__DOT__last_served = 0U;
    }
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_15_1 
        = (1U & (~ (IData)(vlSelfRef.__Vsampled_TOP__rst_n)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_14_1 
        = (1U & (~ (IData)(vlSelfRef.__Vsampled_TOP__rst_n)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_12_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_11_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_4_1 
        = vlSelfRef.__Vsampled_TOP__m_tdata;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_6_1 
        = vlSelfRef.__Vsampled_TOP__m_tkeep;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_8_1 
        = vlSelfRef.__Vsampled_TOP__m_tlast;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_4_1 
        = vlSelfRef.__Vsampled_TOP__s1_tdata;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_6_1 
        = vlSelfRef.__Vsampled_TOP__s1_tkeep;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_8_1 
        = vlSelfRef.__Vsampled_TOP__s1_tlast;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_4_1 
        = vlSelfRef.__Vsampled_TOP__s0_tdata;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_6_1 
        = vlSelfRef.__Vsampled_TOP__s0_tkeep;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_8_1 
        = vlSelfRef.__Vsampled_TOP__s0_tlast;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_9_1 
        = (((1U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)) 
            << 1U) | (2U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_8_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & ((IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w) 
              | (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_7_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & ((IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w) 
              | (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_4_1 
        = vlSelfRef.__Vsampled_TOP__s0_tvalid;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_5_1 
        = vlSelfRef.__Vsampled_TOP__s1_tvalid;
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_3_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (0U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_2_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (0U == (IData)(vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__state = __Vdly__axis_mux_rr_2in_1out__DOT__state;
    vlSelfRef.m_tdata = 0ULL;
    vlSelfRef.m_tkeep = 0U;
    vlSelfRef.m_tlast = 0U;
    vlSelfRef.m_tvalid = 0U;
    if ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
        vlSelfRef.m_tdata = vlSelfRef.s0_tdata;
        vlSelfRef.m_tkeep = vlSelfRef.s0_tkeep;
        vlSelfRef.m_tlast = vlSelfRef.s0_tlast;
        vlSelfRef.m_tvalid = vlSelfRef.s0_tvalid;
    } else if ((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) {
        vlSelfRef.m_tdata = vlSelfRef.s1_tdata;
        vlSelfRef.m_tkeep = vlSelfRef.s1_tkeep;
        vlSelfRef.m_tlast = vlSelfRef.s1_tlast;
        vlSelfRef.m_tvalid = vlSelfRef.s1_tvalid;
    }
    vlSelfRef.s0_tready = ((IData)(vlSelfRef.m_tready) 
                           & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.s1_tready = ((IData)(vlSelfRef.m_tready) 
                           & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w 
        = ((~ (IData)(vlSelfRef.m_tready)) & (IData)(vlSelfRef.m_tvalid));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w 
        = ((~ (IData)(vlSelfRef.s0_tready)) & (IData)(vlSelfRef.s0_tvalid));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1 = ((IData)(vlSelfRef.s0_tvalid) 
                                                & ((IData)(vlSelfRef.s0_tlast) 
                                                   & (IData)(vlSelfRef.s0_tready)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w 
        = ((~ (IData)(vlSelfRef.s1_tready)) & (IData)(vlSelfRef.s1_tvalid));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0 = ((IData)(vlSelfRef.s1_tvalid) 
                                                & ((IData)(vlSelfRef.s1_tlast) 
                                                   & (IData)(vlSelfRef.s1_tready)));
    if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_ON, 8, 1)) {
        if (((IData)(vlSelfRef.s0_tready) & (IData)(vlSelfRef.s1_tready))) {
            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:162: Assertion failed in %m: s0 and s1 were both given TREADY in the same cycle\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_grants_mutually_exclusive", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 162, "");
            }
        } else if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
            Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000a0U, "ai_grants_mutually_exclusive"s, 
                                                                                ((IData)(vlSelfRef.s0_tready) 
                                                                                | (IData)(vlSelfRef.s1_tready)));
        }
        if ((((IData)(vlSelfRef.s0_tready) == ((1U 
                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                               & (IData)(vlSelfRef.m_tready))) 
             & ((IData)(vlSelfRef.s1_tready) == ((2U 
                                                  == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                 & (IData)(vlSelfRef.m_tready))))) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000a6U, "ai_ready_only_for_owner_and_ready_sink"s, 
                                                                                (((1U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                | (2U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))) 
                                                                                & (IData)(vlSelfRef.m_tready)));
            }
        } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
            VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:169: Assertion failed in %m: a source's TREADY is not exactly 'it owns the output and the sink is ready'\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_ready_only_for_owner_and_ready_sink", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 169, "");
        }
        if (((IData)(vlSelfRef.m_tvalid) == (((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                              & (IData)(vlSelfRef.s0_tvalid)) 
                                             | ((2U 
                                                 == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                & (IData)(vlSelfRef.s1_tvalid))))) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000adU, "ai_tvalid_forwarded"s, 
                                                                                (((1U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                & (IData)(vlSelfRef.s0_tvalid)) 
                                                                                | ((2U 
                                                                                == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                                                                                & (IData)(vlSelfRef.s1_tvalid))));
            }
        } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
            VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:176: Assertion failed in %m: m TVALID is not the owning source's TVALID, or is high with no owner\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_tvalid_forwarded", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 176, "");
        }
        if (((IData)(vlSelfRef.m_tvalid) & (IData)(vlSelfRef.m_tready))) {
            if (((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state))
                  ? (((vlSelfRef.m_tdata == vlSelfRef.s0_tdata) 
                      & ((IData)(vlSelfRef.m_tkeep) 
                         == (IData)(vlSelfRef.s0_tkeep))) 
                     & ((IData)(vlSelfRef.m_tlast) 
                        == (IData)(vlSelfRef.s0_tlast)))
                  : ((((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
                       & (vlSelfRef.m_tdata == vlSelfRef.s1_tdata)) 
                      & ((IData)(vlSelfRef.m_tkeep) 
                         == (IData)(vlSelfRef.s1_tkeep))) 
                     & ((IData)(vlSelfRef.m_tlast) 
                        == (IData)(vlSelfRef.s1_tlast))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 8, 1)) {
                    Vaxis_mux_rr_2in_1out___024root____Vdpiimwrap_axis_mux_rr_2in_1out__DOT__u_sva__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_axis_mux_rr_2in_1out__u_sva), 
                                                                                "../../common/sva/axis_mux_rr_2in_1out_sva.sv", 0x000000b7U, "ai_payload_forwarded_on_transfer"s, 1U);
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 8, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_mux_rr_2in_1out_sva.sv:185: Assertion failed in %m: an accepted m beat does not carry the owning source's TDATA, TKEEP and TLAST\n",3, 'M',vlSymsp->name(),"axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_payload_forwarded_on_transfer", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../common/sva/axis_mux_rr_2in_1out_sva.sv", 185, "");
            }
        }
    }
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1)) 
           & (1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)) 
           & (2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)));
    vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w 
        = (((2U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)) 
           | ((1U == (IData)(vlSelfRef.axis_mux_rr_2in_1out__DOT__state)) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1)));
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
                Vaxis_mux_rr_2in_1out___024root___nba_sequent__TOP__0(vlSelf);
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
    {
        // Inlined CFunc: _sample
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__state;
        vlSelfRef.__Vsampled_TOP__rst_n = vlSelfRef.rst_n;
        vlSelfRef.__Vsampled_TOP__s0_tvalid = vlSelfRef.s0_tvalid;
        vlSelfRef.__Vsampled_TOP__s1_tvalid = vlSelfRef.s1_tvalid;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w;
        vlSelfRef.__Vsampled_TOP__m_tvalid = vlSelfRef.m_tvalid;
        vlSelfRef.__Vsampled_TOP__m_tdata = vlSelfRef.m_tdata;
        vlSelfRef.__Vsampled_TOP__m_tkeep = vlSelfRef.m_tkeep;
        vlSelfRef.__Vsampled_TOP__m_tlast = vlSelfRef.m_tlast;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w;
        vlSelfRef.__Vsampled_TOP__s1_tdata = vlSelfRef.s1_tdata;
        vlSelfRef.__Vsampled_TOP__s1_tkeep = vlSelfRef.s1_tkeep;
        vlSelfRef.__Vsampled_TOP__s1_tlast = vlSelfRef.s1_tlast;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w;
        vlSelfRef.__Vsampled_TOP__s0_tdata = vlSelfRef.s0_tdata;
        vlSelfRef.__Vsampled_TOP__s0_tkeep = vlSelfRef.s0_tkeep;
        vlSelfRef.__Vsampled_TOP__s0_tlast = vlSelfRef.s0_tlast;
        vlSelfRef.__Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w 
            = vlSelfRef.axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w;
    }
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vaxis_mux_rr_2in_1out___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/tb/verilator/ptp_ts/obj_dir_sva_campaign/mutant-illegal_state_reached-w64/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
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
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/tb/verilator/ptp_ts/obj_dir_sva_campaign/mutant-illegal_state_reached-w64/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vaxis_mux_rr_2in_1out___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/scratch/tb/verilator/ptp_ts/obj_dir_sva_campaign/mutant-illegal_state_reached-w64/axis_mux_rr_2in_1out.sv", 10, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
