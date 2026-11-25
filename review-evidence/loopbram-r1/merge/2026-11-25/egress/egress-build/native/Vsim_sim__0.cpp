// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___ico_sequent__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_at_w 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
           | ((IData)(vlSymsp->TOP.mbx_rx_last) & (0x000eU 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))));
}

void Vsim_sim___ico_sequent__TOP__sim__1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__soc_tx_fifo_do_read = (((~ (IData)(vlSelfRef.__PVT__soc_tx_fifo_readable)) 
                                             | (IData)(vlSymsp->TOP.serial_source_ready)) 
                                            & (0U != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
}

void Vsim_sim___ico_sequent__TOP__sim__2(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__word_w 
        = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r 
           | ((IData)(vlSymsp->TOP.mbx_rx_data) << 
              ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r) 
               << 3U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype 
        = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b12_r) 
            << 8U) | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b13_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype 
        = ((0x000eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (IData)(vlSymsp->TOP.mbx_rx_data) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__sub_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (0x0000000fU & (IData)(vlSymsp->TOP.mbx_rx_data))
            : 0U);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
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
}

void Vsim_sim___ico_sequent__TOP__sim__3(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w 
        = ((IData)(vlSymsp->TOP.mbx_rx_valid) & (IData)(vlSymsp->TOP.mbx_rx_ready));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w 
        = ((8U > ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                  - (IData)(0x00000012U))) & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w));
}

void Vsim_sim___ico_sequent__TOP__sim__4(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w = 0U;
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
    }
}

void Vsim_sim___ico_sequent__TOP__sim__5(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0U;
    if (((IData)(vlSymsp->TOP.mbx_link_up) != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 1U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 2U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 3U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 4U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 5U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 6U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 7U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 7U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 8U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 8U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 9U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 9U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0aU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0aU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0bU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0bU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0cU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0cU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0dU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0dU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0eU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0eU;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
            >> 0x0000000fU))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0fU;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 3U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0U;
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 4U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 5U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 6U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U])) 
               & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U]))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 1U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 1U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 1U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 2U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 2U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 2U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 3U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 3U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 3U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 4U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 4U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 4U;
    }
}

void Vsim_sim___ico_sequent__TOP__sim__6(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 5U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 5U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 5U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 6U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 6U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 6U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 7U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 7U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 7U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 8U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 8U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 8U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 9U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 9U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 9U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0aU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0aU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0aU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0bU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0bU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0bU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0cU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0cU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0cU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0dU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0dU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0dU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0eU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0eU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0eU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0fU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0fU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0fU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x10U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x10U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x10U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x11U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x11U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x11U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x12U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x12U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x12U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x13U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x13U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x13U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x14U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x14U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x14U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x15U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x15U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x15U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x16U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x16U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x16U;
    }
}

void Vsim_sim___ico_sequent__TOP__sim__7(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_sequent__TOP__sim__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x17U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x17U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x17U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x18U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x18U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x18U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x19U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x19U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x19U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1aU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1aU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1aU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1bU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1bU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1bU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1cU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1cU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1cU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1dU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1dU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1dU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1eU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1eU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1eU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1fU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1fU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1fU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x20U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x20U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x20U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x21U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x21U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x21U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x22U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x22U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x22U;
    }
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
}

void Vsim_sim___ico_comb__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xf7ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xefffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xdfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0x3fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)) 
                                                       & (4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      << 0x0000001fU) 
                                                     | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                          & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)) 
                                                         & (0U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        << 0x0000001eU)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffffcU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                       & (4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      << 1U) 
                                                     | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                         & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                        & (0U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffffbU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 2U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffff7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 3U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffefU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffdfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 5U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffbfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 6U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffff7fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 7U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffeffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0014U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 8U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffdffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x001cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffbffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0040U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffff7ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0044U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffefffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x004cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffdfffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0050U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffbfffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0060U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000eU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffff7fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0064U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffeffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x006cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000010U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffdffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0070U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000011U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffbffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0074U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000012U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfff7ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0080U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000013U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffefffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0084U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000014U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffdfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0088U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000015U));
}

