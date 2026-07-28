// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___nba_comb__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_comb__TOP__3\n"); );
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

void Vmilan_datapath___024root___nba_sequent__TOP__0(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__1(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__2(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath_axi_stream_if__TC3___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0(Vmilan_datapath_axi_stream_if__TC3* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__4(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__5(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__6(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__7(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__8(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__9(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__11(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_comb__TOP__1(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__12(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__13(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__15(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_comb__TOP__2(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0(Vmilan_datapath_axi_stream_if* vlSelf);
void Vmilan_datapath___024root___ico_sequent__TOP__10(Vmilan_datapath___024root* vlSelf);

void Vmilan_datapath___024root___eval_nba(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_nba\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__0(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__1(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__2(vlSelf);
        Vmilan_datapath_axi_stream_if__TC3___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue__0((&vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo__0((&vlSymsp->TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx));
        {
            // Inlined CFunc: _nba_sequent__TOP__3
            CData/*4:0*/ __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
            __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int = 0;
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
            __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int 
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
                                & (0U != __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int)))) 
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
                        = __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
                }
                if ((1U & (~ ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))) 
                              | (~ (0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))))))) {
                    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next 
                        = __Vinline_0__nba_sequent__TOP__3_milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_int;
                }
            } else if ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))) {
                vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_next 
                    = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_reg;
                vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tvalid_next = 0U;
            }
            vlSelfRef.milan_datapath__DOT__dpaaf_tvalid 
                = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel)
                     ? (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))
                     : (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tvalid)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__active));
            vlSelfRef.milan_datapath__DOT__dpaaf_tlast 
                = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_final_mux__DOT__gsel)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)
                    : (IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tlast));
        }
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered));
        Vmilan_datapath_axi_stream_if___nba_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered));
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__4(vlSelf);
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__5(vlSelf);
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__6(vlSelf);
    }
    if ((0x0000000000000020ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__7(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__8(vlSelf);
    }
    if ((0x0000000000000040ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__9(vlSelf);
    }
    if ((0x0000000000000080ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__10
            CData/*1:0*/ __Vinline_0__nba_sequent__TOP__10___Vdly__milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r;
            __Vinline_0__nba_sequent__TOP__10___Vdly__milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r = 0;
            __Vinline_0__nba_sequent__TOP__10___Vdly__milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r 
                = vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r;
            __Vinline_0__nba_sequent__TOP__10___Vdly__milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r 
                = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r) 
                          << 1U)) | (IData)(vlSelfRef.axis_resetn));
            vlSelfRef.milan_datapath__DOT__chmap_tdm_dout_w 
                = (((IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r) 
                    >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__dout_nxt_r));
            vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r 
                = __Vinline_0__nba_sequent__TOP__10___Vdly__milan_datapath__DOT__chan_tdm_render__DOT__nrst_n_r;
            vlSelfRef.tdm_dout_o = vlSelfRef.milan_datapath__DOT__chmap_tdm_dout_w;
        }
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__11(vlSelf);
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__0
            if ((4U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                if ((2U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                        = (0x00ffffffU & 0U);
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                        = (0x00ffffffU & 0U);
                } else if ((1U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                        = (0x00ffffffU & (IData)((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_sel_w 
                                                  >> 0x00000018U)));
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                        = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_sel_w));
                } else {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                        = (0x00ffffffU & vlSelfRef.milan_datapath__DOT__tone_smp);
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                        = (0x00ffffffU & vlSelfRef.milan_datapath__DOT__tone_smp);
                }
            } else if ((2U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                if ((1U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                        = (0x00ffffffU & (IData)((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__ring_hold_r
                                                  [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10] 
                                                  >> 0x00000018U)));
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                        = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__ring_hold_r
                                                 [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10]));
                } else {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                        = (0x00ffffffU & (IData)(((
                                                   (4U 
                                                    > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                    ? vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                   [
                                                   (3U 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))]
                                                    : 0ULL) 
                                                  >> 0x00000018U)));
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                        = (0x00ffffffU & (IData)(((4U 
                                                   > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                   ? vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                  [
                                                  (3U 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))]
                                                   : 0ULL)));
                }
            } else if ((1U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2))) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                    = (0x00ffffffU & (IData)((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                              >> 0x00000018U)));
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                    = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r));
            } else {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_l_w 
                    = (0x00ffffffU & 0U);
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                    = (0x00ffffffU & 0U);
            }
        }
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_comb__TOP__1(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__12(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__13(vlSelf);
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__14
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U];
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U];
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U];
        }
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__15(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_comb__TOP__2(vlSelf);
        Vmilan_datapath___024root___nba_comb__TOP__3(vlSelf);
        Vmilan_datapath_axi_stream_if___ico_sequent__TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx__0((&vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx));
        Vmilan_datapath___024root___ico_sequent__TOP__10(vlSelf);
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__5
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                = (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                   - ((vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U] 
                       << 8U) | (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U] 
                                 >> 0x00000018U)));
        }
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__16
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hidx_r 
                = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r;
        }
    }
    if ((0x000000000000000dULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__6
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
                = ((0xfffffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
                   | ((VL_GTS_III(32, 0U, vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
                       << 1U) | (VL_LTES_III(32, 0U, vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
                                 & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                                    > ((IData)(0x00989680U) 
                                       + vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__pres_offset_r)))));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
                = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
                   | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                      << 2U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U] 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                    >> 0x0000001eU) | ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_fsh) 
                                       << 2U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[2U] 
                = (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_fsh) 
                    >> 0x0000001eU) | ((IData)((vlSelfRef.milan_datapath__DOT__avtprx_fsh 
                                                >> 0x00000020U)) 
                                       << 2U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[3U] 
                = (((IData)((vlSelfRef.milan_datapath__DOT__avtprx_fsh 
                             >> 0x00000020U)) >> 0x0000001eU) 
                   | (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                      << 2U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U] 
                = ((0x003ffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
                   | (0x003fffffU & (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                                     >> 0x0000001eU)));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U] 
                = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
                   | (0x003fffffU & (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx) 
                                      << 0x00000013U) 
                                     | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype) 
                                         << 0x0000000bU) 
                                        | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                                            << 3U) 
                                           | ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tu_bit) 
                                              << 2U))))));
        }
    }
}

