// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vaxis_mux_rr_2in_1out.h for the primary calling header

#ifndef VERILATED_VAXIS_MUX_RR_2IN_1OUT___024UNIT_H_
#define VERILATED_VAXIS_MUX_RR_2IN_1OUT___024UNIT_H_  // guard

#include "verilated.h"


class Vaxis_mux_rr_2in_1out__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vaxis_mux_rr_2in_1out___024unit final {
  public:

    // INTERNAL VARIABLES
    Vaxis_mux_rr_2in_1out__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vaxis_mux_rr_2in_1out___024unit();
    ~Vaxis_mux_rr_2in_1out___024unit();
    void ctor(Vaxis_mux_rr_2in_1out__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vaxis_mux_rr_2in_1out___024unit);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
