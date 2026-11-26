// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__45(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__45\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver = 0U;
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
                        if ((0x00000068U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x0000006cU != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000070U == 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver 
                                            = (3U & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                    }
                                }
                                if ((0x00000070U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000074U 
                                         == (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver 
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__46(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__46\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver = 0U;
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
                        if ((0x00000068U != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                            if ((0x0000006cU != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                if ((0x00000070U != 
                                     (0x003ffffcU & 
                                      (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                       - (IData)(0xf0c00000U))))) {
                                    if ((0x00000074U 
                                         != (0x003ffffcU 
                                             & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                - (IData)(0xf0c00000U))))) {
                                        if ((0x00000078U 
                                             == (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver 
                                                    = 
                                                    (3U 
                                                     & vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_data);
                                            }
                                        }
                                        if ((0x00000078U 
                                             != (0x003ffffcU 
                                                 & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                    - (IData)(0xf0c00000U))))) {
                                            if ((0x0000007cU 
                                                 == 
                                                 (0x003ffffcU 
                                                  & (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_address 
                                                     - (IData)(0xf0c00000U))))) {
                                                if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__factory_doWrite) {
                                                    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver 
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

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__47(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__47\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip = 0U;
    } else {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000019U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001dU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000018U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001cU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001bU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001aU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000015U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000013U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000017U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000016U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000011U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000014U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000012U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((0x00000010U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip = 0U;
                            }
                        }
                    }
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip = 0U;
                            }
                        }
                    }
                }
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                              >> 3U)))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip = 0U;
                            }
                        }
                    }
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip = 0U;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__48(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__48\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip = 0U;
        vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1 = 0U;
        vlSelfRef.__PVT__dma_bus_w_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1 = 1U;
        vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = 0U;
        vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_errorAcc = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_errorAcc = 0U;
    } else {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000010U));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001eU));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion)))) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip 
                = (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                   >> 0x0000001fU);
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_valid) {
            if ((0x00000010U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip = 0U;
                            }
                        }
                    }
                }
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_claim_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__peripheral_bus_decoder_core_io_up_d_valid) {
            vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskLocked_1 
                = vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__maskRouted_1;
        }
        if (vlSelfRef.__PVT__dma_bus_w_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bus_w_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bus_w_rValidN)) 
                         | (3U == (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__state_r))));
        }
        if ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)) 
              | (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_w_ready)) 
             & (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_1_valid))) {
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1 = 0U;
        }
        if (vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_input_ready) {
            vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2__DOT__logic_linkEnable_1 = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_down_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 
                = vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0;
        }
        if (vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_valid) {
            vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskLocked_0 
                = vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__maskRouted_0;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge_io_up_w_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter 
                = (3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counterPlus));
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_ready) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_valid))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_counter 
                = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN)
                    ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_payload_offset)
                    : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_offset));
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT___zz_upB_handle_error) 
             & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_isFiring))) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_errorAcc = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l219) {
            if ((1U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_up_b_rValid)))) {
                    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__upB_handle_errorAcc = 0U;
                }
            }
        }
        if (((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_error) 
             & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid) 
                & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready)))) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_errorAcc = 1U;
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked) {
            if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_isForked) {
                if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_CHUNK_LAST) {
                    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_errorAcc = 0U;
                }
            }
        }
    }
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__Vdly__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__Vdly__peripheral_bus_decoder_core__DOT__d_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_d_tracker_beat;
    vlSelfRef.__PVT__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat 
        = vlSelfRef.__Vdly__dma_bridge_down_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat;
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__logic_time 
        = vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__logic_time;
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_beat 
        = vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_d_tracker_beat;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__downR_counter;
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_up_a_tracker_beat;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__toTileink__DOT__io_down_d_tracker_beat;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_counter;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_lenCounter;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_len;
    vlSelfRef.__PVT__peripheral_clint_thread_core__DOT__factory_unburstify_counter 
        = vlSelfRef.__Vdly__peripheral_clint_thread_core__DOT__factory_unburstify_counter;
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_blockCounter;
    vlSelfRef.__PVT__dma_bus_ar_rValid = vlSelfRef.__Vdly__dma_bus_ar_rValid;
    vlSelfRef.__PVT__dma_bus_aw_rValid = vlSelfRef.__Vdly__dma_bus_aw_rValid;
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_counter;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd;
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp 
        = vlSelfRef.__Vdly__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp;
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__a_buffered_fork2_io_outputs_0_tracker_beat;
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__d_counter 
        = vlSelfRef.__Vdly__peripheral_toAxiLite4_logic_bridge__DOT__d_counter;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__compactor__DOT__onW_commitCmd_rValid;
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_header;
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value 
        = vlSelfRef.__Vdly__peripheral_plic_intc_thread_logic__DOT__mapping_coherencyStall_value;
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__49(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__49\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__dma_bridge_up_b_rValid = vlSelfRef.__Vdly__dma_bridge_up_b_rValid;
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN = 1U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion = 0U;
    } else {
        if (((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__errored) 
             & ((~ (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core_io_ups_2_d_valid)) 
                & (0U == (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_down_d_tracker_beat))))) {
            vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_up_d_tracker_last) 
             & (IData)(vlSelfRef.__PVT__dma_filter_logic_core_io_up_d_valid))) {
            vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid) {
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_headerDone) {
                if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l164) {
                    if ((((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_ups) 
                          == (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups)) 
                         & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink_io_up_w_ready))) {
                        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone = 1U;
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__toTileink__DOT__io_up_w_fire) {
            if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_w_payload_last) {
                vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone = 0U;
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_halted_fork2_io_outputs_1_valid) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 1U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_2) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 3U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion = 0U;
                            }
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full 
        = (0U == (4U ^ ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_cmd) 
                        ^ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_rsp))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full 
        = (0U == (4U ^ ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_cmd) 
                        ^ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_rsp))));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT___zz_io_up_a_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__pending_valid) 
                    & (0U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__io_up_a_tracker_beat)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110 = (1U 
                                                  & (~ 
                                                     ((~ 
                                                       ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_ip) 
                                                        & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_0_driver))) 
                                                      | (0U 
                                                         >= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_3_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_2_driver));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__50(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__50\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_2_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_1_driver));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion = 0U;
    } else {
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_1) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 2U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_5) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 6U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_3) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 4U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_4) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 5U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_6) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 7U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_11) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000cU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_10) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000bU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_14) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000fU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_7) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 8U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_8) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 9U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_9) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000aU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_12) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000dU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion = 0U;
                            }
                        }
                    }
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion = 0U;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion = 0U;
                            }
                        }
                    }
                }
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion = 0U;
                            }
                        }
                    }
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion = 0U;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion = 0U;
                            }
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_6_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_5_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_4_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_3_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_5_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_4_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_7_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_6_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_12_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_11_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_11_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_10_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_15_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_14_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_8_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_7_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_9_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_8_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_10_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_9_driver));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__51(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__51\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_13_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_12_driver));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid = 0U;
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid = 0U;
        vlSelfRef.__PVT__dma_bridge_up_r_rValidN = 1U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion = 0U;
    } else {
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_13) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000000eU));
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_up_ar_ready) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_split_valid 
                = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__onPerId_bridge_io_down_ar_valid;
        }
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_up_aw_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_valid 
                = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor_io_down_aw_valid;
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid) {
            vlSelfRef.__PVT__dma_bridge_up_r_rValidN = 0U;
        }
        if (vlSelfRef.__PVT__dma_bridge_up_r_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_up_r_rValidN = 1U;
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_24) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000019U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_28) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001dU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_23) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000018U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_27) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001cU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_26) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001bU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_25) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001aU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_20) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000015U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_18) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000013U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_22) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000017U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_21) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000016U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                          >> 4U)))) {
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion = 0U;
                            }
                        }
                    }
                }
            }
            if ((0x00000010U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion = 0U;
                            }
                        }
                    }
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion = 0U;
                            }
                        }
                    }
                }
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                              >> 3U)))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion = 0U;
                            }
                        }
                    }
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion = 0U;
                            }
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_14_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_13_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_24_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_28_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_23_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_27_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_26_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_25_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_20_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_18_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_22_driver));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__52(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__52\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_21_driver));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion = 0U;
        vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid = 0U;
    } else {
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_16) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000011U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_19) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000014U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_17) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000012U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_15) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x00000010U));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_29) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion 
                = (1U & (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                         >> 0x0000001eU));
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_30) {
            vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion 
                = (vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_interrupt 
                   >> 0x0000001fU);
        }
        if (vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_targetMapping_0_targetCompletion_valid) {
            if ((0x00000010U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion = 0U;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion = 0U;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion = 0U;
                            }
                        }
                    }
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion = 0U;
                            }
                        }
                    }
                }
                if ((8U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                    if ((4U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                        if ((2U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                            if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload)))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion = 0U;
                            }
                            if ((1U & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__mapping_completion_payload))) {
                                vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion = 0U;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_ready) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_valid 
                = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_fetch_valid;
        }
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_16_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_19_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_17_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_15_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_29_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_ip) 
           & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_ie_30_driver));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid 
        = ((IData)(vlSelfRef.__PVT__dma_bus_w_s2mPipe_rValid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge__DOT__onAw_toW_s2mPipe_rValid));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__io_down_d_tracker_beat 
        = vlSelfRef.__Vdly__dma_filter_logic_core__DOT__io_down_d_tracker_beat;
    vlSelfRef.__PVT__dma_filter_logic_core__DOT__errored 
        = vlSelfRef.__Vdly__dma_filter_logic_core__DOT__errored;
    vlSelfRef.__PVT__dma_bridge_read_bridge_io_down_a_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_full)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner_io_down_aw_valid 
        = ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_full)) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_valid));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups 
        = vlSelfRef.__Vdly__dma_bridge_write_bridge__DOT__aligner__DOT__downW_ups;
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_priority_driver) 
           & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110))));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_36 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_25_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_24_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_42 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_29_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_28_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_39 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_27_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_26_valid))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__53(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__53\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_33 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_23_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_22_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_30 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_21_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_20_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_27 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_19_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_18_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_24 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_17_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_16_valid))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_45 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_31_valid)) 
                 | (((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_priority_driver) 
                     <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_priority_driver)) 
                    & (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__targets_0_requests_30_valid))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__when_Axi4Compactor_l66 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onW_awS2m_rValid) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__onPerId_bridge_io_down_w_valid));
    vlSelfRef.__PVT__dma_filter_logic_core__DOT___zz_io_up_a_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__errored) 
                    | (IData)(vlSelfRef.__PVT__dma_filter_logic_core__DOT__doIt))));
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__when_Axi4Aligner_l164 
        = (1U & (~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__downW_upsDone)));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid = 0U;
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid = 0U;
    } else {
        if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready) {
            vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rValid 
                = (1U & ((~ (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN)) 
                         | (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_valid)));
        }
        if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready) {
            vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid 
                = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid;
        }
    }
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_0_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_2 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_3)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_priority_driver)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_2_priority_driver));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_1 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_1_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_5 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_5_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_3 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_3_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_4 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_4_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_6 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_6_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_11 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_11_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_10 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_10_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_14 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_14_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_7 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_7_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_8 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_8_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_9 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_9_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_12 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_12_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_13 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_13_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_24 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_24_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_28 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_28_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_23 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_23_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_27 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_27_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_26 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_26_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_25 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_25_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_20 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_20_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_18 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_18_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_22 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_22_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_21 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_21_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_16 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_16_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_19 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_19_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_17 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_17_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_15 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_15_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_29 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_29_waitCompletion)));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__when_PlicGateway_l21_30 
        = (1U & (~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT__gateways_30_waitCompletion)));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_66 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_41)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_38) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_40) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_37)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_63 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_35)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_32) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_34) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_31)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_60 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_29)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_26) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_28) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_25)))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__54(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__54\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_69 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_47)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_44) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_46) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_43)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_48)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_1)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_4));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_51)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_7)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_10));
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
    vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__io_up_r_fire 
        = ((IData)(vlSelfRef.__PVT__dma_bridge_up_r_rValidN) 
           & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_valid));
    if (vlSelfRef.__PVT__litex_reset) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid = 0U;
    } else if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_valid 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT___zz_upR_handle_isForked;
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_72)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_49)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_52));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_55)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_58));
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
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_74)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_56)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_59))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79)) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77) 
                    & ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3) 
                       <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2)))));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_80)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_1));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5 
        = ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81)
            ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_2)
            : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_3));
    vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_6 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_81)
                      ? (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_77)
                      : (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_id_79))) 
                 | ((IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_5) 
                    <= (IData)(vlSelfRef.__PVT__peripheral_plic_intc_thread_logic__DOT___zz_targets_0_bestRequest_priority_4))));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__55(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__55\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__cpuResetCtrl_fiber_holder_counter 
        = vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter;
    if (vlSelfRef.__PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1) {
        vlSelfRef.__Vdly__cpuResetCtrl_fiber_holder_counter = 0U;
    } else if ((0x40U != (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter))) {
        vlSelfRef.__Vdly__cpuResetCtrl_fiber_holder_counter 
            = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__cpuResetCtrl_fiber_holder_counter)));
    }
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__56(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__56\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_ctxFetcher_hitUpD 
        = ((7U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1))) 
           | ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_1_FROM_NONE)) 
              & (6U == (7U & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_ctxMem_spinal_port1)))));
    vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_cmd_forked_ready 
        = ((4U == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode))
            ? (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_ar_ready)
            : (IData)(vlSymsp->TOP__sim.__PVT__soc_vexiiriscv_pbus_aw_ready));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11 = ((0U 
                                                  == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)) 
                                                 | (1U 
                                                    == (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_opcode)));
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_d_ready) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_D_PAYLOAD_source 
            = (3U & (IData)(vlSelfRef.__PVT__peripheral_bus_decoder_core__DOT__d_arbiter__DOT___zz_io_output_payload_source));
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_LAST 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_0_LAST;
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_ready) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode 
            = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN)
                ? (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_opcode)
                : (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_opcode));
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_LAST 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_LAST;
    }
    vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode 
        = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__streamArbiter_12__DOT___zz___05Fzz_io_output_payload_opcode;
    vlSelfRef.__PVT__vexiis_0_priv_stoptime_regNext = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rValid)))) {
        vlSelfRef.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_size 
            = vlSelfRef.__PVT__peripheral_bus_arbiter_core_io_down_a_payload_size;
    }
    if (vlSelfRef.__PVT__dma_bus_w_s2mPipe_ready) {
        vlSelfRef.__PVT__dma_bus_w_s2mPipe_rData_last 
            = ((IData)(vlSelfRef.__PVT__dma_bus_w_rValidN)
                ? (IData)(vlSelfRef.__PVT__dma_bus_wlast)
                : (IData)(vlSelfRef.__PVT__dma_bus_w_rData_last));
    }
    if (vlSelfRef.__PVT__dma_bus_awready) {
        vlSelfRef.__PVT__dma_bus_aw_rData_id = 0U;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor_io_down_r_ready) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__compactor__DOT__onR_process_fetch_R_id 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_CTX_id;
    }
    if (vlSelfRef.__PVT__dma_bus_arready) {
        vlSelfRef.__PVT__dma_bus_ar_rData_id = 0U;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rValidN) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_rData_offset 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_payload_offset;
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_read_cmd_valid) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem_spinal_port1 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem
            [(3U & (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__ptr_fetch))];
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_ready) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_s2mPipe_rData_ups 
            = ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN)
                ? (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS)
                : (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_ups));
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid)))) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_param 
            = ((((~ (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests) 
                      & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask)) 
                     | (0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param)))) 
                 & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire)) 
                | ((1U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode)) 
                   | (0U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode))))
                ? 2U : 1U);
    }
    vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__compactor__DOT__onAw_toW_payload_offset 
        = (3U & ((~ ((0x000000ffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__dma_bus_aw_rData_size))) 
                     - (IData)(1U))) & vlSelfRef.__PVT__dma_bus_aw_rData_addr));
    if (vlSelfRef.__VdlySet__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem[vlSelfRef.__VdlyDim0__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0] 
            = vlSelfRef.__VdlyVal__dma_bridge_write_bridge__DOT__aligner__DOT__context_mem__v0;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98 = ((4U 
                                                  == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)) 
                                                 | (6U 
                                                    == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_opcode)));
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_rData_opcode 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_opcode;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_1_LAST 
            = vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_LAST;
    }
    if (vlSelfRef.__PVT__dma_bus_wready) {
        vlSelfRef.__PVT__dma_bus_w_rData_last = vlSelfRef.__PVT__dma_bus_wlast;
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_handle_ready_output) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__upR_rsp_handle_CTX_id 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1) 
                              >> 1U));
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rValidN) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_wCmd_rData_ups 
            = vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS;
    }
    if (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_ready_output) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode 
            = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode;
    }
    vlSelfRef.__PVT__dma_bus_wlast = ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__chunk_r) 
                                      == (0x0000001fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__count_r))));
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_ready) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_s2mPipe_rData_opcode 
            = ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN)
                ? (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode)
                : (IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_opcode));
    }
    if (vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_read_cmd_valid) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem_spinal_port1 
            = vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem
            [(3U & (IData)(vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__ptr_fetch))];
    }
    if (vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_ready_output) {
        vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_allocateSlot_split_spliter_CHUNKS_WORDS 
            = (0x0000000fU & ((IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordEnd) 
                              - (IData)(vlSelfRef.__PVT__dma_bridge_write_bridge__DOT__aligner__DOT__frontend_split_spliter_chunkWordStart)));
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_ready) {
        if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_param 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode 
                = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode;
        } else {
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_param 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_param;
            vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode 
                = vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_opcode;
        }
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire 
        = ((7U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode)) 
           | (6U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_opcode)));
    if (vlSelfRef.__VdlySet__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0) {
        vlSelfRef.__PVT__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem[vlSelfRef.__VdlyDim0__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0] 
            = vlSelfRef.__VdlyVal__dma_bridge_read_bridge__DOT__aligner__DOT__context_mem__v0;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire) 
           & (2U != (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_param)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_isAcquire) 
           & (8U == (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_source)));
    if (vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) {
        vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_c_rData_opcode 
            = vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode;
    }
    if (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rValidN) {
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_param 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1;
        vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_rData_opcode 
            = vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask 
        = (1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_selfMask)));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_fromNone)))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask = 1U;
    }
    if ((0U != (0x81000000U & vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_spawn_CMD_address))) {
        vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask = 0U;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats 
        = ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode)) 
           | (1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rData_opcode)));
}

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__58(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__58\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__dma_bus_wstrb = (0x0000000fU & 
                                      ((IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__tail_be_r) 
                                       | (- (IData)(
                                                    (1U 
                                                     & (~ (IData)(vlSymsp->TOP__sim.__PVT__KL_mbx_dma__DOT__last_word_w)))))));
}

