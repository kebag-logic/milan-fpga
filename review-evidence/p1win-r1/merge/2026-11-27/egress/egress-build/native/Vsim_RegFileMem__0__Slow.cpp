// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_RegFileMem___ctor_var_reset(Vsim_RegFileMem* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vsim_RegFileMem___ctor_var_reset\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__PVT__io_writes_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4398047383820645312ull);
    vlSelf->__PVT__io_writes_0_address = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11252921136554600944ull);
    vlSelf->__PVT__io_writes_0_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2421658671621477650ull);
    vlSelf->__PVT__io_writes_0_uopId = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7589194838319044890ull);
    vlSelf->__PVT__io_reads_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7278703588779709614ull);
    vlSelf->__PVT__io_reads_0_address = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6309745243976816700ull);
    vlSelf->__PVT__io_reads_0_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8449990240452176861ull);
    vlSelf->__PVT__io_reads_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10914792305623475356ull);
    vlSelf->__PVT__io_reads_1_address = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12178529984363086585ull);
    vlSelf->__PVT__io_reads_1_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16204873623468405564ull);
    vlSelf->__PVT__litex_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7160073992957751673ull);
    vlSelf->__PVT__cpuResetCtrl_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3165815507858932020ull);
    vlSelf->__PVT__asMem_ram_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11609174921076594940ull);
    vlSelf->__PVT__asMem_ram_spinal_port2 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11569083151025639419ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->asMem_ram[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10073441719044316491ull);
    }
}
