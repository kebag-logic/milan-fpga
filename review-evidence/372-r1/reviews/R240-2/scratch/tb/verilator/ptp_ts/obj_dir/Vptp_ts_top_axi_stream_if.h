// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vptp_ts_top.h for the primary calling header

#ifndef VERILATED_VPTP_TS_TOP_AXI_STREAM_IF_H_
#define VERILATED_VPTP_TS_TOP_AXI_STREAM_IF_H_  // guard

#include "verilated.h"


class Vptp_ts_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vptp_ts_top_axi_stream_if final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ __PVT__clk;
    CData/*0:0*/ __PVT__rst_n;
    CData/*0:0*/ tready;

    // INTERNAL VARIABLES
    Vptp_ts_top__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vptp_ts_top_axi_stream_if();
    ~Vptp_ts_top_axi_stream_if();
    void ctor(Vptp_ts_top__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vptp_ts_top_axi_stream_if);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