void Vmilan_datapath___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vmilan_datapath___024root___eval_phase__act(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_phase__act\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        (((((((~ (IData)(vlSelfRef.tdm_bclk_i)) 
                                                              & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__1)) 
                                                             << 3U) 
                                                            | (((IData)(vlSelfRef.tdm_bclk_i) 
                                                                & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__1))) 
                                                               << 2U)) 
                                                           | ((((IData)(vlSelfRef.clk_tdm_i) 
                                                                & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_tdm_i__1))) 
                                                               << 1U) 
                                                              | ((IData)(vlSelfRef.i_ps_clk) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__1))))) 
                                                          << 4U) 
                                                         | (((((IData)(vlSelfRef.gtx_clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1))) 
                                                              << 3U) 
                                                             | (((~ (IData)(vlSelfRef.axis_resetn)) 
                                                                 & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__1)) 
                                                                << 2U)) 
                                                            | ((((IData)(vlSelfRef.clk_audio_i) 
                                                                 & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__1))) 
                                                                << 1U) 
                                                               | ((IData)(vlSelfRef.axis_clk) 
                                                                  & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__1))))))));
        vlSelfRef.__Vtrigprevexpr___TOP__axis_clk__1 
            = vlSelfRef.axis_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__clk_audio_i__1 
            = vlSelfRef.clk_audio_i;
        vlSelfRef.__Vtrigprevexpr___TOP__axis_resetn__1 
            = vlSelfRef.axis_resetn;
        vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1 
            = vlSelfRef.gtx_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__1 
            = vlSelfRef.i_ps_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__clk_tdm_i__1 
            = vlSelfRef.clk_tdm_i;
        vlSelfRef.__Vtrigprevexpr___TOP__tdm_bclk_i__1 
            = vlSelfRef.tdm_bclk_i;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmilan_datapath___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vmilan_datapath___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vmilan_datapath___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vmilan_datapath___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

