// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___nba_sequent__TOP__sim__26(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__26\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r = vlSelfRef.__Vdly__KL_mbx__DOT__now_ms_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_wait_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_tag_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_wait_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__ctr_wait_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_wait_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__ctr_wait_r__v2] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_tag_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__ctr_tag_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__ctr_tag_r__v1;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r = vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__amap_wait_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__amap_tag_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__amap_wait_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__amap_wait_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__amap_wait_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__amap_wait_r__v2] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__amap_tag_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__amap_tag_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__amap_tag_r__v1;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r = vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_wait_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_tag_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_wait_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__gsi_wait_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_wait_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__gsi_wait_r__v2] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_tag_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__gsi_tag_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__gsi_tag_r__v1;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r = vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r;
    vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1 
        = vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited1;
    vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r = vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__edit_wait_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__edit_data_r[0U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__edit_wait_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__edit_wait_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__edit_wait_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__edit_wait_r__v2] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__edit_data_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__edit_data_r[0U] = 1ULL;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__edit_tag_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__edit_tag_r__v1;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_v_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_c_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_c_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_seq_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_seq_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__widx_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__left_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_ch_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__ch_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r = vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__err_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__err_r__v5] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__err_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v5] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v6] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v6;
    }
    vlSelfRef.__PVT__soc_rx_fifo_wrport_adr = vlSelfRef.__PVT__soc_rx_fifo_produce;
    vlSelfRef.__PVT__soc_tx_fifo_wrport_adr = vlSelfRef.__PVT__soc_tx_fifo_produce;
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_data_o = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r
        [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r];
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_en_o = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r;
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_addr_o = 
        (0x0000003fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                        + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r)));
    vlSelfRef.__PVT__builder_error = 0U;
    if ((0U == vlSelfRef.__PVT__builder_count)) {
        vlSelfRef.__PVT__builder_error = 1U;
    }
    if ((0x0001869fU == vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_cnt)) {
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_ms_cnt = 0U;
        vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick = 1U;
    } else {
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_ms_cnt 
            = (0x0001ffffU & ((IData)(1U) + vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_cnt));
        vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick = 0U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__tmr_deadline_r = 0U;
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_ms_cnt = 0U;
        vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick = 0U;
    } else if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                & (0x0038U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                               << 2U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__tmr_deadline_r 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__27(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__27\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[0U] = (IData)(
                                                            (((QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U]))) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(
                                                                               (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[1U] = (IData)(
                                                            ((((QData)((IData)(
                                                                               (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U]))) 
                                                               << 0x00000020U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U])))) 
                                                             >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[2U] = 
        (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w = ((1U & 
                                               (~ (IData)(vlSymsp->TOP.sys_reset))) 
                                              && (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_w) 
                                                   & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r) 
                                                      & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r)) 
                                                         & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r)) 
                                                            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_fits_w))))) 
                                                  | ((3U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                                                     | (4U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w = ((4U 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                 ? 
                                                ((- (IData)(
                                                            (1U 
                                                             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))))) 
                                                 & (vlSelfRef.__PVT__KL_mbx__DOT__srp_tx_rdata_w 
                                                    & (- (IData)(
                                                                 (1U 
                                                                  & (~ 
                                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r) 
                                                                      >> 1U)))))))
                                                 : 
                                                ((2U 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__maap_tx_rdata_w
                                                   : vlSelfRef.__PVT__KL_mbx__DOT__aecp_tx_rdata_w)
                                                  : 
                                                 ((1U 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__acmp_tx_rdata_w
                                                   : vlSelfRef.__PVT__KL_mbx__DOT__adp_tx_rdata_w)));
    vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r = 0U;
    if (vlSelfRef.__PVT__builder_csr_bankarray_sel_r) {
        vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r 
            = vlSelfRef.__PVT__mem_dat0;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank2_req_re) {
        vlSelfRef.__PVT__storage = (1U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__ack_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__reg_rdata_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r = 0U;
        vlSelfRef.__PVT__storage = 0U;
    } else {
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0018U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r 
                = (1U & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
        }
        if (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i) {
            if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))) 
                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r)) 
                       | (0x0000ffffU & ((1U & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10) 
                                         << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))));
            }
        }
        vlSelfRef.__PVT__KL_mbx__DOT__ack_r = (((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma7) 
                                                & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__reg_rd_w))) 
                                               | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_q_r));
        if (vlSelfRef.__PVT__KL_mbx__DOT__rd_q_r) {
            vlSelfRef.__PVT__KL_mbx__DOT__reg_rdata_r 
                = vlSelfRef.__PVT__KL_mbx__DOT__reg_rdata_w;
        }
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wdata_w;
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__waddr_w;
        vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w = vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r;
        if (vlSelfRef.__PVT__KL_mbx__DOT__reg_rd_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r 
                = ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                   << 2U);
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_wait = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
                vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            }
        }
        if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 = 1U;
            }
        } else if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_source_valid = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_valid = 1U;
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__28(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__28\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__add_devices_mmap_source_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_width = 1U;
        }
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 1U;
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_sink_ready = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
                }
            }
        }
    } else if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
        }
    }
    vlSelfRef.__PVT__builder_interface0_ack = 0U;
    if (vlSelfRef.__PVT__builder_wishbone2csr_state) {
        vlSelfRef.__PVT__builder_interface0_ack = 1U;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_scratch_re) {
        vlSelfRef.__PVT__soc_scratch_storage = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_reset_re) {
        vlSelfRef.__PVT__soc_reset_storage = (3U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__soc_rx_fifo_do_read) {
        vlSelfRef.__PVT__storage_2_dat1 = vlSelfRef.__PVT__storage_2
            [vlSelfRef.__PVT__soc_rx_fifo_consume];
        vlSelfRef.__PVT__soc_rx_fifo_readable = 1U;
    } else if (vlSelfRef.__PVT__soc_rx_clear) {
        vlSelfRef.__PVT__soc_rx_fifo_readable = 0U;
    }
    if (vlSelfRef.__PVT__soc_tx_fifo_do_read) {
        vlSelfRef.__PVT__soc_tx_fifo_readable = 1U;
    } else if (vlSymsp->TOP.serial_source_ready) {
        vlSelfRef.__PVT__soc_tx_fifo_readable = 0U;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_enable_re) {
        vlSelfRef.__PVT__soc_enable_storage = (3U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__soc_scratch_storage = 0x12345678U;
        vlSelfRef.__PVT__soc_reset_storage = 0U;
        vlSelfRef.__PVT__soc_tx_fifo_readable = 0U;
        vlSelfRef.__PVT__soc_rx_fifo_readable = 0U;
        vlSelfRef.__PVT__soc_enable_storage = 0U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_109 = (0x0000ffffU 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                                                     - vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r));
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
        = (((QData)((IData)((0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_base_hi_r))) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__maap_base_lo_r)));
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
}