void Vsim_sim___ico_comb__TOP__sim__1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffbfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x008cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000016U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xff7fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0090U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000017U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfeffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0094U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000018U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfdffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x009cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000019U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfbffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00a0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xf7ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00a4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xefffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xdfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xbfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001eU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0x7fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00ccU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffeU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                     & (0x00d4U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffdU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00d8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 1U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffbU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00dcU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 2U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffff7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 3U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffefU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffdfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 5U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffbfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 6U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffff7fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 7U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffeffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 8U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffdffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffe3ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0108U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000cU) 
                                                     | (((0x0104U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000bU) 
                                                        | ((0x0100U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000aU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffff1fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0114U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000fU) 
                                                     | (((0x0110U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000eU) 
                                                        | ((0x010cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000dU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfff8ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0120U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000012U) 
                                                     | (((0x011cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000011U) 
                                                        | ((0x0118U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000010U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffc7ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x012cU 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000015U) 
                                                     | (((0x0128U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000014U) 
                                                        | ((0x0124U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000013U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfe3fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0138U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000018U) 
                                                     | (((0x0134U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000017U) 
                                                        | ((0x0130U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000016U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xf1ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0144U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000001bU) 
                                                     | (((0x0140U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000001aU) 
                                                        | ((0x013cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000019U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0x8fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0150U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000001eU) 
                                                     | (((0x014cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000001dU) 
                                                        | ((0x0148U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000001cU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0x7fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((0x0154U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                     << 0x0000001fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003fffcU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & ((0x7ffffffeU 
                                                         & ((0x015cU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 1U)) 
                                                        | ((0x7fffffffU 
                                                            & (0x0158U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r))) 
                                                           | ((0x0154U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              >> 1U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003ffe3U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0168U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 4U) 
                                                        | (((0x0164U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 3U) 
                                                           | ((0x0160U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 2U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003ff1fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0174U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 7U) 
                                                        | (((0x0170U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 6U) 
                                                           | ((0x016cU 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 5U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003f8ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0180U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000aU) 
                                                        | (((0x017cU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 9U) 
                                                           | ((0x0178U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 8U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003c7ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x018cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000dU) 
                                                        | (((0x0188U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 0x0000000cU) 
                                                           | ((0x0184U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 0x0000000bU)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x00023fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0198U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000010U) 
                                                        | (((0x0194U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 0x0000000fU) 
                                                           | ((0x0190U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 0x0000000eU)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0001ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & ((0x019cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                        << 0x00000011U)));
    vlSelfRef.__Vfunc_mbx_place_f__161__value = (((
                                                   (vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U] 
                                                    != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U]) 
                                                   << 4U) 
                                                  | (((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U] 
                                                       != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                      << 3U) 
                                                     | ((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U] 
                                                         != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]) 
                                                        << 2U))) 
                                                 | (((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U] 
                                                      != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                     << 1U) 
                                                    | (vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U] 
                                                       != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])));
}

void Vsim_sim___ico_comb__TOP__sim__2(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_place_f__162__value;
    __Vfunc_mbx_place_f__162__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__163__value;
    __Vfunc_mbx_place_f__163__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__164__value;
    __Vfunc_mbx_place_f__164__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__165__value;
    __Vfunc_mbx_place_f__165__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__166__value;
    __Vfunc_mbx_place_f__166__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__167__value;
    __Vfunc_mbx_place_f__167__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__168__value;
    __Vfunc_mbx_place_f__168__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__169__value;
    __Vfunc_mbx_place_f__169__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__170__value;
    __Vfunc_mbx_place_f__170__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__171__value;
    __Vfunc_mbx_place_f__171__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__172__value;
    __Vfunc_mbx_place_f__172__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__173__value;
    __Vfunc_mbx_place_f__173__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__174__value;
    __Vfunc_mbx_place_f__174__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__175__value;
    __Vfunc_mbx_place_f__175__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__177__value;
    __Vfunc_mbx_place_f__177__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__178__value;
    __Vfunc_mbx_place_f__178__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__179__value;
    __Vfunc_mbx_place_f__179__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__180__value;
    __Vfunc_mbx_place_f__180__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__181__value;
    __Vfunc_mbx_place_f__181__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__182__value;
    __Vfunc_mbx_place_f__182__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__183__value;
    __Vfunc_mbx_place_f__183__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__184__value;
    __Vfunc_mbx_place_f__184__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__185__value;
    __Vfunc_mbx_place_f__185__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__186__value;
    __Vfunc_mbx_place_f__186__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__187__value;
    __Vfunc_mbx_place_f__187__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__188__value;
    __Vfunc_mbx_place_f__188__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__189__value;
    __Vfunc_mbx_place_f__189__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__190__value;
    __Vfunc_mbx_place_f__190__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__191__value;
    __Vfunc_mbx_place_f__191__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__192__value;
    __Vfunc_mbx_place_f__192__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__193__value;
    __Vfunc_mbx_place_f__193__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__194__value;
    __Vfunc_mbx_place_f__194__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__195__value;
    __Vfunc_mbx_place_f__195__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__196__value;
    __Vfunc_mbx_place_f__196__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__197__value;
    __Vfunc_mbx_place_f__197__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__198__value;
    __Vfunc_mbx_place_f__198__value = 0;
    // Body
    vlSelfRef.KL_mbx__DOT____VlemCall_161__mbx_place_f 
        = (0x000000ffU & vlSelfRef.__Vfunc_mbx_place_f__161__value);
    __Vfunc_mbx_place_f__162__value = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                                       != (0x0000ffffU 
                                           & vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r));
    vlSelfRef.KL_mbx__DOT____VlemCall_162__mbx_place_f 
        = (0x00000100U & (__Vfunc_mbx_place_f__162__value 
                          << 8U));
    __Vfunc_mbx_place_f__163__value = vlSelfRef.__PVT__KL_mbx__DOT__err_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_163__mbx_place_f 
        = (__Vfunc_mbx_place_f__163__value << 0x0000001fU);
    __Vfunc_mbx_place_f__164__value = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_164__mbx_place_f 
        = __Vfunc_mbx_place_f__164__value;
    __Vfunc_mbx_place_f__165__value = vlSymsp->TOP.mbx_link_up;
    vlSelfRef.KL_mbx__DOT____VlemCall_165__mbx_place_f 
        = (0x0000000fU & __Vfunc_mbx_place_f__165__value);
    __Vfunc_mbx_place_f__166__value = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_166__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__166__value);
    __Vfunc_mbx_place_f__167__value = vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_167__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__167__value);
    __Vfunc_mbx_place_f__168__value = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_168__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__168__value);
    __Vfunc_mbx_place_f__169__value = (IData)(vlSymsp->TOP.mbx_gm_id);
    vlSelfRef.KL_mbx__DOT____VlemCall_169__mbx_place_f 
        = __Vfunc_mbx_place_f__169__value;
    __Vfunc_mbx_place_f__170__value = vlSelfRef.__PVT__KL_mbx__DOT__gm_hi_snap_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_170__mbx_place_f 
        = __Vfunc_mbx_place_f__170__value;
    __Vfunc_mbx_place_f__171__value = vlSelfRef.__PVT__KL_mbx__DOT__domain_snap_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_171__mbx_place_f 
        = (0x000000ffU & __Vfunc_mbx_place_f__171__value);
    __Vfunc_mbx_place_f__172__value = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                             >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r)));
    vlSelfRef.KL_mbx__DOT____VlemCall_172__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__172__value);
    __Vfunc_mbx_place_f__173__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_173__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__173__value);
    __Vfunc_mbx_place_f__174__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_174__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__174__value);
    __Vfunc_mbx_place_f__175__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_175__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__175__value << 1U));
    vlSelfRef.__Vfunc_mbx_place_f__176__value = ((0U 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                 && (1U 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r) 
                                                        >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_176__mbx_place_f 
        = (4U & (vlSelfRef.__Vfunc_mbx_place_f__176__value 
                 << 2U));
    if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))) {
        __Vfunc_mbx_place_f__177__value = vlSelfRef.__PVT__KL_mbx__DOT__ctr_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__181__value = vlSelfRef.__PVT__KL_mbx__DOT__amap_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__185__value = vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__189__value = vlSelfRef.__PVT__KL_mbx__DOT__gsi_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
    } else {
        __Vfunc_mbx_place_f__177__value = 0U;
        __Vfunc_mbx_place_f__181__value = 0U;
        __Vfunc_mbx_place_f__185__value = 0U;
        __Vfunc_mbx_place_f__189__value = 0U;
    }
    vlSelfRef.KL_mbx__DOT____VlemCall_177__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__177__value 
                          << 8U));
    __Vfunc_mbx_place_f__178__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_178__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__178__value);
    __Vfunc_mbx_place_f__179__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_179__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__179__value << 1U));
    __Vfunc_mbx_place_f__180__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_180__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__180__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_181__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__181__value 
                          << 8U));
    __Vfunc_mbx_place_f__182__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_182__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__182__value);
    __Vfunc_mbx_place_f__183__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_183__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__183__value << 1U));
    __Vfunc_mbx_place_f__184__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_184__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__184__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_185__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__185__value 
                          << 8U));
    __Vfunc_mbx_place_f__186__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_186__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__186__value);
    __Vfunc_mbx_place_f__187__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_187__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__187__value << 1U));
    __Vfunc_mbx_place_f__188__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_188__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__188__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_189__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__189__value 
                          << 8U));
    __Vfunc_mbx_place_f__190__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_190__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__190__value);
    __Vfunc_mbx_place_f__191__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_191__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__191__value);
    __Vfunc_mbx_place_f__192__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_192__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__192__value);
    __Vfunc_mbx_place_f__193__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_193__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__193__value);
    __Vfunc_mbx_place_f__194__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_194__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__194__value);
    __Vfunc_mbx_place_f__195__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_195__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__195__value);
    __Vfunc_mbx_place_f__196__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_196__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__196__value);
    __Vfunc_mbx_place_f__197__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_197__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__197__value);
    __Vfunc_mbx_place_f__198__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_198__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__198__value);
    vlSelfRef.__Vfunc_mbx_place_f__199__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U];
}
