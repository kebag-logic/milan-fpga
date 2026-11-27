// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__FetchL1Plugin_logic_plru_mem__v0 = 0U;
    vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_0_mem__v0 = 0U;
    vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_1_mem__v0 = 0U;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_ways_0_mem__v0 = 0U;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loadedCounter 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 = 0U;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 = 0U;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 = 0U;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 = 0U;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA;
    vlSelfRef.__VdlySet__CsrRamPlugin_logic_mem__v0 = 0U;
    vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_0_mem__v0 = 0U;
    vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_1_mem__v0 = 0U;
    vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter 
        = vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__counter;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 = 0U;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_shared_mem__v0 = 0U;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_timer_counter 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty;
    vlSelfRef.__VdlySet__LsuL1Plugin_logic_writeback_victimBuffer__v0 = 0U;
    if (vlSelfRef.__PVT___zz_4) {
        vlSelfRef.__VdlyVal__FetchL1Plugin_logic_plru_mem__v0 
            = vlSelfRef.__PVT__fetch_logic_ctrls_0_down_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0;
        vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_plru_mem__v0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_plru_write_payload_address;
        vlSelfRef.__VdlySet__FetchL1Plugin_logic_plru_mem__v0 = 1U;
    }
    if ((1U & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask))) {
        vlSelfRef.__VdlyVal__FetchL1Plugin_logic_ways_0_mem__v0 
            = vlSelfRef.__PVT___zz_FetchL1Plugin_logic_ways_0_mem_port;
        vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_ways_0_mem__v0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address;
        vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_0_mem__v0 = 1U;
    }
}

extern const VlUnpacked<CData/*0:0*/, 512> Vsim__ConstPool__TABLE_h5eb9ad86_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((2U & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask))) {
        vlSelfRef.__VdlyVal__FetchL1Plugin_logic_ways_1_mem__v0 
            = vlSelfRef.__PVT___zz_FetchL1Plugin_logic_ways_0_mem_port;
        vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_ways_1_mem__v0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address;
        vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_1_mem__v0 = 1U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask) {
        vlSelfRef.__VdlyVal__LsuL1Plugin_logic_ways_0_mem__v0 
            = ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique) 
                 << 0x00000015U) | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_fault) 
                                    << 0x00000014U)) 
               | ((vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_address 
                   << 1U) | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded)));
        vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_ways_0_mem__v0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address;
        vlSelfRef.__VdlySet__LsuL1Plugin_logic_ways_0_mem__v0 = 1U;
    }
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loadedCounter 
        = (1U & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter) 
                 + (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loaded) 
                     & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter))) 
                    & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze)))));
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))) {
        vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loadedCounter = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_mask) {
        if ((1U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask))) {
            vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 
                = (0x000000ffU & vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData);
            vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address;
            vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 = 1U;
        }
        if ((2U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask))) {
            vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 
                = (0x000000ffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData 
                                  >> 8U));
            vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address;
            vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 = 1U;
        }
        if ((4U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask))) {
            vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 
                = (0x000000ffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData 
                                  >> 0x10U));
            vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address;
            vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 = 1U;
        }
        if ((8U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask))) {
            vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 
                = (vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData 
                   >> 0x18U);
            vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address;
            vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 = 1U;
        }
    }
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA 
        = ((IData)(vlSelfRef.__PVT__when_LsuL1Bus_l235)
            ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_PROBE_DATA)
            : (6U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_opcode)));
    if (vlSelfRef.__PVT___zz_3) {
        vlSelfRef.__VdlyVal__CsrRamPlugin_logic_mem__v0 
            = ((vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                & (- (IData)((1U & ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked) 
                                    >> 1U))))) | (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data 
                                                  & (- (IData)(
                                                               (1U 
                                                                & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked))))));
        vlSelfRef.__VdlyDim0__CsrRamPlugin_logic_mem__v0 
            = (3U & (((0x00000240U >> ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                                       << 1U)) & (- (IData)(
                                                            (1U 
                                                             & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked))))) 
                     | (((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                         & (- (IData)((1U & ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked) 
                                             >> 2U))))) 
                        | ((IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_address) 
                           & (- (IData)((1U & ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked) 
                                               >> 1U))))))));
        vlSelfRef.__VdlySet__CsrRamPlugin_logic_mem__v0 = 1U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_wayToAllocate)) 
         & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid))) {
        vlSelfRef.__VdlyVal__FetchL1Plugin_logic_banks_0_mem__v0 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_data;
        vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_banks_0_mem__v0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_write_payload_address;
        vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_0_mem__v0 = 1U;
    }
    if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid) 
         & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_wayToAllocate))) {
        vlSelfRef.__VdlyVal__FetchL1Plugin_logic_banks_1_mem__v0 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_data;
        vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_banks_1_mem__v0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_write_payload_address;
        vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_1_mem__v0 = 1U;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done)))) {
        vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter 
            = (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__counter)));
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result 
            = (vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result 
               << 1U);
        if ((1U & (~ (IData)((vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sub1 
                              >> 0x00000021U))))) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result 
                = (1U | vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result);
        }
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
            = (vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
               << 1U);
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy)))) {
        if ((3U == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))) {
            vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter = 0U;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
                = vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0;
        } else if ((2U == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))) {
            vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter = 8U;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
                = (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                   << 8U);
        } else if ((1U == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))) {
            vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter = 0x10U;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
                = (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                   << 0x00000010U);
        } else {
            vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter = 0x18U;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
                = (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                   << 0x00000018U);
        }
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result 
            = ((0U == vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0)
                ? 0xffffffffU : 0U);
    }
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_SHARED;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_UNIQUE;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram_wr_en) {
        vlSelfRef.__VdlyVal__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 
            = (((QData)((IData)(((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA) 
                                   << 4U) | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo) 
                                              << 3U) 
                                             | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_PROBE_DATA) 
                                                << 2U))) 
                                 | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE) 
                                     << 1U) | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED))))) 
                << 0x00000024U) | (((QData)((IData)(
                                                    ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT) 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)) 
                                                      << 1U) 
                                                     | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT) 
                                                        & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)) 
                                                           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED)))))) 
                                    << 0x00000022U) 
                                   | (((QData)((IData)(
                                                       ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE)) 
                                                        & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT)))) 
                                       << 0x00000021U) 
                                      | (((QData)((IData)(
                                                          ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT) 
                                                           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE)))) 
                                          << 0x00000020U) 
                                         | (QData)((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS))))));
        vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 
            = (1U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push));
        vlSelfRef.__VdlySet__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 = 1U;
    }
    if (Vsim__ConstPool__TABLE_h5eb9ad86_0[(((((4U 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                                                     >> 7U)) 
                                                   << 2U)) 
                                               | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                   << 1U) 
                                                  | (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168))) 
                                              << 6U) 
                                             | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                 << 5U) 
                                                | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                                   << 4U))) 
                                            | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                                                << 3U) 
                                               | ((((~ 
                                                     ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                                      | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))) 
                                                    & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)) 
                                                   << 2U) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))]) {
        vlSelfRef.__VdlyVal__LsuL1Plugin_logic_shared_mem__v0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty;
        vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_shared_mem__v0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address;
        vlSelfRef.__VdlySet__LsuL1Plugin_logic_shared_mem__v0 = 1U;
    }
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_timer_counter 
        = (1U & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter) 
                 + ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter)) 
                    & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze)))));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid)))) {
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_timer_counter = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty;
    }
    if (((6U != (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer)) 
         & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer 
            = (7U & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer) 
                     + (1U & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze)) 
                              | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent)))));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_valid) {
        vlSelfRef.__VdlyVal__LsuL1Plugin_logic_writeback_victimBuffer__v0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_rd_data;
        vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_writeback_victimBuffer__v0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_payload_wordIndex;
        vlSelfRef.__VdlySet__LsuL1Plugin_logic_writeback_victimBuffer__v0 = 1U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_DIRTY 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_DIRTY;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_last 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_last;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_victimBuffer_spinal_port1 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_victimBuffer
            [vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_wordIndex];
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_dirty 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty;
    }
    if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_down_valid) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_tval 
            = (IData)((vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception 
                       >> 1U));
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem_spinal_port2 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem
            [(0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
                             >> 6U))];
    }
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapCodeReg 
        = vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trapCode;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALUE_dirty 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SHARED_dirty 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_SHARED_dirty;
    if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
        vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_RAW_0 
            = ((0xffff0000U & (vlSelfRef.__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0 
                               & ((- (IData)((3U == 
                                              (3U & vlSelfRef.__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0)))) 
                                  << 0x00000010U))) 
               | (0x0000ffffU & vlSelfRef.__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HITS 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT;
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid 
        = ((IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id_1)
            ? (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid)
            : (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_2_valid));
}

extern const VlUnpacked<CData/*0:0*/, 32> Vsim__ConstPool__TABLE_h19c9bdaa_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_BYPASS_TRANSLATION = 1U;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_1_mem_spinal_port1;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_0 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_mem_spinal_port1;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_PAGE_FAULT = 0U;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_ACCESS_FAULT = 0U;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_REFILL = 0U;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_HAZARD = 0U;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HIT 
            = ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_0) 
               | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_1));
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_0 
            = vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_0;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_PC_FAULT 
            = vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_PC_FAULT;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_1_error 
            = (1U & (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem_spinal_port1 
                     >> 1U));
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_0_error 
            = (1U & (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem_spinal_port1 
                     >> 1U));
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_HAZARD 
            = ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE) 
               & ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE_ADDRESS) 
                  == (0x0000007fU & (vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC 
                                     >> 6U))));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_FAULT 
        = ((vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 
            >> 0x00000014U) & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT));
    if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
        vlSelfRef.__PVT__decode_ctrls_1_up_Decode_DECOMPRESSION_FAULT_0 = 0U;
        vlSelfRef.__PVT__decode_ctrls_1_up_TRAP_0 = vlSelfRef.__PVT__decode_ctrls_0_down_TRAP_0;
    }
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                      >> 2U)))) {
            if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_triggerEbreakReg = 0U;
                }
            }
        }
    }
    if (Vsim__ConstPool__TABLE_h19c9bdaa_0[(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh) 
                                             << 4U) 
                                            | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))]) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_targetPrivilege 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_privilege;
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_code 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id;
    }
    if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_down_valid) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_exception 
            = (1U & (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception));
    }
    vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_address 
        = (0x0000007fU & (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_WORD_PC 
                          >> 6U));
    vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_data_0 
        = vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_1;
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapReg 
        = vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap;
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_ACCESS_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl5_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_down_lane0_integer_WriteBackPlugin_logic_DATA_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_MMU_BYPASS_TRANSLATION_lane0 = 1U;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_FAILURE_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_2_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_MAY_FLUSH_PRECISE_3_lane0 
            = vlSelfRef.__PVT___zz_execute_ctrl1_down_AguPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_CLEAN_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_CLEAN_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_INVALID_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_INVALID_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_FROM_LSU_MSB_FAILED_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_MMU_REFILL_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_PAGE_FAULT_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_MMU_ACCESS_FAULT_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_MMU_HAZARD_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_RSP_lane0_fault 
            = vlSelfRef.__PVT__execute_ctrl3_down_LsuPlugin_logic_onPma_IO_RSP_lane0_fault;
        vlSelfRef.__PVT__execute_ctrl3_up_BYPASSED_AT_3_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_3_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_TRAP_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_TRAP_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onTrigger_HIT_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl1_up_RS2_PHYS_lane0 
            = (0x0000001fU & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                              >> 0x00000014U));
        vlSelfRef.__PVT__execute_ctrl1_up_RS1_PHYS_lane0 
            = (0x0000001fU & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                              >> 0x0000000fU));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_address 
            = (0x0007ffffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
                              >> 1U));
        vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_FLOAT_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_FLOAT_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_integer_RS2_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_BYPASSED_AT_4_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_BYPASSED_AT_4_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_PREFETCH_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PREFETCH_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_PREFETCH_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_Decode_UOP_ID_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_Decode_UOP_ID_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_BarrelShifterPlugin_SIGNED_lane0 
            = (0x40000000U == (0x40000000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_CLEAR_lane0 
            = (0x00001000U == (0x00001000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_IMM_lane0 
            = (0x00004000U == (0x00004000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_1_lane0 
            = (0x0000001fU & ((7U & (IData)((vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_2_lane0 
                                             >> 0x0000002cU))) 
                              + ((7U & (IData)((vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_1_lane0 
                                                >> 0x0000002cU))) 
                                 + (7U & (vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_3_lane0 
                                          >> 0x0000001bU)))));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0 
            = (((0x10000000U == (0x30001000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                << 2U) | ((((0U == (0x00000040U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                            | (0x20000000U == (0x20000000U 
                                               & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))) 
                           << 1U) | ((0U == (0x00000040U 
                                             & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                                     | (0x00100000U 
                                        == (0x00100000U 
                                            & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)))));
        vlSelfRef.__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS1_SIGNED_lane0 
            = ((0U == (0x00001000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | (0U == (0x00006000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid)))) {
        vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_data 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_data;
        vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_error 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_denied;
    }
    if ((1U & ((0x0120U >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)) 
               & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg)))) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_readed 
            = vlSelfRef.__PVT__CsrRamPlugin_logic_mem_spinal_port1;
    }
    if ((1U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_aluInput 
            = vlSelfRef.__PVT__CsrAccessPlugin_bus_read_toWriteBits;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy)))) {
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__div1 
            = (QData)((IData)(vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0));
    }
    if (vlSelfRef.__PVT__when_FetchL1Plugin_l256) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid)))) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                = vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED;
        }
    }
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                vlSelfRef.__PVT__REG_CSR_CsrRamPlugin_csrMapper_selFilter 
                    = vlSelfRef.__PVT__COMB_CSR_CsrRamPlugin_csrMapper_selFilter;
            }
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_cmdSent = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_oh) {
        if ((1U & (~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid)))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_cmdSent = 1U;
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_LOCK_HIT = 0U;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_FORCE_HAZARD 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_FORCE_HAZARD;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SET_HAZARD 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_SET_HAZARD) 
           | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask) 
              & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address) 
                 == (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
                                    >> 6U)))));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_ATOMIC_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_ATOMIC_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique 
            = (1U & (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
                     >> 0x00000015U));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault 
            = (1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21)));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_FLUSH_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_COMMIT_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_COMMIT_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_UNSIGNED_lane0 
            = ((0x00002000U == (0x00002010U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | (0x00001000U == (0x00005000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_ZERO_lane0 
            = (0x00000024U == (0x00000024U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_SIGNED_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & ((0x00001008U == (0x00001048U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | (0x00000050U == (0x00003050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))));
        vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_MulPlugin_HIGH_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_MulPlugin_HIGH_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_STORE_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_STORE_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault 
            = (1U & (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
                     >> 0x00000014U));
        vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0 
            = (((4U == (0x0000000cU & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                << 1U) | (8U == (8U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_REVERT_lane0 
            = ((0x00000040U == (0x00000040U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | ((0x00002010U == (0x00002014U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | (0x40000030U == (0x40000034U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))));
        vlSelfRef.__PVT__execute_ctrl5_up_RD_PHYS_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_up_RD_PHYS_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FENCE_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FENCE_lane0;
        vlSelfRef.__PVT__execute_ctrl5_up_RD_ENABLE_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_up_RD_ENABLE_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_0_lane0 
            = (0x7fffffffffffffffULL & ((0x1ffffffffffe0000ULL 
                                         & (vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_2_lane0 
                                            << 0x00000011U)) 
                                        + ((0x1ffffffffffe0000ULL 
                                            & (vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_1_lane0 
                                               << 0x00000011U)) 
                                           + (((QData)((IData)(
                                                               (0x07ffffffU 
                                                                & vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_3_lane0))) 
                                               << 0x00000022U) 
                                              | vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_0_lane0))));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_lane0 
            = (1U & (~ ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21) 
                        | ((IData)(vlSelfRef.__PVT__execute_ctrl3_down_LsuPlugin_logic_onPma_IO_RSP_lane0_fault) 
                           | ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FENCE_lane0) 
                              | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_PREFETCH_lane0))))));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_LOAD_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_LOAD_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0 
            = (((2U == (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0)) 
                & (0U != (3U & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0))) 
               | ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0)) 
                  & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done)))) {
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifter 
            = (IData)((0x00000001ffffffffULL & ((1U 
                                                 & (IData)(
                                                           (vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sub1 
                                                            >> 0x00000021U)))
                                                 ? vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifted
                                                 : vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sub1)));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy)))) {
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifter 
            = ((3U == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))
                ? 0U : ((2U == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))
                         ? (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                            >> 0x00000018U) : ((1U 
                                                == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel))
                                                ? (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                                                   >> 0x00000010U)
                                                : (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                                                   >> 8U))));
    }
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_write 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0) 
            & (~ (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
           & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_write));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_jumpTarget 
        = (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_pc 
           + (((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_slices) 
               & ((8U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)) 
                  | ((6U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)) 
                     | ((2U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)) 
                        | (5U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))))) 
              << 2U));
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                vlSelfRef.__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_epcFilter 
                    = (0x0341U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                   >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_tvecFilter 
                    = (0x0305U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                   >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_4016 = (0x0fb0U 
                                                 == 
                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_3858 = (0x0f12U 
                                                 == 
                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_769 = (0x0301U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_836 = (0x0344U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_3073 = (0x0c01U 
                                                 == 
                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_3201 = (0x0c81U 
                                                 == 
                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U));
            }
        }
    }
    if (((IData)(vlSelfRef.__PVT__REG_CSR_774) & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo))) {
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_mcounteren_tm 
            = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                     >> 1U));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_TAG_UPDATE 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_SHARED)) 
                 | ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_UNIQUE)) 
                    & (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_UNIQUE))));
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_read 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0) 
            & (~ (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_ENABLE_lane0) 
              | (IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_MASK_lane0)));
}

