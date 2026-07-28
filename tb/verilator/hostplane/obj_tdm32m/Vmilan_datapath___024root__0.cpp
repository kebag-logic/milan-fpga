// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___eval_triggers_vec__ico(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_triggers_vec__ico\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = (((QData)((IData)(
                                                      (((((IData)(vlSelfRef.pb_mem_valid_i) 
                                                          != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__pb_mem_valid_i__0)) 
                                                         << 0x00000014U) 
                                                        | (((((vlSelfRef.pb_mem_data_i 
                                                               != vlSelfRef.__Vtrigprevexpr___TOP__pb_mem_data_i__0) 
                                                              << 3U) 
                                                             | ((0U 
                                                                 != 
                                                                 ((((((((vlSelfRef.pb_wr_ptr_i[0U] 
                                                                         ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[0U]) 
                                                                        | (vlSelfRef.pb_wr_ptr_i[1U] 
                                                                           ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[1U])) 
                                                                       | (vlSelfRef.pb_wr_ptr_i[2U] 
                                                                          ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[2U])) 
                                                                      | (vlSelfRef.pb_wr_ptr_i[3U] 
                                                                         ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[3U])) 
                                                                     | (vlSelfRef.pb_wr_ptr_i[4U] 
                                                                        ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[4U])) 
                                                                    | (vlSelfRef.pb_wr_ptr_i[5U] 
                                                                       ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[5U])) 
                                                                   | (vlSelfRef.pb_wr_ptr_i[6U] 
                                                                      ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[6U])) 
                                                                  | (vlSelfRef.pb_wr_ptr_i[7U] 
                                                                     ^ vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[7U]))) 
                                                                << 2U)) 
                                                            | (((vlSelfRef.pb_ring_stride_i 
                                                                 != vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_stride_i__0) 
                                                                << 1U) 
                                                               | (vlSelfRef.pb_ring_len_i 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_len_i__0))) 
                                                           << 0x00000010U)) 
                                                       | (((((((vlSelfRef.pb_ring_base_i 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_base_i__0) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.pb_stream_en_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__pb_stream_en_i__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.pb_underrun_silence_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__pb_underrun_silence_i__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.pb_enable_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__pb_enable_i__0)))) 
                                                            << 0x0000000cU) 
                                                           | ((((((IData)(vlSelfRef.i_mmcm_ps_done) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_ps_done__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.i_mmcm_locked) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_locked__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.i_mmcm_drp_rdy) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_rdy__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.i_mmcm_drp_do) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_do__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.i_ps_clk) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.i_mac_events_cap) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events_cap__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.i_mac_events) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.i_ethact_tgl) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethact_tgl__0)))) 
                                                              << 4U) 
                                                             | (((((IData)(vlSelfRef.i_ethtx_tgl) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethtx_tgl__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.i_ethrx_tgl) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethrx_tgl__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.i_full_duplex) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_full_duplex__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.i_link_up) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_link_up__0))))))))) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(
                                                       ((((((((((IData)(vlSelfRef.i_mac_speed) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_speed__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tlast__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.s_axis_mac_rx_tvalid) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tvalid__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.s_axis_mac_rx_tkeep) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tkeep__0)))) 
                                                            << 0x0000000cU) 
                                                           | (((((vlSelfRef.s_axis_mac_rx_tdata 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tdata__0) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.m_axis_mac_tx_tready) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_mac_tx_tready__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.m_axis_pcm_tready) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_pcm_tready__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.m_axis_ts_tready) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_ts_tready__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.m_axis_rx_tready) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_rx_tready__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.s_axis_tx_tlast) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tlast__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.s_axis_tx_tvalid) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.s_axis_tx_tkeep) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0)))) 
                                                              << 4U) 
                                                             | ((((vlSelfRef.s_axis_tx_tdata 
                                                                   != vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tdata__0) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.tdm_data_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_data_i__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.tdm_fsync_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_fsync_i__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.tdm_bclk_i) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__0)))))) 
                                                         << 0x00000010U) 
                                                        | ((((((((IData)(vlSelfRef.i2s_sdout_i) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i2s_sdout_i__0)) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.s_axi_rready) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_rready__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.s_axi_arvalid) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_arvalid__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.s_axi_araddr) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_araddr__0)))) 
                                                             << 0x0000000cU) 
                                                            | ((((((IData)(vlSelfRef.s_axi_bready) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_bready__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.s_axi_wvalid) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wvalid__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.s_axi_wstrb) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wstrb__0)) 
                                                                    << 1U) 
                                                                   | (vlSelfRef.s_axi_wdata 
                                                                      != vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wdata__0))) 
                                                               << 8U)) 
                                                           | (((((((IData)(vlSelfRef.s_axi_awvalid) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awvalid__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awaddr__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.gtx_resetn) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_resetn__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.gtx_clk) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__0)))) 
                                                               << 4U) 
                                                              | (((((IData)(vlSelfRef.axis_resetn) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__0)) 
                                                                   << 3U) 
                                                                  | (((IData)(vlSelfRef.clk_tdm_i) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_tdm_i__0)) 
                                                                     << 2U)) 
                                                                 | ((((IData)(vlSelfRef.clk_audio_i) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__0)) 
                                                                     << 1U) 
                                                                    | ((IData)(vlSelfRef.axis_clk) 
                                                                       != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__0))))))))));
    vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__0 = vlSelfRef.axis_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__0 
        = vlSelfRef.clk_audio_i;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_tdm_i__0 = vlSelfRef.clk_tdm_i;
    vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__0 
        = vlSelfRef.axis_resetn;
    vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__0 = vlSelfRef.gtx_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__gtx_resetn__0 
        = vlSelfRef.gtx_resetn;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awaddr__0 
        = vlSelfRef.s_axi_awaddr;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awvalid__0 
        = vlSelfRef.s_axi_awvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wdata__0 
        = vlSelfRef.s_axi_wdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wstrb__0 
        = vlSelfRef.s_axi_wstrb;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wvalid__0 
        = vlSelfRef.s_axi_wvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_bready__0 
        = vlSelfRef.s_axi_bready;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_araddr__0 
        = vlSelfRef.s_axi_araddr;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_arvalid__0 
        = vlSelfRef.s_axi_arvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axi_rready__0 
        = vlSelfRef.s_axi_rready;
    vlSelfRef.__Vtrigprevexpr___TOP__i2s_sdout_i__0 
        = vlSelfRef.i2s_sdout_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__0 
        = vlSelfRef.tdm_bclk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_fsync_i__0 
        = vlSelfRef.tdm_fsync_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_data_i__0 
        = vlSelfRef.tdm_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tdata__0 
        = vlSelfRef.s_axis_tx_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0 
        = vlSelfRef.s_axis_tx_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0 
        = vlSelfRef.s_axis_tx_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_tx_tlast__0 
        = vlSelfRef.s_axis_tx_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_rx_tready__0 
        = vlSelfRef.m_axis_rx_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_ts_tready__0 
        = vlSelfRef.m_axis_ts_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_pcm_tready__0 
        = vlSelfRef.m_axis_pcm_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__m_axis_mac_tx_tready__0 
        = vlSelfRef.m_axis_mac_tx_tready;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tdata__0 
        = vlSelfRef.s_axis_mac_rx_tdata;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tkeep__0 
        = vlSelfRef.s_axis_mac_rx_tkeep;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tvalid__0 
        = vlSelfRef.s_axis_mac_rx_tvalid;
    vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tlast__0 
        = vlSelfRef.s_axis_mac_rx_tlast;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mac_speed__0 
        = vlSelfRef.i_mac_speed;
    vlSelfRef.__Vtrigprevexpr___TOP__i_link_up__0 = vlSelfRef.i_link_up;
    vlSelfRef.__Vtrigprevexpr___TOP__i_full_duplex__0 
        = vlSelfRef.i_full_duplex;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ethrx_tgl__0 
        = vlSelfRef.i_ethrx_tgl;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ethtx_tgl__0 
        = vlSelfRef.i_ethtx_tgl;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ethact_tgl__0 
        = vlSelfRef.i_ethact_tgl;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events__0 
        = vlSelfRef.i_mac_events;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events_cap__0 
        = vlSelfRef.i_mac_events_cap;
    vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__0 = vlSelfRef.i_ps_clk;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_do__0 
        = vlSelfRef.i_mmcm_drp_do;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_rdy__0 
        = vlSelfRef.i_mmcm_drp_rdy;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_locked__0 
        = vlSelfRef.i_mmcm_locked;
    vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_ps_done__0 
        = vlSelfRef.i_mmcm_ps_done;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_enable_i__0 
        = vlSelfRef.pb_enable_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_underrun_silence_i__0 
        = vlSelfRef.pb_underrun_silence_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_stream_en_i__0 
        = vlSelfRef.pb_stream_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_base_i__0 
        = vlSelfRef.pb_ring_base_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_len_i__0 
        = vlSelfRef.pb_ring_len_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_ring_stride_i__0 
        = vlSelfRef.pb_ring_stride_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[0U] 
        = vlSelfRef.pb_wr_ptr_i[0U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[1U] 
        = vlSelfRef.pb_wr_ptr_i[1U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[2U] 
        = vlSelfRef.pb_wr_ptr_i[2U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[3U] 
        = vlSelfRef.pb_wr_ptr_i[3U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[4U] 
        = vlSelfRef.pb_wr_ptr_i[4U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[5U] 
        = vlSelfRef.pb_wr_ptr_i[5U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[6U] 
        = vlSelfRef.pb_wr_ptr_i[6U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_wr_ptr_i__0[7U] 
        = vlSelfRef.pb_wr_ptr_i[7U];
    vlSelfRef.__Vtrigprevexpr___TOP__pb_mem_data_i__0 
        = vlSelfRef.pb_mem_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__pb_mem_valid_i__0 
        = vlSelfRef.pb_mem_valid_i;
    if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VicoDidInit)))))) {
        vlSelfRef.__VicoDidInit = 1U;
        vlSelfRef.__VicoTriggered[0U] = (1ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (2ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (4ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (8ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000010ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000020ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000040ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000080ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000100ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000200ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000400ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000800ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000001000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000002000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000004000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000008000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000010000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000020000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000040000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000080000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000100000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000200000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000400000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000800000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000001000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000002000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000004000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000008000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000010000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000020000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000040000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000080000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000100000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000200000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000400000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000800000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000001000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000002000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000004000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000008000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000010000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000020000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000040000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000080000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000100000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000200000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000400000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000800000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0001000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0002000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0004000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0008000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0010000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
    }
}

bool Vmilan_datapath___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

void Vmilan_datapath___024root___ico_sequent__TOP__0(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit;
    milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit = 0;
    // Body
    vlSelfRef.m_axis_rx_tdata = vlSelfRef.s_axis_mac_rx_tdata;
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
        = (((QData)((IData)(((((0x0000ff00U & ((IData)(vlSelfRef.s_axis_mac_rx_tdata) 
                                               << 8U)) 
                               | (0x000000ffU & (IData)(
                                                        (vlSelfRef.s_axis_mac_rx_tdata 
                                                         >> 8U)))) 
                              << 0x00000010U) | ((0x0000ff00U 
                                                  & ((IData)(
                                                             (vlSelfRef.s_axis_mac_rx_tdata 
                                                              >> 0x00000010U)) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & (IData)(
                                                              (vlSelfRef.s_axis_mac_rx_tdata 
                                                               >> 0x00000018U))))))) 
            << 0x00000010U) | (QData)((IData)(((0x0000ff00U 
                                                & ((IData)(
                                                           (vlSelfRef.s_axis_mac_rx_tdata 
                                                            >> 0x00000020U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 0x00000028U)))))));
    milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit 
        = (((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[15U] 
                 & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[15U] 
                             & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[15U] 
                                ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[14U] 
                           & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[14U] 
                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[14U] 
                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                          << 2U)) | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[13U] 
                                       & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[13U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[13U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                      << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[12U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[12U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[12U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
             << 0x0000000cU) | (((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[11U] 
                                    & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[11U] 
                                                & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[11U] 
                                                   ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                   << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[10U] 
                                              & (0ULL 
                                                 == 
                                                 (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[10U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[10U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                             << 2U)) 
                                 | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[9U] 
                                      & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[9U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[9U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                     << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[8U] 
                                               & (0ULL 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[8U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[8U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
                                << 8U)) | ((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[7U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[7U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[7U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                               << 3U) 
                                              | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[6U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[6U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[6U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                 << 2U)) 
                                             | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[5U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[5U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[5U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                 << 1U) 
                                                | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[4U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[4U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[4U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
                                            << 4U) 
                                           | ((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[3U] 
                                                 & (0ULL 
                                                    == 
                                                    (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[3U] 
                                                     & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[3U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                << 3U) 
                                               | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[2U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[2U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[2U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                  << 2U)) 
                                              | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[1U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[1U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[1U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                  << 1U) 
                                                 | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[0U] 
                                                    & (0ULL 
                                                       == 
                                                       (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[0U] 
                                                        & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[0U] 
                                                           ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac))))))));
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 0U;
    if ((0x00008000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00004000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00002000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00001000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000800U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000400U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000200U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000100U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000080U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000040U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000020U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000010U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((8U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((4U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((2U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = 0U;
    if ((0x00008000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[15U];
    }
    if ((0x00004000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[14U];
    }
    if ((0x00002000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[13U];
    }
    if ((0x00001000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[12U];
    }
    if ((0x00000800U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[11U];
    }
    if ((0x00000400U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[10U];
    }
    if ((0x00000200U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[9U];
    }
    if ((0x00000100U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[8U];
    }
    if ((0x00000080U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[7U];
    }
    if ((0x00000040U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[6U];
    }
    if ((0x00000020U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[5U];
    }
    if ((0x00000010U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[4U];
    }
    if ((8U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[3U];
    }
    if ((4U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[2U];
    }
    if ((2U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[1U];
    }
    if ((1U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[0U];
    }
}

void Vmilan_datapath___024root___ico_sequent__TOP__5(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__5\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__chan_map_render__DOT__avb_ok_w;
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc 
        = ((IData)(vlSelfRef.m_axis_pcm_tready) & (IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w));
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w 
        = (1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w)) 
                 | (IData)(vlSelfRef.m_axis_pcm_tready)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w 
        = (((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
             ? (IData)(vlSelfRef.milan_datapath__DOT__chmap_phys_v_w)
             : (IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w)) 
           & ((IData)(vlSelfRef.m_axis_pcm_tready) 
              | vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl));
    vlSelfRef.milan_datapath__DOT__i2s_feed_mux__DOT__feed_p_w 
        = ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
            ? (IData)(vlSelfRef.milan_datapath__DOT__chmap_phys_v_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
              | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w)))));
    vlSelfRef.milan_datapath__DOT__dpkt_acc_w = ((IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_lpf_act_w)))) {
        if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w))) {
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w 
                    = ((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w)) 
                       << 0x00000018U);
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__i2s_feed_lpf_act_w) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
            = (((QData)((IData)(((((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                             >> 8U)))) 
                                  << 0x00000010U) | 
                                 ((0x0000ff00U & ((IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                           >> 0x00000010U)) 
                                                  << 8U)) 
                                  | (0x000000ffU & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                            >> 0x00000020U))))))) 
                << 0x00000010U) | (QData)((IData)((
                                                   (0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                                >> 0x00000028U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                                 >> 0x00000030U)))))));
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w 
            = vlSelfRef.milan_datapath__DOT__pcm_lpf_tvalid;
    } else if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = ((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)) 
                   << 0x00000018U);
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w)));
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)));
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe));
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w 
        = ((8U > (IData)(vlSelfRef.m_axis_pcm_tuser)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_acc_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w) 
           & (1U <= (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w) 
              >= ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w)
                   ? 2U : 1U)));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wr_n_w 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w) 
                 + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w)) 
            & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w)) 
           | ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w)));
}

void Vmilan_datapath___024root___ico_sequent__TOP__9(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__9\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__ctlf_tx_tready;
    milan_datapath__DOT__ctlf_tx_tready = 0;
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
           & (IData)(vlSelfRef.m_axis_mac_tx_tvalid));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tready = 
        ((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
            & ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
               & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel))));
    vlSelfRef.milan_datapath__DOT__dpcrf_tready = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
                                                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)) 
                                                      & (IData)(vlSelfRef.m_axis_mac_tx_tready)));
    vlSelfRef.milan_datapath__DOT__tx_mac_good_w = 
        ((IData)(vlSelfRef.m_axis_mac_tx_tlast) & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted));
    vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tready));
    vlSelfRef.milan_datapath__DOT__ctlg_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__active) 
         & ((~ (IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__gsel)) 
            & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tready)));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready));
    vlSelfRef.milan_datapath__DOT__dpaaf_tready = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active) 
                                                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)) 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready)));
    vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tready));
    milan_datapath__DOT__ctlf_tx_tready = ((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__active) 
                                           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel)) 
                                              & (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tready)));
    vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tready));
    vlSelfRef.milan_datapath__DOT__aaf_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__active) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel) 
            & (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tready)));
    vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctlf_tx_tvalid) 
           & (IData)(milan_datapath__DOT__ctlf_tx_tready));
    vlSelfRef.milan_datapath__DOT__lwsrp_tx_tready 
        = ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__active) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel) 
              & (IData)(milan_datapath__DOT__ctlf_tx_tready)));
    vlSelfRef.milan_datapath__DOT__ctl_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__active) 
         & ((~ (IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel)) 
            & (IData)(milan_datapath__DOT__ctlf_tx_tready)));
    vlSelfRef.milan_datapath__DOT__aaf_tx_acc_w = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tready));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tready));
    vlSelfRef.milan_datapath__DOT__ctl2_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel) 
            & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tready)));
    vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__tx_mac_good_w) 
             << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_acc_w) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)) 
                       << 2U)) | ((((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_inframe_r)) 
                                    & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_acc_w)) 
                                   << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)));
    vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tready));
    vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w = 0U;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 1U;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
        vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
    } else {
        milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w = 0U;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 1U;
    if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r)) 
         & (IData)(milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
}

