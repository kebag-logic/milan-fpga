// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vptp_ts_top.h for the primary calling header

#ifndef VERILATED_VPTP_TS_TOP___024UNIT_H_
#define VERILATED_VPTP_TS_TOP___024UNIT_H_  // guard

#include "verilated.h"


class Vptp_ts_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vptp_ts_top___024unit final {
  public:

    // INTERNAL VARIABLES
    Vptp_ts_top__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vptp_ts_top___024unit();
    ~Vptp_ts_top___024unit();
    void ctor(Vptp_ts_top__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vptp_ts_top___024unit);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