void Vsim_sim___nba_sequent__TOP__sim__29(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__29\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
}

void Vsim_sim___nba_sequent__TOP__sim__30(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__30\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
}

void Vsim_sim___nba_sequent__TOP__sim__31(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__31\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_tx__DOT__occ_w;
    __PVT__KL_mbx__DOT__u_tx__DOT__occ_w = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w 
        = (0x0000001fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrd_r)
                           ? (VL_MULS_III(32, (IData)(2U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r)) 
                              + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrhi_r))
                           : (VL_MULS_III(32, (IData)(2U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                              + (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r) 
                                       >> 2U)))));
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_clk_divisor_re) {
        vlSelfRef.__PVT__flashboundary_clk_divisor_storage 
            = (0x000003ffU & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_mode_re) {
        vlSelfRef.__PVT__flashboundary_mode_storage 
            = (3U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re) {
        vlSelfRef.__PVT__add_devices_master_phyconfig_storage 
            = (0x00ffffffU & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid)) 
               | (IData)(vlSelfRef.__PVT__add_devices_master_rxtx_we)))) {
        vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid 
            = vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid;
        vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_payload_data 
            = vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_clk_divisor_re) {
        vlSelfRef.__PVT__add_devices_master_clk_divisor_storage 
            = (0x000003ffU & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_clk_divisor_re) {
        vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage 
            = (0x000003ffU & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_cs_re) {
        vlSelfRef.__PVT__add_devices_master_cs_storage 
            = (1U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_dummy_bits_re) {
        vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage 
            = (0x000000ffU & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid)) 
               | (~ (IData)(vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid))))) {
        vlSelfRef.__Vdly__add_devices_tx_pipe_valid_source_valid 
            = vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data 
            = vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len 
            = vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width 
            = vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_update_value_re) {
        vlSelfRef.__PVT__update_value_storage = (1U 
                                                 & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_enable_re) {
        vlSelfRef.__PVT__enable_storage = (1U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__zero_clear) {
        vlSelfRef.__PVT__zero_pending = 0U;
    }
    if (((0U == vlSelfRef.__PVT__value) & (~ (IData)(vlSelfRef.__PVT__zero_trigger_d)))) {
        vlSelfRef.__PVT__zero_pending = 1U;
    }
    vlSelfRef.__Vdly__value = ((IData)(vlSelfRef.__PVT__en_storage)
                                ? ((0U == vlSelfRef.__PVT__value)
                                    ? vlSelfRef.__PVT__reload_storage
                                    : (vlSelfRef.__PVT__value 
                                       - (IData)(1U)))
                                : vlSelfRef.__PVT__load_storage);
    if (vlSelfRef.__PVT__update_value_wr_stb) {
        vlSelfRef.__PVT__value_status = vlSelfRef.__PVT__value;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[0U] = (IData)(
                                                         (((QData)((IData)(
                                                                           (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[3U]) 
                                                                             << 0x00000010U) 
                                                                            | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[2U]))) 
                                                           << 0x00000020U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[1U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[1U] = (IData)(
                                                         ((((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[0U])))) 
                                                          >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[2U] = (0x0000ffffU 
                                                  & vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[4U]);
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid)) 
               | (~ (IData)(vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid))))) {
        vlSelfRef.__Vdly__add_devices_rx_pipe_valid_source_valid 
            = vlSymsp->TOP.flash_rx_valid;
        vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_first = 0U;
        vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_last = 0U;
        vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data 
            = vlSymsp->TOP.flash_rx_data;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__flashboundary_clk_divisor_storage = 8U;
        vlSelfRef.__PVT__flashboundary_mode_storage = 0U;
        vlSelfRef.__PVT__add_devices_master_phyconfig_storage = 0U;
        vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid = 0U;
        vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_payload_data = 0U;
        vlSelfRef.__PVT__add_devices_master_clk_divisor_storage = 0U;
        vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage = 0U;
        vlSelfRef.__PVT__add_devices_master_cs_storage = 0U;
        vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage = 8U;
        vlSelfRef.__Vdly__add_devices_tx_pipe_valid_source_valid = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width = 0U;
        vlSelfRef.__PVT__update_value_storage = 0U;
        vlSelfRef.__PVT__enable_storage = 0U;
        vlSelfRef.__PVT__zero_pending = 0U;
        vlSelfRef.__PVT__value_status = 0U;
        vlSelfRef.__Vdly__value = 0U;
        vlSelfRef.__Vdly__add_devices_rx_pipe_valid_source_valid = 0U;
        vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data = 0U;
    }
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_data = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_resp = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_payload_resp = 0U;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_payload_resp = 0U;
            }
        }
    }
    vlSelfRef.__PVT__soc_adapted_interface_we = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_valid = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_data 
                    = vlSelfRef.__PVT__soc_data;
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_resp = 0U;
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_valid = 1U;
            }
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                vlSelfRef.__PVT__soc_adapted_interface_we = 1U;
            }
        }
    }
    vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_cnt 
        = vlSelfRef.__Vdly__add_devices_stimulusmailbox_ms_cnt;
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
}

