// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__30(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__30\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip = 0U;
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
            if (((((((((0x00000024U == (0x003ffffcU 
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
                   | (0x00000038U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000003cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000040U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000024U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000028U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x0000002cU != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000030U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000034U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000038U 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if ((0x0000003cU 
                                             == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_priority_driver 
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
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000cU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000bU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000fU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 8U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 9U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000aU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000dU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                          >> 4U)))) {
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip = 0U;
                            }
                        }
                    }
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip = 0U;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__31(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__31\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid = 0U;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 = 1U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid = 0U;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2 = 1U;
        vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_15_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_16_driver = 0U;
    } else {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000eU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                          >> 4U)))) {
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid 
                = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid;
        }
        if (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_1 
                = vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_1;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid;
        }
        if (vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid) {
            vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_2 
                = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_2;
        }
        if (vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid)));
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
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_15_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 0x10U));
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_16_driver 
                                    = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                             >> 0x11U));
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__32(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__32\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_17_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_18_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_17_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x12U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_18_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x13U));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__33(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__33\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_19_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_20_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_19_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x14U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_20_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x15U));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__34(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__34\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_21_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_22_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_21_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x16U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_22_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x17U));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__35(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__35\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_23_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_24_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_23_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x18U));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_24_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x19U));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__36(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__36\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_25_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_26_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_25_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x1aU));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_26_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x1bU));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__37(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__37\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_27_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_28_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_27_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x1cU));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_28_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x1dU));
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__38(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__38\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_29_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_30_driver = 0U;
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
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_29_driver 
                                = (1U & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                         >> 0x1eU));
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_30_driver 
                                = (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data 
                                   >> 0x1fU);
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__39(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__39\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver = 0U;
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
            if (((((((((0x00000044U == (0x003ffffcU 
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
                   | (0x00000058U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000005cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000044U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000048U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x0000004cU != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000050U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000054U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000058U 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if ((0x0000005cU 
                                             == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver 
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
                        if ((0x00000030U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000034U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000038U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x0000003cU 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver 
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__40(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__40\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver = 0U;
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
            if (((((((((0x00000044U == (0x003ffffcU 
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
                   | (0x00000058U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000005cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000044U == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver 
                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                    }
                }
                if ((0x00000044U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000048U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver 
                                = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__41(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__41\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver = 0U;
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
            if (((((((((0x00000044U == (0x003ffffcU 
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
                   | (0x00000058U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000005cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000044U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000048U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x0000004cU == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver 
                                    = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                            }
                        }
                        if ((0x0000004cU != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000050U == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver 
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__42(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__42\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver = 0U;
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
            if (((((((((0x00000044U == (0x003ffffcU 
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
                   | (0x00000058U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000005cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000044U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000048U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x0000004cU != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000050U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000054U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver 
                                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                    }
                                }
                                if ((0x00000054U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000058U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver 
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__43(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__43\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver = 0U;
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
            if (((((((((0x00000044U == (0x003ffffcU 
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
                   | (0x00000058U == (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) 
                  | (0x0000005cU == (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) 
                 | (0x00000060U == (0x003ffffcU & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                   - (IData)(0xf0c00000U)))))) {
                if ((0x00000044U != (0x003ffffcU & 
                                     (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                      - (IData)(0xf0c00000U))))) {
                    if ((0x00000048U != (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if ((0x0000004cU != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x00000050U != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000054U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000058U 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if ((0x0000005cU 
                                             != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver 
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
                    if ((0x00000064U == (0x003ffffcU 
                                         & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                            - (IData)(0xf0c00000U))))) {
                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver 
                                = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__44(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__44\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver = 0U;
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
                        if ((0x00000068U == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver 
                                    = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                            }
                        }
                        if ((0x00000068U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x0000006cU == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver 
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
