// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__61(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__61\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__litex_reset = (((IData)(vlSymsp->TOP.sys_reset) 
                                     | (IData)(vlSymsp->TOP__sim.__PVT__soc_soc_rst)) 
                                    | ((IData)(vlSymsp->TOP__sim.__PVT__soc_reset_storage) 
                                       >> 1U));
    vlSelfRef.__PVT__dma_bus_rready = ((IData)(vlSymsp->TOP__sim.__VdfgRegularize_h6e95ff9d_0_101) 
                                       & (6U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r)));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_106 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready) 
                                                  & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid) 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests)));
    vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready)));
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_halfPipe_fire 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready) 
           & (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__62(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__62\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1 
        = ((0x40U != (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter)) 
           || (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_0));
    vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_0 
        = (0x40U != (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__dma_bus_wready = ((~ (IData)(vlSelfRef.__PVT__litex_reset)) 
                                       & (IData)(vlSelfRef.__PVT__dma_bus_w_rValidN));
    vlSelfRef.__PVT__dma_bus_awready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_aw_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
    vlSelfRef.__PVT__dma_bus_arready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_ar_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
    vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__dma_bus_rready)));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__63(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__63\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter 
        = vlSelfRef.__Vdly__cpuResetCtrl_fiber_holder_counter;
}
