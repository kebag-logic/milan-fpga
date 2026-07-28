// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vmilan_datapath.h for the primary calling header

#ifndef VERILATED_VMILAN_DATAPATH_AXI_STREAM_IF__TC3_H_
#define VERILATED_VMILAN_DATAPATH_AXI_STREAM_IF__TC3_H_  // guard

#include "verilated.h"


class Vmilan_datapath__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vmilan_datapath_axi_stream_if__TC3 final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ __PVT__clk;
    CData/*0:0*/ __PVT__rst_n;
    CData/*0:0*/ tvalid;
    CData/*2:0*/ tdest;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_18;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_19;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_96;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_97;

    // INTERNAL VARIABLES
    Vmilan_datapath__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vmilan_datapath_axi_stream_if__TC3();
    ~Vmilan_datapath_axi_stream_if__TC3();
    void ctor(Vmilan_datapath__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vmilan_datapath_axi_stream_if__TC3);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
