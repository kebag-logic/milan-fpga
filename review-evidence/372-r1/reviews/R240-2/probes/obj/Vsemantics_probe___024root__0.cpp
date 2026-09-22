// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsemantics_probe.h for the primary calling header

#include "Vsemantics_probe__pch.h"

extern "C" void probe_result(const char* rule_name, svBit passed);

void Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(const VerilatedScope* __Vscopep, const char* __Vfilenamep, IData/*31:0*/ __Vlineno, const std::string &rule_name, CData/*0:0*/ passed) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP\n"); );
    // Body
    const char* rule_name__Vcvt;
    rule_name__Vcvt = rule_name.c_str();
    svBit passed__Vcvt;
    passed__Vcvt = passed;
    Verilated::dpiContext(__Vscopep, __Vfilenamep, __Vlineno);
    probe_result(rule_name__Vcvt, passed__Vcvt);
}

extern "C" void axis_sva_witness(const char* rule_name, svBit nonvacuous);

void Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP(const VerilatedScope* __Vscopep, const char* __Vfilenamep, IData/*31:0*/ __Vlineno, const std::string &rule_name, CData/*0:0*/ nonvacuous) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP\n"); );
    // Body
    const char* rule_name__Vcvt;
    rule_name__Vcvt = rule_name.c_str();
    svBit nonvacuous__Vcvt;
    nonvacuous__Vcvt = nonvacuous;
    Verilated::dpiContext(__Vscopep, __Vfilenamep, __Vlineno);
    axis_sva_witness(rule_name__Vcvt, nonvacuous__Vcvt);
}

bool Vsemantics_probe___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___trigger_anySet__ico\n"); );
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
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vsemantics_probe___024root___eval_phase__ico(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_phase__ico\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__ico
        vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                        (((((IData)(vlSelfRef.last) 
                                                            != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__last__0)) 
                                                           << 6U) 
                                                          | ((((IData)(vlSelfRef.keep) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__keep__0)) 
                                                              << 5U) 
                                                             | (((IData)(vlSelfRef.data) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__data__0)) 
                                                                << 4U))) 
                                                         | (((((IData)(vlSelfRef.ready) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__ready__0)) 
                                                              << 3U) 
                                                             | (((IData)(vlSelfRef.valid) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__valid__0)) 
                                                                << 2U)) 
                                                            | ((((IData)(vlSelfRef.rst_n) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0)) 
                                                                << 1U) 
                                                               | ((IData)(vlSelfRef.clk) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
        vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
        vlSelfRef.__Vtrigprevexpr___TOP__valid__0 = vlSelfRef.valid;
        vlSelfRef.__Vtrigprevexpr___TOP__ready__0 = vlSelfRef.ready;
        vlSelfRef.__Vtrigprevexpr___TOP__data__0 = vlSelfRef.data;
        vlSelfRef.__Vtrigprevexpr___TOP__keep__0 = vlSelfRef.keep;
        vlSelfRef.__Vtrigprevexpr___TOP__last__0 = vlSelfRef.last;
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
        }
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vsemantics_probe___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vsemantics_probe___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        {
            // Inlined CFunc: _eval_ico
            if ((0x000000000000000cULL & vlSelfRef.__VicoTriggered[0U])) {
                {
                    // Inlined CFunc: _ico_comb__TOP__0
                    vlSelfRef.semantics_probe__DOT__real_checker__DOT__stalled_w 
                        = ((~ (IData)(vlSelfRef.ready)) 
                           & (IData)(vlSelfRef.valid));
                }
            }
        }
    }
    return (__VicoExecute);
}

bool Vsemantics_probe___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___trigger_anySet__act\n"); );
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