void Vsim_sim___nba_sequent__TOP__sim__32(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__32\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
    vlSelfRef.__PVT__soc_rx_fifo_consume = vlSelfRef.__Vdly__soc_rx_fifo_consume;
    if (vlSelfRef.__VdlySet__storage_2__v0) {
        vlSelfRef.__PVT__storage_2[vlSelfRef.__VdlyDim0__storage_2__v0] 
            = vlSelfRef.__VdlyVal__storage_2__v0;
    }
    vlSelfRef.__PVT__soc_rx_clear = 0U;
    if (((IData)(vlSelfRef.__PVT__soc_pending_wr_stb) 
         & ((IData)(vlSelfRef.__PVT__soc_pending_wr_data) 
            >> 1U))) {
        vlSelfRef.__PVT__soc_rx_clear = 1U;
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
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w = 0U;
}

void Vsim_sim___nba_sequent__TOP__sim__33(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__33\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_first;
    __PVT__builder_litespi_tx_mux_source_first = 0;
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_last;
    __PVT__builder_litespi_tx_mux_source_last = 0;
    SData/*9:0*/ __PVT__builder_litespi_tx_mux_source_payload_clk_div;
    __PVT__builder_litespi_tx_mux_source_payload_clk_div = 0;
    CData/*7:0*/ __PVT__builder_litespi_tx_mux_source_payload_mask;
    __PVT__builder_litespi_tx_mux_source_payload_mask = 0;
    // Body
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
    __PVT__builder_litespi_tx_mux_source_first = ((IData)(vlSelfRef.__PVT__builder_litespi_grant) 
                                                  && (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_first));
    __PVT__builder_litespi_tx_mux_source_last = ((IData)(vlSelfRef.__PVT__builder_litespi_grant) 
                                                 && (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_last));
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_width;
        __PVT__builder_litespi_tx_mux_source_payload_mask 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_mask;
        __PVT__builder_litespi_tx_mux_source_payload_clk_div 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_clk_div;
    } else {
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid 
            = vlSelfRef.__PVT__add_devices_mmap_source_valid;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_width;
        __PVT__builder_litespi_tx_mux_source_payload_mask 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_mask;
        __PVT__builder_litespi_tx_mux_source_payload_clk_div 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div;
    }
    vlSelfRef.__PVT__zero_clear = 0U;
    if (((IData)(vlSelfRef.__PVT__pending_wr_stb) & (IData)(vlSelfRef.__PVT__pending_wr_data))) {
        vlSelfRef.__PVT__zero_clear = 1U;
    }
    vlSelfRef.__PVT__builder_rhs_self5 = vlSelfRef.__PVT__soc_adapted_interface_we;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x000003e8U <= ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x0000000aU <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (5U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (5U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x00000014U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U])));
}

