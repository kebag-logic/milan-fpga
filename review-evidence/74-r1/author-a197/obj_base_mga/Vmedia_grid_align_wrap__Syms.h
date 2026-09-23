// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VMEDIA_GRID_ALIGN_WRAP__SYMS_H_
#define VERILATED_VMEDIA_GRID_ALIGN_WRAP__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vmedia_grid_align_wrap.h"

// INCLUDE MODULE CLASSES
#include "Vmedia_grid_align_wrap___024root.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vmedia_grid_align_wrap__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vmedia_grid_align_wrap* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vmedia_grid_align_wrap___024root TOP;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_media_grid_align_wrap__u_junction;

    // CONSTRUCTORS
    Vmedia_grid_align_wrap__Syms(VerilatedContext* contextp, const char* namep, Vmedia_grid_align_wrap* modelp);
    ~Vmedia_grid_align_wrap__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
