// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

extern const VlUnpacked<IData/*31:0*/, 16> Vsim__ConstPool__TABLE_h1e660d21_0;

void Vsim_sim___nba_sequent__TOP__sim__50(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__50\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_valid = 0U;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_valid = 1U;
            }
        }
    }
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_w_ready = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_w_ready = 1U;
                }
            }
        }
    }
    vlSelfRef.__PVT__soc_vexiiriscv_interrupt = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_interrupt = ((0xfffffff9U 
                                                  & vlSelfRef.__PVT__soc_vexiiriscv_interrupt) 
                                                 | ((((IData)(vlSelfRef.__PVT__zero_pending) 
                                                      & (IData)(vlSelfRef.__PVT__enable_storage)) 
                                                     << 2U) 
                                                    | ((0U 
                                                        != 
                                                        ((IData)(vlSelfRef.__PVT__soc_pending_status) 
                                                         & (IData)(vlSelfRef.__PVT__soc_enable_storage))) 
                                                       << 1U)));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__last_word_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w) 
         & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_wlast));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_data_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__last_word_w)
          ? (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_data 
             & Vsim__ConstPool__TABLE_h1e660d21_0[vlSelfRef.__PVT__KL_mbx_dma__DOT__tail_be_r])
          : vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_data);
}

void Vsim_sim___nba_comb__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__soc_adapted_interface_adr = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            vlSelfRef.__PVT__soc_adapted_interface_adr 
                = (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awaddr 
                   >> 2U);
        }
    }
    vlSelfRef.__PVT__builder_rhs_self0 = vlSelfRef.__PVT__soc_adapted_interface_adr;
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = 0U;
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = ((4U & (IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel)) 
                                              | (((0x10U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (vlSelfRef.__PVT__builder_rhs_self0 
                                                       >> 0x0bU))) 
                                                  << 1U) 
                                                 | (1U 
                                                    & (~ 
                                                       (vlSelfRef.__PVT__builder_rhs_self0 
                                                        >> 0x0fU)))));
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = ((3U & (IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel)) 
                                              | ((0x8800U 
                                                  <= 
                                                  (0x0000ffffU 
                                                   & vlSelfRef.__PVT__builder_rhs_self0)) 
                                                 << 2U));
    vlSelfRef.__PVT__add_devices_mmap_bus_adr = (0x3fffffffU 
                                                 & (vlSelfRef.__PVT__builder_rhs_self0 
                                                    - (IData)(0x00400000U)));
    vlSelfRef.__PVT__ctrlmemory1_slave_sel = 0U;
    vlSelfRef.__PVT__ctrlmemory1_slave_sel = ((0x0cU 
                                               & (IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel)) 
                                              | (((2U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__builder_rhs_self0 
                                                       >> 0x0dU))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (3U 
                                                     & (vlSelfRef.__PVT__builder_rhs_self0 
                                                        >> 0x0eU)))));
    vlSelfRef.__PVT__ctrlmemory1_slave_sel = ((3U & (IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel)) 
                                              | (((0x6200U 
                                                   <= 
                                                   (0x0000ffffU 
                                                    & vlSelfRef.__PVT__builder_rhs_self0)) 
                                                  << 3U) 
                                                 | ((0x30U 
                                                     == 
                                                     (0x0000007fU 
                                                      & (vlSelfRef.__PVT__builder_rhs_self0 
                                                         >> 9U))) 
                                                    << 2U)));
    vlSelfRef.__PVT__builder_slave_sel = 0U;
    vlSelfRef.__PVT__builder_slave_sel = ((0x1cU & (IData)(vlSelfRef.__PVT__builder_slave_sel)) 
                                          | (((0x0400U 
                                               == (0x00003fffU 
                                                   & (vlSelfRef.__PVT__builder_rhs_self0 
                                                      >> 0x10U))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0x00003fffU 
                                                 & (vlSelfRef.__PVT__builder_rhs_self0 
                                                    >> 0x10U)))));
    vlSelfRef.__PVT__builder_slave_sel = ((0x13U & (IData)(vlSelfRef.__PVT__builder_slave_sel)) 
                                          | (((1U == 
                                               (0x000000ffU 
                                                & (vlSelfRef.__PVT__builder_rhs_self0 
                                                   >> 0x16U))) 
                                              << 3U) 
                                             | ((0x00010000U 
                                                 == 
                                                 (0x0001ffffU 
                                                  & (vlSelfRef.__PVT__builder_rhs_self0 
                                                     >> 0x0dU))) 
                                                << 2U)));
    vlSelfRef.__PVT__builder_slave_sel = ((0x0fU & (IData)(vlSelfRef.__PVT__builder_slave_sel)) 
                                          | ((0xf000U 
                                              == (0x0000ffffU 
                                                  & (vlSelfRef.__PVT__builder_rhs_self0 
                                                     >> 0x0eU))) 
                                             << 4U));
    vlSelfRef.__PVT__add_devices_mmap_source_payload_data = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                    vlSelfRef.__PVT__add_devices_mmap_source_payload_data = 0x0000deadU;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_data 
                    = ((vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                        << 2U) | (IData)(vlSelfRef.__PVT__add_devices_mmap_byte_count));
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_data = 0x0000000bU;
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value3 = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                        vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value3 
                            = (0x3fffffffU & ((IData)(1U) 
                                              + vlSelfRef.__PVT__add_devices_mmap_burst_adr));
                    }
                }
            }
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value3 
                = vlSelfRef.__PVT__add_devices_mmap_bus_adr;
        }
    }
    vlSelfRef.__PVT__builder_shared_dat_r = ((((((- (IData)(
                                                            (1U 
                                                             & (IData)(vlSelfRef.__PVT__builder_slave_sel_r)))) 
                                                 & ((vlSelfRef.__PVT__rom_bank0_dat0 
                                                     & (- (IData)(
                                                                  (1U 
                                                                   & (IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel))))) 
                                                    | (vlSelfRef.__PVT__rom_bank1_dat0 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & ((IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel) 
                                                                        >> 1U))))))) 
                                                | ((- (IData)(
                                                              (1U 
                                                               & ((IData)(vlSelfRef.__PVT__builder_slave_sel_r) 
                                                                  >> 1U)))) 
                                                   & (((- (IData)(
                                                                  (1U 
                                                                   & (IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel)))) 
                                                       & vlSelfRef.__PVT__sram_bank0
                                                       [vlSelfRef.__PVT__sram_bank0_adr0]) 
                                                      | (((- (IData)(
                                                                     (1U 
                                                                      & ((IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel) 
                                                                         >> 1U)))) 
                                                          & vlSelfRef.__PVT__sram_bank1
                                                          [vlSelfRef.__PVT__sram_bank1_adr0]) 
                                                         | ((- (IData)(
                                                                       (1U 
                                                                        & ((IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel) 
                                                                           >> 2U)))) 
                                                            & vlSelfRef.__PVT__sram_bank2
                                                            [vlSelfRef.__PVT__sram_bank2_adr0]))))) 
                                               | ((- (IData)(
                                                             (1U 
                                                              & ((IData)(vlSelfRef.__PVT__builder_slave_sel_r) 
                                                                 >> 2U)))) 
                                                  & vlSymsp->TOP.mbx_host_rdata)) 
                                              | ((- (IData)(
                                                            (1U 
                                                             & ((IData)(vlSelfRef.__PVT__builder_slave_sel_r) 
                                                                >> 3U)))) 
                                                 & vlSelfRef.__PVT__add_devices_mmap_bus_dat_r)) 
                                             | ((- (IData)(
                                                           (1U 
                                                            & ((IData)(vlSelfRef.__PVT__builder_slave_sel_r) 
                                                               >> 4U)))) 
                                                & vlSelfRef.__PVT__builder_interface0_dat_r));
    if ((0U == vlSelfRef.__PVT__builder_count)) {
        vlSelfRef.__PVT__builder_shared_dat_r = 0xffffffffU;
    }
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_data 
        = ((IData)(vlSelfRef.__PVT__builder_litespi_grant)
            ? vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_data
            : vlSelfRef.__PVT__add_devices_mmap_source_payload_data);
    vlSelfRef.__PVT__soc_data_socbushandler_next_value1 = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_data_socbushandler_next_value1 
                        = vlSelfRef.__PVT__builder_shared_dat_r;
                }
            }
        }
    }
}

