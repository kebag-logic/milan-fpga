// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___nba_comb__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_comb__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*13:0*/ milan_datapath__DOT__amap_edit_out_enc_w;
    milan_datapath__DOT__amap_edit_out_enc_w = 0;
    CData/*0:0*/ milan_datapath__DOT__ctlg2_tvalid;
    milan_datapath__DOT__ctlg2_tvalid = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ikey_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ikey_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_edit_validate__DOT__okey_c;
    milan_datapath__DOT__amap_edit_validate__DOT__okey_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 0;
    CData/*7:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ibase_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ibase_c = 0;
    CData/*7:0*/ milan_datapath__DOT__amap_edit_validate__DOT__iexpect_c;
    milan_datapath__DOT__amap_edit_validate__DOT__iexpect_c = 0;
    SData/*12:0*/ milan_datapath__DOT__amap_edit_validate__DOT__obase_c;
    milan_datapath__DOT__amap_edit_validate__DOT__obase_c = 0;
    SData/*12:0*/ milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c;
    milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c = 0;
    SData/*15:0*/ milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c;
    milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c;
    milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c;
    milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c;
    milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c;
    milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c = 0;
    SData/*13:0*/ __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__Vfuncout;
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i;
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i;
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i = 0;
    SData/*13:0*/ __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r;
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0;
    IData/*23:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__Vfuncout;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a = 0;
    IData/*31:0*/ __Vilp1;
    // Body
    if (vlSelfRef.milan_datapath__DOT__csr__DOT__pp_rd_hit_w) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = (((0x0920U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                 ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r
                 : ((0x0924U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                     ? (0x5b000000U | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r) 
                                         << 0x0000000cU) 
                                        | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w) 
                                              << 3U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_valid_r) 
                                                << 2U)) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__stale_r) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w))) 
                                           << 8U)) 
                                       | (((((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__any_rec_r)) 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r)) 
                                              << 3U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r) 
                                                << 2U)) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_err_r) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r))) 
                                           << 4U) | 
                                          (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fail_r) 
                                              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__walk_blind_r) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r))) 
                                             << 3U) 
                                            | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r) 
                                               << 2U)) 
                                           | (((IData)(vlSelfRef.milan_datapath__DOT__pp_restore_busy_w) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_busy_r))))))
                     : ((0x0928U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                         ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_spaddr_r
                         : ((0x092cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                             ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_sprdata_r
                             : ((0x0930U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                                 ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_tx_frames_w) 
                                     << 0x00000010U) 
                                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_rx_drops_w) 
                                        << 8U) | (0x000000ffU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_rx_frames_w))))
                                 : ((0x0934U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                                     ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r)
                                     : ((0x00000020U 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                         ? ((0x00000010U 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                             ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r
                                                         [
                                                         (3U 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))]) 
                                                 << 0x00000010U) 
                                                | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r
                                                [(3U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))])
                                             : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r
                                                         [
                                                         (3U 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))]) 
                                                 << 0x00000010U) 
                                                | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r
                                                [(3U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))]))
                                         : ((1U == 
                                             (3U & 
                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                               >> 3U)))
                                             ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r
                                            [(7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))]
                                             : ((- (IData)(
                                                           (1U 
                                                            & (~ 
                                                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                                                >> 3U))))) 
                                                & (((4U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                     ? 
                                                    ((- (IData)((IData)(
                                                                        (1U 
                                                                         == 
                                                                         (3U 
                                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))))) 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_id_r))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                      ? 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                       ? 
                                                      (0xc3000000U 
                                                       | (((((((0U 
                                                                != 
                                                                (((((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
                                                                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U]) 
                                                                      | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U]) 
                                                                     | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U]) 
                                                                    | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U]) 
                                                                   | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U]) 
                                                                  | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U]) 
                                                                 | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U])) 
                                                               << 3U) 
                                                              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w) 
                                                                 << 2U)) 
                                                             | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r) 
                                                                 << 1U) 
                                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r))) 
                                                            << 0x00000014U) 
                                                           | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r) 
                                                                 << 3U) 
                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r) 
                                                                   << 2U)) 
                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r) 
                                                                   << 1U) 
                                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r))) 
                                                              << 0x00000010U)) 
                                                          | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r) 
                                                               << 0x0000000cU) 
                                                              | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r) 
                                                                      << 2U)) 
                                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__stale_r) 
                                                                      << 1U) 
                                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w))) 
                                                                 << 8U)) 
                                                             | ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_valid_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r) 
                                                                      << 2U)) 
                                                                  | (((0U 
                                                                       != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r) 
                                                                      << 1U) 
                                                                     | (0U 
                                                                        != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)))) 
                                                                 << 4U) 
                                                                | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r) 
                                                                      << 2U))))))
                                                       : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r)
                                                      : 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r
                                                       : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r))) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                                                     >> 4U))))))))))))))) 
               & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__pp_rd_hit_w))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_swallow_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ver_fail_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w) 
           & ((1U == (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r) 
                                     - (IData)(0x000eU)))) 
              & (0U != (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                       >> 4U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__sub_fail_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w) 
           & ((~ (((0xfeU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r))) 
                  | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r)) 
                     & ((0xfaU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                        | ((0xfbU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                           | (0xfcU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w))))))) 
              & (0U == (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r) 
                                       - (IData)(0x000eU))))));
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
         & (5U > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
        if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
             != ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i))) 
                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r) 
                           >> (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i))))))) {
            if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w) 
                       | (0x1fU & ((IData)(1U) << (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
            ? (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r)
            : (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)));
    vlSelfRef.milan_datapath__DOT__dpcrf_tlast = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                                                  | ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
                                                      ? 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
                                                      & (7U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r)))
                                                      : (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r) 
         | ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
             ? ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r) 
                & (7U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r)))
             : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_last_r)));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
            ? (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_1722_a_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w)));
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000003fU)) {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[__Vilp1] = 0U;
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[0U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    if (vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vln_r) {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[12U] = 0x81U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[14U] 
            = (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vpcp_r) 
                << 5U) | (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vvid_r) 
                                         >> 8U)));
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[15U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__vvid_r));
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[16U] = 0x22U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[17U] = 0xf0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[18U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[0U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[19U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[1U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[20U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[2U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[21U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[3U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[22U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[4U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[23U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[5U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[24U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[6U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[25U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[7U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[26U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[8U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[27U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[9U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[28U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[10U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[29U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[11U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[30U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[12U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[31U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[13U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[32U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[14U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[33U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[15U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[34U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[16U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[35U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[17U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[36U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[18U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[37U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[19U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[38U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[20U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[39U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[21U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[40U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[22U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[41U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[23U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[42U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[24U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[43U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[25U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[44U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[26U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[45U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[27U];
    } else {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[12U] = 0x22U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[13U] = 0xf0U;
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[14U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[0U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[15U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[1U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[16U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[2U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[17U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[3U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[18U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[4U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[19U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[5U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[20U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[6U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[21U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[7U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[22U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[8U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[23U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[9U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[24U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[10U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[25U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[11U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[26U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[12U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[27U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[13U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[28U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[14U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[29U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[15U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[30U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[16U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[31U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[17U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[32U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[18U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[33U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[19U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[34U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[20U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[35U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[21U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[36U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[22U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[37U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[23U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[38U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[24U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[39U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[25U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[40U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[26U];
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[41U] 
            = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[27U];
    }
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a 
        = (0x0000007fU & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i));
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__Vfuncout 
        = ((0x00000040U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a))
            ? 0U : ((4U > (7U & ((IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a) 
                                 >> 3U))) ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r
                    [(3U & ((IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a) 
                            >> 3U))][(7U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__a))]
                     : 0U));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w 
        = __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__216__Vfuncout;
    vlSelfRef.milan_datapath__DOT__asp_resp_capture_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_299) 
           & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w)) 
              & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w)))));
    vlSelfRef.milan_datapath__DOT__gsi_avb_capture_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_299) 
           & ((0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))) 
              & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_ready_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__rd_en_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r) 
               < vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r]) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r)) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_ready_w))));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i) 
           & (0x0aU > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctr_hold_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_req_w) 
            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r))) 
           & (~ ((IData)(vlSelfRef.milan_datapath__DOT__ctr_srv2_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__ctr_sel_match_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_hold_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_amap_req_w) 
            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r))) 
           & (~ ((IData)(vlSelfRef.milan_datapath__DOT__amap_srv_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__amap_sel_match_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsi_hold_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_req_w) 
            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r))) 
           & (~ ((IData)(vlSelfRef.milan_datapath__DOT__gsi_srv2_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__gsi_sel_match_w))));
    vlSelfRef.milan_datapath__DOT__gsi_setl_w = ((0ULL 
                                                  != vlSelfRef.milan_datapath__DOT__gsi_sid_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__gsi_bnd_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294 = (0x000000ffU 
                                                  & ((IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w 
                                                              >> 
                                                              (0x00000038U 
                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                                  << 3U)))) 
                                                     & (- (IData)(
                                                                  ((0x27U 
                                                                    >= 
                                                                    (0x00000038U 
                                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                                        << 3U))) 
                                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_tkfail_w))))));
    vlSelfRef.milan_datapath__DOT__gsi_flags_ex_w = 0U;
    vlSelfRef.milan_datapath__DOT__mcr_streaming_w 
        = ((0x00000010U & (vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl 
                           << 4U)) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w 
        = (((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
             ? (IData)(vlSelfRef.milan_datapath__DOT__cmap_pv_w)
             : (IData)(vlSelfRef.milan_datapath__DOT__zf_pv_w)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w) 
                     & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
                        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w] 
                        & (5U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                           [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                    >> (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w)))));
    vlSelfRef.milan_datapath__DOT__tkd_streaming_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__crft_emit_en_w) 
            << 4U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_27 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_tmo_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w)) 
              & (0x00002710U <= (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                 - vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_t0_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ver_fail_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__sub_fail_w));
    vlSelfRef.milan_datapath__DOT__dpcrf_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w) 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active)));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid = 
        ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r) 
         | ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w) 
            & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w = 0U;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
          & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) 
         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r)))) {
        if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w = 1U;
        } else if (((0x000dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w = 1U;
        }
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w) 
          & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r))) 
         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_val_w = 0U;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
          & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) 
         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r)))) {
        if ((1U & (~ ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w)))))) {
            if (((0x000dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_val_w 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r) 
                        & (0x22eaU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_w))) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r) 
                          & (0x88f5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_w))));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__eof_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w));
    vlSelfRef.milan_datapath__DOT__gsi_flags_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__gsi_in_w) {
        vlSelfRef.milan_datapath__DOT__gsi_flags_ex_w 
            = vlSelfRef.milan_datapath__DOT__gsi_reging_w;
        vlSelfRef.milan_datapath__DOT__gsi_flags_w 
            = (0x80000000U | ((((IData)(vlSelfRef.milan_datapath__DOT__gsi_setl_w) 
                                << 0x0000001eU) | (
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__gsi_reging_w) 
                                                    << 0x0000001dU) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__gsi_setl_w) 
                                                      << 0x0000001cU))) 
                              | (((IData)(vlSelfRef.milan_datapath__DOT__gsi_tkfail_w) 
                                  << 0x0000001bU) | 
                                 (((IData)(vlSelfRef.milan_datapath__DOT__gsi_bnd_w) 
                                   << 0x0000001aU) 
                                  | (((IData)(vlSelfRef.milan_datapath__DOT__gsi_setl_w) 
                                      << 0x00000019U) 
                                     | ((((IData)(vlSelfRef.milan_datapath__DOT__gsi_tkfail_w) 
                                          << 6U) | 
                                         (((IData)(vlSelfRef.milan_datapath__DOT__gsi_bnd_w) 
                                           & (~ ((4U 
                                                  >= 
                                                  (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                 && (1U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_aecp_strm_started_w) 
                                                        >> 
                                                        (7U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))))))) 
                                          << 3U)) | 
                                        (6U & ((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__gsi_bnd_w))) 
                                               << 1U))))))));
    } else if (vlSelfRef.milan_datapath__DOT__gsi_out_w) {
        vlSelfRef.milan_datapath__DOT__gsi_flags_ex_w 
            = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__gsi_lreg_w)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__gsi_decl_w));
        vlSelfRef.milan_datapath__DOT__gsi_flags_w 
            = (0xa0000000U | ((((IData)(vlSelfRef.milan_datapath__DOT__gsi_decl_w) 
                                << 0x0000001eU) | ((IData)(vlSelfRef.milan_datapath__DOT__gsi_decl_w) 
                                                   << 0x0000001cU)) 
                              | (((IData)(vlSelfRef.milan_datapath__DOT__gsi_ofail_w) 
                                  << 0x0000001bU) | 
                                 (((IData)(vlSelfRef.milan_datapath__DOT__gsi_decl_w) 
                                   << 0x00000019U) 
                                  | (((IData)(vlSelfRef.milan_datapath__DOT__gsi_decl_w) 
                                      & (1U == (IData)(vlSelfRef.milan_datapath__DOT__gsi_lreg_w))) 
                                     << 6U)))));
    }
    vlSelfRef.milan_datapath__DOT__pp_amap_edit_data_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_context_w 
        = (((((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_txn_active_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r) 
                 == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_remove_r))) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r) 
                == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_type_r))) 
            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
               == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_index_r))) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r) 
              == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_count_r)));
    vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w 
        = vlSelfRef.milan_datapath__DOT__amap_edit_context_w;
    if ((0x000fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) {
        vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_context_w) 
               & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)));
        if ((1U & (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                   & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 8U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 9U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0aU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0bU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0cU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0dU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0eU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x0fU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 1U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x10U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x11U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x12U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x13U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x14U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x15U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x16U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x17U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 2U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x18U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x19U) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x1aU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x1bU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x1cU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x1dU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if ((1U & ((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                    >> 0x1eU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
        if (((vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
              >> 0x0000001fU) & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                 >> 3U))) {
            vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__amap_edit_accept_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_in_key_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_key_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_in_key_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_key_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_in_word_w 
        = (0x00000080U | ((0x00000038U & ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                   >> 0x00000030U)) 
                                          << 3U)) | 
                          (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                         >> 0x00000020U)))));
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r;
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i 
        = (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                  >> 0x00000010U)));
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0U;
    if (((0U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i)) 
         & (4U > (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
        if ((0U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((1U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((2U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((3U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((4U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((5U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((6U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((7U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((8U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((9U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000aU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000bU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000cU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000dU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000eU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x000fU == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
    }
    if (((1U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i)) 
         & (4U > (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
        if ((0U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((1U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((2U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((3U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((4U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((5U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((6U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((7U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((8U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((9U == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000aU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000bU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000cU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000dU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000eU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000fU == ((IData)(4U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
    }
    if (((2U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i)) 
         & (4U > (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
        if ((0U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((1U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((2U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((3U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((4U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((5U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((6U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((7U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((8U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((9U == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000aU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000bU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000cU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000dU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000eU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000fU == ((IData)(8U) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
    }
    if (((3U == (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__port_i)) 
         & (4U > (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
        if ((0U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((1U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((2U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((3U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((4U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((5U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((6U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((7U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((8U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((9U == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000aU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000bU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000cU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000dU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000eU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
        if ((0x0000000fU == ((IData)(0x0000000cU) + (IData)(__Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__off_i)))) {
            __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r = 0x2000U;
        }
    }
    __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__Vfuncout 
        = __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__r;
    milan_datapath__DOT__amap_edit_out_enc_w = __Vfunc_milan_datapath__DOT__amap_edit_out_encode__6__Vfuncout;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_word_w 
        = (0x00001fffU & (IData)(milan_datapath__DOT__amap_edit_out_enc_w));
    vlSelfRef.milan_datapath__DOT__amap_edit_in_live_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_live_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_w = 0U;
    vlSelfRef.milan_datapath__DOT__amap_edit_out_cluster_w = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ikey_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__okey_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ibase_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__iexpect_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__obase_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c = 0U;
    milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 0U;
        milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 4U;
    }
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 4U;
        milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 4U;
    }
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 8U;
        milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 4U;
    }
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c = 0x0000000cU;
        milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c = 4U;
    }
    if ((IData)(((0ULL == (0xffff000000000000ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r)) 
                       | ((0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                          < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_in_w[0U] 
                             >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 1U;
    }
    if ((IData)(((0x0001000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r) 
                           >> 1U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_in_w[2U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 1U;
    }
    if ((IData)(((0x0002000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r) 
                           >> 2U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_in_w[4U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 1U;
    }
    if ((IData)(((0x0003000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r) 
                           >> 3U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_in_w[6U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c = 1U;
    }
    if ((IData)(((0ULL == (0xffff000000000000ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r)) 
                       | ((0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                          < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_out_w[0U] 
                             >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 1U;
    }
    if ((IData)(((0x0001000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r) 
                           >> 1U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_out_w[2U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 1U;
    }
    if ((IData)(((0x0002000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r) 
                           >> 2U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_out_w[4U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 1U;
    }
    if ((IData)(((0x0003000000000000ULL == (0xffff000000000000ULL 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)) 
                 & ((4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U)))) 
                    & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r) 
                           >> 3U)) | ((0x0000ffffU 
                                       & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000020U))) 
                                      < (vlSelfRef.milan_datapath__DOT__pp_aecp_fmt_out_w[6U] 
                                         >> 0x00000016U))))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c = 1U;
    }
    if ((0U == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                       >> 0x00000030U))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w));
    }
    if ((1U == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                       >> 0x00000030U))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c 
            = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                     >> 1U));
    }
    if ((2U == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                       >> 0x00000030U))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c 
            = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                     >> 2U));
    }
    if ((3U == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                       >> 0x00000030U))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c 
            = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                     >> 3U));
    }
    if ((((0x000eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
          & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
         & (0x0040U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)))) {
        vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w 
            = (1U & (IData)((0x000000000000000fULL 
                             >> (0x0000003fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)))));
    } else if ((((0x000fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                 & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                & (0x0040U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)))) {
        vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w = 0U;
    }
    if ((((((((0x000eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w)) 
             & (0U == (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)))) 
            & ((0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                       >> 0x00000010U))) 
               < milan_datapath__DOT__amap_edit_validate__DOT__ipcls_c)) 
           & (IData)(milan_datapath__DOT__amap_edit_validate__DOT__istream_ok_c)) 
          & (8U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                          >> 0x00000030U))))) 
         & (8U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                         >> 0x00000020U)))))) {
        milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
            = (milan_datapath__DOT__amap_edit_validate__DOT__ipbase_c 
               + (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                         >> 0x00000010U))));
        if ((0x00000010U > milan_datapath__DOT__amap_edit_validate__DOT__ikey_c)) {
            vlSelfRef.milan_datapath__DOT__amap_edit_in_key_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__amap_edit_in_key_w 
                = (0x0000000fU & milan_datapath__DOT__amap_edit_validate__DOT__ikey_c);
            vlSelfRef.milan_datapath__DOT__amap_edit_in_live_w 
                = (0x000000ffU & (((0U == (0x0000001fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                              << 3U)))
                                    ? 0U : (vlSelfRef.milan_datapath__DOT__amap_in_store_r
                                            [(((IData)(7U) 
                                               + (0x0000007fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                     << 3U))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                      << 3U))))) 
                                  | (vlSelfRef.milan_datapath__DOT__amap_in_store_r
                                     [(3U & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                             >> 2U))] 
                                     >> (0x0000001fU 
                                         & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                            << 3U)))));
            milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c 
                = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iclaim_v_r) 
                         >> (0x0000000fU & milan_datapath__DOT__amap_edit_validate__DOT__ikey_c)));
            milan_datapath__DOT__amap_edit_validate__DOT__ibase_c 
                = (0x000000ffU & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c)
                                   ? (((0U == (0x0000001fU 
                                               & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                  << 3U)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__amap_edit_iclaim_word_r
                                                [(((IData)(7U) 
                                                   + 
                                                   (0x0000007fU 
                                                    & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                       << 3U))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                     << 3U))))) 
                                      | (vlSelfRef.milan_datapath__DOT__amap_edit_iclaim_word_r
                                         [(3U & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                 >> 2U))] 
                                         >> (0x0000001fU 
                                             & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                << 3U))))
                                   : (((0U == (0x0000001fU 
                                               & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                  << 3U)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__amap_in_store_r
                                                [(((IData)(7U) 
                                                   + 
                                                   (0x0000007fU 
                                                    & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                       << 3U))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                     << 3U))))) 
                                      | (vlSelfRef.milan_datapath__DOT__amap_in_store_r
                                         [(3U & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                 >> 2U))] 
                                         >> (0x0000001fU 
                                             & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                << 3U))))));
            milan_datapath__DOT__amap_edit_validate__DOT__iexpect_c 
                = (0x000000ffU & (((0U == (0x0000001fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                              << 3U)))
                                    ? 0U : (vlSelfRef.milan_datapath__DOT__amap_edit_iclaim_expect_r
                                            [(((IData)(7U) 
                                               + (0x0000007fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                     << 3U))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                                      << 3U))))) 
                                  | (vlSelfRef.milan_datapath__DOT__amap_edit_iclaim_expect_r
                                     [(3U & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                             >> 2U))] 
                                     >> (0x0000001fU 
                                         & (milan_datapath__DOT__amap_edit_validate__DOT__ikey_c 
                                            << 3U)))));
            vlSelfRef.milan_datapath__DOT__amap_edit_accept_w 
                = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r)
                          ? ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c)
                              ? ((0U == (IData)(milan_datapath__DOT__amap_edit_validate__DOT__ibase_c)) 
                                 & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__iexpect_c) 
                                    == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_in_word_w)))
                              : ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__ibase_c) 
                                 == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_in_word_w)))
                          : ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__iclaim_c)
                              ? ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__ibase_c) 
                                 == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_in_word_w))
                              : ((~ ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__ibase_c) 
                                     >> 7U)) | ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__ibase_c) 
                                                == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_in_word_w))))));
        }
    } else if ((((((((0x000fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w)) 
                    & ((IData)(milan_datapath__DOT__amap_edit_out_enc_w) 
                       >> 0x0dU)) & (0U == (0x0000ffffU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r)))) 
                  & (4U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                  >> 0x00000030U))))) 
                 & (8U > (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                 >> 0x00000020U))))) 
                & (IData)(milan_datapath__DOT__amap_edit_validate__DOT__ostream_ok_c))) {
        milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
            = ((0x0007fff8U & ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                        >> 0x00000030U)) 
                               << 3U)) + (0x0000ffffU 
                                          & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                     >> 0x00000020U))));
        if ((0x00000020U > milan_datapath__DOT__amap_edit_validate__DOT__okey_c)) {
            vlSelfRef.milan_datapath__DOT__amap_edit_out_key_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__amap_edit_out_key_w 
                = (0x0000001fU & milan_datapath__DOT__amap_edit_validate__DOT__okey_c);
            if ((0x019fU >= (0x000001ffU & ((IData)(0x0000000dU) 
                                            * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))) {
                vlSelfRef.milan_datapath__DOT__amap_edit_out_live_w 
                    = (0x00001fffU & (((0U == (0x0000001fU 
                                               & ((IData)(0x0000000dU) 
                                                  * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__cmap_flat_w
                                                [(((IData)(0x0000000cU) 
                                                   + 
                                                   (0x000001ffU 
                                                    & ((IData)(0x0000000dU) 
                                                       * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & ((IData)(0x0000000dU) 
                                                     * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))) 
                                      | (vlSelfRef.milan_datapath__DOT__cmap_flat_w
                                         [(0x0000000fU 
                                           & (((IData)(0x0000000dU) 
                                               * milan_datapath__DOT__amap_edit_validate__DOT__okey_c) 
                                              >> 5U))] 
                                         >> (0x0000001fU 
                                             & ((IData)(0x0000000dU) 
                                                * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))));
                milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c 
                    = (0x00001fffU & (((0U == (0x0000001fU 
                                               & ((IData)(0x0000000dU) 
                                                  * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_expect_r
                                                [(((IData)(0x0000000cU) 
                                                   + 
                                                   (0x000001ffU 
                                                    & ((IData)(0x0000000dU) 
                                                       * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & ((IData)(0x0000000dU) 
                                                     * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))) 
                                      | (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_expect_r
                                         [(0x0000000fU 
                                           & (((IData)(0x0000000dU) 
                                               * milan_datapath__DOT__amap_edit_validate__DOT__okey_c) 
                                              >> 5U))] 
                                         >> (0x0000001fU 
                                             & ((IData)(0x0000000dU) 
                                                * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))));
            } else {
                vlSelfRef.milan_datapath__DOT__amap_edit_out_live_w = 0U;
                milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c = 0U;
            }
            vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_v_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__amap_out_owner_v_r 
                         >> (0x0000001fU & milan_datapath__DOT__amap_edit_validate__DOT__okey_c)));
            vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_w 
                = (0x0000ffffU & (((0U == (0x0000001fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                              << 4U)))
                                    ? 0U : (vlSelfRef.milan_datapath__DOT__amap_out_owner_r
                                            [(((IData)(0x0000000fU) 
                                               + (0x000001ffU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                     << 4U))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                      << 4U))))) 
                                  | (vlSelfRef.milan_datapath__DOT__amap_out_owner_r
                                     [(0x0000000fU 
                                       & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                          >> 1U))] 
                                     >> (0x0000001fU 
                                         & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                            << 4U)))));
            vlSelfRef.milan_datapath__DOT__amap_edit_out_cluster_w 
                = (0x0000ffffU & (((0U == (0x0000001fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                              << 4U)))
                                    ? 0U : (vlSelfRef.milan_datapath__DOT__amap_out_cluster_r
                                            [(((IData)(0x0000000fU) 
                                               + (0x000001ffU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                     << 4U))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                      << 4U))))) 
                                  | (vlSelfRef.milan_datapath__DOT__amap_out_cluster_r
                                     [(0x0000000fU 
                                       & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                          >> 1U))] 
                                     >> (0x0000001fU 
                                         & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                            << 4U)))));
            milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c 
                = (1U & (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_v_r 
                         >> (0x0000001fU & milan_datapath__DOT__amap_edit_validate__DOT__okey_c)));
            if (milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c) {
                milan_datapath__DOT__amap_edit_validate__DOT__obase_c 
                    = (0x00001fffU & ((0x019fU >= (0x000001ffU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                       ? (((0U == (0x0000001fU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                            ? 0U : 
                                           (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_word_r
                                            [(((IData)(0x0000000cU) 
                                               + (0x000001ffU 
                                                  & ((IData)(0x0000000dU) 
                                                     * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))) 
                                          | (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_word_r
                                             [(0x0000000fU 
                                               & (((IData)(0x0000000dU) 
                                                   * milan_datapath__DOT__amap_edit_validate__DOT__okey_c) 
                                                  >> 5U))] 
                                             >> (0x0000001fU 
                                                 & ((IData)(0x0000000dU) 
                                                    * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))
                                       : 0U));
                milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c 
                    = (0x0000ffffU & (((0U == (0x0000001fU 
                                               & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                  << 4U)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_cluster_r
                                                [(((IData)(0x0000000fU) 
                                                   + 
                                                   (0x000001ffU 
                                                    & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                       << 4U))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                     << 4U))))) 
                                      | (vlSelfRef.milan_datapath__DOT__amap_edit_oclaim_cluster_r
                                         [(0x0000000fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                              >> 1U))] 
                                         >> (0x0000001fU 
                                             & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                << 4U)))));
            } else {
                milan_datapath__DOT__amap_edit_validate__DOT__obase_c 
                    = (0x00001fffU & ((0x019fU >= (0x000001ffU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                       ? (((0U == (0x0000001fU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c)))
                                            ? 0U : 
                                           (vlSelfRef.milan_datapath__DOT__cmap_flat_w
                                            [(((IData)(0x0000000cU) 
                                               + (0x000001ffU 
                                                  & ((IData)(0x0000000dU) 
                                                     * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & ((IData)(0x0000000dU) 
                                                      * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))) 
                                          | (vlSelfRef.milan_datapath__DOT__cmap_flat_w
                                             [(0x0000000fU 
                                               & (((IData)(0x0000000dU) 
                                                   * milan_datapath__DOT__amap_edit_validate__DOT__okey_c) 
                                                  >> 5U))] 
                                             >> (0x0000001fU 
                                                 & ((IData)(0x0000000dU) 
                                                    * milan_datapath__DOT__amap_edit_validate__DOT__okey_c))))
                                       : 0U));
                milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c 
                    = (0x0000ffffU & (((0U == (0x0000001fU 
                                               & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                  << 4U)))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__amap_out_cluster_r
                                                [(((IData)(0x0000000fU) 
                                                   + 
                                                   (0x000001ffU 
                                                    & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                       << 4U))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                     << 4U))))) 
                                      | (vlSelfRef.milan_datapath__DOT__amap_out_cluster_r
                                         [(0x0000000fU 
                                           & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                              >> 1U))] 
                                         >> (0x0000001fU 
                                             & (milan_datapath__DOT__amap_edit_validate__DOT__okey_c 
                                                << 4U)))));
            }
            vlSelfRef.milan_datapath__DOT__amap_edit_accept_w 
                = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r)
                          ? ((~ (IData)(milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c)) 
                             & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c)
                                 ? (((0U == (IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_c)) 
                                     & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__oexpect_c) 
                                        == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_word_w))) 
                                    & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c) 
                                       == (0x0000ffffU 
                                           & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                      >> 0x00000010U)))))
                                 : ((((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_v_w) 
                                      & ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_w) 
                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                     & ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_cluster_w) 
                                        == (0x0000ffffU 
                                            & (IData)(
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                       >> 0x00000010U))))) 
                                    & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_c) 
                                       == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_word_w)))))
                          : ((~ (IData)(milan_datapath__DOT__amap_edit_validate__DOT__ostreaming_c)) 
                             & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__oclaim_c)
                                 ? (((IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_c) 
                                     == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_word_w)) 
                                    & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_cluster_c) 
                                       == (0x0000ffffU 
                                           & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                      >> 0x00000010U)))))
                                 : ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_v_w)) 
                                    | ((((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_v_w) 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_owner_w) 
                                            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                        & ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_cluster_w) 
                                           == (0x0000ffffU 
                                               & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                          >> 0x00000010U))))) 
                                       & ((IData)(milan_datapath__DOT__amap_edit_validate__DOT__obase_c) 
                                          == (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_word_w))))))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_amap_edit_data_w 
        = ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))
            ? ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))
                ? 0ULL : ((0xfffffffffffffffeULL & vlSelfRef.milan_datapath__DOT__pp_amap_edit_data_w) 
                          | (IData)((IData)(((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))
                                              ? (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_context_w)
                                              : (((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_context_w) 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r) 
                                                     < 
                                                     (0x000000ffU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_count_r)))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_accept_w)))))))
            : ((0xfffffffffffffffeULL & vlSelfRef.milan_datapath__DOT__pp_amap_edit_data_w) 
               | (IData)((IData)(((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))
                                   ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w)) 
                                      || ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_context_w) 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_changed_r)))
                                   : ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_commit_ok_w)
                                       : (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_dynamic_w)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_req_w 
        = (IData)(((0x00030000U == (0x000f0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_27)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_en_w 
        = (IData)(((0x00040000U == (0x000f0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_27)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__in_budget_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_309 = ((1U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)) 
                                                  & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w)) 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w)));
    milan_datapath__DOT__ctlg2_tvalid = ((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r)) 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__v1_pass_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_309) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r) 
              & (((0x00000fffU & ((IData)(1U) + (0x000007ffU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r) 
                                                    - (IData)(0x000eU))))) 
                  >= (0x00000fffU & ((IData)(0x000cU) 
                                     + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)))) 
                 & (0x0240U >= (0x00000fffU & ((IData)(0x000cU) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)))))));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r) 
           | ((IData)(milan_datapath__DOT__ctlg2_tvalid) 
              | (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid)));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid) 
                      & (IData)(milan_datapath__DOT__ctlg2_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r))
                      : (IData)(milan_datapath__DOT__ctlg2_tvalid))));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tready = 
        ((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__gapping_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
            & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel) 
               & ((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r)) 
                  & (IData)(vlSelfRef.m_axis_mac_tx_tready)))));
    vlSelfRef.m_axis_mac_tx_tkeep = (0x000000ffU & 
                                     (((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)
                                        ? (((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
                                             ? (0x0fU 
                                                | (- (IData)(
                                                             (7U 
                                                              != (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r)))))
                                             : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_keep_r)) 
                                           | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r))))
                                        : (((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
                                             ? (0x0fU 
                                                | (- (IData)(
                                                             (7U 
                                                              != (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__beat_r)))))
                                             : (3U 
                                                | (- (IData)(
                                                             (1U 
                                                              & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192))))))) 
                                           | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r))))) 
                                      | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r)))));
    vlSelfRef.m_axis_mac_tx_tlast = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r) 
                                     | ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)
                                         ? (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast)
                                         : (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tlast)));
    vlSelfRef.milan_datapath__DOT__dpcrf_tready = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r) 
                                                        | (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel))) 
                                                      & (IData)(vlSelfRef.m_axis_mac_tx_tready)));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__src_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)
            ? (IData)(milan_datapath__DOT__ctlg2_tvalid)
            : (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid));
    vlSelfRef.m_axis_mac_tx_tdata = (((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel)
                                       ? (((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
                                            ? vlSelfRef.milan_datapath__DOT__maap_tx_tdata
                                            : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_data_r) 
                                          & (- (QData)((IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r)))))))
                                       : (((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
                                            ? (((QData)((IData)(
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
                                                                         << 3U))])))))
                                            : (((QData)((IData)(
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
                                                                                << 3U))))))))))) 
                                          & (- (QData)((IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r)))))))) 
                                     & (- (QData)((IData)(
                                                          (1U 
                                                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r)))))));
    vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tready));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready));
    vlSelfRef.milan_datapath__DOT__aaf_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active) 
         & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                | (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel))) 
            & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready)));
    vlSelfRef.m_axis_mac_tx_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__src_tvalid_w) 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active)));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tready));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
           & (IData)(vlSelfRef.m_axis_mac_tx_tvalid));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tlast) & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted));
    vlSelfRef.milan_datapath__DOT__mac_events_w = (
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__rx_mac_good_w) 
                                                     << 8U) 
                                                    | (0x000000f0U 
                                                       & (IData)(vlSelfRef.i_mac_events))) 
                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w) 
                                                       << 3U) 
                                                      | (7U 
                                                         & (IData)(vlSelfRef.i_mac_events))));
}

