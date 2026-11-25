// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ico_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ico_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__litex_reset = (((IData)(vlSymsp->TOP.sys_reset) 
                                     | (IData)(vlSymsp->TOP__sim.__PVT__soc_soc_rst)) 
                                    | ((IData)(vlSymsp->TOP__sim.__PVT__soc_reset_storage) 
                                       >> 1U));
    vlSelfRef.__PVT__dma_bus_wready = ((~ (IData)(vlSelfRef.__PVT__litex_reset)) 
                                       & (IData)(vlSelfRef.__PVT__dma_bus_w_rValidN));
    vlSelfRef.__PVT__dma_bus_awready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_aw_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
    vlSelfRef.__PVT__dma_bus_arready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_ar_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0 = 0U;
    vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0 = 0U;
    vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0 = 0U;
    vlSelfRef.__VdlySet__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0 = 0U;
    vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0 = 0U;
    vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0 = 0U;
    vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0 = 0U;
    vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0 = 0U;
    vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0 = 0U;
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4) {
        vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_target_mem_port;
        vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_write_payload_address;
        vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0 = 1U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3) {
        vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_hit_mem_port;
        vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address;
        vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0 = 1U;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid) {
        vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data;
        vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0 
            = ((0x00000030U & ((IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source) 
                               << 4U)) | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter));
        vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0 = 1U;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_1) {
        vlSelfRef.__VdlyVal__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0 
            = (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_id) 
                << 1U) | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST));
        vlSelfRef.__VdlyDim0__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0 
            = (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd));
        vlSelfRef.__VdlySet__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0 = 1U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_2) {
        vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0 
            = (((QData)((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_data)) 
                << 4U) | (QData)((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_mask)));
        vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0 
            = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID) 
                << 4U) | (0x0000000fU & ((vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_address 
                                          >> 2U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat))));
        vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0 = 1U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
        vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0 
            = (((QData)((IData)(((((4U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp)) 
                                          << 2U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_BUFFER_ID)) 
                                  << 9U) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_source) 
                                             << 4U) 
                                            | (((0U 
                                                 != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param)) 
                                                << 3U) 
                                               | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_size)))))) 
                << 0x00000023U) | (((QData)((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address)) 
                                    << 3U) | (QData)((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode))));
        vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0 
            = ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1)) 
                << 1U) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) 
                          | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId)));
        vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0 = 1U;
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_probeAckDataCompleted = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_set 
                = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address 
                                  >> 6U));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_probeAckDataCompleted = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_set 
                = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address 
                                  >> 6U));
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending 
                = (1U & (2U >> (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask)));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_probeAckDataCompleted = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_set 
                = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address 
                                  >> 6U));
        }
        if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_probeAckDataCompleted = 0U;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_5) {
        vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0 
            = ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)
                  ? ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)
                        ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId)
                        : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_PROBE_ID)) 
                      << 1U) | (5U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)))
                  : ((0x00000400U & ((IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                              >> 0x0000002eU)) 
                                     << 0x0000000aU)) 
                     | ((0x00000200U & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_UNIQUE) 
                                         | (IData)(
                                                   (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                                    >> 0x00000026U))) 
                                        << 9U)) | (
                                                   (((4U 
                                                      == 
                                                      (7U 
                                                       & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47)) 
                                                    << 8U) 
                                                   | (0x000000ffU 
                                                      & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS 
                                                         >> 6U)))))) 
                << 6U) | ((0x0000003eU & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)
                                            ? (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_source)
                                            : (IData)(
                                                      (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                                       >> 0x00000027U))) 
                                          << 1U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)));
        vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ID;
        vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0 = 1U;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT___zz_1) {
        vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0 
            = ((0x00000c00U & (((~ ((0x000000ffU & 
                                     ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size))) 
                                    - (IData)(1U))) 
                                & vlSelfRef.__PVT__dma_bus_ar_rData_addr) 
                               << 0x0000000aU)) | (
                                                   (0x00000300U 
                                                    & (((0x000000ffU 
                                                         & ((IData)(1U) 
                                                            << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size))) 
                                                        - (IData)(1U)) 
                                                       << 8U)) 
                                                   | (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_len)));
        vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0 
            = vlSelfRef.__PVT__dma_bus_ar_rData_id;
        vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0 = 1U;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2) {
        vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0 
            = (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS) 
                << 9U) | ((0x000001e0U & (((vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_addr 
                                            - (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)) 
                                           << 3U) & 
                                          ((- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST))) 
                                           << 5U))) 
                          | (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_id) 
                              << 1U) | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST))));
        vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0 
            = (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd));
        vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0 = 1U;
    }
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_data 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data;
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_param 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1;
    if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__when_Clint_l59) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT___zz_factory_rspAsync_payload_data 
            = (IData)((vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time 
                       >> 0x20U));
    }
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_corrupt 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt;
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_denied 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied;
    if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__start) {
        vlSelfRef.__PVT__dma_filter_logic_core__DOT__source 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source;
        vlSelfRef.__PVT__dma_filter_logic_core__DOT__size 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_param = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_data = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_corrupt = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_denied = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_opcode = 6U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_corrupt = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_data = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_param = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_denied = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_opcode = 4U;
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_readAddressBuffer 
            = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                              >> 6U));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_readAddressBuffer 
            = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                              >> 6U));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem_spinal_port1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem
            [(0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                             >> 6U))];
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem_spinal_port1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem
            [(0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                             >> 6U))];
    }
    vlSelfRef.__PVT___zz_vexiis_0_priv_rdtime = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time;
    vlSelfRef.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_corrupt 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt;
    vlSelfRef.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_denied 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied;
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST 
            = (0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter));
    }
    if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_denied = 0U;
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_data 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data;
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_size 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_denied = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_data 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_size 
            = (3U & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size));
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_hit) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassData 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_hit_mem_port;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_hit) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassData 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_target_mem_port;
    }
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_timerInterrupt 
        = (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_cmp 
           <= vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time);
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_len 
            = (0x000000ffU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats) 
                              >> 2U));
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SLOT_ID 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SLOT_ID;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_len 
            = (0x000000ffU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats) 
                              >> 2U));
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_priority 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_6)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_lockedValue 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_firstFree;
    }
    if (vlSelfRef.__PVT__dma_bus_awready) {
        vlSelfRef.__PVT__dma_bus_aw_rData_len = (0x000000ffU 
                                                 & ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__chunk_r) 
                                                    - (IData)(1U)));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotReg 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_data 
            = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_denied 
            = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_size 
            = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_opcode 
            = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending 
                = (1U & (2U >> (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask)));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending 
                = (1U & (2U >> (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask)));
        }
        if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending 
                = (1U & (2U >> (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask)));
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l475) {
        if ((0U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
            if ((1U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                if ((2U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending 
                        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext;
                }
                if ((2U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending 
                        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext;
                }
            }
            if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending 
                    = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext;
            }
        }
        if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext;
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SIZE 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SIZE;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_WRITE_DATA 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_WRITE_DATA;
    }
    if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get 
            = (4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode));
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_source 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_source;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_address 
            = (0xffffffc0U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address);
    }
    if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_opcode 
            = (1U & (- (IData)((4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)))));
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_source 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_source;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_opcode 
            = (1U & (- (IData)((4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)))));
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_source 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_source;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_cache 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_cache;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_size 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_size;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN 
            = (0x0000000fU & (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END) 
                               >> 2U) - ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START) 
                                         >> 2U)));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_cache 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_cache;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_size 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_size;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START;
    }
    if (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem
            [vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_CTX_id];
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_corrupt 
            = ((0U == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param))
                ? (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_corrupt)
                : ((1U == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param)) 
                   && (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_corrupt)));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockSel 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C;
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_opcode = 6U;
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_size = 6U;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_param 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_param;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_address 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_address;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_opcode 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_opcode;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_size 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_size;
    }
    if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__start) {
        vlSelfRef.__PVT__dma_filter_logic_core__DOT__opcode 
            = ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                ? 4U : 1U);
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_FROM_NONE 
            = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fromNone) 
                & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh)) 
               | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fromNone) 
                   & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                      >> 1U)) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fromNone) 
                                  & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                                     >> 3U)) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fromNone) 
                                                & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                                                   >> 2U)))));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat 
            = (3U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN)
                      ? ((0x000000ffU & ((IData)(1U) 
                                         << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size))) 
                         - (IData)(1U)) : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_bytePerBeat)));
    }
    if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_data 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_data;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_source 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_mask 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_mask;
        } else {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_data 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_data;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_source 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_source;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_mask 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_mask;
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)))) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_data 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2) {
        if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_error = 0U;
        }
        if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_error = 0U;
            }
            if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_error = 0U;
                }
                if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_error = 0U;
                }
            }
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid) {
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last) {
            if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_error 
                    = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
            }
            if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_error 
                        = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                }
                if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_error 
                            = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                    }
                    if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_error 
                            = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_1) {
        if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_error = 0U;
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_done = 0U;
        }
        if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_error = 0U;
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_done = 0U;
            }
            if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_error = 0U;
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_done = 0U;
                }
                if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_error = 0U;
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_done = 0U;
                }
            }
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_1_d_valid) {
        if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_error 
                = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_done = 1U;
        }
        if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
            if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_error 
                    = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_done = 1U;
            }
            if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_error 
                        = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_done = 1U;
                }
                if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_error 
                        = (0U != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp));
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_done = 1U;
                }
            }
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2) {
        if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_done = 0U;
        }
        if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
            if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_done = 0U;
            }
            if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_done = 0U;
                }
                if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_done = 0U;
                }
            }
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid) {
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last) {
            if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_done = 1U;
            }
            if ((0U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_done = 1U;
                }
                if ((1U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                    if ((2U != (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_done = 1U;
                    }
                    if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source)))) {
                        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_done = 1U;
                    }
                }
            }
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_size 
            = (7U & (IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                             >> 0x00000023U)));
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_BUFFER_ID 
            = (3U & (IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                             >> 0x0000002cU)));
    }
    if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_address 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_param 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param;
        } else {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_address 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_address;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_param 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_param;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_2 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_size 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_opcode 
                = ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                    ? 4U : 1U);
        } else {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_size 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_size;
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_opcode 
                = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_opcode;
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_param 
            = (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_c_data)
                 ? 1U : 2U) & (- (IData)((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_c_unique))));
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_address 
            = (0xffffffc0U & vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_address);
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l53) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_strb = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_strb = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_strb = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_strb = 0U;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge_io_up_w_ready) {
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_1) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_strb 
                = (1U & ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb) 
                         >> 1U));
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_data 
                = (0x000000ffU & (vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data 
                                  >> 8U));
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_3) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_strb 
                = (1U & ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb) 
                         >> 3U));
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_data 
                = (vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data 
                   >> 0x18U);
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_2) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_strb 
                = (1U & ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb) 
                         >> 2U));
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_data 
                = (0x000000ffU & (vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data 
                                  >> 0x10U));
        }
        if ((0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_strb 
                = (1U & (IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb));
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_data 
                = (0x000000ffU & vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data);
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_source 
            = (0x0000001fU & (IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                      >> 0x00000027U)));
    }
    if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_source 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_source;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_size 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_size;
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PARTIAL_DATA 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PARTIAL_DATA;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_TO_DOWN 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_TO_DOWN;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_data 
            = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_FROM_C)
                ? vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_data
                : (IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram_spinal_port1 
                           >> 4U)));
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_param 
                = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_param;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_address;
        } else {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_param 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_param;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_address;
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)))) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_address 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address;
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode;
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_mask 
            = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                ? (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_mask)
                : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_mask));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_header 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_payload_header;
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_len 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN;
        } else {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_header 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_header;
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_len 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_len;
        }
    }
    if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_first) 
         & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_isFiring))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_base 
            = (0x0000000fU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS 
                              >> 2U));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_data 
            = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_data;
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_size 
            = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_size;
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_address 
            = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_address;
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_opcode 
            = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_opcode;
    }
    if (vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready) {
        vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rData_data 
            = ((IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN)
                ? vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_data
                : vlSelfRef.__PVT__dma_bridge_up_r_rData_data);
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_id 
        = (0x0000001fU & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_6)
                           ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80)
                               ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_72)
                                   ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_48)
                                       ? (1U & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110))))
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3)
                                           ? 2U : 3U))
                                   : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_6)
                                           ? 4U : 5U)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_9)
                                           ? 6U : 7U)))
                               : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74)
                                   ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_54)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_12)
                                           ? 8U : 9U)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_15)
                                           ? 0x0aU : 0x0bU))
                                   : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_57)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_18)
                                           ? 0x0cU : 0x0dU)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_21)
                                           ? 0x0eU : 0x0fU))))
                           : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81)
                               ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_76)
                                   ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_60)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_24)
                                           ? 0x10U : 0x11U)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_27)
                                           ? 0x12U : 0x13U))
                                   : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_63)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_30)
                                           ? 0x14U : 0x15U)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_33)
                                           ? 0x16U : 0x17U)))
                               : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_78)
                                   ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_66)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_36)
                                           ? 0x18U : 0x19U)
                                       : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_39)
                                           ? 0x1aU : 0x1bU))
                                   : ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_69)
                                       ? ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_42)
                                           ? 0x1cU : 0x1dU)
                                       : (0x1eU | (- (IData)(
                                                             (1U 
                                                              & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_45)))))))))));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rData_sink 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rData_ackId;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK 
            = (0x0000003fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
                              + (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                                 >> 6U)));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_addr 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK 
            = (0x0000003fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
                              + (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                                 >> 6U)));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_opcode = 6U;
    }
    vlSelfRef.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_data 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data;
    vlSelfRef.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_data 
        = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data;
    vlSelfRef.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_denied 
        = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied;
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem[vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0] 
            = vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem__v0;
    }
    if (vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem[vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0] 
            = vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem__v0;
    }
    if (vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem[vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0] 
            = vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem__v0;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_id 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_id;
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_data 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_mask 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_address 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address;
        } else {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_data 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_data;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_mask 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_mask;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_address 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_address;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_BUFFER_ID 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_size 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_source 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_source;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_PROBE_ID 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_PROBE_ID;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_UNIQUE 
            = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_unique) 
                & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh)) 
               | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_unique) 
                   & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                      >> 1U)) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_unique) 
                                  & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                                     >> 3U)) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_unique) 
                                                & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                                                   >> 2U)))));
    }
    if (vlSelfRef.__PVT__dma_bus_arready) {
        vlSelfRef.__PVT__dma_bus_ar_rData_size = 2U;
        vlSelfRef.__PVT__dma_bus_ar_rData_len = (0x000000ffU 
                                                 & ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__chunk_r) 
                                                    - (IData)(1U)));
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
                              - (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart)));
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST 
            = (0U == (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter));
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_id 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_id;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_addr 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr;
    }
    if ((0x1000U == (0x00003fffU & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)))) {
        if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_doWrite) {
            vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_cmp 
                = ((0xffffffff00000000ULL & vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_cmp) 
                   | (IData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data)));
        }
    }
    if ((0x1001U == (0x00003fffU & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)))) {
        if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_doWrite) {
            vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_cmp 
                = ((0x00000000ffffffffULL & vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_cmp) 
                   | ((QData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data)) 
                      << 0x00000020U));
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SLOT_ID 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ID;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SIZE 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_WRITE_DATA 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_cache 
            = vlSelfRef.__PVT__dma_bus_ar_rData_cache;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_size 
            = ((0U != (0x000000ffU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats) 
                                      >> 2U))) ? 2U
                : (3U & (0xa4U >> (6U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats) 
                                         << 1U)))));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_cache 
            = vlSelfRef.__PVT__dma_bus_aw_rData_cache;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_size 
            = ((0U != (0x000000ffU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats) 
                                      >> 2U))) ? 2U
                : (3U & (0xa4U >> (6U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats) 
                                         << 1U)))));
    }
    if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_corrupt = 0U;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_corrupt = 0U;
    }
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_ready) {
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_param = 0U;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_address 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_payload_address;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_opcode = 4U;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rData_size = 6U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fromNone 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fromNone 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fromNone 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone;
        }
        if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fromNone 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l475) {
        if ((0U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
            if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt) {
                    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fromNone = 1U;
                }
            }
            if ((1U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                if ((2U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt) {
                        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fromNone = 1U;
                    }
                }
                if ((2U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
                    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt) {
                        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fromNone = 1U;
                    }
                }
            }
        }
        if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))) {
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fromNone = 1U;
            }
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_bytePerBeat 
            = (3U & ((0x000000ffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size))) 
                     - (IData)(1U)));
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 
        = ((((2U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                    << 1U)) | (1U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                     >> 1U))) << 6U) 
           | ((0x00000020U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                              << 3U)) | (0x00000010U 
                                         & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                            << 1U))));
    if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN) {
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_data 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_data;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_source 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_mask 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_mask;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_address 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_param 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_size 
            = vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_source = 8U;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_size 
                = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_size;
        } else {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_source 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_source;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_size 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_size;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PARTIAL_DATA 
            = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)) 
               & (1U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_TO_DOWN 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_data 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_data;
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_param 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_address 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_address;
    }
    if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN) {
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_opcode 
            = ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                ? 4U : 1U);
    }
    if (vlSelfRef.__PVT__dma_bus_w_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_bus_w_rValidN) {
            vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb 
                = vlSelfRef.__PVT__dma_bus_wstrb;
            vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data 
                = vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__buf_r
                [(0x0000000fU & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__count_r))];
        } else {
            vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_strb 
                = vlSelfRef.__PVT__dma_bus_w_rData_strb;
            vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_data 
                = vlSelfRef.__PVT__dma_bus_w_rData_data;
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_header 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_payload_header;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_len 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN;
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_ADDRESS;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_mask 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_FROM_C)
                               ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_mask)
                               : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram_spinal_port1)));
    }
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_ready) {
        vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_data 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0;
        vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_size 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0;
        vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_address 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0;
        vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_opcode 
            = (4U & (- (IData)((1U & (~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0))))));
    }
    if (vlSelfRef.__PVT__dma_bridge_up_r_rValidN) {
        vlSelfRef.__PVT__dma_bridge_up_r_rData_data 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_data;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_mask 
            = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_mask;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
            = vlSelfRef.__PVT__dma_bus_aw_rData_addr;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_id 
            = vlSelfRef.__PVT__dma_bus_aw_rData_id;
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_payload_header 
        = (0x0000000fU & (((vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_addr 
                            - (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)) 
                           >> 2U) & (- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST)))));
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_data 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_mask 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_address 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address;
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_source 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source;
        } else {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_size;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_source 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_source;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_unique = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_unique = 1U;
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_unique = 1U;
        }
        if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_unique = 1U;
        }
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_id 
            = vlSelfRef.__PVT__dma_bus_ar_rData_id;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
            = vlSelfRef.__PVT__dma_bus_ar_rData_addr;
    }
    if (vlSelfRef.__PVT__dma_bus_arready) {
        vlSelfRef.__PVT__dma_bus_ar_rData_cache = 0U;
        vlSelfRef.__PVT__dma_bus_ar_rData_addr = (vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__word_addr_r 
                                                  << 2U);
    }
    if (vlSelfRef.__PVT__dma_bus_awready) {
        vlSelfRef.__PVT__dma_bus_aw_rData_cache = 0U;
        vlSelfRef.__PVT__dma_bus_aw_rData_size = 2U;
        vlSelfRef.__PVT__dma_bus_aw_rData_addr = (vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__word_addr_r 
                                                  << 2U);
    }
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_param 
                = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_param;
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_address 
                = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_address;
        } else {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_param 
                = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_param;
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_address 
                = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_address;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_source = 8U;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_size 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_size;
    }
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_size 
            = ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN)
                ? 6U : (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_size));
    }
    if (vlSelfRef.__PVT__dma_bus_wready) {
        vlSelfRef.__PVT__dma_bus_w_rData_strb = vlSelfRef.__PVT__dma_bus_wstrb;
        vlSelfRef.__PVT__dma_bus_w_rData_data = vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__buf_r
            [(0x0000000fU & (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__count_r))];
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_ADDRESS 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_mask = 0x0fU;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_FROM_C 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram_spinal_port1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram
            [((0x00000030U & ((IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                       >> 0x0000002cU)) 
                              << 4U)) | (0x0000000fU 
                                         & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS 
                                            >> 2U)))];
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN 
            = (0x0000000fU & (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END) 
                               >> 2U) - ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START) 
                                         >> 2U)));
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_data 
            = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN)
                ? vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_data
                : vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_data);
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_data 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_data;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_data 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem_spinal_port1;
    }
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_ready) {
        vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rData_mask 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__execute_ctrl4_up_LsuL1_MASK_lane0;
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
        = (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
           + ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_len) 
              << 2U));
    if (vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram[vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0] 
            = vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram__v0;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
        = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_address;
    if ((0U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xfffffffeU & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if ((1U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xfffffffdU & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if ((2U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xfffffffbU & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if ((3U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xfffffff7U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if ((4U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xffffffefU & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if ((5U < (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
            = (0xffffffdfU & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address);
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_size 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_source 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source;
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
        = (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
           + ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_len) 
              << 2U));
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_param 
            = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_param;
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_address 
            = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_address;
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 
        = ((((2U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                    << 1U)) | (1U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                     >> 1U))) << 6U) 
           | ((0x00000020U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                              << 3U)) | (0x00000010U 
                                         & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                            << 1U))));
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem_spinal_port1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem
            [((0x00000030U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp) 
                              << 4U)) | (0x0000000fU 
                                         & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter) 
                                            + ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1) 
                                               >> 5U))))];
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats 
        = (0x00007fffU & ((3U & ((~ (((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size)) 
                                     - (IData)(1U))) 
                                 & vlSelfRef.__PVT__dma_bus_aw_rData_addr)) 
                          + (((IData)(vlSelfRef.__PVT__dma_bus_aw_rData_len) 
                              << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size)) 
                             + (3U & (0x0034U >> ((IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size) 
                                                  << 1U))))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1));
    if (vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem[vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0] 
            = vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem__v0;
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats 
        = (0x00007fffU & ((3U & ((~ (((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size)) 
                                     - (IData)(1U))) 
                                 & vlSelfRef.__PVT__dma_bus_ar_rData_addr)) 
                          + (((IData)(vlSelfRef.__PVT__dma_bus_ar_rData_len) 
                              << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size)) 
                             + (3U & (0x0034U >> ((IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size) 
                                                  << 1U))))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_data 
            = ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN)
                ? vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_data
                : vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_data);
    }
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_size = 6U;
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_data 
            = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_data;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_sink 
        = ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))
            ? ((0x00000100U & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                               >> 8U)) | (0x000000ffU 
                                          & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                                             >> 6U)))
            : ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))
                ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_sink)
                : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_sink)));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid)))) {
        vlSelfRef.__PVT__dma_bridge_up_b_rData_resp 
            = (2U & (- (IData)(((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_errorAcc) 
                                | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error)))));
    }
    if (vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready) {
        if (vlSelfRef.__PVT__dma_bridge_up_r_rValidN) {
            vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rData_last 
                = vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last;
            vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rData_resp 
                = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_resp;
        } else {
            vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rData_last 
                = vlSelfRef.__PVT__dma_bridge_up_r_rData_last;
            vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rData_resp 
                = vlSelfRef.__PVT__dma_bridge_up_r_rData_resp;
        }
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_sink = 0U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_sink 
            = ((0x00000100U & ((IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                        >> 0x0000002eU)) 
                               << 8U)) | (0x000000ffU 
                                          & (IData)(
                                                    (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                                     >> 9U))));
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx
            [(3U & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source))];
    }
    if (vlSelfRef.__PVT__dma_bridge_up_r_rValidN) {
        vlSelfRef.__PVT__dma_bridge_up_r_rData_last 
            = vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last;
        vlSelfRef.__PVT__dma_bridge_up_r_rData_resp 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_resp;
    }
    if (vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx[vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0] 
            = vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__slots_ctx__v0;
    }
    if ((1U & (~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_ready)) 
                  & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid))))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem
            [vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_PROBE_ID];
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param = 0U;
    if ((1U & (~ vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1))) {
        if ((1U & (~ (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                      >> 0x0000000eU)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param 
                = ((0x00008000U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)
                    ? 0U : 1U);
        }
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_opcode;
    if ((1U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode = 6U;
    } else if ((1U & (~ (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                         >> 0x0000000eU)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode = 5U;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit 
        = (IData)((0x00000041U == (0x00000041U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)));
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_resp 
            = (2U & (- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_ERRORED))));
    }
    if (vlSelfRef.__VdlySet__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem[vlSelfRef.__VdlyDim0__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0] 
            = vlSelfRef.__VdlyVal__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem__v0;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47 = ((1U 
                                                  == 
                                                  (7U 
                                                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
                                                 | (0U 
                                                    == 
                                                    (7U 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))));
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_ERRORED 
            = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_errorAcc) 
               | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error));
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__initializer_counter 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority;
    vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat;
    vlSelfRef.__Vdly__vexiis_0_iBus_bus_a_rValid = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rValid;
    vlSelfRef.__Vdly__vexiis_0_dBus_bus_a_rValid = vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rValid;
    vlSelfRef.__Vdly__vexiis_0_lsuL1Bus_bus_e_rValid 
        = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid;
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__Vdly__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__initializer_counter = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority = 0U;
        vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat = 0U;
        vlSelfRef.__Vdly__vexiis_0_iBus_bus_a_rValid = 0U;
        vlSelfRef.__Vdly__vexiis_0_dBus_bus_a_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids = 0U;
        vlSelfRef.__Vdly__vexiis_0_lsuL1Bus_bus_e_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2 = 1U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid = 0U;
    } else {
        if (vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire) {
            vlSelfRef.__Vdly__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) {
                vlSelfRef.__Vdly__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_fire) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_last) {
                vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat)));
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST) {
                vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter)));
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST) {
                vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter = 0U;
            }
        }
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated 
            = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated) 
                | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set)) 
               & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_clear)));
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l197) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__initializer_counter 
                = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter)));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_isFiring) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority 
                = (((0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))
                     ? 0x0fU : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority)) 
                   & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh)));
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) 
             & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_ups_1_d_valid))) {
            vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat)));
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_0_LAST) {
                vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat = 0U;
            }
        }
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_valid) {
            vlSelfRef.__Vdly__vexiis_0_iBus_bus_a_rValid = 1U;
        }
        if (((~ (IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid)) 
             & (IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rValid))) {
            vlSelfRef.__Vdly__vexiis_0_iBus_bus_a_rValid = 0U;
        }
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_valid) {
            vlSelfRef.__Vdly__vexiis_0_dBus_bus_a_rValid = 1U;
        }
        if (((~ (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid)) 
             & (IData)(vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rValid))) {
            vlSelfRef.__Vdly__vexiis_0_dBus_bus_a_rValid = 0U;
        }
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids 
            = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids) 
                | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_first) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_5))
                    ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4)
                    : 0U)) & (~ (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
                                  & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_slotRelease_fired)) 
                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_LAST)))
                                  ? ((IData)(1U) << (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_source))
                                  : 0U)));
        if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid) {
            vlSelfRef.__Vdly__vexiis_0_lsuL1Bus_bus_e_rValid = 1U;
        }
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid) {
            vlSelfRef.__Vdly__vexiis_0_lsuL1Bus_bus_e_rValid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_stages_1_valid;
        }
        if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassValid = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_hit) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassValid = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_hit) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__locked = 1U;
            vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0;
            vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1;
            vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire))) {
            vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid)));
        }
        if (((~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid)) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_106))) {
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired = 1U;
            }
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted = 1U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fire) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fire) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fire) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid = 1U;
            }
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid = 1U;
            }
            if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid = 1U;
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__12(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__12\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid = 0U;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_first = 1U;
        vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid = 0U;
        vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_first = 1U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_slotRelease_fired = 0U;
        vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN = 1U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid = 0U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid = 0U;
    } else {
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fire) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1) {
            if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId) {
                vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid = 1U;
            }
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST) 
             & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid)));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid 
                = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid) 
                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_fire))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid) 
             & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12_io_inputs_0_ready))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid 
                = ((6U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)) 
                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_valid));
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_2) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock 
                = (1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST)));
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_first 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_isFiring) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_first 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_LAST;
        }
        if (vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rValid) {
            vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45))) {
            vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid = 0U;
        }
        if (vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rValid) {
            vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_a_ready) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52))) {
            vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_slotRelease_fired = 1U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired = 0U;
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_slotRelease_fired = 0U;
        }
        if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_down_a_valid)));
        }
        if (vlSelfRef.__PVT__dma_filter_logic_core_io_down_a_valid) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid 
                = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_valid;
        }
        if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid 
                = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96) 
                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid));
        }
    }
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rValid 
        = ((1U & (~ (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1))) 
           && (IData)(((8U == (0x18U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source))) 
                       & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid))));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__Vdly__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__initializer_counter;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__Vdly__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat;
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid 
        = vlSelfRef.__Vdly__vexiis_0_lsuL1Bus_bus_e_rValid;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_buffer_firstFree_6 
        = (1U & ((~ (0U != (7U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated))))) 
                 & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated) 
                       >> 3U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l197 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                    >> 8U)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId 
        = (1U & ((~ (0U != (7U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))))) 
                 & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids) 
                       >> 3U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99 = (IData)(
                                                        (1U 
                                                         == 
                                                         (3U 
                                                          & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid) 
              & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask 
        = (0x0000000fU & (~ ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
                               << 3U) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid) 
                                         << 2U)) | 
                             (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid) 
                               << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid)))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__13(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__13\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_firstFree 
        = ((2U & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_buffer_firstFree_6) 
                   | ((~ (0U != (3U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated))))) 
                      & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated) 
                            >> 2U)))) << 1U)) | (1U 
                                                 & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_buffer_firstFree_6) 
                                                    | (IData)(
                                                              (1U 
                                                               == 
                                                               (3U 
                                                                & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated)))))));
    vlSelfRef.__PVT__vexiis_0_iBus_bus_a_rValid = vlSelfRef.__Vdly__vexiis_0_iBus_bus_a_rValid;
    vlSelfRef.__PVT__vexiis_0_dBus_bus_a_rValid = vlSelfRef.__Vdly__vexiis_0_dBus_bus_a_rValid;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4 
        = ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId) 
             << 3U) | (4U & (((~ (0U != (3U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))))) 
                              & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids) 
                                    >> 2U))) << 2U))) 
           | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99) 
               << 1U) | (1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready 
        = (1U & (~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted)) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId 
        = (IData)((2U == (3U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1 
        = (1U & ((~ (0U != (3U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask)))) 
                 & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask) 
                    >> 2U)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask) 
                    >> 3U) & (~ (0U != (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId 
        = (((0U != (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4) 
                          >> 2U))) << 1U) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99)));
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid = 0U;
    } else if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_ups_1_d_valid;
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__14(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__14\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rValid 
        = ((1U & (~ (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1))) 
           && ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source) 
                   >> 2U)) & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid)));
    vlSelfRef.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid 
        = ((1U & (~ (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1))) 
           && (IData)(((0U == (0x18U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source))) 
                       & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid))));
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid = 0U;
    } else {
        if (vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46))) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid = 0U;
        }
    }
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000003fU & ((((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                            << 5U) | (((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                       << 4U) | ((IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid) 
                                                 << 3U))) 
                          | (((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                              << 2U) | (((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                         << 1U) | (IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid)))));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1) 
                   << 2U) | (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                              << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2))))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (7U & (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 3U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    if (vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__locked) {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2));
    } else {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 1U));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 2U));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45 = ((IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46 = ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param 
        = (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2) 
            << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__15(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__15\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__Vdly__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch;
    vlSelfRef.__Vdly__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__logic_time 
        = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time;
    vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_d_tracker_beat 
        = vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_beat;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter;
    vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_beat;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len;
    vlSelfRef.__Vdly__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value 
        = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value;
    vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__factory_unburstify_counter 
        = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_counter;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__litex_reset)))) {
        if (VL_UNLIKELY((((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
                          & (~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT___zz_a_logic_2_hit) 
                                | ((0x0000000080010000ULL 
                                    == (0x0000000080810000ULL 
                                        & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)) 
                                   | (0x0000000000800000ULL 
                                      == (0x0000000001800000ULL 
                                          & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key))))))))) {
            VL_WRITEF_NX("FAILURE Tilelink decoder miss ???\n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 7222, "");
        }
        if (VL_UNLIKELY((((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
                          & (1U != (3U & (0xe994U >> 
                                          ((((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_2_a_valid) 
                                             << 3U) 
                                            | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid) 
                                               << 2U)) 
                                           | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_0_a_valid) 
                                              << 1U))))))))) {
            VL_WRITEF_NX("FAILURE Tilelink decoder miss ???\n",0);
            VL_FINISH_MT("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.v", 7232, "");
        }
    }
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter;
    vlSelfRef.__Vdly__dma_bus_ar_rValid = vlSelfRef.__PVT__dma_bus_ar_rValid;
    vlSelfRef.__Vdly__dma_bridge_up_b_rValid = vlSelfRef.__PVT__dma_bridge_up_b_rValid;
    vlSelfRef.__Vdly__dma_bus_aw_rValid = vlSelfRef.__PVT__dma_bus_aw_rValid;
    vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_down_d_tracker_beat;
    vlSelfRef.__Vdly__dma_filter_logic_core__DOT__errored 
        = vlSelfRef.__PVT__dma_filter_logic_core__DOT__errored;
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter;
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd;
    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp;
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat;
    vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__d_counter 
        = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header;
    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups 
        = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups;
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__16(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__16\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__Vdly__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
        vlSelfRef.__Vdly__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch = 0U;
        vlSelfRef.__Vdly__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
        vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__logic_time = 0ULL;
        vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_d_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter = 0U;
        vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_a_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len = 0U;
        vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__factory_unburstify_counter = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = 0U;
        vlSelfRef.__Vdly__dma_bus_ar_rValid = 0U;
        vlSelfRef.__Vdly__dma_bridge_up_b_rValid = 0U;
        vlSelfRef.__Vdly__dma_bus_aw_rValid = 0U;
        vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_down_d_tracker_beat = 0U;
        vlSelfRef.__Vdly__dma_filter_logic_core__DOT__errored = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid = 0U;
    } else {
        if (vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire) {
            vlSelfRef.__Vdly__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) {
                vlSelfRef.__Vdly__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_fire) {
            vlSelfRef.__Vdly__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_last) {
                vlSelfRef.__Vdly__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_fire) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat)));
            if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_last) {
                vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_read_cmd_valid) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch)));
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_read_cmd_valid) {
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch)));
        }
        if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_fire) {
            vlSelfRef.__Vdly__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat)));
            if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) {
                vlSelfRef.__Vdly__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = 0U;
            }
            vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_a_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_beat)));
            if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_last) {
                vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_a_tracker_beat = 0U;
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_priv_stoptime_regNext)))) {
            vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__logic_time 
                = (1ULL + vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time);
        }
        if (vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid) {
            vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_d_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_beat)));
            if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_last) {
                vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_d_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid) {
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter)));
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat)));
            if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last) {
                vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter = 0U;
                vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
            if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked) {
                vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter)));
                if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST) {
                    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter = 0U;
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire) {
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter)));
            if (vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last) {
                vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len)));
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last) {
                vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len = 0U;
            }
        }
        if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19) {
            vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__factory_unburstify_counter 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_counter)));
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94) 
                 & (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core_io_bus_a_ready))) {
                vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__factory_unburstify_counter = 0U;
            }
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_2_a_valid) 
             & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_a_ready))) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat)));
            if ((1U & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                       | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat) 
                          == (0x0000000fU & (0xff731000U 
                                             >> ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size) 
                                                 << 2U))))))) {
                vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat = 0U;
            }
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid))) {
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)));
            if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST) {
                vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = 0U;
            }
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid))) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)));
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST) {
                vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = 0U;
            }
        }
        if ((5U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r))) {
            vlSelfRef.__Vdly__dma_bus_ar_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bus_ar_rValid) 
             & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready) 
                & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready)))) {
            vlSelfRef.__Vdly__dma_bus_ar_rValid = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid) {
            vlSelfRef.__Vdly__dma_bridge_up_b_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid) 
             & (4U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r)))) {
            vlSelfRef.__Vdly__dma_bridge_up_b_rValid = 0U;
        }
        if ((2U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r))) {
            vlSelfRef.__Vdly__dma_bus_aw_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bus_aw_rValid) 
             & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready) 
                & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready)))) {
            vlSelfRef.__Vdly__dma_bus_aw_rValid = 0U;
        }
        if (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid) 
             & (~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)))) {
            vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_down_d_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_down_d_tracker_beat)));
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49) 
                 | ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_down_d_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size) 
                                           << 2U)))))) {
                vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_down_d_tracker_beat = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__start) {
            vlSelfRef.__Vdly__dma_filter_logic_core__DOT__errored = 1U;
        }
        if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt) {
            if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_last) {
                vlSelfRef.__Vdly__dma_filter_logic_core__DOT__errored = 0U;
            }
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready) 
             & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid))) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter)));
            if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_fire) {
                vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter = 0U;
            }
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_valid) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready) 
             & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid))) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid = 0U;
        }
    }
    vlSelfRef.__Vdly__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value 
        = ((1U & (~ (IData)(vlSelfRef.__PVT__litex_reset))) 
           && (1U & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_willIncrement) 
                     + (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value))));
}