void Vsemantics_probe___024root___nba_sequent__TOP__0(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___nba_sequent__TOP__0\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_ON, 1, 1)) {
        if (vlSelfRef.semantics_probe__DOT___Vpast_1_1) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x0000000fU, "past_one"s, 1U);
            }
        } else if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)) {
            Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x00000010U, "past_one"s, 0U);
        }
        if (vlSelfRef.semantics_probe__DOT___Vpast_1_1) {
            if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x00000012U, "stable_one"s, 1U);
            }
        } else if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)) {
            Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x00000013U, "stable_one"s, 0U);
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.semantics_probe__DOT___Vpast_5_1)) 
                       | (IData)(vlSelfRef.__Vsampled_TOP__valid)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x00000016U, "bad_flag"s, (IData)(vlSelfRef.semantics_probe__DOT___Vpast_4_1));
                }
            } else if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)) {
                Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__probe_result_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe), 
                                                                                "$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 0x00000017U, "unexpected_fail"s, 1U);
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_2_1)) 
                       | (IData)(vlSelfRef.__Vsampled_TOP__valid)))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe__real_checker), 
                                                                                "$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 0x00000045U, "ap_tvalid_held_until_handshake"s, (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:71: Assertion failed in %m: TVALID fell before TREADY took the beat (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"semantics_probe.real_checker.ap_tvalid_held_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 71, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_4_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__data))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe__real_checker), 
                                                                                "$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 0x0000004bU, "ap_tdata_stable_until_handshake"s, (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:77: Assertion failed in %m: TDATA changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"semantics_probe.real_checker.ap_tdata_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 77, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_6_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__keep))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe__real_checker), 
                                                                                "$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 0x00000051U, "ap_tkeep_stable_until_handshake"s, (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:83: Assertion failed in %m: TKEEP changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"semantics_probe.real_checker.ap_tkeep_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 83, "");
            }
        }
        if (vlSelfRef.rst_n) {
            if ((1U & ((~ (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_2_1)) 
                       | ((IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_8_1) 
                          == (IData)(vlSelfRef.__Vsampled_TOP__last))))) {
                if (vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_PASS_ON_NONVACUOUS, 1, 1)) {
                    Vsemantics_probe___024root____Vdpiimwrap_semantics_probe__DOT__real_checker__DOT__axis_sva_witness_TOP(
                                                                                (vlSymsp->__Vscopep_semantics_probe__real_checker), 
                                                                                "$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 0x00000057U, "ap_tlast_stable_until_handshake"s, (IData)(vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_1_1));
                }
            } else if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertCtlGet(VerilatedAssertCtlQuery::ASSERT_CTL_FAIL_ON, 1, 1)))) {
                VL_WRITEF_NX("[%0t] %%Error: axis_stream_source_sva.sv:89: Assertion failed in %m: TLAST changed while the beat was stalled (IHI0051A 2.2)\n",3, 'M',vlSymsp->name(),"semantics_probe.real_checker.ap_tlast_stable_until_handshake", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("$VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv", 89, "");
            }
        }
    }
    vlSelfRef.semantics_probe__DOT___Vpast_1_1 = 1U;
    vlSelfRef.semantics_probe__DOT___Vpast_4_1 = ((IData)(vlSelfRef.__Vsampled_TOP__valid) 
                                                  & (~ (IData)(vlSelfRef.__Vsampled_TOP__ready)));
    vlSelfRef.semantics_probe__DOT___Vpast_5_1 = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
                                                  & ((IData)(vlSelfRef.__Vsampled_TOP__valid) 
                                                     & (~ (IData)(vlSelfRef.__Vsampled_TOP__ready))));
    vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_4_1 
        = vlSelfRef.__Vsampled_TOP__data;
    vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_6_1 
        = vlSelfRef.__Vsampled_TOP__keep;
    vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_8_1 
        = vlSelfRef.__Vsampled_TOP__last;
    vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_2_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__semantics_probe__DOT__real_checker__DOT__stalled_w));
    vlSelfRef.semantics_probe__DOT__real_checker__DOT___Vpast_1_1 
        = ((IData)(vlSelfRef.__Vsampled_TOP__rst_n) 
           & (IData)(vlSelfRef.__Vsampled_TOP__semantics_probe__DOT__real_checker__DOT__stalled_w));
}

void Vsemantics_probe___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vsemantics_probe___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vsemantics_probe___024root___eval_phase__act(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_phase__act\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vsemantics_probe___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vsemantics_probe___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vsemantics_probe___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vsemantics_probe___024root___eval_phase__nba(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_phase__nba\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vsemantics_probe___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vsemantics_probe___024root___nba_sequent__TOP__0(vlSelf);
            }
        }
        Vsemantics_probe___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vsemantics_probe___024root___eval(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    {
        // Inlined CFunc: _sample
        vlSelfRef.__Vsampled_TOP__valid = vlSelfRef.valid;
        vlSelfRef.__Vsampled_TOP__ready = vlSelfRef.ready;
        vlSelfRef.__Vsampled_TOP__rst_n = vlSelfRef.rst_n;
        vlSelfRef.__Vsampled_TOP__data = vlSelfRef.data;
        vlSelfRef.__Vsampled_TOP__keep = vlSelfRef.keep;
        vlSelfRef.__Vsampled_TOP__last = vlSelfRef.last;
        vlSelfRef.__Vsampled_TOP__semantics_probe__DOT__real_checker__DOT__stalled_w 
            = vlSelfRef.semantics_probe__DOT__real_checker__DOT__stalled_w;
    }
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vsemantics_probe___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 3, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vsemantics_probe___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vsemantics_probe___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 3, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vsemantics_probe___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv", 3, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vsemantics_probe___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vsemantics_probe___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vsemantics_probe___024root___eval_debug_assertions(Vsemantics_probe___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsemantics_probe___024root___eval_debug_assertions\n"); );
    Vsemantics_probe__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.valid & 0xfeU)))) {
        Verilated::overWidthError("valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.ready & 0xfeU)))) {
        Verilated::overWidthError("ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.keep & 0xfeU)))) {
        Verilated::overWidthError("keep");
    }
    if (VL_UNLIKELY(((vlSelfRef.last & 0xfeU)))) {
        Verilated::overWidthError("last");
    }
}
#endif  // VL_DEBUG
