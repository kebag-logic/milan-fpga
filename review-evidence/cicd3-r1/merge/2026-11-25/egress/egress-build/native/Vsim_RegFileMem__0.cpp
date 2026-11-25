// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_RegFileMem___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga__0(Vsim_RegFileMem* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+            Vsim_RegFileMem___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VdlyVal__asMem_ram__v0;
    __VdlyVal__asMem_ram__v0 = 0;
    CData/*4:0*/ __VdlyDim0__asMem_ram__v0;
    __VdlyDim0__asMem_ram__v0 = 0;
    CData/*0:0*/ __VdlySet__asMem_ram__v0;
    __VdlySet__asMem_ram__v0 = 0;
    // Body
    __VdlySet__asMem_ram__v0 = 0U;
    if ((1U & ((~ ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__integer_RegFilePlugin_logic_initalizer_counter) 
                   >> 5U)) | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__lane0_integer_WriteBackPlugin_logic_write_port_valid)))) {
        __VdlyVal__asMem_ram__v0 = (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_down_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
                                    & (- (IData)((1U 
                                                  & ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__integer_RegFilePlugin_logic_initalizer_counter) 
                                                     >> 5U)))));
        __VdlyDim0__asMem_ram__v0 = (0x0000001fU & 
                                     ((0x00000020U 
                                       & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__integer_RegFilePlugin_logic_initalizer_counter))
                                       ? (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_up_RD_PHYS_lane0)
                                       : (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__integer_RegFilePlugin_logic_initalizer_counter)));
        __VdlySet__asMem_ram__v0 = 1U;
    }
    if ((1U & (~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__asMem_ram_spinal_port1 = vlSelfRef.asMem_ram
            [(0x0000001fU & (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                             >> 0x0000000fU))];
        vlSelfRef.__PVT__asMem_ram_spinal_port2 = vlSelfRef.asMem_ram
            [(0x0000001fU & (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                             >> 0x00000014U))];
    }
    if (__VdlySet__asMem_ram__v0) {
        vlSelfRef.asMem_ram[__VdlyDim0__asMem_ram__v0] 
            = __VdlyVal__asMem_ram__v0;
    }
}
