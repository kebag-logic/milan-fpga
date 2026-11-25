// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9 = ((0U 
                                                 == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
                                                | (1U 
                                                   == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key 
        = (((QData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA) 
            & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter) 
               == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE) 
                                                  << 2U))))) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0) 
            & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid)) 
           | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1)) 
              | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2) 
            << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1));
    vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority))));
    if ((0U == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_data;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_denied));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_size;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_opcode;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rData_source;
    } else if ((1U == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_data;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied 
            = (1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_denied));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_size;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_opcode;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source 
            = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rData_source;
    } else {
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data 
            = vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_r_payload_data;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied 
            = (1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get)
                         ? (0U == (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_r_payload_resp))
                         : (0U == (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_b_payload_resp)))));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = (1U & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get))));
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source 
            = vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_source;
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2)))));
    if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0) {
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source 
            = (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address 
            = ((0xfffff000U & vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_addr) 
               | (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK) 
                   << 6U) | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param 
            = (2U & (- (IData)((0x0fU != (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_cache)))));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size 
            = (7U & ((((0U != (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                              >> 1U))) 
                       << 2U) | (((0U != (3U & (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                                 >> 1U) 
                                                | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                                   >> 5U)))) 
                                  << 1U) | (IData)(
                                                   (0U 
                                                    != 
                                                    (0xaaU 
                                                     & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2)))))) 
                     + ((0U == (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN))
                         ? (3U & (0xa4U >> (6U & (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END) 
                                                   - (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)) 
                                                  << 1U))))
                         : (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_size))));
    } else {
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source 
            = (4U | (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address 
            = ((0xfffff000U & vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_addr) 
               | (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK) 
                   << 6U) | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param 
            = (2U & (- (IData)((0x0fU != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_cache)))));
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size 
            = (7U & ((((0U != (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                              >> 1U))) 
                       << 2U) | (((0U != (3U & (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                                 >> 1U) 
                                                | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2) 
                                                   >> 5U)))) 
                                  << 1U) | (IData)(
                                                   (0U 
                                                    != 
                                                    (0xaaU 
                                                     & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2)))))) 
                     + ((0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN))
                         ? (3U & (0xa4U >> (6U & (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END) 
                                                   - (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START)) 
                                                  << 1U))))
                         : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_size))));
    }
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_data 
        = (((((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_data) 
              << 0x00000018U) | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_data) 
                                 << 0x00000010U)) | 
            (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_data) 
              << 8U) | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_data))) 
           & (- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0))))));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_mask 
        = ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0))))) 
           & (((((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_strb) 
                 << 3U) | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_strb) 
                           << 2U)) | (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_strb) 
                                       << 1U) | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_strb))) 
              & (- (IData)(((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone)) 
                            & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53 = (1U 
                                                 & (~ 
                                                    ((0U 
                                                      == 
                                                      ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                                                        ? 4U
                                                        : 1U)) 
                                                     | (1U 
                                                        == 
                                                        ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                                                          ? 4U
                                                          : 1U)))));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid 
        = (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1) 
            & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid)) 
           | ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0) 
              & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid)));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data = 0U;
    if ((0xbff8U == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                    << 2U)))) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data 
            = (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time);
    } else if ((0xbffcU == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                           << 2U)))) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data 
            = vlSelfRef.__PVT__peripheral_clint_thread_core__DOT___zz_factory_rspAsync_payload_data;
    } else if ((0U == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                      << 2U)))) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data 
            = ((0xfffffffeU & vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data) 
               | (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_softwareInterrupt));
    }
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last 
        = (1U & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_0_a_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
           & (0x0000000080010000ULL == (0x0000000080810000ULL 
                                        & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
           & (0x0000000000800000ULL == (0x0000000001800000ULL 
                                        & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT___zz_a_logic_2_hit 
        = ((0ULL == (0x0000000040000000ULL & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)) 
           | (0ULL == (0x0000000000810000ULL & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96 = (1U 
                                                 & (~ 
                                                    ((0x0000000fU 
                                                      == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids)) 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE))));
    if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_denied;
    } else if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_denied;
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_denied;
    }
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode;
    __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode = 0;
    CData/*0:0*/ __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready;
    __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready = 0;
    CData/*3:0*/ __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last;
    __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last = 0;
    SData/*8:0*/ __PVT__dma_filter_logic_core__DOT__instruction;
    __PVT__dma_filter_logic_core__DOT__instruction = 0;
    CData/*0:0*/ __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit;
    __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_43;
    __VdfgRegularize_h6e95ff9d_0_43 = 0;
    // Body
    if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                              >> 1U));
    } else if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_source));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_source));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48 = (1U 
                                                 & (~ 
                                                    ((1U 
                                                      == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)) 
                                                     | (5U 
                                                        == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)))));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_ups_1_d_valid 
        = (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source) 
            >> 2U) & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53) 
           | ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size) 
                                                 << 2U)))));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53) 
           | ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size) 
                                                 << 2U)))));
    __PVT__dma_filter_logic_core__DOT__instruction 
        = (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param) 
            << 6U) | (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size) 
                       << 3U) | ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0)
                                  ? 4U : 1U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94 = (((4U 
                                                   == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
                                                  | (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_last)) 
                                                 & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_0_a_valid));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askWrite 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askRead 
        = ((4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_2_a_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT___zz_a_logic_2_hit));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp 
        = (2U & (- (IData)(((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied) 
                            | (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)))));
    __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last 
        = (0x0000000fU & (0xff731000U >> (((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)
                                            ? (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__size)
                                            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size)) 
                                          << 2U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49 = (1U 
                                                 & (~ 
                                                    ((1U 
                                                      == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode)) 
                                                     | (5U 
                                                        == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode)))));
    if (vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt) {
        __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode 
            = (7U & (0x00961900U >> ((IData)(3U) * (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__opcode))));
        vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source 
            = (7U & (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__source));
    } else {
        __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode 
            = (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode));
        vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source 
            = (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source));
    }
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid 
        = (IData)(((0x10U == (0x18U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source))) 
                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid)));
    __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready 
        = (1U & ((0U == (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source) 
                               >> 3U))) | ((1U == (3U 
                                                   & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source) 
                                                      >> 3U))) 
                                           | (~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set = 0U;
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set 
            = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set) 
               | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID))));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_0_LAST 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
           | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_6 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4))));
    __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit 
        = ((4U == (7U & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))) 
           | (1U == (7U & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_willIncrement = 0U;
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_willIncrement = 1U;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askWrite) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_willIncrement = 1U;
    }
    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askRead) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_willIncrement = 1U;
    }
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_2_a_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
    __VdfgRegularize_h6e95ff9d_0_43 = (1U & (~ ((1U 
                                                 == (IData)(__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode)) 
                                                | (5U 
                                                   == (IData)(__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode)))));
    vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid 
        = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt) 
           | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid) 
           & (IData)(__PVT__splited_wc_cBus_arbiter_core_io_down_d_ready));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1) 
                    & (IData)(__PVT__splited_wc_cBus_arbiter_core_io_down_d_ready))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2) 
                    & (IData)(__PVT__splited_wc_cBus_arbiter_core_io_down_d_ready))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12_io_inputs_0_ready 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0) 
           & (IData)(__PVT__splited_wc_cBus_arbiter_core_io_down_d_ready));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit 
        = (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
            & (0xf0000000U == (0xffff0000U & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
           | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
               & (0x01000000U == (0xff000000U & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
              | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                  & (0x80000000U == (0xffff8000U & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                 | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                     & (0x10030000U == (0xffff8000U 
                                        & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                    | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                        & (0x10020000U == (0xffff0000U 
                                           & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                       | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                           & (0x10000000U == (0xfffe0000U 
                                              & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                          | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                              & (0x00030000U == (0xffff8000U 
                                                 & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                             | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                                 & (0x00020000U == 
                                    (0xffff0000U & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                                | (((IData)(__PVT__dma_filter_logic_core__DOT__argsHits_2_argHit) 
                                    & (0U == (0xfffe0000U 
                                              & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                                   | (((4U == (7U & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))) 
                                       & (0xf0010000U 
                                          == (0xffff0000U 
                                              & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address))) 
                                      | (((4U == (0x0037U 
                                                  & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))) 
                                          | (4U == 
                                             (0x002fU 
                                              & (IData)(__PVT__dma_filter_logic_core__DOT__instruction)))) 
                                         & (0xf0c00000U 
                                            == (0xffc00000U 
                                                & vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address)))))))))))));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire 
        = ((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_43) 
           | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat) 
              == (IData)(__PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last)));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_last 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_43) 
           | ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_beat) 
              == (IData)(__PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last)));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source) 
               >> 2U)) & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_1_d_valid 
        = (((IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source) 
            >> 2U) & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12_io_inputs_0_ready) 
                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102))) 
                 | ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready)) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit))));
    vlSelfRef.__PVT__dma_filter_logic_core_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit) 
           & ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready) 
              & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid)));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__peripheral_bus_arbiter_core_io_down_d_ready;
    __PVT__peripheral_bus_arbiter_core_io_down_d_ready = 0;
    CData/*0:0*/ __PVT__dma_filter_logic_core_io_up_a_ready;
    __PVT__dma_filter_logic_core_io_up_a_ready = 0;
    CData/*0:0*/ __PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready;
    __PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready = 0;
    CData/*0:0*/ __PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready;
    __PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready = 0;
    CData/*0:0*/ __PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready;
    __PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready = 0;
    CData/*0:0*/ __PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead;
    __PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_44;
    __VdfgRegularize_h6e95ff9d_0_44 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_97;
    __VdfgRegularize_h6e95ff9d_0_97 = 0;
    // Body
    __PVT__dma_filter_logic_core_io_up_a_ready = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready) 
                                                  & ((~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit)) 
                                                     | (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5))));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_fire 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid) 
           & (IData)(__PVT__dma_filter_logic_core_io_up_a_ready));
    __VdfgRegularize_h6e95ff9d_0_44 = (1U & ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0) 
                                                 & (IData)(__PVT__dma_filter_logic_core_io_up_a_ready))) 
                                             | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid) 
           & ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1) 
              & (IData)(__PVT__dma_filter_logic_core_io_up_a_ready)));
    __PVT__peripheral_bus_arbiter_core_io_down_d_ready 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source) 
                     >> 2U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready)));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__start 
        = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_fire) 
           & ((~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit)) 
              & (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_last)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_44)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid) 
                    & (IData)(__VdfgRegularize_h6e95ff9d_0_44))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42 = (1U 
                                                 & (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2)) 
                                                     & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN)) 
                                                        & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full)))) 
                                                    | ((~ 
                                                        ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last) 
                                                         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready))) 
                                                       | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready = 0U;
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid) {
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone)))) {
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready 
                    = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready;
            }
        }
    }
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_fire 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid) 
           & (IData)(__PVT__peripheral_bus_arbiter_core_io_down_d_ready));
    vlSelfRef.__PVT__pBus_rready = ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2) 
                                    & (IData)(__PVT__peripheral_bus_arbiter_core_io_down_d_ready));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0) 
                    & (IData)(__PVT__peripheral_bus_arbiter_core_io_down_d_ready))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1) 
                    & (IData)(__PVT__peripheral_bus_arbiter_core_io_down_d_ready))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid)) 
                 | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) 
                    & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_cmd_ready = 0U;
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire) {
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_cmd_ready = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_1 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid) 
                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l53 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_firstCycle) 
           | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready) 
              & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid)));
    vlSelfRef.__PVT__dma_bridge_write_bridge_io_up_w_ready 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l66) 
           & ((~ ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready)) 
                  & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid))) 
              & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid)));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_fire 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid) 
           & (IData)(vlSelfRef.__PVT__pBus_rready));
    vlSelfRef.__PVT__pBus_bready = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB)) 
                                          | (IData)(vlSelfRef.__PVT__pBus_rready)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19 = ((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready) 
                                                 & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_0_a_valid));
    vlSelfRef.__PVT__peripheral_clint_thread_core_io_bus_a_ready 
        = (((4U != (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
            | (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_last)) 
           & (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready));
    __PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready 
        = ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value)) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT___zz_1 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge_io_down_ar_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_cmd_ready)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid)) 
                 | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) 
                    & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))));
    vlSelfRef.__PVT__dma_bus_w_s2mPipe_ready = (1U 
                                                & ((~ (IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rValid)) 
                                                   | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_up_w_ready)));
    __PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready 
        = ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_last) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_up_w_ready));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_doWrite 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__when_Clint_l59 = 0U;
    if ((0xbff8U == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                    << 2U)))) {
        if (((4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19))) {
            vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__when_Clint_l59 = 1U;
        }
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askWrite) 
           & (IData)(__PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready));
    __PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askRead) 
           & (IData)(__PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_a_ready 
        = (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT___zz_a_logic_2_hit) 
            & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_a_ready)) 
           | (((0x0000000080010000ULL == (0x0000000080810000ULL 
                                          & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)) 
               & (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core_io_bus_a_ready)) 
              | ((0x0000000000800000ULL == (0x0000000001800000ULL 
                                            & vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key)) 
                 & (IData)(__PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready = 1U;
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready = 0U;
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid)) 
                 | (IData)(__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid)) 
                 | (IData)(__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid = 0U;
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid = 0U;
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload = 0U;
    if ((0x00200004U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                        - (IData)(0xf0c00000U))))) {
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid = 1U;
        }
        if (__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid = 1U;
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload 
                = vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_claim;
        }
    }
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire 
        = ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_a_ready));
    __VdfgRegularize_h6e95ff9d_0_97 = ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1) 
                                           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_a_ready))) 
                                       & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_TO_DOWN));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 1U;
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 0U;
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload 
        = (0x0000001fU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                          & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_isFiring 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_97)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid) 
                                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_97));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_clear = 0U;
    if (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid) 
         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)) 
            & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_LAST) 
               & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_FROM_C)) 
                  & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_WRITE_DATA)))))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_clear 
            = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_clear) 
               | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_BUFFER_ID))));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid) 
                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104))));
    __PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid) 
           & (IData)(__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_ready 
        = (1U & (~ ((~ (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C) 
                         & (IData)(__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready)) 
                        | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98))) 
                    | ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready)) 
                       & (6U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_ready 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready)
            : ((IData)(__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready) 
               & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C)) 
                  & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_5 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring));
    vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_ready) 
                    & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid)))));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l475 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid) 
           | ((4U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)) 
              & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_ready) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_valid))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_ready)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_isFiring 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fire = 0U;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fire = 0U;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fire = 0U;
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fire = 0U;
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_isFiring) {
        if ((1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fire = 1U;
        }
        if ((2U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fire = 1U;
        }
        if ((4U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fire = 1U;
        }
        if ((8U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh))) {
            vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fire = 1U;
        }
    }
}

extern const VlWide<16>/*511:0*/ Vsim__ConstPool__CONST_hcb361019_0;

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__11\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_data 
        = (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_victimBuffer_spinal_port1 
           & (- (IData)((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0))));
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0) {
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_address 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_address;
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_param 
            = (7U & (((0U == (0x0000001fU & ((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique) 
                                               << 8U) 
                                              | (0x00000080U 
                                                 & ((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique)) 
                                                    << 7U))) 
                                             | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique) 
                                                 << 6U) 
                                                | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared) 
                                                   << 5U)))))
                       ? 0U : (Vsim__ConstPool__CONST_hcb361019_0
                               [(((IData)(2U) + ((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique) 
                                                   << 8U) 
                                                  | (0x00000080U 
                                                     & ((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique)) 
                                                        << 7U))) 
                                                 | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique) 
                                                     << 6U) 
                                                    | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared) 
                                                       << 5U)))) 
                                 >> 5U)] << ((IData)(0x00000020U) 
                                             - (0x0000001fU 
                                                & ((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique) 
                                                     << 8U) 
                                                    | (0x00000080U 
                                                       & ((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique)) 
                                                          << 7U))) 
                                                   | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique) 
                                                       << 6U) 
                                                      | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared) 
                                                         << 5U))))))) 
                     | (Vsim__ConstPool__CONST_hcb361019_0
                        [(((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique) 
                             << 8U) | (0x00000080U 
                                       & ((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique)) 
                                          << 7U))) 
                           | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique) 
                               << 6U) | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared) 
                                         << 5U))) >> 5U)] 
                        >> (0x0000001fU & ((((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique) 
                                             << 8U) 
                                            | (0x00000080U 
                                               & ((~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique)) 
                                                  << 7U))) 
                                           | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique) 
                                               << 6U) 
                                              | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared) 
                                                 << 5U)))))));
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode 
            = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_release)
                ? (7U & (6U | (- (IData)((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_dirty)))))
                : 5U);
    } else {
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_address 
            = (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                      [(1U & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))]);
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_param 
            = (7U & (((0U == (0x0000001fU & ((0x00000100U 
                                              & ((IData)(
                                                         (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                          [
                                                          (1U 
                                                           & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                          >> 0x00000020U)) 
                                                 << 8U)) 
                                             | ((0x00000080U 
                                                 & ((IData)(
                                                            (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                             [
                                                             (1U 
                                                              & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                             >> 0x00000021U)) 
                                                    << 7U)) 
                                                | (0x00000060U 
                                                   & ((IData)(
                                                              (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                               [
                                                               (1U 
                                                                & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                               >> 0x00000022U)) 
                                                      << 5U))))))
                       ? 0U : (Vsim__ConstPool__CONST_hcb361019_0
                               [(((IData)(2U) + ((0x00000100U 
                                                  & ((IData)(
                                                             (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                              [
                                                              (1U 
                                                               & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                              >> 0x00000020U)) 
                                                     << 8U)) 
                                                 | ((0x00000080U 
                                                     & ((IData)(
                                                                (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                                 [
                                                                 (1U 
                                                                  & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                                 >> 0x00000021U)) 
                                                        << 7U)) 
                                                    | (0x00000060U 
                                                       & ((IData)(
                                                                  (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                                   [
                                                                   (1U 
                                                                    & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                                   >> 0x00000022U)) 
                                                          << 5U))))) 
                                 >> 5U)] << ((IData)(0x00000020U) 
                                             - (0x0000001fU 
                                                & ((0x00000100U 
                                                    & ((IData)(
                                                               (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                                [
                                                                (1U 
                                                                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                                >> 0x00000020U)) 
                                                       << 8U)) 
                                                   | ((0x00000080U 
                                                       & ((IData)(
                                                                  (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                                   [
                                                                   (1U 
                                                                    & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                                   >> 0x00000021U)) 
                                                          << 7U)) 
                                                      | (0x00000060U 
                                                         & ((IData)(
                                                                    (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                                     [
                                                                     (1U 
                                                                      & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                                     >> 0x00000022U)) 
                                                            << 5U)))))))) 
                     | (Vsim__ConstPool__CONST_hcb361019_0
                        [(((0x00000100U & ((IData)(
                                                   (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                    [
                                                    (1U 
                                                     & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                           | ((0x00000080U & ((IData)(
                                                      (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                       [
                                                       (1U 
                                                        & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                       >> 0x00000021U)) 
                                              << 7U)) 
                              | (0x00000060U & ((IData)(
                                                        (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                         [
                                                         (1U 
                                                          & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                         >> 0x00000022U)) 
                                                << 5U)))) 
                          >> 5U)] >> (0x0000001fU & 
                                      ((0x00000100U 
                                        & ((IData)(
                                                   (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                    [
                                                    (1U 
                                                     & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                                       | ((0x00000080U 
                                           & ((IData)(
                                                      (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                       [
                                                       (1U 
                                                        & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                       >> 0x00000021U)) 
                                              << 7U)) 
                                          | (0x00000060U 
                                             & ((IData)(
                                                        (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block
                                                         [
                                                         (1U 
                                                          & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))] 
                                                         >> 0x00000022U)) 
                                                << 5U))))))));
        vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode = 4U;
    }
    vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid 
        = (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid) 
            & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0)) 
           | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1) 
              & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid)));
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_halfPipe_fire 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready) 
           & (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid));
    vlSelfRef.__PVT__dma_bus_wstrb = (0x0000000fU & 
                                      ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__tail_be_r) 
                                       | (- (IData)(
                                                    (1U 
                                                     & (~ (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__last_word_w)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82 = (1U 
                                                 & (~ 
                                                    ((5U 
                                                      == (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode)) 
                                                     | (7U 
                                                        == (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode)))));
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset_0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset_0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__PVT__litex_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8175657585880426569ull);
    vlSelf->__PVT__peripheral_externalInterrupts_port = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15812319728941706406ull);
    vlSelf->__PVT__dma_bus_awvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3068028795192658043ull);
    vlSelf->__PVT__dma_bus_awready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2352127249982439758ull);
    vlSelf->__PVT__dma_bus_awaddr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12284074195573699580ull);
    vlSelf->__PVT__dma_bus_awid = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1879302294834114566ull);
    vlSelf->__PVT__dma_bus_awregion = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5755714737688337525ull);
    vlSelf->__PVT__dma_bus_awlen = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2980262983242649963ull);
    vlSelf->__PVT__dma_bus_awsize = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11581594885848327144ull);
    vlSelf->__PVT__dma_bus_awburst = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 123538218260935235ull);
    vlSelf->__PVT__dma_bus_awlock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18117956313016560481ull);
    vlSelf->__PVT__dma_bus_awcache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10184681792136234216ull);
    vlSelf->__PVT__dma_bus_awqos = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14658184718223393988ull);
    vlSelf->__PVT__dma_bus_awprot = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11834071688020378423ull);
    vlSelf->__PVT__dma_bus_wvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6987882061887536450ull);
    vlSelf->__PVT__dma_bus_wready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1908016938162420963ull);
    vlSelf->__PVT__dma_bus_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8122892205105671773ull);
    vlSelf->__PVT__dma_bus_wstrb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16819862197172327708ull);
    vlSelf->__PVT__dma_bus_wlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16300632088472650682ull);
    vlSelf->__PVT__dma_bus_bvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10640146641945236849ull);
    vlSelf->__PVT__dma_bus_bready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14733860065517728844ull);
    vlSelf->__PVT__dma_bus_bid = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17232712707964794527ull);
    vlSelf->__PVT__dma_bus_bresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14894710934115336687ull);
    vlSelf->__PVT__dma_bus_arvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1820525773921927807ull);
    vlSelf->__PVT__dma_bus_arready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14856157259204866037ull);
    vlSelf->__PVT__dma_bus_araddr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13532546196077051246ull);
    vlSelf->__PVT__dma_bus_arid = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14487103365876807481ull);
    vlSelf->__PVT__dma_bus_arregion = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17497454945105701502ull);
    vlSelf->__PVT__dma_bus_arlen = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16693208573303395932ull);
    vlSelf->__PVT__dma_bus_arsize = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1719386827977059389ull);
    vlSelf->__PVT__dma_bus_arburst = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6932566368644174837ull);
    vlSelf->__PVT__dma_bus_arlock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17359813896867471708ull);
    vlSelf->__PVT__dma_bus_arcache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14219662228963840334ull);
    vlSelf->__PVT__dma_bus_arqos = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16997064772022274645ull);
    vlSelf->__PVT__dma_bus_arprot = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14697913863928596308ull);
    vlSelf->__PVT__dma_bus_rvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1920468240471168317ull);
    vlSelf->__PVT__dma_bus_rready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 112832418950424734ull);
    vlSelf->__PVT__dma_bus_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1095825781243125240ull);
    vlSelf->__PVT__dma_bus_rid = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17427328220843051858ull);
    vlSelf->__PVT__dma_bus_rresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13069777853912326405ull);
    vlSelf->__PVT__dma_bus_rlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 526288098147464521ull);
    vlSelf->__PVT__pBus_awvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12597699947117630252ull);
    vlSelf->__PVT__pBus_awready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12499855819896636487ull);
    vlSelf->__PVT__pBus_awaddr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16029102956389101459ull);
    vlSelf->__PVT__pBus_awprot = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11976804179086049197ull);
    vlSelf->__PVT__pBus_wvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11812638303567358726ull);
    vlSelf->__PVT__pBus_wready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12050267041490976246ull);
    vlSelf->__PVT__pBus_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10770854034834029395ull);
    vlSelf->__PVT__pBus_wstrb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6246523613048322598ull);
    vlSelf->__PVT__pBus_bvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6175565666126936788ull);
    vlSelf->__PVT__pBus_bready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5682319573112059146ull);
    vlSelf->__PVT__pBus_bresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15013123653568761079ull);
    vlSelf->__PVT__pBus_arvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 396478291728331701ull);
    vlSelf->__PVT__pBus_arready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10741638016122489731ull);
    vlSelf->__PVT__pBus_araddr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9191887123286288090ull);
    vlSelf->__PVT__pBus_arprot = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7278073862216251734ull);
    vlSelf->__PVT__pBus_rvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16164865976986504109ull);
    vlSelf->__PVT__pBus_rready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3343830572234548292ull);
    vlSelf->__PVT__pBus_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8149510844209690183ull);
    vlSelf->__PVT__pBus_rresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 816637978769601760ull);
    vlSelf->__PVT__debug = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8781005679405889265ull);
    vlSelf->__PVT__litex_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7160073992957751673ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17334592715631182607ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8217055657979140242ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17367778681371058418ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16454656110985689612ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14739679538964829377ull);
    vlSelf->__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14114010195704222378ull);
    vlSelf->__PVT__dma_bridge_read_bridge_io_up_r_payload_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 532628078929292937ull);
    vlSelf->__PVT__dma_bridge_read_bridge_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12036208027700032531ull);
    vlSelf->__PVT__dma_bridge_write_bridge_io_up_w_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5401157588973779017ull);
    vlSelf->__PVT__dma_bridge_write_bridge_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15700604437203908527ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11366444746305268366ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_ups_1_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15085249154752241157ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3102091820508504583ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12271668769821889523ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5988630021257861288ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5567513889494037572ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1575768899449836937ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3425004778117730925ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core_io_down_a_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10251124112576277656ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9979213343003669034ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13867128416752507973ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_ups_1_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12712134409948906037ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9595964092029158561ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16928612706087396914ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_payload_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12433364871458554533ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10336552771613027028ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11037781613373045434ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 820615074243497833ull);
    vlSelf->__PVT__dma_filter_logic_core_io_up_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14334051001688192385ull);
    vlSelf->__PVT__dma_filter_logic_core_io_up_d_payload_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10875993820542875747ull);
    vlSelf->__PVT__dma_filter_logic_core_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13267696614233068361ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3045124938294338959ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5800784762987654733ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12897293195929386596ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6270927742659067966ull);
    vlSelf->__PVT__peripheral_clint_thread_core_io_bus_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13060076868328739412ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic_io_targets = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3144621547195125918ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge_io_up_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2310327225678869575ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2763230523311985664ull);
    vlSelf->__PVT__peripheral_bus_decoder_core_io_up_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10703925630183463509ull);
    vlSelf->__PVT__peripheral_bus_decoder_core_io_up_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5821197507087152052ull);
    vlSelf->__PVT__peripheral_bus_decoder_core_io_downs_0_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10415920651871148758ull);
    vlSelf->__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15161251156075115307ull);
    vlSelf->__PVT__peripheral_bus_decoder_core_io_downs_2_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8956283128203992945ull);
    vlSelf->__PVT__vexiis_0_priv_stoptime_regNext = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15130333225192937821ull);
    vlSelf->__PVT___zz_vexiis_0_priv_rdtime = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5488391361322957109ull);
    vlSelf->__PVT__dma_bus_aw_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7362588027218562479ull);
    vlSelf->__PVT__dma_bus_aw_rData_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3978436117229633273ull);
    vlSelf->__PVT__dma_bus_aw_rData_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12046507652066421006ull);
    vlSelf->__PVT__dma_bus_aw_rData_len = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4350252847007881556ull);
    vlSelf->__PVT__dma_bus_aw_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3495868890118480059ull);
    vlSelf->__PVT__dma_bus_aw_rData_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17840286494017066377ull);
    vlSelf->__PVT__dma_bus_w_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 35877343441723653ull);
    vlSelf->__PVT__dma_bus_w_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2842403564634961927ull);
    vlSelf->__PVT__dma_bus_w_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11677849508600865429ull);
    vlSelf->__PVT__dma_bus_w_rData_strb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3050915535460522918ull);
    vlSelf->__PVT__dma_bus_w_rData_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1971911518568985521ull);
    vlSelf->__PVT__dma_bus_w_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7044616480675172145ull);
    vlSelf->__PVT__dma_bus_w_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16800525405260074208ull);
    vlSelf->__PVT__dma_bus_w_s2mPipe_rData_strb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12498625645358772402ull);
    vlSelf->__PVT__dma_bus_w_s2mPipe_rData_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12206145373021856222ull);
    vlSelf->__PVT__dma_bridge_up_b_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9114231944494728101ull);
    vlSelf->__PVT__dma_bridge_up_b_rData_resp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1844073720145192742ull);
    vlSelf->__PVT__dma_bus_ar_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14247104787681125831ull);
    vlSelf->__PVT__dma_bus_ar_rData_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1290738140214116837ull);
    vlSelf->__PVT__dma_bus_ar_rData_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14282923216219255123ull);
    vlSelf->__PVT__dma_bus_ar_rData_len = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4594487134305827696ull);
    vlSelf->__PVT__dma_bus_ar_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11300557538394547429ull);
    vlSelf->__PVT__dma_bus_ar_rData_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14637217971425410272ull);
    vlSelf->__PVT__dma_bridge_up_r_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14080761881815917891ull);
    vlSelf->__PVT__dma_bridge_up_r_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15370825984046760928ull);
    vlSelf->__PVT__dma_bridge_up_r_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2551198175061954676ull);
    vlSelf->__PVT__dma_bridge_up_r_rData_resp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7644965919356181761ull);
    vlSelf->__PVT__dma_bridge_up_r_rData_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10882383604277803174ull);
    vlSelf->__PVT__dma_bridge_up_r_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16725056516274897932ull);
    vlSelf->__PVT__dma_bridge_up_r_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7358141383149135161ull);
    vlSelf->__PVT__dma_bridge_up_r_s2mPipe_rData_resp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6558796487542162453ull);
    vlSelf->__PVT__dma_bridge_up_r_s2mPipe_rData_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5484096732309722793ull);
    vlSelf->__PVT__cpuResetCtrl_fiber_holder_counter = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 11621190247295325044ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13246332274365152647ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18307003232571632561ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12417289795785845086ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10680987138084500002ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6859526058156731659ull);
    vlSelf->__PVT__vexiis_0_dBus_bus_a_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4313445468883062805ull);
    vlSelf->__PVT__vexiis_0_dBus_noDecoder_toDown_d_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6015128027908210517ull);
    vlSelf->__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11064966484543235781ull);
    vlSelf->__PVT__vexiis_0_dBus_noDecoder_toDown_d_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7062233305588546295ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11226549999926155252ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8678340723610602922ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6753100543745849433ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14647428998302371392ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13247210948154874159ull);
    vlSelf->__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17080600204615388665ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5985200236515311034ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9398929126486284586ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 857176230977866886ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7193121835404357565ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4646301699887893726ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_halfPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11510177921196327057ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18208928365902049566ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17830910440248691073ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2506702992662691033ull);
    vlSelf->__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10002833896593687957ull);
    vlSelf->__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16027797673034183202ull);
    vlSelf->__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6956524731102897132ull);
    vlSelf->__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5573451549242245824ull);
    vlSelf->__PVT__vexiis_0_iBus_noDecoder_toDown_d_rData_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17178692314231685625ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5116451276965437594ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8837173833428756717ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8356509633958754816ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7454244563662154558ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 18271424054192235391ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14080654312085518910ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7587967615170589190ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3837574033921854917ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8109655949571618282ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4734809381856481349ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11510096956457847591ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13297280969909049264ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10628468769992957709ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16779037158855796565ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3296370020447596545ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12900524019641417063ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7424616385078320165ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10475756382309176674ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14064941521557787619ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3237577292293837030ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16650705859188133013ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9113385668705684344ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2633403202590238722ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11274951220930573585ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13868538269518006189ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8842759326439368115ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17644764541673251713ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8921424955281327525ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10010711309382993516ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11939122017729301597ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6102274502200118368ull);
    vlSelf->__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 344491559041279298ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_a_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9093970304043340506ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10601203582611115928ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_a_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10972876040027429868ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17124744567900251317ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8146989051563323793ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16231793955350077020ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16454323611904705760ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17708437113276908491ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 14267885171280270659ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8749949176437437813ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1749630546216566503ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3034890312388438736ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9747392714655148240ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_halfPipe_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9647518276123806386ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7976316280812723390ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3652905178213236543ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 196237055178963505ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13010613118699199318ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5007206257865501507ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11586168620779223933ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1640887544469664985ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6381432128046795465ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14376707195198589874ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3384796268323997292ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6064133607107067478ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9288283240564522630ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16075908278055760157ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13365536472736311492ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5086311672153666005ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6270310146110642704ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_e_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8661207907694827613ull);
    vlSelf->__PVT__vexiis_0_lsuL1Bus_bus_e_rData_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 14381619057708771384ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6636036450058609972ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15004657964922124677ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18007242058471862011ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13001957677465577865ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7115894554041146882ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9476266371346419525ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17504265366695017305ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2086894187611898860ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2654214387540765005ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10969854066800058220ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7506267225439027083ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8818859234498752199ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4112886677152080306ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2919634428112785478ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14440521917438149195ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16878385428640954107ull);
    vlSelf->__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17029703198110206173ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6113550845551933780ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18195478195279815962ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor_io_down_aw_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2594083603055175693ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14067599666415987398ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6279419636082158038ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8816402943988447815ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1540593522692033946ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16324513925334204181ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 200393126853626410ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 381109465751898042ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8603694234070175330ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 117055728386513644ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18055740645109126204ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_bytesBeats = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1490335806858272307ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_payload_offset = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4810225314003397700ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4902011617649247149ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16903959477562104903ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5300135762593432188ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_bytePerBeat = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 121812230226028481ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_offset = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3451711966358192974ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7931484511722005286ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rData_bytePerBeat = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12777617992784246286ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17767075347250373303ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_firstCycle = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10817555574108437818ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3286924516696841127ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_0_strb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17274278202263577009ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l53 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5262955335545505719ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2405348786976052498ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_1_strb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12960529710382720118ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9307369754734240288ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_2_strb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11143554534029563294ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15621188471716998700ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_buffer_3_strb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14724959514781086861ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18186951688516199253ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counterPlus = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1033275108029260550ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l66 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12764643844021284801ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17503463084254396969ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1757122544080667159ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l74_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6099690877655622811ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5292463549918427803ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10072501071836024480ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 904139146933444537ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2123317525101417583ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6954484061115244674ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14151786206039710803ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4319421491651214383ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9173124915441136986ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16557455146913271843ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5277079493780422023ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3542597252416544348ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16907080067885197782ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14896306697346175347ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3759695157918352696ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9710024856525726991ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2584999285488876818ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13918857206471589259ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16078746929342048352ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17943113390603666141ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4108710275777845727ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10441801866794255968ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14577818102542485293ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4306202805698441337ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3887378985770413353ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 2557125952501449452ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 958812208962685390ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 238974161853136896ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 356716254262324034ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8313802705850623725ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AW_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15037409668183247722ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6143047858502399407ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6320968838518626187ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6035510320572739591ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13124952194961064128ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14860857804939021692ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6323267833074246334ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_len = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15861669670508563542ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13634438547675403978ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11707965151247539190ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12658104090332745493ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12529042813249792729ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3662394765082457443ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17491733996136745959ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14539738214330872535ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7595921146147905680ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3355999255714913427ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2907989028449462686ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9826746262171902211ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8556799225388134194ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 539303997504654375ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2581012245132625265ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9183667810895707068ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_read_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8933521628939293437ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8277279554890511800ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11160855590796131334ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9078986374606737510ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14611427781527474639ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_aligner_mask = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1788260781590225834ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15065128358506872653ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11029531413325231870ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_payload_header = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17576819335254914197ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9050375772497229748ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4546002464014476474ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16061418945389515539ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 149561248361558257ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_header = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10231354776899676973ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_ups = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 440484250706929533ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_len = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4763621873723155379ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_cmd_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11918176522055936765ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12219277934617509659ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_header = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2377287245541270975ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_ups = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13483712350512836106ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_len = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14490182581668608488ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11934858081869975347ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 215137676886610632ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3755636385676222965ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3093136290371225042ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4964606680580955398ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l164 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8735488611242502162ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7995134540727058355ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4059338391229972423ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_errorAcc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5362086496242823087ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2680108735246957631ull);
    vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11426368194865581869ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14358034126360507781ull);
    }
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge_io_down_ar_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17206260718793462115ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14306116203667316860ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14200227874659891437ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16822787342480083005ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_1 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11749361580011192824ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT___zz_a_lenToSize_2 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12913682712872880612ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7488004001640531667ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 15445940252639646391ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13868270967982459855ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2217948034439316649ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8857303661418201273ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8783630214350233013ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_ERRORED = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15112985089813519372ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_CTX_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4903891836486298828ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5414500857772659144ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7083731819351279596ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2384778748118585857ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6448623442630311811ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_END = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17677390050320738897ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_LEN = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18036259987343141462ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_BOUNDED_BLOCK = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11340722149817491600ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7205905450193120222ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_FIRST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15919080389060850127ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_aligner_CHUNK_START = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12682926252083579065ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8261741170742953715ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17550438778075068082ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5572523490640069560ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_bufferize_AR_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12540801235107804049ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14086929091229244024ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_END = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11255581759438940839ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_CHUNK_START = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 10049151326091281634ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10751808968307414019ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16398045577996898137ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14225843656049281417ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_len = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18045940181928120562ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2953715390447305535ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_cache = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12556795795786168995ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16605466777376368652ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5382866515425771009ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1439319095414799079ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2934510376127257010ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14103104861055976548ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8806896988945355137ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8622289778220271041ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17736562438060613439ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8913218689679024253ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3155779637813217249ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9776760046243922529ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2288136460074254022ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2031046362455360680ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_read_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5541309899521534385ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5199838999077521249ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14559777560269105879ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12468182773316197779ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4456509448747955357ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9465060833480198012ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_aligner_mask = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 13349509037648758139ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 518714465871627386ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10161134896918858601ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8675783502195526526ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6999130960652126841ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3781766561151323995ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5953457835213941449ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_errorAcc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14146503862767502997ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16512600887798554365ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16148937427302300052ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4729497069686115544ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4946097172282034679ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 12042860906171684928ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10995903333109356462ull);
    }
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 7457653586615263017ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1026993561635955238ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_id = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16543345941945361324ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_resp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 389088684128499361ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT___zz_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16991443834286153592ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onAr_bytesBeats = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14575924431896777749ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5477354363590297456ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_first = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1171857528285187272ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7360278443881303198ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3425521814503831592ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7057026347844115897ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13896298519526274006ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 6931071680158639233ull);
    }
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10075457869997072139ull);
    vlSelf->__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8299269634619411049ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2495399277135403117ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6717839178731745347ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11498724049477143617ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10438466324416657466ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10423535522060397706ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7927086874669873341ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 293428082030218203ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7937767586116645532ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8435146275733266685ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6391873236658038657ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12506849837703099402ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11852845039074108734ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7123401625244317693ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5433535955496038320ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17331894042262074932ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 14902642418707253536ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15105444421719591089ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11739879726377423576ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7442345389019351029ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8205405819377898262ull);
    vlSelf->__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8784470756525572648ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 14184146611665896137ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13302446344185254306ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2584417004558744309ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram_spinal_port1 = VL_SCOPED_RAND_RESET_Q(36, __VscopeHash, 10078221303136528509ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1 = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 17000816375493747827ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7272894786605641287ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12_io_inputs_0_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10497202739731586692ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_target_mem_port = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14599769870907731888ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_hit_mem_port = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3066895753201583513ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SIZE = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7753698758017179017ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12677248151769972973ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_SLOT_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5536800356799331154ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PARTIAL_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16397879618073839898ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_TO_DOWN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1396363080619095271ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4939877864937993166ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_source = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 586752306074593254ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9158649457842671422ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2866879385706657098ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13186731931361617716ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18050127464995244808ull);
}

