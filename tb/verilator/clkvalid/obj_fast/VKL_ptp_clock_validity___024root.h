// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VKL_ptp_clock_validity.h for the primary calling header

#ifndef VERILATED_VKL_PTP_CLOCK_VALIDITY___024ROOT_H_
#define VERILATED_VKL_PTP_CLOCK_VALIDITY___024ROOT_H_  // guard

#include "verilated.h"


class VKL_ptp_clock_validity__Syms;

class alignas(VL_CACHE_LINE_BYTES) VKL_ptp_clock_validity___024root final {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk_i,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(sw_wr_p_i,0,0);
    VL_IN8(sw_sync_ok_i,0,0);
    VL_IN8(sw_disc_p_i,0,0);
    VL_IN8(phc_load_p_i,0,0);
    VL_IN8(phc_adj_p_i,0,0);
    VL_OUT8(ts_uncertain_o,0,0);
    CData/*2:0*/ KL_ptp_clock_validity__DOT__qdiv_r;
    CData/*0:0*/ KL_ptp_clock_validity__DOT__sync_ok_r;
    CData/*0:0*/ KL_ptp_clock_validity__DOT__no_lease_r;
    CData/*1:0*/ KL_ptp_clock_validity__DOT__hold_r;
    CData/*1:0*/ KL_ptp_clock_validity__DOT__ival_r;
    CData/*0:0*/ KL_ptp_clock_validity__DOT__tu_seen_r;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk_i__0;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    VL_IN16(sw_wdog_q_i,11,0);
    SData/*11:0*/ KL_ptp_clock_validity__DOT__lease_r;
    VL_OUT(stat_o,31,0);
    VL_OUT(tu_ivals_o,31,0);
    IData/*31:0*/ KL_ptp_clock_validity__DOT__tu_ivals_r;
    IData/*31:0*/ __VactIterCount;
    VL_IN64(gm_id_i,63,0);
    QData/*63:0*/ KL_ptp_clock_validity__DOT__gm_r;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;

    // INTERNAL VARIABLES
    VKL_ptp_clock_validity__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    VKL_ptp_clock_validity___024root(VKL_ptp_clock_validity__Syms* symsp, const char* namep);
    ~VKL_ptp_clock_validity___024root();
    VL_UNCOPYABLE(VKL_ptp_clock_validity___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