extern const VlWide<16>/*511:0*/ Vsim__ConstPool__CONST_hcb361019_0;

void Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0(Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_setsBusy_hit_mem_port 
        = (IData)((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                    >> 8U) & ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid)
                               ? ((IData)(vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_e_rData_sink) 
                                  >> 8U) : (vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
                                            >> 0x00000010U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_rsp 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassValid)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_checkConflicts_targetPort_bypass_bypassData)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_target_mem_spinal_port1));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_hitOh_3 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_set) 
              == (0x000000ffU & (vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_c_s2mPipe_rData_address 
                                 >> 6U))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_0_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_done 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_probeAckDataCompleted)) 
               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_pending))) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_1_valid));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_TO_DOWN) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_2_valid));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102 = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_fired) 
                                                  | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_0_BUFFER_ID 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_locked)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_lockedValue)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_buffer_firstFree));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_stages_0_SLOT_ID 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotLock)
            ? (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__backend_allocateSlot_slotReg)
            : (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_freeId));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_rsp_bypass_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
           & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_fired)) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toProbe_hit)));
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
    vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid 
        = ((~ ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_cmdSent) 
               | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_victim))) 
           & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__PVT__LsuL1Plugin_logic_refill_slots_0_valid));
    if ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__vexiis_0_iBus_bus_a_halfPipe_rData_opcode;
    } else if ((1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param))) {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source = 8U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask = 0U;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__vexiis_0_lsuL1Bus_bus_a_rData_opcode;
    } else {
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_data 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_data;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_source 
            = (0x00000010U | (IData)(vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_source));
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_mask 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_mask;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_address 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_address;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_size;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_param_1 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_param;
        vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode 
            = vlSelfRef.__PVT__dma_filter_down_to_splited_wc_cBus_up_bus_a_s2mPipe_rData_opcode;
    }
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit 
        = ((vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1 
            >> 0x0000000eU) & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_fired) 
                                   | vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__slots_ctx_spinal_port1)) 
                               & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_LAST)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_fired)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_payload_mask));
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
    vlSelfRef.__PVT__peripheral_bus_arbiter_core__DOT__a_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000000fU & ((((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub_io_down_a_valid) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__vexiis_0_dBus_to_ioBus_down_bus_a_rValid))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toUp_upD_valid 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102)) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid));
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
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__setsBusy_hit_downD_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_stages_1_valid) 
           & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__downD_toSetsBusy_hit));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82 = (1U 
                                                 & (~ 
                                                    ((5U 
                                                      == (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode)) 
                                                     | (7U 
                                                        == (IData)(vlSelfRef.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_payload_opcode)))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_2 
        = ((IData)(vlSelfRef.__PVT__splited_wc_cBus_to_splited_wc_hub_hub_up_down_bus_a_s2mPipe_rValid) 
           & ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard)) 
              & (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_withBeats)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__when_Pipeline_l282 
        = (1U & ((~ ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__initializer_counter) 
                     >> 8U)) | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_spawn_dataSplit_hazard)));
    vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_last 
        = (1U & ((~ ((0U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)) 
                     | (1U == (IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz___05Fzz_io_output_payload_opcode)))) 
                 | ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT__io_output_tracker_beat) 
                    == (0x0000000fU & (0xff731000U 
                                       >> ((IData)(vlSelfRef.__PVT__splited_wc_cBus_arbiter_core__DOT__a_arbiter__DOT___zz_io_output_payload_size) 
                                           << 2U))))));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_push_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_valid) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__frontendA_stages_1_ready 
        = ((~ (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_cmd_requests)) 
           & ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT___zz_probe_push_ready) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103)));
    vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_stages_0_valid 
        = ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_wake_insertion_hits_roundRobinMasked_doubleMask_range_4_to_5) 
           | ((IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_3_done) 
              | (IData)(vlSelfRef.__PVT__splited_wc_hub_hub_logic_hub__DOT__probe_slots_2_done)));
}