void Vsim_sim___nba_comb__TOP__sim__1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__ctrlmemory1_bus_cyc;
    __PVT__ctrlmemory1_bus_cyc = 0;
    // Body
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 0U;
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 
                    = (1U & (~ (IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)));
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 
                    = (1U & (~ (IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)));
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
            }
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                         >> 1U)))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 
                    = (1U & (~ (IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)));
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
            }
        }
    }
    vlSelfRef.__PVT__soc_adapted_interface_stb = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_cyc = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                vlSelfRef.__PVT__soc_adapted_interface_stb 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_wvalid;
                vlSelfRef.__PVT__soc_adapted_interface_cyc 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_wvalid;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            vlSelfRef.__PVT__soc_adapted_interface_stb = 1U;
            vlSelfRef.__PVT__soc_adapted_interface_cyc = 1U;
        }
    }
    vlSelfRef.__PVT__builder_rhs_self4 = vlSelfRef.__PVT__soc_adapted_interface_stb;
    vlSelfRef.__PVT__builder_rhs_self3 = vlSelfRef.__PVT__soc_adapted_interface_cyc;
    vlSelfRef.__PVT__ctrlmemory0_bus_cyc = ((IData)(vlSelfRef.__PVT__builder_rhs_self3) 
                                            & (IData)(vlSelfRef.__PVT__builder_slave_sel));
    __PVT__ctrlmemory1_bus_cyc = ((IData)(vlSelfRef.__PVT__builder_rhs_self3) 
                                  & ((IData)(vlSelfRef.__PVT__builder_slave_sel) 
                                     >> 1U));
    vlSelfRef.__PVT__adapted_interface_cyc = ((IData)(vlSelfRef.__PVT__builder_rhs_self3) 
                                              & ((IData)(vlSelfRef.__PVT__builder_slave_sel) 
                                                 >> 3U));
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma0 = 
        ((IData)(vlSelfRef.__PVT__builder_rhs_self3) 
         & (((IData)(vlSelfRef.__PVT__builder_slave_sel) 
             >> 2U) & ((~ (IData)(vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r)) 
                       & (IData)(vlSelfRef.__PVT__builder_rhs_self4))));
    vlSelfRef.__PVT__builder_interface0_cyc = ((IData)(vlSelfRef.__PVT__builder_rhs_self3) 
                                               & ((IData)(vlSelfRef.__PVT__builder_slave_sel) 
                                                  >> 4U));
    vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc = ((IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel) 
                                                  & (IData)(__PVT__ctrlmemory1_bus_cyc));
    vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc = (((IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel) 
                                                   >> 1U) 
                                                  & (IData)(__PVT__ctrlmemory1_bus_cyc));
    vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc = (((IData)(vlSelfRef.__PVT__ctrlmemory1_slave_sel) 
                                                   >> 2U) 
                                                  & (IData)(__PVT__ctrlmemory1_bus_cyc));
    vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
    vlSelfRef.__PVT__builder_litespi_next_state = vlSelfRef.__PVT__builder_litespi_state;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
                }
            }
        } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
            vlSelfRef.__PVT__builder_litespi_next_state = 0U;
        }
    } else {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                         & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                        vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                        vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                    }
                }
            }
        }
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                    if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                        vlSelfRef.__PVT__builder_litespi_next_state = 8U;
                    }
                } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                    vlSelfRef.__PVT__builder_litespi_next_state = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                    vlSelfRef.__PVT__builder_litespi_next_state = 6U;
                }
            } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                vlSelfRef.__PVT__builder_litespi_next_state 
                    = ((0U == (IData)(vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage))
                        ? 7U : 5U);
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                    vlSelfRef.__PVT__builder_litespi_next_state = 4U;
                }
            } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                vlSelfRef.__PVT__builder_litespi_next_state = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                vlSelfRef.__PVT__builder_litespi_next_state = 2U;
            }
        } else if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                    & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                vlSelfRef.__PVT__builder_litespi_next_state 
                    = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                        & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                           == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                        ? 7U : 1U);
            }
        }
    }
}

