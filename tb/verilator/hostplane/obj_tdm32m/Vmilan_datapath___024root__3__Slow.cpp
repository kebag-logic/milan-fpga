// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__3\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__ctlf_tx_tvalid) 
              | (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid)));
    vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__ctlf_tx_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid))));
    vlSelfRef.milan_datapath__DOT__rx_mac_good_w = 
        ((IData)(vlSelfRef.s_axis_mac_rx_tlast) & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc));
    vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i 
        = (((((IData)(vlSelfRef.m_axis_pcm_tready) 
              & ((IData)(vlSelfRef.m_axis_pcm_tvalid) 
                 & (IData)(vlSelfRef.m_axis_pcm_tlast))) 
             << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__dpkt_acc_w) 
                        & (IData)(vlSelfRef.m_axis_pcm_tlast)) 
                       << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w) 
                                   << 1U) | ((~ (IData)(vlSelfRef.milan_datapath__DOT__mac_rx_inframe_r)) 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc))));
    vlSelfRef.milan_datapath__DOT__tkd_streaming_w 
        = ((0x00000100U & (vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl 
                           << 8U)) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w 
        = (((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
             ? (IData)(vlSelfRef.milan_datapath__DOT__cmap_pv_w)
             : ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                | (IData)(vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__pend_any_c))) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w) 
                     & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
                        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w] 
                        & (5U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                           [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                    >> (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w)))));
    vlSelfRef.milan_datapath__DOT__ctlg_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel)
          ? ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid) 
             & (8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r)))
          : (IData)(vlSelfRef.milan_datapath__DOT__ctlf_tx_tlast));
    vlSelfRef.milan_datapath__DOT__ctlg_tx_tvalid = 
        (((IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel)
           ? (IData)(vlSelfRef.milan_datapath__DOT__acmpl_tx_tvalid)
           : (IData)(vlSelfRef.milan_datapath__DOT__ctlf_tx_tvalid)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push 
        = ((((((IData)(vlSelfRef.milan_datapath__DOT__rx_mac_good_w) 
               & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_type_valid)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid)) 
            & (0U == (0x0cU & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type)))) 
           & (2U != (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl)));
    vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w = 0U;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 1U;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
        vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
    } else {
        milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w = 0U;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 1U;
    if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r)) 
         & (IData)(milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i))) {
            vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tvalid)));
    vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r))));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__gsel)
          ? ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r) 
             & (7U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r)))
          : (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tlast));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid = 
        (((IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__gsel)
           ? (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)
           : (IData)(vlSelfRef.milan_datapath__DOT__ctlg_tx_tvalid)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__ctlg2_tvalid = (
                                                   (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid));
}

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__4(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__4\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__ctlf_tx_tready;
    milan_datapath__DOT__ctlf_tx_tready = 0;
    CData/*4:0*/ milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
    milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int = 0;
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_next 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_reg;
    if (((IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.tvalid) 
         & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg))) {
        if ((0x00000100U & vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U])) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_next = 0U;
        }
    }
    if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_reg)) 
          & (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.tvalid)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg))) {
        if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__s_axis_tready_reg) 
                       & (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.tvalid)) 
                      & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                         >> 8U))))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_next = 1U;
        }
    }
    milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int 
        = (0x0000001fU & (((~ (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.__VdfgRegularize_h6e95ff9d_0_97)) 
                           & (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.__VdfgRegularize_h6e95ff9d_0_19)) 
                          << ((IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.__VdfgRegularize_h6e95ff9d_0_18)
                               ? (IData)(vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.tdest)
                               : (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__select_reg))));
    vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__locked_r) 
           | ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)));
    vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__sel_r)
                  : (((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                      & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__last_grant_r))
                      : (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_early 
        = (1U & ((~ ((0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_reg)) 
                     | ((0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)) 
                        & (0U != (IData)(milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int))))) 
                 | (0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_next 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_reg;
    if (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_reg) {
        if ((1U & ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))) 
                   | (~ (0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_next 
                = milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
        }
        if ((1U & (~ ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                              & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))) 
                      | (~ (0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))))))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next 
                = milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
        }
    } else if ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_next 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next = 0U;
    }
    vlSelfRef.milan_datapath__DOT__dpaaf_tlast = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel)
                                                   ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)
                                                   : (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tlast));
    vlSelfRef.milan_datapath__DOT__dpaaf_tvalid = (
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel)
                                                     ? 
                                                    (3U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))
                                                     : (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tvalid)));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__dpcrf_tlast = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
                                                   ? 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
                                                   & (7U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r)))
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tlast));
    vlSelfRef.milan_datapath__DOT__dpcrf_tvalid = (
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
                                                     ? (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r)
                                                     : (IData)(vlSelfRef.milan_datapath__DOT__dpaaf_tvalid)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__ctlg2_tvalid) 
              | (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid)));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__ctlg2_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__ctlg2_tvalid))));
    if (vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel) {
        if (vlSelfRef.milan_datapath__DOT__maap_ctl_mux__DOT__gsel) {
            vlSelfRef.m_axis_mac_tx_tdata = vlSelfRef.milan_datapath__DOT__maap_tx_tdata;
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (0x0fU 
                                                | (- (IData)(
                                                             (7U 
                                                              != (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r))))));
        } else if (vlSelfRef.milan_datapath__DOT__lstn_ctl_mux__DOT__gsel) {
            vlSelfRef.m_axis_mac_tx_tdata = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat;
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (0x3fU 
                                                | (- (IData)(
                                                             (8U 
                                                              != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))))));
        } else if (vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel) {
            vlSelfRef.m_axis_mac_tx_tdata = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)
                                              ? vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r
                                              : (((QData)((IData)(
                                                                  ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                      [
                                                                      (0x0000007fU 
                                                                       & ((IData)(7U) 
                                                                          + 
                                                                          ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                           << 3U)))] 
                                                                      & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(7U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                     << 0x00000018U) 
                                                                    | ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                        [
                                                                        (0x0000007fU 
                                                                         & ((IData)(6U) 
                                                                            + 
                                                                            ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                             << 3U)))] 
                                                                        & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(6U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                       << 0x00000010U)) 
                                                                   | (((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                        [
                                                                        (0x0000007fU 
                                                                         & ((IData)(5U) 
                                                                            + 
                                                                            ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                             << 3U)))] 
                                                                        & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(5U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                       << 8U) 
                                                                      | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                         [
                                                                         (0x0000007fU 
                                                                          & ((IData)(4U) 
                                                                             + 
                                                                             ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                              << 3U)))] 
                                                                         & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(4U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))))))) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(
                                                                   ((((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                       [
                                                                       (0x0000007fU 
                                                                        & ((IData)(3U) 
                                                                           + 
                                                                           ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                            << 3U)))] 
                                                                       & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                      << 0x00000018U) 
                                                                     | ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                         [
                                                                         (0x0000007fU 
                                                                          & ((IData)(2U) 
                                                                             + 
                                                                             ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                              << 3U)))] 
                                                                         & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                        << 0x00000010U)) 
                                                                    | (((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                         [
                                                                         (0x0000007fU 
                                                                          & ((IData)(1U) 
                                                                             + 
                                                                             ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                              << 3U)))] 
                                                                         & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                        << 8U) 
                                                                       | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb
                                                                          [
                                                                          ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                           << 3U)] 
                                                                          & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
                                                                                << 3U)))))))))));
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)
                                                  ? 
                                                 ((VL_SHIFTL_III(8,8,16, (IData)(1U), 
                                                                 (0x0000ffffU 
                                                                  & ((IData)(1U) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r)))) 
                                                   - (IData)(1U)) 
                                                  & (- (IData)(
                                                               (5U 
                                                                == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r)))))
                                                  : 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w)
                                                   ? 
                                                  (((IData)(1U) 
                                                    << 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w)
                                                      ? 2U
                                                      : 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full_w)
                                                       ? 8U
                                                       : 4U))) 
                                                   - (IData)(1U))
                                                   : 
                                                  (- (IData)(
                                                             (1U 
                                                              == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r)))))) 
                                                & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid)))));
        } else if (vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel) {
            if (vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__gsel) {
                vlSelfRef.m_axis_mac_tx_tdata = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat;
                vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                                 & (0x3fU 
                                                    | (- (IData)(
                                                                 (8U 
                                                                  != (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))))));
            } else {
                vlSelfRef.m_axis_mac_tx_tdata = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_r;
                vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_keep_r));
            }
        } else {
            vlSelfRef.m_axis_mac_tx_tdata = (((QData)((IData)(
                                                              ((((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                  [
                                                                  (0x0000007fU 
                                                                   & ((IData)(7U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(7U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                    [
                                                                    (0x0000007fU 
                                                                     & ((IData)(6U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(6U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                    [
                                                                    (0x0000007fU 
                                                                     & ((IData)(5U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(5U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                     [
                                                                     (0x0000007fU 
                                                                      & ((IData)(4U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(4U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))))))) 
                                              << 0x00000020U) 
                                             | (QData)((IData)(
                                                               ((((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                   [
                                                                   (0x0000007fU 
                                                                    & ((IData)(3U) 
                                                                       + 
                                                                       ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                        << 3U)))] 
                                                                   & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                  << 0x00000018U) 
                                                                 | ((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                     [
                                                                     (0x0000007fU 
                                                                      & ((IData)(2U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                    << 0x00000010U)) 
                                                                | (((vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                     [
                                                                     (0x0000007fU 
                                                                      & ((IData)(1U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                (0x0000007fU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                    << 8U) 
                                                                   | (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb
                                                                      [
                                                                      ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                       << 3U)] 
                                                                      & (- (IData)(
                                                                                (0x57U 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r) 
                                                                                << 3U))))))))));
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_tlast)
                                                 ? 3U
                                                 : 
                                                (- (IData)(
                                                           (1U 
                                                            == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__state_r))))));
        }
        vlSelfRef.m_axis_mac_tx_tlast = vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast;
    } else {
        if (vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel) {
            vlSelfRef.m_axis_mac_tx_tdata = (((QData)((IData)(
                                                              (((((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                          [
                                                                          (0x0000003fU 
                                                                           & ((IData)(7U) 
                                                                              + 
                                                                              (0x00000038U 
                                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                                << 3U))))]) 
                                                                  << 8U) 
                                                                 | vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                 [
                                                                 (0x0000003fU 
                                                                  & ((IData)(6U) 
                                                                     + 
                                                                     (0x00000038U 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                         << 3U))))]) 
                                                                << 0x00000010U) 
                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                           [
                                                                           (0x0000003fU 
                                                                            & ((IData)(5U) 
                                                                               + 
                                                                               (0x00000038U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                                << 3U))))]) 
                                                                   << 8U) 
                                                                  | vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                  [
                                                                  (0x0000003fU 
                                                                   & ((IData)(4U) 
                                                                      + 
                                                                      (0x00000038U 
                                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                          << 3U))))])))) 
                                              << 0x00000020U) 
                                             | (QData)((IData)(
                                                               (((((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                           [
                                                                           (0x0000003fU 
                                                                            & ((IData)(3U) 
                                                                               + 
                                                                               (0x00000038U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                                << 3U))))]) 
                                                                   << 8U) 
                                                                  | vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                  [
                                                                  (0x0000003fU 
                                                                   & ((IData)(2U) 
                                                                      + 
                                                                      (0x00000038U 
                                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                          << 3U))))]) 
                                                                 << 0x00000010U) 
                                                                | (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                            [
                                                                            (0x0000003fU 
                                                                             & ((IData)(1U) 
                                                                                + 
                                                                                (0x00000038U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                                << 3U))))]) 
                                                                    << 8U) 
                                                                   | vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb
                                                                   [
                                                                   (0x00000038U 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r) 
                                                                       << 3U))])))));
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (0x0fU 
                                                | (- (IData)(
                                                             (7U 
                                                              != (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r))))));
        } else if (vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel) {
            vlSelfRef.m_axis_mac_tx_tdata = (((QData)((IData)(
                                                              ((((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                  [
                                                                  (0x000000ffU 
                                                                   & ((IData)(7U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(7U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(6U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(6U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(5U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(5U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                     [
                                                                     (0x000000ffU 
                                                                      & ((IData)(4U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(4U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))))))) 
                                              << 0x00000020U) 
                                             | (QData)((IData)(
                                                               ((((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                   [
                                                                   (0x000000ffU 
                                                                    & ((IData)(3U) 
                                                                       + 
                                                                       ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                        << 3U)))] 
                                                                   & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                  << 0x00000018U) 
                                                                 | ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                     [
                                                                     (0x000000ffU 
                                                                      & ((IData)(2U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                    << 0x00000010U)) 
                                                                | (((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                     [
                                                                     (0x000000ffU 
                                                                      & ((IData)(1U) 
                                                                         + 
                                                                         ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                          << 3U)))] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                    << 8U) 
                                                                   | (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb
                                                                      [
                                                                      ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                       << 3U)] 
                                                                      & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                                                << 3U))))))))));
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (3U 
                                                | (- (IData)(
                                                             (1U 
                                                              & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76)))))));
        } else {
            vlSelfRef.m_axis_mac_tx_tdata = vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata;
            vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU 
                                             & (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tkeep));
        }
        vlSelfRef.m_axis_mac_tx_tlast = vlSelfRef.milan_datapath__DOT__dpcrf_tlast;
    }
    vlSelfRef.m_axis_mac_tx_tvalid = (((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)
                                        ? (IData)(vlSelfRef.milan_datapath__DOT__ctlg2_tvalid)
                                        : (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid)) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tready = 
        ((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
            & ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
               & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel))));
    vlSelfRef.milan_datapath__DOT__dpcrf_tready = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
                                                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)) 
                                                      & (IData)(vlSelfRef.m_axis_mac_tx_tready)));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
           & (IData)(vlSelfRef.m_axis_mac_tx_tvalid));
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
    vlSelfRef.milan_datapath__DOT__tx_mac_good_w = 
        ((IData)(vlSelfRef.m_axis_mac_tx_tlast) & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted));
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
    vlSelfRef.milan_datapath__DOT__mac_events_w = (
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__rx_mac_good_w) 
                                                     << 8U) 
                                                    | (0x000000f0U 
                                                       & (IData)(vlSelfRef.i_mac_events))) 
                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__tx_mac_good_w) 
                                                       << 3U) 
                                                      | (7U 
                                                         & (IData)(vlSelfRef.i_mac_events))));
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

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vmilan_datapath___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__0(Vmilan_datapath___024root* vlSelf);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__1(Vmilan_datapath___024root* vlSelf);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__2(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf);
VL_ATTR_COLD void Vmilan_datapath_axi_stream_if__TC3___stl_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0(Vmilan_datapath_axi_stream_if__TC3* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf);
VL_ATTR_COLD void Vmilan_datapath_axi_stream_if___stl_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath___024root___ico_sequent__TOP__10(Vmilan_datapath___024root* vlSelf);

VL_ATTR_COLD bool Vmilan_datapath___024root___eval_phase__stl(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_phase__stl\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[0U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmilan_datapath___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vmilan_datapath___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vmilan_datapath___024root___stl_sequent__TOP__0(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__1(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__2(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__3(vlSelf);
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx));
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx));
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo));
                Vmilan_datapath_axi_stream_if__TC3___stl_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0((&vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue));
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0((&vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo));
                Vmilan_datapath_axi_stream_if___stl_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx));
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered));
                Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered));
                Vmilan_datapath___024root___stl_sequent__TOP__4(vlSelf);
                Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx));
                Vmilan_datapath___024root___ico_sequent__TOP__10(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool Vmilan_datapath___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vmilan_datapath___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( clk_tdm_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( axis_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( gtx_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( gtx_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( s_axi_awaddr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( s_axi_awvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( s_axi_wdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( s_axi_wstrb)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( s_axi_wvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( s_axi_bready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( s_axi_araddr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( s_axi_arvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( s_axi_rready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @( i2s_sdout_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000010U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 16 is active: @( tdm_bclk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000011U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 17 is active: @( tdm_fsync_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000012U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 18 is active: @( tdm_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000013U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 19 is active: @( s_axis_tx_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000014U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 20 is active: @( s_axis_tx_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000015U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 21 is active: @( s_axis_tx_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000016U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 22 is active: @( s_axis_tx_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000017U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 23 is active: @( m_axis_rx_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000018U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 24 is active: @( m_axis_ts_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000019U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 25 is active: @( m_axis_pcm_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 26 is active: @( m_axis_mac_tx_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 27 is active: @( s_axis_mac_rx_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 28 is active: @( s_axis_mac_rx_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 29 is active: @( s_axis_mac_rx_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 30 is active: @( s_axis_mac_rx_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 31 is active: @( i_mac_speed)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000020U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 32 is active: @( i_link_up)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000021U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 33 is active: @( i_full_duplex)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000022U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 34 is active: @( i_ethrx_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000023U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 35 is active: @( i_ethtx_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000024U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 36 is active: @( i_ethact_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000025U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 37 is active: @( i_mac_events)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000026U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 38 is active: @( i_mac_events_cap)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000027U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 39 is active: @( i_ps_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000028U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 40 is active: @( i_mmcm_drp_do)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000029U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 41 is active: @( i_mmcm_drp_rdy)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 42 is active: @( i_mmcm_locked)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 43 is active: @( i_mmcm_ps_done)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 44 is active: @( pb_enable_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 45 is active: @( pb_underrun_silence_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 46 is active: @( pb_stream_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 47 is active: @( pb_ring_base_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000030U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 48 is active: @( pb_ring_len_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000031U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 49 is active: @( pb_ring_stride_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000032U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 50 is active: @( pb_wr_ptr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000033U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 51 is active: @( pb_mem_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000034U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 52 is active: @( pb_mem_valid_i)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vmilan_datapath___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vmilan_datapath___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(negedge axis_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(posedge gtx_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @(posedge i_ps_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @(posedge clk_tdm_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @(posedge tdm_bclk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @(negedge tdm_bclk_i)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmilan_datapath___024root___ctor_var_reset(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ctor_var_reset\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->axis_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6077951788264469019ull);
    vlSelf->clk_audio_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1594742816405956070ull);
    vlSelf->clk_tdm_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7413527665814040540ull);
    vlSelf->axis_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13353824713052781882ull);
    vlSelf->gtx_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5173468789992344027ull);
    vlSelf->gtx_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2680759800423739578ull);
    vlSelf->s_axi_awaddr = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7303631981020876172ull);
    vlSelf->s_axi_awvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13986037914296269070ull);
    vlSelf->s_axi_awready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14099717354022636468ull);
    vlSelf->s_axi_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11311253403970331505ull);
    vlSelf->s_axi_wstrb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18112015138521062007ull);
    vlSelf->s_axi_wvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12168530306759773544ull);
    vlSelf->s_axi_wready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17608475915581965368ull);
    vlSelf->s_axi_bresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15162762900795686431ull);
    vlSelf->s_axi_bvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9334582144896637853ull);
    vlSelf->s_axi_bready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15653039750784194130ull);
    vlSelf->s_axi_araddr = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8722301305194254610ull);
    vlSelf->s_axi_arvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17746383479076595557ull);
    vlSelf->s_axi_arready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17791137924766170856ull);
    vlSelf->s_axi_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12866136205313389248ull);
    vlSelf->s_axi_rresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14929039895447920609ull);
    vlSelf->s_axi_rvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15026938065200214434ull);
    vlSelf->s_axi_rready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1794163653381394343ull);
    vlSelf->i2s_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423347039955195428ull);
    vlSelf->i2s_sclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12336826856301995358ull);
    vlSelf->i2s_lrck_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12702184149590278752ull);
    vlSelf->i2s_sdout_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12609160700012968368ull);
    vlSelf->tdm_bclk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5699283679770343600ull);
    vlSelf->tdm_fsync_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10282997290289300815ull);
    vlSelf->tdm_bclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6965329311526475437ull);
    vlSelf->tdm_fsync_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16814085176203882082ull);
    vlSelf->tdm_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10274639198335473810ull);
    vlSelf->tdm_dout_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10075644028125443285ull);
    vlSelf->tdm_data_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 249104219551189225ull);
    vlSelf->i2s_dac_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15991117030507183412ull);
    vlSelf->i2s_dac_sclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6188101327151889509ull);
    vlSelf->i2s_dac_lrck_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15109550057939289842ull);
    vlSelf->i2s_dac_sdin_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12092247001711845357ull);
    vlSelf->s_axis_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16415501603384742319ull);
    vlSelf->s_axis_tx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3157636447565749703ull);
    vlSelf->s_axis_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11371248574670827460ull);
    vlSelf->s_axis_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6321668314625288019ull);
    vlSelf->s_axis_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1739555264497535737ull);
    vlSelf->m_axis_rx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 259829326048321033ull);
    vlSelf->m_axis_rx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3749104770080218473ull);
    vlSelf->m_axis_rx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 48968215238118370ull);
    vlSelf->m_axis_rx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3101536001143430368ull);
    vlSelf->m_axis_rx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4361656292483556361ull);
    vlSelf->m_axis_ts_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10564418914368938687ull);
    vlSelf->m_axis_ts_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3211204145821392554ull);
    vlSelf->m_axis_ts_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 772386564919162376ull);
    vlSelf->m_axis_ts_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4348073148603558035ull);
    vlSelf->m_axis_ts_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16829592571201778493ull);
    vlSelf->m_axis_pcm_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1132034560091874225ull);
    vlSelf->m_axis_pcm_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15564697711141249833ull);
    vlSelf->m_axis_pcm_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15108892509901311844ull);
    vlSelf->m_axis_pcm_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 857924586046500163ull);
    vlSelf->m_axis_pcm_tuser = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3629428872415217789ull);
    vlSelf->m_axis_pcm_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 322232804442252154ull);
    vlSelf->m_axis_mac_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15143801499840899111ull);
    vlSelf->m_axis_mac_tx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 738608253460617607ull);
    vlSelf->m_axis_mac_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5400468824722945811ull);
    vlSelf->m_axis_mac_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10639951793926383514ull);
    vlSelf->m_axis_mac_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9083978707389035195ull);
    vlSelf->s_axis_mac_rx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12209863760678251275ull);
    vlSelf->s_axis_mac_rx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16585703592530200061ull);
    vlSelf->s_axis_mac_rx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14244922896429315029ull);
    vlSelf->s_axis_mac_rx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2220400039292505466ull);
    vlSelf->s_axis_mac_rx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13317654005310498863ull);
    vlSelf->o_mac_tx_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15037823534458705414ull);
    vlSelf->o_mac_rx_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5063602202964203523ull);
    vlSelf->o_mac_promisc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4670518256112370292ull);
    vlSelf->o_mac_allmulti = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10925070383356420001ull);
    vlSelf->o_mac_is_1g = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4966978584655898513ull);
    vlSelf->o_mac_ifg = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12558639081818450165ull);
    vlSelf->o_mac_addr = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1090671019676852888ull);
    vlSelf->o_mc_hash = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5755992057034942001ull);
    vlSelf->o_phy_reset_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5522851275748308250ull);
    vlSelf->i_mac_speed = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8070410579128174512ull);
    vlSelf->i_link_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11482461471016620714ull);
    vlSelf->o_mac_reinit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3309491463662001815ull);
    vlSelf->o_eth_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11540013861626318719ull);
    vlSelf->i_full_duplex = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8284182092553005671ull);
    vlSelf->i_ethrx_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13779400073553134942ull);
    vlSelf->i_ethtx_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6328850538460614146ull);
    vlSelf->i_ethact_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8350416218769883425ull);
    vlSelf->i_mac_events = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 15629906174150829998ull);
    vlSelf->i_mac_events_cap = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3340822992242150149ull);
    vlSelf->o_irq_csr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6225454987077696020ull);
    vlSelf->o_identify = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18283969343321504074ull);
    vlSelf->i_ps_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6937211462614486023ull);
    vlSelf->o_mmcm_drp_addr = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9865487830482611112ull);
    vlSelf->o_mmcm_drp_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18272286907461658735ull);
    vlSelf->o_mmcm_drp_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14416325893219994434ull);
    vlSelf->o_mmcm_drp_di = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10469714080661564417ull);
    vlSelf->i_mmcm_drp_do = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16827613955313012702ull);
    vlSelf->i_mmcm_drp_rdy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6419347779287378628ull);
    vlSelf->o_mmcm_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9755853081830159184ull);
    vlSelf->i_mmcm_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16896774293450154370ull);
    vlSelf->o_mmcm_ps_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5587911038871228330ull);
    vlSelf->o_mmcm_ps_incdec = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3062487017950512122ull);
    vlSelf->i_mmcm_ps_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16029815512320568101ull);
    vlSelf->pb_enable_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12464769880058229185ull);
    vlSelf->pb_underrun_silence_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1372220939174789710ull);
    vlSelf->pb_stream_en_i = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8396851030060468818ull);
    vlSelf->pb_ring_base_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6289538639615071639ull);
    vlSelf->pb_ring_len_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3875773263943364672ull);
    vlSelf->pb_ring_stride_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17882708897052422163ull);
    VL_SCOPED_RAND_RESET_W(256, vlSelf->pb_wr_ptr_i, __VscopeHash, 9424087468125025294ull);
    vlSelf->pb_mem_addr_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14920871145320799965ull);
    vlSelf->pb_mem_rd_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16108621862669729602ull);
    vlSelf->pb_mem_data_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1790999946194295579ull);
    vlSelf->pb_mem_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 923119832750283413ull);
    VL_SCOPED_RAND_RESET_W(256, vlSelf->pb_rd_ptr_o, __VscopeHash, 7090246253028141600ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->pb_underrun_o, __VscopeHash, 8780627307261684305ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->pb_overrun_o, __VscopeHash, 6934863781511822362ull);
    vlSelf->pb_playing_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2160907150970365803ull);
    vlSelf->milan_datapath__DOT__media_tick_cnt_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 1420530880733737040ull);
    vlSelf->milan_datapath__DOT__media_tick_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11265168358881453983ull);
    vlSelf->milan_datapath__DOT__aafcap_pv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11497447767300903891ull);
    vlSelf->milan_datapath__DOT__cmap_pv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8426201612662789099ull);
    vlSelf->milan_datapath__DOT__cmap_slot_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10857960519165212280ull);
    vlSelf->milan_datapath__DOT__cmap_l_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15823033237472017079ull);
    vlSelf->milan_datapath__DOT__cmap_r_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10996773100535320075ull);
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i = 0;
    vlSelf->milan_datapath__DOT__zf_adiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 10007575598630145481ull);
    vlSelf->milan_datapath__DOT__zf_apulse_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10825683663302235363ull);
    VL_SCOPED_RAND_RESET_W(288, vlSelf->milan_datapath__DOT__stats_counts, __VscopeHash, 10706589549752702121ull);
    vlSelf->milan_datapath__DOT__cfg_adp_entity_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12778838654269787552ull);
    vlSelf->milan_datapath__DOT__cfg_adp_entity_model_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8265942394376190644ull);
    vlSelf->milan_datapath__DOT__cfg_adp_gptp_gm = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14108897804125996559ull);
    vlSelf->milan_datapath__DOT__cfg_adp_association_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13433048629579876626ull);
    vlSelf->milan_datapath__DOT__adp_available_index = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8734082961166506353ull);
    vlSelf->milan_datapath__DOT__adp_depart_cnt = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2908872380178742692ull);
    vlSelf->milan_datapath__DOT__adp_rearm_cnt = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14676005258527941534ull);
    vlSelf->milan_datapath__DOT__adp_depart_src = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5372172923079574735ull);
    vlSelf->milan_datapath__DOT__adp_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4120828855008099017ull);
    vlSelf->milan_datapath__DOT__aecp_discover_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7238793592120996424ull);
    vlSelf->milan_datapath__DOT__ctl2_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6389237749341502971ull);
    vlSelf->milan_datapath__DOT__ctl2_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11454320652291967814ull);
    vlSelf->milan_datapath__DOT__ctl2_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2957342349022689531ull);
    vlSelf->milan_datapath__DOT__acmp_cmd_count = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17697449430785949180ull);
    vlSelf->milan_datapath__DOT__acmp_resp_count = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1585175002500342731ull);
    vlSelf->milan_datapath__DOT__acmp_talker_active_v = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 200421672576940339ull);
    vlSelf->milan_datapath__DOT__acmp_probe_armed_v = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13368608947088661368ull);
    vlSelf->milan_datapath__DOT__cfg_lwsrp_dmac = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11751275771794093645ull);
    vlSelf->milan_datapath__DOT__lwsrp_stream_gate = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 7574568390007009598ull);
    vlSelf->milan_datapath__DOT__lwsrp_slope_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18113093111389468175ull);
    vlSelf->milan_datapath__DOT__lwsrp_ctx_oor_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9996101646392796066ull);
    vlSelf->milan_datapath__DOT__lwsrp_idle_slope = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11585220018578787556ull);
    vlSelf->milan_datapath__DOT__lwsrp_listener_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11281255878166338913ull);
    vlSelf->milan_datapath__DOT__lwsrp_listener_reg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14327205488949290140ull);
    vlSelf->milan_datapath__DOT__lwsrp_listener_decl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3671276769258653978ull);
    vlSelf->milan_datapath__DOT__lwsrp_over_limit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 444258967936069198ull);
    vlSelf->milan_datapath__DOT__lwsrp_talker_declared = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16673440748199762827ull);
    vlSelf->milan_datapath__DOT__lwsrp_tfail_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2951463562747452403ull);
    vlSelf->milan_datapath__DOT__lwsrp_tfail_code = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4507931381005058632ull);
    vlSelf->milan_datapath__DOT__lwsrp_rx_drops = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5271464372960728638ull);
    vlSelf->milan_datapath__DOT__lwsrp_tx_count = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 439358672659430944ull);
    vlSelf->milan_datapath__DOT__lwsrp_rx_pdus = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11406506321257111538ull);
    vlSelf->milan_datapath__DOT__lwsrp_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15142947367011489573ull);
    vlSelf->milan_datapath__DOT__lwsrp_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5492531815078328502ull);
    vlSelf->milan_datapath__DOT__lwsrp_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11117999738083681587ull);
    vlSelf->milan_datapath__DOT__acmpl_cmd_count = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15708600598859172157ull);
    vlSelf->milan_datapath__DOT__acmpl_probe_count = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1315407829299926552ull);
    vlSelf->milan_datapath__DOT__acmpl_tx_wedge = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14345320969839144627ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_registered = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13584710908053121631ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_failed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14209351771644049158ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_fail_code = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11149421810067148588ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_vlan = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 6191960469046918478ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_acclat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6853946393119755746ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_fail_bridge = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12290809192558035110ull);
    vlSelf->milan_datapath__DOT__lwsrp_tfail_bridge = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8529006327971315932ull);
    vlSelf->milan_datapath__DOT__lwsrp_lstn_declared = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8656199831388397936ull);
    vlSelf->milan_datapath__DOT__acmpl_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4820269088178701028ull);
    vlSelf->milan_datapath__DOT__avtprx_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9581928488041677097ull);
    vlSelf->milan_datapath__DOT__avtprx_tu_bit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15750408439100639188ull);
    vlSelf->milan_datapath__DOT__avtprx_subtype = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15517962545694870490ull);
    vlSelf->milan_datapath__DOT__avtprx_seq = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15318652276024131232ull);
    vlSelf->milan_datapath__DOT__avtprx_parse_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17471729444664175489ull);
    vlSelf->milan_datapath__DOT__avtprx_b3 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6854776964281988079ull);
    vlSelf->milan_datapath__DOT__avtprx_sid_frame = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9357593800724767191ull);
    vlSelf->milan_datapath__DOT__avtprx_fsh2 = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13813041616072532820ull);
    vlSelf->milan_datapath__DOT__crf_delta_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11585917338666239029ull);
    vlSelf->milan_datapath__DOT__crf_rate_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14603279414965205478ull);
    vlSelf->milan_datapath__DOT__cmap_rd_data_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2072824648919118899ull);
    vlSelf->milan_datapath__DOT__cmap_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6545621321986456474ull);
    vlSelf->milan_datapath__DOT__rmap_rd_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16740915263080753453ull);
    vlSelf->milan_datapath__DOT__rmap_rd_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1959725660008616375ull);
    vlSelf->milan_datapath__DOT__crf_pducnt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10817382443418001049ull);
    vlSelf->milan_datapath__DOT__crf_fmterr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8743435823925351606ull);
    vlSelf->milan_datapath__DOT__crf_seqerr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12301550503346426821ull);
    vlSelf->milan_datapath__DOT__crf_locked_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14272717680748612485ull);
    vlSelf->milan_datapath__DOT__crf_cnt_locked_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15495759896246371449ull);
    vlSelf->milan_datapath__DOT__crf_cnt_unlocked_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 878607864546400700ull);
    vlSelf->milan_datapath__DOT__cfg_crft_sid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3719907576149270471ull);
    vlSelf->milan_datapath__DOT__cfg_crft_dmac = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9316951305529298624ull);
    vlSelf->milan_datapath__DOT__crft_count_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10242208974377535130ull);
    vlSelf->milan_datapath__DOT__avtprx_fsh = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12124802238740490791ull);
    vlSelf->milan_datapath__DOT__i2spb_converged = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13323077818788284387ull);
    vlSelf->milan_datapath__DOT__avtprx_locked_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10220531439738838723ull);
    vlSelf->milan_datapath__DOT__avtprx_unlocked_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3610443356898165884ull);
    vlSelf->milan_datapath__DOT__avtprx_intr_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12867675969829508175ull);
    vlSelf->milan_datapath__DOT__avtprx_seqmm_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9497827592088147795ull);
    vlSelf->milan_datapath__DOT__avtprx_tu_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2830501567389268452ull);
    vlSelf->milan_datapath__DOT__avtprx_unsupp_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9723216014700180783ull);
    vlSelf->milan_datapath__DOT__avtprx_frx_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14931353203232863924ull);
    vlSelf->milan_datapath__DOT__avtprx_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14348297884874342533ull);
    vlSelf->milan_datapath__DOT__avtprx_dirty_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10798932733262181739ull);
    vlSelf->milan_datapath__DOT__avtprx_ts = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8506778929196827176ull);
    vlSelf->milan_datapath__DOT__avtprx_last_ts = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 799081269505565408ull);
    vlSelf->milan_datapath__DOT__avtprx_last_tsd = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5367327513087317926ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdus = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10063322807260198664ull);
    vlSelf->milan_datapath__DOT__pcmrx_drops = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15777613349304698758ull);
    vlSelf->milan_datapath__DOT__i2spb_overruns = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4055730579710252853ull);
    vlSelf->milan_datapath__DOT__i2spb_reset_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 202267063101715777ull);
    vlSelf->milan_datapath__DOT__avtprx_mreset_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8002412835173788800ull);
    vlSelf->milan_datapath__DOT__avtprx_late_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17866018677138587934ull);
    vlSelf->milan_datapath__DOT__avtprx_early_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17285264507100190796ull);
    vlSelf->milan_datapath__DOT__tone_smp = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 16772839412458705638ull);
    vlSelf->milan_datapath__DOT__maap_conflicts = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18441516264322472447ull);
    vlSelf->milan_datapath__DOT__maap_defends = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1591325562359595527ull);
    vlSelf->milan_datapath__DOT__maap_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 641374759029110921ull);
    vlSelf->milan_datapath__DOT__eff_aaf_dmac = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6957940404518977664ull);
    vlSelf->milan_datapath__DOT__listener_observed_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 168145898767164494ull);
    vlSelf->milan_datapath__DOT__acmp_lobs_v_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12755437314808280995ull);
    vlSelf->milan_datapath__DOT__eff_crft_dmac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3863360558293694943ull);
    vlSelf->milan_datapath__DOT__eff_crft_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3698678806625628442ull);
    vlSelf->milan_datapath__DOT__aaf_gate = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1010047791604198495ull);
    vlSelf->milan_datapath__DOT__clkv_tu_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16340567062227817511ull);
    vlSelf->milan_datapath__DOT__aaf_stream_en_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5162039671192246409ull);
    vlSelf->milan_datapath__DOT__tctx_en_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12898531126016371076ull);
    vlSelf->milan_datapath__DOT__aaf_frames_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9527180539345585902ull);
    vlSelf->milan_datapath__DOT__aaf_pairs_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15192115273525669703ull);
    vlSelf->milan_datapath__DOT__aaf_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423823035082437557ull);
    vlSelf->milan_datapath__DOT__aaf_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7661987217693464025ull);
    vlSelf->milan_datapath__DOT__ctl_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13179404058159254725ull);
    vlSelf->milan_datapath__DOT__ctl_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5314756815191521738ull);
    vlSelf->milan_datapath__DOT__ctl_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10421127908974753772ull);
    vlSelf->milan_datapath__DOT__cfg_entity_name8 = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9057530258487432263ull);
    vlSelf->milan_datapath__DOT__cfg_as_parent_ckid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18152005974883516338ull);
    vlSelf->milan_datapath__DOT__pcm_lpf_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8229790780032518910ull);
    vlSelf->milan_datapath__DOT__pcm_lpf_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5646003237951859627ull);
    vlSelf->milan_datapath__DOT__pcm_lpf_active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5439123634673765252ull);
    vlSelf->milan_datapath__DOT__eff_link_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16817596118108666834ull);
    vlSelf->milan_datapath__DOT__speed_meta = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4837278814806877417ull);
    vlSelf->milan_datapath__DOT__speed_sync = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6272108155055891160ull);
    vlSelf->milan_datapath__DOT__speed_q = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9158718518922404271ull);
    vlSelf->milan_datapath__DOT__evt_link_change = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10946406234754321371ull);
    vlSelf->milan_datapath__DOT__csr_srp_ctx_dir = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6007756352700249320ull);
    vlSelf->milan_datapath__DOT__csr_srp_ctx_idx = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14559533033895061751ull);
    vlSelf->milan_datapath__DOT__srp_ctx_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7447292313886470403ull);
    vlSelf->milan_datapath__DOT__srp_ctx_rd_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6111181497415336223ull);
    vlSelf->milan_datapath__DOT__srp_ctx_rd_stat_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14817035630974283909ull);
    vlSelf->milan_datapath__DOT__lctx_rd_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13827211125096639787ull);
    vlSelf->milan_datapath__DOT__lctx_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 116946274760354784ull);
    vlSelf->milan_datapath__DOT__tctx_rd_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10637310815187602338ull);
    vlSelf->milan_datapath__DOT__tctx_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14633195025871186257ull);
    vlSelf->milan_datapath__DOT__tctx_wr_rdy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15699263573784844206ull);
    vlSelf->milan_datapath__DOT__acmp_tbl_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6642017972192233275ull);
    vlSelf->milan_datapath__DOT__acmp_rest_ack_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12361526156679570471ull);
    vlSelf->milan_datapath__DOT__acmp_rest_status_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16746372945601867431ull);
    VL_SCOPED_RAND_RESET_W(512, vlSelf->milan_datapath__DOT__ltap_regs_w, __VscopeHash, 2531630792937749745ull);
    VL_SCOPED_RAND_RESET_W(160, vlSelf->milan_datapath__DOT__aprb_regs_w, __VscopeHash, 15465088788055703711ull);
    vlSelf->milan_datapath__DOT__aprb_parsed_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7391203514751151266ull);
    vlSelf->milan_datapath__DOT__aprb_matched_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10366795533886555106ull);
    VL_SCOPED_RAND_RESET_W(96, vlSelf->milan_datapath__DOT__pbk_regs_w, __VscopeHash, 3948721975004052036ull);
    vlSelf->milan_datapath__DOT__pbk_feeds_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11362432915085426356ull);
    vlSelf->milan_datapath__DOT__pbk_unarmed_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7372427306241820878ull);
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt = 0;
    VL_ZERO_RESET_W(320, vlSelf->milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10);
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_avtprx_stat = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_acmpl_state = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_tlk_lobs_v = 0;
    VL_SCOPED_RAND_RESET_W(160, vlSelf->milan_datapath__DOT__cbs_idle_slope_mux, __VscopeHash, 7552968137075053694ull);
    vlSelf->milan_datapath__DOT__cbs_enable_mux = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13663418601677125456ull);
    vlSelf->milan_datapath__DOT__cnt_link_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14161186083375211980ull);
    vlSelf->milan_datapath__DOT__adp_tick_cnt = VL_SCOPED_RAND_RESET_I(27, __VscopeHash, 9434251741600375827ull);
    vlSelf->milan_datapath__DOT__adp_tick_1s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9978307480630999714ull);
    vlSelf->milan_datapath__DOT__link_up_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 524997223378161355ull);
    vlSelf->milan_datapath__DOT__adp_en_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17770767265017051521ull);
    vlSelf->milan_datapath__DOT__adp_link_up_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2379963824652114179ull);
    vlSelf->milan_datapath__DOT__adp_link_down_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13507144379705171434ull);
    vlSelf->milan_datapath__DOT__aaf_frame_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8194287604016912902ull);
    vlSelf->milan_datapath__DOT__aaf_frame_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13568086263833277174ull);
    VL_SCOPED_RAND_RESET_W(320, vlSelf->milan_datapath__DOT__mon_diag_cnt_w, __VscopeHash, 10109929257218015994ull);
    VL_SCOPED_RAND_RESET_W(160, vlSelf->milan_datapath__DOT__tkdiag_cnt_w, __VscopeHash, 3144959983453501658ull);
    vlSelf->milan_datapath__DOT__tkd_crfq_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 728874270301053323ull);
    vlSelf->milan_datapath__DOT__tkd_crf_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13100405196424847648ull);
    vlSelf->milan_datapath__DOT__tkd_crf_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11091641088012514478ull);
    vlSelf->milan_datapath__DOT__tkd_streaming_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 7503956593502142891ull);
    vlSelf->milan_datapath__DOT____Vcellinp__talker_diag__frame_idx_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__aecp_listener__in0_cnt_unlocked_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__aecp_listener__in0_cnt_locked_i = 0;
    VL_ZERO_RESET_W(317, vlSelf->milan_datapath__DOT____Vcellout__acmp_listener_sm__tbl_ctx_o);
    VL_SCOPED_RAND_RESET_W(512, vlSelf->milan_datapath__DOT__strtbl_sid_w, __VscopeHash, 2197151249041805420ull);
    vlSelf->milan_datapath__DOT__strtbl_en_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2415354827475649420ull);
    vlSelf->milan_datapath__DOT__strtbl_bind_rise_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10631870050422074585ull);
    vlSelf->milan_datapath__DOT__avtprx_idx = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7253558521628751539ull);
    vlSelf->milan_datapath__DOT__wing_sid_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6822039806007354170ull);
    vlSelf->milan_datapath__DOT__wing_sid_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7561302499200290245ull);
    vlSelf->milan_datapath__DOT__wing_tbl_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2522355131957675015ull);
    vlSelf->milan_datapath__DOT__wing_route_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9896004326696419040ull);
    vlSelf->milan_datapath__DOT__wing_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13371789636650930020ull);
    vlSelf->milan_datapath__DOT__wing_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13282963973772837908ull);
    vlSelf->milan_datapath__DOT__wing_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4096128156033715318ull);
    vlSelf->milan_datapath__DOT__wing_route_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16829449398551260536ull);
    vlSelf->milan_datapath__DOT__wing_stg_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12651530673605954376ull);
    vlSelf->milan_datapath__DOT__wing_stg_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13673431677608847409ull);
    vlSelf->milan_datapath__DOT__wing_stg_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6617029147642252770ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__tctx_chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8350233718241234744ull);
    }
    vlSelf->milan_datapath__DOT__tctx_w0_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4469228481413523085ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__tctx_maxf_w[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15063315558721320024ull);
    }
    vlSelf->milan_datapath__DOT__srp_tk_row_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12308518650040176400ull);
    vlSelf->milan_datapath__DOT__crf_srp_want_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9647211820058406608ull);
    vlSelf->milan_datapath__DOT__crf_srp_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5653753590363559341ull);
    vlSelf->milan_datapath__DOT__crf_srp_val_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15365211252743890020ull);
    vlSelf->milan_datapath__DOT__crf_srp_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1353806922124206502ull);
    vlSelf->milan_datapath__DOT__crf_srp_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2055388394057292874ull);
    vlSelf->milan_datapath__DOT__crf_srp_dmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12798085621215528935ull);
    vlSelf->milan_datapath__DOT__crf_srp_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15711879245649495753ull);
    vlSelf->milan_datapath__DOT__crf_srp_svc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14083372119619231861ull);
    vlSelf->milan_datapath__DOT__crf_srp_own_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2110618217077677669ull);
    vlSelf->milan_datapath__DOT__crft_class_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17244308569989807487ull);
    vlSelf->milan_datapath__DOT__aprb_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8626551245803039595ull);
    vlSelf->milan_datapath__DOT__aprb_subtype_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11566530242074326322ull);
    vlSelf->milan_datapath__DOT__aprb_hit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10868826433648112151ull);
    vlSelf->milan_datapath__DOT__aprb_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15310557036444193693ull);
    vlSelf->milan_datapath__DOT__mon_wire_chans_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14997162187788332156ull);
    vlSelf->milan_datapath__DOT__mon_wire_chans_all_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1579744739283457856ull);
    vlSelf->milan_datapath__DOT__avtprx_accept_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3677133579513647104ull);
    vlSelf->milan_datapath__DOT__avtprx_accept_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1414169440209116727ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdu_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11547547182200947428ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdu_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8145486983957448768ull);
    vlSelf->milan_datapath__DOT__dpkt_pcm_tdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8554004855514103865ull);
    vlSelf->milan_datapath__DOT__dpkt_pcm_tready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6990875934992280186ull);
    vlSelf->milan_datapath__DOT__rend_pcm_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14431392197082314153ull);
    vlSelf->milan_datapath__DOT__route_render_sel_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11928752886124669833ull);
    vlSelf->milan_datapath__DOT__i2s_feed_chans_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17345182056777913413ull);
    vlSelf->milan_datapath__DOT__i2s_feed_lpf_act_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5820127872302925757ull);
    VL_SCOPED_RAND_RESET_W(240, vlSelf->milan_datapath__DOT__chmap_phys_w, __VscopeHash, 3677016458347152428ull);
    vlSelf->milan_datapath__DOT__chmap_phys_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1999757154879253284ull);
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__i2s_feed_mux__phys_armed_i = 0;
    vlSelf->milan_datapath__DOT__tdmr_wr_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 278285439553727445ull);
    vlSelf->milan_datapath__DOT__tdmr_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12328268894559694755ull);
    vlSelf->milan_datapath__DOT__tdmr_data_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1827069103070707090ull);
    vlSelf->milan_datapath__DOT__tdmr_tick_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12987244902608268764ull);
    vlSelf->milan_datapath__DOT__tdmr_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12521660788355992079ull);
    vlSelf->milan_datapath__DOT__chmap_tdm_dout_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5259147741834413279ull);
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_interval_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_max_frame_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_dir_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_valid_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__lwsrp__ctx_we_i = 0;
    vlSelf->milan_datapath__DOT__ctlf_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5864668315594870118ull);
    vlSelf->milan_datapath__DOT__ctlf_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10669531167879086915ull);
    vlSelf->milan_datapath__DOT__ctlg_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16656611637399614043ull);
    vlSelf->milan_datapath__DOT__ctlg_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15057780798429123857ull);
    vlSelf->milan_datapath__DOT__ctlg_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12151491910601463908ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14372429060308740682ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12742594518137470220ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11453844930191532468ull);
    vlSelf->milan_datapath__DOT__dpaaf_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9791657981304578468ull);
    vlSelf->milan_datapath__DOT__dpaaf_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13608976244297899868ull);
    vlSelf->milan_datapath__DOT__dpaaf_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3689499032805475367ull);
    vlSelf->milan_datapath__DOT__dpcrf_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2972672093548872413ull);
    vlSelf->milan_datapath__DOT__dpcrf_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3910787324050117696ull);
    vlSelf->milan_datapath__DOT__dpcrf_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1390320617332859170ull);
    vlSelf->milan_datapath__DOT__ctlg2_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8375117889216856622ull);
    vlSelf->milan_datapath__DOT__tx_mac_good_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13172510129184841958ull);
    vlSelf->milan_datapath__DOT__rx_mac_good_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9818600552637486117ull);
    vlSelf->milan_datapath__DOT__mac_events_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 6308855516434980455ull);
    vlSelf->milan_datapath__DOT__aaf_tx_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10442009229077531590ull);
    vlSelf->milan_datapath__DOT__dpkt_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 624778982836511191ull);
    vlSelf->milan_datapath__DOT__aaf_tx_inframe_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13384495303817452635ull);
    vlSelf->milan_datapath__DOT__mac_rx_inframe_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1063427539316110407ull);
    vlSelf->milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__rx_stage_p_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__g_ltap__DOT__aaf_latency_taps__tx_stage_p_i = 0;
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_ready_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11663359228919987872ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep = 0;
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast = 0;
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid = 0;
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata = 0;
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__mem[__Vi0], __VscopeHash, 13833476351785165190ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 9914423126305089713ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__mem[__Vi0], __VscopeHash, 11580895080126533304ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 2925564432082011007ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__mem[__Vi0], __VscopeHash, 2637858493282548295ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 13663228802268838521ull);
    }
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__axis_tx_rx_ts_switch_rr__DOT__state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 125873965149093636ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3676396609605244137ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9103570539468380527ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_sop = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8860760533294428356ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 848443107499170204ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11593741181615167566ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15566504375715809862ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12257960731619684439ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5808596954844714262ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3545031151054325585ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11825029948096835201ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16696512425086233092ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10257611915020644349ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12997241070679619261ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1689857920873026846ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15697248792342318451ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 124060774576873884ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__cur_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9019515551993795012ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__cur_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9924031312506396663ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__cur_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14996769700444657825ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1658801109986468385ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17017889986582237877ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_sop = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9345933390606104586ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5622538483183408152ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8762473319907885821ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 104758376815520792ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18110580789280265932ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 628478565407831347ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13533667353213074900ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1161868533387654375ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13665701641864064711ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13763274425379075792ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7425908007867552538ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13320233279060207988ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4110080652324026649ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_state = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 135617052059885929ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__cur_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8579577897802141596ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__cur_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15101506348050903370ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__cur_mt = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14663627135147532670ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13740162005777766834ull);
    VL_SCOPED_RAND_RESET_W(88, vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc, __VscopeHash, 1437404772882663993ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8714012939006528443ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__tod_snapshot_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2965648774854609564ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_meta = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7571855433146413797ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__en_sync = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4221660844294847626ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7640541358291717579ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__incr_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1357785671542715061ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6220694474674133326ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5968642265941388787ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13000440816600946138ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14854616473385256704ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16455588740428602822ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11672728581561090638ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11509327438188517428ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13671695121420236089ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_wr_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16809960782672930314ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__offset_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14293446368565600102ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1929958395354877306ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11299236641462424304ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_val_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16413825751323354164ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl_ts = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3406420840860110920ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_ret_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11860155963174409215ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_rd_reg = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6431252333815520409ull);
    vlSelf->milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__tod_rd_valid_reg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7285011935613928249ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__queue_grant = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 5272621335626611978ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 677062100657149756ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6403146390677274274ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__s_axis_tready = 0;
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__s_axis_tready = 0;
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__s_axis_tready = 0;
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__s_axis_tready = 0;
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__s_axis_tready = 0;
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 16737728633227141975ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 3584798386941986594ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2793968258078762609ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 9044642658007745406ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 16735559126090304159ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11765712611474866852ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 18010948114585022994ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 3654989671246152392ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 232885355798367730ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 11993669186165239152ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 10997805146628502793ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4759207332707972451ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 10189746058989657616ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 12309682206005902379ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10199748244962213108ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__frame_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16488225280339789880ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_early = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12432058338787637704ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_next = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15701214181496795945ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6423834960880083632ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12479253718133061439ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_temp = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6895350215854821019ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_temp_to_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14632589481847210443ull);
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent_raw[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12493023249552425811ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11696026031531223471ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__active_queue = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14304135894937475733ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__hold_grant = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16383701634686996985ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__sel_comb = 0;
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__credit = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14788877476843268050ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__idle_slope_per_cycle_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10677922094991696560ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__send_slope_per_byte_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9882667688840458394ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_cnt = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 10574341479383771137ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_idle_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2085004777360357798ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_is1g_s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7053821753019078425ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_sign = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5987097232689279072ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_num = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 18389461487180955996ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_rem = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 7710518723658096484ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6581527620177438513ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_q1 = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17262034026614422603ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 18003457931845113365ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__send_delta = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7527962963127772440ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__credit_add_idle = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15650636645864140544ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__is_transmitting = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15897191406285920339ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13266999861099918200ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__shaped = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10931006875968661569ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_ldval = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11641271775738625792ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_trial = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2383239282959237293ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_ge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6303325370651093068ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1550324074090417867ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__credit = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14290260992979422547ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__idle_slope_per_cycle_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11117091433620178141ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__send_slope_per_byte_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9452988951380439567ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_cnt = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17795216132410049625ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_idle_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9834689186209135426ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_is1g_s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16879373406637175479ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_sign = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9270055457815992178ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_num = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13673990659052930802ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_rem = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 1687178187295010939ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13082637258423548697ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_q1 = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5818368216527750521ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 2205519157493235901ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__send_delta = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16031392062947614353ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__credit_add_idle = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13119859131881687425ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__is_transmitting = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14273414387566187349ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14002623894965375898ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__shaped = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5747326035370738991ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_ldval = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3205516885186111531ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_trial = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11483878815954802883ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_ge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1964035965795957710ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 4564632305420711865ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__credit = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17578028548338709006ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__idle_slope_per_cycle_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16069550754242388450ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__send_slope_per_byte_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8409450553194536571ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_cnt = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 6550554824227634628ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_idle_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 826966556251859669ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_is1g_s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 179698194625649721ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_sign = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1396025988893710139ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_num = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8432072486617870604ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_rem = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 9074452725352224067ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11257970610086532378ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_q1 = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2877742729512483403ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 9957171553414380230ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__send_delta = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9060453130806158251ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__credit_add_idle = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17410801601001766314ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__is_transmitting = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16241050737490338430ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11183124029917413168ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__shaped = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2593259092556065319ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_ldval = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6007660901511874964ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_trial = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14096157603486628492ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_ge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11022534809079368876ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7133657803099429895ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__credit = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11822077156585705042ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__idle_slope_per_cycle_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5451568920534435103ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__send_slope_per_byte_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16098867565860990195ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_cnt = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16194566985989369903ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_idle_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3308290720467994914ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_is1g_s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5615243556391865014ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_sign = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15430950002203701931ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_num = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 4170343697778257879ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_rem = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 11335593821871711533ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11744397469880599347ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_q1 = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15300548379412416309ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 16946075832218448428ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__send_delta = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2913036746200051244ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__credit_add_idle = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5287004496604242796ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__is_transmitting = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13917207128628938393ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10152419354657582476ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__shaped = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12041406298594175866ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_ldval = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12033321499061457031ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_trial = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11207794235355996642ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_ge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4870152647413375260ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13610909622327713539ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__credit = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10451620791282015643ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__idle_slope_per_cycle_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1513215149853350938ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__send_slope_per_byte_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1155640878989750620ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_cnt = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 11769775976716656007ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_idle_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14333674598483909905ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_is1g_s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7478273774852988318ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_sign = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12815736725477700602ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_num = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5378313985330432069ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_rem = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 1128870139255081719ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16532541423928183128ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_q1 = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13465019119513313566ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 15543426088450276422ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__send_delta = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6221727959362337908ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__credit_add_idle = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6595644742933798067ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__is_transmitting = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11225183007973153717ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__queue_has_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6325036612647318021ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__shaped = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8246495361047567609ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_ldval = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16500466759119819325ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_trial = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 326474821130467637ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_ge = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15011894194444026897ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_s = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11716956074322192207ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header, __VscopeHash, 7647128130551786040ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5966829581761496313ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10841712048121941789ull);
    }
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_wr = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 896069023921119197ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_rd = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3517422172935649769ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_pushed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8582219464356216819ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__in_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13120292663894416929ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12456497149433741515ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted, __VscopeHash, 8832830399079621212ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__do_push = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14902482835312243718ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff, __VscopeHash, 4461220709079507429ull);
    vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9452888020208348253ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__mem[__Vi0], __VscopeHash, 14460576657573623727ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(73, vlSelf->milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 4889332292857888243ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__ethernet_counters__DOT__counters[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7988988791378497093ull);
    }
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT__rollover_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14981883684186643757ull);
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx_count_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12156625357770482687ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tick_1khz_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7648122128813728939ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__join_tick_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10259125738478694525ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__leaveall_tick_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9490353260302465198ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_lstn_p_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 2473727642323722908ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_tadv_p_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11225515715122990929ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_tfail_p_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8614416185925976747ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_evt_w = VL_SCOPED_RAND_RESET_Q(45, __VscopeHash, 15090932940300965105ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_par_w = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 14073884519085441610ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__e_tfail_code_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16208082104333277433ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__row_fresh_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8361228756336792276ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__row_lv_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8076561182324574580ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8308584175310857322ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14195188173502206718ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17760448326504162438ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_fastjoin_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2685249635557589007ull);
    VL_SCOPED_RAND_RESET_W(120, vlSelf->milan_datapath__DOT__lwsrp__DOT__rec_data_w, __VscopeHash, 3477714501803850710ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7545204019508885003ull);
    for (int __Vi0 = 0; __Vi0 < 15; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__gate_maxf_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8053034013133077633ull);
    }
    for (int __Vi0 = 0; __Vi0 < 15; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__gate_intv_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11220148118076842185ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8047173123340264419ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9067162880915725203ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__pdu_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1666839184979944208ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_leaveall_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15417551699189703601ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_domain_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7160085567134268580ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_domain_class = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2145463679521041781ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_domain_prio = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4318970136568336304ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_domain_vid = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4965566443392408292ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_domain_evt = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17567444721543077668ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15591172743741417289ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_evt = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6006314389976428ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_listener_decl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12234882884547262233ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_tadv_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7408256997295940304ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_tfail_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1346700250615866008ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_tfail_code = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4453295423925284933ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_tadv_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16062994927864783793ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_tfail_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10072988193822140992ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_evt = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11053025224219308240ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__w_l_tfail_code = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8210598237369166518ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT____Vcellinp__ta_registrar__enable_i = 0;
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16537071120997405572ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16060638286778896986ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxd_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16735080693350003548ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxk_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4336522775486267588ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1691064531960645601ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_l_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17448022774710335373ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6345812050913742581ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_k_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10552655056718726713ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14671382914724799208ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10891265592117503066ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__skip_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3739641268009928946ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__kind_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16543202831250095574ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_dst_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10748637237998778101ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__et_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11452066778502946659ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_mvrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1712933376075528572ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3283258066376423672ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15235737043065357597ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17127880703545330331ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_user = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18120061487517831363ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__mem[__Vi0], __VscopeHash, 15114144553008530192ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 9023949512181800678ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__lstn_leave_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8142615988231760266ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4663573562323919152ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_age_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 16401980943695729490ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__dom_class_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8016017653987457163ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__dom_match_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4123147824170808999ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__ta_leave_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 14677302074852613578ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__tf_leave_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 889270620716015478ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__ta_registrar__DOT__w_join_evt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10938053503895381033ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cur_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15159266008362455514ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cur_l_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1271402291055490471ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cur_u_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6400555381436038088ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cur_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 976172498224439324ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cur_k_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2212158171375916720ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lane_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2368714248317663312ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__byte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18419240408765082917ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lane_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16763619417954296962ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__byte_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12430553669165480532ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__frame_end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17417860459560073557ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16062634776132079394ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__hdr_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5241956611071513071ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__kind_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5257431176498568648ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lva_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4426186266535387906ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__attr_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4475292181796583676ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__attr_len_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10149633782783006261ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__vech_hi_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17788822444928255580ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 13748672851359339409ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_idx_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8992147145994132038ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5190970812213569409ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tfail_code_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11960642448913297895ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tk_vlan_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3524213200231419405ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tk_acclat_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5768515728892723783ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tk_bridge_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10196718678376040407ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_class_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16179000028863454847ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_prio_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13753995699169880188ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_vid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 146941335696587008ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__dom_a_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 71653800582478351ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__val_match_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3420064727702643726ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__k_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 13191378604550607155ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lval_match_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3866017890673645213ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lk_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 6032401700276434025ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lcap_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4736120345132648287ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ematch_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 9138835585671347370ull);
    VL_SCOPED_RAND_RESET_W(195, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ek_r, __VscopeHash, 10919670896995680283ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ecap_evt_r = VL_SCOPED_RAND_RESET_Q(45, __VscopeHash, 7878926390860858426ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ecap_par_r = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 4571398523394969660ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__vbase_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 14347831048812076628ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cap_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1120818688186517423ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cap_par_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12582190177695475133ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__pack_idx_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 5710885204354642516ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__pack_n_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 14297068878946581201ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__is_listener_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16398446179286857195ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__is_domain_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9304010646078131124ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__is_tadv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17641521215189982548ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__is_tfail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14097632996436623309ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__is_stream_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13092260219272106881ull);
    VL_SCOPED_RAND_RESET_W(65, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__sid_sub_w, __VscopeHash, 11533217637533342402ull);
    VL_SCOPED_RAND_RESET_W(65, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lsid_sub_w, __VscopeHash, 14949820140470440261ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_hit_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8332191174523100190ull);
    VL_SCOPED_RAND_RESET_W(195, vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w, __VscopeHash, 5819263132452974126ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__n_evt_q = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 11758639070456561356ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__n_par_q = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 10719177704506073007ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14292771375666635551ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q1_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15269419724612251457ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cidx_q2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16953012585980992844ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__frame_bytes_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 3973916958369621227ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__iv_bytes_r = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 15894890926942962098ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_q_r[__Vi0] = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 7055861082979120995ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9313386859298918647ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__acc_r = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 13477492540305253231ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_r = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 15895084697978790624ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__over_acc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9014932084241571822ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 7446273494258358477ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__grant_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 10295069328527107607ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_on_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 5631389333613566758ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__slope_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 7184352159835533098ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cand_w = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 2908585104299690255ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__fit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9306804547490945523ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__refuse_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17635255739394865524ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__sacc_nx_w = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 6657946845519740222ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 6692339019133084354ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 6412918653277608398ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__hold_r[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17275050182662140338ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__enable_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 970368909272506113ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14364928461327896813ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__msrp_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12987254184519021819ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__mvrp_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16929773018119103368ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__jdiv_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 608088663490451707ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_lv_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9551255606072271975ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_lv_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7292812304218396742ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__engine_lv_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10366541959228781789ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10313972697803557352ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_domain_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10346147046048157944ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_vid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16621380978322464458ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_talker_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8797292623089451773ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__fresh_lstn_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5144283314448962177ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18040891640763270329ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_ready_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13548814251948801213ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11212309140163433419ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__gap_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 1546514443620256891ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14069925050774073159ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10887235095705816141ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13515155313127855015ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4417389948542936845ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16155875910301562423ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6621801935995522704ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16492985324868526769ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16108624638524765260ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 768588550654612517ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17849768094825109060ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7860694659019044019ull);
    for (int __Vi0 = 0; __Vi0 < 88; ++__Vi0) {
        vlSelf->milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4178013817652221776ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__t_mask_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12473118398278685161ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__l_mask_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6402512998797649858ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 9607788983086829939ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nt_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3968727771927920480ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nl_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3539735961975674326ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_len_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8129959993638722034ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__incl_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12124979513569021634ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11546005767205678110ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15536866341893000772ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9399886516576366961ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6722841341546906317ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__loaded_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 695239408152745443ull);
    VL_SCOPED_RAND_RESET_W(120, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r, __VscopeHash, 3533731477409651487ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__fb_cnt_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 4152984800439939994ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__beat_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11693965949063637427ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__bidx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16708772743939040421ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9610725834526569775ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__gap_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14213382006471396534ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8003524981089680090ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16039062671769408253ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__frame_end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 48703906764153740ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6075610169248538360ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12787839143954954442ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__onwire_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 17070752914473187825ull);
    VL_SCOPED_RAND_RESET_W(960, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r, __VscopeHash, 16782555371901358772ull);
    for (int __Vi0 = 0; __Vi0 < 15; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(120, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rec_ram_r[__Vi0], __VscopeHash, 12610173440736770799ull);
    }
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__svc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11052162854110936043ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 5030023023535122443ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__afail_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 8834827977458857477ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 11337959418002317908ull);
    VL_SCOPED_RAND_RESET_W(120, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__acode_r, __VscopeHash, 6834034947436999692ull);
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rleave_r, __VscopeHash, 14565817874519498138ull);
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__fleave_r, __VscopeHash, 15362023741779584462ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 4145271688095303605ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jn_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14092912328005314425ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__in_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 4513787810310794537ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__lv_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 9318097389001086615ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__jdiv_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6486926530240463399ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__refresh_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5806598347611623611ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__ready_q_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 5901658576006012856ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8455601584325295302ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__timers__DOT__ms_ctr_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 17607474014444929098ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__timers__DOT__join_ctr_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11424072962088811436ull);
    vlSelf->milan_datapath__DOT__lwsrp__DOT__timers__DOT__la_ctr_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 16451517410420155909ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__ig_to_val_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4865270848045639436ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__ig_to_val_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8134412315570334214ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__val_to_par_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3530332078782922712ull);
    VL_SCOPED_RAND_RESET_W(230, vlSelf->milan_datapath__DOT__aecp_listener__DOT__hdr_w, __VscopeHash, 6749934962765990788ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__mismatch_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15821877120722831926ull);
    VL_SCOPED_RAND_RESET_W(210, vlSelf->milan_datapath__DOT__aecp_listener__DOT__l0_state_w, __VscopeHash, 8777950508057480151ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__val_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11525674332681599172ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__val_drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7266053415200620166ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__val_msgtype_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17589126607945681288ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__tick_1khz_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7046990555857958300ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__req_src_mac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3477353775394687450ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__req_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2224413078276917903ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__req_pop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15268924137445088527ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_raddr_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4766432695511842113ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_waddr_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3384650141360256802ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9151492992038849291ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_wdata_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8852413759908996921ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_rom_byte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16222215745040022840ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5711114982462151839ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__st_raddr_d1 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15586348711403881267ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__pres_wr_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1081830220771427733ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__pres_wr_val_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12945251460821552863ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__pres_offset_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7756910674080700550ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__evt_cmd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3459420998782218353ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__evt_resp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8557145010613564896ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__cmd_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6188327213278226213ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__resp_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12805567469121028221ull);
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11018402770038980939ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 72274086505516733ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw1_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8168867190669728012ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw3_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5135818446978825534ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 4423955339258067268ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__nochg_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9536310954491667215ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__state_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14696924980932876320ull);
    VL_SCOPED_RAND_RESET_W(230, vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q, __VscopeHash, 2468638414061231670ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_status_q = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8250195390257694214ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_reject_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2041439018909869727ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__discard_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8148724503025656416ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__vu_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12354666446246146998ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_cmd_eff = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 13547209286053388313ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_si_flags = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13950245781768657771ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_set_fmt = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11698836658779258326ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__acc_found = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7771779293387772214ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__acc_base = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16784872649451858836ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__acc_len = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17894937834696197435ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_name_ptr = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 15647126962721981555ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_in_fidx = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10345790080993620144ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_in_ref_fmt = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15257832652753571944ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_si_is_stream = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1647831403775266200ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_in_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2905859010011643282ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_out_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6811407643154273505ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_pi_in = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16953814508807406181ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_pi_out = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4326197983435797398ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_rows = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16607773832138944172ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_milan_ns = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15678902504680872716ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_has = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7876015151353044859ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_badidx = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15604472837583468993ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12484197675839030898ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3257905547408352206ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17410348558049014022ull);
    }
    for (int __Vi0 = 0; __Vi0 < 96; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__const_q[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16947766364756135555ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cdl_q = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 6550199021539156969ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__status_q = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1033160041701892195ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__msg_resp_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10663099628988938245ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__dst_mac_q = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10795622698612588930ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16027721136881259614ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_ph_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15617365995779789352ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_acc_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8299603021242331600ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pay_len_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6747537642009393170ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_done_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14466856557724122767ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_addr_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3375775613198862953ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_len_q = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 4271119728002388897ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_src_q = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 3074158065976926638ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_cnt_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 1967258310408187447ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wbp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7433132440693584832ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_used_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16761131029173266687ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_diff_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 613670163797766823ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__batch_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8661840976386679423ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsub_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7900142381493111000ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bscan_ptr_q = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3591846070330412053ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bscan_ph_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 654265774057788390ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsc_lo_q = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9126581921811645292ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bslh_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15120557911254926536ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsch_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16244863711465008874ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bcdl_acc_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2088495963673986211ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bfit_map_q = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7433547802831704698ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bidx_q = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4866560077938225803ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bpay_end_q = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 5653791146043189375ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ptr_q = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3527929883958244445ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ph_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6779326378416368384ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_cmd_q = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 4029090339710046573ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_dlen_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14229759087848199862ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_rlen_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15760558001562333459ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_base_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15563219650568481074ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_abase_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3683366690009618953ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11660228614938262137ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bh_i_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17575791953644553130ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bcdl_q = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 1008868627804403403ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cap_done_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3539324868474547885ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg0_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4322039823759079402ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg1_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14345881714669441155ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bdbg2_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15310380223551544863ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cwld_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14529162466422400184ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_raddr = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 7151448069397695266ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_rbyte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15269546397723127525ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_bscan_c = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 16467629701080668720ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_bscan_rl = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9725368444138446033ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_brec_rl = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16874956060437345951ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_hdr_len = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17189309792109556257ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_frame_len = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3996963920788962658ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fi_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10751282960520661603ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_seg = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2971347635378919679ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_soff = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8613451118530520223ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_wb_read = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1060247719532878767ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11652253537592832937ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_n_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16997860174113430959ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3009651263780888120ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7899013785296120832ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_keep_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11347755484297274777ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__is_hdr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13835435624595546644ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdrbyte_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13911622144479097599ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__emseg_kind_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15941960950963495615ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__emseg_addr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10975472652838842693ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__emsoff_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11584883333556471840ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pop_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10270487337823310075ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__identify_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6666528757881180930ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__sysuid_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5841530680383448814ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__mcr_user_prio_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10651960207873023439ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkup_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9160997504844300364ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkdn_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10932912249700572937ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_gmchg_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12763396266817414416ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__link_prev_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12950667940114703146ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__gm_prev_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8223953675678055140ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fmt_in0_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1761518216553954431ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__clk_src_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 298459125954174418ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_dirty_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2975580488648198248ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_rl_ms_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 4953206175432801949ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11604699183203976477ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_eid_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8056453555101237381ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_mac_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17892533036322754478ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10845933772856015250ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8455161511390850112ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5766344301337122519ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend3_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8743857011658803447ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend4_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10615470321702708689ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_frame_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8910267743487906221ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__ta_prev_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14151343876927460892ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__lo_prev_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12571641423512242942ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_match = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3065317148547236301ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_fill_idx = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8176390895115453428ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_push_idx = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3257535249542322172ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_push2_idx = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4033622279114235456ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_push3_idx = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 523204622280623798ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_unsol_push4_idx = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5164180187461745089ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__started_in_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 721674006810872569ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unnamedblk16__DOT__k = 0;
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3714434160796767205ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6734475085553686816ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxd_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16151775775167285203ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rxk_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3345021396044525954ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__wbeat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13109313603363085614ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__pushing_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11141923942399038356ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__drop_rest_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12976650719749396600ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__kill_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8859988848042391949ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__dst_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17860007260135883445ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__subtype_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7157008447699285690ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__msgtype_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1454211795840047308ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__is_avtp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1897344055097710215ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__tgt_hi_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5911428296352822126ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__adp_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14468374783910966627ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_b1_avtp = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6820856030703070720ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__fw_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12147974362547056772ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__fw_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1209573249338414303ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__fw_user = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7292599076411363591ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11813231116775555639ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14982752235923819686ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11214150575352620342ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7887859405519799049ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__src_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9017733941870452497ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14194944331330933443ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__mem[__Vi0], __VscopeHash, 11474918676576472088ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 4663017731416587217ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9118999214351867ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_clock_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3485215858609656867ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12209187803106094534ull);
    for (int __Vi0 = 0; __Vi0 < 23777; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_store__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9479301171994806897ull);
    }
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1624405164354511010ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15217578813380878059ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__lock_timer_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 6711777064136862164ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5135356974705600765ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__w_block_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14423447366989805629ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__w_lock_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 268323606908140109ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__w_bad_config = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3353141303658376490ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__state_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 161910758838027198ull);
    VL_SCOPED_RAND_RESET_W(230, vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__hdr_r, __VscopeHash, 9498104733878312846ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__w_hs = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13581440904266899180ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4489782208080055779ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3408064663686136394ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__s_tready_l = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13886520526285102620ull);
    vlSelf->milan_datapath__DOT__aecp_listener__DOT__u_timers__DOT__ms_ctr_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 235209449728710009ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1199367844541895023ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10525660526044815813ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9765631063469914319ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17220224632502900057ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9984591259429571592ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 6367591780856805063ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4015928105186370163ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15626538650372458635ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13247234318528579280ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14575243297029245807ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5717366874026349944ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 297334776200572226ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 12899305383254223625ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 10345082901790545033ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 7461485207038989896ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14701217712712923670ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 721190254482443778ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7794214198742978928ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 14549205714899318864ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7720020888755070673ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11562345301486076182ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10993484480241482404ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16264217931063933185ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1346890366976414338ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14526895245696190763ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6811775163955888517ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8640671458113247037ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6863495994505845597ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15970572415030042247ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wr_n_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2434175711617030479ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10827797995250520728ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9869767004989633528ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5765597695171486388ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17140762555644307664ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13446133948111077384ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7851982691073516608ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 755125253113134100ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5141898114419003584ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17675006794609586613ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_frame_a_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9097434007545026377ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1592337628700772438ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7915059837949334438ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8412296246686189179ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_meta_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12198055048420856788ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_sync_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3907700736420722308ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_meta_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4738738567499543276ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_sync_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 50283463061671655ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4158626396930396270ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16607369193527480790ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6622571710003288768ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17481025007313027037ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11610797580783187703ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3461850140231179378ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1789632774265781463ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8156513846963390685ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 903452659236422217ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r1_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4644718734027076255ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r2_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 543060870551218166ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17090397731848891693ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13985841412882431879ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6273939600865911900ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16661469293255464872ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11619779898570861359ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6941531551319956634ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8545647611478462754ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__locked_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1745837030565256401ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15419504392202772199ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14736950254529441852ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3250579978994282202ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7542390822911592473ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__state_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8001903630719396085ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__dstate_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4091947002557018570ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 11111978174438365363ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_start_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13551802875299335538ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12175314228100954804ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_skip_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14384010732966366789ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ew_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11627751675869233751ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_run_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17785202736916315017ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_cnt_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12495334039247330377ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__integ_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10246020060512661598ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_cmd_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11461358087524829170ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__lock_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15038513309621532791ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_seq_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3397084741920954052ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_run_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11781225111205515651ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18172854647922590050ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_spann_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12056569907774400204ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_locerr_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5520118000190301118ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_rate_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12310750090942566639ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_isum_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13531924972631513995ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_thr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3930500975056992225ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_ig_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9911360701222082956ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_un_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14674169965380148901ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_ut_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 709789492214545154ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_du_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12089670643531878355ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_gain_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13954565267405244904ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14800197632174590781ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_send_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10343533513370093637ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_data_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11832398884529052294ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_hold_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6088439436423558861ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 590727073402988909ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_second_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2620301314913987821ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__repairing_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15140463147160262748ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_val_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7449765302757099402ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__verified_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10247491543183279472ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__mismatch_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 490695811978306810ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_fault_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1072024958454834311ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__relock_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 7751707712390928800ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rst_settle_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12598973018361002124ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__exp_val_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10113062304904127254ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__exp_mask_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18175128700945335004ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ptp_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15418384730948276261ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10485604773314952935ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14885225624640812176ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 5270052906721326930ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7318462042179430439ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 117574268076146972ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 3705898732959895901ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16253272370252323768ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12737230810038219004ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9790965214494575254ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__src_send_d = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2517125027075489853ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7101727235483008596ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__data_hold = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 10323698129609927802ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18336191858756470361ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15315447054756657750ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_out_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 13820377244584414907ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4580948918296233594ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3632286756775668184ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3091492968299740922ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15300035259290159099ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6266469597484012055ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6243220253051098481ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2270741442939387784ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8329299471340960092ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2056240750540354644ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5568086125856953443ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18351354645706085996ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7100249991306488364ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6286961003208127014ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7701619647540268985ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7439539410802103604ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9782101185124163941ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11437823046893370281ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7114029900706214493ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17096782294864692786ull);
    vlSelf->milan_datapath__DOT__aaf_final_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12765438448512317610ull);
    vlSelf->milan_datapath__DOT__maap_ctl_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5211102162721373796ull);
    vlSelf->milan_datapath__DOT__maap_ctl_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9797526016106493676ull);
    vlSelf->milan_datapath__DOT__maap_ctl_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4832524414678303317ull);
    vlSelf->milan_datapath__DOT__maap_ctl_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7253043438527589429ull);
    vlSelf->milan_datapath__DOT__maap_ctl_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1951954717872647228ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4815025700480575111ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8987402998069865865ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11654996843427477025ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6211517217674342187ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14125169468013899236ull);
    vlSelf->milan_datapath__DOT__lstn_ctl_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10749631496120935081ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8530703332388534275ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 499902486268260759ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12800854381927060464ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6332956348153935333ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1767794266458840888ull);
    vlSelf->milan_datapath__DOT__srp_ctl_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9914348830059441519ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3610326048497818135ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13184962848309969206ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5550739806543779914ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17745417963012150095ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8329326523292947328ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12885865259239512308ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9527775798586372144ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8887304342636538623ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13422739609038153781ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1537031116251191691ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18098111086208080022ull);
    vlSelf->milan_datapath__DOT__aecp_acmp_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13260651693846185707ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8999682421569456673ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4845474252695617536ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13316604820235534526ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4296525945032586500ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2394613515968002929ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17658702619394923769ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10105195447828329145ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14101907015455959805ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15492852327889388884ull);
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15241391179595562276ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8991065796671773981ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2977742342598283333ull);
    }
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8518592359819562464ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13225328205034623004ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7514143673796468161ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11410300957276403036ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8440371116942964842ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9124457214038440919ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18259043154334295379ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 830604151673692243ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16952249663792952013ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16976400244371404462ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2488768413801506322ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3489178009994638489ull);
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3995902407128096139ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5631320453847156990ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12957914967490242200ull);
    }
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9044825234529125018ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1355620477585546534ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17536462827761623709ull);
    vlSelf->milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 593163490559558659ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__arst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4702644607541866548ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__adiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13973974788862635897ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 5324145493602299683ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__aevt_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7145376842551796687ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__ts_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1152980841155199512ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__seq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16085790371680289529ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__frame_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17587723922996360482ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__tu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9055541482634606299ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vln_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2899678594131139957ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vpcp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2191961353266714310ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vvid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3924147351671677240ull);
    for (int __Vi0 = 0; __Vi0 < 28; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_tx__DOT__pdu[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11444048398030434914ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_tx__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3616455940315271579ull);
    }
    vlSelf->milan_datapath__DOT__crf_tx__DOT__st_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14284557797424822327ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15700616228807514895ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14022875488956122426ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9616987612383374399ull);
    vlSelf->milan_datapath__DOT__zf_tick_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 548858884099513199ull);
    vlSelf->milan_datapath__DOT__zf_tick_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4131885674473170281ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17766125145139645198ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__in_frame = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7847582356564656787ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15346095915984653831ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11829716660200141772ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_sof = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9653446831909198493ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_now = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11983283202532701456ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1672423968018691440ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7528741892787638466ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2299591252912849714ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10954790848561287945ull);
    }
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2769185763766042543ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9667804316940675262ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__arst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2476774103094919210ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__mdiv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2498111400521418307ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__phase_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14677108831371684124ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bclk_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15629013256241097039ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__tick_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4535441637243028784ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__brise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2753588130507526996ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fpos_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 7556051697070904848ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__fsync_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13914011113093767510ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__startp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8234767015817872301ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__bit_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16765294128626492466ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__slot_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8045194235368337808ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__shift_r = VL_SCOPED_RAND_RESET_I(31, __VscopeHash, 13563618792863695310ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__lhold_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11079988422540953172ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_wen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4039308669486392913ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_slot_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11385832974164288155ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_l_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 544476447420635881ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_r_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10756387081609875301ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_full_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13084175364650881222ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__eslot_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1281886368397213886ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__ebit_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 18233559848855745759ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_rempty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18273768971909368790ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w = VL_SCOPED_RAND_RESET_Q(52, __VscopeHash, 2987941642775941216ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16078310913061559365ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(52, __VscopeHash, 16542080081132346347ull);
    }
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2344280523340294177ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5819905194656516042ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1131790106642446810ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16446909882011001623ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w1_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7693130009211789205ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14790224934314482416ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10746217289787412819ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15438456500732634718ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18331291914471643890ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12143035625734330881ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11912461101428257688ull);
    vlSelf->milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15647144368498708572ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__bank_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13625269170046689675ull);
    }
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__wfull_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15940975368766291144ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__fifo_wen_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17833909581515889305ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__brst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4874935043901674567ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__rdata_w, __VscopeHash, 17158468738600464191ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__rempty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4649409116376869587ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__ren_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1380178800800447332ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__fsync_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7864825791457213044ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7361047106123505463ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__run_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8572694288783440035ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5239344393370599858ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__bit_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15756900920005737616ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__active_r, __VscopeHash, 11277154609594219791ull);
    VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__next_r, __VscopeHash, 1697612860319691078ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__have_next_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17210852746296671922ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__fetch_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 845033205618024692ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__dout_nxt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4059295829034719279ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__unders_b_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18120356598605882647ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__start_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15525773445931326537ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__eslot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15570263359528175491ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__ebit_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3376004242118925817ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 856115651153563360ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(192, vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__mem_r[__Vi0], __VscopeHash, 17215515843973782411ull);
    }
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3082616713379640361ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_gray_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13314110389986526147ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rptr_bin_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3780216825797219834ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rptr_gray_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2305196034497673817ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rgray_w1_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1610921934608171031ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rgray_w2_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12582724087059348996ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wgray_r1_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17860882500688069431ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wgray_r2_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1201005956974050528ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_n = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12261237100805096896ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_gray_n = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17611247854708599124ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rptr_bin_n = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14150177531384916119ull);
    vlSelf->milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rptr_gray_n = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18433285899644714958ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__good_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17256738131828586164ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__in_frame_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13310215683799157150ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__wv_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4150956771800167844ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13057375267745762422ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5752005312799155981ull);
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3784084933833027858ull);
    }
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5577644233173959075ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17074462168683259374ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5837267000956981274ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17315250115472460349ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5271510841197838407ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17432527769314052164ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3648689227113557827ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17177073758092427431ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12838129666757485292ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14675545324066737725ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__Vi0], __VscopeHash, 14837388420136471902ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 14183867525397544016ull);
    }
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15845664245727519107ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 10010499279283708786ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tick_1ms_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9221488872205071591ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__lfsr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2731952579026339856ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram[__Vi0], __VscopeHash, 1984352793179959838ull);
    }
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10931156030921560157ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14020775189607979967ull);
    VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w, __VscopeHash, 10829509579118500302ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 786378820945343121ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9356987161280799003ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3102286497589825572ull);
    VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r, __VscopeHash, 5685259657107216302ull);
    VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view1_r, __VscopeHash, 9545479692709419509ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__active_vec_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 2451725301295809543ull);
    VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r, __VscopeHash, 9598908124854805256ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10339191402993933603ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 15113541515501883791ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8267732725210626349ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 526490118148984561ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14748309033953424839ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxd_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14438752803350478485ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxk_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16781500874957962217ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_classify_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11229621532745080409ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_fc_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15662549937358247317ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_flags_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18083828212893758611ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__dbg_basehit_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8656907106350554199ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__txwd_r = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 14687043112870626933ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1095383770539853161ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__fword_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10376010516151495034ull);
    }
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wbeat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9572943479569841098ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ovfl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8811353231333401297ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__len_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13507604906997868626ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_len_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3062731861908560001ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_cap_hs = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 308170531539839573ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dst_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 422080731502530401ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_etype_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17548528601271851219ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sv0_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16466978542463807744ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_subtype_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2945672020245007509ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9973965678799118391ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9621224303366757551ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16620111078855187592ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5101527199915639998ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11008902525068063147ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_hi_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6029955731987743878ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_lstnr_lo_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1706405570943450383ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16370010846673574408ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2802143054507110094ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7087713596791014371ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16897673782874715975ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_vlan_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 15571506162808483115ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstnr_us = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14781214047010076044ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_acmp_base = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13168402638480572558ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_is_lstn_cmd = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12962210486352574437ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstn_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18096292685137343346ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_luid_idx = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9888974738667064824ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_sm_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1376623894701512825ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_seen = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12063208957592052165ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_same_talker = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13864170971967099722ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_flags_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16620908065085740249ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6608157744620320804ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13527955434198715285ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16455097300446598194ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 369933550771093732ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11790055023068911039ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5060886463287816613ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10235015708477170732ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp_flags = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5961144094085196672ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4725018192891134594ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10569386071835141970ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 575767074496385999ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16163439508323780529ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_ms_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11749551870517290231ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_1s_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9019683522074175675ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__c_adp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17563623896006865869ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ms_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 251523847531490802ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__s1_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9929224106821941418ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 861198570956242730ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1232318915234403687ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__adp_avail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11371915893637704986ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_reg_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16410537949546026184ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__srv_fail_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12900126364633418392ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_adp_now = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3785399056365895406ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4755539052005687001ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18274611553817593415ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_sm_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11627146992898510274ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_pend = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18415769056669375477ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5260021259874120862ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_tbl_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9580196724373367474ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_set_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12398861199272936151ull);
    VL_SCOPED_RAND_RESET_W(317, vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w, __VscopeHash, 5057340673535907649ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13171248121493960070ull);
    vlSelf->milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_probe_set_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6349938738437212121ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11172897067832704629ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 7989728970043931816ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9957547606533263147ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 542284071629328248ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14797330970465308157ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2153993046585768995ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10226546362500914175ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12496182149945137001ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13499019565274589756ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13075844088637485733ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2752225614203899989ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16713906991442137837ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14493160851013244918ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1307663788517071716ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9410149733716856998ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13251545266174315522ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3303454394569907374ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1301079848489047426ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2953908247814018391ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9525233757058620095ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 188553316597498730ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__new_off_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14229856282866922033ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1118566636771447440ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3246833815323396871ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13679864809238892990ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16094534049219825673ull);
    }
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3660679493284897835ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11973415886751816670ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5457512508907291301ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10139425757867947312ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1079358788619364180ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 6520039323234183374ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12192183913575894170ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 7069381669913313442ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8388374678210131653ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1085759031476937101ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17153594281558486633ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12030792037895771617ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12740560322218139144ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10781146018636517692ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3538385279785576067ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15573492843812070809ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = VL_SCOPED_RAND_RESET_Q(44, __VscopeHash, 669251602262134178ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8936756660401357148ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16089405510922980905ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w = VL_SCOPED_RAND_RESET_Q(41, __VscopeHash, 4827794215717381555ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17965522183166064131ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__gap_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3037197690939959602ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__gapping_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7164260530689217802ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14955978692144943468ull);
    vlSelf->milan_datapath__DOT__i2s_feed_mux__DOT__feed_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7714488854052722483ull);
    for (int __Vi0 = 0; __Vi0 < 10; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10053316931249481898ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__chpos_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7320026279811759778ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__eff_chans_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15006563009121935262ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__ch1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2563287964740149090ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 8; ++__Vi1) {
            vlSelf->milan_datapath__DOT__chan_map_render__DOT__cur_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15950518565320158182ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_render__DOT__pbcur_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17468586608678324862ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9373002482229372779ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_seed_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10301703137156937570ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w0_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1629980290258838214ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w1_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17035684146502086057ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w0_addr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7051236067688470580ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w1_addr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17449599142789915687ull);
    for (int __Vi0 = 0; __Vi0 < 10; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_render__DOT__sel_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14519706626061297722ull);
    }
    vlSelf->milan_datapath__DOT__pcm_route__DOT__render_active_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18419991141951143258ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pcm_route__DOT__route_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8984510757036864958ull);
    }
    vlSelf->milan_datapath__DOT__pcm_route__DOT__cur_route_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6427837285810774723ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14622065670122390313ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[__Vi0], __VscopeHash, 15430697001142611947ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17362706939262636967ull);
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r, __VscopeHash, 15685297020129853347ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2087811172068529944ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2792570892404568599ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13060468068515878231ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9909333545390814525ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8811581609622783574ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1269870397131517630ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10083612483744281916ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5437361188095732188ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7497901483064090341ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3854555034230141215ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5997824553514827741ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9023262490013526047ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__mr_add_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6329395683025500099ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11712287505304448284ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8862104144150537527ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__servo_pend_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 186274693691894156ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15187390846301837804ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11662891475857227249ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6234798159294592240ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1865214815742977915ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12931490876469748808ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[__Vi0] = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17755078034659646192ull);
    }
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7916785597338757399ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15653809701594851254ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 395929483942599856ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3975439784211546110ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12286988643141797428ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15157742014147402989ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 3021355262171967498ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12146398033882798152ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7982733701408713830ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5493015344807664390ull);
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w, __VscopeHash, 518361002865256527ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2908356655003156678ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8115096178605422038ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3456729606547324877ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15042857255433237123ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2636221605792140609ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5860425179636536049ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__lock_now_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14135952977749081709ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8447802588018996438ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14094376045547682629ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13328925474830464260ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6579028671195353711ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5827093552888003154ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5004036784858595221ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__leg_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3915359615882650407ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 10; ++__Vi1) {
            vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9729056219764228362ull);
        }
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_ridx_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11842843849640638883ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13236602052094429364ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_fmt_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10522875603045515651ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_crf_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11379143846798012241ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_rx__DOT__ts_hist_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5751950040872497243ull);
    }
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hist_old_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2126901756118269505ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__ts_new_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10365913307368472954ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__rate_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15213768936097733128ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hidx_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8347445078272008613ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hfill_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12685665967167196181ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__exp_seq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11736501980353030304ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__have_seq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9427441939956363762ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__settle_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15735112532841544741ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__tout_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11400314798336086975ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14028052261861268074ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tdata_q = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12123540848625841582ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tvalid_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2205722405258801641ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tready_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16601842273036230406ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tlast_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11490017988269911512ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__beat_be = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7415454402184239744ull);
    VL_SCOPED_RAND_RESET_W(448, vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__hdr, __VscopeHash, 7631136129642521852ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16871129492222051209ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__in_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2998594054211217415ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__parsed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14369799751640003813ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__et_off = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3543618249937577763ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__subtype = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2877338005700665167ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__sid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7369480024387029132ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15647204075577153630ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12069146240932430484ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6174796174499732474ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_sid_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5836600025842032663ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_en_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8610899206661485935ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_armed_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5278153249296783299ull);
    }
    vlSelf->milan_datapath__DOT__stream_table__DOT__en_q_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11498123079812195256ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__rxv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 611533100172507869ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__rxl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2445501570441758836ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__rxd_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17224443024047702432ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__rxk_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3946921347122323957ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4393958905148037732ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__acmp_responder__DOT__fword_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15468777088171840328ull);
    }
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__wbeat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14844567867479495195ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__ovfl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5330490267897945181ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__len_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11704693496415238896ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_cap_hs = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5903638380663555862ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__dst_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11717129270667732402ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__hdr_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8175690745271981265ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2318919333840938009ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__tk_hi_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17461582309819459802ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__tk_lo_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9986527136401971034ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__tuid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14244430273444113954ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3784369633200957634ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_uid_idx = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17305989638790940856ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__resp_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10733075170904387666ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__resp_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13117544572475392398ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__resp_mode_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7629733035834166874ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__flag_clr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8021055110140868576ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__live_dmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7276634099782742457ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__live_vid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 9813751874831549973ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__acmp_responder__DOT__tmr_ram[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11526495902666452925ull);
    }
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__tmr_wr_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14375270411065380845ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__tmr_rd_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16408164320893355480ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__swp_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2350815453055548076ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__swp_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7959930870416353168ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__s1_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9449250479820096132ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_arm_wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5330421435669770580ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_swp_run = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5990262739759769419ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15278786395095511362ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__rword_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5893376681427021834ull);
    vlSelf->milan_datapath__DOT__acmp_responder__DOT__w_beat = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8532025559370902817ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(27, __VscopeHash, 7170498985484180712ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__tick_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5855683744885085915ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__start_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8537183809594744008ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__stop_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15466657672989210874ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__mreset_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5816501462738206896ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__tuiv_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8643799597278655667ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__ftx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12152206246454849272ull);
    }
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_f_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 17549255226952657454ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_tu_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16916263998414430998ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_mr_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 17281777268225639028ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__strm_q_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16842806567351608481ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__ridx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2078712402106711788ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__available_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17265065363264681874ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__send_pending_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5040566211666396094ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__pend_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9911390000877940968ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__adv_tick_cnt_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4144874433866924817ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__disc_lfsr_r = VL_SCOPED_RAND_RESET_I(26, __VscopeHash, 11513148853297500127ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__disc_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3781451512156333162ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__disc_dly_r = VL_SCOPED_RAND_RESET_I(28, __VscopeHash, 7351494739344564440ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__tmr_advertise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3192385628157218058ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1505471053713064678ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 988646426638809468ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__tx_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9771695145998133005ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__tx_index_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4379762264227059487ull);
    for (int __Vi0 = 0; __Vi0 < 88; ++__Vi0) {
        vlSelf->milan_datapath__DOT__adp_adv__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8682672431171194757ull);
    }
    vlSelf->milan_datapath__DOT__adp_adv__DOT__rearm_tick_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13653687277820127370ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__rearm_fire_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14502009227958761874ull);
    vlSelf->milan_datapath__DOT__adp_adv__DOT__depart_evt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12216853982585975017ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15916183860178299118ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7071941923478831061ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__act_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12671872054067894333ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__man_reinit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15084789911786723802ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_trans_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16495505893704889792ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_trans_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17606571613770347269ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_dead_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 12943586142425463810ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_dead_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 10454050727543716532ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_alive_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2995488038637301601ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_alive_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4451929964332348361ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5334664624194689024ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 684872722566134824ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__act_age_r = VL_SCOPED_RAND_RESET_I(27, __VscopeHash, 2226991931239606812ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13359297620767161239ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__settle_r = VL_SCOPED_RAND_RESET_I(22, __VscopeHash, 13435235668080576870ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__bounce_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 402627201830618389ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__guard_rst_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2178403524073781789ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__eth_rst_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17142633955302803513ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__bounced_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1227313587859577751ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__both_alive_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13294933488369916783ull);
    vlSelf->milan_datapath__DOT__csr__DOT__b_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13714494621205693037ull);
    vlSelf->milan_datapath__DOT__csr__DOT__r_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10503574739617361174ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_pend = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14490135098466730862ull);
    vlSelf->milan_datapath__DOT__csr__DOT__r_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12322062386511221102ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_addr_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6595945997244090344ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_busy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1838070856009293287ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_cnt = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 2597626500227431288ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_is_slow_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15844231368139016641ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15632904727200795000ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2576900481489799569ull);
    vlSelf->milan_datapath__DOT__csr__DOT__irq_mask = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2376295935016826797ull);
    vlSelf->milan_datapath__DOT__csr__DOT__irq_status = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11505584028027618962ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17018259252392059163ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ifg = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15121606105290994221ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_alo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18288736837750982907ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ahi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 782746863443379205ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mc_lo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5831616978633483419ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mc_hi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 238490697787957232ull);
    vlSelf->milan_datapath__DOT__csr__DOT__phy_rst = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 809839818496205232ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cls_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9821296827944453400ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cls_dpcp = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1793090881185418392ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cls_map = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17775171415704190378ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cls_regen = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7287260936759983007ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cls_tcq = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1086990576307349979ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7159777413653490169ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_incr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8207339968338810145ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_adj = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3312056880301096159ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_twlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4730099932413380500ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_twhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12601456620279226798ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_oflo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11555497851140061087ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_ofhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 138357968536966172ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_ilat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4536522702413773369ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_elat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4333278202560506795ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_tod_rd = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9518998572414028519ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__stat_snap[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12350890656454470542ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__cbs_idle[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14278568143375227651ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__cbs_hi[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11685685825709529937ull);
    }
    for (int __Vi0 = 0; __Vi0 < 5; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__cbs_lo[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3235813423337147794ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__cbs_en = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7638473253352739297ull);
    vlSelf->milan_datapath__DOT__csr__DOT__stats_rst_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10017351510739428585ull);
    vlSelf->milan_datapath__DOT__csr__DOT__i2spb_clru_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16683129708530402759ull);
    vlSelf->milan_datapath__DOT__csr__DOT__i2spb_clro_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13518283653898073113ull);
    vlSelf->milan_datapath__DOT__csr__DOT__clkv_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14198976612086101686ull);
    vlSelf->milan_datapath__DOT__csr__DOT__clkv_wr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1062208003209822022ull);
    vlSelf->milan_datapath__DOT__csr__DOT__clkv_disc_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1489309376698260266ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_load_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17937085731260552793ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_adj_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2650445069227214791ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_snap_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6053579945606747085ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8759610603064104929ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17912260040090226521ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_dmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4328653323409169554ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_dmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2267395976655123260ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_lobs = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10635196965850591178ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5759742362018291521ull);
    vlSelf->milan_datapath__DOT__csr__DOT__maap_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11309480783826895116ull);
    vlSelf->milan_datapath__DOT__csr__DOT__link_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17230803420400324052ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ent_name_lo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3945393222788876144ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ent_name_hi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17903895162374595361ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lpf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13320599515544578254ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4236181310976816398ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_sidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17348827527673671810ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_sidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17064190797701331552ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4269561266067534930ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_sidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14398692195160633906ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_sidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1401393356969275147ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_dmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14723331479705173299ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_dmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 508046437882537176ull);
    vlSelf->milan_datapath__DOT__csr__DOT__as2_lo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12162146439031554693ull);
    vlSelf->milan_datapath__DOT__csr__DOT__as2_hi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4193149877199672720ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tone_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18194934328590750685ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mcsrv_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14319602854640694512ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ltap_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14901849583261391137ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ltap_clr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1099971044474508918ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15814317113089025199ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_sel = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 289893510951932791ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_word = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12064112562497560825ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_commits = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6590000247914501319ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_refused = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 786551900314066785ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_wr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10452850805249207062ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1647126954436129995ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_flush_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7401261008494427915ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9350041551297280223ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_to_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1771175108087247947ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_unsup_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16605521671389585891ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12522474273616277630ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_side_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11963740656349791237ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_addr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7879796706432343072ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_data_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17748678681380318329ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_wd_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17809964285985748875ull);
    vlSelf->milan_datapath__DOT__csr__DOT__gptp_pdelay = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6957385573391964496ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_vid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10009375411199016705ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_dmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6296725393726618650ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_dmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15271029105095848848ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_tspec = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2760202365565388229ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_lat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15207630477840778715ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_eidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10964907143668503054ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_eidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4151186418388875646ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_midlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8662002850644773694ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_midhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4966851519894731815ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_ecaps = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17384281455577255449ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_ccaps = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17376643863563358155ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_gmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6573149472347519262ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_gmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6337733469446186178ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_domain = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17056869285216777368ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_idx0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10638228031971173045ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_idx1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3529350234587612731ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_aslo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8782630362057336208ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_ashi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16847673663606879803ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_adv_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3373897657170827778ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_dep_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17995345689920372659ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5605924520227998396ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_klo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7050550392683724099ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_khi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7126416350406199490ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_mlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16446666664095245209ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_mhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16457401808690757210ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_act = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17255198050796877158ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14848887488537196220ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_index = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 577020327276202862ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11425649800745150887ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2191016090365079151ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2473179754331825974ull);
    vlSelf->milan_datapath__DOT__csr__DOT__stg_sid_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18407111063316808264ull);
    vlSelf->milan_datapath__DOT__csr__DOT__stg_sid_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7429881293474493392ull);
    vlSelf->milan_datapath__DOT__csr__DOT__stg_dmac_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2503377254568490714ull);
    vlSelf->milan_datapath__DOT__csr__DOT__stg_dmac_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10429374869629111049ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7447757951872317670ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_addr_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2616336660015513041ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2353885409056742122ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1560205352452286441ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_addr_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 10201995388155925905ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4152439075251573206ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10655686080085856533ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7665934513844959298ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5215646545762901120ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_row_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13920916676522139547ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17076418675892450743ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_wr_dmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15225102064557772467ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_cmd_was_wr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5516436394940040844ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_fresh_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17833066521657112009ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_fresh_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1506875643656530723ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_sid_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16677134815942112616ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_dmac_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12265674320600836525ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_state_q_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6322528348199834388ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_probing_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5743055432065944602ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_status_q_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10534155452935918122ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_ctlr_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4518839411219037243ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_flags_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5338870236867212191ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_tuid_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10622876397401828265ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_tklo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17915919733851692340ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_tkhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12302789131455812550ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14728139198237384471ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_ctlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9326927267029812465ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_cthi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14993823869268668225ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4517679852334449665ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8796116156453441777ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_stat_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6808364345817571680ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6888392363568966134ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_flags_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7738964906072919666ull);
    for (int __Vi0 = 0; __Vi0 < 12; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__snap_shadow_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17587902219882628948ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__snap_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13401243747251288645ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11396009220070497634ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10087902531055751017ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6778552146079125458ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_wi_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10128347099574544739ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_cyc_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13570655677034949205ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_word_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9535550438515498905ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9920192665422252616ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_rden_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12476638454605304675ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_m8_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13146359122280446010ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10547011445023463007ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15935505477321121189ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_cyc_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 427335538908098653ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_word_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7187495083838431147ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15114061500259906504ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_reinit_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7107896989702823441ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_ctrl_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3823672466909055624ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_dmlo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10299521400825600779ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_dmhi_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11007010693916361975ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__shadow_ram[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17715787520329520062ull);
    }
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__dflt_rom[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 574837959447466248ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__shadow_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15992117034319299972ull);
    vlSelf->milan_datapath__DOT__csr__DOT__dflt_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9754662354176750976ull);
    vlSelf->milan_datapath__DOT__csr__DOT__shadow_axi_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 594599094268029815ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6973513038012338370ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_mux = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3971510024697558245ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1751065730186971503ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_wire_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7806366114111279884ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_mux = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12629574862558621301ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10215571311606879523ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sel_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14645260474820965396ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_srp9_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11606304147016669678ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_poll_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9006328553005374207ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_sel_row_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6520186371352897103ull);
    vlSelf->milan_datapath__DOT__csr__DOT__srp_prov_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8592047057516714466ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r = VL_SCOPED_RAND_RESET_I(25, __VscopeHash, 1691855097502160009ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__sync_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4169062852005070280ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__lease_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 9327648998287655377ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__no_lease_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12467268227150373987ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__gm_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4453817519304898443ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6074053983101350171ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__ival_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15423599261249573040ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__tu_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10620318943667371231ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__tu_ivals_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11180446964022865620ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17871775881516171892ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1899785309538159450ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 8674119600448016694ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 12208193128776567302ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5963577860569068586ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16334770945009261429ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7456264598591434293ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15765338554287631209ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 4788127773326635489ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17771969784989835681ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11217948867763725957ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12853281243080674311ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11096691945592641739ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6565025543535203189ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14588698973261883580ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12434896338724407506ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6966222693255677569ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__own_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5072003806064769699ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3731182413336555198ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4168703494689461300ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 106442723612964873ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__est_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3405786319015103622ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__et_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4691085994660922745ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ebank_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 821534779399544186ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__fph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13016944412270609976ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__beat_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11335113700708864469ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__rr_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6122908276088449531ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6256100198185193653ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11389123144432984513ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__esmp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10322848712792155464ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eo_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12998868375141184013ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eseq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8148661617784911198ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ets_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18211812824830942656ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__etu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 212215363238968094ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__edmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 53299994515341900ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__euid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16657596977466152150ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__evid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 16795413757673090315ull);
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9494029606082145961ull);
    }
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2090405633593579566ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 410489550010125916ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17438309378887445789ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5683696604543584112ull);
    for (int __Vi0 = 0; __Vi0 < 240; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15647322579175543919ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7816973055398998190ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6896101680176286428ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__fed_now_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13001472491103593177ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__fed_prev_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14158520945752770730ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__pend_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16165429449751575900ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__pend_any_c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 934086077291960599ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__pend_slot_c = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2226260105636771888ull);
    vlSelf->milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3225686926160039377ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__map_r[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 17672175980922143777ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12868497344440148806ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15316308791018785694ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7412035743948137912ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 162037843714216571ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__ring_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17097075857365041428ull);
    }
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2102110978853521090ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__slot_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 775011392815299049ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__lb_sel_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12968677569886618957ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__sel_l_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1710837633302685184ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__sel_r_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 22553266102013722ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 617647150233310410ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4669000913684669080ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__gap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3301763615805424823ull);
    vlSelf->milan_datapath__DOT__tone_gen__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11721313366426049816ull);
    vlSelf->milan_datapath__DOT__tone_gen__DOT__idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17118182703207828577ull);
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__28__e = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__29__e = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__30__e = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__31__e = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack4__32__p = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__146__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__147__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__rnd = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__cnt = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__o = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__187__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__188__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__207__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__208__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__live = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__echo = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__270__a = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__w = 0;
    VL_ZERO_RESET_W(65, vlSelf->__VdfgRegularize_h6e95ff9d_0_1);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_2 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_7 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_8 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_10 = 0;
    VL_ZERO_RESET_W(72, vlSelf->__VdfgRegularize_h6e95ff9d_0_13);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_16 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_17 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_21 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_41 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_42 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_43 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_44 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_45 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_46 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_47 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_48 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_52 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_64 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_66 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_67 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_68 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_76 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_77 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_78 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_80 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_82 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_83 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_89 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_90 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_94 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_95 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_99 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_100 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_101 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_tick_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_tick_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__tdmr_slot_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__axis_tx_rx_ts_switch_rr__DOT__state = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_state = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_state = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__load_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__adj_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_sync__DOT__snap_ret_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_is1g_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_q1 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_num = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_is1g_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_q1 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_num = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_is1g_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_q1 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_num = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_is1g_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_q1 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_num = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_is1g_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_q1 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_num = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_wr = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__i2spb_overruns = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__src_level = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__locked_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_send_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_gain_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_skip_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__lock_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__dstate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_cmd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__integ_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_run_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_second_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_pass_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__repairing_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_d_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_rate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_run_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__zf_tick_cdc__DOT__sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aafcap_pv_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__maap_conflicts = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtprx_dirty_p = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__servo_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0;
    VL_ZERO_RESET_W(448, vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr);
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__disc_lfsr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__disc_dly_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__disc_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__rearm_tick_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__send_pending_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_available_index = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__beat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_adv__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__act_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__act_age_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__aaf_ctrl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__rest_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__sweep_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_m8_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__srp_wr_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__lease_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__tu_seen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__ival_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__esmp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__et_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ebank_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__gap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp_ta_failed = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp_ta_registered = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lane_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__cap_par_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ecap_par_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__vbase_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__pack_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__dom_a_evt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_class_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_prio_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__d_vid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__tfail_code_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__hdr_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__pres_offset_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__req_pop_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pop_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_rl_ms_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__in0_dirty_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend2_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkup_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_linkdn_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cnt_gmchg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend3_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cap_done_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw1_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw3_r = 0;
    VL_ZERO_RESET_W(230, vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__hdr_q);
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_status_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__l0_reject_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__vu_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__discard_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_ph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_done_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__pack_n_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fi_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_len_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ptr_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bidx_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_ph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_rlen_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__status_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cwld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsc_lo_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bsch_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_dlen_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bslh_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bcdl_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_base_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__bscan_ph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__batch_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cdl_q = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_pend4_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_frame_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__sysuid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__started_in_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__req_valid_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__src_mac_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aecp_listener__DOT__u_timers__DOT__ms_ctr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__tout_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_locked_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__settle_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__have_seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__hfill_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r = 0;
    VL_ZERO_RESET_W(88, vlSelf->__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc);
    vlSelf->__VdlyVal__milan_datapath__DOT__tctx_chans_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__tctx_chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__tctx_chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__tctx_chans_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__ts_buffer_to_ps__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__ptp_timestamp__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__bytes_sent__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_mem__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(73, vlSelf->__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__mrpdu_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    VL_ZERO_RESET_W(120, vlSelf->__VdlyVal__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rec_ram_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rec_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rec_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cbuf_r__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__mem__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__mem__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aecp_listener__DOT__u_store__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aecp_listener__DOT__u_store__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_store__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_tdm_render__DOT__bank_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_tdm_render__DOT__bank_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_tdm_render__DOT__bank_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_tdm_render__DOT__bank_r__v1 = 0;
    VL_ZERO_RESET_W(192, vlSelf->__VdlyVal__milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    VL_ZERO_RESET_W(317, vlSelf->__VdlyVal__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__fword_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__fword_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__fword_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__pbcur_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v30 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r__v0 = 0;
    vlSelf->__VdlyDim1__milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__cnt_mir_r__v1 = 0;
    VL_ZERO_RESET_W(150, vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0 = 0;
    VL_ZERO_RESET_W(150, vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1);
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1 = 0;
    VL_ZERO_RESET_W(150, vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2);
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2 = 0;
    VL_ZERO_RESET_W(150, vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3);
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3 = 0;
    VL_ZERO_RESET_W(150, vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4);
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__acmp_responder__DOT__fword_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__acmp_responder__DOT__fword_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__acmp_responder__DOT__fword_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__acmp_responder__DOT__tmr_ram__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__acmp_responder__DOT__tmr_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__acmp_responder__DOT__tmr_ram__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v3 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v3 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v3 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v4 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v4 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v4 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v5 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v5 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v5 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v6 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v6 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v6 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v7 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v7 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v7 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v8 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v9 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v9 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v9 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v10 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v10 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v10 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v11 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v11 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v11 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v12 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v12 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v12 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v12 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v12 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v12 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v13 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v13 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v13 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v14 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v14 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v14 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v15 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v15 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v15 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v16 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v16 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v16 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v17 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v17 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v17 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v18 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v18 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v18 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v19 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v19 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v19 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v19 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v19 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v19 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v20 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v20 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v20 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v20 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v20 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v20 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v21 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v21 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v21 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v21 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v21 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v21 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v22 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v22 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v22 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v22 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v22 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v22 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v23 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v23 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v23 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v23 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v23 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v23 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v24 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v24 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v24 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v24 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v24 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v24 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v25 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v25 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v25 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v25 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v25 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v25 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v25 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v25 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v25 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v26 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v26 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v26 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v26 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v26 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v26 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v26 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v26 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v26 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v27 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v27 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v27 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v27 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v27 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v27 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v27 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v27 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v27 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v28 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v28 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v28 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v28 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v28 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v28 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v28 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v28 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v28 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v29 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v29 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v29 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v29 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v29 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v29 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v30 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v30 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v30 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v30 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v30 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v30 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v30 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v30 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v30 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v31 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v31 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v31 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v31 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v31 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v31 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v31 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v31 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v31 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v32 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v32 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v32 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v32 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v32 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v32 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v32 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v32 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v32 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v33 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v33 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v33 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v33 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v33 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v33 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v33 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v33 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v33 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v34 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v34 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v34 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v34 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v34 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v34 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v34 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v34 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v34 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v35 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v35 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v35 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v35 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v35 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v35 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v35 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v35 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v35 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v36 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v36 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v36 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v36 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v36 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v36 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v36 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v36 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v36 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v37 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v37 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v37 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v37 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v37 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v37 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v37 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v37 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v37 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v38 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v38 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v38 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v38 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v38 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v38 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v38 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v38 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v38 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v39 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v39 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v39 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v39 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v39 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v39 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v40 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v40 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v40 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v40 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v40 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v40 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v41 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v41 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v41 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v41 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v41 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v41 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v41 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v41 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v41 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v42 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v42 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v42 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v42 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v42 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v42 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v42 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v42 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v42 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v43 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v43 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v43 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v43 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v43 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v43 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v43 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v43 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v43 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v44 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v44 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v44 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v44 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v44 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v44 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v44 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v44 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v44 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v45 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v45 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v45 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v45 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v45 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v45 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v45 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v45 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v45 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v46 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v46 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v46 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v46 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v46 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v46 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v46 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v46 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v46 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v47 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v47 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v47 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v47 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v47 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v47 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v47 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v47 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v47 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v48 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v48 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v48 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v48 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v48 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v48 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v48 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v48 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v48 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v49 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v49 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v49 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v49 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v49 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v49 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v49 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v49 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v49 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v50 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v50 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v50 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v50 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v50 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v50 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v50 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v50 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v50 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v51 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v51 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v51 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v51 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v51 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v51 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v51 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v51 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v51 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v52 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v52 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v52 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v52 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v52 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v52 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v52 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v52 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v52 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v53 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v53 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v53 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v53 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v53 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v53 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v53 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v53 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v53 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v54 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v54 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v54 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v54 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v54 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v54 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v54 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v54 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v54 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v55 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v55 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v55 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v55 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v55 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v55 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v55 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v55 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v55 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v56 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v56 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v56 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v56 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v56 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v56 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v56 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v56 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v56 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v57 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v57 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v57 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v57 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v57 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v57 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v57 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v57 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v57 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v58 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v58 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v58 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v58 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v58 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v58 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v58 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v58 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v58 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v59 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v59 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v59 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v59 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v59 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v59 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v59 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v59 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v59 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v60 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v60 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v60 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v60 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v60 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v60 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v60 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v60 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v60 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v61 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v61 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v61 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v61 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v61 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v61 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v61 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v61 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v61 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v62 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v62 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v62 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v62 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v62 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v62 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v62 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v62 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v62 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v63 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v63 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v63 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v63 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v63 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v63 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v63 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v63 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v63 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v64 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v64 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v64 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v64 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v64 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v64 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v64 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v64 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v64 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v65 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v65 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v65 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v65 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v65 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v65 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v65 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v65 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v65 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v66 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v66 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v66 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v66 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v66 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v66 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v66 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v66 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v66 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v67 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v67 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v67 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v67 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v67 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v67 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v67 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v67 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v67 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v68 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v68 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v68 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v68 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v68 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v68 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v68 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v68 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v68 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v69 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v69 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v69 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v69 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v69 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v69 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v69 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v69 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v69 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v70 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v70 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v70 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v70 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v70 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v70 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v70 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v70 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v70 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v71 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v71 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v71 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v71 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v71 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v71 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v71 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v71 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v71 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v72 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v72 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v72 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v72 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v72 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v72 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v72 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v72 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v72 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v73 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v73 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v73 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v73 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v73 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v73 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v73 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v73 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v73 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v74 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v74 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v74 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v74 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v74 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v74 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v74 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v74 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v74 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v75 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v75 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v75 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v75 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v75 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v75 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v75 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v75 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v75 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v76 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v76 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v76 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v76 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v76 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v76 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v76 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v76 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v76 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v77 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v77 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v77 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v77 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v77 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v77 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v77 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v77 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v77 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v78 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v78 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v78 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v78 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v78 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v78 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v78 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v78 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v78 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v79 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v79 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v79 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v79 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v79 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v79 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v79 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v79 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v79 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v80 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v80 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v80 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v80 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v80 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v80 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v80 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v80 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v80 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v81 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v81 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v81 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v81 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v81 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v81 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v81 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v81 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v81 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v82 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v82 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v82 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v82 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v82 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v82 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v82 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v82 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v82 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v83 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v83 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v83 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v83 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v83 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v83 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v83 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v83 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v83 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v84 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v84 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v84 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v84 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v84 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v84 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v84 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v84 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v84 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v85 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v85 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v85 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v85 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v85 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v85 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v85 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v85 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v85 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v86 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v86 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v86 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v86 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v86 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v86 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v86 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v86 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v86 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v87 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v87 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v87 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v87 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v87 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v87 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v87 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v87 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v87 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v88 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v88 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v88 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v88 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v88 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v88 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v88 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v88 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v88 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v89 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v89 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v89 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v89 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v89 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v89 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v89 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v89 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v89 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v90 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v90 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v90 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v90 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v90 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v90 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v90 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v90 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v90 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v91 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v91 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v91 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v91 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v91 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v91 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v91 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v91 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v91 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v92 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v92 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v92 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v92 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v92 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v92 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v92 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v92 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v92 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v93 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v93 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v93 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v93 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v93 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v93 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v93 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v93 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v93 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v94 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v94 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v94 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v94 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v94 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v94 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v94 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v94 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v94 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v95 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v95 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v95 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v95 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v95 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v95 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v95 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v95 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v95 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v96 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v96 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v96 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v96 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v96 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v96 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v96 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v96 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v96 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v97 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v97 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v97 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v97 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v97 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v97 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v97 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v97 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v97 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v98 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v98 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v98 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v98 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v98 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v98 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v98 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v98 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v98 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v99 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v99 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v99 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v99 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v99 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v99 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v99 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v99 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v99 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v100 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v100 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v100 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v100 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v100 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v100 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v100 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v100 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v100 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v101 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v101 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v101 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v101 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v101 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v101 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v101 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v101 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v101 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v102 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v102 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v102 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v102 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v102 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v102 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v102 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v102 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v102 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v103 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v103 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v103 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v103 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v103 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v103 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v103 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v103 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v103 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v104 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v104 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v104 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v104 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v104 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v104 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v104 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v104 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v104 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v105 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v105 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v105 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v105 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v105 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v105 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v105 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v105 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v105 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v106 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v106 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v106 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v106 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v106 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v106 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v106 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v106 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v106 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v107 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v107 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v107 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v107 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v107 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v107 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v107 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v107 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v107 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v108 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v108 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v108 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v108 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v108 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v108 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v108 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v108 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v108 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v109 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v109 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v109 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v109 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v109 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v109 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v109 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v109 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v109 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v110 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v110 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v110 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v110 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v110 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v110 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v110 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v110 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v110 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v111 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v111 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v111 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v111 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v111 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v111 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v111 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v111 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v111 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v112 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v112 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v112 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v112 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v112 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v112 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v112 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v112 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v112 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v113 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v113 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v113 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v113 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v113 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v113 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v113 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v113 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v113 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v114 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v114 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v114 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v114 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v114 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v114 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v114 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v114 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v114 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v115 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v115 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v115 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v115 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v115 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v115 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v115 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v115 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v115 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v116 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v116 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v116 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v116 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v116 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v116 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v116 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v116 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v116 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v117 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v117 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v117 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v117 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v117 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v117 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v117 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v117 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v117 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v118 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v118 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v118 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v118 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v118 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v118 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v118 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v118 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v118 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v119 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v119 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v119 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v119 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v119 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v119 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v119 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v119 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v119 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v120 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v120 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v120 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v120 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v120 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v120 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v120 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v120 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v120 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v121 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v121 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v121 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v121 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v121 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v121 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v121 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v121 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v121 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v122 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v122 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v122 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v122 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v122 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v122 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v122 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v122 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v122 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v123 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v123 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v123 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v123 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v123 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v123 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v123 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v123 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v123 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v124 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v124 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v124 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v124 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v124 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v124 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v124 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v124 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v124 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v125 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v125 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v125 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v125 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v125 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v125 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v125 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v125 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v125 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v126 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v126 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v126 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v126 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v126 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v126 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v126 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v126 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v126 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v127 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v127 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v127 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v127 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v127 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v127 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v127 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v127 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v127 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v128 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v128 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v128 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v128 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v128 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v128 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v128 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v128 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v128 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v129 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v129 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v129 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v129 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v129 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v129 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v129 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v129 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v129 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v130 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v130 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v130 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v130 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v130 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v130 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v130 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v130 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v130 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v131 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v131 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v131 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v131 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v131 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v131 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v131 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v131 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v131 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v132 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v132 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v132 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v132 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v132 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v132 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v132 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v132 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v132 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v133 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v133 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v133 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v133 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v133 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v133 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v133 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v133 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v133 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v134 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v134 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v134 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v134 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v134 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v134 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v134 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v134 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v134 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v135 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v135 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v135 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v135 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v135 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v135 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v135 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v135 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v135 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v136 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v136 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v136 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v136 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v136 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v136 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v136 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v136 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v136 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v137 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v137 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v137 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v137 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v137 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v137 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v137 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v137 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v137 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v138 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v138 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v138 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v138 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v138 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v138 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v138 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v138 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v138 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v139 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v139 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v139 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v139 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v139 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v139 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v139 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v139 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v139 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v140 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v140 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v140 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v140 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v140 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v140 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v140 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v140 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v140 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v141 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v141 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v141 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v141 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v141 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v141 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v141 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v141 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v141 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v142 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v142 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v142 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v142 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v142 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v142 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v142 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v142 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v142 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v143 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v143 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v143 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v143 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v143 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v143 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v143 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v143 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v143 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v144 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v144 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v144 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v144 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v144 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v144 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v144 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v144 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v144 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v145 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v145 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v145 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v145 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v145 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v145 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v145 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v145 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v145 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v146 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v146 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v146 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v146 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v146 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v146 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v146 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v146 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v146 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v147 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v147 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v147 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v147 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v147 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v147 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v147 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v147 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v147 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v148 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v148 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v148 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v148 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v148 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v148 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v148 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v148 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v148 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v149 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v149 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v149 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v149 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v149 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v149 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v149 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v149 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v149 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v150 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v150 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v150 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v150 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v150 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v150 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v150 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v150 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v150 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v151 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v151 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v151 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v151 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v151 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v151 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v151 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v151 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v151 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v152 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v152 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v152 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v152 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v152 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v152 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v152 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v152 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v152 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v153 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v153 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v153 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v153 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v153 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v153 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v153 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v153 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v153 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v154 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v154 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v154 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v154 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v154 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v154 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v154 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v154 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v154 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v155 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v155 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v155 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v155 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v155 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v155 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v155 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v155 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v155 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v156 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v156 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v156 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v156 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v156 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v156 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v156 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v156 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v156 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v157 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v157 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v157 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v157 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v157 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v157 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v157 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v157 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v157 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v158 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v158 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v158 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v158 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v158 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v158 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v158 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v158 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v158 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v159 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v159 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v159 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v159 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v159 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v159 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v159 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v159 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v159 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v160 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v160 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v160 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v160 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v160 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v160 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v160 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v160 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v160 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v161 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v161 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v161 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v161 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v161 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v161 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v161 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v161 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v161 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v162 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v162 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v162 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v162 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v162 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v162 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v162 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v162 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v162 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v163 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v163 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v163 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v163 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v163 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v163 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v163 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v163 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v163 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v164 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v164 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v164 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v164 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v164 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v164 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v164 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v164 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v164 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v165 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v165 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v165 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v165 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v165 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v165 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v165 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v165 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v165 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v166 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v166 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v166 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v166 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v166 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v166 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v166 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v166 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v166 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v167 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v167 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v167 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v167 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v167 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v167 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v167 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v167 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v167 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v168 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v168 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v168 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v168 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v168 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v168 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v168 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v168 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v168 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_lo__v169 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_lo__v169 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_lo__v169 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_hi__v169 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_hi__v169 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_hi__v169 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__cbs_idle__v169 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__cbs_idle__v169 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v169 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v170 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__cbs_idle__v171 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v51 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__ring_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cum_q__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v34 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v35 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v36 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v37 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v38 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v41 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v42 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q__v43 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v44 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v45 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v46 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v43 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v44 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v49 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v50 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v51 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v52 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v47 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v48 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v49 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v56 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v57 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v51 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v52 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v61 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v62 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v54 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v65 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v66 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v67 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v68 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v57 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v58 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v71 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v59 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v60 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v61 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v75 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v76 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v77 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v62 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v63 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v80 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v81 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v82 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v64 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v65 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v66 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v86 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v87 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v88 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v67 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v68 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v91 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v70 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v71 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v72 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v73 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v74 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v75 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v76 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v100 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v101 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v77 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v104 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v79 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v80 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v81 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_len_q__v108 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v82 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v83 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v84 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v85 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v86 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v87 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v88 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v89 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v90 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v91 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v92 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v93 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v94 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v95 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v96 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v97 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v98 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v99 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v100 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v101 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v102 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v103 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v104 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v105 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v106 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v107 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v108 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v109 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v110 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v111 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v112 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v113 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v114 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v115 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v116 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v117 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_seq_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v118 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v119 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v120 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v121 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v122 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v123 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v124 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v125 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v126 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v127 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v128 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v129 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v130 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v131 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v132 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v133 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__rec_hdr_q__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__unsol_valid_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_kind_q__v134 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_tdm_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_awaddr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_awvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wstrb__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_bready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_araddr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_arvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_rready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i2s_sdout_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_bclk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_fsync_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_tx_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_rx_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_ts_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_pcm_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_mac_tx_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_speed__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_link_up__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_full_duplex__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethrx_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethtx_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethact_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_events__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_events_cap__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ps_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_drp_do__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_drp_rdy__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_locked__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_ps_done__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_enable_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_underrun_silence_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_stream_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_ring_base_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_ring_len_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_ring_stride_i__0 = 0;
    VL_ZERO_RESET_W(256, vlSelf->__Vtrigprevexpr___TOP__pb_wr_ptr_i__0);
    vlSelf->__Vtrigprevexpr___TOP__pb_mem_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__pb_mem_valid_i__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio_i__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_resetn__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ps_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_tdm_i__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_bclk_i__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
