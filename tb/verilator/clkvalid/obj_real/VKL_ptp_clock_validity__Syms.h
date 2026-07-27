// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VKL_PTP_CLOCK_VALIDITY__SYMS_H_
#define VERILATED_VKL_PTP_CLOCK_VALIDITY__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "VKL_ptp_clock_validity.h"

// INCLUDE MODULE CLASSES
#include "VKL_ptp_clock_validity___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) VKL_ptp_clock_validity__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    VKL_ptp_clock_validity* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    VKL_ptp_clock_validity___024root TOP;

    // CONSTRUCTORS
    VKL_ptp_clock_validity__Syms(VerilatedContext* contextp, const char* namep, VKL_ptp_clock_validity* modelp);
    ~VKL_ptp_clock_validity__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
