// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__19(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__19\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_slave_sel = ((0x0fU & (IData)(vlSelfRef.__PVT__builder_slave_sel)) 
                                          | ((0xf000U 
                                              == (0x0000ffffU 
                                                  & (vlSelfRef.__PVT__builder_rhs_self0 
                                                     >> 0x0eU))) 
                                             << 4U));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_end_w = 
        ((6U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
         & (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) 
             & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_last_r)) 
            | ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w) 
               & ((~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w)) 
                  & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_last)))));
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

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__20(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__20\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__ctrlmemory1_bus_cyc;
    __PVT__ctrlmemory1_bus_cyc = 0;
    // Body
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
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w = 
        (0x0000000fU & (VL_MULS_III(32, (IData)(0x00000010U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_if_w)) 
                        + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_entry_w)));
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
    vlSelfRef.__PVT__add_devices_mmap_request = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_request 
                = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
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
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
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
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                                  & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                     == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                        vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                    }
                }
            }
        } else {
            if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                vlSelfRef.__PVT__builder_litespi_next_state = 0U;
            }
            vlSelfRef.__PVT__add_devices_mmap_request = 1U;
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
            vlSelfRef.__PVT__add_devices_mmap_request = 1U;
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                    vlSelfRef.__PVT__builder_litespi_next_state = 4U;
                }
            } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                vlSelfRef.__PVT__builder_litespi_next_state = 3U;
            }
            vlSelfRef.__PVT__add_devices_mmap_request = 1U;
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if (vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready) {
                vlSelfRef.__PVT__builder_litespi_next_state = 2U;
            }
            vlSelfRef.__PVT__add_devices_mmap_request = 1U;
        } else {
            vlSelfRef.__PVT__add_devices_mmap_request 
                = vlSelfRef.__PVT__add_devices_mmap_burst_cs;
            if (((IData)(vlSelfRef.__PVT__adapted_interface_cyc) 
                 & (IData)(vlSelfRef.__PVT__builder_rhs_self4))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_rhs_self5)))) {
                    vlSelfRef.__PVT__builder_litespi_next_state 
                        = (((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                            & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                               == vlSelfRef.__PVT__add_devices_mmap_burst_adr))
                            ? 7U : 1U);
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                                  & (vlSelfRef.__PVT__add_devices_mmap_bus_adr 
                                     == vlSelfRef.__PVT__add_devices_mmap_burst_adr))))) {
                        vlSelfRef.__PVT__add_devices_mmap_request = 0U;
                    }
                }
            }
        }
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__21(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__21\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma7 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)
          ? ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__fill_req_w) 
             | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w))
          : (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) 
             || (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma0)));
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
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i 
        = ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_at_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_108 = ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7) 
                                                  & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma8));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_w = ((~ (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma8)) 
                                          & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7));
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
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re = 0U;
    if ((IData)((0x0605U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
    vlSelfRef.__PVT__add_devices_master_rxtx_re = 0U;
    if ((IData)((0x0606U == (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
        vlSelfRef.__PVT__add_devices_master_rxtx_re 
            = vlSelfRef.__PVT__builder_interface1_we;
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__22(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__22\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
        vlSelfRef.__PVT__add_devices_master_rxtx_we 
            = vlSelfRef.__PVT__builder_interface1_re;
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
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__23(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__23\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__KL_mbx__DOT__tmr_cmd_p_w;
    __PVT__KL_mbx__DOT__tmr_cmd_p_w = 0;
    // Body
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

VL_ATTR_COLD void Vsim_sim___ctor_var_reset_0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ctor_var_reset_0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->audio_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12462280889005755289ull);
    vlSelf->audio_tdm_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5413948399227823105ull);
    vlSelf->flash_cs = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7255794963022757664ull);
    vlSelf->flash_rx_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8802421814854729555ull);
    vlSelf->flash_rx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423837276700678229ull);
    vlSelf->flash_rx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17789749695252465462ull);
    vlSelf->flash_tx_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4182198138983956969ull);
    vlSelf->flash_tx_len = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3197588221592898328ull);
    vlSelf->flash_tx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13059070663017614748ull);
    vlSelf->flash_tx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17534642262895807053ull);
    vlSelf->flash_tx_width = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 669027698148927646ull);
    vlSelf->mbx_amap_wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13173040641504320749ull);
    vlSelf->mbx_asp_chg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9389837737349363835ull);
    vlSelf->mbx_avb_chg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1414334382951439449ull);
    vlSelf->mbx_domain = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13232456389494613888ull);
    vlSelf->mbx_gm_change = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10675885280483565098ull);
    vlSelf->mbx_gm_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5324599952719613123ull);
    vlSelf->mbx_host_ack = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15395814796466849453ull);
    vlSelf->mbx_host_addr = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 5590183630757749138ull);
    vlSelf->mbx_host_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8469723683417989429ull);
    vlSelf->mbx_host_req = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6052294283063882772ull);
    vlSelf->mbx_host_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7110123708436204860ull);
    vlSelf->mbx_host_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13776551202371385470ull);
    vlSelf->mbx_link_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3557674121578675774ull);
    vlSelf->mbx_ms_tick = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16892885806497512599ull);
    vlSelf->mbx_rx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15363302603865357597ull);
    vlSelf->mbx_rx_if = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1366435488215255091ull);
    vlSelf->mbx_rx_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4510311912441291199ull);
    vlSelf->mbx_rx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13693448134670629485ull);
    vlSelf->mbx_rx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10323207466166538961ull);
    vlSelf->mbx_tx_ch = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5923475415192670401ull);
    vlSelf->mbx_tx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11974658817752159988ull);
    vlSelf->mbx_tx_if = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2154894095737347039ull);
    vlSelf->mbx_tx_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13654315388401743911ull);
    vlSelf->mbx_tx_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17679267980591550443ull);
    vlSelf->mbx_tx_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13206040831982127523ull);
    vlSelf->milan_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16387643398324370288ull);
    vlSelf->serial_sink_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9573462725403686387ull);
    vlSelf->serial_sink_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3758950120267853273ull);
    vlSelf->serial_sink_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13511602996822676087ull);
    vlSelf->serial_source_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17344215306608104219ull);
    vlSelf->serial_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9973345444914751179ull);
    vlSelf->serial_source_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18327467128597415915ull);
    vlSelf->sim_trace = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16134794833742535666ull);
    vlSelf->sys_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7302336598091101382ull);
    vlSelf->sys_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 763759673302712755ull);
    vlSelf->__PVT__adapted_interface_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17082351601670825256ull);
    vlSelf->__PVT__add_devices_crossbar_source_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 99926532863404635ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4839044091566849127ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma10 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4906792606351869532ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma11 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2265286353438549211ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14990667514994181998ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma7 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6535706333835074549ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma8 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13748800464352430253ull);
    vlSelf->__PVT__add_devices_ctrlmailboxdma9 = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 821079053450750862ull);
    vlSelf->__PVT__builder_interface0_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6087995481848750024ull);
    vlSelf->__PVT__builder_litespi_request = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14495958849755072346ull);
    vlSelf->__PVT__ctrlmemory0_bus_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13003762934908008091ull);
    vlSelf->__PVT__ctrlmemory1_sram2_bus_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10819572599475074039ull);
    vlSelf->__PVT__ctrlmemory1_sram3_bus_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10644777971383823869ull);
    vlSelf->__PVT__ctrlmemory1_sram4_bus_cyc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15090957110291867857ull);
    vlSelf->__PVT__soc_rx_fifo_do_read = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9116994007664449531ull);
    vlSelf->__PVT__soc_tx_fifo_do_read = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4288677865716828907ull);
    for (int __Vi0 = 0; __Vi0 < 49; ++__Vi0) {
        vlSelf->__PVT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4032165174000709208ull);
    }
    vlSelf->__PVT__mem_dat0 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18323421414622234558ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__storage_1[__Vi0] = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 15654753350756652249ull);
    }
    vlSelf->__PVT__storage_1_dat1 = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8149492790143177989ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__storage_2[__Vi0] = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8314512570075127425ull);
    }
    vlSelf->__PVT__storage_2_dat1 = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 18079697672397464756ull);
    for (int __Vi0 = 0; __Vi0 < 32768; ++__Vi0) {
        vlSelf->__PVT__rom_bank0[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18430278542131642994ull);
    }
    vlSelf->__PVT__rom_bank0_dat0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14930865186502576043ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->__PVT__rom_bank1[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6144667060251706783ull);
    }
    vlSelf->__PVT__rom_bank1_dat0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10820945449670922465ull);
    for (int __Vi0 = 0; __Vi0 < 16384; ++__Vi0) {
        vlSelf->__PVT__sram_bank0[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3981872559970540971ull);
    }
    vlSelf->__PVT__sram_bank0_adr0 = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 641559921053932640ull);
    for (int __Vi0 = 0; __Vi0 < 8192; ++__Vi0) {
        vlSelf->__PVT__sram_bank1[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2048117831169176684ull);
    }
    vlSelf->__PVT__sram_bank1_adr0 = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 6990071207877931728ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->__PVT__sram_bank2[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4081763599285852335ull);
    }
    vlSelf->__PVT__sram_bank2_adr0 = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 6335232944260010862ull);
    vlSelf->__PVT__KL_mbx__DOT__now_ms_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17494694322056715809ull);
    vlSelf->__PVT__KL_mbx__DOT__wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15241363264925323672ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3340887846058623972ull);
    vlSelf->__PVT__KL_mbx__DOT__refused_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8245828905302964870ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14272437296117403539ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_off_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 10491877066733790373ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__rx_head_w, __VscopeHash, 5128974995855743156ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__rx_drop_w, __VscopeHash, 2834957262991586341ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__rate_drop_w, __VscopeHash, 14454767808520901256ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__rx_pass_w, __VscopeHash, 10065001716904964003ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__tx_tail_w, __VscopeHash, 5073308966616021393ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__tx_err_w, __VscopeHash, 7330217207826381628ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->__PVT__KL_mbx__DOT__tx_head_w, __VscopeHash, 9491600282596172522ull);
    vlSelf->__PVT__KL_mbx__DOT__tmr_bad_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11183210638663901473ull);
    vlSelf->__PVT__KL_mbx__DOT__rxw_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3215452931984775874ull);
    vlSelf->__PVT__KL_mbx__DOT__rxw_ch_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7947645912525241815ull);
    vlSelf->__PVT__KL_mbx__DOT__rxw_addr_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 9672030815094686121ull);
    vlSelf->__PVT__KL_mbx__DOT__rxw_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9988110272299590442ull);
    vlSelf->__PVT__KL_mbx__DOT__txr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 608056044654227254ull);
    vlSelf->__PVT__KL_mbx__DOT__txr_ch_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10478511905178337618ull);
    vlSelf->__PVT__KL_mbx__DOT__txr_addr_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 10433954462536077299ull);
    vlSelf->__PVT__KL_mbx__DOT__bnd_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11802283004866804094ull);
    vlSelf->__PVT__KL_mbx__DOT__bnd_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16863229520846617054ull);
    vlSelf->__PVT__KL_mbx__DOT__bnd_entry_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7916896871736965820ull);
    vlSelf->__PVT__KL_mbx__DOT__bnd_reg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5380672619304533532ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12456463370532017564ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_src_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17437210499300564429ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1086286173102394207ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8900895263469780079ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_s_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1086468499995711211ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_k_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6627662446021591339ull);
    vlSelf->__PVT__KL_mbx__DOT__pub_reg_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 15312092539238735263ull);
    vlSelf->__PVT__KL_mbx__DOT__face_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3397657611895464837ull);
    vlSelf->__PVT__KL_mbx__DOT__face_area_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17392260067441632518ull);
    vlSelf->__PVT__KL_mbx__DOT__face_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14628635565812263145ull);
    vlSelf->__PVT__KL_mbx__DOT__face_s_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5892940856432118508ull);
    vlSelf->__PVT__KL_mbx__DOT__face_k_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 885514396724613002ull);
    vlSelf->__PVT__KL_mbx__DOT__face_reg_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 13191335479445320382ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_bnd_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14492326848536236252ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_bnd_reg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16298603586759037587ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6558736467929746363ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_src_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13002589686173498362ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17205545933092850066ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15489597201297775250ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_s_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4274415010411642795ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_k_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14127250925796781474ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_pub_reg_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1118928239792709758ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3864726323777687329ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_area_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13636900585812838775ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4824739282046344876ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_s_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3180885200606065286ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_k_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15856417737863377201ull);
    vlSelf->__PVT__KL_mbx__DOT__rd_face_reg_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8163728819111269144ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_ctrl_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1052250179105354223ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_entity_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14400209752689825430ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_clock_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1543804448550134751ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_aecp_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 189452708720648592ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_restore_r[__Vi0] = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 6552209949141536050ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_f_nvm_r[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 687462433800985106ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_ctr_req_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13954709501388004858ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_ctr_word_r[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 13335900354286787021ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_amap_req_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17569962473289541617ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_amap_page_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14118497589795936999ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_req_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11619979990185248052ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_beat_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 45992125031871062ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_record_lo_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12344449046754101378ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_record_hi_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11710410175479419972ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_value_lo_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9742403319963021612ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_edit_value_hi_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6986169449837516040ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_gsi_req_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3651305237180765642ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_gsi_sel_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16804246332264165365ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_gsi_prop_lo_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15501185797655763219ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__face_gsi_prop_hi_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2305353408751993495ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_pt_offset_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17748847934465002369ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13972285938168656221ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7056804901916699800ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_src_valid_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11198701493957371030ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6451827485746047057ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 887608262500212160ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__face_f_snk_valid_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11450999176276217536ull);
        }
    }
    vlSelf->__PVT__KL_mbx__DOT__fw_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12918775791379235371ull);
    vlSelf->__PVT__KL_mbx__DOT__ctr_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10308039545115297750ull);
    vlSelf->__PVT__KL_mbx__DOT__ctr_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11297171377668303034ull);
    vlSelf->__PVT__KL_mbx__DOT__ctr_tmo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2718728299198230133ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__ctr_tag_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2516032606744709691ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__ctr_wait_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1140694623830865216ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__ctr_data_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2715908372811723672ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__amap_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2718923616359189894ull);
    vlSelf->__PVT__KL_mbx__DOT__amap_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9811346579058459009ull);
    vlSelf->__PVT__KL_mbx__DOT__amap_tmo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10565344318544869624ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__amap_tag_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 255020208135114123ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__amap_wait_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11948465650804616740ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__amap_data_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1745866655519814133ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__edit_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4694457654791011582ull);
    vlSelf->__PVT__KL_mbx__DOT__edit_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1707064368288747040ull);
    vlSelf->__PVT__KL_mbx__DOT__edit_tmo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15368411971112685304ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__edit_tag_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 158853030660336375ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__edit_wait_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13369975958680736878ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__edit_data_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10156460241301789980ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__gsi_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4226262152233552823ull);
    vlSelf->__PVT__KL_mbx__DOT__gsi_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10924350266582343833ull);
    vlSelf->__PVT__KL_mbx__DOT__gsi_tmo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2565415735740944206ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__gsi_tag_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8784621314219648945ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__gsi_wait_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12846589788547033984ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__gsi_data_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1710380275432370160ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__face_refused_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15884381195817973015ull);
    vlSelf->__PVT__KL_mbx__DOT__irq_enable_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14750709769726633667ull);
    vlSelf->__PVT__KL_mbx__DOT__tick_ctl_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11700239805875581824ull);
    vlSelf->__PVT__KL_mbx__DOT__own_eid_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8588230431423614589ull);
    vlSelf->__PVT__KL_mbx__DOT__own_eid_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1545235757357381395ull);
    vlSelf->__PVT__KL_mbx__DOT__filter_en_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7645162387204376681ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_base_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15924556301722837850ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_base_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5246511086893910467ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_count_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13108846424616581528ull);
    vlSelf->__PVT__KL_mbx__DOT__tmr_deadline_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17671573567381528220ull);
    vlSelf->__PVT__KL_mbx__DOT__evt_tail_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16591453244187689415ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__rx_tail_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1012193256498220741ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__tx_head_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10334045876197182945ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__own_mac_lo_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4311683365967856272ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__own_mac_hi_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4110441238173719555ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10632151148245024461ull);
    vlSelf->__PVT__KL_mbx__DOT__bus_err_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14735199179928204751ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__gm_hi_snap_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9519355317045632104ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__domain_snap_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16079378215431164154ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__pub_da_gate_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 305913195982724842ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__pub_licence_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16033375586984622049ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__pub_idle_slope_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2025969518742589712ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__pub_sr_domain_r[__Vi0] = VL_SCOPED_RAND_RESET_I(25, __VscopeHash, 2535497625653440014ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__pub_talker_decl_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7793369176523826893ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__pub_src_sid_lo_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16879193839792652407ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__pub_src_sid_hi_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8210869431469380516ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__pub_sid_lo_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11328379220984688584ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__pub_sid_hi_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9807422463687504402ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 16; ++__Vi1) {
            vlSelf->__PVT__KL_mbx__DOT__pub_binding_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14153254843426711149ull);
        }
    }
    VL_SCOPED_RAND_RESET_W(114, vlSelf->__PVT__KL_mbx__DOT__rd_hit_w, __VscopeHash, 6504737167956651698ull);
    vlSelf->__PVT__KL_mbx__DOT__reg_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11254866587681500667ull);
    vlSelf->__PVT__KL_mbx__DOT__evt_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11372395796227592082ull);
    vlSelf->__PVT__KL_mbx__DOT__evt_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15397082857827234870ull);
    vlSelf->__PVT__KL_mbx__DOT__adp_rx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7086337023208958928ull);
    vlSelf->__PVT__KL_mbx__DOT__adp_rx_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15876308669418814766ull);
    vlSelf->__PVT__KL_mbx__DOT__adp_tx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1431887857458680548ull);
    vlSelf->__PVT__KL_mbx__DOT__acmp_rx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18075192139537739886ull);
    vlSelf->__PVT__KL_mbx__DOT__acmp_rx_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9417197400720545549ull);
    vlSelf->__PVT__KL_mbx__DOT__acmp_tx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15417913717049513454ull);
    vlSelf->__PVT__KL_mbx__DOT__aecp_rx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7317490669609246167ull);
    vlSelf->__PVT__KL_mbx__DOT__aecp_rx_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9944815079540541953ull);
    vlSelf->__PVT__KL_mbx__DOT__aecp_tx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1697604538082241217ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_rx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16715259619689114605ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_rx_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15237428049073342732ull);
    vlSelf->__PVT__KL_mbx__DOT__maap_tx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11751282538697542012ull);
    vlSelf->__PVT__KL_mbx__DOT__srp_rx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3037294612873619022ull);
    vlSelf->__PVT__KL_mbx__DOT__srp_rx_host_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3739531390230079598ull);
    vlSelf->__PVT__KL_mbx__DOT__srp_tx_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17706817546061140107ull);
    vlSelf->__PVT__KL_mbx__DOT__ack_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4352937761790993646ull);
    vlSelf->__PVT__KL_mbx__DOT__reg_rdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6489311882831361143ull);
    vlSelf->__PVT__KL_mbx__DOT__rsel_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13263871009642063338ull);
    vlSelf->__PVT__KL_mbx__DOT__txr_ch_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12452441410138858925ull);
    vlSelf->__PVT__KL_mbx__DOT__reg_rd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8576097711100552455ull);
    vlSelf->__PVT__KL_mbx__DOT__txr_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15637206169397551511ull);
    vlSelf->KL_mbx__DOT____Vcellinp__u_rx__maap_base_i = 0;
    vlSelf->KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i = 0;
    vlSelf->KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i = 0;
    vlSelf->KL_mbx__DOT____Vcellinp__u_rx__own_eid_i = 0;
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_srp_tx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9683536637454641304ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_maap_tx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11055048358503254619ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_maap_rx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11821370431322544280ull);
    }
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_aecp_tx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13255262624227701995ull);
    }
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_aecp_rx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8996273535781373539ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_acmp_tx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5142002036185138470ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_acmp_rx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 104322327166806902ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_adp_tx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 297627259992889598ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_adp_rx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12496786465766999880ull);
    }
    vlSelf->KL_mbx__DOT__u_evt__DOT__wr_en_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5223533173290231196ull);
    vlSelf->KL_mbx__DOT__u_evt__DOT__wr_addr_o = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7040611212037063165ull);
    vlSelf->KL_mbx__DOT__u_evt__DOT__wr_data_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7339421343543720121ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__armed_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17181630922829842744ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10422700571686956876ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17559306916346878794ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 181386202790022857ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__scan_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 743699488889202490ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 667513641807341243ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14031640352628237892ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12629443969036839411ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__head_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1332647838480792820ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11173773172533827310ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__k_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12093304279906246746ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2717967157915040309ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4980133071604938604ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11096814991606221129ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3269200680789746220ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12027815949538146454ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3615504271328366956ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4634665586684019865ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(35, __VscopeHash, 10976639310650825191ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(35, __VscopeHash, 10649169425101554215ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16691157094744019854ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6286256010575566533ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7455455974700164328ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__src_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10336501290732538457ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4025442668914344096ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13969215966804201650ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11090286308325267186ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__start_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5625953510890711378ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__w0_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4339695183459897986ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__w1_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15975331888350816562ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13828960022502513405ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__w3_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14312310035075443976ull);
    vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15614663740858063513ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[__Vi0] = VL_SCOPED_RAND_RESET_Q(35, __VscopeHash, 16482040604742688955ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[__Vi0] = VL_SCOPED_RAND_RESET_Q(35, __VscopeHash, 10151428568697501426ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1127638196147774161ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__ch_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 722125301163564296ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__last_ch_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3349682331637051489ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5552577415612404293ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__scan_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3299522396379014871ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__scan_c_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8720710960250760534ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 677539455160493796ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4554514672781536762ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__best_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11209369294110685380ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__w0_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5008294188952943226ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__left_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16180805412075191693ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__widx_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 17148628700231335710ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__pw_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2969573914099790421ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__lane_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15305634479848706568ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6879076250634485382ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__err_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13347572243705193094ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__pend_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3914719364871409306ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__scan_rd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17084134606145696771ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11068220525058420678ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1023529337464049920ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__len_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9506661498239374167ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__rec_words_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4874946186391837389ull);
    vlSelf->__PVT__KL_mbx__DOT__u_tx__DOT__w0_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13631724209536879046ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3669195894933071295ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2495188972902612377ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16885710492529445843ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__lane_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12534504919222800848ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__widx_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12513365964029326802ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__dst_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7875055291072268366ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__b12_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4066875320604931355ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__b13_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1446417983805352511ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__sub_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8684857073921004920ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 62863078523314649ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__hit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14647953710022923820ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__mis_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13370260261938043795ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5469411378125715607ull);
    vlSelf->KL_mbx__DOT__u_rx__DOT__ch_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7820865431595960082ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16654752847382597100ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__if_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4470159334602712952ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__arrival_ms_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18260852587976098989ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12941999306275040058ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17923022034407818775ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1877184030933187611ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14594230279576997000ull);
    for (int __Vi0 = 0; __Vi0 < 15; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__field_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9585222851775575593ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1260470278388054902ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3198111074955578539ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14118745290177514406ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15815725823253928252ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1294553670409269761ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__head_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11747474583743529364ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12496716602345599040ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__held_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 135560718344496110ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13068891144097385267ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 479419843053327904ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14436175883061012759ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13317022992090627359ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16112397297213699603ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11092813792328035572ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__take_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12606908080496480606ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17299425894564047698ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__en_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12837852282769500714ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15310531031827913046ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16792131192056111739ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__owed_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6132821189645819646ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9728359160237403192ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1034076652775803246ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3042249869960801856ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__match_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15387753382210600714ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__hk_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1172873789233924374ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7780014433877405876ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6944968696003528330ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__hrd_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3340869399005491782ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5357257670971153455ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__hrhi_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13429841910888994206ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rb_mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17933289523417260928ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14833814367821304712ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14290148686002247609ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14001070880435276292ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14767438199914100945ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12791847683617120705ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__live_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4148872806024682503ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__eq_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16475724456587174417ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18330262032049244690ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cls_at_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10101605568606380423ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8419964935082703463ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1252169982239226572ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6689860720436563259ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9655675205384193511ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__free_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4553553024543776786ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 12198380817820336272ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14424913519423972838ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__drain_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3805888278027897152ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__drain_fits_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16200709107046604439ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__waddr_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 5170374768867671301ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12602589399435792745ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 276882874595513432ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__bad_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9869160519499962035ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vd_drop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8741340737877350724ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vd_rate_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17914609264761528780ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vd_acc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10196025384528231704ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__vd_mis_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 225224896078536843ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7667676846015950085ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12123505306506980151ull);
    vlSelf->KL_mbx__DOT__u_rx__DOT__commit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1204809086330087150ull);
    vlSelf->KL_mbx__DOT__u_rx__DOT__hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16510623306909360305ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17471662681379904176ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__rate_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14033618485624773517ull);
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__mis_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14049757618960719592ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7415189219337247028ull);
    }
    vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__word_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10495246161628267713ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16997820290204918155ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->KL_mbx__DOT__u_rx__DOT__rel_w[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9305005812554036311ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2207293164314519950ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15191235658064105018ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1985133815756765411ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9019051506578854630ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 340585604310045410ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 426734485116101979ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 398934730112773517ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4361868535521937812ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5372642729801291152ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3140910378737906071ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4735231230108015466ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8316321623172039472ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7877429316265855670ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7195229599854458710ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9708556904145465947ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10149986376063681372ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1024; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_srp_rx__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11893146807546414439ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->__PVT__KL_mbx__DOT__u_evt_ring__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9289936823784447233ull);
    }
    vlSelf->__PVT__KL_mbx_wb__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11369158497165140597ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__state_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5255273591627792455ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__base_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 15040986498739159332ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__mask_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 675346370550676213ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9385033787830243549ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__word_addr_r = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 14909013640028537141ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__left_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 12664191128942260869ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__tail_be_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 270949451417621041ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__chunk_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15080788674745204850ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__count_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6011625021183255680ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2684829446476550675ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__rerr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18281189363540229758ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__hold_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8863413573806832545ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__hold_wdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11549754416536351930ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__hold_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12667824275018007895ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__KL_mbx_dma__DOT__buf_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7669497552749226651ull);
    }
    vlSelf->__PVT__KL_mbx_dma__DOT__pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11316109739198519199ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__pend_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17868699731055966911ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__pend_addr_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 14215263471338122964ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__pend_wdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16114523758364329289ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__pend_be_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12694985452346428774ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__cpu_wait_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11133935376738383150ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__last_chunk_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1124120721584186093ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__left_next_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 17344733126136069681ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__word_addr_next_w = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 7801152740977125917ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__ring_addr_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 8437062098300523723ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__ring_addr_next_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 3840549333327578588ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__fill_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4226178205592522578ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__beat_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9017546664350647793ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__ring_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7139494956062949990ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__last_word_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9533726646866280382ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__beat_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18387259579441046051ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__mover_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13823944721873691045ull);
    vlSelf->__PVT__KL_mbx_dma__DOT__chunk_end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12013236233190642722ull);
    vlSelf->__Vfunc_mbx_place_f__161__value = 0;
    vlSelf->__Vfunc_mbx_place_f__176__value = 0;
    vlSelf->__Vfunc_mbx_place_f__199__value = 0;
    vlSelf->__Vfunc_mbx_place_f__236__value = 0;
    vlSelf->__Vfunc_mbx_place_f__237__value = 0;
    vlSelf->__Vfunc_mbx_place_f__238__Vfuncout = 0;
    vlSelf->__Vfunc_mbx_place_f__238__value = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_0 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_101 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_107 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_108 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_109 = 0;
    vlSelf->__Vdly__add_devices_tx_pipe_valid_source_valid = 0;
    vlSelf->__Vdly__add_devices_rx_pipe_valid_source_valid = 0;
    vlSelf->__Vdly__soc_tx_fifo_level0 = 0;
    vlSelf->__Vdly__ctrlmemory1_sram2_bus_ack = 0;
    vlSelf->__Vdly__soc_tx_fifo_consume = 0;
    vlSelf->__Vdly__ctrlmemory0_sram1_bus_ack = 0;
    vlSelf->__Vdly__add_devices_stimulusmailbox_waited1 = 0;
    vlSelf->__Vdly__ctrlmemory1_sram3_bus_ack = 0;
    vlSelf->__Vdly__ctrlmemory1_sram4_bus_ack = 0;
    vlSelf->__Vdly__soc_rx_fifo_consume = 0;
    vlSelf->__Vdly__value = 0;
    vlSelf->__Vdly__soc_rx_fifo_level0 = 0;
    vlSelf->__Vdly__add_devices_stimulusmailbox_ms_cnt = 0;
    vlSelf->__Vdly__soc_bus_errors = 0;
    vlSelf->__Vdly__ctrlmemory0_sram0_bus_ack = 0;
    vlSelf->__Vdly__add_devices_stimulusmailbox_waited0 = 0;
    vlSelf->__Vdly__KL_mbx__DOT__now_ms_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__fw_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__ctr_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__amap_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__edit_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__gsi_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__bus_err_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__scan_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__head_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__seq_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__k_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__ch_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r = 0;
}

