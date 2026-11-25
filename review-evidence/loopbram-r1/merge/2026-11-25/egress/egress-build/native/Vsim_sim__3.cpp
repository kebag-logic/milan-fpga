// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___nba_sequent__TOP__sim__16(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__16\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_field_f__56__word;
    __Vfunc_mbx_field_f__56__word = 0;
    IData/*31:0*/ __Vfunc_mbx_field_f__57__word;
    __Vfunc_mbx_field_f__57__word = 0;
    IData/*31:0*/ __Vfunc_mbx_field_f__58__word;
    __Vfunc_mbx_field_f__58__word = 0;
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__amap_done_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_done_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v0 = 1U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r) {
            if ((0x00000040U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__amap_wait_r[0U]))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r = 1U;
            }
            vlSelfRef.__VdlyVal__KL_mbx__DOT__amap_wait_r__v1 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_wait_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v1 = 1U;
        }
        __Vfunc_mbx_field_f__56__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.KL_mbx__DOT____VlemCall_56__mbx_field_f 
            = (1U & __Vfunc_mbx_field_f__56__word);
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0068U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_56__mbx_field_f))) {
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__amap_tag_r__v1 
                    = (0x0000000fU & ((IData)(1U) + 
                                      ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__amap_tag_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__face_if_w]
                                        : 0U)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__amap_tag_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v1 = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r 
                    = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r) 
                       | (1U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))));
                vlSelfRef.__PVT__KL_mbx__DOT__amap_done_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_done_r));
                vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__amap_wait_r__v2 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v2 = 1U;
            }
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r) {
            if ((0x00000040U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__gsi_wait_r[0U]))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r = 1U;
            }
            vlSelfRef.__VdlyVal__KL_mbx__DOT__gsi_wait_r__v1 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_wait_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v1 = 1U;
        }
        __Vfunc_mbx_field_f__58__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.KL_mbx__DOT____VlemCall_58__mbx_field_f 
            = (1U & __Vfunc_mbx_field_f__58__word);
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x00d0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_58__mbx_field_f))) {
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__gsi_tag_r__v1 
                    = (0x0000000fU & ((IData)(1U) + 
                                      ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__gsi_tag_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__face_if_w]
                                        : 0U)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__gsi_tag_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v1 = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r 
                    = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r) 
                       | (1U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))));
                vlSelfRef.__PVT__KL_mbx__DOT__gsi_done_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_done_r));
                vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__gsi_wait_r__v2 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v2 = 1U;
            }
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) {
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) 
                  & (0x3fU == (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1))) 
                 & (vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r[0U] 
                    == vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r[0U]))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r = 1U;
                vlSelfRef.__VdlySet__KL_mbx__DOT__edit_data_r__v1 = 1U;
            } else if ((0x00000040U <= ((IData)(1U) 
                                        + vlSelfRef.__PVT__KL_mbx__DOT__edit_wait_r[0U]))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r = 1U;
            }
            vlSelfRef.__VdlyVal__KL_mbx__DOT__edit_wait_r__v1 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_wait_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v1 = 1U;
        }
        __Vfunc_mbx_field_f__57__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.KL_mbx__DOT____VlemCall_57__mbx_field_f 
            = (1U & __Vfunc_mbx_field_f__57__word);
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0098U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_57__mbx_field_f))) {
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__edit_tag_r__v1 
                    = (0x0000000fU & ((IData)(1U) + 
                                      ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__face_if_w]
                                        : 0U)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__edit_tag_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v1 = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r 
                    = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r) 
                       | (1U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))));
                vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r));
                vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__edit_wait_r__v2 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v2 = 1U;
            }
        }
    }
    vlSelfRef.__PVT__builder_csr_bankarray_interface4_bank_bus_dat_r = 0U;
    if ((4U == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                               >> 9U)))) {
        if (((((((((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))) 
                   | (1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                  | (2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                 | (3U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                | (4U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
               | (5U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
              | (6U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
             | (7U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface4_bank_bus_dat_r 
                = ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                    ? vlSelfRef.__PVT__load_storage
                    : ((1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                        ? vlSelfRef.__PVT__reload_storage
                        : ((2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                            ? (IData)(vlSelfRef.__PVT__en_storage)
                            : ((3U == (0x000001ffU 
                                       & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                ? (IData)(vlSelfRef.__PVT__update_value_storage)
                                : ((4U == (0x000001ffU 
                                           & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                    ? vlSelfRef.__PVT__value_status
                                    : ((5U == (0x000001ffU 
                                               & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                        ? (0U == vlSelfRef.__PVT__value)
                                        : ((6U == (0x000001ffU 
                                                   & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                            ? (IData)(vlSelfRef.__PVT__zero_pending)
                                            : (IData)(vlSelfRef.__PVT__enable_storage))))))));
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__17(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__17\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready)) 
               & (~ (IData)(vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid))))) {
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_first 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_first;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_last 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_last;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data;
    }
    vlSelfRef.__PVT__builder_state = vlSelfRef.__PVT__builder_next_state;
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_mis_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__ch_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__last_ch_r = 4U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_c_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_ch_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_seq_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__left_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pw_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v0 = 1U;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_valid = 0U;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_payload_data = 0U;
        vlSelfRef.__PVT__builder_state = 0U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_mis_r 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_r;
        }
        if ((8U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                          >> 2U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r) 
                              >> 1U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r)))) {
                        if ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))) {
                            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v5 
                                = (0x0000ffffU & ((
                                                   (4U 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                                    : 0U) 
                                                  + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__rec_words_w)));
                            vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v5 
                                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
                            vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v5 = 1U;
                        }
                        vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__last_ch_r 
                            = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
                    }
                }
            }
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 0U;
        } else if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                    if ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))) {
                        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__tail_r__v6 
                            = ((0x4fU >= (0x0000007fU 
                                          & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r) 
                                             << 4U)))
                                ? (0x0000ffffU & ((
                                                   (0U 
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
                                                         << 4U)))))
                                : 0U);
                        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__tail_r__v6 
                            = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
                        vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v6 = 1U;
                    }
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 0U;
                    if ((0xffffU != ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                      ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                      : 0U))) {
                        if ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))) {
                            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_tx__DOT__err_r__v5 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + 
                                                  ((4U 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r))
                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r]
                                                    : 0U)));
                            vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_tx__DOT__err_r__v5 
                                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
                            vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__err_r__v5 = 1U;
                        }
                    }
                    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__last_ch_r 
                        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
                } else if (vlSymsp->TOP.mbx_tx_ready) {
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__left_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r) 
                                          - (IData)(1U)));
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r 
                        = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r)));
                    if ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r))) {
                        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 8U;
                    } else if ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r))) {
                        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r 
                            = (0x000001ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__widx_r)));
                        vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 5U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pw_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r = 0U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 6U;
            } else if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_ok_w) 
                        & (0U == (vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w 
                                  >> 0x00000010U)))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__left_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__len_w;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r = 0U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 5U;
            } else {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 7U;
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__w0_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 4U;
            } else if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r) 
                        & ((4U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r)) 
                           && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w) 
                                     >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r)))))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__ch_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 3U;
            } else {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r)));
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_v_r) 
                 & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r)) 
                    | (1U & ((vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w 
                              - (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_seq_r)) 
                             >> 0x0000000fU))))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_ch_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_c_r;
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_seq_r 
                    = (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w);
            }
            if ((6U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 2U;
            }
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_rd_w;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_c_r 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_ch_w;
        } else if ((0U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__pend_w))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r = 1U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r = 1U;
        }
    }
    vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r = 0U;
    if ((0x1dU == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                                  >> 9U)))) {
        if ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage;
        } else if ((1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage;
        } else if ((2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage;
        } else if ((3U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                = (((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r) 
                    << 1U) | (0U != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)));
        }
    }
    vlSelfRef.__PVT__soc_rx_fifo_level0 = vlSelfRef.__Vdly__soc_rx_fifo_level0;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v7;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__18(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__18\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v7;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__19(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__19\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v0;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v1;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v2;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v3;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v4) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v4;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt__DOT__tag_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__tag_r__v16;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r;
    vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack = vlSelfRef.__Vdly__ctrlmemory1_sram2_bus_ack;
    vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack = vlSelfRef.__Vdly__ctrlmemory1_sram3_bus_ack;
    vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack = vlSelfRef.__Vdly__ctrlmemory1_sram4_bus_ack;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_data_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_data_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__amap_data_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__amap_data_r[0U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_data_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__gsi_data_r[0U] = 0ULL;
    }
    vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack = vlSelfRef.__Vdly__ctrlmemory0_sram1_bus_ack;
    vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack = vlSelfRef.__Vdly__ctrlmemory0_sram0_bus_ack;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
        = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_pend_r__v0;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
        = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_seen_r__v0;
    if (vlSelfRef.__VdlySet__sram_bank0__v0) {
        vlSelfRef.__PVT__sram_bank0[vlSelfRef.__VdlyDim0__sram_bank0__v0] 
            = ((0xffffff00U & vlSelfRef.__PVT__sram_bank0
                [vlSelfRef.__VdlyDim0__sram_bank0__v0]) 
               | (IData)(vlSelfRef.__VdlyVal__sram_bank0__v0));
    }
    if (vlSelfRef.__VdlySet__sram_bank0__v1) {
        vlSelfRef.__PVT__sram_bank0[vlSelfRef.__VdlyDim0__sram_bank0__v1] 
            = ((0xffff00ffU & vlSelfRef.__PVT__sram_bank0
                [vlSelfRef.__VdlyDim0__sram_bank0__v1]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank0__v1) 
                  << 8U));
    }
    if (vlSelfRef.__VdlySet__sram_bank0__v2) {
        vlSelfRef.__PVT__sram_bank0[vlSelfRef.__VdlyDim0__sram_bank0__v2] 
            = ((0xff00ffffU & vlSelfRef.__PVT__sram_bank0
                [vlSelfRef.__VdlyDim0__sram_bank0__v2]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank0__v2) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__VdlySet__sram_bank0__v3) {
        vlSelfRef.__PVT__sram_bank0[vlSelfRef.__VdlyDim0__sram_bank0__v3] 
            = ((0x00ffffffU & vlSelfRef.__PVT__sram_bank0
                [vlSelfRef.__VdlyDim0__sram_bank0__v3]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank0__v3) 
                  << 0x00000018U));
    }
    if (vlSelfRef.__VdlySet__sram_bank1__v0) {
        vlSelfRef.__PVT__sram_bank1[vlSelfRef.__VdlyDim0__sram_bank1__v0] 
            = ((0xffffff00U & vlSelfRef.__PVT__sram_bank1
                [vlSelfRef.__VdlyDim0__sram_bank1__v0]) 
               | (IData)(vlSelfRef.__VdlyVal__sram_bank1__v0));
    }
    if (vlSelfRef.__VdlySet__sram_bank1__v1) {
        vlSelfRef.__PVT__sram_bank1[vlSelfRef.__VdlyDim0__sram_bank1__v1] 
            = ((0xffff00ffU & vlSelfRef.__PVT__sram_bank1
                [vlSelfRef.__VdlyDim0__sram_bank1__v1]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank1__v1) 
                  << 8U));
    }
    if (vlSelfRef.__VdlySet__sram_bank1__v2) {
        vlSelfRef.__PVT__sram_bank1[vlSelfRef.__VdlyDim0__sram_bank1__v2] 
            = ((0xff00ffffU & vlSelfRef.__PVT__sram_bank1
                [vlSelfRef.__VdlyDim0__sram_bank1__v2]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank1__v2) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__VdlySet__sram_bank1__v3) {
        vlSelfRef.__PVT__sram_bank1[vlSelfRef.__VdlyDim0__sram_bank1__v3] 
            = ((0x00ffffffU & vlSelfRef.__PVT__sram_bank1
                [vlSelfRef.__VdlyDim0__sram_bank1__v3]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank1__v3) 
                  << 0x00000018U));
    }
    if (vlSelfRef.__VdlySet__sram_bank2__v0) {
        vlSelfRef.__PVT__sram_bank2[vlSelfRef.__VdlyDim0__sram_bank2__v0] 
            = ((0xffffff00U & vlSelfRef.__PVT__sram_bank2
                [vlSelfRef.__VdlyDim0__sram_bank2__v0]) 
               | (IData)(vlSelfRef.__VdlyVal__sram_bank2__v0));
    }
    if (vlSelfRef.__VdlySet__sram_bank2__v1) {
        vlSelfRef.__PVT__sram_bank2[vlSelfRef.__VdlyDim0__sram_bank2__v1] 
            = ((0xffff00ffU & vlSelfRef.__PVT__sram_bank2
                [vlSelfRef.__VdlyDim0__sram_bank2__v1]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank2__v1) 
                  << 8U));
    }
    if (vlSelfRef.__VdlySet__sram_bank2__v2) {
        vlSelfRef.__PVT__sram_bank2[vlSelfRef.__VdlyDim0__sram_bank2__v2] 
            = ((0xff00ffffU & vlSelfRef.__PVT__sram_bank2
                [vlSelfRef.__VdlyDim0__sram_bank2__v2]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank2__v2) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__VdlySet__sram_bank2__v3) {
        vlSelfRef.__PVT__sram_bank2[vlSelfRef.__VdlyDim0__sram_bank2__v3] 
            = ((0x00ffffffU & vlSelfRef.__PVT__sram_bank2
                [vlSelfRef.__VdlyDim0__sram_bank2__v3]) 
               | ((IData)(vlSelfRef.__VdlyVal__sram_bank2__v3) 
                  << 0x00000018U));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__mismatch_r;
    vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r = vlSelfRef.__Vdly__KL_mbx__DOT__bus_err_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__seq_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__seq_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__k_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__head_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v10) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v10;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v11) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v12) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v12;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v13) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U] = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__20(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__20\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v14) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v14;
    }
    vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0 
        = vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited0;
    vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r = vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__own_mac_lo_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__own_mac_lo_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__own_mac_lo_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__own_mac_hi_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__own_mac_hi_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__own_mac_hi_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_talker_decl_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_talker_decl_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_talker_decl_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_talker_decl_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_idle_slope_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_idle_slope_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_idle_slope_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_idle_slope_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_da_gate_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_da_gate_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_da_gate_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_da_gate_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_licence_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_licence_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_licence_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_licence_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sr_domain_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sr_domain_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sr_domain_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sr_domain_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v9;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_hi_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_hi_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_value_hi_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_value_hi_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_lo_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_lo_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_value_lo_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_value_lo_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_ctrl_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_ctrl_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_ctrl_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_ctrl_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_lo_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_lo_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_record_lo_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_record_lo_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_clock_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_clock_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_clock_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_clock_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_lo_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_lo_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_prop_lo_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_prop_lo_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_hi_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_hi_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_record_hi_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_record_hi_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_hi_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_hi_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_prop_hi_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_prop_hi_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_word_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_word_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_ctr_word_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_ctr_word_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_entity_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_entity_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_entity_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_entity_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_req_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_req_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_req_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_req_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_amap_req_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_amap_req_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_amap_req_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_amap_req_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_req_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_req_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_req_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_req_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_aecp_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_aecp_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_aecp_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_aecp_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_req_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_req_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_ctr_req_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_ctr_req_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_sel_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_sel_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_sel_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_sel_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_amap_page_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_amap_page_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_amap_page_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_amap_page_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_beat_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_edit_beat_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_beat_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_beat_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[0U][15U] = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__21(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__21\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_src_sid_lo_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_src_sid_lo_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_src_sid_lo_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_src_sid_hi_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_src_sid_hi_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_src_sid_hi_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_sid_lo_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sid_lo_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sid_lo_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_sid_hi_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sid_hi_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sid_hi_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_nvm_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_nvm_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_nvm_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_nvm_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[0U][15U] = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__22(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__22\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_binding_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_binding_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_binding_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_restore_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_restore_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_restore_r__v1] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_restore_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_hi_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_hi_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_in_hi_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_lo_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_lo_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_in_lo_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_snk_valid_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_snk_valid_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_snk_valid_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[0U][15U] = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__23(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__23\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_lo_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_lo_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_out_lo_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_hi_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_hi_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_out_hi_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_pt_offset_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_pt_offset_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_pt_offset_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[0U][15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r[vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_src_valid_r__v16][vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_src_valid_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_src_valid_r__v16;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v9;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v8;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__24(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__24\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v9;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v9;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_k_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v9;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v10) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v10;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v11) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v11;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v12) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v12;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v13) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v13;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v14) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v14;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v7;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v8;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v9;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v9;
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__pend_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v5;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v6;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v7;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v8;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v9;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v10) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v10;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v11) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v11;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v12) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v12;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v13) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v13;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v14) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v14;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__gm_hi_snap_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__gm_hi_snap_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__gm_hi_snap_r__v1;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__domain_snap_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v1) {
        vlSelfRef.__PVT__KL_mbx__DOT__domain_snap_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__domain_snap_r__v1;
    }
    vlSelfRef.__PVT__soc_tx_fifo_consume = vlSelfRef.__Vdly__soc_tx_fifo_consume;
    if (vlSelfRef.__VdlySet__storage_1__v0) {
        vlSelfRef.__PVT__storage_1[vlSelfRef.__VdlyDim0__storage_1__v0] 
            = vlSelfRef.__VdlyVal__storage_1__v0;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__25(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__25\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_srp_tx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_maap_tx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_aecp_tx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_acmp_tx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_adp_tx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_maap_rx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_aecp_rx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_acmp_rx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_adp_rx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_srp_rx__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt_ring__DOT__mem_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0;
    }
    vlSelfRef.__PVT__soc_bus_errors = vlSelfRef.__Vdly__soc_bus_errors;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v6) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v7) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v8) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v9) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v10) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v11) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v12) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v13) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v14) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[0U] = 8U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[1U] = 0x10U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[2U] = 0x10U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[3U] = 8U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[4U] = 0x20U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v5) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v5;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v6;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v7;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v8;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v9;
    }
    vlSelfRef.__PVT__soc_tx_fifo_level0 = vlSelfRef.__Vdly__soc_tx_fifo_level0;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__armed_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__scan_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[4U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[5U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[6U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[7U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[8U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[9U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[10U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[11U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[12U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[13U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[14U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt__DOT__dl_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__dl_r__v16;
    }
}
