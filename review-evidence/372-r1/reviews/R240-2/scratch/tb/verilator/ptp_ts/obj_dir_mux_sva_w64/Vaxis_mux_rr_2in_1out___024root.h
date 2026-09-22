// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#ifndef VERILATED_VAXIS_MUX_RR_2IN_1OUT___024ROOT_H_
#define VERILATED_VAXIS_MUX_RR_2IN_1OUT___024ROOT_H_  // guard

#include "verilated.h"


class Vaxis_mux_rr_2in_1out__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vaxis_mux_rr_2in_1out___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(rst_n,0,0);
        VL_IN8(s0_tvalid,0,0);
        VL_OUT8(s0_tready,0,0);
        VL_IN8(s0_tlast,0,0);
        VL_IN8(s0_tkeep,7,0);
        VL_IN8(s1_tvalid,0,0);
        VL_OUT8(s1_tready,0,0);
        VL_IN8(s1_tlast,0,0);
        VL_IN8(s1_tkeep,7,0);
        VL_OUT8(m_tvalid,0,0);
        VL_IN8(m_tready,0,0);
        VL_OUT8(m_tlast,0,0);
        VL_OUT8(m_tkeep,7,0);
        CData/*1:0*/ axis_mux_rr_2in_1out__DOT__state;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__last_served;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_2_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_3_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_4_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_5_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_7_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_8_1;
        CData/*1:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_9_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_11_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_12_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_14_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT___Vpast_15_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_1_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_2_1;
        CData/*7:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_6_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_8_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_1_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_2_1;
        CData/*7:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_6_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_8_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_1_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_2_1;
        CData/*7:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_6_1;
        CData/*0:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_8_1;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_0;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_1;
        CData/*1:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__state;
        CData/*0:0*/ __Vsampled_TOP__rst_n;
        CData/*0:0*/ __Vsampled_TOP__s0_tvalid;
        CData/*0:0*/ __Vsampled_TOP__s1_tvalid;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s0_mid_packet_w;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__s1_mid_packet_w;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__owner_last_handshake_w;
        CData/*0:0*/ __Vsampled_TOP__m_tvalid;
        CData/*7:0*/ __Vsampled_TOP__m_tkeep;
        CData/*0:0*/ __Vsampled_TOP__m_tlast;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT__stalled_w;
        CData/*7:0*/ __Vsampled_TOP__s1_tkeep;
        CData/*0:0*/ __Vsampled_TOP__s1_tlast;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT__stalled_w;
        CData/*7:0*/ __Vsampled_TOP__s0_tkeep;
        CData/*0:0*/ __Vsampled_TOP__s0_tlast;
        CData/*0:0*/ __Vsampled_TOP__axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT__stalled_w;
    };
    struct {
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s0_tvalid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s0_tlast__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__s0_tkeep__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s1_tvalid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s1_tlast__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__s1_tkeep__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__m_tready__0;
        CData/*0:0*/ __VicoDidInit;
        CData/*0:0*/ __VicoPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__1;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        IData/*31:0*/ __VactIterCount;
        VL_IN64(s0_tdata,63,0);
        VL_IN64(s1_tdata,63,0);
        VL_OUT64(m_tdata,63,0);
        QData/*63:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_m_dut__DOT___Vpast_4_1;
        QData/*63:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s1_stimulus__DOT___Vpast_4_1;
        QData/*63:0*/ axis_mux_rr_2in_1out__DOT__u_sva__DOT__u_s0_stimulus__DOT___Vpast_4_1;
        QData/*63:0*/ __Vsampled_TOP__m_tdata;
        QData/*63:0*/ __Vsampled_TOP__s1_tdata;
        QData/*63:0*/ __Vsampled_TOP__s0_tdata;
        QData/*63:0*/ __Vtrigprevexpr___TOP__s0_tdata__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__s1_tdata__0;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    Vaxis_mux_rr_2in_1out__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vaxis_mux_rr_2in_1out___024root(Vaxis_mux_rr_2in_1out__Syms* symsp, const char* namep);
    ~Vaxis_mux_rr_2in_1out___024root();
    VL_UNCOPYABLE(Vaxis_mux_rr_2in_1out___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
