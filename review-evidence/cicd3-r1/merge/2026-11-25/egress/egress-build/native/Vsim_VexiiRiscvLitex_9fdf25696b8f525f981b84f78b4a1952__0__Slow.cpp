// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l164 
        = (1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l197 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                    >> 8U)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_1 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_2 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_3 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_4 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_5 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_6 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_7 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_8 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_9 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_10 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_11 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_12 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_13 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_14 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_15 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_16 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_17 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_18 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_19 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_20 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_21 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_22 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_23 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_24 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_25 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_26 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_27 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_28 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_29 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_30 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_payload_offset 
        = (3U & ((~ ((0x000000ffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size))) 
                     - (IData)(1U))) & vlSelfRef.__PVT__dma_bus_aw_rData_addr));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counterPlus 
        = (7U & ((IData)(1U) + ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat) 
                                + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_1 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter) 
           == (1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_2 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter) 
           == (2U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_3 
        = ((3U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat))) 
           == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid));
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats 
        = (0x00007fffU & ((3U & ((~ (((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size)) 
                                     - (IData)(1U))) 
                                 & vlSelfRef.__PVT__dma_bus_aw_rData_addr)) 
                          + (((IData)(vlSelfRef.__PVT__dma_bus_aw_rData_len) 
                              << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size)) 
                             + (3U & (0x0034U >> ((IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size) 
                                                  << 1U))))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_payload_header 
        = (0x0000000fU & (((vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_addr 
                            - (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)) 
                           >> 2U) & (- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST)))));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_last 
        = (1U & ((~ ((1U == (1U & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get))))) 
                     | (5U == (1U & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get))))))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats 
        = (0x00007fffU & ((3U & ((~ (((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size)) 
                                     - (IData)(1U))) 
                                 & vlSelfRef.__PVT__dma_bus_ar_rData_addr)) 
                          + (((IData)(vlSelfRef.__PVT__dma_bus_ar_rData_len) 
                              << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size)) 
                             + (3U & (0x0034U >> ((IData)(vlSelfRef.__PVT__dma_bus_ar_rData_size) 
                                                  << 1U))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_hit_mem_port 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                    >> 8U) & ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid)
                               ? ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rData_sink) 
                                  >> 8U) : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                                            >> 0x00000010U))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error 
        = ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
            ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_error)
            : ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
                ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_error)
                : ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
                    ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_error)
                    : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_error))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error 
        = ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
            ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_error)
            : ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
                ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_error)
                : ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
                    ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_error)
                    : (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_error))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd) 
           != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd) 
           != (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param = 0U;
    if ((1U & (~ vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1))) {
        if ((1U & (~ (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                      >> 0x0000000eU)))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param 
                = ((0x00008000U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)
                    ? 0U : 1U);
        }
    }
    vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid 
        = ((~ ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_cmdSent) 
               | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_victim))) 
           & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_valid));
    if ((0x00000100U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_write_payload_address 
            = (0x000000ffU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address 
                              >> 6U));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address 
            = (0x000000ffU & ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid)
                               ? (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rData_sink)
                               : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                                  >> 6U)));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_write_payload_address 
            = (0x000000ffU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address 
            = (0x000000ffU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter));
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                    >> (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_id))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask 
        = (0x0000000fU & (~ ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
                               << 3U) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid) 
                                         << 2U)) | 
                             (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid) 
                               << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_buffer_firstFree_6 
        = (1U & ((~ (0U != (7U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated))))) 
                 & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated) 
                       >> 3U))));
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
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter) 
           == (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1) 
                              >> 9U)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitOh_3 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_set) 
              == (0x000000ffU & (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                                 >> 6U))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart 
        = (0x0000000fU & ((- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))) 
                          & (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart 
        = (0x0000000fU & ((- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))) 
                          & (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                    >> (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_id))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId 
        = (1U & ((~ (0U != (7U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))))) 
                 & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids) 
                       >> 3U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99 = (IData)(
                                                        (1U 
                                                         == 
                                                         (3U 
                                                          & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))));
    vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter) 
           == (0x000000ffU & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_opcode;
    if ((1U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode = 6U;
    } else if ((1U & (~ (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                         >> 0x0000000eU)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode = 5U;
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus 
        = (7U & ((IData)(1U) + ((3U & (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1) 
                                        >> 0x0000000aU) 
                                       & (- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_first))))) 
                                + ((3U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1) 
                                          >> 8U)) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter)))));
    vlSelfRef.__PVT__dma_bus_wlast = ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__chunk_r) 
                                      == (0x0000001fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__count_r))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_len) 
           == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 
        = ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
            ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_done)
            : ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
                ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_done)
                : ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))
                    ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_done)
                    : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_done))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD 
        = ((7U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
           | ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_FROM_NONE)) 
              & (6U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1)))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rValid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 
        = ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
            ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_done)
            : ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
                ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_done)
                : ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))
                    ? (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_done)
                    : (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_done))));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
        = (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
           + ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_len) 
              << 2U));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid) 
              & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
        = (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
           + ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_len) 
              << 2U));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats 
        = ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode)) 
           | (1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassData)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem_spinal_port1));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid) 
                    & (0U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic_io_targets 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_threshold_driver) 
           < (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_priority));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47 = ((1U 
                                                  == 
                                                  (7U 
                                                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
                                                 | (0U 
                                                    == 
                                                    (7U 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__errored) 
                    | (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire 
        = ((7U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode)) 
           | (6U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode)));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000003fU & ((((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                            << 5U) | (((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                       << 4U) | ((IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid) 
                                                 << 3U))) 
                          | (((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                              << 2U) | (((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                         << 1U) | (IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110 = (1U 
                                                  & (~ 
                                                     ((~ 
                                                       ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip) 
                                                        & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_0_driver))) 
                                                      | (0U 
                                                         >= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver)))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 
        = ((((2U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                    << 1U)) | (1U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                     >> 1U))) << 6U) 
           | ((0x00000020U & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                              << 3U)) | (0x00000010U 
                                         & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                            << 1U))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 
        = ((((2U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                    << 1U)) | (1U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                     >> 1U))) << 6U) 
           | ((0x00000020U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                              << 3U)) | (0x00000010U 
                                         & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN) 
                                            << 1U))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_2_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_1_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_3_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_2_driver));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98 = ((4U 
                                                  == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)) 
                                                 | (6U 
                                                    == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_4_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_3_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_5_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_4_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_6_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_5_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_7_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_6_driver));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit 
        = ((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
            >> 0x0000000eU) & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired) 
                                   | vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)) 
                               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_LAST)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_8_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_7_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_9_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_8_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_10_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_9_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_11_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_10_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_12_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_11_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_13_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_12_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_14_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_13_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_15_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_14_driver));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11 = ((0U 
                                                  == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                                 | (1U 
                                                    == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)));
    vlSelfRef.__PVT__pBus_awaddr = (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_address 
                                    | (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter) 
                                        | (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat)) 
                                       << 2U));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter) 
           == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size) 
                                              << 2U))));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_15_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_16_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_17_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_18_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_19_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_20_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_21_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_22_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_23_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_24_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_25_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_26_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_27_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_28_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_29_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_30_driver));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full 
        = (0U == (4U ^ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd) 
                        ^ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full 
        = (0U == (4U ^ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd) 
                        ^ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_header) 
           == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_TO_DOWN) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit 
        = (IData)((0x00000041U == (0x00000041U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)));
    vlSelfRef.__PVT__litex_reset = (((IData)(vlSymsp->TOP.sys_reset) 
                                     | (IData)(vlSymsp->TOP__sim.__PVT__soc_soc_rst)) 
                                    | ((IData)(vlSymsp->TOP__sim.__PVT__soc_reset_storage) 
                                       >> 1U));
    vlSelfRef.__PVT__dma_bus_rready = ((IData)(vlSymsp->TOP__sim.__VdfgRegularize_h6e95ff9d_0_101) 
                                       & (6U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r)));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready 
        = ((4U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode))
            ? (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_ar_ready)
            : (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_aw_ready));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge_io_down_ar_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bus_ar_rValid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId 
        = (IData)((2U == (3U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1 
        = (1U & ((~ (0U != (3U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask)))) 
                 & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask) 
                    >> 2U)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask) 
                    >> 3U) & (~ (0U != (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask))))));
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
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bus_aw_rValid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4 
        = ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId) 
             << 3U) | (4U & (((~ (0U != (3U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids))))) 
                              & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids) 
                                    >> 2U))) << 2U))) 
           | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99) 
               << 1U) | (1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids)))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid)) 
                 | ((IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN) 
                    & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last) 
                       | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus) 
                          >> 2U)))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l66 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1));
    vlSelfRef.__PVT__pBus_awvalid = ((4U != (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                     & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid));
    vlSelfRef.__PVT__pBus_arvalid = ((4U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                     & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
           == (0x0000003fU & ((vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                               >> 6U) - (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                                         >> 6U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready 
        = (1U & (~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted)) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
           == (0x0000003fU & ((vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                               >> 6U) - (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                                         >> 6U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard 
        = ((0x0000000fU == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_target_mem_port 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp)) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
              >> 8U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103 = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassValid)
                                                    ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassData)
                                                    : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem_spinal_port1)) 
                                                  == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_a_ready 
        = ((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_claim 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_id) 
           & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic_io_targets))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority) 
                                                & ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done) 
                                                     << 3U) 
                                                    | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done) 
                                                       << 2U)) 
                                                   | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done) 
                                                       << 1U) 
                                                      | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire) 
           & (2U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire) 
           & (8U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_source)));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1) 
                   << 2U) | (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                              << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2))))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver) 
           & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_3_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_2_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_6 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_5_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_4_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_9 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_7_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_6_valid))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_12 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_9_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_8_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_15 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_11_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_10_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_18 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_13_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_12_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_21 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_15_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_14_valid))));
    vlSelfRef.__PVT__pBus_wvalid = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11) 
                                    & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid 
        = ((IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_r_valid) 
           | ((IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_b_valid) 
              & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB)));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_24 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_27 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_30 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_33 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_36 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_39 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_42 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_45 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid))));
    vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid) 
           & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone)) 
              | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone))));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000000fU & ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
           & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired)) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired) 
                                                  | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit));
    vlSelfRef.__PVT__dma_bus_wready = ((~ (IData)(vlSelfRef.__PVT__litex_reset)) 
                                       & (IData)(vlSelfRef.__PVT__dma_bus_w_rValidN));
    vlSelfRef.__PVT__dma_bus_awready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_aw_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
    vlSelfRef.__PVT__dma_bus_arready = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bus_ar_rValid) 
                                                 | (IData)(vlSelfRef.__PVT__litex_reset))));
    vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__dma_bus_rready)));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready 
        = (((4U != (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
            | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter) 
               == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_size) 
                                                  << 2U))))) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_lockedValue)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_firstFree));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId 
        = (((0U != (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4) 
                          >> 2U))) << 1U) | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output 
        = (1U & (~ ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready)) 
                    & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid = 0U;
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219) {
        if ((1U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424 = 0U;
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST)))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424 = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd 
        = (0x0000000fU & ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                          | (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd 
        = (0x0000000fU & ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                          | (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                             >> 2U)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_2 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid) 
           & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard)) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                     >> 8U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done) 
              | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_0_to_5 
        = ((0U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask 
        = (1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask)));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask = 1U;
    }
    if ((0U != (0x81000000U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask = 0U;
    }
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (7U & (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 3U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_6) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_8 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_4_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_8 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_5_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_9) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_11 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_6_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_11 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_7_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_priority_driver;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid) 
            << 1U) | (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_12) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_14 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_8_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_13 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_14 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_9_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_13 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_15) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_17 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_10_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_16 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_17 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_11_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_16 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_18) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_20 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_12_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_19 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_20 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_13_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_19 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_21) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_23 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_14_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_22 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_23 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_15_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_22 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_priority_driver;
    }
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000003fU & ((((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid) 
                            << 5U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
                                       << 4U) | ((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid) 
                                                 << 3U))) 
                          | (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid) 
                              << 2U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
                                         << 1U) | (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid)))));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_24) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_27) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_30) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_33) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_36) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_39) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_42) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_45) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver;
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask;
    __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask = 0;
    CData/*3:0*/ __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask;
    __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask = 0;
    CData/*3:0*/ __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2;
    __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_100;
    __VdfgRegularize_h6e95ff9d_0_100 = 0;
    // Body
    __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                   << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1)))) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid)) 
           & (5U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_param)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId 
        = (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid)
                  ? (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                     >> 7U) : (((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid) 
                                  & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_set) 
                                     == (0x000000ffU 
                                         & (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                                            >> 6U)))) 
                                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitOh_3)) 
                                << 1U) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid) 
                                           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_set) 
                                              == (0x000000ffU 
                                                  & (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                                                     >> 6U)))) 
                                          | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitOh_3)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_valid 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_fire 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready = 1U;
    if (((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready)) 
         & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0))) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready = 0U;
    }
    if (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1) 
         & ((~ (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_w_ready)) 
            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)))) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready = 0U;
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor_io_down_aw_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ID 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotReg)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked));
    __VdfgRegularize_h6e95ff9d_0_100 = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1)) 
                                              | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid) 
                                                 & (IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1)))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready = 0U;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready = 0U;
    }
    __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
           ^ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart));
    __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
           ^ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_stages_1_valid 
        = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard) 
                  | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST))))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_stages_1_valid = 0U;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_stages_1_valid = 0U;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1 
        = ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted) 
               | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh 
        = (((((IData)((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2) 
                        >> 3U) & (~ (IData)((0U != 
                                             (7U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))))))) 
              << 3U) | (4U & (((~ (0U != (3U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)))) 
                               << 2U) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)))) 
            | (((IData)((2U == (3U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)))) 
                << 1U) | (1U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)))) 
           | (((((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done) 
                     | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_0_to_5))) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done)) 
                << 3U) | (((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_0_to_5)) 
                           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done)) 
                          << 2U)) | ((((~ ((0U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)) 
                                           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done))) 
                                       & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done)) 
                                      << 1U) | ((~ 
                                                 (0U 
                                                  != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) 
                                                & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_48 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_2_valid)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_3_valid))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_11)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_8) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1) 
                    >> 1U) & (~ (1U & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1) 
                                        - (IData)(1U)) 
                                       >> 1U)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_54 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_17)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_14) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_16) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_13)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_57 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_23)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_20) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_22) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_19)))));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1) 
                   << 2U) | (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0) 
                              << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2))))) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_60 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_63 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_66 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_69 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43)))));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000000fU & ((((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid))));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (3U & (((IData)(__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 2U) | (IData)(__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext 
        = (1U & (~ ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))
                     ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending)
                     : ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))
                         ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending)
                         : ((2U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId))
                             ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending)
                             : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toBackend_valid 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_0)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid) 
            << 2U) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid) 
                       << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_valid 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN)) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid = 0U;
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_isFiring 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_100)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid) 
                    & (IData)(__VdfgRegularize_h6e95ff9d_0_100))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid)) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_mask 
        = ((((4U & ((IData)(__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                    >> 1U)) | (((0U != (3U & ((IData)(__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                                              >> 2U))) 
                                << 1U) | (0U != (7U 
                                                 & ((IData)(__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                                                    >> 1U))))) 
            << 3U) | (((0U != (IData)(__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask)) 
                       << 2U) | (3U & ((0x0034U >> 
                                        ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_size) 
                                         << 1U)) | 
                                       (- (IData)((0U 
                                                   != (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_len))))))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_mask 
        = ((((4U & ((IData)(__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                    >> 1U)) | (((0U != (3U & ((IData)(__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                                              >> 2U))) 
                                << 1U) | (0U != (7U 
                                                 & ((IData)(__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask) 
                                                    >> 1U))))) 
            << 3U) | (((0U != (IData)(__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask)) 
                       << 2U) | (3U & ((0x0034U >> 
                                        ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_size) 
                                         << 1U)) | 
                                       (- (IData)((0U 
                                                   != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_len))))))));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2;
    __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 = 0;
    CData/*2:0*/ __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3;
    __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3 = 0;
    // Body
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_PROBE_ID 
        = (((0U != (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                          >> 2U))) << 1U) | (IData)(
                                                    (0U 
                                                     != 
                                                     (0x0aU 
                                                      & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_106 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready) 
                                                  & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid) 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests)) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45 = ((IData)(vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46 = ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rValid) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1));
    vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2))));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param 
        = (((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2) 
            << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_48)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_54) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_14;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_13;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_17;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_16;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_57) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_20;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_19;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_23;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_22;
    }
    __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3 
        = (7U & (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 3U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2)));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_60) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_62 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_61 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_62 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_61 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_63) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_65 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_64 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_65 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_64 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_66) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_68 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_67 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_68 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_67 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_69) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_71 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_70 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_71 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_70 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46;
    }
    __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                   << 1U) | (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1)))) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
    if (vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__locked) {
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1));
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0));
    } else {
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 1U));
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockSel)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toBackend_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1 
        = ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_read_cmd_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_read_cmd_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START 
        = (0x0000003fU & (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                          & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_mask)) 
                             & (- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END 
        = (0x0000003fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_mask) 
                          | ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                             | vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START 
        = (0x0000003fU & (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                          & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_mask)) 
                             & (- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END 
        = (0x0000003fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_mask) 
                          | ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                             | vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd)));
    if ((0x00000100U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid) 
                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready)));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3 
            = (1U & ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid) 
                     | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire)));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4 
            = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                        >> 8U)));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3 
            = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                        >> 8U)));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20 = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready)) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready)));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45) 
           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46) 
              | ((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2))));
    if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_opcode;
    } else if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source = 8U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_opcode;
    } else {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_data;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source 
            = (0x00000010U | (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_source));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_mask;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_opcode;
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_72 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_8)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_11))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55)))));
    if (vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__locked) {
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1));
    } else {
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2 
            = (1U & ((IData)(__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 2U));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1 
            = (1U & ((IData)(__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 1U));
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_76 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_65)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_62) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_64) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_61)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_78 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_71)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_68) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_70) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_67)))));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (3U & (((IData)(__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 2U) | (IData)(__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_source 
        = ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0))))) 
           & (4U | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SLOT_ID)));
    if (vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0) {
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
            = vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_data;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size 
            = vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_size;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
            = vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_address;
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid;
    } else {
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_data;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SIZE;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
            = ((0xffffffc0U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS) 
               | ((0x0000003cU & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_first)
                                    ? (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS 
                                       >> 2U) : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_base)) 
                                  << 2U)) | (3U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS)));
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = 0U;
    }
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
            ? (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_opcode)
            : ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_WRITE_DATA)
                ? (1U & (- (IData)((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PARTIAL_DATA))))
                : 4U));
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toBackend_valid;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE = 6U;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA 
            = ((5U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)) 
               | (7U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS 
            = (((IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                         >> 9U)) << 6U) | ((0x0000003cU 
                                            & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter) 
                                                + (IData)(
                                                          (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                                           >> 5U))) 
                                               << 2U)) 
                                           | (3U & (IData)(
                                                           (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                                                            >> 3U)))));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid 
            = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE 
            = (7U & (IData)((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 
                             >> 0x00000023U)));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA 
            = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)) 
           & ((6U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
              | (4U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1)))));
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_1));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_2));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1) 
                     >> 1U));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1) 
                     >> 2U));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_hit 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_write_payload_address) 
              == (0x000000ffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)
                                  ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_readAddressBuffer)
                                  : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                                     >> 6U)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
           & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last 
        = (1U & ((~ ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)) 
                     | (1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)))) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_72)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_hit 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address) 
              == (0x000000ffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)
                                  ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_readAddressBuffer)
                                  : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                                     >> 6U)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid 
        = (((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid) 
            & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0)) 
           | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
               & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1)) 
              | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2) 
                 & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid))));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param 
        = (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2) 
            << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1));
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_76) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_62;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_61;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_65;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_64;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_78) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_68;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_67;
    } else {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_71;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_70;
    }
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__locked) {
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0));
    } else {
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 
            = (1U & ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 1U));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3));
    }
    vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
           | ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid)));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_last 
        = ((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_counter) 
           == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size) 
                                              << 2U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55 = (0x00003fffU 
                                                 & ((vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     >> 2U) 
                                                    | (0x3fffffffU 
                                                       & (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_counter))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data = 0U;
    if (((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U)))) 
               | (0x00001000U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
             | (0x0000000cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
            | (0x00000010U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
           | (0x00000014U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
          | (0x00000018U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
         | (0x0000001cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U)))))) {
        if ((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                   - (IData)(0xf0c00000U))))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver));
        } else if ((0x00001000U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0xfffffe01U & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip) 
                          << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip) 
                                    << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip))) 
                       << 5U) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip) 
                                    << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip) 
                                              << 2U)) 
                                  | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip) 
                                      << 1U) | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip))) 
                                 << 1U)));
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0xfffe01ffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip) 
                          << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip) 
                                    << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip))) 
                       << 0x0000000dU) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip) 
                                             << 3U) 
                                            | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip) 
                                               << 2U)) 
                                           | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip))) 
                                          << 9U)));
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0xfe01ffffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip) 
                          << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip) 
                                    << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip))) 
                       << 0x00000015U) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip) 
                                             << 3U) 
                                            | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip) 
                                               << 2U)) 
                                           | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip))) 
                                          << 0x00000011U)));
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0x01ffffffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip) 
                         << 6U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip) 
                                    << 5U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip) 
                                              << 4U))) 
                       | ((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip)))) 
                      << 0x00000019U));
        } else {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
                = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
                   | ((8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))
                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver)
                       : ((0x0000000cU == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver)
                           : ((0x00000010U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                               ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver)
                               : ((0x00000014U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))
                                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver)
                                   : ((0x00000018U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_priority_driver)
                                       : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_priority_driver)))))));
        }
    } else if (((((((((0x00000020U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                      | (0x00000024U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                     | (0x00000028U == (0x003ffffcU 
                                        & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) 
                    | (0x0000002cU == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                   | (0x00000030U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x00000034U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000038U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x0000003cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U)))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((0x00000020U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_priority_driver)
                   : ((0x00000024U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))
                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_priority_driver)
                       : ((0x00000028U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_priority_driver)
                           : ((0x0000002cU == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                               ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_priority_driver)
                               : ((0x00000030U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))
                                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_priority_driver)
                                   : ((0x00000034U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_priority_driver)
                                       : ((0x00000038U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_priority_driver)
                                           : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_priority_driver)))))))));
    } else if (((((((((0x00000040U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                      | (0x00000044U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                     | (0x00000048U == (0x003ffffcU 
                                        & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) 
                    | (0x0000004cU == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                   | (0x00000050U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x00000054U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000058U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x0000005cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U)))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((0x00000040U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver)
                   : ((0x00000044U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))
                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver)
                       : ((0x00000048U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver)
                           : ((0x0000004cU == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                               ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver)
                               : ((0x00000050U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))
                                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver)
                                   : ((0x00000054U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver)
                                       : ((0x00000058U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver)
                                           : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver)))))))));
    } else if (((((((((0x00000060U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                      | (0x00000064U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                     | (0x00000068U == (0x003ffffcU 
                                        & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) 
                    | (0x0000006cU == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                   | (0x00000070U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x00000074U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000078U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x0000007cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U)))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver)
                   : ((0x00000064U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))
                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver)
                       : ((0x00000068U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver)
                           : ((0x0000006cU == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                               ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver)
                               : ((0x00000070U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))
                                   ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver)
                                   : ((0x00000074U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))
                                       ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver)
                                       : ((0x00000078U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))
                                           ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver)
                                           : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver)))))))));
    } else if ((0x00200000U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffffffcU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_threshold_driver));
    } else if ((0x00200004U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xffffffe0U & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_claim));
    } else if ((0x00002000U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffffe01U & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_7_driver) 
                      << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_6_driver) 
                                << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_5_driver) 
                                            << 1U) 
                                           | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_4_driver))) 
                   << 5U) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_3_driver) 
                                << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_2_driver) 
                                          << 2U)) | 
                              (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_1_driver) 
                                << 1U) | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_0_driver))) 
                             << 1U)));
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfffe01ffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_15_driver) 
                      << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_14_driver) 
                                << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_13_driver) 
                                            << 1U) 
                                           | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_12_driver))) 
                   << 0x0000000dU) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_11_driver) 
                                         << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_10_driver) 
                                                   << 2U)) 
                                       | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_9_driver) 
                                           << 1U) | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_8_driver))) 
                                      << 9U)));
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0xfe01ffffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | ((((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_23_driver) 
                      << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_22_driver) 
                                << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_21_driver) 
                                            << 1U) 
                                           | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_20_driver))) 
                   << 0x00000015U) | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_19_driver) 
                                         << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_18_driver) 
                                                   << 2U)) 
                                       | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_17_driver) 
                                           << 1U) | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_16_driver))) 
                                      << 0x00000011U)));
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data 
            = ((0x01ffffffU & vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data) 
               | (((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_30_driver) 
                     << 6U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_29_driver) 
                                << 5U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_28_driver) 
                                          << 4U))) 
                   | ((((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_27_driver) 
                        << 3U) | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_26_driver) 
                                  << 2U)) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_25_driver) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_24_driver)))) 
                  << 0x00000019U));
    }
}
