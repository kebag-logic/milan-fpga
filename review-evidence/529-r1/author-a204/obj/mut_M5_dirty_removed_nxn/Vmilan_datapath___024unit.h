// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vmilan_datapath.h for the primary calling header

#ifndef VERILATED_VMILAN_DATAPATH___024UNIT_H_
#define VERILATED_VMILAN_DATAPATH___024UNIT_H_  // guard

#include "verilated.h"


class Vmilan_datapath__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vmilan_datapath___024unit final {
  public:

    // INTERNAL VARIABLES
    Vmilan_datapath__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vmilan_datapath___024unit();
    ~Vmilan_datapath___024unit();
    void ctor(Vmilan_datapath__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vmilan_datapath___024unit);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