extern const VlUnpacked<CData/*0:0*/, 512> Vsim__ConstPool__TABLE_hcaf816ea_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALID 
        = (Vsim__ConstPool__TABLE_h5eb9ad86_0[(((((4U 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                                                        >> 7U)) 
                                                      << 2U)) 
                                                  | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                      << 1U) 
                                                     | (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168))) 
                                                 << 6U) 
                                                | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                    << 5U) 
                                                   | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                                      << 4U))) 
                                               | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                                                   << 3U) 
                                                  | ((((~ 
                                                        ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                                         | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))) 
                                                       & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)) 
                                                      << 2U) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))] 
           & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address) 
              == (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
                                 >> 6U))));
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WRITE_TO_READ_HAZARDS_lane0 
            = ((((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0) 
                 & ((0U != ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MASK_lane0) 
                            & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_MASK_lane0))) 
                    & ((vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                        >> 2U) == (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_ADDRESS_lane0 
                                   >> 2U)))) << 1U) 
               | ((IData)(vlSelfRef.__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0) 
                  & (((vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 
                       >> 2U) == (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                                  >> 2U)) & (0U != 
                                             ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MASK_lane0) 
                                              & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MASK_lane0))))));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_SHARED_lane0_dirty 
            = ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address) 
                 == (0x0000007fU & (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                                    >> 6U))) & Vsim__ConstPool__TABLE_h5eb9ad86_0
                [(((((4U & ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                                >> 7U)) << 2U)) | (
                                                   ((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168))) 
                    << 6U) | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                               << 5U) | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                         << 4U))) | 
                  (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                    << 3U) | ((((~ ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                    | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))) 
                                & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)) 
                               << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))])
                ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty)
                : ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALID_lane0)
                    ? (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALUE_lane0_dirty)
                    : (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem_spinal_port1)));
        vlSelfRef.__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
            = (vlSelfRef.__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
               | ((- (IData)(((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0) 
                              & ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_early0_DivPlugin_SEL_lane0) 
                                 | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_CsrAccessPlugin_SEL_lane0))))) 
                  & ((vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_csrValue 
                      & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl3_up_CsrAccessPlugin_SEL_lane0)))) 
                     | (vlSelfRef.__PVT__execute_ctrl3_up_DivPlugin_DIV_RESULT_lane0 
                        & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl3_up_early0_DivPlugin_SEL_lane0)))))));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANK_BUSY_REMAPPED_lane0 
            = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_rb1_onBanks_0_busyReg) 
               | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_BANK_BUSY_lane0));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0 
            = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state) 
               | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0 
            = ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0) 
               | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_persistance) 
                  | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_hit)));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANKS_MUXES_lane0_0 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_rd_data;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_locked)))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_lockedOh 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_askCmd;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_writeCmdDone = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_readCmdDone 
            = (1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty)));
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_victimBufferReady 
            = (1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty)));
    }
    if (vlSelfRef.__PVT__when_LsuL1Plugin_l679) {
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_oh) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_writeCmdDone = 1U;
        }
    }
    if (vlSelfRef.__PVT__when_LsuL1Plugin_l608) {
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_oh) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_readCmdDone = 1U;
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_fromUnique;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toShared;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_release 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_release;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toUnique;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_address 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_address;
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_victim 
            = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded) 
               & ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid) 
                      | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_askUpgrade))) 
                  & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties)));
    }
    if (vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_victim = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_valid) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_victimBufferReady = 1U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_WB_HAZARD 
        = (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid) 
            & ((0x00007fffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_address 
                               >> 6U)) == (0x00007fffU 
                                           & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
                                              >> 6U)))) 
           | (Vsim__ConstPool__TABLE_hcaf816ea_0[((
                                                   ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA) 
                                                      << 4U) 
                                                     | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                         << 3U) 
                                                        | ((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168) 
                                                           << 2U))) 
                                                    | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                        << 1U) 
                                                       | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid))) 
                                                   << 4U) 
                                                  | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                                                      << 3U) 
                                                     | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded) 
                                                         << 2U) 
                                                        | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))] 
              & ((0x00007fffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
                                 >> 6U)) == (0x00007fffU 
                                             & (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address 
                                                >> 6U)))));
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0] 
            = vlSelfRef.__VdlyVal__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0;
    }
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_writeback_victimBuffer__v0) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_victimBuffer[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_writeback_victimBuffer__v0] 
            = vlSelfRef.__VdlyVal__LsuL1Plugin_logic_writeback_victimBuffer__v0;
    }
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__when_FetchL1Plugin_l256) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid)))) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_wayToAllocate 
                = (1U & (~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_PLRU_BYPASSED_0)));
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_PROBE_DATA 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_payload_wordIndex 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem
            [(0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
                             >> 6U))];
    }
    if (vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_banks_1_mem_spinal_port1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_1_mem
            [(0x000007ffU & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                             >> 2U))];
        vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_mem_spinal_port1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_mem
            [(0x000007ffU & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                             >> 2U))];
        vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem_spinal_port1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem
            [(0x0000007fU & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                             >> 6U))];
    }
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_privilege = 3U;
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_PC_FAULT 
            = vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_fault;
    }
}

