// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___eval_triggers_vec__ico(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_triggers_vec__ico\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[2U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[2U]) 
                                     | (IData)((IData)(vlSelfRef.__VicoFirstIteration)));
    vlSelfRef.__VicoTriggered[0U] = (((QData)((IData)(
                                                      ((((((((((IData)(vlSelfRef.i_mmcm_drp_do) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_do__0)) 
                                                              << 3U) 
                                                             | (((IData)(vlSelfRef.i_ps_clk) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__0)) 
                                                                << 2U)) 
                                                            | ((((IData)(vlSelfRef.i_mac_events_cap) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events_cap__0)) 
                                                                << 1U) 
                                                               | ((IData)(vlSelfRef.i_mac_events) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_events__0)))) 
                                                           << 0x0000000cU) 
                                                          | ((((((IData)(vlSelfRef.i_gptp_txseal_ack) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txseal_ack__0)) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.i_gptp_txrec_abort) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_abort__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.i_gptp_txrec_delta) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_delta__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.i_gptp_txrec_seq) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_seq__0)))) 
                                                             << 8U)) 
                                                         | (((((((IData)(vlSelfRef.i_gptp_txrec_type) 
                                                                 != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_type__0)) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.i_gptp_txrec_gen) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_gen__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.i_gptp_txrec_oidx) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_oidx__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.i_gptp_txrec_kind) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_kind__0)))) 
                                                             << 4U) 
                                                            | (((((IData)(vlSelfRef.i_gptp_txrec_valid) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_valid__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.i_ethact_tgl) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethact_tgl__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.i_ethtx_tgl) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethtx_tgl__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.i_ethrx_tgl) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ethrx_tgl__0)))))) 
                                                        << 0x00000010U) 
                                                       | ((((((((IData)(vlSelfRef.i_full_duplex) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_full_duplex__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.i_link_up) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_link_up__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.i_mac_speed) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mac_speed__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tlast__0)))) 
                                                            << 0x0000000cU) 
                                                           | ((((((IData)(vlSelfRef.s_axis_mac_rx_tvalid) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tvalid__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.s_axis_mac_rx_tkeep) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tkeep__0)) 
                                                                   << 2U)) 
                                                               | (((vlSelfRef.s_axis_mac_rx_tdata 
                                                                    != vlSelfRef.__Vtrigprevexpr___TOP__s_axis_mac_rx_tdata__0) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__m_axis_mac_tx_tready__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.tdm_data_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_data_i__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.tdm_fsync_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_fsync_i__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.tdm_bclk_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.i2s_sdout_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i2s_sdout_i__0)))) 
                                                              << 4U) 
                                                             | (((((IData)(vlSelfRef.s_axi_rready) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_rready__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.s_axi_arvalid) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_arvalid__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.s_axi_araddr) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_araddr__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.s_axi_bready) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_bready__0))))))))) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(
                                                       ((((((((((IData)(vlSelfRef.s_axi_wvalid) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wvalid__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.s_axi_wstrb) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wstrb__0)) 
                                                                 << 2U)) 
                                                             | (((vlSelfRef.s_axi_wdata 
                                                                  != vlSelfRef.__Vtrigprevexpr___TOP__s_axi_wdata__0) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.s_axi_awvalid) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awvalid__0)))) 
                                                            << 0x0000000cU) 
                                                           | ((((((IData)(vlSelfRef.s_axi_awaddr) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__s_axi_awaddr__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.gtx_resetn) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_resetn__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.gtx_clk) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.axis_resetn) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.clk_tdm_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_tdm_i__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.clk_audio_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.axis_clk) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.i_nvm_mem_wr_err) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_err__0)))) 
                                                              << 4U) 
                                                             | (((((IData)(vlSelfRef.i_nvm_mem_wr_done) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_done__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.i_nvm_mem_wr_ready) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_ready__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.i_nvm_mem_rsp_err) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_err__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.i_nvm_mem_rsp_last) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_last__0)))))) 
                                                         << 0x00000010U) 
                                                        | (((((((vlSelfRef.i_nvm_mem_rsp_data 
                                                                 != vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_data__0) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.i_nvm_mem_rsp_valid) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_valid__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.i_nvm_mem_req_ready) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_req_ready__0)) 
                                                                  << 1U) 
                                                                 | ((IData)(vlSelfRef.i_resp_mem_wr_err) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_err__0)))) 
                                                             << 0x0000000cU) 
                                                            | ((((((IData)(vlSelfRef.i_resp_mem_wr_done) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_done__0)) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.i_resp_mem_wr_ready) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_ready__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.i_resp_mem_rsp_err) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_err__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.i_resp_mem_rsp_last) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_last__0)))) 
                                                               << 8U)) 
                                                           | ((((((vlSelfRef.i_resp_mem_rsp_data 
                                                                   != vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_data__0) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.i_resp_mem_rsp_valid) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_valid__0)) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.i_resp_mem_req_ready) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_req_ready__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.i_desc_mem_rsp_err) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_err__0)))) 
                                                               << 4U) 
                                                              | (((((IData)(vlSelfRef.i_desc_mem_rsp_last) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_last__0)) 
                                                                   << 3U) 
                                                                  | ((vlSelfRef.i_desc_mem_rsp_data 
                                                                      != vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_data__0) 
                                                                     << 2U)) 
                                                                 | ((((IData)(vlSelfRef.i_desc_mem_rsp_valid) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_valid__0)) 
                                                                     << 1U) 
                                                                    | ((IData)(vlSelfRef.i_desc_mem_req_ready) 
                                                                       != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_req_ready__0))))))))));
    vlSelfRef.__VicoTriggered[1U] = (QData)((IData)(
                                                    ((((IData)(vlSelfRef.i_mmcm_ps_done) 
                                                       != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_ps_done__0)) 
                                                      << 2U) 
                                                     | ((((IData)(vlSelfRef.i_mmcm_locked) 
                                                          != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_locked__0)) 
                                                         << 1U) 
                                                        | ((IData)(vlSelfRef.i_mmcm_drp_rdy) 
                                                           != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_mmcm_drp_rdy__0))))));
    vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_req_ready__0 
        = vlSelfRef.i_desc_mem_req_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_valid__0 
        = vlSelfRef.i_desc_mem_rsp_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_data__0 
        = vlSelfRef.i_desc_mem_rsp_data;
    vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_last__0 
        = vlSelfRef.i_desc_mem_rsp_last;
    vlSelfRef.__Vtrigprevexpr___TOP__i_desc_mem_rsp_err__0 
        = vlSelfRef.i_desc_mem_rsp_err;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_req_ready__0 
        = vlSelfRef.i_resp_mem_req_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_valid__0 
        = vlSelfRef.i_resp_mem_rsp_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_data__0 
        = vlSelfRef.i_resp_mem_rsp_data;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_last__0 
        = vlSelfRef.i_resp_mem_rsp_last;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_rsp_err__0 
        = vlSelfRef.i_resp_mem_rsp_err;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_ready__0 
        = vlSelfRef.i_resp_mem_wr_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_done__0 
        = vlSelfRef.i_resp_mem_wr_done;
    vlSelfRef.__Vtrigprevexpr___TOP__i_resp_mem_wr_err__0 
        = vlSelfRef.i_resp_mem_wr_err;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_req_ready__0 
        = vlSelfRef.i_nvm_mem_req_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_valid__0 
        = vlSelfRef.i_nvm_mem_rsp_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_data__0 
        = vlSelfRef.i_nvm_mem_rsp_data;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_last__0 
        = vlSelfRef.i_nvm_mem_rsp_last;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_rsp_err__0 
        = vlSelfRef.i_nvm_mem_rsp_err;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_ready__0 
        = vlSelfRef.i_nvm_mem_wr_ready;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_done__0 
        = vlSelfRef.i_nvm_mem_wr_done;
    vlSelfRef.__Vtrigprevexpr___TOP__i_nvm_mem_wr_err__0 
        = vlSelfRef.i_nvm_mem_wr_err;
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
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_valid__0 
        = vlSelfRef.i_gptp_txrec_valid;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_kind__0 
        = vlSelfRef.i_gptp_txrec_kind;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_oidx__0 
        = vlSelfRef.i_gptp_txrec_oidx;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_gen__0 
        = vlSelfRef.i_gptp_txrec_gen;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_type__0 
        = vlSelfRef.i_gptp_txrec_type;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_seq__0 
        = vlSelfRef.i_gptp_txrec_seq;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_delta__0 
        = vlSelfRef.i_gptp_txrec_delta;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txrec_abort__0 
        = vlSelfRef.i_gptp_txrec_abort;
    vlSelfRef.__Vtrigprevexpr___TOP__i_gptp_txseal_ack__0 
        = vlSelfRef.i_gptp_txseal_ack;
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
        vlSelfRef.__VicoTriggered[0U] = (0x0020000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0040000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0080000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0100000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0200000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0400000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0800000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x1000000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x2000000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x4000000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x8000000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[1U] = (1ULL | vlSelfRef.__VicoTriggered[1U]);
        vlSelfRef.__VicoTriggered[1U] = (2ULL | vlSelfRef.__VicoTriggered[1U]);
        vlSelfRef.__VicoTriggered[1U] = (4ULL | vlSelfRef.__VicoTriggered[1U]);
    }
}