void Vmilan_datapath___024root___ico_sequent__TOP__10(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__10\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe 
        = (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant) 
            >> 4U) & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe 
        = (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant) 
            >> 3U) & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe 
        = (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant) 
            >> 2U) & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe 
        = (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant) 
            >> 1U) & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe 
        = ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant) 
           & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__beat_acc 
        = ((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid) 
           & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw 
        = ((0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw)) 
           | ((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue))) 
               & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
              & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[0U] 
        = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw))
            ? (0x0000ffffU & VL_COUNTONES_I((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep)))
            : 0U);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw 
        = ((0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw)) 
           | (((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant) 
                 & (1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue))) 
                & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
               & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready)) 
              << 1U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[1U] 
        = ((2U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw))
            ? (0x0000ffffU & VL_COUNTONES_I((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep)))
            : 0U);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw 
        = ((0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw)) 
           | (((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant) 
                 & (2U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue))) 
                & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
               & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready)) 
              << 2U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[2U] 
        = ((4U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw))
            ? (0x0000ffffU & VL_COUNTONES_I((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep)))
            : 0U);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw 
        = ((0x17U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw)) 
           | (((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant) 
                 & (3U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue))) 
                & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
               & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready)) 
              << 3U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[3U] 
        = ((8U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw))
            ? (0x0000ffffU & VL_COUNTONES_I((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep)))
            : 0U);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw 
        = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw)) 
           | (((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant) 
                 & (4U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue))) 
                & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
               & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tready)) 
              << 4U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[4U] 
        = ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__is_transmitting_raw))
            ? (0x0000ffffU & VL_COUNTONES_I((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep)))
            : 0U);
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push 
        = (((((((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__beat_acc) 
                & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tlast)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl)));
}

void Vmilan_datapath___024root___ico_sequent__TOP__11(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__11\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ __Vfunc_reorder_endian_func__16__Vfuncout;
    __Vfunc_reorder_endian_func__16__Vfuncout = 0;
    QData/*63:0*/ __Vfunc_reorder_endian_func__16__data_in;
    __Vfunc_reorder_endian_func__16__data_in = 0;
    IData/*31:0*/ __Vfunc_reorder_endian_func__16__width;
    __Vfunc_reorder_endian_func__16__width = 0;
    IData/*31:0*/ __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i;
    __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i = 0;
    QData/*63:0*/ __Vfunc_reorder_endian_func__16__data_out;
    __Vfunc_reorder_endian_func__16__data_out = 0;
    CData/*4:0*/ __VdfgRegularize_h6e95ff9d_0_91;
    __VdfgRegularize_h6e95ff9d_0_91 = 0;
    // Body
    __Vfunc_reorder_endian_func__16__width = 0x00000040U;
    __Vfunc_reorder_endian_func__16__data_in = vlSelfRef.s_axis_tx_tdata;
    __Vfunc_reorder_endian_func__16__data_out = 0;
    __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i = 0U;
    while (VL_LTS_III(32, __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i, 
                      VL_DIVS_III(32, __Vfunc_reorder_endian_func__16__width, (IData)(8U)))) {
        __Vfunc_reorder_endian_func__16__data_out = 
            (((~ (0x00000000000000ffULL << (0x0000003fU 
                                            & VL_MULS_III(32, (IData)(8U), __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i)))) 
              & __Vfunc_reorder_endian_func__16__data_out) 
             | ((QData)((IData)((0x000000ffU & (IData)(
                                                       (__Vfunc_reorder_endian_func__16__data_in 
                                                        >> 
                                                        (0x0000003fU 
                                                         & (__Vfunc_reorder_endian_func__16__width 
                                                            - 
                                                            VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(1U) 
                                                                         + __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i))))))))) 
                << (0x0000003fU & VL_MULS_III(32, (IData)(8U), __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i))));
        __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i 
            = ((IData)(1U) + __Vfunc_reorder_endian_func__16__unnamedblk1__DOT__i);
    }
    __Vfunc_reorder_endian_func__16__Vfuncout = __Vfunc_reorder_endian_func__16__data_out;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be 
        = __Vfunc_reorder_endian_func__16__Vfuncout;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[0U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[1U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[2U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[0U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[3U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[1U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[4U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[2U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[5U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[3U];
    if ((0x12U <= (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter))) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[0U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[2U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[3U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[3U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[4U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[5U];
    } else {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[0U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[2U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[3U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[3U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[4U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[5U];
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 = ((0x8100U 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
                                                   >> 0x00000010U))
                                                  ? 
                                                 (((QData)((IData)(
                                                                   (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
                                                                    >> 0x00000010U))) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U])))
                                                  : 
                                                 ((QData)((IData)(
                                                                  (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
                                                                   >> 0x00000010U))) 
                                                  << 0x00000020U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame 
        = (IData)(((0x000088f700000000ULL == (0x0000ffff00000000ULL 
                                              & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16)) 
                   & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_ctrl 
                          >> 1U)) | (0x00000180c200000eULL 
                                     == (0x0000ffffffffffffULL 
                                         & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U])) 
                                             << 0x00000010U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U])) 
                                               >> 0x00000010U)))))));
    __VdfgRegularize_h6e95ff9d_0_91 = (0x0000001fU 
                                       & ((IData)(3U) 
                                          * (7U & (
                                                   (0x8100U 
                                                    == 
                                                    (0x0000ffffU 
                                                     & (IData)(
                                                               (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 
                                                                >> 0x00000010U))))
                                                    ? (IData)(
                                                              (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 
                                                               >> 0x0000000dU))
                                                    : vlSelfRef.milan_datapath__DOT__csr__DOT__cls_dpcp))));
    if ((1U & (~ VL_ONEHOT_I((((IData)(((0x000022f000000000ULL 
                                         == (0x0000ffff00000000ULL 
                                             & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16)) 
                                        & (0x8100U 
                                           != (0x0000ffffU 
                                               & (IData)(
                                                         (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 
                                                          >> 0x00000010U)))))) 
                               << 2U) | (((IData)((0x000022f081000000ULL 
                                                   == 
                                                   (0x0000ffffffff0000ULL 
                                                    & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16))) 
                                          << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame))))))) {
        if ((0U != (((IData)(((0x000022f000000000ULL 
                               == (0x0000ffff00000000ULL 
                                   & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16)) 
                              & (0x8100U != (0x0000ffffU 
                                             & (IData)(
                                                       (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 
                                                        >> 0x00000010U)))))) 
                     << 2U) | (((IData)((0x000022f081000000ULL 
                                         == (0x0000ffffffff0000ULL 
                                             & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16))) 
                                << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame))))) {
            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                VL_WRITEF_NX("[%0t] %%Error: traffic_class_map.sv:229: Assertion failed in %m: unique case, but multiple matches found for '1'h1'\n",3, 'M',vlSymsp->name(),"milan_datapath.traffic_controller.classifier.class_map.classify", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee8021q/ts/traffic_class_map.sv", 229, "");
            }
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93 = (0x0000001fU 
                                                 & (((IData)(3U) 
                                                     * 
                                                     (7U 
                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_regen 
                                                         >> (IData)(__VdfgRegularize_h6e95ff9d_0_91)))) 
                                                    & (- (IData)(
                                                                 (0x17U 
                                                                  >= (IData)(__VdfgRegularize_h6e95ff9d_0_91))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92 = (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_tcq 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(3U) 
                                                         * 
                                                         (7U 
                                                          & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_map 
                                                             >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93)))) 
                                                        & (- (IData)(
                                                                     (0x17U 
                                                                      >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93))))))));
}

void Vmilan_datapath___024root___ico_comb__TOP__2(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_comb__TOP__2\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_79;
    __VdfgRegularize_h6e95ff9d_0_79 = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__csr__DOT__sel_wr_w 
        = ((0x0800U == (IData)(vlSelfRef.s_axi_awaddr)) 
           & (IData)(vlSelfRef.s_axi_awready));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmlo_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x081cU 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmhi_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x0820U 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)));
    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
        = ((IData)(vlSelfRef.s_axi_awready) & (~ (0U 
                                                  != 
                                                  (0x0000001fU 
                                                   & ((IData)(vlSelfRef.s_axi_awaddr) 
                                                      >> 0x0bU)))));
    if (vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a 
            = vlSelfRef.s_axi_awaddr;
        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 0U;
        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                        }
                                    } else if ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                    }
                                } else if (((0x0400U 
                                             <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                            & (0x04a0U 
                                               > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                                & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                            & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
            }
        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)) 
                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))) 
                     | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                    | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a)))) 
                   | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a))));
        }
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_axi_we 
        = vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    __VdfgRegularize_h6e95ff9d_0_79 = ((0x0810U == (IData)(vlSelfRef.s_axi_awaddr)) 
                                       & (IData)(vlSelfRef.s_axi_awready));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_ctrl_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_79) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20));
    vlSelfRef.milan_datapath__DOT__csr__DOT__srp_prov_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_79) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_poll_w));
}

