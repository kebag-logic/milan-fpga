// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VSIM__SYMS_H_
#define VERILATED_VSIM__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vsim.h"

// INCLUDE MODULE CLASSES
#include "Vsim___024root.h"
#include "Vsim_sim.h"
#include "Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.h"
#include "Vsim_VexiiRiscv.h"
#include "Vsim_KL_mbx_pkg.h"
#include "Vsim_RegFileMem.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vsim__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vsim* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vsim___024root                 TOP;
    Vsim_KL_mbx_pkg                TOP__KL_mbx_pkg;
    Vsim_sim                       TOP__sim;
    Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952 TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952;
    Vsim_VexiiRiscv                TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core;
    Vsim_RegFileMem                TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_sim__KL_mbx__u_evt;
    VerilatedScope* __Vscopep_sim__KL_mbx__u_rx;
    VerilatedScope* __Vscopep_sim__KL_mbx__u_rx__verdict__unnamedblk11__unnamedblk12;
    VerilatedScope* __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core;
    VerilatedScope* __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga;

    // CONSTRUCTORS
    Vsim__Syms(VerilatedContext* contextp, const char* namep, Vsim* modelp);
    ~Vsim__Syms();
    void Vsim__Syms__ctor__0();
    void Vsim__Syms__dtor__0();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