void Vmilan_datapath___024root___nba_sequent__TOP__0(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__1(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__2(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__3(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__4(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__5(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__6(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__7(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__8(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__9(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__10(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_sequent__TOP__11(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___nba_comb__TOP__0(Vmilan_datapath___024root* vlSelf);

void Vmilan_datapath___024root___eval_nba(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_nba\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__0(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__1(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__2(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__3(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__4(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__5(vlSelf);
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__6(vlSelf);
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__7(vlSelf);
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__8(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__9(vlSelf);
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_sequent__TOP__10(vlSelf);
        Vmilan_datapath___024root___nba_sequent__TOP__11(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vmilan_datapath___024root___nba_comb__TOP__0(vlSelf);
        Vmilan_datapath___024root___nba_comb__TOP__1(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__12
            vlSelfRef.milan_datapath__DOT__pp_maap_req_ready_w 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r)));
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_ren_r 
                = vlSelfRef.__Vdly__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_ren_r;
            vlSelfRef.milan_datapath__DOT__pp_ack_w 
                = vlSelfRef.__Vdly__milan_datapath__DOT__pp_ack_w;
            vlSelfRef.milan_datapath__DOT__pp_err_w 
                = vlSelfRef.__Vdly__milan_datapath__DOT__pp_err_w;
            vlSelfRef.milan_datapath__DOT__pp_rdata_w 
                = vlSelfRef.__Vdly__milan_datapath__DOT__pp_rdata_w;
        }
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__13
            if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0) {
                vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0] 
                    = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0;
            }
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r 
                = ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tarst_n_r))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n)
                    : 0U);
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n 
                = ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n) 
                   ^ ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n) 
                      >> 1U));
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tarst_n_r 
                = vlSelfRef.__Vdly__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tarst_n_r;
        }
    }
    if ((0x0000000000000010ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__14
            vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ts_counter__DOT__acc[0U];
            vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ts_counter__DOT__acc[1U];
            vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[2U] 
                = vlSelfRef.__Vdly__milan_datapath__DOT__ts_counter__DOT__acc[2U];
        }
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__2
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_ready_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_valid_w));
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n 
                = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r) 
                                  + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_rempty_w)) 
                                     & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_ren_r))));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w = 0U;
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_rel_r))) {
                if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w) 
                           | (0x1fU & ((IData)(1U) 
                                       << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r))));
                }
            }
            vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_n 
                = ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n) 
                   ^ ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n) 
                      >> 1U));
        }
    }
    if ((0x0000000000000011ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__3
            IData/*31:0*/ __Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w;
            __Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w = 0;
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_tsd 
                = ((IData)((vlSelfRef.milan_datapath__DOT__avtprx_fsh2 
                            >> 0x00000020U)) - ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                                                 << 8U) 
                                                | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                                   >> 0x00000018U)));
            __Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                = (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                   - ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                       << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                 >> 0x00000018U)));
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_lt_w 
                = (VL_GTS_III(32, 0U, vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_tsd) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc));
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_et_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc) 
                   & (VL_LTES_III(32, 0U, vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_tsd) 
                      & (0x00b71b00U < vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_tsd)));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
                = ((0xfffffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
                   | ((VL_GTS_III(32, 0U, __Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
                       << 1U) | (VL_LTES_III(32, 0U, __Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
                                 & (__Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                                    > ((IData)(0x00989680U) 
                                       + vlSelfRef.milan_datapath__DOT____Vcellinp__avtp_rx_monitor__pres_ofs_i)))));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
                = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
                   | (__Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                      << 2U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U] 
                = ((__Vinline_0__nba_comb__TOP__3_milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
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
                = ((0x007ffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
                   | (0x007fffffU & (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                                     >> 0x0000001eU)));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U] 
                = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
                   | (0x007fffffU & (((((IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx) 
                                        << 0x00000013U) 
                                       | ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype) 
                                          << 0x0000000bU)) 
                                      | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                                          << 3U) | 
                                         (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tu_bit) 
                                           << 2U) | 
                                          (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tv_bit) 
                                            << 1U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_mr_bit))))) 
                                     << 2U)));
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
                                                        ((((IData)(vlSelfRef.gtx_clk) 
                                                           & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1))) 
                                                          << 4U) 
                                                         | (((((IData)(vlSelfRef.i_ps_clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__1))) 
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
        vlSelfRef.__Vtrigprevexpr___TOP__i_ps_clk__1 
            = vlSelfRef.i_ps_clk;
        vlSelfRef.__Vtrigprevexpr___TOP__gtx_clk__1 
            = vlSelfRef.gtx_clk;
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
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 3> &triggers, const std::string &tag);
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
    vlSelfRef.__VicoFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vmilan_datapath___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("../../../configs/generated/endstation_arty_4x4/../../../hdl/milan/milan_datapath.sv", 64, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vmilan_datapath___024root___eval_phase__ico(vlSelf);
        vlSelfRef.__VicoFirstIteration = 0U;
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vmilan_datapath___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("../../../configs/generated/endstation_arty_4x4/../../../hdl/milan/milan_datapath.sv", 64, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vmilan_datapath___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("../../../configs/generated/endstation_arty_4x4/../../../hdl/milan/milan_datapath.sv", 64, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
    if (VL_UNLIKELY(((vlSelfRef.i_desc_mem_req_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_desc_mem_req_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_desc_mem_rsp_valid 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_desc_mem_rsp_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_desc_mem_rsp_last 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_desc_mem_rsp_last");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_desc_mem_rsp_err 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_desc_mem_rsp_err");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_req_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_req_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_rsp_valid 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_rsp_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_rsp_last 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_rsp_last");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_rsp_err 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_rsp_err");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_wr_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_wr_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_wr_done 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_wr_done");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_resp_mem_wr_err & 0xfeU)))) {
        Verilated::overWidthError("i_resp_mem_wr_err");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_req_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_req_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_rsp_valid 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_rsp_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_rsp_last 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_rsp_last");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_rsp_err & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_rsp_err");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_wr_ready 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_wr_ready");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_wr_done & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_wr_done");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_nvm_mem_wr_err & 0xfeU)))) {
        Verilated::overWidthError("i_nvm_mem_wr_err");
    }
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
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_valid 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_gptp_txrec_valid");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_kind & 0xfeU)))) {
        Verilated::overWidthError("i_gptp_txrec_kind");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_oidx & 0xf000U)))) {
        Verilated::overWidthError("i_gptp_txrec_oidx");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_gen & 0xf0U)))) {
        Verilated::overWidthError("i_gptp_txrec_gen");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_type & 0xf0U)))) {
        Verilated::overWidthError("i_gptp_txrec_type");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txrec_abort 
                      & 0xfeU)))) {
        Verilated::overWidthError("i_gptp_txrec_abort");
    }
    if (VL_UNLIKELY(((vlSelfRef.i_gptp_txseal_ack & 0xfeU)))) {
        Verilated::overWidthError("i_gptp_txseal_ack");
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
}
#endif  // VL_DEBUG