VL_ATTR_COLD void Vsim_sim___ctor_var_reset_1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ctor_var_reset_1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__scan_c_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__best_ch_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__best_seq_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__left_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__cp_k_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__match_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__dst_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__q_rd_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__q_wr_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__q_cnt_r = 0;
    vlSelf->__Vdly__KL_mbx__DOT__u_rx__DOT__mismatch_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__state_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__index_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__chunk_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__count_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__rerr_r = 0;
    vlSelf->__Vdly__KL_mbx_dma__DOT__pend_r = 0;
    vlSelf->__VdlyVal__storage_1__v0 = 0;
    vlSelf->__VdlyDim0__storage_1__v0 = 0;
    vlSelf->__VdlySet__storage_1__v0 = 0;
    vlSelf->__VdlyVal__storage_2__v0 = 0;
    vlSelf->__VdlyDim0__storage_2__v0 = 0;
    vlSelf->__VdlySet__storage_2__v0 = 0;
    vlSelf->__VdlyVal__sram_bank0__v0 = 0;
    vlSelf->__VdlyDim0__sram_bank0__v0 = 0;
    vlSelf->__VdlySet__sram_bank0__v0 = 0;
    vlSelf->__VdlyVal__sram_bank0__v1 = 0;
    vlSelf->__VdlyDim0__sram_bank0__v1 = 0;
    vlSelf->__VdlySet__sram_bank0__v1 = 0;
    vlSelf->__VdlyVal__sram_bank0__v2 = 0;
    vlSelf->__VdlyDim0__sram_bank0__v2 = 0;
    vlSelf->__VdlySet__sram_bank0__v2 = 0;
    vlSelf->__VdlyVal__sram_bank0__v3 = 0;
    vlSelf->__VdlyDim0__sram_bank0__v3 = 0;
    vlSelf->__VdlySet__sram_bank0__v3 = 0;
    vlSelf->__VdlyVal__sram_bank1__v0 = 0;
    vlSelf->__VdlyDim0__sram_bank1__v0 = 0;
    vlSelf->__VdlySet__sram_bank1__v0 = 0;
    vlSelf->__VdlyVal__sram_bank1__v1 = 0;
    vlSelf->__VdlyDim0__sram_bank1__v1 = 0;
    vlSelf->__VdlySet__sram_bank1__v1 = 0;
    vlSelf->__VdlyVal__sram_bank1__v2 = 0;
    vlSelf->__VdlyDim0__sram_bank1__v2 = 0;
    vlSelf->__VdlySet__sram_bank1__v2 = 0;
    vlSelf->__VdlyVal__sram_bank1__v3 = 0;
    vlSelf->__VdlyDim0__sram_bank1__v3 = 0;
    vlSelf->__VdlySet__sram_bank1__v3 = 0;
    vlSelf->__VdlyVal__sram_bank2__v0 = 0;
    vlSelf->__VdlyDim0__sram_bank2__v0 = 0;
    vlSelf->__VdlySet__sram_bank2__v0 = 0;
    vlSelf->__VdlyVal__sram_bank2__v1 = 0;
    vlSelf->__VdlyDim0__sram_bank2__v1 = 0;
    vlSelf->__VdlySet__sram_bank2__v1 = 0;
    vlSelf->__VdlyVal__sram_bank2__v2 = 0;
    vlSelf->__VdlyDim0__sram_bank2__v2 = 0;
    vlSelf->__VdlySet__sram_bank2__v2 = 0;
    vlSelf->__VdlyVal__sram_bank2__v3 = 0;
    vlSelf->__VdlyDim0__sram_bank2__v3 = 0;
    vlSelf->__VdlySet__sram_bank2__v3 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_entity_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_entity_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_entity_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_entity_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_req_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_gsi_req_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_gsi_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_value_hi_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_value_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_value_lo_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_value_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_src_valid_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_src_valid_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_src_valid_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_ctrl_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_ctrl_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_record_lo_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_record_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_restore_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_restore_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_restore_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_restore_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_beat_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_beat_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_beat_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_beat_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_clock_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_clock_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_clock_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_clock_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_pt_offset_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_pt_offset_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_pt_offset_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_amap_req_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_amap_req_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_amap_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_amap_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_gsi_prop_lo_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_gsi_prop_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_req_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_req_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_aecp_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_aecp_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_aecp_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_aecp_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_nvm_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_nvm_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_nvm_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_nvm_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_edit_record_hi_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_edit_record_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_gsi_sel_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_gsi_sel_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_ctr_req_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_ctr_req_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_ctr_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_ctr_req_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_gsi_prop_hi_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_gsi_prop_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_ctr_word_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_ctr_word_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_ctr_word_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_ctr_word_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_amap_page_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_amap_page_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_amap_page_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_amap_page_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__face_f_snk_valid_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__face_f_snk_valid_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__face_f_snk_valid_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__ctr_tag_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__ctr_wait_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__ctr_wait_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__ctr_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__ctr_tag_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__ctr_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__ctr_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__ctr_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__ctr_data_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__amap_tag_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__amap_wait_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__amap_wait_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__amap_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__amap_tag_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__amap_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__amap_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__amap_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__amap_data_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__edit_tag_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__edit_data_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__edit_wait_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__edit_wait_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__edit_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__edit_tag_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__edit_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__edit_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__edit_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gsi_tag_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__gsi_wait_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gsi_wait_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__gsi_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__gsi_tag_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gsi_tag_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__gsi_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gsi_wait_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gsi_data_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__tx_head_r__v5 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__tx_head_r__v6 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__tx_head_r__v7 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__tx_head_r__v8 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v8 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__tx_head_r__v9 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__tx_head_r__v9 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__rx_tail_r__v5 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__rx_tail_r__v6 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__rx_tail_r__v7 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__rx_tail_r__v8 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v8 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__rx_tail_r__v9 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__rx_tail_r__v9 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__gm_hi_snap_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__domain_snap_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__domain_snap_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__domain_snap_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__own_mac_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__own_mac_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__own_mac_lo_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__own_mac_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__own_mac_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__own_mac_hi_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_talker_decl_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_talker_decl_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_sr_domain_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_sr_domain_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_idle_slope_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_idle_slope_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_da_gate_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_da_gate_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_da_gate_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_da_gate_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_licence_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_licence_r__v1 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_licence_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_licence_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_sid_lo_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_sid_lo_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__pub_sid_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_sid_hi_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_sid_hi_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__pub_sid_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_binding_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__pub_binding_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__pub_binding_r__v16 = 0;
    vlSelf->__VdlyDim1__KL_mbx__DOT__pub_binding_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__pub_binding_r__v16 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__tag_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_evt__DOT__tag_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__dl_r__v16 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_evt__DOT__dl_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v16 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_seen_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_pend_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v4 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v7 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v5 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v5 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v6 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v6 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_tx__DOT__err_r__v5 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_tx__DOT__err_r__v5 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_tx__DOT__err_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 = 0;
    vlSelf->__VdlyDim0__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v1 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v2 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v3 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v4 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v5 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v6 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v7 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0 = 0;
    vlSelf->__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v1 = 0;
}