VL_ATTR_COLD void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset_1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___ctor_var_reset_1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7997305830784340891ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_0_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 899335373993459265ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16872661376493095700ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3897371260401630548ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PAYLOAD_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11619777118493585167ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SIZE = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2103767594564233875ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9031875462780063044ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_SLOT_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8935420357708738386ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PARTIAL_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16596019610281554767ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_WRITE_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8793080787683895105ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_TO_DOWN = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14854484818933039495ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15613711423766596429ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_BUFFER_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3469994362179195189ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_WRITE_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3860025198397222059ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12761286960932782679ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_FROM_C = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 570228310391351229ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1119695245647943538ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_PAYLOAD_C_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13542779975112643696ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6074352844307676858ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5967637489559140776ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12222804574114955801ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10872552980670663040ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9347061392402759160ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1541640503615367644ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10710682531959740029ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_UNIQUE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18064860914139860822ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_PROBE_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15836640101717888928ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_FROM_NONE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17318730552871815625ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4675107771353770098ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_PROBE_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11470295883056517023ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3300711370505099611ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1260308433547855465ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_BUFFER_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2811083633617258833ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5663447089697979610ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15428110200599654906ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1656551668034567203ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10884085542847031975ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13768214770441334994ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7029273093019898499ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17219173000016505520ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16632746986750719478ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4756968370004572319ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5641329540813956704ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13101707527490760385ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11778054400787224193ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12132151462095106938ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l197 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4731238219828089891ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12374614885338185127ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeOh_4 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7342775864190702280ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_slots_freeId = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1215071624958430922ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 77007994881591533ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_write_payload_address = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 131034430439283732ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2438451482363403511ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8158117820591836253ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_stages_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17786871389552414167ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16484614968217776180ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_allocated = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13530061526475236829ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10210187567281793682ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_clear = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9231515773374300888ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_frontendA_buffer_firstFree_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8759853813049992492ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_firstFree = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1337889709158658577ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7882887665733173052ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17003197009297011976ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17745310383489749671ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3958709400786091891ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 326525339652295017ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 630482699299030865ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_lockedValue = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9485374330529085003ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1015211866123404897ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16640020196368454655ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_bypassData = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6848345351650510745ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_readAddressBuffer = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9296194270985752241ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12234007648769516143ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2991233592113190505ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3490674413616161482ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassData = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 625618863392729661ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_readAddressBuffer = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13345723838191133081ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6871489030765342169ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7348840907298983805ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17710561190700099426ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1719500231217148938ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15389868062178551527ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4112462597774562798ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1704486380347036558ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16146771552369811234ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13054553104113608024ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_fromNone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13080351603033758222ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17436791727137278465ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_probeAckDataCompleted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16462751074829501481ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8931505131507324676ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5041659020675930750ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11845169064043891590ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_set = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8918157295759801339ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18116151692414452161ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_fromNone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5414887904072641654ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1385063767782960760ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_probeAckDataCompleted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7408635040476977354ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1953914895527005577ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14653197131801551806ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5682599778341270626ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_set = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17413990958048240350ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 588677326926694586ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_fromNone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11004916817844404523ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2219076630666661720ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_probeAckDataCompleted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11046116245521646756ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 609206688553987180ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9595003096842811212ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 596334953812632508ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_set = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11626812843444618163ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8769057706394287455ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_fromNone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14900682516191092180ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9075651628561916023ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_probeAckDataCompleted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13223464698848055245ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16248107811382804496ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_slotted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16000464512041399447ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_full = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17784043595492901598ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeMask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7572744632152085408ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14535382858978047980ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16330942113027264327ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_cmd_freeId_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10614135196629624092ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14763150763375449500ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12950674467994803128ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15368109689730464662ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4938239894125210979ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14993464848415048970ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6701651718639353095ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitOh_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1294899306446616951ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitId = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14120260366921185093ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_pendingNext = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1231019136293456652ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_lostIt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16272465572220596648ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l475 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4356483272674126313ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toBackend_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15990729207950722810ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17383660818891720056ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1641143925087948639ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5958756201534352460ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16165446860013429862ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11554867739077714663ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinNext_priority = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15570417787817088978ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18355932202456756547ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_0_to_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9039680557965368003ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5522359447102719919ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9935033903496034889ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8321130835134464885ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18128795169898806848ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8385694901082587371ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11966347184160138015ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9707599306118680500ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockSel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14759451883013759706ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12231891957248605328ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_first = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6634422291665613428ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13547619839931600366ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotReg = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17421732054354001294ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5239672256434615142ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_first = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9256451354756973880ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_toDown_base = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10752655330721304015ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9571111959645032569ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15636556881880003528ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_slotRelease_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 928698136343197159ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11629485170189497166ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10965300004442889783ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15144816566459238136ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1657746101740136406ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15507694857501761308ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13709096738377994106ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11399692301243752523ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15962874264422466305ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9394542880783851706ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9903986121104255354ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6425989983906762594ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3690563338176326273ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11927082196751459904ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 980682854883958486ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9136032407880070156ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7053067430146552798ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2514029729064643898ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7632115243176437055ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13365680361662543186ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3531741640933066089ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6301786859967454081ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16698515994850892969ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 7218244930270840320ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12968810892128194011ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1774864771142054111ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16357121818298893283ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11599606790904384712ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12620333585626368285ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17763049523270109358ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16531599984018131699ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8745312380755125240ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx[__Vi0] = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 5424670223962276836ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12289467519502558053ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5412758239969515629ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_ram[__Vi0] = VL_SCOPED_RAND_RESET_Q(36, __VscopeHash, 5338197404108859254ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem[__Vi0] = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 3517761316355537961ull);
    }
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6487547319373366417ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5838519847054948048ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12505936642305075671ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8073819595431017626ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17834966478928155552ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13064360669157753102ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6495117443710480556ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9574753556589213596ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8830088466945032514ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14242738035579229828ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9131018528289975650ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8121355189173298911ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6329594547360580683ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16818535490125268462ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14140360632483572537ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5945795168651723628ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7682448311205919780ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10202975907758908571ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8112460610745484505ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6591032626481235486ull);
    vlSelf->__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4646689652097512442ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11226256889209759755ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12094136079152952418ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4099862392010386490ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12724460374336341988ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2596173438162873283ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10273507053102068346ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1350323008632625775ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17387055647572609110ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1385390533879150175ull);
    vlSelf->__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16483361031273666000ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8712728169684425489ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4466395796616557914ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8457878844987938059ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11068148793654914677ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12696300239917970343ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17921603154888950036ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17534941335267984803ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8374098540239256886ull);
    vlSelf->__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1553542355705225657ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT___zz_a_logic_2_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16537849018769967871ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__a_key = VL_SCOPED_RAND_RESET_Q(35, __VscopeHash, 6894363855845517176ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1976016733147435089ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1311522429809839033ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16687923390607848343ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4563541985362834554ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9494473623637940342ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11823588225744687343ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4480113958601893723ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11869636112896954197ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3344138487728059433ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3465084247432029384ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14381350946463671488ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4966922583034740274ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1 = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11040554443302670590ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2 = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 10421225737387791156ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4856418173105565812ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11949652245440653576ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11628270977492967114ull);
    vlSelf->__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7532217977947863654ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4515278772702388228ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15601513277768968379ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12306867417297591015ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 951213102645973483ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10070986086141691434ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3668171035473681408ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13593982765595043870ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3329333851117075923ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7714843618635328749ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_source = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10889699935816648106ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14398995453770710824ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5249404110621124517ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9248466710377745130ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8793311710575292675ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1038789725086820162ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14091953240079850404ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6100436617941407229ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9272916514751152053ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15891102801725011744ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9414415406938024020ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14666274125434796845ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15224827471134514151ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 929614538180059911ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10662906407534347991ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5681667015807534033ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11543439150817786173ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10690010515074954611ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15140113411260106982ull);
    vlSelf->__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9940413711928482025ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 957711258915602434ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9300715257783291021ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17460935117774293205ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3720396801811184218ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9668352323548248890ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6215215652551059381ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3432858028577494913ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17901121609600850836ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9336414453039628422ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12627516180992808613ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17839276031505242480ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10316322754154434617ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8430364333988593718ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6782549169052481543ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_4 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5340209853665349844ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10958996119329564879ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16941786757744910270ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11879103303848377116ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12030545150329606618ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15384392663269835684ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7301143822536862474ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8067763371624261887ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17176406071537378391ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_7 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10432094416153899929ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17604291239919416073ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2591293307713131706ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_8 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7814798224437282967ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5819173258227531929ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9500301154148855588ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_9 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2643471950580127471ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15960977300785913440ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14042854634094204381ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_10 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10230285475270173191ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16455594163665567439ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11363778621450493481ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_11 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17632330586338366482ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 985261667753139466ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10311508108069577484ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_12 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8859142164054260347ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4703800098087649349ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2933736612329659730ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_13 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5193374255603695150ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2057187913327075633ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10243171415145722018ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_14 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 312712613135753475ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10590980141233186940ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7242703019968820755ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_15 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2864088165279420579ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15300518937027522372ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3836695040520448704ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_16 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12045293297768998800ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11555216087944524892ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12865884573258206152ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_17 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4794505876600434093ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1295984143799853718ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18034877208243909217ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_18 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1588867464979932770ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17094819726283383767ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3498711957030855083ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_19 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9926668243780059949ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17085167518386229500ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9765704731024429411ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_20 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12425565157256089904ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10422368088927700587ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8099957788466820714ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_21 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10194122977869419493ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3885923294187645510ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11224755458472027444ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_22 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 911267767772004369ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17213061427144379191ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17465044651664147061ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_23 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7788132111443412598ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1553420382080771459ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4383576283713799490ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_24 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16471209258440350047ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7958885700990961077ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3484584485421101202ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_25 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7530732462010854343ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14328042720415172941ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18411520682498660696ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_26 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9769626733764281108ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14234887201365140823ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 506001302953309270ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_27 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5661372401491762017ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5822521855209051186ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3682527761734976676ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_28 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3451672965336112635ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12997354409560065935ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11867180560111073633ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_29 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3579957809470677360ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4117972640290196707ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12557648734537577149ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_30 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5115326797605161626ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_2_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1800284114647375499ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_3_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17834131033414471689ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_4_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6347540897620875941ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_5_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5134677782014940306ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_6_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15034776313581311566ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_7_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9013656779121006617ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_8_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15074725158594903805ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_9_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16675039841405998474ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_10_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4081941341631064070ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_11_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12429134180119825886ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_12_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7874017609625953150ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_13_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4611926882135547085ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_14_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3817975619551363596ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_15_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11395343344391671913ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11024556876522213968ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2466287725002743627ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5436247755102180723ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14564333122359804552ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7061042450435601537ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6097063719305995259ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6612890608330244262ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14812734108416201115ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17526156619992358539ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8138573853328356013ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11977332519645936406ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12356074214141544188ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2341015774912949543ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14301935776300501457ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4857780306570568386ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11203324257962498742ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8819211464112991158ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5103407565421999958ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6795795926418681276ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2901727406657674603ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6586334706236602268ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_8 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1736248679161863350ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_9 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14596615719175596692ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2145677423958432890ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_11 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8007055705783393832ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_12 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5355845912954462188ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_13 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8234531714039962389ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_14 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9059513620783242830ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_15 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10109590285915781558ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_16 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4837953845291355801ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_17 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1778572583515461279ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_18 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 387588682365071241ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_19 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17257586290753320482ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_20 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7771250230974097766ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_21 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11705068700480094737ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_22 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12525473700506256122ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_23 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5197111486545309476ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_24 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1864820922131025440ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14951332252124474958ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9512469105907713637ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_27 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2840680111487366053ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1959433887953679023ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9950231225444875783ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_30 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16659260176038815827ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4422589737920290355ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15186197912618832301ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_33 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13690873753869720624ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17885727873031131766ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9756819122985400639ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_36 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4830202567736492664ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 177502803910589881ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17108585158358515477ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_39 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6474739191899261663ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10001694951779746018ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12287277268270528998ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_42 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2937917483963451758ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2171789505775730512ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4742085062802960317ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_45 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 748538321672717215ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4308817859986706888ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9847864232539589241ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_48 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2405973961609965505ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11672599346814848520ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 936273276665140767ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1369851857041367928ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_54 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4728393629036691606ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4877029581312455249ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5994922913184644668ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_57 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4818573346691094490ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15484874636557414900ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2938170162847100150ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_60 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17490898683088505086ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_61 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1984472695462384965ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_62 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16575706224414328366ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_63 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13729634244495909643ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_64 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14997667988006242925ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_65 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 395686718224152732ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_66 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18035556215558231052ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_67 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12167105661293570866ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_68 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 99835404097043561ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_69 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10745409504913474694ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_70 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2277670394161693424ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_71 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17482787044060525870ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_72 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17336161155616254032ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16662405509374857540ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11665097696858037447ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 707742893940852332ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_76 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4891528513909895239ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4488457683774059406ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8993704514898719805ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_78 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8699730706246807450ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3113095021361530332ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14657161709908142618ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4217883285193782495ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13932703646057897117ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3793559086477832352ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7485339742678821899ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1813823789314242001ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_priority = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12744986443513484718ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_id = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4220996818980405664ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_claim = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15997887614219113655ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13706988295234017093ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3130778815043175192ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askWrite = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2613777747894689527ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__factory_askRead = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 736085688448979718ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 228164756312166699ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12465172128648082275ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2685320879946494374ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16465558809535339501ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7224801859259274305ull);
    vlSelf->__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10932256566580469585ull);
}
