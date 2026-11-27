// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_0_to_5 
        = ((0U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2)) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rValid) 
            << 2U) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rValid) 
                       << 1U) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid)));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid) 
            << 1U) | (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20 = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready)) 
                                                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready)));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1 
        = ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1));
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__locked) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_0;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_1));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2 
            = (1U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskLocked_2));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_0 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_1 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1) 
                     >> 1U));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__maskRouted_2 
            = (1U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_maskProposal_1_1) 
                     >> 2U));
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_FROM_C 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockValid)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_lockSel)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toBackend_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1) 
                    >> 1U) & (~ (1U & (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11__DOT___zz_maskProposal_1) 
                                        - (IData)(1U)) 
                                       >> 1U)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_4 
        = (1U & ((0x00000100U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter))
                  ? ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid) 
                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready))
                  : (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                        >> 8U))));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_PROBE_ID 
        = (((0U != (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh) 
                          >> 2U))) << 1U) | (IData)(
                                                    (0U 
                                                     != 
                                                     (0x0aU 
                                                      & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hitOh)))));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3 
        = (1U & ((0x00000100U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter))
                  ? ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid) 
                     | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_fire))
                  : (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                        >> 8U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_a_ready));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST 
        = (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA) 
            & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_insertion_counter) 
               == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SIZE) 
                                                  << 2U))))) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_WRITE_DATA) 
           | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_READ_DATA));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_up_a_fire) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_LAST)));
    if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_denied;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_payload_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                              >> 1U));
    } else if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_denied;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_toUpD_rData_source));
    } else {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_data;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_corrupt 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_corrupt;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_denied;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_size;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_opcode;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source 
            = (0x0000001fU & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_toUpD_rData_source));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96 = (1U 
                                                 & (~ 
                                                    ((0x0000000fU 
                                                      == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_valids)) 
                                                     & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ALLOCATE))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_hit 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_3) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_write_payload_address) 
              == (0x000000ffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)
                                  ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_hitPort_bypass_readAddressBuffer)
                                  : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_spawn_CMD_address 
                                     >> 6U)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set = 0U;
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Hub_l276) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set 
            = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_set) 
               | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID))));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49 = (1U 
                                                 & (~ 
                                                    ((1U 
                                                      == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode)) 
                                                     | (5U 
                                                        == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode)))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid 
        = (IData)(((0x10U == (0x18U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source))) 
                   & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_up_d_valid)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT__io_output_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask;
    __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask = 0;
    CData/*3:0*/ __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask;
    __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask = 0;
    // Body
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_last 
        = (1U & ((~ ((1U == (1U & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get))))) 
                     | (5U == (1U & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_get))))))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter) 
           == (0x000000ffU & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart 
        = (0x0000000fU & ((- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))) 
                          & (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
           == (0x0000003fU & ((vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                               >> 6U) - (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_bufferize_AR_addr 
                                         >> 6U))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter) 
           == (0x0000003fU & ((vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                               >> 6U) - (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                                         >> 6U))));
    if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_done;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_0_error;
    } else if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_done;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_1_error;
    } else if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_done;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_2_error;
    } else {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_done;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__slots_3_error;
    }
    if ((0U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_done;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_0_error;
    } else if ((1U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_done;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_1_error;
    } else if ((2U == (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_done;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_2_error;
    } else {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_done;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__slots_3_error;
    }
    vlSelfRef.__PVT__pBus_awaddr = (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_address 
                                    | (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter) 
                                        | (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat)) 
                                       << 2U));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter) 
           == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_size) 
                                              << 2U))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus 
        = (7U & ((IData)(1U) + ((3U & (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1) 
                                        >> 0x0000000aU) 
                                       & (- (IData)((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_first))))) 
                                + ((3U & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__context_mem_spinal_port1) 
                                          >> 8U)) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic_io_targets 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_threshold_driver) 
           < (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_priority));
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
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_len) 
           == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_header) 
           == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready 
        = (((4U != (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
            | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter) 
               == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_size) 
                                                  << 2U))))) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                    >> (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_id))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                    >> (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_id))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart 
        = (0x0000000fU & ((- (IData)((0U == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter)))) 
                          & (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_bufferize_AW_addr 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter) 
           == (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1) 
                              >> 9U)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd 
        = (0x0000000fU & ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                          | (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd 
        = (0x0000000fU & ((- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_LAST))))) 
                          | (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_spliter_boundedEnd 
                             >> 2U)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid 
        = ((IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_r_valid) 
           | ((IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_b_valid) 
              & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid)) 
                 | ((IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN) 
                    & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last) 
                       | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus) 
                          >> 2U)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_claim 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_bestRequest_id) 
           & (- (IData)((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic_io_targets))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid) 
           & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone)) 
              | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone))));
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
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT___zz_io_up_aw_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bus_aw_rValid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge_io_down_ar_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT___zz_io_up_ar_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bus_ar_rValid));
    __PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
           ^ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart));
    __PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_split_aligner_mask 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
           ^ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424 = 0U;
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST)))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424 = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid = 0U;
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219) {
        if ((1U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid = 1U;
        }
    }
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000003fU & ((((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid) 
                            << 5U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
                                       << 4U) | ((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid) 
                                                 << 3U))) 
                          | (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid) 
                              << 2U) | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
                                         << 1U) | (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid)))));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output 
        = (1U & (~ ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready)) 
                    & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid))));
    vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid));
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2;
    __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 = 0;
    CData/*2:0*/ __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3;
    __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_100;
    __VdfgRegularize_h6e95ff9d_0_100 = 0;
    // Body
    __VdfgRegularize_h6e95ff9d_0_100 = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_done_1)) 
                                              | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid) 
                                                 & (IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid))));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1) 
                   << 2U) | (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0) 
                              << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2))))) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready 
        = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_done_1)))) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready = 0U;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_forkRequest_Axi4Aligner_l424) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready = 0U;
    }
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000000fU & ((((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge_io_down_a_valid) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor_io_down_aw_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid));
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
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_isFiring 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_100)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid) 
                    & (IData)(__VdfgRegularize_h6e95ff9d_0_100))));
    __PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_3 
        = (7U & (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 3U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid = 0U;
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__rData_read_cmd_valid = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid)) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready)));
    __PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                   << 1U) | (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1)))) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
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
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (3U & (((IData)(__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 2U) | (IData)(__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_param 
        = (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2) 
            << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1));
    vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid 
        = (((IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid) 
            & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0)) 
           | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid) 
               & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1)) 
              | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2) 
                 & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_d_valid))));
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
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*8:0*/ __PVT__dma_filter_logic_core__DOT__instruction;
    __PVT__dma_filter_logic_core__DOT__instruction = 0;
    CData/*0:0*/ __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit;
    __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit = 0;
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48 = (1U 
                                                 & (~ 
                                                    ((1U 
                                                      == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)) 
                                                     | (5U 
                                                        == (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)))));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_ups_1_d_valid 
        = (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source) 
            >> 2U) & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid));
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
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_last 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
           | ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
    __PVT__dma_filter_logic_core__DOT__argsHits_2_argHit 
        = ((4U == (7U & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))) 
           | (1U == (7U & (IData)(__PVT__dma_filter_logic_core__DOT__instruction))));
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
    vlSelfRef.__PVT__dma_filter_logic_core_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit) 
           & ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready) 
              & (IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid)));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__59(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__59\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch;
    vlSelfRef.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1 
        = ((IData)(vlSelfRef.__PVT__litex_reset) || (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_0));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge_io_up_a_ready 
        = ((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__dma_bus_w_rValidN = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN = 1U;
    } else {
        if ((3U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r))) {
            vlSelfRef.__PVT__dma_bus_w_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_bus_w_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bus_w_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN = 1U;
        }
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd) 
           != (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd) 
           != (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid));
    vlSelfRef.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_0 
        = vlSelfRef.__PVT__litex_reset;
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__60(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__60\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN = 1U;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN = 1U;
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN = 1U;
    } else {
        if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_106) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid = 1U;
        }
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_halfPipe_fire) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid = 0U;
        }
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid)));
        }
        if (vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
            vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN = 1U;
        }
    }
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45) 
           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46) 
              | ((IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2))));
    vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_2))));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) 
           & (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_down_a_valid));
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rValid)) 
                 | (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN)));
    vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid 
        = (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid) 
            & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0)) 
           | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1) 
              & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid)));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode;
    __PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode = 0;
    CData/*0:0*/ __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready;
    __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready = 0;
    CData/*0:0*/ __PVT__dma_filter_logic_core_io_up_a_ready;
    __PVT__dma_filter_logic_core_io_up_a_ready = 0;
    CData/*3:0*/ __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2;
    __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 = 0;
    CData/*3:0*/ __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last;
    __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_43;
    __VdfgRegularize_h6e95ff9d_0_43 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_44;
    __VdfgRegularize_h6e95ff9d_0_44 = 0;
    // Body
    __PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0) 
                   << 1U) | (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1)))) 
           & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_b_payload_resp 
        = (2U & (- (IData)(((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_denied) 
                            | (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)))));
    __PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last 
        = (0x0000000fU & (0xff731000U >> (((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)
                                            ? (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__size)
                                            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_size)) 
                                          << 2U)));
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
    __PVT__splited_wc_cBus_arbiter_core_io_down_d_ready 
        = (1U & ((0U == (3U & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source) 
                               >> 3U))) | ((1U == (3U 
                                                   & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz_io_output_payload_source) 
                                                      >> 3U))) 
                                           | (~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt)))));
    vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid 
        = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt) 
           | (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_0_LAST 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__io_down_d_tracker_beat) 
              == (0x0000000fU & (0xff731000U >> ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_size) 
                                                 << 2U)))));
    __PVT__dma_filter_logic_core_io_up_a_ready = ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready) 
                                                  & ((~ (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__hit)) 
                                                     | (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_rValidN)));
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_3 
        = (3U & (((IData)(__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 2U) | (IData)(__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_2)));
    __VdfgRegularize_h6e95ff9d_0_43 = (1U & (~ ((1U 
                                                 == (IData)(__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode)) 
                                                | (5U 
                                                   == (IData)(__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_payload_opcode)))));
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
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_0_d_valid 
        = ((~ ((IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source) 
               >> 2U)) & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid));
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_ups_1_d_valid 
        = (((IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_payload_source) 
            >> 2U) & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid));
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
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink_io_up_r_payload_last 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_43) 
           | ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat) 
              == (IData)(__PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last)));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_last 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_43) 
           | ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_beat) 
              == (IData)(__PVT__dma_filter_logic_core__DOT___zz_io_up_d_tracker_last)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12_io_inputs_0_ready) 
                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102))) 
                 | ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_11_io_inputs_1_ready)) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit))));
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
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode 
            = vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rData_opcode;
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
        vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode 
            = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_WRITE_DATA)
                ? (1U & (- (IData)((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_PARTIAL_DATA))))
                : 4U);
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = 0U;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
                    & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282_5))));
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__peripheral_bus_arbiter_core_io_down_d_ready;
    __PVT__peripheral_bus_arbiter_core_io_down_d_ready = 0;
    CData/*0:0*/ __PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready;
    __PVT__peripheral_plic_intc_thread_logic_io_bus_a_ready = 0;
    CData/*0:0*/ __PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready;
    __PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_aw_ready = 0;
    CData/*0:0*/ __PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready;
    __PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready = 0;
    CData/*0:0*/ __PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead;
    __PVT__peripheral_plic_intc_thread_logic__DOT__factory_doRead = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_97;
    __VdfgRegularize_h6e95ff9d_0_97 = 0;
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9 = ((0U 
                                                 == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
                                                | (1U 
                                                   == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)));
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__a_key 
        = (((QData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address)));
    __PVT__peripheral_bus_arbiter_core_io_down_d_ready 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source) 
                     >> 2U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready)));
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
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data = 0U;
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
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 1U;
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN)) 
         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1))) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready = 0U;
    }
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
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_doWrite 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19));
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__when_Clint_l59 = 0U;
    if ((0xbff8U == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                    << 2U)))) {
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_payload_data 
            = (IData)(vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time);
        if (((4U == (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_opcode)) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19))) {
            vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__when_Clint_l59 = 1U;
        }
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
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire 
        = ((~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_valid));
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
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rValid)) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_input_ready) 
                    & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid)))));
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__pBus_awvalid = ((4U != (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                     & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid));
    vlSelfRef.__PVT__pBus_arvalid = ((4U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                     & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_fire 
        = ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_valid) 
           & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_ready));
    vlSelfRef.__PVT__pBus_wvalid = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11) 
                                    & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_read_cmd_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid));
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_read_cmd_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_valid 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN)) 
                 | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid)));
}
