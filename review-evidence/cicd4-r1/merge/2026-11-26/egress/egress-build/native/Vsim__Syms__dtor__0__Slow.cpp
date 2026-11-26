// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsim__pch.h"

void Vsim__Syms::Vsim__Syms__dtor__0() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_sim__KL_mbx__u_evt, __Vscopep_sim__KL_mbx__u_evt = nullptr);
    VL_DO_CLEAR(delete __Vscopep_sim__KL_mbx__u_rx, __Vscopep_sim__KL_mbx__u_rx = nullptr);
    VL_DO_CLEAR(delete __Vscopep_sim__KL_mbx__u_rx__verdict__unnamedblk11__unnamedblk12, __Vscopep_sim__KL_mbx__u_rx__verdict__unnamedblk11__unnamedblk12 = nullptr);
    VL_DO_CLEAR(delete __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core, __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core = nullptr);
    VL_DO_CLEAR(delete __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga, __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga = nullptr);
    // Tear down sub module instances
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.dtor();
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.dtor();
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.dtor();
    TOP__sim.dtor();
    TOP__KL_mbx_pkg.dtor();
}