void Vsim_sim___nba_sequent__TOP__sim__34(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__34\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (2U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w 
        = (vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r 
           & ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
              & (0x0000000aU <= ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
    vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                        = (((IData)(vlSymsp->TOP.mbx_tx_ready) 
                            & (3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r))) 
                           & (1U < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r)));
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
                vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w = 1U;
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
            vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                = ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)) 
                   || ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r) 
                       & ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r)) 
                          && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w) 
                                    >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r))))));
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
            vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_rd_w;
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
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma5 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ack_r) 
         & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_q_r = ((1U & (~ (IData)(vlSymsp->TOP.sys_reset))) 
                                            && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__reg_rd_w));
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__dst_r = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b12_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b13_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__sub_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r = 0x7fffU;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r = 0x7fffU;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_rd_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_wr_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_cnt_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v0 = 1U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w) {
            if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_at_w) {
                vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w;
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r 
                    = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w) 
                       & ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w)) 
                          && (1U & (vlSelfRef.__PVT__KL_mbx__DOT__filter_en_r 
                                    >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w)))));
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_r 
                    = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w) 
                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)));
            }
            if ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r 
                    = vlSymsp->TOP.mbx_rx_if;
            }
            if (((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r)) 
                 | (IData)(vlSymsp->TOP.mbx_rx_last))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__q_data_r__v4 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__word_w;
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__q_data_r__v4 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r;
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_data_r__v4 = 1U;
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r = 0U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r = 0U;
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r;
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r;
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4 = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_wr_r 
                    = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r)));
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r 
                    = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r)));
            } else {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r 
                    = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r)));
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__word_w;
            }
            if ((0x07ffU != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r 
                    = (0x000007ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)));
            }
            if ((6U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__dst_r 
                    = ((0x0000ffffffffff00ULL & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
                                                 << 8U)) 
                       | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
            }
            if ((0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b12_r 
                    = vlSymsp->TOP.mbx_rx_data;
            }
            if ((0x000dU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b13_r 
                    = vlSymsp->TOP.mbx_rx_data;
            }
            if ((0x000eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__sub_r 
                    = vlSymsp->TOP.mbx_rx_data;
            }
            if ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r 
                    = (0x0000000fU & (IData)(vlSymsp->TOP.mbx_rx_data));
            }
            if (((0x0012U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x001aU > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v15 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[0U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v15 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x00000012U))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7ffeU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7ffdU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7ffbU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7ffeU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7ffdU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7ffbU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v16 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[1U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v16 = 1U;
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v17 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[2U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v17 = 1U;
            }
            if (((0x0022U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x002aU > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v18 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[3U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v18 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x00000022U))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7ff7U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7ff7U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if (((0x002aU <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x0032U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v19 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[4U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v19 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x0000002aU))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7fefU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7fefU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if ((8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v20 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[5U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v20 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7fdfU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7fdfU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if (((0x0012U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x001aU > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v21 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[6U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v21 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x00000012U))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7fbfU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7fbfU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if (((0x001aU <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x0022U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v22 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[7U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v22 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x0000001aU))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7f7fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7f7fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if ((8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v23 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[8U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v23 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7effU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7effU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if (((0x001aU <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                 & (0x0022U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v24 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[9U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v24 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                                                      - (IData)(0x0000001aU))) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7dffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7dffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
            }
            if ((8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v25 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[10U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v25 = 1U;
                if (((IData)(vlSymsp->TOP.mbx_rx_data) 
                     != (0x000000ffU & (IData)((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
                                                >> 
                                                (0x0000003fU 
                                                 & (((IData)(7U) 
                                                     - (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                    << 3U))))))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x7bffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x77ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x6fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x5fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r 
                        = (0x3fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r));
                }
                if ((0U != (IData)(vlSymsp->TOP.mbx_rx_data))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x7bffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x77ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x6fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x5fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r 
                        = (0x3fffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r));
                }
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v26 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[11U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v26 = 1U;
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v27 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[12U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v27 = 1U;
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v28 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[13U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v28 = 1U;
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v29 
                    = ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[14U] 
                        << 8U) | (QData)((IData)(vlSymsp->TOP.mbx_rx_data)));
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v29 = 1U;
            }
            if (vlSymsp->TOP.mbx_rx_last) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 1U;
                if ((0x000eU > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r = 1U;
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r = 0U;
                }
            }
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_w) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_rd_r 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r)));
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_fits_w)))) {
                if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r] 
                     >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r = 1U;
                } else {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r = 1U;
                }
            }
        }
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_cnt_r 
            = (7U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r) 
                      + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w) 
                         & ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r)) 
                            | (IData)(vlSymsp->TOP.mbx_rx_last)))) 
                     - (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_w)));
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 2U;
        }
        if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r 
                = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__accept_w)
                    ? 3U : 0U);
        }
        if ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 4U;
        }
        if ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r = 0U;
        }
        if ((((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
              & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__accept_w))) 
             | (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r = 0x7fffU;
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r = 0x7fffU;
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v30 = 1U;
        }
    }
}
