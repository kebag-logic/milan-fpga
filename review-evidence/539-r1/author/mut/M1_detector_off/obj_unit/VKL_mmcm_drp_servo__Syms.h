// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VKL_MMCM_DRP_SERVO__SYMS_H_
#define VERILATED_VKL_MMCM_DRP_SERVO__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "VKL_mmcm_drp_servo.h"

// INCLUDE MODULE CLASSES
#include "VKL_mmcm_drp_servo___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) VKL_mmcm_drp_servo__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    VKL_mmcm_drp_servo* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    VKL_mmcm_drp_servo___024root   TOP;

    // CONSTRUCTORS
    VKL_mmcm_drp_servo__Syms(VerilatedContext* contextp, const char* namep, VKL_mmcm_drp_servo* modelp);
    ~VKL_mmcm_drp_servo__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
