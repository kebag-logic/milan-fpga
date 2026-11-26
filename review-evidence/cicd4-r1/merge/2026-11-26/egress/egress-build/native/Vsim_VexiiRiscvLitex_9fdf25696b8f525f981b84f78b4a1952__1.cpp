// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__17(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__17\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd = 0U;
        vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat = 0U;
        vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__d_counter = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header = 0U;
        vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0 = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0 = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_first = 1U;
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0 = 1U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter = 0U;
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_softwareInterrupt = 0U;
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1 = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1 = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2 = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_threshold_driver = 0U;
    } else {
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_2) {
            vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd)));
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
            if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked) {
                if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST) {
                    vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp)));
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_1) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd)));
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_isFiring) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp)));
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_fire) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat)));
            if ((1U & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)) 
                       | ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat) 
                          == (0x0000000fU & (0xff731000U 
                                             >> ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_size) 
                                                 << 2U))))))) {
                vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat = 0U;
            }
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0 = 0U;
        }
        if (((IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_b_valid) 
             & (IData)(vlSelfRef.__PVT__pBus_bready))) {
            vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__d_counter 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter)));
            if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_lastB) {
                vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__d_counter = 0U;
            }
        }
        if ((1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid)) 
                   | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_w_ready)))) {
            vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid 
                = (((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_last) 
                    | ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counterPlus) 
                       >> 2U)) & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l66));
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone)))) {
                vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header 
                    = (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header) 
                                      + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready)));
            }
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone)))) {
                    vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups 
                        = (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups) 
                                          + (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready)));
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire) {
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last) {
                vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header = 0U;
                vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_valid;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor_io_down_aw_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0 = 0U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_aw_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0 = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_valid 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_fetch_valid;
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_first 
                = vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last;
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter 
                = (3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounterPlus));
            if (vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last) {
                vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_wordCounter = 0U;
            }
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready) {
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_0 = 1U;
        }
        if ((0U == (0x0000ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                   << 2U)))) {
            if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_doWrite) {
                vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_softwareInterrupt 
                    = (1U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
            }
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_last) 
             & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_fire))) {
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid = 0U;
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_fire) {
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids 
                = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_id))));
        }
        if (((~ (IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid)) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_b_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids 
                = ((~ ((IData)(1U) << (0x0000000fU 
                                       & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1) 
                                          >> 1U)))) 
                   & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__pendings_valids));
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT___zz_1) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids 
                = ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_ar_rData_id))));
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge_io_up_r_payload_last) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_id))) 
                   & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge__DOT__pendings_valids));
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1 = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_input_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_0 = 1U;
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2__DOT__logic_linkEnable_1 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_outputs_1_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1 = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2_io_input_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_0 = 1U;
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__io_up_aw_fork2__DOT__logic_linkEnable_1 = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid)));
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2 = 1U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_frontend_allocateSlot_haltRequest_Axi4Aligner_l136_2 = 0U;
        }
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if (((((((((0x00000064U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                               | (0x00000068U == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x0000006cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000070U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000074U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000078U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000007cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00200000U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
                        if ((0x00000064U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000068U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x0000006cU != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000070U 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if ((0x00000074U 
                                             != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if ((0x00000078U 
                                                 != 
                                                 (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) {
                                                if (
                                                    (0x0000007cU 
                                                     != 
                                                     (0x003ffffcU 
                                                      & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                         - (IData)(0xf0c00000U))))) {
                                                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_threshold_driver 
                                                            = 
                                                            (3U 
                                                             & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_firstCycle 
        = vlSelfRef.__PVT__litex_reset;
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__18(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__18\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_0_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_1_driver = 0U;
    } else {
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((1U & (~ ((((((((0x00000064U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                                        | (0x00000068U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                                       | (0x0000006cU 
                                          == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                                      | (0x00000070U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                                     | (0x00000074U 
                                        == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                                    | (0x00000078U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000007cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00200000U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))))))) {
                        if ((0x00002000U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_0_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 1U));
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_1_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 2U));
                            }
                        }
                    }
                }
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 1U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                   | (8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                  | (0x0000000cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000010U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000014U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
               | (0x00000018U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (0x0000001cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
             | (0x00000020U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
            if ((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver 
                        = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__19(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__19\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_2_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver = 0U;
    } else {
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((1U & (~ ((((((((0x00000064U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                                        | (0x00000068U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                                       | (0x0000006cU 
                                          == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                                      | (0x00000070U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                                     | (0x00000074U 
                                        == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                                    | (0x00000078U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000007cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00200000U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))))))) {
                        if ((0x00002000U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_2_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 3U));
                            }
                        }
                    }
                }
            }
        }
        if (((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                   | (8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                  | (0x0000000cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000010U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000014U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
               | (0x00000018U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (0x0000001cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
             | (0x00000020U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
            if ((4U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                if ((8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) {
                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver 
                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                    }
                }
                if ((8U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) {
                    if ((0x0000000cU == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver 
                                = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__20(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__20\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip = 0U;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__locked = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_3_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_4_driver = 0U;
    } else {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 3U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 2U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid) {
            vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__locked = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_fire))) {
            vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__locked = 0U;
        }
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((1U & (~ ((((((((0x00000064U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                                        | (0x00000068U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                                       | (0x0000006cU 
                                          == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                                      | (0x00000070U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                                     | (0x00000074U 
                                        == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                                    | (0x00000078U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000007cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00200000U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))))))) {
                        if ((0x00002000U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_3_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 4U));
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_4_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 5U));
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__21(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__21\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_5_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_6_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                            | (0x00000028U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000002cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000030U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000034U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000038U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000003cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000040U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000044U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000048U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000004cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000050U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000054U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000058U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000005cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000060U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000064U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000068U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000006cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000070U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000074U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000078U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000007cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00200000U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((0x00002000U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_5_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 6U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_6_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 7U));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__22(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__22\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_priority_driver = 0U;
    } else if (((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U)))) 
                      | (8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                     | (0x0000000cU == (0x003ffffcU 
                                        & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) 
                    | (0x00000010U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                   | (0x00000014U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x00000018U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x0000001cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000020U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U)))))) {
        if ((4U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                   - (IData)(0xf0c00000U))))) {
            if ((8U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                if ((0x0000000cU != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000010U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_priority_driver 
                                = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                        }
                    }
                    if ((0x00000010U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x00000014U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_priority_driver 
                                    = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                            }
                        }
                        if ((0x00000014U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000018U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_priority_driver 
                                        = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                }
                            }
                            if ((0x00000018U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x0000001cU == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_priority_driver 
                                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__23(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__23\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip = 0U;
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid = 0U;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0 = 0U;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = 1U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_7_driver = 0U;
    } else {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 6U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 4U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 5U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 7U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                              >> 3U)))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip = 0U;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__locked = 1U;
            vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1;
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_fire))) {
            vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        }
        if (vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_busA_ready) {
            vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_rspAsync_rValid 
                = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94;
        }
        if (vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid) {
            vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_0 
                = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_0;
        }
        if (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__locked = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last) 
             & (IData)(vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_fire))) {
            vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__locked = 0U;
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_ready) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_rspAsync_rValid 
                = ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value)) 
                   & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core_io_downs_1_a_valid));
        }
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((1U & (~ ((((((((0x00000064U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                                        | (0x00000068U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                                       | (0x0000006cU 
                                          == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                                      | (0x00000070U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                                     | (0x00000074U 
                                        == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                                    | (0x00000078U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000007cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00200000U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))))))) {
                        if ((0x00002000U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_7_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 8U));
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__24(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__24\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_8_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_9_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                            | (0x00000028U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000002cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000030U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000034U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000038U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000003cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000040U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000044U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000048U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000004cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000050U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000054U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000058U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000005cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000060U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000064U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000068U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000006cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000070U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000074U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000078U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000007cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00200000U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((0x00002000U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_8_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 9U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_9_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x0aU));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__25(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__25\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_10_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_11_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                            | (0x00000028U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000002cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000030U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000034U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000038U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000003cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000040U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000044U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000048U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000004cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000050U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000054U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000058U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000005cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000060U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000064U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000068U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000006cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000070U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000074U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000078U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000007cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00200000U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((0x00002000U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_10_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x0bU));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_11_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x0cU));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__26(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__26\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_12_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_13_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                            | (0x00000028U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000002cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000030U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000034U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000038U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000003cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000040U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000044U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000048U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000004cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000050U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000054U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000058U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000005cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000060U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000064U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000068U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000006cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000070U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000074U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000078U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000007cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00200000U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((0x00002000U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_12_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x0dU));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_13_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x0eU));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__27(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__27\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_14_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_priority_driver = 0U;
    } else {
        if ((1U & (~ ((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                            | (8U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                           | (0x0000000cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000010U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000014U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                        | (0x00000018U == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                       | (0x0000001cU == (0x003ffffcU 
                                          & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                             - (IData)(0xf0c00000U))))) 
                      | (0x00000020U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U)))))))) {
            if ((1U & (~ ((((((((0x00000024U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))) 
                                | (0x00000028U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000002cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000030U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000034U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000038U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x0000003cU == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x00000040U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))))))) {
                if ((1U & (~ ((((((((0x00000044U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))) 
                                    | (0x00000048U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000004cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00000050U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                                 | (0x00000054U == 
                                    (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                                | (0x00000058U == (0x003ffffcU 
                                                   & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                      - (IData)(0xf0c00000U))))) 
                               | (0x0000005cU == (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) 
                              | (0x00000060U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U)))))))) {
                    if ((1U & (~ ((((((((0x00000064U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U)))) 
                                        | (0x00000068U 
                                           == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                                       | (0x0000006cU 
                                          == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                                      | (0x00000070U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                                     | (0x00000074U 
                                        == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U))))) 
                                    | (0x00000078U 
                                       == (0x003ffffcU 
                                           & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                              - (IData)(0xf0c00000U))))) 
                                   | (0x0000007cU == 
                                      (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U))))) 
                                  | (0x00200000U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U)))))))) {
                        if ((0x00002000U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_14_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 0x0fU));
                            }
                        }
                    }
                }
            }
        }
        if (((((((((4U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                   | (8U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                  | (0x0000000cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000010U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000014U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
               | (0x00000018U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (0x0000001cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
             | (0x00000020U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
            if ((4U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                if ((8U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                           - (IData)(0xf0c00000U))))) {
                    if ((0x0000000cU != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x00000010U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000014U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000018U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x0000001cU 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_priority_driver 
                                                = (3U 
                                                   & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__28(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__28\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_priority_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if (((((((((0x00000024U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                   | (0x00000028U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000002cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000030U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000034U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
               | (0x00000038U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (0x0000003cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
             | (0x00000040U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
            if ((0x00000024U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_priority_driver 
                        = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                }
            }
            if ((0x00000024U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                if ((0x00000028U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_priority_driver 
                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                    }
                }
                if ((0x00000028U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x0000002cU == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_priority_driver 
                                = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__29(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__29\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_priority_driver = 0U;
    } else if ((1U & (~ ((((((((4U == (0x003ffffcU 
                                       & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                          - (IData)(0xf0c00000U)))) 
                               | (8U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) 
                              | (0x0000000cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) 
                             | (0x00000010U == (0x003ffffcU 
                                                & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                            | (0x00000014U == (0x003ffffcU 
                                               & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
                           | (0x00000018U == (0x003ffffcU 
                                              & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
                          | (0x0000001cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
                         | (0x00000020U == (0x003ffffcU 
                                            & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))))) {
        if (((((((((0x00000024U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))) 
                   | (0x00000028U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000002cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000030U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U))))) 
                | (0x00000034U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                  - (IData)(0xf0c00000U))))) 
               | (0x00000038U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                 - (IData)(0xf0c00000U))))) 
              | (0x0000003cU == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) 
             | (0x00000040U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                               - (IData)(0xf0c00000U)))))) {
            if ((0x00000024U != (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                if ((0x00000028U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x0000002cU != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x00000030U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_priority_driver 
                                    = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                            }
                        }
                        if ((0x00000030U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000034U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_priority_driver 
                                        = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                }
                            }
                            if ((0x00000034U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000038U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_priority_driver 
                                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