extern const VlUnpacked<CData/*0:0*/, 512> Vsim__ConstPool__TABLE_h5879e089_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlWide<3>/*95:0*/ __Vtemp_2;
    VlWide<3>/*95:0*/ __Vtemp_3;
    VlWide<3>/*95:0*/ __Vtemp_4;
    // Body
    if (vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem_spinal_port1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem
            [(0x0000007fU & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                             >> 6U))];
    }
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id 
        = ((IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id_1)
            ? ((IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_1_valid)
                ? 3U : 7U) : 0x0bU);
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_1 
            = vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_1;
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED 
            = vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC;
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE_ADDRESS 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address;
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE 
            = (0U != (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask));
    }
    if (vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_port_cmd_valid) {
        vlSelfRef.__PVT__CsrRamPlugin_logic_mem_spinal_port1 
            = vlSelfRef.__PVT__CsrRamPlugin_logic_mem
            [(3U & ((2U & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits_ohFirst_masked))
                     ? (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_address)
                     : (0x00010c00U >> ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                                        << 1U))))];
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_CLEAN_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_INVALID_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_3_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_TRAP_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass;
        vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_FLOAT_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_FLOAT_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_integer_RS2_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_BYPASSED_AT_4_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_4_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_PREFETCH_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_Decode_UOP_ID_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_ID_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_ATOMIC_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_ATOMIC_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_FLUSH_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_COMMIT_lane0 
            = Vsim__ConstPool__TABLE_h5879e089_0[(((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77) 
                                                   << 4U) 
                                                  | ((((IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid) 
                                                       << 3U) 
                                                      | (4U 
                                                         & ((~ (IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_commit)) 
                                                            << 2U))) 
                                                     | (((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid) 
                                                         << 1U) 
                                                        | (1U 
                                                           & (~ (IData)(vlSelfRef.__PVT__execute_ctrl2_up_TRAP_lane0))))))];
        vlSelfRef.__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_SIGNED_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_MulPlugin_HIGH_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_MulPlugin_HIGH_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_AguPlugin_STORE_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_STORE_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_lane0_integer_WriteBackPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_early0_MulPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_RD_ENABLE_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid)) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_RD_ENABLE_lane0));
        vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_2_lane0 
            = (((QData)((IData)((0x00001fffU & (- (IData)(
                                                          (1U 
                                                           & (IData)(
                                                                     (vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_1 
                                                                      >> 0x00000021U)))))))) 
                << 0x00000022U) | vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_1);
        vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_1_lane0 
            = (((QData)((IData)((0x00001fffU & (- (IData)(
                                                          (1U 
                                                           & (IData)(
                                                                     (vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_1 
                                                                      >> 0x00000021U)))))))) 
                << 0x00000022U) | vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_1);
        vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_3_lane0 
            = (0x3fffffffU & VL_MULS_III(32, VL_EXTENDS_II(32,16, (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_2)), 
                                         VL_EXTENDS_II(32,16, (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_3))));
        vlSelfRef.__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_0_lane0 
            = (0x00000003ffffffffULL & ((QData)((IData)(
                                                        (0x0001ffffU 
                                                         & vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0))) 
                                        * (QData)((IData)(
                                                          (0x0001ffffU 
                                                           & vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0)))));
        vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_PREFETCH_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FENCE_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_LsuPlugin_logic_FENCE_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_LOAD_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_LOAD_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_MASK_lane0 
            = (0x00002000U == (0x00002000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_MASK_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MASK_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_ADDRESS_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALUE_lane0_dirty 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty;
        vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem_spinal_port1 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem
            [(0x0000007fU & (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                             >> 6U))];
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALID_lane0 
            = (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address) 
                == (0x0000007fU & (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                                   >> 6U))) & Vsim__ConstPool__TABLE_h5eb9ad86_0
               [(((((4U & ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                               >> 7U)) << 2U)) | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                   << 1U) 
                                                  | (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168))) 
                   << 6U) | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                              << 5U) | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                        << 4U))) | 
                 (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                   << 3U) | ((((~ ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                   | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))) 
                               & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)) 
                              << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))]);
        vlSelfRef.__PVT__execute_ctrl3_up_early0_DivPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_early0_DivPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_CsrAccessPlugin_SEL_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_DivPlugin_DIV_RESULT_lane0 
            = (((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_divRevertResult)
                 ? (~ vlSelfRef.__PVT__early0_DivPlugin_logic_processing_selected)
                 : vlSelfRef.__PVT__early0_DivPlugin_logic_processing_selected) 
               + (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_divRevertResult));
        vlSelfRef.__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
            = ((((IData)(4U) + vlSelfRef.__PVT__execute_ctrl2_up_PC_lane0) 
                & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_BranchPlugin_SEL_lane0)))) 
               | ((- (IData)(((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                              & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_SEL_lane0) 
                                 | (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_BarrelShifterPlugin_SEL_lane0))))) 
                  & ((((IData)(vlSelfRef.__PVT__execute_ctrl2_up_BarrelShifterPlugin_LEFT_lane0)
                        ? ((((((((2U & ((IData)(vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted) 
                                        << 1U)) | (1U 
                                                   & (IData)(
                                                             (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                              >> 1U)))) 
                                << 6U) | (((2U & ((IData)(
                                                          (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                           >> 2U)) 
                                                  << 1U)) 
                                           | (1U & (IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 3U)))) 
                                          << 4U)) | 
                              ((((2U & ((IData)((vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                 >> 4U)) 
                                        << 1U)) | (1U 
                                                   & (IData)(
                                                             (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                              >> 5U)))) 
                                << 2U) | ((2U & ((IData)(
                                                         (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                          >> 6U)) 
                                                 << 1U)) 
                                          | (1U & (IData)(
                                                          (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                           >> 7U)))))) 
                             << 0x00000018U) | ((((
                                                   ((2U 
                                                     & ((IData)(
                                                                (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                 >> 8U)) 
                                                        << 1U)) 
                                                    | (1U 
                                                       & (IData)(
                                                                 (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                  >> 9U)))) 
                                                   << 6U) 
                                                  | (((2U 
                                                       & ((IData)(
                                                                  (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                   >> 0x0000000aU)) 
                                                          << 1U)) 
                                                      | (1U 
                                                         & (IData)(
                                                                   (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                    >> 0x0000000bU)))) 
                                                     << 4U)) 
                                                 | ((((2U 
                                                       & ((IData)(
                                                                  (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                   >> 0x0000000cU)) 
                                                          << 1U)) 
                                                      | (1U 
                                                         & (IData)(
                                                                   (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                    >> 0x0000000dU)))) 
                                                     << 2U) 
                                                    | ((2U 
                                                        & ((IData)(
                                                                   (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                    >> 0x0000000eU)) 
                                                           << 1U)) 
                                                       | (1U 
                                                          & (IData)(
                                                                    (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                                     >> 0x0000000fU)))))) 
                                                << 0x00000010U)) 
                           | (((((((2U & ((IData)((vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                   >> 0x00000010U)) 
                                          << 1U)) | 
                                   (1U & (IData)((vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                  >> 0x00000011U)))) 
                                  << 6U) | (((2U & 
                                              ((IData)(
                                                       (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                        >> 0x00000012U)) 
                                               << 1U)) 
                                             | (1U 
                                                & (IData)(
                                                          (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                           >> 0x00000013U)))) 
                                            << 4U)) 
                                | ((((2U & ((IData)(
                                                    (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                     >> 0x00000014U)) 
                                            << 1U)) 
                                     | (1U & (IData)(
                                                     (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                      >> 0x00000015U)))) 
                                    << 2U) | ((2U & 
                                               ((IData)(
                                                        (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                         >> 0x00000016U)) 
                                                << 1U)) 
                                              | (1U 
                                                 & (IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 0x00000017U)))))) 
                               << 8U) | (((((2U & ((IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 0x00000018U)) 
                                                   << 1U)) 
                                            | (1U & (IData)(
                                                            (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                             >> 0x00000019U)))) 
                                           << 6U) | 
                                          (((2U & ((IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 0x0000001aU)) 
                                                   << 1U)) 
                                            | (1U & (IData)(
                                                            (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                             >> 0x0000001bU)))) 
                                           << 4U)) 
                                         | ((((2U & 
                                               ((IData)(
                                                        (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                         >> 0x0000001cU)) 
                                                << 1U)) 
                                              | (1U 
                                                 & (IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 0x0000001dU)))) 
                                             << 2U) 
                                            | ((2U 
                                                & ((IData)(
                                                           (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                            >> 0x0000001eU)) 
                                                   << 1U)) 
                                               | (1U 
                                                  & (IData)(
                                                            (vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
                                                             >> 0x0000001fU))))))))
                        : (IData)(vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted)) 
                      & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_BarrelShifterPlugin_SEL_lane0)))) 
                     | ((- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_SEL_lane0))) 
                        & (((IData)(vlSelfRef.__PVT___zz_early0_IntAluPlugin_logic_alu_result_5) 
                            & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_SLTX_lane0)))) 
                           | (((2U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_BITWISE_CTRL_lane0))
                                ? (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                   & vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0)
                                : ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_BITWISE_CTRL_lane0))
                                    ? (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                       | vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0)
                                    : ((vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                        ^ vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0) 
                                       & (- (IData)(
                                                    (0U 
                                                     == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_BITWISE_CTRL_lane0))))))) 
                              | (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                                 & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_ADD_SUB_lane0))))))))));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_FORCE_HAZARD 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                    >> 7U)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_SET_HAZARD 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask) 
           & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address) 
              == (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
                                 >> 6U))));
    vlSelfRef.integer_write_0_uopId = vlSelfRef.__PVT__execute_ctrl4_up_Decode_UOP_ID_lane0;
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_pmaFault 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_RSP_lane0_fault));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifted 
        = (((QData)((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifter)) 
            << 1U) | (QData)((IData)((vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator 
                                      >> 0x0000001fU))));
    vlSelfRef.__PVT__LsuPlugin_logic_iwb_valid = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_FLOAT_lane0)) 
                                                  & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_SEL_lane0));
    if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_slices = 1U;
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_pc 
            = vlSelfRef.__PVT__execute_ctrl4_up_PC_lane0;
    }
    __Vtemp_2[0U] = (IData)(vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_0_lane0);
    __Vtemp_2[1U] = (IData)((vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_0_lane0 
                             >> 0x00000020U));
    __Vtemp_2[2U] = 0U;
    __Vtemp_3[0U] = 0U;
    __Vtemp_3[1U] = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_1_lane0) 
                     << 0x0000001dU);
    __Vtemp_3[2U] = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_1_lane0) 
                     >> 3U);
    VL_ADD_W(3, __Vtemp_4, __Vtemp_2, __Vtemp_3);
    vlSelfRef.__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0[0U] 
        = __Vtemp_4[0U];
    vlSelfRef.__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0[1U] 
        = __Vtemp_4[1U];
    vlSelfRef.__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0[2U] 
        = (3U & __Vtemp_4[2U]);
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                vlSelfRef.__PVT__REG_CSR_774 = (0x0306U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
            }
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_SHARED 
        = ((IData)(vlSelfRef.__PVT__when_LsuL1Bus_l235)
            ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED)
            : (2U != (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_param)));
    if ((1U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_csrValue 
            = vlSelfRef.__PVT__CsrAccessPlugin_bus_read_toWriteBits;
    }
}

