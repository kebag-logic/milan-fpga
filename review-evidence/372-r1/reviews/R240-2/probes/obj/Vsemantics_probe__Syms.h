// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VSEMANTICS_PROBE__SYMS_H_
#define VERILATED_VSEMANTICS_PROBE__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vsemantics_probe.h"

// INCLUDE MODULE CLASSES
#include "Vsemantics_probe___024root.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vsemantics_probe__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vsemantics_probe* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vsemantics_probe___024root     TOP;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_semantics_probe;
    VerilatedScope* __Vscopep_semantics_probe__ap_bad_flag;
    VerilatedScope* __Vscopep_semantics_probe__ap_past_one;
    VerilatedScope* __Vscopep_semantics_probe__ap_stable_one;
    VerilatedScope* __Vscopep_semantics_probe__real_checker;
    VerilatedScope* __Vscopep_semantics_probe__real_checker__ap_tdata_stable_until_handshake;
    VerilatedScope* __Vscopep_semantics_probe__real_checker__ap_tkeep_stable_until_handshake;
    VerilatedScope* __Vscopep_semantics_probe__real_checker__ap_tlast_stable_until_handshake;
    VerilatedScope* __Vscopep_semantics_probe__real_checker__ap_tvalid_held_until_handshake;

    // CONSTRUCTORS
    Vsemantics_probe__Syms(VerilatedContext* contextp, const char* namep, Vsemantics_probe* modelp);
    ~Vsemantics_probe__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
