// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__2(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__2\n"); );
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
    vlSelfRef.milan_datapath__DOT__aaf_gate = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                               & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                  & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                      >> 1U) 
                                                     | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate)) 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v)))));
    vlSelfRef.milan_datapath__DOT__ctlf_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel)
          ? (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tlast)
          : (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tlast));
    vlSelfRef.milan_datapath__DOT__ctlf_tx_tvalid = 
        (((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel)
           ? (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid)
           : (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tvalid)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__active));
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wr_n_w 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w) 
                 + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w)) 
            & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w)) 
           | ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w)));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc 
        = ((IData)(vlSelfRef.s_axis_mac_rx_tvalid) 
           & (IData)(vlSelfRef.s_axis_mac_rx_tready));
    vlSelfRef.milan_datapath__DOT__aaf_stream_en_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                    >> 7U) & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                               >> 1U) | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                          | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                             >> 7U)) 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                            >> 7U))))) 
               << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                          & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                              >> 6U) & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                         >> 1U) | (
                                                   ((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                       >> 6U)) 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                      >> 6U))))) 
                         << 2U)) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                      & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                                          >> 5U) & 
                                         ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                           >> 1U) | 
                                          (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                            | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                               >> 5U)) 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                              >> 5U))))) 
                                     << 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                                                   >> 4U) 
                                                  & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                      >> 1U) 
                                                     | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                            >> 4U)) 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                           >> 4U))))))) 
            << 4U) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                         & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                             >> 3U) & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                        >> 1U) | ((
                                                   (~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                      >> 3U)) 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                     >> 3U))))) 
                        << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                   & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                                       >> 2U) & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                  >> 1U) 
                                                 | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                     | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                        >> 2U)) 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                       >> 2U))))) 
                                  << 2U)) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__tctx_en_r) 
                                                   >> 1U) 
                                                  & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                      >> 1U) 
                                                     | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                            >> 1U)) 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_talker_active_v) 
                                                           >> 1U))))) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_gate))));
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