extern const VlUnpacked<CData/*0:0*/, 64> Vsim__ConstPool__TABLE_h90f7dc7a_0;
extern const VlUnpacked<CData/*0:0*/, 256> Vsim__ConstPool__TABLE_h5901c4e5_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_BANK_BUSY_lane0 
            = vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0 
            = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect) 
               & ((0x0000007fU & (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                                  >> 6U)) == (0x0000007fU 
                                              & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                                                 >> 6U))));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_fromUnique 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toShared 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_release 
            = Vsim__ConstPool__TABLE_h90f7dc7a_0[vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78];
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toUnique 
            = Vsim__ConstPool__TABLE_h5901c4e5_0[(((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE) 
                                                   << 7U) 
                                                  | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE) 
                                                      << 6U) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78)))];
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)) 
               | (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_rd_data 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block
            [(0x000007ffU & ((IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1)
                              ? ((0x000007f0U & (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_address 
                                                 >> 2U)) 
                                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex))
                              : (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                                 >> 2U)))];
    }
    if (vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_1_mem__v0) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_banks_1_mem[vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_banks_1_mem__v0] 
            = vlSelfRef.__VdlyVal__FetchL1Plugin_logic_banks_1_mem__v0;
    }
    if (vlSelfRef.__VdlySet__FetchL1Plugin_logic_banks_0_mem__v0) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_mem[vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_banks_0_mem__v0] 
            = vlSelfRef.__VdlyVal__FetchL1Plugin_logic_banks_0_mem__v0;
    }
    if (vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_1_mem__v0) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem[vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_ways_1_mem__v0] 
            = vlSelfRef.__VdlyVal__FetchL1Plugin_logic_ways_1_mem__v0;
    }
    if (vlSelfRef.__VdlySet__FetchL1Plugin_logic_ways_0_mem__v0) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem[vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_ways_0_mem__v0] 
            = vlSelfRef.__VdlyVal__FetchL1Plugin_logic_ways_0_mem__v0;
    }
    if (vlSelfRef.__VdlySet__CsrRamPlugin_logic_mem__v0) {
        vlSelfRef.__PVT__CsrRamPlugin_logic_mem[vlSelfRef.__VdlyDim0__CsrRamPlugin_logic_mem__v0] 
            = vlSelfRef.__VdlyVal__CsrRamPlugin_logic_mem__v0;
    }
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sub1 
        = (0x00000003ffffffffULL & (vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifted 
                                    - vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__div1));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED;
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_shared_mem__v0) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_shared_mem__v0] 
            = vlSelfRef.__VdlyVal__LsuL1Plugin_logic_shared_mem__v0;
    }
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0] 
            = ((0xffffff00U & vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block
                [vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0]) 
               | (IData)(vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0));
    }
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1] 
            = ((0xffff00ffU & vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block
                [vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1]) 
               | ((IData)(vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1) 
                  << 8U));
    }
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2] 
            = ((0xff00ffffU & vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block
                [vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2]) 
               | ((IData)(vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3] 
            = ((0x00ffffffU & vlSelfRef.__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block
                [vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3]) 
               | ((IData)(vlSelfRef.__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3) 
                  << 0x00000018U));
    }
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_PLRU_BYPASSED_0 
            = ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_VALID)
                ? (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0)
                : (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_plru_mem_spinal_port1));
    }
    vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_topi_interrupt 
        = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id) 
           & (- (IData)((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid))));
    vlSelfRef.__PVT__when_FetchL1Plugin_l488 = (1U 
                                                & ((~ 
                                                    ((0U 
                                                      == 
                                                      (0xeffe0000U 
                                                       & vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED)) 
                                                     | ((0x00020000U 
                                                         == 
                                                         (0xefff0000U 
                                                          & vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED)) 
                                                        | (0x00030000U 
                                                           == 
                                                           (0xefff8000U 
                                                            & vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED))))) 
                                                   | ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_HAZARD)) 
                                                      & (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_1_error) 
                                                          & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_1)) 
                                                         | ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_0_error) 
                                                            & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_0))))));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_FLOAT_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_4_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_ID_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_ID_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_ATOMIC_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & (IData)(vlSelfRef.__PVT___zz_execute_ctrl1_down_AguPlugin_SEL_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_TRAP_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 
            = (0U == (0x00004010U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 
            = ((((0x00002000U == (0x00002000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                 | (0x00000010U == (0x00000010U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))) 
                << 1U) | (0x00001000U == (0x00001010U 
                                          & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_MulPlugin_HIGH_lane0 
            = ((0x00001000U == (0x00001000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | (0x00002000U == (0x00002000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_lane0_integer_WriteBackPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & ((4U == (0x0000000cU & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | ((0x00000048U == (0x00000048U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                     | ((0x00001010U == (0x00001010U 
                                         & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                        | ((0x00002010U == (0x00002010U 
                                            & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                           | ((0x00000010U == (0x00000050U 
                                               & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                              | (0U == (0x00000028U 
                                        & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))))))));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_MulPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & (0x02000030U == (0x02004074U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl4_up_PC_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_PC_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_RD_ENABLE_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid)) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_ENABLE_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_down_integer_RS1_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_LsuPlugin_logic_FENCE_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & (8U == (0x00001048U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_LOAD_lane0 
            = (0U == (0x00000028U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0 
            = (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
               & ((0x0007ffffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
                                  >> 1U)) == (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                                              >> 0x0000000dU)));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_DivPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & (0x02004020U == (0x02004064U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_SLTX_lane0 
            = (0x00002000U == (0x00006004U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_ADD_SUB_lane0 
            = ((0U == (0x00006000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | (4U == (4U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_BITWISE_CTRL_lane0 
            = ((((0x00001000U == (0x00001000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)) 
                << 1U) | ((0x00002000U == (0x00003000U 
                                           & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                          | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)));
        vlSelfRef.__PVT__execute_ctrl2_up_BarrelShifterPlugin_LEFT_lane0 
            = (0U == (0x00004000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_IntAluPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & ((0x00002010U == (0x00002030U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | ((4U == (0x0000004cU & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                     | ((0x00000010U == (0x00001030U 
                                         & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                        | ((0x00002010U == (0x02002050U 
                                            & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                           | (0x00000010U == (0x02001050U 
                                              & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)))))));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_BarrelShifterPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & ((0x00001010U == (0x00003034U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | (0x00001010U == (0x02003054U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_BranchPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & (0x00000040U == (0x00000050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
            = ((4U == (0x00000044U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))
                ? (0xfffff000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)
                : vlSelfRef.__PVT__execute_ctrl1_down_integer_RS1_lane0);
        vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0 
            = ((0U == (IData)(vlSelfRef.__PVT__execute_ctrl1_down_early0_SrcPlugin_logic_SRC2_CTRL_lane0))
                ? vlSelfRef.__PVT__execute_ctrl1_down_integer_RS2_lane0
                : ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl1_down_early0_SrcPlugin_logic_SRC2_CTRL_lane0))
                    ? (((- (IData)((vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
                                    >> 0x0000001fU))) 
                        << 0x0000000cU) | (vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
                                           >> 0x00000014U))
                    : ((2U == (IData)(vlSelfRef.__PVT__execute_ctrl1_down_early0_SrcPlugin_logic_SRC2_CTRL_lane0))
                        ? vlSelfRef.__PVT__execute_ctrl1_up_PC_lane0
                        : (((- (IData)((vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
                                        >> 0x0000001fU))) 
                            << 0x0000000cU) | ((0x00000fe0U 
                                                & (vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
                                                   >> 0x00000014U)) 
                                               | (0x0000001fU 
                                                  & (vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
                                                     >> 7U)))))));
    }
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_divRevertResult 
        = (((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1) 
            ^ ((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1) 
               & (~ (IData)(vlSelfRef.__PVT__execute_ctrl2_up_DivPlugin_REM_lane0)))) 
           & (~ (((0U == vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0) 
                  & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS2_SIGNED_lane0)) 
                 & (~ (IData)(vlSelfRef.__PVT__execute_ctrl2_up_DivPlugin_REM_lane0)))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE 
        = vlSelfRef.__PVT___zz_LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_UNIQUE;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_address 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address;
    }
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_plru_mem_spinal_port1 
            = vlSelfRef.__PVT__FetchL1Plugin_logic_plru_mem
            [(0x0000007fU & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                             >> 6U))];
    }
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0 
            = vlSelfRef.__PVT__fetch_logic_ctrls_0_down_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0;
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_VALID 
            = ((IData)(vlSelfRef.__PVT___zz_4) & ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_plru_write_payload_address) 
                                                  == 
                                                  (0x0000007fU 
                                                   & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                                                      >> 6U))));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_ID_lane0 
            = vlSelfRef.__PVT__DecoderPlugin_logic_harts_0_uopId;
        vlSelfRef.__PVT__execute_ctrl3_up_PC_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_PC_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_RD_ENABLE_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel)) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl1_up_RD_ENABLE_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_down_integer_RS2_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_DivPlugin_REM_lane0 
            = (0x00002000U == (0x00002000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS2_SIGNED_lane0 
            = ((0x00004000U == (0x00005000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
               | (0U == (0x00006000U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
        vlSelfRef.__PVT__execute_ctrl2_up_PC_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_PC_lane0;
        vlSelfRef.__PVT__execute_ctrl1_up_RD_ENABLE_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel)) 
               & ((~ ((~ (IData)(vlSelfRef.__PVT__execute_ctrl0_up_LANE_SEL_lane0)) 
                      | (IData)(vlSelfRef.__PVT__execute_ctrl0_down_COMPLETED_lane0))) 
                  & (((4U == (0x0000000cU & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                      | ((0x00000048U == (0x00000048U 
                                          & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                         | ((0x00001010U == (0x00001010U 
                                             & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                            | ((0x00002010U == (0x00002010U 
                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                               | ((0x00000010U == (0x00000050U 
                                                   & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                  | (0U == (0x00000028U 
                                            & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0))))))) 
                     & (0U != (0x0000001fU & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                              >> 7U))))));
    }
    vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS1_SIGNED_lane0) 
           & (vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0 
              >> 0x0000001fU));
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FAULT_lane0 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0) 
           & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0)) 
              & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault)));
    vlSelfRef.__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted 
        = (0x00000001ffffffffULL & VL_SHIFTRS_QQI(33,33,5, 
                                                  (((QData)((IData)(
                                                                    ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_BarrelShifterPlugin_SIGNED_lane0) 
                                                                     & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                        >> 0x0000001fU)))) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(
                                                                     ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_BarrelShifterPlugin_LEFT_lane0)
                                                                       ? 
                                                                      ((((((((2U 
                                                                              & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                << 1U)) 
                                                                             | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 1U))) 
                                                                            << 6U) 
                                                                           | (((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 1U)) 
                                                                               | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 3U))) 
                                                                              << 4U)) 
                                                                          | ((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 3U)) 
                                                                               | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 5U))) 
                                                                              << 2U) 
                                                                             | ((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 5U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 7U))))) 
                                                                         << 0x00000018U) 
                                                                        | ((((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 7U)) 
                                                                               | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 9U))) 
                                                                              << 6U) 
                                                                             | (((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 9U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000bU))) 
                                                                                << 4U)) 
                                                                            | ((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000bU)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000dU))) 
                                                                                << 2U) 
                                                                               | ((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000dU)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000fU))))) 
                                                                           << 0x00000010U)) 
                                                                       | (((((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000000fU)) 
                                                                               | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000011U))) 
                                                                              << 6U) 
                                                                             | (((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000011U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000013U))) 
                                                                                << 4U)) 
                                                                            | ((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000013U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000015U))) 
                                                                                << 2U) 
                                                                               | ((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000015U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000017U))))) 
                                                                           << 8U) 
                                                                          | (((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000017U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000019U))) 
                                                                               << 6U) 
                                                                              | (((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x00000019U)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000001bU))) 
                                                                                << 4U)) 
                                                                             | ((((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000001bU)) 
                                                                                | (1U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000001dU))) 
                                                                                << 2U) 
                                                                                | ((2U 
                                                                                & (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000001dU)) 
                                                                                | (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                                                                >> 0x0000001fU))))))
                                                                       : vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0)))), 
                                                  (0x0000001fU 
                                                   & vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0)));
    vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_alu_EQ_lane0 
        = (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
           == vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0);
    vlSelfRef.__PVT__early0_SrcPlugin_logic_addsub_combined_rs2Patched 
        = vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0;
    if (vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_REVERT_lane0) {
        vlSelfRef.__PVT__early0_SrcPlugin_logic_addsub_combined_rs2Patched 
            = (~ vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0);
    }
    if (vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_ZERO_lane0) {
        vlSelfRef.__PVT__early0_SrcPlugin_logic_addsub_combined_rs2Patched = 0U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS;
    if (vlSelfRef.__VdlySet__FetchL1Plugin_logic_plru_mem__v0) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_plru_mem[vlSelfRef.__VdlyDim0__FetchL1Plugin_logic_plru_mem__v0] 
            = vlSelfRef.__VdlyVal__FetchL1Plugin_logic_plru_mem__v0;
    }
    vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_2 
        = (((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1) 
            << 0x0000000fU) | (vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0 
                               >> 0x00000011U));
    vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
        = (((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1)
             ? (~ vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0)
             : vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0) 
           + (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_2 
        = (IData)((0U == (0xffff0000U & vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0)));
    vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_1 
        = (0x00000003ffffffffULL & VL_MULS_QQQ(34, 
                                               (0x00000003ffffffffULL 
                                                & VL_EXTENDS_QI(34,16, (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_2))), 
                                               (0x00000003ffffffffULL 
                                                & VL_EXTENDS_QI(34,18, 
                                                                (0x0001ffffU 
                                                                 & vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0)))));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_selected 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_DivPlugin_REM_lane0)
            ? vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__shifter
            : vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__result);
    vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS2_SIGNED_lane0) 
           & (vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0 
              >> 0x0000001fU));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT 
        = (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 
           & ((0x0007ffffU & (vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 
                              >> 1U)) == (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
                                          >> 0x0000000dU)));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_1 
        = (IData)(((0U == (0x0000ff00U & vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0)) 
                   & (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_2)));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0 
        = (((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1)
             ? (~ vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0)
             : vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0) 
           + (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1));
    vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_3 
        = (((IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1) 
            << 0x0000000fU) | (vlSelfRef.__PVT__execute_ctrl2_up_integer_RS2_lane0 
                               >> 0x00000011U));
    vlSelfRef.__PVT___zz_LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_UNIQUE 
        = ((vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 
            >> 0x00000015U) & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT));
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl1_up_PC_lane0 
            = vlSelfRef.__PVT__decode_ctrls_1_up_PC_0;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88 = ((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_1) 
                                                 | (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_2));
    vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_1 
        = (0x00000003ffffffffULL & VL_MULS_QQQ(34, 
                                               (0x00000003ffffffffULL 
                                                & VL_EXTENDS_QI(34,18, 
                                                                (0x0001ffffU 
                                                                 & vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0))), 
                                               (0x00000003ffffffffULL 
                                                & VL_EXTENDS_QI(34,16, (IData)(vlSelfRef.__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_3)))));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_6 
        = (1U & (~ ((0U == (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                            >> 0x00000018U)) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88))));
    if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
        vlSelfRef.__PVT__decode_ctrls_1_up_PC_0 = vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_WORD_PC;
    }
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__sel 
        = ((((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_6) 
             | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88)) 
                & (0U == (vlSelfRef.__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 
                          >> 0x00000018U)))) << 1U) 
           | ((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_6) 
              | ((~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_1)) 
                 & (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_2))));
    if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
        vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_WORD_PC 
            = vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC;
        vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC 
            = (0xfffffffcU & vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target);
    }
    vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_0 
        = (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem_spinal_port1 
           & ((0x0007ffffU & (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_0_mem_spinal_port1 
                              >> 2U)) == (vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC 
                                          >> 0x0000000dU)));
    vlSelfRef.__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_1 
        = (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem_spinal_port1 
           & ((0x0007ffffU & (vlSelfRef.__PVT__FetchL1Plugin_logic_ways_1_mem_spinal_port1 
                              >> 2U)) == (vlSelfRef.__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC 
                                          >> 0x0000000dU)));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__11(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__11\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.FetchL1Plugin_logic_bus_rsp_payload_error 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_denied) 
           | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_corrupt));
    vlSelfRef.LsuPlugin_logic_bus_rsp_payload_error 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_denied;
    vlSelfRef.FetchL1Plugin_logic_bus_cmd_payload_address 
        = (0xffffffc0U & vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address);
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_unique 
            = vlSelfRef.__PVT__execute_ctrl4_down_LsuL1Plugin_logic_NEED_UNIQUE_lane0;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_address 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_ready) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rData_ackId 
            = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackId) 
               & (- (IData)((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackRequest))));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_STORE_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MASK_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MASK_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_RD_PHYS_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_RD_PHYS_lane0;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SIZE_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_STORE_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_STORE_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MASK_lane0 
            = (0x0000000fU & ((0x0f31U >> ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SIZE_lane0) 
                                           << 2U)) 
                              << (3U & vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address)));
        vlSelfRef.__PVT__execute_ctrl3_up_RD_PHYS_lane0 
            = vlSelfRef.__PVT__execute_ctrl2_up_RD_PHYS_lane0;
        vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
            = vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address;
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_STORE_lane0 
            = (0x00000020U == (0x00000020U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0));
        vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SIZE_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_AguPlugin_SIZE_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_RD_PHYS_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_RD_PHYS_lane0;
        vlSelfRef.__PVT__execute_ctrl1_up_AguPlugin_SIZE_lane0 
            = (3U & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                     >> 0x0000000cU));
        vlSelfRef.__PVT__execute_ctrl1_up_RD_PHYS_lane0 
            = (0x0000001fU & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                              >> 7U));
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackId 
                = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_sink;
        }
    }
    vlSelfRef.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0 = 0U;
    if ((0U == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0))) {
        vlSelfRef.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0 
            = ((vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0 
                << 0x00000018U) | ((0x00ff0000U & (vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0 
                                                   << 0x00000010U)) 
                                   | ((0x0000ff00U 
                                       & (vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0 
                                          << 8U)) | 
                                      (0x000000ffU 
                                       & vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0))));
    } else if ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0))) {
        vlSelfRef.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0 
            = ((vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0 
                << 0x00000010U) | (0x0000ffffU & vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0));
    } else if ((2U == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0))) {
        vlSelfRef.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0 
            = vlSelfRef.__PVT__execute_ctrl4_up_integer_RS2_lane0;
    }
    vlSelfRef.LsuPlugin_logic_bus_cmd_payload_write 
        = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69 = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_LOAD_lane0) 
                                                 | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0));
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1Plugin_logic_NEED_UNIQUE_lane0 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_ATOMIC_lane0) 
           | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0));
    vlSelfRef.integer_write_0_address = vlSelfRef.__PVT__execute_ctrl4_up_RD_PHYS_lane0;
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_MISS_UNIQUE_lane0 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0) 
            & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1Plugin_logic_NEED_UNIQUE_lane0)) 
           & (~ ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault) 
                 | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique))));
    vlSelfRef.LsuPlugin_logic_bus_cmd_payload_address 
        = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 = (1U 
                                                 & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                                    | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_MISS_UNIQUE_lane0)));
    vlSelfRef.__PVT__LsuPlugin_pmaBuilder_io_argsBits 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0) 
            << 1U) | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_STORE_lane0));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21 = ((0x00020000U 
                                                  == 
                                                  (0xefff0000U 
                                                   & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                                                 | ((0x00030000U 
                                                     == 
                                                     (0xefff8000U 
                                                      & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                                                    | (0U 
                                                       == 
                                                       (0xeffe0000U 
                                                        & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0))));
    vlSelfRef.__PVT__execute_ctrl3_down_LsuPlugin_logic_onPma_IO_RSP_lane0_fault 
        = (1U & ((~ (((((0x80010000U == (0x80010000U 
                                         & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                        | (0x00800000U == (0x01800000U 
                                           & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0))) 
                       & ((4U == (4U & (IData)(vlSelfRef.__PVT__LsuPlugin_pmaBuilder_io_argsBits))) 
                          | (0U == (1U & (IData)(vlSelfRef.__PVT__LsuPlugin_pmaBuilder_io_argsBits))))) 
                      | ((0U == (0x40000000U & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                         | (0U == (0x00810000U & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)))) 
                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21) 
                        | ((0xf0000000U == (0xfffe0000U 
                                            & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                           | ((0x80000000U == (0xffff8000U 
                                               & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                              | ((0x01000000U == (0xff000000U 
                                                  & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)) 
                                 | (0xf0c00000U == 
                                    (0xffc00000U & vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0)))))))) 
                 | ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_ACCESS_lane0) 
                    | (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_ATOMIC_lane0))));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__12(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__12\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push;
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push = 0;
    CData/*1:0*/ __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop;
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop = 0;
    CData/*3:0*/ __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat;
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat = 0;
    // Body
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat;
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push;
    __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop;
    vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_pushCounter 
        = vlSelfRef.__PVT__FetchL1Plugin_logic_refill_pushCounter;
    vlSelfRef.__Vdly__AlignerPlugin_logic_feeder_harts_0_dopId 
        = vlSelfRef.__PVT__AlignerPlugin_logic_feeder_harts_0_dopId;
    vlSelfRef.__Vdly__LsuPlugin_logic_onAddress0_ls_storeId 
        = vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_ls_storeId;
    vlSelfRef.__Vdly__execute_ctrl3_up_LsuL1_SEL_lane0 
        = vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SEL_lane0;
    vlSelfRef.__Vdly__DecoderPlugin_logic_harts_0_uopId 
        = vlSelfRef.__PVT__DecoderPlugin_logic_harts_0_uopId;
    vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_interrupt_validBuffer 
        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_validBuffer;
    vlSelfRef.__Vdly__PcPlugin_logic_harts_0_self_id 
        = vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_id;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loaded;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_pushCounter 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_pushCounter;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_busy;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2;
    vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 
        = vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_read_wordIndex 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_freezeTimeout_counter_value 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value;
    vlSelfRef.__Vdly__fetch_logic_ctrls_1_up_valid 
        = vlSelfRef.__PVT__fetch_logic_ctrls_1_up_valid;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_write_wordIndex 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_wordIndex;
    vlSelfRef.__Vdly__CsrRamPlugin_logic_readLogic_ohReg 
        = vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight;
    vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_onRsp_wordIndex 
        = vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex;
    vlSelfRef.__Vdly__integer_RegFilePlugin_logic_initalizer_counter 
        = vlSelfRef.__PVT__integer_RegFilePlugin_logic_initalizer_counter;
    vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie 
        = vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mpie;
    vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie 
        = vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie;
    vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_slots_0_valid 
        = vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid;
    vlSelfRef.__Vdly__CsrRamPlugin_logic_flush_counter 
        = vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter;
    vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg 
        = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg;
    vlSelfRef.__Vdly__FetchL1Plugin_logic_invalidate_counter 
        = vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter;
    vlSelfRef.__Vdly__execute_ctrl1_up_LANE_SEL_lane0 
        = vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0;
    vlSelfRef.__Vdly__execute_ctrl3_up_LANE_SEL_lane0 
        = vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0;
    vlSelfRef.__Vdly__FetchL1Plugin_logic_ctrl_trapSent 
        = vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent;
    vlSelfRef.__Vdly__fetch_logic_ctrls_2_up_valid 
        = vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_initializer_counter 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter;
    vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_trap_fsm_stateReg 
        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg;
    vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_sampled 
        = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled;
    vlSelfRef.__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid 
        = vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid;
    vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_stateReg 
        = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_valid 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid;
    vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_read_wordIndex 
        = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_wordIndex;
    vlSelfRef.__Vdly__execute_ctrl2_up_LANE_SEL_lane0 
        = vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0;
    vlSelfRef.__Vdly__execute_ctrl4_up_LANE_SEL_lane0 
        = vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0;
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat = 0U;
        __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push = 0U;
        __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__locked = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_1 = 1U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_0 = 0U;
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done = 0U;
    } else {
        if (vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_c_fire) {
            __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_last) {
                __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram_wr_en) {
            __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push)));
        }
        if (vlSelfRef.__PVT___zz_LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight_5) {
            __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop)));
        }
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__locked = 1U;
            vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_1 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1;
            vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_0 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0;
        }
        if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_c_fire))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__locked = 0U;
        }
        if (((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy) 
             & (0x1fU == (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__counter)))) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done = 1U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done = 0U;
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat 
        = __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push 
        = __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop 
        = __Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push) 
           != (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop));
}

