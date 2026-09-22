// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsemantics_probe.h for the primary calling header

#ifndef VERILATED_VSEMANTICS_PROBE___024ROOT_H_
#define VERILATED_VSEMANTICS_PROBE___024ROOT_H_  // guard

#include "verilated.h"


class Vsemantics_probe__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vsemantics_probe___024root final {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(valid,0,0);
    VL_IN8(ready,0,0);
    VL_IN8(data,7,0);
    VL_IN8(keep,0,0);
    VL_IN8(last,0,0);
    CData/*0:0*/ semantics_probe__DOT___Vpast_1_1;
    CData/*0:0*/ semantics_probe__DOT___Vpast_4_1;
    CData/*0:0*/ semantics_probe__DOT___Vpast_5_1;
    CData/*0:0*/ semantics_probe__DOT__real_checker__DOT__stalled_w;
    CData/*0:0*/ semantics_probe__DOT__real_checker__DOT___Vpast_1_1;
    CData/*0:0*/ semantics_probe__DOT__real_checker__DOT___Vpast_2_1;
    CData/*7:0*/ semantics_probe__DOT__real_checker__DOT___Vpast_4_1;
    CData/*0:0*/ semantics_probe__DOT__real_checker__DOT___Vpast_6_1;
    CData/*0:0*/ semantics_probe__DOT__real_checker__DOT___Vpast_8_1;
    CData/*0:0*/ __Vsampled_TOP__valid;
    CData/*0:0*/ __Vsampled_TOP__ready;
    CData/*0:0*/ __Vsampled_TOP__rst_n;
    CData/*7:0*/ __Vsampled_TOP__data;
    CData/*0:0*/ __Vsampled_TOP__keep;
    CData/*0:0*/ __Vsampled_TOP__last;
    CData/*0:0*/ __Vsampled_TOP__semantics_probe__DOT__real_checker__DOT__stalled_w;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__valid__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__ready__0;
    CData/*7:0*/ __Vtrigprevexpr___TOP__data__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__keep__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__last__0;
    CData/*0:0*/ __VicoDidInit;
    CData/*0:0*/ __VicoPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__1;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vsemantics_probe__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vsemantics_probe___024root(Vsemantics_probe__Syms* symsp, const char* namep);
    ~Vsemantics_probe___024root();
    VL_UNCOPYABLE(Vsemantics_probe___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