bool Vmilan_datapath___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 3> &in) {
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
    } while ((3U > n));
    return (0U);
}

void Vmilan_datapath___024root___ico_sequent__TOP__10(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_sequent__TOP__10\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w 
        = ((0x0000ff00U & ((IData)((vlSelfRef.s_axis_mac_rx_tdata 
                                    >> 0x00000020U)) 
                           << 8U)) | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 0x00000028U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__accept_w 
        = ((0x22f0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w)) 
           | (((0x00000180c200000eULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_r) 
               & (0x22eaU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w))) 
              | ((0x00000180c2000021ULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_r) 
                 & (0x88f5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w 
        = (((QData)((IData)(((0x0000ff00U & ((IData)(vlSelfRef.s_axis_mac_rx_tdata) 
                                             << 8U)) 
                             | (0x000000ffU & (IData)(
                                                      (vlSelfRef.s_axis_mac_rx_tdata 
                                                       >> 8U)))))) 
            << 0x00000020U) | (QData)((IData)((((IData)(
                                                        (vlSelfRef.s_axis_mac_rx_tdata 
                                                         >> 0x00000010U)) 
                                                << 0x00000018U) 
                                               | ((0x00ff0000U 
                                                   & ((IData)(
                                                              (vlSelfRef.s_axis_mac_rx_tdata 
                                                               >> 0x00000018U)) 
                                                      << 0x00000010U)) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w))))));
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit 
        = (((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[15U] 
                 & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[15U] 
                             & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[15U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[14U] 
                           & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[14U] 
                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[14U] 
                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                          << 2U)) | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[13U] 
                                       & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[13U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[13U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                      << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[12U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[12U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[12U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
             << 0x0000000cU) | (((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[11U] 
                                    & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[11U] 
                                                & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[11U] 
                                                   ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                   << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[10U] 
                                              & (0ULL 
                                                 == 
                                                 (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[10U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[10U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                             << 2U)) 
                                 | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[9U] 
                                      & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[9U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[9U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                     << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[8U] 
                                               & (0ULL 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[8U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[8U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
                                << 8U)) | ((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[7U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[7U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[7U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                               << 3U) 
                                              | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[6U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[6U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[6U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                 << 2U)) 
                                             | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[5U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[5U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[5U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                 << 1U) 
                                                | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[4U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[4U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[4U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
                                            << 4U) 
                                           | ((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[3U] 
                                                 & (0ULL 
                                                    == 
                                                    (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[3U] 
                                                     & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[3U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                << 3U) 
                                               | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[2U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[2U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[2U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                  << 2U)) 
                                              | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[1U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[1U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[1U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                  << 1U) 
                                                 | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[0U] 
                                                    & (0ULL 
                                                       == 
                                                       (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[0U] 
                                                        & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[0U] 
                                                           ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w))))))));
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 0U;
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = 0U;
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[15U];
    }
    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[14U];
    }
    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[13U];
    }
    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[12U];
    }
    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[11U];
    }
    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[10U];
    }
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[9U];
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[8U];
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[7U];
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[6U];
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[5U];
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[4U];
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[3U];
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[2U];
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[1U];
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[0U];
    }
}

void Vmilan_datapath___024root___ico_comb__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ico_comb__TOP__3\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__soff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__soff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__loff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__loff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff = 0;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                                                    (0x2000U 
                                                                     == 
                                                                     (0x6000U 
                                                                      & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r)))) 
                                                            << 0x00000012U) 
                                                           | ((0x00030000U 
                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r) 
                                                                  << 3U)) 
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__mcsrv_stat_w;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w));
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r))) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r)) 
                                  << 0x0000000dU) | 
                                 ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r) 
                                  << 0x0000000cU)) 
                                | ((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r))) 
                                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r)) 
                                    << 9U) | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r) 
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__asp_gen_w) 
                                            << 4U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__asp_count_w));
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__adopted_r) 
                                    << 0x00000018U) 
                                   | ((0x00070000U 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r) 
                                          << 0x00000010U)) 
                                      | (0x00000fffU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r))));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (0xa7000000U | (((IData)(vlSelfRef.milan_datapath__DOT__txarb_stall_sticky_r) 
                                                   << 0x00000010U) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__txarb_abort_sticky_r) 
                                                      << 8U) 
                                                     | (((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r) 
                                                         << 3U) 
                                                        | (((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
                                                            << 2U) 
                                                           | (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r))))));
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = (1U | 
                                               ((0U 
                                                 != (IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r)) 
                                                << 3U));
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((((IData)(vlSelfRef.milan_datapath__DOT__crft_pcp_w) 
                                     & (- (IData)((0U 
                                                   != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28))))) 
                                    << 0x00000014U) 
                                   | ((((IData)(vlSelfRef.milan_datapath__DOT__crft_vid_w) 
                                        & (- (IData)(
                                                     (0U 
                                                      != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28))))) 
                                       << 8U) | (((IData)(vlSelfRef.milan_datapath__DOT__crft_emit_en_w) 
                                                  << 7U) 
                                                 | ((0x00000040U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                        << 5U)) 
                                                    | (((0U 
                                                         != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28)) 
                                                        << 5U) 
                                                       | (3U 
                                                          & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl))))));
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((vlSelfRef.milan_datapath__DOT__crf_pducnt_w 
                                        << 0x00000010U) 
                                       | ((0x0000ff00U 
                                           & (vlSelfRef.milan_datapath__DOT__crf_fmterr_w 
                                              << 8U)) 
                                          | (0x000000ffU 
                                             & vlSelfRef.milan_datapath__DOT__crf_seqerr_w)));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__rst_epoch_r;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code) 
                                       << 0x00000010U);
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_disc_seen_cnt_r) 
                                       << 0x00000010U);
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_raw_w) 
                                         << 3U) | (4U 
                                                   & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                      << 2U))) 
                                       | (2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                << 1U)));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r) 
                               << 0x00000010U);
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__pp_cd_adp_avail_index_w;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    }
}