bool Vmilan_datapath___024root___eval_phase__nba(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_phase__nba\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vmilan_datapath___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vmilan_datapath___024root___eval_nba(vlSelf);
        Vmilan_datapath___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG
bool Vmilan_datapath___024root___eval_phase__ico(Vmilan_datapath___024root* vlSelf);

void Vmilan_datapath___024root___eval(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vmilan_datapath___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/milan/milan_datapath.sv", 34, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vmilan_datapath___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vmilan_datapath___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/milan/milan_datapath.sv", 34, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vmilan_datapath___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/milan/milan_datapath.sv", 34, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vmilan_datapath___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vmilan_datapath___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vmilan_datapath___024root___eval_debug_assertions(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_debug_assertions\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.axis_clk & 0xfeU)))) {
        Verilated::overWidthError("axis_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.clk_audio_i & 0xfeU)))) {
        Verilated::overWidthError("clk_audio_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.clk_tdm_i & 0xfeU)))) {
        Verilated::overWidthError("clk_tdm_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.axis_resetn & 0xfeU)))) {
        Verilated::overWidthError("axis_resetn");
    }
    if (VL_UNLIKELY(((vlSelfRef.gtx_clk & 0xfeU)))) {
        Verilated::overWidthError("gtx_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.gtx_resetn & 0xfeU)))) {
        Verilated::overWidthError("gtx_resetn");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_awvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axi_awvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_wstrb & 0xf0U)))) {
        Verilated::overWidthError("s_axi_wstrb");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_wvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axi_wvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_bready & 0xfeU)))) {
        Verilated::overWidthError("s_axi_bready");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_arvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axi_arvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axi_rready & 0xfeU)))) {
        Verilated::overWidthError("s_axi_rready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i2s_sdout_i & 0xfeU)))) {
        Verilated::overWidthError("i2s_sdout_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_bclk_i & 0xfeU)))) {
        Verilated::overWidthError("tdm_bclk_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_fsync_i & 0xfeU)))) {
        Verilated::overWidthError("tdm_fsync_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_data_i & 0xfeU)))) {
        Verilated::overWidthError("tdm_data_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_tx_tvalid & 0xfeU)))) {
        Verilated::overWidthError("s_axis_tx_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_tx_tlast & 0xfeU)))) {
        Verilated::overWidthError("s_axis_tx_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_rx_tready & 0xfeU)))) {
        Verilated::overWidthError("m_axis_rx_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_ts_tready & 0xfeU)))) {
        Verilated::overWidthError("m_axis_ts_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_pcm_tready & 0xfeU)))) {
        Verilated::overWidthError("m_axis_pcm_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.m_axis_mac_tx_tready 
                      & 0xfeU)))) {
        Verilated::overWidthError("m_axis_mac_tx_tready");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_mac_rx_tvalid 
                      & 0xfeU)))) {
        Verilated::overWidthError("s_axis_mac_rx_tvalid");
    }
    if (VL_UNLIKELY(((vlSelfRef.s_axis_mac_rx_tlast 
                      & 0xfeU)))) {
        Verilated::overWidthError("s_axis_mac_rx_tlast");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mac_speed & 0xfcU)))) {
        Verilated::overWidthError("i_mac_speed");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_link_up & 0xfeU)))) {
        Verilated::overWidthError("i_link_up");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_full_duplex & 0xfeU)))) {
        Verilated::overWidthError("i_full_duplex");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ethrx_tgl & 0xfeU)))) {
        Verilated::overWidthError("i_ethrx_tgl");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ethtx_tgl & 0xfeU)))) {
        Verilated::overWidthError("i_ethtx_tgl");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ethact_tgl & 0xfeU)))) {
        Verilated::overWidthError("i_ethact_tgl");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mac_events & 0xfe00U)))) {
        Verilated::overWidthError("i_mac_events");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mac_events_cap & 0xfe00U)))) {
        Verilated::overWidthError("i_mac_events_cap");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_ps_clk & 0xfeU)))) {
        Verilated::overWidthError("i_ps_clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mmcm_drp_rdy & 0xfeU)))) {
        Verilated::overWidthError("i_mmcm_drp_rdy");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mmcm_locked & 0xfeU)))) {
        Verilated::overWidthError("i_mmcm_locked");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_mmcm_ps_done & 0xfeU)))) {
        Verilated::overWidthError("i_mmcm_ps_done");
    }
    if (VL_UNLIKELY(((vlSelfRef.pb_enable_i & 0xfeU)))) {
        Verilated::overWidthError("pb_enable_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.pb_underrun_silence_i 
                      & 0xfeU)))) {
        Verilated::overWidthError("pb_underrun_silence_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.pb_mem_valid_i & 0xfeU)))) {
        Verilated::overWidthError("pb_mem_valid_i");
    }
}
#endif  // VL_DEBUG