extern const VlUnpacked<CData/*0:0*/, 256> Vsim__ConstPool__TABLE_hb7cce103_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vsim__ConstPool__TABLE_h2ec615e0_0;
extern const VlUnpacked<CData/*1:0*/, 512> Vsim__ConstPool__TABLE_hc4c64601_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__13(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__13\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_cmdSent = 0U;
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_unscheduleRequest = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege = 3U;
        vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie = 0U;
        vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mprv = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_interrupt = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_code = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_meip = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_mtip = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_msip = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_meie = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_mtie = 0U;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_msie = 0U;
        vlSelfRef.__Vdly__FetchL1Plugin_logic_invalidate_counter = 0U;
        vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_firstEver = 1U;
        vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_slots_0_valid = 0U;
        vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_cmdSent = 1U;
        vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_pushCounter = 0U;
        vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_locked = 0U;
        vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_onRsp_wordIndex = 0U;
        vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_firstCycle = 1U;
        vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_valid = 0U;
        vlSelfRef.__Vdly__FetchL1Plugin_logic_ctrl_trapSent = 0U;
        vlSelfRef.__Vdly__AlignerPlugin_logic_feeder_harts_0_dopId = 0U;
        vlSelfRef.__Vdly__LsuPlugin_logic_onAddress0_ls_storeId = 0U;
        vlSelfRef.__Vdly__execute_ctrl3_up_LsuL1_SEL_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SEL_lane0 = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_tooEarly = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_allowIt = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doItReg = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent = 0U;
        vlSelfRef.__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_fenceTrap_doItReg = 0U;
        vlSelfRef.__Vdly__DecoderPlugin_logic_harts_0_uopId = 0U;
        vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered = 0U;
        vlSelfRef.__PVT__DispatchPlugin_logic_feeds_0_sent = 0U;
        vlSelfRef.__PVT__CsrRamPlugin_csrMapper_fired = 0U;
        vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0 = 0U;
        vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_interrupt_validBuffer = 0U;
        vlSelfRef.__Vdly__PcPlugin_logic_harts_0_self_id = 0U;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_increment = 0U;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_fault = 0U;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_state = 0U;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_holdReg = 1U;
        vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze = 0U;
        vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg = 0U;
        vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_sampled = 0U;
        vlSelfRef.__Vdly__CsrRamPlugin_logic_readLogic_ohReg = 0U;
        vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_busy = 0U;
        vlSelfRef.__Vdly__CsrRamPlugin_logic_flush_counter = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_valid = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded = 1U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_pushCounter = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_lock = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_read_wordIndex = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_hadError = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_lock = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_read_wordIndex = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_valid = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_lock = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_write_wordIndex = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_rb1_onBanks_0_busyReg = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_hazardReg = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_flushHazardReg = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_freezeTimeout_counter_value = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_persistance = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_initializer_counter = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight = 0U;
        vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat = 0U;
        vlSelfRef.__Vdly__execute_ctrl1_up_LANE_SEL_lane0 = 0U;
        vlSelfRef.__Vdly__execute_ctrl2_up_LANE_SEL_lane0 = 0U;
        vlSelfRef.__Vdly__execute_ctrl3_up_LANE_SEL_lane0 = 0U;
        vlSelfRef.__Vdly__execute_ctrl4_up_LANE_SEL_lane0 = 0U;
        vlSelfRef.__PVT__execute_ctrl5_up_LANE_SEL_lane0 = 0U;
        vlSelfRef.__Vdly__integer_RegFilePlugin_logic_initalizer_counter = 0U;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 = 0ULL;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 = 0ULL;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 = 0ULL;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 = 0ULL;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 = 0ULL;
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 = 0ULL;
        vlSelfRef.__Vdly__fetch_logic_ctrls_1_up_valid = 0U;
        vlSelfRef.__Vdly__fetch_logic_ctrls_2_up_valid = 0U;
        vlSelfRef.__PVT__decode_ctrls_1_up_valid = 0U;
        vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_trap_fsm_stateReg = 0U;
        vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_stateReg = 0U;
    } else {
        if (Vsim__ConstPool__TABLE_hb7cce103_0[((((IData)(vlSelfRef.__PVT__when_FetchL1Plugin_l545) 
                                                  | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent)) 
                                                 << 7U) 
                                                | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15))]) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_ctrl_trapSent = 1U;
        }
        if (vlSelfRef.__PVT__decode_ctrls_0_up_isFiring) {
            vlSelfRef.__Vdly__AlignerPlugin_logic_feeder_harts_0_dopId 
                = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__AlignerPlugin_logic_feeder_harts_0_dopId)));
        }
        vlSelfRef.__Vdly__LsuPlugin_logic_onAddress0_ls_storeId 
            = (0x00000fffU & ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_ls_storeId) 
                              + ((~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)) 
                                 & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_valid))));
        if (Vsim__ConstPool__TABLE_h2ec615e0_0[(((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg))]) {
            vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg = 1U;
        }
        vlSelfRef.__Vdly__CsrRamPlugin_logic_flush_counter 
            = (7U & ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                     + (IData)(vlSelfRef.__PVT___zz_CsrRamPlugin_logic_flush_counter_1)));
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_valid) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_pushCounter 
                = ((IData)(1U) + vlSelfRef.__PVT__LsuL1Plugin_logic_refill_pushCounter);
        }
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_fire) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy = 0U;
        }
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_read_wordIndex 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex) 
                              + (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1)));
        vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_write_wordIndex 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_wordIndex) 
                              + ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty) 
                                 & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire))));
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_FORCE_HAZARD) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_initializer_counter 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter)));
        }
        if (vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_c_fire) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat)));
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__VdfgRegularize_h6e95ff9d_0_82) 
                 | (0x0fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat)))) {
                vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__when_RegFilePlugin_l132) {
            vlSelfRef.__Vdly__integer_RegFilePlugin_logic_initalizer_counter 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__integer_RegFilePlugin_logic_initalizer_counter)));
        }
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 
                                        + (QData)((IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))));
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 
                                        + (QData)((IData)(
                                                          ((~ (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_candidates_0_fire)) 
                                                           & (IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1))))));
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 
                                        + (QData)((IData)(
                                                          (1U 
                                                           & (~ 
                                                              (2U 
                                                               >> (IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1))))))));
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 
                                        + (QData)((IData)(
                                                          (1U 
                                                           & (2U 
                                                              >> (IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1)))))));
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 
                                        + (QData)((IData)(
                                                          (1U 
                                                           & (~ (IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCount)))))));
        vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 
            = (0x0fffffffffffffffULL & (vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 
                                        + (QData)((IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCount))));
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rValid) {
            vlSelfRef.__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid = 1U;
        }
        if (((~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy)) 
             & (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div_io_cmd_valid))) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_cmdSent = 1U;
        }
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_unscheduleRequest 
            = vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_meip 
            = vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_external;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_mtip 
            = vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_timer;
        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_msip 
            = vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_software;
        if ((0x00000080U & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter))) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_firstEver = 0U;
        }
        if (vlSelfRef.FetchL1Plugin_logic_bus_cmd_valid) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_locked = 1U;
        }
        vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_valid 
            = ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid) 
               & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady));
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_tooEarly = 1U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_allowIt = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doItReg 
            = vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doIt;
        if (((IData)(vlSelfRef.LsuPlugin_logic_bus_cmd_ready) 
             & (IData)(vlSelfRef.LsuPlugin_logic_bus_cmd_valid))) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent = 1U;
        }
        if (((~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)) 
             & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid))) {
            vlSelfRef.__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid = 0U;
        }
        if (vlSelfRef.__PVT__DispatchPlugin_logic_candidates_0_fire) {
            vlSelfRef.__PVT__DispatchPlugin_logic_feeds_0_sent = 1U;
        }
        if (vlSelfRef.__PVT__decode_ctrls_1_up_isMoving) {
            vlSelfRef.__Vdly__DecoderPlugin_logic_harts_0_uopId 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_harts_0_uopId)));
            vlSelfRef.__PVT__DispatchPlugin_logic_feeds_0_sent = 0U;
        }
        if ((((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked) 
              >> 1U) & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_write_valid))) {
            vlSelfRef.__PVT__CsrRamPlugin_csrMapper_fired = 1U;
        }
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_holdReg 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_holdPort;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_state 
            = (0xfffffffcU & vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target);
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_fault 
            = vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_fault;
        vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_increment = 0U;
        if (vlSelfRef.__PVT__fetch_logic_ctrls_0_up_isFiring) {
            vlSelfRef.__Vdly__PcPlugin_logic_harts_0_self_id 
                = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_id)));
            vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_increment = 1U;
        }
        vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze = 0U;
        if (((IData)(vlSelfRef.__PVT__REG_CSR_772) 
             & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo))) {
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_meie 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 0x0bU));
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_mtie 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 7U));
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_msie 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 3U));
        }
        vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_busy 
            = vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_port_cmd_valid;
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_lock 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_oh;
        if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_payload_error) 
             & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_hadError = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter) 
             & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze)) 
                & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_busy)) 
                   | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_fire))))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid = 0U;
        }
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_lock 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_oh;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_valid 
            = vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_lock 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_oh;
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid 
                = vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0;
        }
        if (vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_rb1_onBanks_0_busyReg = 1U;
        }
        vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_hazardReg 
            = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0) 
               & (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1));
        vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_flushHazardReg 
            = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FLUSH_HAZARD_lane0) 
               & (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1));
        if ((0x4fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state = 1U;
        }
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_hit) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_persistance = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_refill) 
             & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedSet) 
                | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loaded)))) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid = 0U;
        }
        if (vlSelfRef.__PVT___zz_fetch_logic_ctrls_0_haltRequest_FetchL1Plugin_l218) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_invalidate_counter 
                = vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counterIncr;
        }
        if (vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_tooEarly = 0U;
        }
        if (((~ ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93))) 
             & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0))) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_allowIt = 1U;
        }
        if (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) {
            vlSelfRef.__PVT__CsrRamPlugin_csrMapper_fired = 0U;
        }
        if (((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid)) 
             & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_lock = 0U;
        }
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
            if ((5U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode))) {
                vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_read_wordIndex 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_wordIndex)));
            }
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
                vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_hadError = 0U;
                vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid = 1U;
            }
        }
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_ready) {
            if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackRequest) {
                vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid = 1U;
                vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid = 0U;
            } else {
                vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid = 0U;
            }
        }
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l608) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_lock = 0U;
        }
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l679) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_lock = 0U;
        }
        if (vlSelfRef.__PVT__when_LsuPlugin_l1000) {
            if (vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_WAIT_REFILL_lane0) {
                vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid = 1U;
            }
        }
        vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_stateReg 
            = Vsim__ConstPool__TABLE_hc4c64601_0[((
                                                   ((((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) 
                                                      << 4U) 
                                                     | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) 
                                                         << 3U) 
                                                        | (4U 
                                                           & ((~ 
                                                               ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap) 
                                                                | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
                                                              << 2U)))) 
                                                    | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) 
                                                        << 1U) 
                                                       | (1U 
                                                          & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))))) 
                                                   << 4U) 
                                                  | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) 
                                                      << 3U) 
                                                     | ((4U 
                                                         & ((~ 
                                                             ((~ 
                                                               ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg) 
                                                                >> 1U)) 
                                                              & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid))) 
                                                            << 2U)) 
                                                        | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))))];
        if ((IData)((((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                      >> 7U) & ((~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid) 
                                    | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_start_valid))) 
                                & (0x1000U >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))))) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_invalidate_counter = 0U;
        }
        if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                    if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) {
                        if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) {
                            if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) {
                                vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze 
                                    = vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
            vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered 
                = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_validBuffer;
        }
        if (vlSelfRef.FetchL1Plugin_logic_bus_cmd_ready) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_locked = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_fenceTrap_doItReg = 0U;
            vlSelfRef.__PVT__execute_ctrl5_up_LANE_SEL_lane0 
                = vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_cmdSent = 0U;
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_unscheduleRequest = 0U;
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent = 0U;
            vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg = 0U;
            vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_rb1_onBanks_0_busyReg = 0U;
            vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state = 0U;
            vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_persistance = 0U;
        }
        if (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_ctrl_trapSent = 0U;
        }
        if (VL_UNLIKELY((((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid) 
                          & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                                >> 7U)))))) {
            VL_WRITEF_NX("FAILURE \n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25260, "");
        }
        vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_interrupt_validBuffer 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_result_valid;
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedSet) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_free) 
             & Vsim__ConstPool__TABLE_hcaf816ea_0[(
                                                   (((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA) 
                                                       << 4U) 
                                                      | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                          << 3U) 
                                                         | ((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168) 
                                                            << 2U))) 
                                                     | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                         << 1U) 
                                                        | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid))) 
                                                    << 4U) 
                                                   | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                                                       << 3U) 
                                                      | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded) 
                                                          << 2U) 
                                                         | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))])) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid = 1U;
            vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy = 1U;
        }
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_freezeTimeout_counter_value 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_valueNext;
        if ((1U != Vsim__ConstPool__TABLE_hc4c64601_0
             [((((((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) 
                   << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) 
                              << 3U) | (4U & ((~ ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap) 
                                                  | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
                                              << 2U)))) 
                 | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) 
                     << 1U) | (1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))))) 
                << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) 
                           << 3U) | ((4U & ((~ ((~ 
                                                 ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg) 
                                                  >> 1U)) 
                                                & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid))) 
                                            << 2U)) 
                                     | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))))])) {
            if ((2U != Vsim__ConstPool__TABLE_hc4c64601_0
                 [((((((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) 
                       << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) 
                                  << 3U) | (4U & ((~ 
                                                   ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap) 
                                                    | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
                                                  << 2U)))) 
                     | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) 
                         << 1U) | (1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))))) 
                    << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) 
                               << 3U) | ((4U & ((~ 
                                                 ((~ 
                                                   ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg) 
                                                    >> 1U)) 
                                                  & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid))) 
                                                << 2U)) 
                                         | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))))])) {
                if ((3U == Vsim__ConstPool__TABLE_hc4c64601_0
                     [((((((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) 
                           << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) 
                                      << 3U) | (4U 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap) 
                                                     | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap))) 
                                                   << 2U)))) 
                         | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) 
                             << 1U) | (1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))))) 
                        << 4U) | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) 
                                   << 3U) | ((4U & 
                                              ((~ (
                                                   (~ 
                                                    ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg) 
                                                     >> 1U)) 
                                                   & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid))) 
                                               << 2U)) 
                                             | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))))])) {
                    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze = 1U;
                }
            }
        }
        if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
            vlSelfRef.__PVT__decode_ctrls_1_up_valid 
                = vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__Vdly__execute_ctrl4_up_LANE_SEL_lane0 
                = ((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid)) 
                   & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0));
            vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SEL_lane0 
                = ((~ ((~ (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0)) 
                       & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_LSU_lane0))) 
                   & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SEL_lane0));
        }
        if (VL_UNLIKELY(((((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                           & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0)) 
                          & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid))))) {
            VL_WRITEF_NX("FAILURE CsrAccessPlugin saw forbidden select && cancel request\n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25356, "");
        }
        if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
            vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0 
                = ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel)) 
                   & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid));
        }
        if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid) 
             & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze)) 
                & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter)))) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_valid = 0U;
        }
        vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight 
            = (3U & ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight) 
                       + (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_halfPipe_fire)) 
                      - (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight_5)) 
                     - ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81))));
        if (((IData)(vlSelfRef.__PVT__REG_CSR_768) 
             & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo))) {
            vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 7U));
            vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 3U));
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mprv 
                = (1U & (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                         >> 0x11U));
        }
        if (((IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel) 
             & (IData)(vlSelfRef.__PVT__when_DispatchPlugin_l373))) {
            vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0 = 0U;
        }
        if (vlSelfRef.__PVT__when_FetchL1Plugin_l256) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_pushCounter 
                = ((IData)(1U) + vlSelfRef.__PVT__FetchL1Plugin_logic_refill_pushCounter);
            if (vlSelfRef.__PVT___zz_when) {
                vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_slots_0_valid = 1U;
                vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_cmdSent = 0U;
            }
        }
        if (vlSelfRef.FetchL1Plugin_logic_bus_cmd_ready) {
            if (vlSelfRef.FetchL1Plugin_logic_bus_cmd_valid) {
                vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_cmdSent = 1U;
            }
        }
        vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_sampled 
            = vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1;
        if (((IData)(vlSelfRef.__PVT__REG_CSR_834) 
             & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo))) {
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_interrupt 
                = (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
                   >> 0x1fU);
            vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_code 
                = (0x0000001fU & vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits);
        }
        vlSelfRef.__Vdly__CsrRamPlugin_logic_readLogic_ohReg 
            = ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_port_cmd_valid)
                ? (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits_ohFirst_masked)
                : 0U);
        if (((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)) 
             & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_valid))) {
            vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_valid = 1U;
            vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__Vdly__execute_ctrl3_up_LANE_SEL_lane0 
                = vlSelfRef.__PVT__execute_ctrl2_LANE_SEL_lane0_bypass;
            vlSelfRef.__Vdly__execute_ctrl3_up_LsuL1_SEL_lane0 
                = vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_valid;
        }
        if (VL_UNLIKELY(((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) 
                           & (5U != (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode))) 
                          & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_data))))) {
            VL_WRITEF_NX("FAILURE Data cache asked for data but didn't recieved any :(\n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25408, "");
        }
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid;
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_firstCycle = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__Vdly__execute_ctrl2_up_LANE_SEL_lane0 
                = ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel)) 
                   & (IData)(vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0));
        }
        if (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel) {
            vlSelfRef.__Vdly__fetch_logic_ctrls_2_up_valid = 0U;
        }
        if (((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_ABORD_lane0)) 
             & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0))) {
            if (VL_UNLIKELY(((2U <= (3U & (0xe994U 
                                           >> ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_payload_data) 
                                                 << 3U) 
                                                | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doUpgrade) 
                                                   << 2U)) 
                                               | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) 
                                                  << 1U)))))))) {
                VL_WRITEF_NX("FAILURE \n",0);
                VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25505, "");
            }
        }
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid) {
            vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_onRsp_wordIndex 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex)));
            if ((0x0fU == (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex))) {
                vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_firstCycle = 1U;
                vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_slots_0_valid = 0U;
            }
        }
        if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
            vlSelfRef.__Vdly__fetch_logic_ctrls_2_up_valid 
                = ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel)) 
                   & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_valid));
        }
        if (VL_UNLIKELY((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_full) 
                          & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid))))) {
            VL_WRITEF_NX("FAILURE \n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25556, "");
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__Vdly__execute_ctrl1_up_LANE_SEL_lane0 
                = vlSelfRef.__PVT__execute_ctrl0_LANE_SEL_lane0_bypass;
        }
        vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid;
        if ((8U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                          >> 2U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege = 3U;
                        if ((3U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_arg))) {
                            vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie 
                                = vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mpie;
                            vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie = 1U;
                        }
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                    vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege 
                        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_targetPrivilege;
                    if ((3U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_targetPrivilege))) {
                        vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie 
                            = vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie;
                        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_code 
                            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_code;
                        vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_interrupt 
                            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt;
                        vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie = 0U;
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_TrapPlugin_l454)))) {
                    if (VL_UNLIKELY(((0x00000010U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                        VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                        VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                    } else if ((8U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                        if (VL_UNLIKELY(((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                            VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                        } else if (VL_UNLIKELY(((2U 
                                                 & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                            VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                        } else if (VL_UNLIKELY(((1U 
                                                 & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                            VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                        }
                    } else if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                            if (VL_UNLIKELY(((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                                VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                                VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                        if (VL_UNLIKELY(((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))))) {
                            VL_WRITEF_NX("FAILURE Unexpected trap reason\n",0);
                            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25652, "");
                        }
                    } else if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))) {
                        if (VL_UNLIKELY((vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_valid))) {
                            VL_WRITEF_NX("FAILURE \n",0);
                            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 25628, "");
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel) {
            vlSelfRef.__Vdly__fetch_logic_ctrls_1_up_valid = 0U;
        }
        if (vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady) {
            vlSelfRef.__Vdly__fetch_logic_ctrls_1_up_valid 
                = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90) 
                   & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_0_up_isValid));
        }
        vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_trap_fsm_stateReg 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext;
    }
}
