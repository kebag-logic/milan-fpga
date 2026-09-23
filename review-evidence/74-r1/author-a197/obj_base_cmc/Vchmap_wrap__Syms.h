// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VCHMAP_WRAP__SYMS_H_
#define VERILATED_VCHMAP_WRAP__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vchmap_wrap.h"

// INCLUDE MODULE CLASSES
#include "Vchmap_wrap___024root.h"
#include "Vchmap_wrap_KL_chan_map_capture.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vchmap_wrap__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vchmap_wrap* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vchmap_wrap___024root          TOP;
    Vchmap_wrap_KL_chan_map_capture TOP__chmap_wrap__DOT__u_chmap_a;
    Vchmap_wrap_KL_chan_map_capture TOP__chmap_wrap__DOT__u_chmap_b;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_chmap_wrap__u_chmap_a;
    VerilatedScope* __Vscopep_chmap_wrap__u_chmap_b;

    // CONSTRUCTORS
    Vchmap_wrap__Syms(VerilatedContext* contextp, const char* namep, Vchmap_wrap* modelp);
    ~Vchmap_wrap__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