void Vmilan_datapath___024root___ico_comb__TOP__5(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_comb__TOP__5\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__soff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__soff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__loff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__loff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__poff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__poff = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__soff 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                          - (IData)(0x0210U)));
    milan_datapath__DOT__csr__DOT__read_mux__DOT__loff 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                          - (IData)(0x0874U)));
    milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                          - (IData)(0x08b4U)));
    milan_datapath__DOT__csr__DOT__read_mux__DOT__poff 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                          - (IData)(0x08c8U)));
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_valid_r)
                                ? (0x04000000U | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r) 
                                                   << 0x0000001bU) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r) 
                                                      << 0x00000014U) 
                                                     | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r) 
                                                         << 0x00000013U) 
                                                        | (((IData)(
                                                                    (0x4000U 
                                                                     == 
                                                                     (0xc000U 
                                                                      & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r)))) 
                                                            << 0x00000012U) 
                                                           | ((0x00030000U 
                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r) 
                                                                  << 2U)) 
                                                              | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r)))))))
                                : 0xdeaddeadU);
                    }
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = (0xc5000300U | ((((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r) 
                                            << 0x00000016U) 
                                           | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r) 
                                              << 0x00000010U)) 
                                          | ((((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_armed_r) 
                                               << 4U) 
                                              | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_unsup_r) 
                                                  << 3U) 
                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_to_r) 
                                                    << 2U))) 
                                             | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_valid_r) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r)))));
                }
            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_refused) 
                                << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_commits));
                    }
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word);
                }
            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel;
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl;
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__csr__DOT__mcsrv_ctrl;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((VL_SHIFTRS_III(24,24,32, vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_cmd_r, 5U) 
                                        << 0x00000010U) 
                                       | ((((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_cnt_r) 
                                            << 0x0000000aU) 
                                           | ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_fault_r) 
                                              << 8U)) 
                                          | (((((2U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r)) 
                                                | (1U 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_send_r) 
                                                      | ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r) 
                                                         >> 1U)))) 
                                               << 6U) 
                                              | (((2U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__locked_sync_r)) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__mismatch_r)) 
                                                 << 4U)) 
                                             | (((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__verified_r) 
                                                 << 3U) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__state_r)))));
                            }
                        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r))) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r)) 
                                  << 0x0000000dU) | 
                                 ((IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r) 
                                  << 0x0000000cU)) 
                                | ((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r))) 
                                     & (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r)) 
                                    << 9U) | ((IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r) 
                                              << 8U))) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_en_r) 
                                  << 1U));
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_pend_r) 
                                            << 0x0000001fU) 
                                           | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_done_r) 
                                               << 0x0000001eU) 
                                              | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_stat_r) 
                                                  << 8U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_idx_r))));
                                }
                            } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0234U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__tu_ivals_r;
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                        if (((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (8U 
                                                    >= 
                                                    (0x0000000fU 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                        >> 2U)))
                                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                                   [
                                                   (0x0000000fU 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x0874U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08b4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                                [(0x0000000fU 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                     >> 2U))];
                                        } else if (
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (0x9fU 
                                                    >= 
                                                    (0x000000e0U 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                        << 3U)))
                                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                                   [
                                                   (7U 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (0x5fU 
                                                    >= 
                                                    (0x00000060U 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                        << 3U)))
                                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                                   [
                                                   (3U 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else if ((1U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                        if (((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (8U 
                                                    >= 
                                                    (0x0000000fU 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                        >> 2U)))
                                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                                   [
                                                   (0x0000000fU 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x0874U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08b4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                                [(0x0000000fU 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                     >> 2U))];
                                        } else if (
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (0x9fU 
                                                    >= 
                                                    (0x000000e0U 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                        << 3U)))
                                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                                   [
                                                   (7U 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                                = (
                                                   (0x5fU 
                                                    >= 
                                                    (0x00000060U 
                                                     & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                        << 3U)))
                                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                                   [
                                                   (3U 
                                                    & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                       >> 2U))]
                                                    : 0U);
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = (((IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__lease_r) 
                                                << 4U) 
                                               | ((((0U 
                                                     != (IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r)) 
                                                    << 3U) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__no_lease_r) 
                                                      << 2U)) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__sync_ok_r) 
                                                      << 1U) 
                                                     | (IData)(vlSelfRef.milan_datapath__DOT__clkv_tu_w))));
                                    }
                                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__csr__DOT__clkv_ctrl;
                                }
                            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r) 
                                            << 0x00000010U) 
                                           | ((0x00000300U 
                                               & (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                                                  << 6U)) 
                                              | ((((0x07ffffffU 
                                                    != vlSelfRef.milan_datapath__DOT__link_guard__DOT__act_age_r) 
                                                   << 7U) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r) 
                                                      << 6U) 
                                                     | ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__state_r) 
                                                        << 4U))) 
                                                 | (((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r) 
                                                     << 2U) 
                                                    | (((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r) 
                                                        << 1U) 
                                                       | (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_alive_r))))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg2_q;
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg1_q;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg0_q;
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__crft_count_w;
                            }
                        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x00300000U & (
                                                   (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__crft_class_a_w))) 
                                                   << 0x00000014U)) 
                                   | ((0x000fff00U 
                                       & ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
                                           & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__crft_class_a_w)))) 
                                          << 8U)) | 
                                      ((0x00000040U 
                                        & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                           >> 2U)) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__crft_class_a_w) 
                                           << 5U) | 
                                          (((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_val_r) 
                                            << 4U) 
                                           | (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl))))));
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__crf_pducnt_w) 
                                        << 0x00000010U) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__crf_fmterr_w) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__crf_seqerr_w)));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__crf_rate_w;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__crf_delta_w;
                        }
                    } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__crf_locked_w) 
                                        << 0x0000001fU) 
                                       | (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__crf_ctrl));
                            }
                        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__rst_epoch_r;
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_sync_r;
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__avtprx_last_tsd;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_classify_r) 
                                         << 0x00000018U) 
                                        | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_fc_r) 
                                           << 0x00000010U)) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_flags_r) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_basehit_r)));
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_sync_r) 
                                        << 0x00000010U) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__i2spb_overruns));
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r)) 
                                        << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts) 
                                    << 0x00000018U) 
                                   | (((IData)(vlSelfRef.milan_datapath__DOT__maap_defends) 
                                       << 0x00000010U) 
                                      | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r)));
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__avtprx_last_ts;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = (((vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c 
                                 | (- (IData)((0x0000ffffU 
                                               < vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c)))) 
                                << 0x00000010U) | (
                                                   (0x0000ff00U 
                                                    & ((vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c 
                                                        | (- (IData)(
                                                                     (0x000000ffU 
                                                                      < vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c)))) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (vlSelfRef.milan_datapath__DOT__avtprx_tu_c 
                                                         | (- (IData)(
                                                                      (0x000000ffU 
                                                                       < vlSelfRef.milan_datapath__DOT__avtprx_tu_c)))))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((8U 
                                                >= 
                                                (0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U)))
                                                ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                               [(0x0000000fU 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0874U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08b4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                            [(0x0000000fU 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                                    } else if (((0x08b4U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08c8U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x9fU 
                                                >= 
                                                (0x000000e0U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                               [(7U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x08c8U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x08d4U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = ((0x5fU 
                                                >= 
                                                (0x00000060U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    << 3U)))
                                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                               [(3U 
                                                 & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                    >> 2U))]
                                                : 0U);
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__avtprx_frx_c;
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_stat;
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_wedge) 
                                        << 0x00000018U) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code) 
                                           << 0x00000010U) 
                                          | (0x0000ffffU 
                                             & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[8U] 
                                                >> 0x0000000cU))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__acmpl_probe_count) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__acmpl_cmd_count));
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[3U];
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[2U];
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state;
                        }
                    } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_rx_pdus) 
                                        << 0x00000010U) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_count));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__lwsrp_idle_slope;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status;
                        }
                    } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((8U >= (0x0000000fU 
                                       & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                : 0U);
                    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x9fU >= (0x000000e0U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       >> 2U))] : 0U);
                    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((0x5fU >= (0x00000060U 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                                ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       >> 2U))] : 0U);
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((8U >= (0x0000000fU 
                                                   & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                      >> 2U)))
                                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                           [(0x0000000fU 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                >> 2U))]
                                            : 0U);
                                } else if (((0x0874U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08b4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                        [(0x0000000fU 
                                          & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                             >> 2U))];
                                } else if (((0x08b4U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08c8U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x9fU >= 
                                            (0x000000e0U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x08c8U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x08d4U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = ((0x5fU >= 
                                            (0x00000060U 
                                             & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                << 3U)))
                                            ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                   >> 2U))]
                                            : 0U);
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_gate) 
                                         << 3U) | (4U 
                                                   & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                      << 2U))) 
                                       | ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                 << 1U)) 
                                          | (1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__adp_depart_src) 
                                    << 0x00000010U) 
                                   | (((IData)(vlSelfRef.milan_datapath__DOT__adp_rearm_cnt) 
                                       << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__adp_depart_cnt)));
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__aaf_pairs_w;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__aaf_frames_w;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__acmp_resp_count) 
                                << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__acmp_cmd_count));
                    }
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__resp_cnt_r) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r));
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r) 
                                << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__cmd_cnt_r));
                    }
                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__adp_available_index;
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((8U >= (0x0000000fU 
                                               & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                       [(0x0000000fU 
                                         & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                                        : 0U);
                            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08b4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                    [(0x0000000fU & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                       >> 2U))];
                            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08c8U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x9fU >= (0x000000e0U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x08d4U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((0x5fU >= (0x00000060U 
                                                  & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                     << 3U)))
                                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                               >> 2U))]
                                        : 0U);
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_tod_rd 
                                           >> 0x20U));
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((8U >= (0x0000000fU 
                                           & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                                   [(0x0000000fU & 
                                     ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))] : 0U);
                        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                                 >> 2U))];
                        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x9fU >= (0x000000e0U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((0x5fU >= (0x00000060U 
                                              & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                           >> 2U))]
                                    : 0U);
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_tod_rd);
                    }
                } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = (0x0108U | (IData)(vlSelfRef.i_mac_events_cap));
            }
        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                                  >> 2U)))
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                           [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                            >> 2U))]
                            : 0U);
                } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                        [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                         >> 2U))];
                } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x9fU >= (0x000000e0U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                           [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                   >> 2U))] : 0U);
                } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                        = ((0x5fU >= (0x00000060U & 
                                      ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                       << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                           [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                   >> 2U))] : 0U);
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = (((IData)(vlSelfRef.i_full_duplex) 
                        << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__speed_sync) 
                                   << 1U) | (IData)(vlSelfRef.i_link_up)));
            }
        } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                          >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                   [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                    >> 2U))] : 0U);
        } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                 >> 2U))];
        } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                   [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                           >> 2U))] : 0U);
        } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                             << 3U)))
                    ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                   [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                           >> 2U))] : 0U);
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                              >> 2U)))
                        ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
                       [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                        >> 2U))] : 0U);
            } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = vlSelfRef.milan_datapath__DOT__ltap_regs_w
                    [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                                     >> 2U))];
            } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
                       [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                               >> 2U))] : 0U);
            } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                    = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                                 << 3U)))
                        ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
                       [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                               >> 2U))] : 0U);
            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                        & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
            }
        } else {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status;
        }
    } else if (((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = ((8U >= (0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                      >> 2U))) ? vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap
               [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__soff) 
                                >> 2U))] : 0U);
    } else if (((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = vlSelfRef.milan_datapath__DOT__ltap_regs_w
            [(0x0000000fU & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__loff) 
                             >> 2U))];
    } else if (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = ((0x9fU >= (0x000000e0U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                                         << 3U))) ? vlSelfRef.milan_datapath__DOT__aprb_regs_w
               [(7U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff) 
                       >> 2U))] : 0U);
    } else if (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = ((0x5fU >= (0x00000060U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                                         << 3U))) ? vlSelfRef.milan_datapath__DOT__pbk_regs_w
               [(3U & ((IData)(milan_datapath__DOT__csr__DOT__read_mux__DOT__poff) 
                       >> 2U))] : 0U);
    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    }
}
