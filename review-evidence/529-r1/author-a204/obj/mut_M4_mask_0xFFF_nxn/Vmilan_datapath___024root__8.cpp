// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*6:0*/, 64> Vmilan_datapath__ConstPool__TABLE_hdd8b0743_0;

void Vmilan_datapath___024root___nba_comb__TOP__0(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_comb__TOP__0\n"); );
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_swallow_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r) 
           & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_309 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
                                                  & (0U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wptr_r) 
              != (0x40U ^ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
           & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w) 
                 & (0x000eU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)))));
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
         & (5U > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
              ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_tu_w)
              : (IData)(vlSelfRef.milan_datapath__DOT__crft_tu_last_w))) {
            if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w) 
                       | (0x1fU & ((IData)(1U) << (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_mr_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__crft_mr_last_w));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
              | (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
                      & (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r))));
    vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c 
        = vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_r;
    if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
        vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_hi_r) 
            << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r;
    vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    vlSelfRef.milan_datapath__DOT__gsi_lreg_w = (3U 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                                                     >> 
                                                     (0x0000000eU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                         << 1U))) 
                                                    & (- (IData)(
                                                                 (9U 
                                                                  >= 
                                                                  (0x0000000eU 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                                      << 1U)))))));
    vlSelfRef.milan_datapath__DOT__gsi_decl_w = ((4U 
                                                  >= 
                                                  (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                     >> 
                                                     (7U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_pend_r) 
           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r)));
    vlSelfRef.milan_datapath__DOT__sfv_base_ok_w = 
        ((~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                     >> 0x00000034U))) & ((0xffefffff003fffffULL 
                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                          == (0xffefffff003fffffULL 
                                              & vlSelfRef.milan_datapath__DOT__sfv_decl_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
          & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) 
         & (5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f0010000ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f000ff00ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__132__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c200000eULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__133__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c2000021ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__m 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__m 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__ctr_avb_link_edge_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctr_link_q_r) 
           != (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__gsi_ofail_w = ((2U 
                                                   == 
                                                   (3U 
                                                    & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w) 
                                                        >> 
                                                        (0x0000000eU 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                            << 1U))) 
                                                       & (- (IData)(
                                                                    (9U 
                                                                     >= 
                                                                     (0x0000000eU 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                                         << 1U)))))))) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[0U] = 4U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[1U] 
        = (0x00000080U | (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__mr_r) 
                           << 3U) | (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__tu_r)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[2U] 
        = vlSelfRef.milan_datapath__DOT__crf_tx__DOT__seq_r;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[3U] = 1U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000038U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[5U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000030U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__eff_crft_sid_w));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[12U] = 0U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[13U] = 0U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[14U] = 0xbbU;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[15U] = 0x80U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[16U] = 0U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[17U] = 8U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[18U] = 0U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[19U] = 0x60U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[20U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000038U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[21U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000030U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[25U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[27U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__ts_r));
    if (vlSelfRef.milan_datapath__DOT__amap_edit_iwr_p_r) {
        vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i 
            = vlSelfRef.milan_datapath__DOT__amap_edit_iwr_word_r;
        vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_addr_r));
    } else {
        vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i 
            = ((((2U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                        >> 0x0000000eU)) | (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                                                  >> 0x0000000cU))) 
                << 6U) | ((0x00000038U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                                          >> 1U)) | 
                          (7U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word)));
        vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i 
            = (0x0000000fU & Vmilan_datapath__ConstPool__TABLE_hdd8b0743_0
               [(0x0000003fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel)]);
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_valid_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
                : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S)) 
                   && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_299 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__gsi_req_q_r)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))
            ? ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_need_r)))) 
               && (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r))))
            : ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r)) 
               && (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i 
        = (((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_p_r) 
            & (0x0aU > (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_addr_r))) 
           | ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_txn_active_r)) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r)) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_wr_p) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_p_r)) 
                       & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                              >> 8U)) & ((Vmilan_datapath__ConstPool__TABLE_hdd8b0743_0
                                          [(0x0000003fU 
                                            & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel)] 
                                          >> 6U) & 
                                         (0x0aU > (0x0000003fU 
                                                   & Vmilan_datapath__ConstPool__TABLE_hdd8b0743_0
                                                   [
                                                   (0x0000003fU 
                                                    & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel)])))))))));
    vlSelfRef.milan_datapath__DOT__ctr_sel_match_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__ctrq_type_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__ctrq_index_r) 
               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__ctrq_word_r) 
                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_word_w))));
    vlSelfRef.milan_datapath__DOT__amap_sel_match_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__amapq_type_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__amapq_index_r) 
               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
              & (((IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r) 
                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r)) 
                 & (((IData)(vlSelfRef.milan_datapath__DOT__amapq_sel_r) 
                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_sel_w)) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__amapq_rec_r) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r))))));
    vlSelfRef.milan_datapath__DOT__gsi_sel_match_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_kind_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_type_r) 
               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
              & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                 & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_sel_r) 
                     == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_ord_r) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r))))));
    vlSelfRef.milan_datapath__DOT__gsi_bnd_w = ((4U 
                                                 >= 
                                                 (7U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                    >> 
                                                    (7U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w)));
    vlSelfRef.milan_datapath__DOT__gsi_tkfail_w = (
                                                   (2U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__gsi_tkreg_w)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w));
    vlSelfRef.milan_datapath__DOT__gsi_reging_w = (
                                                   (0U 
                                                    != (IData)(vlSelfRef.milan_datapath__DOT__gsi_tkreg_w)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w));
    vlSelfRef.milan_datapath__DOT__aaf_stream_en_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_resv_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_raw_w));
    vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_r) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__crf_dirty_p_w) 
               << 4U) | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w)));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w 
        = (1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                     >> 0x00000013U)) & ((0x00040000U 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                          ? (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_we_r) 
                                                | (0U 
                                                   != 
                                                   (0x00030000U 
                                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r))))
                                          : ((0x00020000U 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                              ? ((0x00010000U 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                  ? 
                                                 (0U 
                                                  == 
                                                  (0x000000ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                                                      >> 8U)))
                                                  : 
                                                 (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_we_r)))
                                              : ((0x00010000U 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                  ? 
                                                 (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_we_r))
                                                  : 
                                                 ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_we_r)) 
                                                  | (~ (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i))))))));
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
                                                   != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41))))) 
                                    << 0x00000014U) 
                                   | ((((IData)(vlSelfRef.milan_datapath__DOT__crft_vid_w) 
                                        & (- (IData)(
                                                     (0U 
                                                      != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41))))) 
                                       << 8U) | (((IData)(vlSelfRef.milan_datapath__DOT__crft_emit_en_w) 
                                                  << 7U) 
                                                 | ((0x00000040U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                        << 2U)) 
                                                    | (((0U 
                                                         != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)) 
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
                                    = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_gate) 
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
