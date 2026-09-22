// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VAXIS_MUX_RR_2IN_1OUT__SYMS_H_
#define VERILATED_VAXIS_MUX_RR_2IN_1OUT__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vaxis_mux_rr_2in_1out.h"

// INCLUDE MODULE CLASSES
#include "Vaxis_mux_rr_2in_1out___024root.h"
#include "Vaxis_mux_rr_2in_1out___024unit.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vaxis_mux_rr_2in_1out__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vaxis_mux_rr_2in_1out* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vaxis_mux_rr_2in_1out___024root TOP;

    // CONSTRUCTORS
    Vaxis_mux_rr_2in_1out__Syms(VerilatedContext* contextp, const char* namep, Vaxis_mux_rr_2in_1out* modelp);
    ~Vaxis_mux_rr_2in_1out__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
