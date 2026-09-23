// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vmedia_grid_align_wrap.h for the primary calling header

#ifndef VERILATED_VMEDIA_GRID_ALIGN_WRAP___024ROOT_H_
#define VERILATED_VMEDIA_GRID_ALIGN_WRAP___024ROOT_H_  // guard

#include "verilated.h"


class Vmedia_grid_align_wrap__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vmedia_grid_align_wrap___024root final {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(sel_i,0,0);
    VL_IN8(frame_ev_i,0,0);
    VL_OUT8(tick_o,0,0);
    VL_OUT8(engaged_o,0,0);
    CData/*0:0*/ media_grid_align_wrap__DOT__u_junction__DOT__tdm_pair_valid_i;
    CData/*0:0*/ media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r;
    CData/*0:0*/ media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r;
    CData/*4:0*/ media_grid_align_wrap__DOT__u_align__DOT__slip_r;
    CData/*0:0*/ media_grid_align_wrap__DOT__u_align__DOT__engaged_r;
    CData/*0:0*/ media_grid_align_wrap__DOT__u_align__DOT__fold_dn_w;
    CData/*0:0*/ media_grid_align_wrap__DOT__u_align__DOT__fold_up_w;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__sel_i__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__frame_ev_i__0;
    CData/*0:0*/ __VicoDidInit;
    CData/*0:0*/ __VicoPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__1;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    VL_OUT16(u_o,15,0);
    VL_OUT16(err_cyc_o,15,0);
    VL_OUT16(phase_o,15,0);
    VL_OUT16(tdm_dup_cnt_o,15,0);
    VL_OUT16(tdm_skip_cnt_o,15,0);
    SData/*15:0*/ media_grid_align_wrap__DOT__u_w;
    SData/*11:0*/ media_grid_align_wrap__DOT__u_nco__DOT__cnt_r;
    SData/*15:0*/ media_grid_align_wrap__DOT__u_nco__DOT__frac_r;
    SData/*12:0*/ media_grid_align_wrap__DOT__u_align__DOT__tst_r;
    SData/*12:0*/ media_grid_align_wrap__DOT__u_align__DOT__ref_r;
    SData/*13:0*/ media_grid_align_wrap__DOT__u_align__DOT__quiet_r;
    SData/*12:0*/ media_grid_align_wrap__DOT__u_align__DOT__tst_next_w;
    SData/*15:0*/ media_grid_align_wrap__DOT__u_align__DOT__err_r;
    IData/*31:0*/ media_grid_align_wrap__DOT__u_nco__DOT__trim_sel_w;
    IData/*17:0*/ media_grid_align_wrap__DOT__u_nco__DOT__trim_r;
    IData/*17:0*/ media_grid_align_wrap__DOT__u_nco__DOT__sum_w;
    IData/*31:0*/ media_grid_align_wrap__DOT__u_align__DOT__acc_r;
    IData/*31:0*/ media_grid_align_wrap__DOT__u_align__DOT__err_w;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<QData/*47:0*/, 1> media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vmedia_grid_align_wrap__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vmedia_grid_align_wrap___024root(Vmedia_grid_align_wrap__Syms* symsp, const char* namep);
    ~Vmedia_grid_align_wrap___024root();
    VL_UNCOPYABLE(Vmedia_grid_align_wrap___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
