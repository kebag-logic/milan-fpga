// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

extern const VlUnpacked<CData/*0:0*/, 2> Vsim__ConstPool__TABLE_h1dda76f3_0;

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__7(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfcU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 1U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfbU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 2U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f000ff00ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfeU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 3U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfeU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (4U >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 3U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x00000180c200000eULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x22eaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
          & (0x22eaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 4U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x00000180c2000021ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x88f5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
          & (0x88f5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 4U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_fits_w 
        = ((((IData)(2U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
             [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r]) 
            < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__free_w)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r] 
              < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__waddr_w 
        = (0x000003ffU & ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
                           ? (((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                               [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                : 0U) & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                         - (IData)(1U)))
                           : ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
                               ? (((IData)(1U) + ((4U 
                                                   >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                  [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                   : 0U)) 
                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                     - (IData)(1U)))
                               : (((IData)(2U) + (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r] 
                                                  + 
                                                  (0x0000ffffU 
                                                   & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                      [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r] 
                                                      & (- (IData)(
                                                                   (4U 
                                                                    >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))))))) 
                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                     - (IData)(1U))))));
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready = 0U;
    vlSelfRef.__PVT__builder_rhs_self1 = vlSelfRef.__PVT__soc_adapted_interface_dat_w;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data = 0U;
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready 
            = vlSelfRef.__PVT__add_devices_crossbar_source_ready;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data;
    }
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_grant)))) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready 
            = vlSelfRef.__PVT__add_devices_crossbar_source_ready;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w 
        = ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w
              [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r] 
              | (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r
                 [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w = 
        ((((((((IData)(vlSymsp->TOP.mbx_rx_data) == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
               [(0x0000000fU & ((IData)(0x0fU) + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
              << 3U) | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                         == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                         [(0x0000000fU & ((IData)(0x0eU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                        << 2U)) | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                     == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                     [(0x0000000fU 
                                       & ((IData)(0x0dU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                    << 1U) | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                              [(0x0000000fU 
                                                & ((IData)(0x0cU) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
           << 0x0000000cU) | ((((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                  == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                  [(0x0000000fU & ((IData)(0x0bU) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                 << 3U) | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                            == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                            [(0x0000000fU 
                                              & ((IData)(0x0aU) 
                                                 + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                           << 2U)) 
                               | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                    == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                    [(0x0000000fU & 
                                      ((IData)(9U) 
                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                   << 1U) | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                             == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                             [(0x0000000fU 
                                               & ((IData)(8U) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
                              << 8U)) | (((((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                              [(0x0000000fU 
                                                & ((IData)(7U) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                             << 3U) 
                                            | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [(0x0000000fU 
                                                  & ((IData)(6U) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                               << 2U)) 
                                           | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [(0x0000000fU 
                                                  & ((IData)(5U) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                               << 1U) 
                                              | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                 == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                 [(0x0000000fU 
                                                   & ((IData)(4U) 
                                                      + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
                                          << 4U) | 
                                         (((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                             == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                             [(0x0000000fU 
                                               & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                            << 3U) 
                                           | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                               == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                               [(0x0000000fU 
                                                 & ((IData)(2U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                              << 2U)) 
                                          | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                               == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                               [(0x0000000fU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                              << 1U) 
                                             | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0])))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w 
        = (((((((Vsim__ConstPool__TABLE_h1dda76f3_0
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                 & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                        >> (0x0000000fU & ((IData)(0x0fU) 
                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                    & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                       >> (0x0000000fU & ((IData)(0x0fU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                << 3U) | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                           & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                  >> (0x0000000fU & 
                                      ((IData)(0x0eU) 
                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                              & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                 >> (0x0000000fU & 
                                     ((IData)(0x0eU) 
                                      + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                          << 2U)) | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                       & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                              >> (0x0000000fU 
                                                  & ((IData)(0x0dU) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                          & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                             >> (0x0000000fU 
                                                 & ((IData)(0x0dU) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                      << 1U) | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(0x0cU) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                   & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(0x0cU) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
             << 0x0000000cU) | (((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                    & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                           >> (0x0000000fU 
                                               & ((IData)(0x0bU) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                       & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                          >> (0x0000000fU 
                                              & ((IData)(0x0bU) 
                                                 + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                   << 3U) | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                              & ((~ 
                                                  ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                   >> 
                                                   (0x0000000fU 
                                                    & ((IData)(0x0aU) 
                                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & ((IData)(0x0aU) 
                                                        + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                             << 2U)) 
                                 | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                      [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                      & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                             >> (0x0000000fU 
                                                 & ((IData)(9U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                         & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                            >> (0x0000000fU 
                                                & ((IData)(9U) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                     << 1U) | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                               [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                               & ((~ 
                                                   ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & ((IData)(8U) 
                                                        + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(8U) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
                                << 8U)) | ((((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(7U) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                   & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(7U) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                               << 3U) 
                                              | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                  & ((~ 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(6U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(6U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                 << 2U)) 
                                             | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                  & ((~ 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(5U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(5U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                 << 1U) 
                                                | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(4U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(4U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
                                            << 4U) 
                                           | ((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                 & ((~ 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(3U) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                    & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(3U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                << 3U) 
                                               | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(2U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(2U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                  << 2U)) 
                                              | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(1U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(1U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                  << 1U) 
                                                 | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                    & ((~ 
                                                        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                         >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))) 
                                                       & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                          >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))))));
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__8(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_tx__DOT__occ_w;
    __PVT__KL_mbx__DOT__u_tx__DOT__occ_w = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w 
        = ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
            ? (0x0000ffffU & vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_TX_WORDS_TBL_C
               [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r])
            : 0U);
    __PVT__KL_mbx__DOT__u_tx__DOT__occ_w = (0x0000ffffU 
                                            & (((0x4fU 
                                                 >= 
                                                 (0x0000007fU 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                     << 4U)))
                                                 ? 
                                                (((0U 
                                                   == 
                                                   (0x0000001fU 
                                                    & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                       << 4U)))
                                                   ? 0U
                                                   : 
                                                  (vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w
                                                   [
                                                   (((IData)(0x0000000fU) 
                                                     + 
                                                     (0x0000007fU 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                         << 4U))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                        << 4U))))) 
                                                 | (vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w
                                                    [
                                                    (3U 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                        >> 1U))] 
                                                    >> 
                                                    (0x0000001fU 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                                        << 4U))))
                                                 : 0U) 
                                               - ((4U 
                                                   >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                                   : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__len_w 
        = (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r);
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__rec_words_w 
        = (0x0000ffffU & ((IData)(2U) + (0x00003fffU 
                                         & (((IData)(3U) 
                                             + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__len_w)) 
                                            >> 2U))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_ok_w 
        = ((((((2U == (vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r 
                       >> 0x0000001cU)) & (1U > (0x0000000fU 
                                                 & (vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r 
                                                    >> 0x00000010U)))) 
              & (0x000eU <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__len_w))) 
             & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__len_w) 
                <= ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                     : 0U))) & ((IData)(__PVT__KL_mbx__DOT__u_tx__DOT__occ_w) 
                                <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w))) 
           & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__rec_words_w) 
              <= (IData)(__PVT__KL_mbx__DOT__u_tx__DOT__occ_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w 
        = ((0x1cU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w)) 
           | ((((vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[0U] 
                 >> 0x00000010U) != vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U]) 
               << 1U) | ((0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[0U]) 
                         != vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w 
        = ((0x13U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w)) 
           | ((((vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[1U] 
                 >> 0x00000010U) != vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U]) 
               << 3U) | (((0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[1U]) 
                          != vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U]) 
                         << 2U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w 
        = ((0x0fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w)) 
           | (((0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[2U]) 
               != vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[4U]) 
              << 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__arbiter__DOT__sum 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__last_ch_r) 
           + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w 
        = (7U & ((5U <= vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__arbiter__DOT__sum)
                  ? (vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__arbiter__DOT__sum 
                     - (IData)(5U)) : vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__arbiter__DOT__sum));
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_rd_w 
        = (((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)) 
            & VL_GTES_III(32, 5U, (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r))) 
           & ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w)) 
              && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w) 
                        >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w)))));
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid = 0U;
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid;
    }
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_grant)))) {
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid;
    }
    vlSelfRef.__PVT__builder_rhs_self2 = vlSelfRef.__PVT__soc_adapted_interface_sel;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r)) 
           & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w) 
              & (4U <= (0x0000ffffU & (((IData)(0x0040U) 
                                        - (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_109)) 
                                       & (- (IData)(
                                                    (0x0040U 
                                                     >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_109)))))))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__etype 
        = ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
            ? 2U : ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                     ? 3U : ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                              ? 1U : ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                                       ? 4U : ((4U 
                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                                                ? 8U
                                                : (
                                                   (5U 
                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                                                    ? 6U
                                                    : 
                                                   ((6U 
                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                                                     ? 7U
                                                     : 5U)))))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w0_w 
        = ((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__etype 
            | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w) 
               << 8U)) | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__seq_r) 
                          << 0x00000010U));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex = 0U;
    if ((0x10U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 5U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w;
    }
    if (((0x10U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x20U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 6U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000010U));
    }
    if (((0x20U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x21U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 9U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000020U));
    }
    if (((0x21U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x22U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 0x00000024U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000021U));
    }
    if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w 
            = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
        if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
            if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
                vlSelfRef.__Vfunc_mbx_place_f__238__value 
                    = (0x22U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w));
                vlSelfRef.__Vfunc_mbx_place_f__238__Vfuncout 
                    = (1U & vlSelfRef.__Vfunc_mbx_place_f__238__value);
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
                    = vlSelfRef.__Vfunc_mbx_place_f__238__Vfuncout;
                vlSelfRef.__Vfunc_mbx_place_f__236__value 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype;
                vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_0__mbx_place_f 
                    = (0x0000ffffU & vlSelfRef.__Vfunc_mbx_place_f__236__value);
                vlSelfRef.__Vfunc_mbx_place_f__237__value 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex;
                vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_1__mbx_place_f 
                    = (vlSelfRef.__Vfunc_mbx_place_f__237__value 
                       << 0x00000010U);
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                    = (vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_0__mbx_place_f 
                       | vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_1__mbx_place_f);
            } else {
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                    = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r
                       [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                        : 0U);
            }
        } else {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                    ? ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r
                       [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                        : 0U) : ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r
                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                                  : 0U));
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w 
            = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
        if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r;
        } else {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r
                [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w];
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r
                   [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w] 
                   | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w) 
                      << 0x00000010U));
        }
    } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w 
            = (0x000000ffU & (IData)(vlSymsp->TOP.mbx_domain));
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
            = (IData)((vlSymsp->TOP.mbx_gm_id >> (0x0000003fU 
                                                  & ((IData)(0x20U) 
                                                     + 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w) 
                                                      << 6U)))));
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
            = (IData)(vlSymsp->TOP.mbx_gm_id);
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w 
            = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
            = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)) 
               && (1U & ((IData)(vlSymsp->TOP.mbx_link_up) 
                         >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))));
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__9(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_rhs_self5 = vlSelfRef.__PVT__soc_adapted_interface_we;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__fill_req_w = 
        ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101) 
         & ((1U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
            & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r) 
               != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w = 0U;
    if ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r));
    }
    if ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r));
    }
    if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 1U));
    }
    if ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 1U));
    }
    if ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 2U));
    }
    if ((5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 2U));
    }
    if ((6U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 3U));
    }
    if ((7U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 3U));
    }
    if ((8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 4U));
    }
    if ((9U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 4U));
    }
    if ((0x0aU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 5U));
    }
    if ((0x0bU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 5U));
    }
    if ((0x0cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 6U));
    }
    if ((0x0dU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 6U));
    }
    if ((0x0eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 7U));
    }
    if ((0x0fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 7U));
    }
    if ((0x10U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 8U));
    }
    if ((0x11U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 8U));
    }
    if ((0x12U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 9U));
    }
    if ((0x13U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 9U));
    }
    if ((0x14U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0aU));
    }
    if ((0x15U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0aU));
    }
    if ((0x16U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0bU));
    }
    if ((0x17U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0bU));
    }
    if ((0x18U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0cU));
    }
    if ((0x19U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0cU));
    }
    if ((0x1aU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0dU));
    }
    if ((0x1bU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0dU));
    }
    if ((0x1cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0eU));
    }
    if ((0x1dU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0eU));
    }
    if ((0x1eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                     >> 0x0fU));
    }
    if ((0x1fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w 
            = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                     >> 0x0fU));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w 
        = ((8U > ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                  - (IData)(0x00000012U))) & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w));
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
    vlSelfRef.__PVT__add_devices_master_status_status 
        = (((IData)(vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid) 
            << 1U) | (1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid)) 
                            | (IData)(vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready))));
    vlSelfRef.__PVT__builder_basiclowerer_self = vlSelfRef.__PVT__builder_rhs_self1;
    vlSelfRef.__PVT__add_devices_mmap_bus_dat_r = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    vlSelfRef.__PVT__add_devices_mmap_bus_dat_r 
                        = ((((0x0000ff00U & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                             << 8U)) 
                             | (0x000000ffU & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                               >> 8U))) 
                            << 0x00000010U) | ((0x0000ff00U 
                                                & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                                   >> 8U)) 
                                               | (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                                  >> 0x18U)));
                }
            }
        }
    }
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w)) 
                                                & (4U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w = ((4U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w 
        = (0U != ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                        = (((IData)(vlSymsp->TOP.mbx_tx_ready) 
                            & (3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r))) 
                           & (1U < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r)));
                }
            } else if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w = 1U;
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                = ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)) 
                   || ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r) 
                       & ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r)) 
                          && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w) 
                                    >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r))))));
        } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_rd_w;
        }
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                      >> 2U)))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w 
                        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w;
            }
        }
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__10(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w 
                        = (0x000003ffU & (((IData)(3U) 
                                           + (((4U 
                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                                ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                               [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                                : 0U) 
                                              + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__widx_r))) 
                                          & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w) 
                                             - (IData)(1U))));
                }
            } else if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w 
                    = (0x000003ffU & (((IData)(2U) 
                                       + ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                           ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                          [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                           : 0U)) & 
                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w) 
                                       - (IData)(1U))));
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w 
                = (0x000003ffU & ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))
                                   ? (((IData)(1U) 
                                       + ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                           ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                          [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                           : 0U)) & 
                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ring_words_w) 
                                       - (IData)(1U)))
                                   : (((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r]
                                        : 0U) & (((4U 
                                                   >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r))
                                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_TX_WORDS_TBL_C
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r]
                                                   : 0U) 
                                                 - (IData)(1U)))));
        } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w 
                = (0x000003ffU & (((IData)(1U) + ((4U 
                                                   >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w]
                                                   : 0U)) 
                                  & (((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w))
                                       ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_TX_WORDS_TBL_C
                                      [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w]
                                       : 0U) - (IData)(1U))));
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_bus_ack = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                        vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 1U;
                        vlSelfRef.__PVT__add_devices_mmap_bus_ack = 1U;
                    }
                }
            }
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 1U;
        }
    }
    vlSelfRef.__PVT__builder_csr_data_width = 0U;
    if ((0U != (IData)(vlSelfRef.__PVT__builder_rhs_self2))) {
        vlSelfRef.__PVT__builder_csr_data_width = 0U;
    }
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma11 = 0x0fU;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)))) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma11 
            = (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
                ? (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_be_r)
                : (IData)(vlSelfRef.__PVT__builder_rhs_self2));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U];
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w)
            ? 0ULL : vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U]);
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
          & (7U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
         & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
        if ((0x22U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U] 
                = ((~ (1ULL << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) 
                   & vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U]);
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
                = (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
                   | (0x00000007ffffffffULL & ((QData)((IData)(1U)) 
                                               << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))));
        }
    }
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma8 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)
          ? (6U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))
          : (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
              ? (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_we_r)
              : (IData)(vlSelfRef.__PVT__builder_rhs_self5)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w 
        = (0x000000ffU & ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_mem_r
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w] 
                           >> (0x0000001fU & VL_MULS_III(32, (IData)(8U), 
                                                         (3U 
                                                          & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r))))) 
                          & (- (IData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffffff8U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((8U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 2U) 
                                                     | (((4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 1U) 
                                                        | (0U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffffffc7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0014U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 5U) 
                                                     | (((0x0010U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 4U) 
                                                        | ((0x000cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 3U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffffe3fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0024U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 8U) 
                                                     | (((0x0020U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 7U) 
                                                        | ((0x0018U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 6U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffff1ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0030U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000bU) 
                                                     | (((0x002cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000aU) 
                                                        | ((0x0028U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 9U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffff8fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0060U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000eU) 
                                                     | (((0x0038U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000dU) 
                                                        | ((0x0034U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000cU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffc7fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0074U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000011U) 
                                                     | (((0x0070U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000010U) 
                                                        | ((0x0064U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000fU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffe3ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0048U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000014U) 
                                                     | (((0x0044U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000013U) 
                                                        | ((0x0040U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000012U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffdfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((0x0080U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                     << 0x00000015U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xff3fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w))) 
                                                      << 0x00000017U) 
                                                     | ((0x0084U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                        << 0x00000016U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfeffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w) 
                                                       & (2U 
                                                          != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w))) 
                                                      & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w)) 
                                                     << 0x00000018U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfdffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x00000019U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfbffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001aU));
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__15(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__15\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_interface1_dat_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_wishbone2csr_state)))) {
        vlSelfRef.__PVT__builder_interface1_dat_w = vlSelfRef.__PVT__builder_basiclowerer_self;
    }
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[0U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[0U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
         & (8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[0U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[1U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[1U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
         & (0x0010U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[1U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[2U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[2U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
         & (0x0010U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[2U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[3U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[3U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
         & (8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[3U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[4U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
         & (0x0020U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[4U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/adp970-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__16(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__16\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & ((IData)(1U) + VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/adp970-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & ((IData)(2U) + VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/adp970-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__17(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__17\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_shared_ack = ((((((IData)(vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack) 
                                               | (IData)(vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack)) 
                                              | ((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack) 
                                                 | ((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack) 
                                                    | (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack)))) 
                                             | ((IData)(vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r) 
                                                & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma5))) 
                                            | (IData)(vlSelfRef.__PVT__add_devices_mmap_bus_ack)) 
                                           | (IData)(vlSelfRef.__PVT__builder_interface0_ack));
    if ((0U == vlSelfRef.__PVT__builder_count)) {
        vlSelfRef.__PVT__builder_shared_ack = 1U;
    }
    vlSelfRef.__PVT__builder_interface0_dat_r = 0U;
    if (vlSelfRef.__PVT__builder_wishbone2csr_state) {
        vlSelfRef.__PVT__builder_interface0_dat_r = 0U;
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_csr_data_width)))) {
            vlSelfRef.__PVT__builder_interface0_dat_r 
                = (vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r 
                   | (vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                      | (vlSelfRef.__PVT__builder_csr_bankarray_interface2_bank_bus_dat_r 
                         | (vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r 
                            | (vlSelfRef.__PVT__builder_csr_bankarray_interface4_bank_bus_dat_r 
                               | (vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r 
                                  | vlSelfRef.__PVT__builder_csr_bankarray_interface5_bank_bus_dat_r))))));
        }
    }
    vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1 = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_w_ready = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_ar_ready = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_aw_ready = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1 = 1U;
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_ar_ready = 1U;
                }
            }
        }
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_w_ready = 1U;
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_aw_ready = 1U;
                }
            }
        }
    }
}

extern const VlUnpacked<IData/*31:0*/, 16> Vsim__ConstPool__TABLE_h1e660d21_0;

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__18(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__18\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx_dma__DOT__last_word_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w) 
         & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_wlast));
    vlSelfRef.__PVT__soc_adapted_interface_adr = 0U;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rValid) 
                                                & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_rready));
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 0U;
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_stb = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_cyc = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            vlSelfRef.__PVT__soc_adapted_interface_adr 
                = (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awaddr 
                   >> 2U);
        }
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
    vlSelfRef.__PVT__builder_next_state = vlSelfRef.__PVT__builder_state;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 
                    = (1U & (~ (IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)));
                vlSelfRef.__PVT__builder_next_state 
                    = ((IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)
                        ? 3U : 1U);
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 1U;
                vlSelfRef.__PVT__builder_next_state = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
                vlSelfRef.__PVT__builder_next_state = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) 
                 & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid))) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 
                    = (1U & (~ (IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)));
                vlSelfRef.__PVT__builder_next_state 
                    = ((IData)(vlSelfRef.__PVT__soc_last_ar_aw_n)
                        ? 3U : 1U);
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_arvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 1U;
                vlSelfRef.__PVT__builder_next_state = 1U;
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_awvalid) {
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 1U;
                vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
                vlSelfRef.__PVT__builder_next_state = 3U;
            }
        } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__pBus_bready) {
            vlSelfRef.__PVT__builder_next_state = 0U;
        }
    } else {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
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
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
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
    vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_data_w = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__last_word_w)
          ? (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_data 
             & Vsim__ConstPool__TABLE_h1e660d21_0[vlSelfRef.__PVT__KL_mbx_dma__DOT__tail_be_r])
          : vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_data);
    vlSelfRef.__PVT__builder_rhs_self0 = vlSelfRef.__PVT__soc_adapted_interface_adr;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w = (
                                                   (~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__rerr_r) 
                                                     | ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_resp) 
                                                        >> 1U))) 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w));
    vlSelfRef.__PVT__builder_rhs_self4 = vlSelfRef.__PVT__soc_adapted_interface_stb;
    vlSelfRef.__PVT__builder_rhs_self3 = vlSelfRef.__PVT__soc_adapted_interface_cyc;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)
          ? ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r)
              ? vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_wdata_r
              : vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_data_w)
          : (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
              ? vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_wdata_r
              : vlSelfRef.__PVT__builder_rhs_self1));
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = 0U;
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = ((4U & (IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel)) 
                                              | (((0x40U 
                                                   == 
                                                   (0x0000007fU 
                                                    & (vlSelfRef.__PVT__builder_rhs_self0 
                                                       >> 9U))) 
                                                  << 1U) 
                                                 | (1U 
                                                    & (~ 
                                                       (vlSelfRef.__PVT__builder_rhs_self0 
                                                        >> 0x0fU)))));
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = ((3U & (IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel)) 
                                              | ((0x8200U 
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
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma9 = vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w)))) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma9 
            = (0x00001fffU & (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))
                               ? (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_addr_r)
                               : vlSelfRef.__PVT__builder_rhs_self0));
    }
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
}