void Vsim_sim___nba_comb__TOP__sim__2(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__add_devices_mmap_request = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_request 
                = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                                  & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                     == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                        vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_request 
                = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                                  & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                     == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                        vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_request 
                = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                                  & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                     == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                        vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                    }
                }
            }
        } else {
            vlSelfRef.__PVT__add_devices_mmap_request = 1U;
        }
    } else if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        vlSelfRef.__PVT__add_devices_mmap_request = 1U;
    } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        vlSelfRef.__PVT__add_devices_mmap_request = 1U;
    } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        vlSelfRef.__PVT__add_devices_mmap_request = 1U;
    } else {
        vlSelfRef.__PVT__add_devices_mmap_request = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
        if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
             & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                              & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                 == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                    vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                }
            }
        }
    }
    if (vlSelfRef.__PVT__builder_wishbone2csr_state) {
        vlSelfRef.__PVT__builder_wishbone2csr_next_state = 1U;
        vlSelfRef.__PVT__builder_wishbone2csr_next_state = 0U;
    } else {
        vlSelfRef.__PVT__builder_wishbone2csr_next_state = 0U;
        if (((IData)(vlSelfRef.__PVT__builder_interface0_cyc) 
             & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
            vlSelfRef.__PVT__builder_wishbone2csr_next_state = 1U;
        }
    }
    vlSelfRef.__PVT__builder_interface1_re = 0U;
    vlSelfRef.__PVT__builder_interface1_we = 0U;
    vlSelfRef.__PVT__builder_interface1_adr = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_wishbone2csr_state)))) {
        if (((IData)(vlSelfRef.__PVT__builder_interface0_cyc) 
             & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
            vlSelfRef.__PVT__builder_interface1_re 
                = ((~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                   & (0U != (IData)(vlSelfRef.__PVT__builder_rhs_self2)));
            vlSelfRef.__PVT__builder_interface1_we 
                = ((IData)(vlSelfRef.__PVT__builder_rhs_self5) 
                   & (0U != (IData)(vlSelfRef.__PVT__builder_rhs_self2)));
            vlSelfRef.__PVT__builder_interface1_adr 
                = (0x00003fffU & vlSelfRef.__PVT__builder_rhs_self0);
        }
    }
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = ((0x0eU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we)) 
                                             | ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                 & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                & (IData)(vlSelfRef.__PVT__builder_rhs_self2)));
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = ((0x0dU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 1U)) 
                                                << 1U));
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = ((0x0bU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 2U)) 
                                                << 2U));
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = ((7U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 3U)) 
                                                << 3U));
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = ((0x0eU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we)) 
                                             | ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                 & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                & (IData)(vlSelfRef.__PVT__builder_rhs_self2)));
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = ((0x0dU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 1U)) 
                                                << 1U));
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = ((0x0bU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 2U)) 
                                                << 2U));
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = ((7U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 3U)) 
                                                << 3U));
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = ((0x0eU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we)) 
                                             | ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                 & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                & (IData)(vlSelfRef.__PVT__builder_rhs_self2)));
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = ((0x0dU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 1U)) 
                                                << 1U));
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = ((0x0bU 
                                              & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 2U)) 
                                                << 2U));
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = ((7U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we)) 
                                             | (((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc) 
                                                   & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
                                                  & (IData)(vlSelfRef.__PVT__builder_rhs_self5)) 
                                                 & ((IData)(vlSelfRef.__PVT__builder_rhs_self2) 
                                                    >> 3U)) 
                                                << 3U));
    vlSelfRef.__PVT__builder_litespi_request = (((IData)(vlSelfRef.__PVT__add_devices_master_cs_storage) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.__PVT__add_devices_mmap_request));
    vlSelfRef.__PVT__add_devices_mmap_cs = 0U;
    if (vlSelfRef.__PVT__add_devices_mmap_request) {
        vlSelfRef.__PVT__add_devices_mmap_cs = 1U;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_reset_re = 0U;
    if ((IData)((0U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_reset_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_scratch_re = 0U;
    if ((IData)((1U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_scratch_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank2_req_re = 0U;
    if ((IData)((0x3800U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank2_req_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_clk_divisor_re = 0U;
    if ((IData)((0x0600U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_clk_divisor_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_mode_re = 0U;
    if ((IData)((0x0601U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_mode_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_clk_divisor_re = 0U;
    if ((IData)((0x0602U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_clk_divisor_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_dummy_bits_re = 0U;
    if ((IData)((0x0603U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_dummy_bits_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_cs_re = 0U;
    if ((IData)((0x0604U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_cs_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
}

void Vsim_sim___nba_comb__TOP__sim__3(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re = 0U;
    if ((IData)((0x0605U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__add_devices_master_rxtx_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_clk_divisor_re = 0U;
    if ((IData)((0x0608U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_clk_divisor_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_load_re = 0U;
    if ((IData)((0x0800U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_load_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_reload_re = 0U;
    if ((IData)((0x0801U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_reload_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_en_re = 0U;
    if ((IData)((0x0802U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_en_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_update_value_re = 0U;
    if ((IData)((0x0803U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_update_value_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_pending_re = 0U;
    if ((IData)((0x0806U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_pending_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_enable_re = 0U;
    if ((IData)((0x0807U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_enable_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__soc_rxtx_re = 0U;
    if ((IData)((0x0400U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__soc_rxtx_re = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_pending_re = 0U;
    if ((IData)((0x0404U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_pending_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_enable_re = 0U;
    if ((IData)((0x0405U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_enable_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__add_devices_master_rxtx_we = 0U;
    if ((IData)((0x0606U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__add_devices_master_rxtx_re 
            = vlSelfRef.__PVT__builder_interface1_we;
        vlSelfRef.__PVT__add_devices_master_rxtx_we 
            = vlSelfRef.__PVT__builder_interface1_re;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cfg_re = 0U;
    if ((IData)((0x3a00U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cfg_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_mem_re = 0U;
    if ((IData)((0x3a01U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_mem_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cmd_re = 0U;
    if ((IData)((0x3a02U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cmd_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__add_devices_crossbar_cs = vlSelfRef.__PVT__add_devices_master_cs_storage;
        vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready 
            = (1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid)) 
                     | (IData)(vlSelfRef.__PVT__add_devices_master_rxtx_we)));
    } else {
        vlSelfRef.__PVT__add_devices_crossbar_cs = vlSelfRef.__PVT__add_devices_mmap_cs;
        vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready 
            = (1U & (IData)(vlSelfRef.__PVT__add_devices_mmap_sink_ready));
    }
}

void Vsim_sim___nba_sequent__TOP__sim__51(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__51\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w = (1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r) 
                                                     | (0U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__fill_req_w = 
        ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101) 
         & ((1U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
            & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r) 
               != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r))));
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma11 = 0x0fU;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)))) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma11 
            = (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
                ? (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_be_r)
                : (IData)(vlSelfRef.__PVT__builder_rhs_self2));
    }
    if (vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma8 
            = (6U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r));
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
            = ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r)
                ? vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_wdata_r
                : vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_data_w);
    } else if (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma8 
            = vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_we_r;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
            = vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_wdata_r;
    } else {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma8 
            = vlSelfRef.__PVT__builder_rhs_self5;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
            = vlSelfRef.__PVT__builder_rhs_self1;
    }
}

void Vsim_sim___nba_comb__TOP__sim__4(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_next_state = vlSelfRef.__PVT__builder_state;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__builder_next_state 
                    = ((IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)
                        ? 3U : 1U);
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__builder_next_state = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__builder_next_state = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__builder_next_state 
                    = ((IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)
                        ? 3U : 1U);
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__builder_next_state = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__builder_next_state = 3U;
            }
        } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_bready) {
            vlSelfRef.__PVT__builder_next_state = 0U;
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (vlSelfRef.__PVT__builder_shared_ack) {
                vlSelfRef.__PVT__builder_next_state = 4U;
            }
        } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_rready) {
            vlSelfRef.__PVT__builder_next_state = 0U;
        }
    } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if (vlSelfRef.__PVT__builder_shared_ack) {
            vlSelfRef.__PVT__builder_next_state = 2U;
        }
    } else if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
        vlSelfRef.__PVT__builder_next_state = ((IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)
                                                ? 3U
                                                : 1U);
    } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
        vlSelfRef.__PVT__builder_next_state = 1U;
    } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
        vlSelfRef.__PVT__builder_next_state = 3U;
    }
}

void Vsim_sim___nba_comb__TOP__sim__5(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma9 = vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)))) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma9 
            = (0x00001fffU & (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
                               ? (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_addr_r)
                               : vlSelfRef.__PVT__builder_rhs_self0));
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rValid) 
                                                & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_rready));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__rel 
        = (0x00007fffU & (((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                           << 2U) - (IData)(0x0800U)));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if 
        = (0x01ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_srcs 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if) 
                          - (IData)(0x0080U)));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_sinks 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if) 
                          - (IData)(0x0100U)));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__src_entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_srcs) 
           >> 3U);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_sinks) 
           >> 4U);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w = (1U & 
                                              ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__rel) 
                                               >> 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w = (0x0100U 
                                                <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w)) 
                                               & (0x0080U 
                                                  <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_s_w = (0x0000000fU 
                                             & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__src_entry));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_k_w = (0x0000000fU 
                                             & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w)
                                                ? (0x000fU 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_sinks))
                                                : ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)
                                                    ? 
                                                   (7U 
                                                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_srcs))
                                                    : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__pub_at_w = (((0x0800U 
                                                <= 
                                                ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                 << 2U)) 
                                               & (1U 
                                                  > 
                                                  ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__rel) 
                                                   >> 9U))) 
                                              & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w)
                                                  ? 
                                                 ((0x0010U 
                                                   > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__entry)) 
                                                  & (((0U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)) 
                                                      | (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))) 
                                                     | (8U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))))
                                                  : 
                                                 ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)
                                                   ? 
                                                  ((0x0010U 
                                                    > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__src_entry)) 
                                                   & ((0U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)) 
                                                      | (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))))
                                                   : 
                                                  (((((0U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)) 
                                                      | (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))) 
                                                     | (8U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))) 
                                                    | (0x000cU 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))) 
                                                   | (0x0010U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w))))));
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel 
        = (0x00007fffU & (((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                           << 2U) - (IData)(0x0200U)));
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry 
        = (0x000fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__entry 
        = (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel) 
                      >> 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__bnd_if_w = (1U & 
                                              ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel) 
                                               >> 8U));
    vlSelfRef.__PVT__KL_mbx__DOT__bnd_entry_w = (0x0000001fU 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w = 0U;
    if ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w = 1U;
    }
    if ((8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w = 2U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__bnd_at_w = ((((0x0200U 
                                                 <= 
                                                 ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                  << 2U)) 
                                                & (1U 
                                                   > 
                                                   ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel) 
                                                    >> 8U))) 
                                               & (0x0010U 
                                                  > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__entry))) 
                                              & (((0U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry)) 
                                                  | (4U 
                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry))) 
                                                 | (8U 
                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry))));
    vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__rel 
        = (0x00007fffU & (((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                           << 2U) - (IData)(0x6000U)));
    vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if 
        = (0x03ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__face_if_w = (1U & 
                                               ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__rel) 
                                                >> 0x0000000aU));
    vlSelfRef.__PVT__KL_mbx__DOT__face_area_w = ((0x0200U 
                                                  <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if))
                                                  ? 2U
                                                  : 
                                                 ((0x0100U 
                                                   <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if))
                                                   ? 1U
                                                   : 0U));
    if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if) 
                               - (IData)(0x0200U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w = 
            (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if) 
                        - (IData)(0x0200U)));
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if) 
                               - (IData)(0x0100U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w = 
            ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))
              ? (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if) 
                            - (IData)(0x0100U))) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__face_s_w = (0x0000000fU 
                                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__face_k_w = (0x0000000fU 
                                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__face_at_w = (((0x6000U 
                                                 <= 
                                                 ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                  << 2U)) 
                                                & (1U 
                                                   > 
                                                   ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__rel) 
                                                    >> 0x0000000aU))) 
                                               & ((((0U 
                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w)) 
                                                    & (((((((((((((((((((((((((((((((((((((0U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)) 
                                                                                | (4U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (8U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x000cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0010U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0014U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0018U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x001cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0040U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0044U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x0048U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                                | (0x004cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                               | (0x0050U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                              | (0x0060U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                             | (0x0064U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                            | (0x0068U 
                                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                           | (0x006cU 
                                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                          | (0x0070U 
                                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                         | (0x0074U 
                                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                        | (0x0080U 
                                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                       | (0x0084U 
                                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                      | (0x0088U 
                                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                     | (0x008cU 
                                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                    | (0x0090U 
                                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                   | (0x0094U 
                                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                  | (0x0098U 
                                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                 | (0x009cU 
                                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                                | (0x00a0U 
                                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                               | (0x00a4U 
                                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                              | (0x00c0U 
                                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                             | (0x00c4U 
                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                            | (0x00c8U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                           | (0x00ccU 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                          | (0x00d0U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                         | (0x00d4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                        | (0x00d8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                       | (0x00dcU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                                                   | (((1U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w)) 
                                                       & (0x0010U 
                                                          > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry))) 
                                                      & ((((0U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)) 
                                                           | (4U 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                          | (8U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                         | (0x000cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))))) 
                                                  | (((2U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w)) 
                                                      & (0x0010U 
                                                         > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry))) 
                                                     & (((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                                                        | (8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))))));
}

void Vsim_sim___nba_comb__TOP__sim__6(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w = (
                                                   (~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__rerr_r) 
                                                     | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_resp) 
                                                        >> 1U))) 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w = 
        (0x0000000fU & (VL_MULS_III(32, (IData)(0x00000010U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_if_w)) 
                        + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_entry_w)));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_end_w = 
        ((6U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
         & (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) 
             & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_last_r)) 
            | ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w) 
               & ((~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w)) 
                  & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_last)))));
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma7 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)
          ? ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__fill_req_w) 
             | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w))
          : (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) 
             || (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma0)));
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i 
        = ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_at_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_108 = ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7) 
                                                  & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma8));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_w = ((~ (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma8)) 
                                          & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w 
        = ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrd_r) 
               | (IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i))) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r));
    vlSelfRef.__PVT__KL_mbx__DOT__refused_w = ((0x0fU 
                                                != (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma11)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_108));
    vlSelfRef.__PVT__KL_mbx__DOT__wr_w = ((0x0fU == (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma11)) 
                                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_108));
    vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_host_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
         & ((0x3000U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x3200U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_host_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
         & ((0x2000U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x2800U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_host_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
         & ((0x1800U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x1c00U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_host_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
                                                   & ((0x1000U 
                                                       <= 
                                                       ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                        << 2U)) 
                                                      & (0x1400U 
                                                         > 
                                                         ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                          << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_host_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
                                                   & ((0x4000U 
                                                       <= 
                                                       ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                        << 2U)) 
                                                      & (0x5000U 
                                                         > 
                                                         ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                          << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__evt_host_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w) 
                                                & ((0x0400U 
                                                    <= 
                                                    ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                     << 2U)) 
                                                   & (0x0500U 
                                                      > 
                                                      ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                                       << 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w 
        = ((((((((0x0fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                << 3U) | (((0x0eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                          << 2U)) | ((((0x0dU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                      << 1U) | ((0x0cU 
                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)))) 
             << 0x0000000cU) | ((((((0x0bU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                   << 3U) | (((0x0aU 
                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                             << 2U)) 
                                 | ((((9U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                      & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                     << 1U) | ((8U 
                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)))) 
                                << 8U)) | (((((((7U 
                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                               << 3U) 
                                              | (((6U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                                 << 2U)) 
                                             | ((((5U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                                 << 1U) 
                                                | ((4U 
                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)))) 
                                            << 4U) 
                                           | (((((3U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                                << 3U) 
                                               | (((2U 
                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                                  << 2U)) 
                                              | ((((1U 
                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w)) 
                                                  << 1U) 
                                                 | ((0U 
                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                                                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w))))));
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_at_w) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w));
    vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
          & ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w)) 
             && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r) 
                       >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))))) 
         & ((((((((((((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                          & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                         & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                        | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                            & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                           & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                       | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                           & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                          & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                      | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                          & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                         & (0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                     | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                         & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                        & (0x0010U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                    | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                        & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                       & (0x0014U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                   | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                       & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                      & (0x0018U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                  | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                      & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                     & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                 | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                     & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                    & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                    & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                   & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
               | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                   & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                  & (0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
              | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
             | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
            | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
               & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 1U;
    }
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
          & ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w)) 
             && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r) 
                       >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))))) 
         & (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0040U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (0x0044U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
            | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
               & (0x0048U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 1U;
    }
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
          & ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w)) 
             && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r) 
                       >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))))) 
         & (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0060U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (0x0064U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
            | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
               & (0x0068U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 1U;
    }
}

void Vsim_sim___nba_comb__TOP__sim__7(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_comb__TOP__sim__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__KL_mbx__DOT__tmr_cmd_p_w;
    __PVT__KL_mbx__DOT__tmr_cmd_p_w = 0;
    // Body
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
          & ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w)) 
             && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) 
                       >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))))) 
         & (((((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                   & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                  & (0x0080U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
                 | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                     & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                    & (0x0084U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
                | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                    & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                   & (0x0088U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
               | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                   & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                  & (0x008cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
              | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0090U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
             | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (0x0094U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
            | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
               & (0x0098U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 1U;
    }
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
          & ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w)) 
             && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r) 
                       >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))))) 
         & (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (0x00c0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
               | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                   & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                  & (0x00c4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
              | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x00c8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
             | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                & (0x00ccU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) 
            | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
               & (0x00d0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w = 1U;
    }
    __PVT__KL_mbx__DOT__tmr_cmd_p_w = ((0x000fU == (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9)) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w));
    vlSelfRef.__PVT__KL_mbx__DOT__reg_rd_w = ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__evt_host_w) 
                                                  | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_host_w) 
                                                     | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_host_w) 
                                                        | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_host_w) 
                                                           | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_host_w) 
                                                              | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_host_w))))))) 
                                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_w));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w 
        = ((IData)(__PVT__KL_mbx__DOT__tmr_cmd_p_w) 
           & ((0x10U > (0x000000ffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10)) 
              & ((1U == (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                         >> 0x0000001eU)) | (2U == 
                                             (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                              >> 0x0000001eU)))));
    vlSelfRef.__PVT__KL_mbx__DOT__tmr_bad_p_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w)) 
                                                 & (IData)(__PVT__KL_mbx__DOT__tmr_cmd_p_w));
}
