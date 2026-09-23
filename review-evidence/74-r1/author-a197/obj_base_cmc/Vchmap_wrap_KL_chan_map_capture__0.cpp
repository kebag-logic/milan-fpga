// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tdm_pair_valid_i = vlSymsp->TOP.tdm_pair_valid_i;
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__tdm_frame_ev_w = ((IData)(vlSymsp->TOP.tdm_pair_valid_i) 
                                       & (0U == (IData)(vlSymsp->TOP.tdm_pair_slot_i)));
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__1(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__1\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)))))))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__2(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__2\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ lb_tdata_i;
    lb_tdata_i = 0;
    // Body
    lb_tdata_i = vlSymsp->TOP.lb_tdata_i;
    vlSelfRef.__PVT__lb_smp0_w = ((0x00ff0000U & ((IData)(lb_tdata_i) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 8U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000010U)))));
    vlSelfRef.__PVT__lb_smp1_w = ((0x00ff0000U & ((IData)(
                                                          (lb_tdata_i 
                                                           >> 0x00000020U)) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 0x00000028U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000030U)))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__3(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__3\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_tlast_i = vlSymsp->TOP.lb_tlast_i;
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__4(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__4\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_flush_i = vlSymsp->TOP.a_lb_flush_i;
    vlSelfRef.__PVT__flush_clr_w = 0U;
    if ((1U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (1U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (2U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (4U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (8U | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((2U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000010U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000020U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000040U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000080U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((4U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000100U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000200U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000400U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000800U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((8U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00001000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00002000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00004000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00008000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000010U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00010000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00020000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00040000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00080000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000020U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00100000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00200000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00400000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00800000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000040U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x01000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x02000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x04000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x08000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000080U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x10000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x20000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x40000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x80000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__5(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__5\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_tvalid_i = vlSymsp->TOP.lb_tvalid_i;
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__6(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__6\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_wire_chans_i = vlSymsp->TOP.lb_wire_chans_i;
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__7(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__7\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_tuser_i = vlSymsp->TOP.lb_tuser_i;
    vlSelfRef.__PVT__lb_a0_w = (0x0000001fU & (((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                >> 1U) 
                                               + (0x0000001cU 
                                                  & ((IData)(vlSelfRef.lb_tuser_i) 
                                                     << 2U))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__1(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__1\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__beat_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__2(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__2\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__lb_ok_w = ((IData)(vlSelfRef.lb_tvalid_i) 
                                & (8U > (IData)(vlSelfRef.lb_tuser_i)));
    vlSelfRef.__PVT__lb_w0_w = ((8U > (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                & (IData)(vlSelfRef.__PVT__lb_ok_w));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__3(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__3\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__lb_chans_raw_w;
    __PVT__lb_chans_raw_w = 0;
    // Body
    __PVT__lb_chans_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & vlSelfRef.lb_wire_chans_i);
    }
    if ((1U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x18U));
    }
    if ((7U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (vlSelfRef.lb_wire_chans_i 
                                 >> 0x1cU);
    }
    vlSelfRef.__PVT__lb_chans_w = ((0U == (IData)(__PVT__lb_chans_raw_w))
                                    ? 2U : (IData)(__PVT__lb_chans_raw_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__4(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__4\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__prime_set_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (1U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (2U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (4U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (8U | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (1U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000010U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000020U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000040U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000080U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (2U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000100U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000200U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000400U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000800U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (3U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00001000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00002000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00004000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00008000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (4U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00010000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00020000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00040000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00080000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (5U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00100000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00200000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00400000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00800000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (6U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x01000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x02000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x04000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x08000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (7U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x10000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x20000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x40000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x80000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__5(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__5\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    // Body
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU & ((IData)(vlSelfRef.__PVT__lb_pair01_w)
                                                   ? (IData)(vlSelfRef.__PVT__lb_a0_w)
                                                   : 
                                                  (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                    >> 1U) 
                                                   + 
                                                   (0x0000001cU 
                                                    & ((IData)(vlSelfRef.lb_tuser_i) 
                                                       << 2U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__6(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__6\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__7(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__7\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__8(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__8\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__cm1_data_w = ((IData)(vlSelfRef.__PVT__lb_pair01_w)
                                    ? (((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)))
                                    : ((QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)) 
                                       << 0x00000018U));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__9(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__9\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__10(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__10\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_57;
    __VdfgRegularize_h6e95ff9d_0_57 = 0;
    // Body
    __VdfgRegularize_h6e95ff9d_0_57 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_57));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_57)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}

void Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_56;
    __VdfgRegularize_h6e95ff9d_0_56 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_57;
    __VdfgRegularize_h6e95ff9d_0_57 = 0;
    CData/*1:0*/ __Vdly__skid_wp_r;
    __Vdly__skid_wp_r = 0;
    CData/*1:0*/ __Vdly__skid_rp_r;
    __Vdly__skid_rp_r = 0;
    CData/*2:0*/ __Vdly__skid_cnt_r;
    __Vdly__skid_cnt_r = 0;
    CData/*1:0*/ __Vdly__st_r;
    __Vdly__st_r = 0;
    CData/*4:0*/ __Vdly__slot_r;
    __Vdly__slot_r = 0;
    CData/*5:0*/ __Vdly__pop_idx_r;
    __Vdly__pop_idx_r = 0;
    SData/*12:0*/ __VdlyVal__map_r__v0;
    __VdlyVal__map_r__v0 = 0;
    CData/*5:0*/ __VdlyDim0__map_r__v0;
    __VdlyDim0__map_r__v0 = 0;
    CData/*0:0*/ __VdlySet__map_r__v0;
    __VdlySet__map_r__v0 = 0;
    CData/*0:0*/ __VdlySet__map_r__v1;
    __VdlySet__map_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__tdm_hold_r__v0;
    __VdlyVal__tdm_hold_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__tdm_hold_r__v0;
    __VdlyDim0__tdm_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__tdm_hold_r__v0;
    __VdlySet__tdm_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__tdm_hold_r__v1;
    __VdlySet__tdm_hold_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__lb_hold_r__v0;
    __VdlyVal__lb_hold_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__lb_hold_r__v0;
    __VdlyDim0__lb_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v0;
    __VdlySet__lb_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v1;
    __VdlySet__lb_hold_r__v1 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v2;
    __VdlySet__lb_hold_r__v2 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v3;
    __VdlySet__lb_hold_r__v3 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v4;
    __VdlySet__lb_hold_r__v4 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v5;
    __VdlySet__lb_hold_r__v5 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v6;
    __VdlySet__lb_hold_r__v6 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v7;
    __VdlySet__lb_hold_r__v7 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v8;
    __VdlySet__lb_hold_r__v8 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v9;
    __VdlySet__lb_hold_r__v9 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v10;
    __VdlySet__lb_hold_r__v10 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v11;
    __VdlySet__lb_hold_r__v11 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v12;
    __VdlySet__lb_hold_r__v12 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v13;
    __VdlySet__lb_hold_r__v13 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v14;
    __VdlySet__lb_hold_r__v14 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v15;
    __VdlySet__lb_hold_r__v15 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v16;
    __VdlySet__lb_hold_r__v16 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v17;
    __VdlySet__lb_hold_r__v17 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v18;
    __VdlySet__lb_hold_r__v18 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v19;
    __VdlySet__lb_hold_r__v19 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v20;
    __VdlySet__lb_hold_r__v20 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v21;
    __VdlySet__lb_hold_r__v21 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v22;
    __VdlySet__lb_hold_r__v22 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v23;
    __VdlySet__lb_hold_r__v23 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v24;
    __VdlySet__lb_hold_r__v24 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v25;
    __VdlySet__lb_hold_r__v25 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v26;
    __VdlySet__lb_hold_r__v26 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v27;
    __VdlySet__lb_hold_r__v27 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v28;
    __VdlySet__lb_hold_r__v28 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v29;
    __VdlySet__lb_hold_r__v29 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v30;
    __VdlySet__lb_hold_r__v30 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v31;
    __VdlySet__lb_hold_r__v31 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v32;
    __VdlySet__lb_hold_r__v32 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v33;
    __VdlySet__lb_hold_r__v33 = 0;
    CData/*2:0*/ __VdlyVal__q_wr_r__v0;
    __VdlyVal__q_wr_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_wr_r__v0;
    __VdlyDim0__q_wr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v0;
    __VdlySet__q_wr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v1;
    __VdlySet__q_wr_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v2;
    __VdlySet__q_wr_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v3;
    __VdlySet__q_wr_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v4;
    __VdlySet__q_wr_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v5;
    __VdlySet__q_wr_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v6;
    __VdlySet__q_wr_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v7;
    __VdlySet__q_wr_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v8;
    __VdlySet__q_wr_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v9;
    __VdlySet__q_wr_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v10;
    __VdlySet__q_wr_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v11;
    __VdlySet__q_wr_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v12;
    __VdlySet__q_wr_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v13;
    __VdlySet__q_wr_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v14;
    __VdlySet__q_wr_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v15;
    __VdlySet__q_wr_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v16;
    __VdlySet__q_wr_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v17;
    __VdlySet__q_wr_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v18;
    __VdlySet__q_wr_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v19;
    __VdlySet__q_wr_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v20;
    __VdlySet__q_wr_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v21;
    __VdlySet__q_wr_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v22;
    __VdlySet__q_wr_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v23;
    __VdlySet__q_wr_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v24;
    __VdlySet__q_wr_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v25;
    __VdlySet__q_wr_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v26;
    __VdlySet__q_wr_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v27;
    __VdlySet__q_wr_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v28;
    __VdlySet__q_wr_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v29;
    __VdlySet__q_wr_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v30;
    __VdlySet__q_wr_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v31;
    __VdlySet__q_wr_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v32;
    __VdlySet__q_wr_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v33;
    __VdlySet__q_wr_r__v33 = 0;
    CData/*3:0*/ __VdlyVal__q_cnt_r__v0;
    __VdlyVal__q_cnt_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_cnt_r__v0;
    __VdlyDim0__q_cnt_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v0;
    __VdlySet__q_cnt_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__q_cnt_r__v1;
    __VdlyVal__q_cnt_r__v1 = 0;
    CData/*4:0*/ __VdlyDim0__q_cnt_r__v1;
    __VdlyDim0__q_cnt_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v1;
    __VdlySet__q_cnt_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v2;
    __VdlySet__q_cnt_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v3;
    __VdlySet__q_cnt_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v4;
    __VdlySet__q_cnt_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v5;
    __VdlySet__q_cnt_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v6;
    __VdlySet__q_cnt_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v7;
    __VdlySet__q_cnt_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v8;
    __VdlySet__q_cnt_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v9;
    __VdlySet__q_cnt_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v10;
    __VdlySet__q_cnt_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v11;
    __VdlySet__q_cnt_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v12;
    __VdlySet__q_cnt_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v13;
    __VdlySet__q_cnt_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v14;
    __VdlySet__q_cnt_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v15;
    __VdlySet__q_cnt_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v16;
    __VdlySet__q_cnt_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v17;
    __VdlySet__q_cnt_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v18;
    __VdlySet__q_cnt_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v19;
    __VdlySet__q_cnt_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v20;
    __VdlySet__q_cnt_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v21;
    __VdlySet__q_cnt_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v22;
    __VdlySet__q_cnt_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v23;
    __VdlySet__q_cnt_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v24;
    __VdlySet__q_cnt_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v25;
    __VdlySet__q_cnt_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v26;
    __VdlySet__q_cnt_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v27;
    __VdlySet__q_cnt_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v28;
    __VdlySet__q_cnt_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v29;
    __VdlySet__q_cnt_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v30;
    __VdlySet__q_cnt_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v31;
    __VdlySet__q_cnt_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v32;
    __VdlySet__q_cnt_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v33;
    __VdlySet__q_cnt_r__v33 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v34;
    __VdlySet__q_cnt_r__v34 = 0;
    CData/*2:0*/ __VdlyVal__q_rd_r__v0;
    __VdlyVal__q_rd_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_rd_r__v0;
    __VdlyDim0__q_rd_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v0;
    __VdlySet__q_rd_r__v0 = 0;
    CData/*2:0*/ __VdlyVal__q_rd_r__v1;
    __VdlyVal__q_rd_r__v1 = 0;
    CData/*4:0*/ __VdlyDim0__q_rd_r__v1;
    __VdlyDim0__q_rd_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v1;
    __VdlySet__q_rd_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v2;
    __VdlySet__q_rd_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v3;
    __VdlySet__q_rd_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v4;
    __VdlySet__q_rd_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v5;
    __VdlySet__q_rd_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v6;
    __VdlySet__q_rd_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v7;
    __VdlySet__q_rd_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v8;
    __VdlySet__q_rd_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v9;
    __VdlySet__q_rd_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v10;
    __VdlySet__q_rd_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v11;
    __VdlySet__q_rd_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v12;
    __VdlySet__q_rd_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v13;
    __VdlySet__q_rd_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v14;
    __VdlySet__q_rd_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v15;
    __VdlySet__q_rd_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v16;
    __VdlySet__q_rd_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v17;
    __VdlySet__q_rd_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v18;
    __VdlySet__q_rd_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v19;
    __VdlySet__q_rd_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v20;
    __VdlySet__q_rd_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v21;
    __VdlySet__q_rd_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v22;
    __VdlySet__q_rd_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v23;
    __VdlySet__q_rd_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v24;
    __VdlySet__q_rd_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v25;
    __VdlySet__q_rd_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v26;
    __VdlySet__q_rd_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v27;
    __VdlySet__q_rd_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v28;
    __VdlySet__q_rd_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v29;
    __VdlySet__q_rd_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v30;
    __VdlySet__q_rd_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v31;
    __VdlySet__q_rd_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v32;
    __VdlySet__q_rd_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v33;
    __VdlySet__q_rd_r__v33 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v34;
    __VdlySet__q_rd_r__v34 = 0;
    CData/*4:0*/ __VdlyVal__skid_addr_r__v0;
    __VdlyVal__skid_addr_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_addr_r__v0;
    __VdlyDim0__skid_addr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_addr_r__v0;
    __VdlySet__skid_addr_r__v0 = 0;
    CData/*4:0*/ __VdlyVal__skid_addr_r__v1;
    __VdlyVal__skid_addr_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_addr_r__v1;
    __VdlyDim0__skid_addr_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_addr_r__v1;
    __VdlySet__skid_addr_r__v1 = 0;
    CData/*3:0*/ __VdlyVal__skid_strm_r__v0;
    __VdlyVal__skid_strm_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_strm_r__v0;
    __VdlyDim0__skid_strm_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_strm_r__v0;
    __VdlySet__skid_strm_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__skid_strm_r__v1;
    __VdlyVal__skid_strm_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_strm_r__v1;
    __VdlyDim0__skid_strm_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_strm_r__v1;
    __VdlySet__skid_strm_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__lb_q_r__v0;
    __VdlyVal__lb_q_r__v0 = 0;
    CData/*7:0*/ __VdlyDim0__lb_q_r__v0;
    __VdlyDim0__lb_q_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_q_r__v0;
    __VdlySet__lb_q_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__skid_data_r__v0;
    __VdlyVal__skid_data_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_data_r__v0;
    __VdlyDim0__skid_data_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_data_r__v0;
    __VdlySet__skid_data_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__skid_data_r__v1;
    __VdlyVal__skid_data_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_data_r__v1;
    __VdlyDim0__skid_data_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_data_r__v1;
    __VdlySet__skid_data_r__v1 = 0;
    IData/*31:0*/ __Vilp1;
    // Body
    __Vdly__skid_wp_r = vlSelfRef.__PVT__skid_wp_r;
    __VdlySet__tdm_hold_r__v0 = 0U;
    __VdlySet__tdm_hold_r__v1 = 0U;
    __VdlySet__lb_q_r__v0 = 0U;
    __Vdly__skid_cnt_r = vlSelfRef.__PVT__skid_cnt_r;
    __VdlySet__map_r__v0 = 0U;
    __VdlySet__map_r__v1 = 0U;
    __VdlySet__skid_addr_r__v0 = 0U;
    __VdlySet__skid_addr_r__v1 = 0U;
    __Vdly__skid_rp_r = vlSelfRef.__PVT__skid_rp_r;
    __Vdly__st_r = vlSelfRef.__PVT__st_r;
    __Vdly__slot_r = vlSelfRef.__PVT__slot_r;
    __Vdly__pop_idx_r = vlSelfRef.__PVT__pop_idx_r;
    __VdlySet__skid_strm_r__v0 = 0U;
    __VdlySet__skid_strm_r__v1 = 0U;
    __VdlySet__q_wr_r__v0 = 0U;
    __VdlySet__q_wr_r__v1 = 0U;
    __VdlySet__q_wr_r__v2 = 0U;
    __VdlySet__q_wr_r__v3 = 0U;
    __VdlySet__q_wr_r__v4 = 0U;
    __VdlySet__q_wr_r__v5 = 0U;
    __VdlySet__q_wr_r__v6 = 0U;
    __VdlySet__q_wr_r__v7 = 0U;
    __VdlySet__q_wr_r__v8 = 0U;
    __VdlySet__q_wr_r__v9 = 0U;
    __VdlySet__q_wr_r__v10 = 0U;
    __VdlySet__q_wr_r__v11 = 0U;
    __VdlySet__q_wr_r__v12 = 0U;
    __VdlySet__q_wr_r__v13 = 0U;
    __VdlySet__q_wr_r__v14 = 0U;
    __VdlySet__q_wr_r__v15 = 0U;
    __VdlySet__q_wr_r__v16 = 0U;
    __VdlySet__q_wr_r__v17 = 0U;
    __VdlySet__q_wr_r__v18 = 0U;
    __VdlySet__q_wr_r__v19 = 0U;
    __VdlySet__q_wr_r__v20 = 0U;
    __VdlySet__q_wr_r__v21 = 0U;
    __VdlySet__q_wr_r__v22 = 0U;
    __VdlySet__q_wr_r__v23 = 0U;
    __VdlySet__q_wr_r__v24 = 0U;
    __VdlySet__q_wr_r__v25 = 0U;
    __VdlySet__q_wr_r__v26 = 0U;
    __VdlySet__q_wr_r__v27 = 0U;
    __VdlySet__q_wr_r__v28 = 0U;
    __VdlySet__q_wr_r__v29 = 0U;
    __VdlySet__q_wr_r__v30 = 0U;
    __VdlySet__q_wr_r__v31 = 0U;
    __VdlySet__q_wr_r__v32 = 0U;
    __VdlySet__q_wr_r__v33 = 0U;
    __VdlySet__q_rd_r__v0 = 0U;
    __VdlySet__q_rd_r__v1 = 0U;
    __VdlySet__q_rd_r__v2 = 0U;
    __VdlySet__q_rd_r__v3 = 0U;
    __VdlySet__q_rd_r__v4 = 0U;
    __VdlySet__q_rd_r__v5 = 0U;
    __VdlySet__q_rd_r__v6 = 0U;
    __VdlySet__q_rd_r__v7 = 0U;
    __VdlySet__q_rd_r__v8 = 0U;
    __VdlySet__q_rd_r__v9 = 0U;
    __VdlySet__q_rd_r__v10 = 0U;
    __VdlySet__q_rd_r__v11 = 0U;
    __VdlySet__q_rd_r__v12 = 0U;
    __VdlySet__q_rd_r__v13 = 0U;
    __VdlySet__q_rd_r__v14 = 0U;
    __VdlySet__q_rd_r__v15 = 0U;
    __VdlySet__q_rd_r__v16 = 0U;
    __VdlySet__q_rd_r__v17 = 0U;
    __VdlySet__q_rd_r__v18 = 0U;
    __VdlySet__q_rd_r__v19 = 0U;
    __VdlySet__q_rd_r__v20 = 0U;
    __VdlySet__q_rd_r__v21 = 0U;
    __VdlySet__q_rd_r__v22 = 0U;
    __VdlySet__q_rd_r__v23 = 0U;
    __VdlySet__q_rd_r__v24 = 0U;
    __VdlySet__q_rd_r__v25 = 0U;
    __VdlySet__q_rd_r__v26 = 0U;
    __VdlySet__q_rd_r__v27 = 0U;
    __VdlySet__q_rd_r__v28 = 0U;
    __VdlySet__q_rd_r__v29 = 0U;
    __VdlySet__q_rd_r__v30 = 0U;
    __VdlySet__q_rd_r__v31 = 0U;
    __VdlySet__q_rd_r__v32 = 0U;
    __VdlySet__q_rd_r__v33 = 0U;
    __VdlySet__q_rd_r__v34 = 0U;
    __VdlySet__lb_hold_r__v0 = 0U;
    __VdlySet__lb_hold_r__v1 = 0U;
    __VdlySet__lb_hold_r__v2 = 0U;
    __VdlySet__lb_hold_r__v3 = 0U;
    __VdlySet__lb_hold_r__v4 = 0U;
    __VdlySet__lb_hold_r__v5 = 0U;
    __VdlySet__lb_hold_r__v6 = 0U;
    __VdlySet__lb_hold_r__v7 = 0U;
    __VdlySet__lb_hold_r__v8 = 0U;
    __VdlySet__lb_hold_r__v9 = 0U;
    __VdlySet__lb_hold_r__v10 = 0U;
    __VdlySet__lb_hold_r__v11 = 0U;
    __VdlySet__lb_hold_r__v12 = 0U;
    __VdlySet__lb_hold_r__v13 = 0U;
    __VdlySet__lb_hold_r__v14 = 0U;
    __VdlySet__lb_hold_r__v15 = 0U;
    __VdlySet__lb_hold_r__v16 = 0U;
    __VdlySet__lb_hold_r__v17 = 0U;
    __VdlySet__lb_hold_r__v18 = 0U;
    __VdlySet__lb_hold_r__v19 = 0U;
    __VdlySet__lb_hold_r__v20 = 0U;
    __VdlySet__lb_hold_r__v21 = 0U;
    __VdlySet__lb_hold_r__v22 = 0U;
    __VdlySet__lb_hold_r__v23 = 0U;
    __VdlySet__lb_hold_r__v24 = 0U;
    __VdlySet__lb_hold_r__v25 = 0U;
    __VdlySet__lb_hold_r__v26 = 0U;
    __VdlySet__lb_hold_r__v27 = 0U;
    __VdlySet__lb_hold_r__v28 = 0U;
    __VdlySet__lb_hold_r__v29 = 0U;
    __VdlySet__lb_hold_r__v30 = 0U;
    __VdlySet__lb_hold_r__v31 = 0U;
    __VdlySet__lb_hold_r__v32 = 0U;
    __VdlySet__lb_hold_r__v33 = 0U;
    __VdlySet__q_cnt_r__v0 = 0U;
    __VdlySet__q_cnt_r__v1 = 0U;
    __VdlySet__q_cnt_r__v2 = 0U;
    __VdlySet__q_cnt_r__v3 = 0U;
    __VdlySet__q_cnt_r__v4 = 0U;
    __VdlySet__q_cnt_r__v5 = 0U;
    __VdlySet__q_cnt_r__v6 = 0U;
    __VdlySet__q_cnt_r__v7 = 0U;
    __VdlySet__q_cnt_r__v8 = 0U;
    __VdlySet__q_cnt_r__v9 = 0U;
    __VdlySet__q_cnt_r__v10 = 0U;
    __VdlySet__q_cnt_r__v11 = 0U;
    __VdlySet__q_cnt_r__v12 = 0U;
    __VdlySet__q_cnt_r__v13 = 0U;
    __VdlySet__q_cnt_r__v14 = 0U;
    __VdlySet__q_cnt_r__v15 = 0U;
    __VdlySet__q_cnt_r__v16 = 0U;
    __VdlySet__q_cnt_r__v17 = 0U;
    __VdlySet__q_cnt_r__v18 = 0U;
    __VdlySet__q_cnt_r__v19 = 0U;
    __VdlySet__q_cnt_r__v20 = 0U;
    __VdlySet__q_cnt_r__v21 = 0U;
    __VdlySet__q_cnt_r__v22 = 0U;
    __VdlySet__q_cnt_r__v23 = 0U;
    __VdlySet__q_cnt_r__v24 = 0U;
    __VdlySet__q_cnt_r__v25 = 0U;
    __VdlySet__q_cnt_r__v26 = 0U;
    __VdlySet__q_cnt_r__v27 = 0U;
    __VdlySet__q_cnt_r__v28 = 0U;
    __VdlySet__q_cnt_r__v29 = 0U;
    __VdlySet__q_cnt_r__v30 = 0U;
    __VdlySet__q_cnt_r__v31 = 0U;
    __VdlySet__q_cnt_r__v32 = 0U;
    __VdlySet__q_cnt_r__v33 = 0U;
    __VdlySet__q_cnt_r__v34 = 0U;
    __VdlySet__skid_data_r__v0 = 0U;
    __VdlySet__skid_data_r__v1 = 0U;
    if (vlSymsp->TOP.rst_n) {
        __Vdly__skid_wp_r = (3U & ((IData)(vlSelfRef.__PVT__skid_wp_r) 
                                   + (IData)(vlSelfRef.__PVT__skid_enq_n_w)));
        if (((IData)(vlSymsp->TOP.tdm_pair_valid_i) 
             & (4U > (IData)(vlSymsp->TOP.tdm_pair_slot_i)))) {
            __VdlyVal__tdm_hold_r__v0 = (((QData)((IData)(vlSymsp->TOP.tdm_l_i)) 
                                          << 0x00000018U) 
                                         | (QData)((IData)(vlSymsp->TOP.tdm_r_i)));
            __VdlyDim0__tdm_hold_r__v0 = (3U & (IData)(vlSymsp->TOP.tdm_pair_slot_i));
            __VdlySet__tdm_hold_r__v0 = 1U;
        }
        vlSelfRef.__PVT__q_primed_r = ((vlSelfRef.__PVT__q_primed_r 
                                        | vlSelfRef.__PVT__prime_set_w) 
                                       & (~ vlSelfRef.__PVT__flush_clr_w));
        if (vlSelfRef.__PVT__push_ram_w) {
            __VdlyVal__lb_q_r__v0 = vlSelfRef.__PVT__skid_data_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlyDim0__lb_q_r__v0 = (((IData)(vlSelfRef.__PVT__skid_addr_r
                                               [vlSelfRef.__PVT__skid_rp_r]) 
                                       << 3U) | vlSelfRef.__PVT__q_wr_r
                                      [vlSelfRef.__PVT__skid_addr_r
                                      [vlSelfRef.__PVT__skid_rp_r]]);
            __VdlySet__lb_q_r__v0 = 1U;
            __VdlyVal__q_wr_r__v0 = (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__q_wr_r
                                                     [vlSelfRef.__PVT__skid_addr_r
                                                     [vlSelfRef.__PVT__skid_rp_r]])));
            __VdlyDim0__q_wr_r__v0 = vlSelfRef.__PVT__skid_addr_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlySet__q_wr_r__v0 = 1U;
            if (vlSelfRef.__PVT__push_drop_w) {
                __VdlyVal__q_rd_r__v1 = (7U & ((IData)(1U) 
                                               + ((IData)(vlSelfRef.__PVT__q_rd_r
                                                          [vlSelfRef.__PVT__skid_addr_r
                                                          [vlSelfRef.__PVT__skid_rp_r]]) 
                                                  + (IData)(vlSelfRef.__PVT__push_same_w))));
                __VdlyDim0__q_rd_r__v1 = vlSelfRef.__PVT__skid_addr_r
                    [vlSelfRef.__PVT__skid_rp_r];
                __VdlySet__q_rd_r__v1 = 1U;
                __VdlyVal__q_cnt_r__v1 = (0x0000000fU 
                                          & (IData)(vlSelfRef.__PVT__push_cnt1_w));
            } else {
                __VdlyVal__q_cnt_r__v1 = (0x0000000fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSelfRef.__PVT__push_cnt1_w)));
            }
            __VdlyDim0__q_cnt_r__v1 = vlSelfRef.__PVT__skid_addr_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlySet__q_cnt_r__v1 = 1U;
            vlSelfRef.__PVT__q_fed_r = (vlSelfRef.__PVT__q_fed_r 
                                        | (0x00000000ffffffffULL 
                                           & ((IData)(1U) 
                                              << vlSelfRef.__PVT__skid_addr_r
                                              [vlSelfRef.__PVT__skid_rp_r])));
        }
        __Vdly__skid_cnt_r = (7U & (((IData)(vlSelfRef.__PVT__skid_cnt_r) 
                                     + (IData)(vlSelfRef.__PVT__skid_enq_n_w)) 
                                    - ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                        ? 1U : 0U)));
        if ((2U == (((IData)(vlSelfRef.__PVT__tdm_frame_ev_w) 
                     << 1U) | (IData)(vlSymsp->TOP.a_tick_i)))) {
            if (((IData)(vlSelfRef.tdm_frame_pend_r) 
                 & (0xffffU != (IData)(vlSelfRef.tdm_skip_cnt_o)))) {
                vlSelfRef.tdm_skip_cnt_o = (0x0000ffffU 
                                            & ((IData)(1U) 
                                               + (IData)(vlSelfRef.tdm_skip_cnt_o)));
            }
            vlSelfRef.tdm_frame_pend_r = 1U;
            vlSelfRef.tdm_fed_r = 1U;
        } else {
            if ((1U == (((IData)(vlSelfRef.__PVT__tdm_frame_ev_w) 
                         << 1U) | (IData)(vlSymsp->TOP.a_tick_i)))) {
                if ((((IData)(vlSelfRef.tdm_fed_r) 
                      & (~ (IData)(vlSelfRef.tdm_frame_pend_r))) 
                     & (0xffffU != (IData)(vlSelfRef.tdm_dup_cnt_o)))) {
                    vlSelfRef.tdm_dup_cnt_o = (0x0000ffffU 
                                               & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tdm_dup_cnt_o)));
                }
                vlSelfRef.tdm_frame_pend_r = 0U;
            } else if ((3U == (((IData)(vlSelfRef.__PVT__tdm_frame_ev_w) 
                                << 1U) | (IData)(vlSymsp->TOP.a_tick_i)))) {
                vlSelfRef.tdm_frame_pend_r = 0U;
            }
            if ((1U != (((IData)(vlSelfRef.__PVT__tdm_frame_ev_w) 
                         << 1U) | (IData)(vlSymsp->TOP.a_tick_i)))) {
                if ((3U == (((IData)(vlSelfRef.__PVT__tdm_frame_ev_w) 
                             << 1U) | (IData)(vlSymsp->TOP.a_tick_i)))) {
                    vlSelfRef.tdm_fed_r = 1U;
                }
            }
        }
        if (vlSymsp->TOP.a_map_wr_en_i) {
            __VdlyVal__map_r__v0 = vlSymsp->TOP.a_map_wr_data_i;
            __VdlyDim0__map_r__v0 = vlSymsp->TOP.a_map_wr_addr_i;
            __VdlySet__map_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__enq0_v_w) {
            if (vlSelfRef.__PVT__cm0_v_w) {
                __VdlyVal__skid_addr_r__v0 = vlSelfRef.__PVT__lb_a0_w;
                __VdlyVal__skid_data_r__v0 = ((1U & (IData)(vlSelfRef.__PVT__lb_chpos_r))
                                               ? (((QData)((IData)(
                                                                   (vlSelfRef.__PVT__stash_val_r 
                                                                    & (- (IData)((IData)(vlSelfRef.__PVT__stash_vld_r)))))) 
                                                   << 0x00000018U) 
                                                  | (QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)))
                                               : ((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                                  << 0x00000018U));
            } else {
                __VdlyVal__skid_addr_r__v0 = vlSelfRef.__PVT__cm1_addr_w;
                __VdlyVal__skid_data_r__v0 = vlSelfRef.__PVT__cm1_data_w;
            }
            __VdlyDim0__skid_addr_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_addr_r__v0 = 1U;
            __VdlyVal__skid_strm_r__v0 = vlSelfRef.lb_tuser_i;
            __VdlyDim0__skid_strm_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_strm_r__v0 = 1U;
            __VdlyDim0__skid_data_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_data_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__enq1_v_w) {
            __VdlyVal__skid_addr_r__v1 = vlSelfRef.__PVT__cm1_addr_w;
            __VdlyDim0__skid_addr_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_addr_r__v1 = 1U;
            __VdlyVal__skid_strm_r__v1 = vlSelfRef.lb_tuser_i;
            __VdlyDim0__skid_strm_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_strm_r__v1 = 1U;
            __VdlyVal__skid_data_r__v1 = vlSelfRef.__PVT__cm1_data_w;
            __VdlyDim0__skid_data_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_data_r__v1 = 1U;
        }
        __Vdly__skid_rp_r = (3U & ((IData)(vlSelfRef.__PVT__skid_rp_r) 
                                   + ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                       ? 1U : 0U)));
        vlSelfRef.__PVT__skid_v_r = (0x0000000fU & 
                                     (((((IData)(vlSelfRef.__PVT__skid_v_r) 
                                         & (~ ((0U 
                                                != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                                ? ((IData)(1U) 
                                                   << (IData)(vlSelfRef.__PVT__skid_rp_r))
                                                : 0U))) 
                                        & (~ (IData)(vlSelfRef.__PVT__skid_kill_w))) 
                                       | ((IData)(vlSelfRef.__PVT__enq0_v_w)
                                           ? ((IData)(1U) 
                                              << (IData)(vlSelfRef.__PVT__skid_wp_r))
                                           : 0U)) | 
                                      ((IData)(vlSelfRef.__PVT__enq1_v_w)
                                        ? ((IData)(1U) 
                                           << (3U & 
                                               ((IData)(1U) 
                                                + (IData)(vlSelfRef.__PVT__skid_wp_r))))
                                        : 0U)));
        if ((1U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v1 = 1U;
            __VdlySet__q_rd_r__v2 = 1U;
            __VdlySet__lb_hold_r__v1 = 1U;
            __VdlySet__q_cnt_r__v2 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffeU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((2U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v2 = 1U;
            __VdlySet__q_rd_r__v3 = 1U;
            __VdlySet__lb_hold_r__v2 = 1U;
            __VdlySet__q_cnt_r__v3 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffdU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((4U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v3 = 1U;
            __VdlySet__q_rd_r__v4 = 1U;
            __VdlySet__lb_hold_r__v3 = 1U;
            __VdlySet__q_cnt_r__v4 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffbU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((8U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v4 = 1U;
            __VdlySet__q_rd_r__v5 = 1U;
            __VdlySet__lb_hold_r__v4 = 1U;
            __VdlySet__q_cnt_r__v5 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffff7U 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000010U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v5 = 1U;
            __VdlySet__q_rd_r__v6 = 1U;
            __VdlySet__lb_hold_r__v5 = 1U;
            __VdlySet__q_cnt_r__v6 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffefU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000020U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v6 = 1U;
            __VdlySet__q_rd_r__v7 = 1U;
            __VdlySet__lb_hold_r__v6 = 1U;
            __VdlySet__q_cnt_r__v7 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffdfU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000040U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v7 = 1U;
            __VdlySet__q_rd_r__v8 = 1U;
            __VdlySet__lb_hold_r__v7 = 1U;
            __VdlySet__q_cnt_r__v8 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffbfU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000080U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v8 = 1U;
            __VdlySet__q_rd_r__v9 = 1U;
            __VdlySet__lb_hold_r__v8 = 1U;
            __VdlySet__q_cnt_r__v9 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffff7fU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000100U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v9 = 1U;
            __VdlySet__q_rd_r__v10 = 1U;
            __VdlySet__lb_hold_r__v9 = 1U;
            __VdlySet__q_cnt_r__v10 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffeffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000200U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v10 = 1U;
            __VdlySet__q_rd_r__v11 = 1U;
            __VdlySet__lb_hold_r__v10 = 1U;
            __VdlySet__q_cnt_r__v11 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffdffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000400U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v11 = 1U;
            __VdlySet__q_rd_r__v12 = 1U;
            __VdlySet__lb_hold_r__v11 = 1U;
            __VdlySet__q_cnt_r__v12 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffbffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000800U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v12 = 1U;
            __VdlySet__q_rd_r__v13 = 1U;
            __VdlySet__lb_hold_r__v12 = 1U;
            __VdlySet__q_cnt_r__v13 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffff7ffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00001000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v13 = 1U;
            __VdlySet__q_rd_r__v14 = 1U;
            __VdlySet__lb_hold_r__v13 = 1U;
            __VdlySet__q_cnt_r__v14 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffefffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00002000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v14 = 1U;
            __VdlySet__q_rd_r__v15 = 1U;
            __VdlySet__lb_hold_r__v14 = 1U;
            __VdlySet__q_cnt_r__v15 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffdfffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00004000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v15 = 1U;
            __VdlySet__q_rd_r__v16 = 1U;
            __VdlySet__lb_hold_r__v15 = 1U;
            __VdlySet__q_cnt_r__v16 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffbfffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00008000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v16 = 1U;
            __VdlySet__q_rd_r__v17 = 1U;
            __VdlySet__lb_hold_r__v16 = 1U;
            __VdlySet__q_cnt_r__v17 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffff7fffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00010000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v17 = 1U;
            __VdlySet__q_rd_r__v18 = 1U;
            __VdlySet__lb_hold_r__v17 = 1U;
            __VdlySet__q_cnt_r__v18 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffeffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00020000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v18 = 1U;
            __VdlySet__q_rd_r__v19 = 1U;
            __VdlySet__lb_hold_r__v18 = 1U;
            __VdlySet__q_cnt_r__v19 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffdffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00040000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v19 = 1U;
            __VdlySet__q_rd_r__v20 = 1U;
            __VdlySet__lb_hold_r__v19 = 1U;
            __VdlySet__q_cnt_r__v20 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffbffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00080000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v20 = 1U;
            __VdlySet__q_rd_r__v21 = 1U;
            __VdlySet__lb_hold_r__v20 = 1U;
            __VdlySet__q_cnt_r__v21 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfff7ffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00100000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v21 = 1U;
            __VdlySet__q_rd_r__v22 = 1U;
            __VdlySet__lb_hold_r__v21 = 1U;
            __VdlySet__q_cnt_r__v22 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffefffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00200000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v22 = 1U;
            __VdlySet__q_rd_r__v23 = 1U;
            __VdlySet__lb_hold_r__v22 = 1U;
            __VdlySet__q_cnt_r__v23 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffdfffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00400000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v23 = 1U;
            __VdlySet__q_rd_r__v24 = 1U;
            __VdlySet__lb_hold_r__v23 = 1U;
            __VdlySet__q_cnt_r__v24 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffbfffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00800000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v24 = 1U;
            __VdlySet__q_rd_r__v25 = 1U;
            __VdlySet__lb_hold_r__v24 = 1U;
            __VdlySet__q_cnt_r__v25 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xff7fffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x01000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v25 = 1U;
            __VdlySet__q_rd_r__v26 = 1U;
            __VdlySet__lb_hold_r__v25 = 1U;
            __VdlySet__q_cnt_r__v26 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfeffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x02000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v26 = 1U;
            __VdlySet__q_rd_r__v27 = 1U;
            __VdlySet__lb_hold_r__v26 = 1U;
            __VdlySet__q_cnt_r__v27 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfdffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x04000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v27 = 1U;
            __VdlySet__q_rd_r__v28 = 1U;
            __VdlySet__lb_hold_r__v27 = 1U;
            __VdlySet__q_cnt_r__v28 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfbffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x08000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v28 = 1U;
            __VdlySet__q_rd_r__v29 = 1U;
            __VdlySet__lb_hold_r__v28 = 1U;
            __VdlySet__q_cnt_r__v29 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xf7ffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x10000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v29 = 1U;
            __VdlySet__q_rd_r__v30 = 1U;
            __VdlySet__lb_hold_r__v29 = 1U;
            __VdlySet__q_cnt_r__v30 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xefffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x20000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v30 = 1U;
            __VdlySet__q_rd_r__v31 = 1U;
            __VdlySet__lb_hold_r__v30 = 1U;
            __VdlySet__q_cnt_r__v31 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xdfffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x40000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v31 = 1U;
            __VdlySet__q_rd_r__v32 = 1U;
            __VdlySet__lb_hold_r__v31 = 1U;
            __VdlySet__q_cnt_r__v32 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xbfffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((vlSelfRef.__PVT__flush_clr_w >> 0x1fU)) {
            __VdlySet__q_wr_r__v32 = 1U;
            __VdlySet__q_rd_r__v33 = 1U;
            __VdlySet__lb_hold_r__v32 = 1U;
            __VdlySet__q_cnt_r__v33 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0x7fffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if (vlSelfRef.__PVT__pop_act_w) {
            __VdlyVal__q_rd_r__v0 = (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__q_rd_r
                                                     [
                                                     (0x0000001fU 
                                                      & (IData)(vlSelfRef.__PVT__pop_idx_r))])));
            __VdlyDim0__q_rd_r__v0 = (0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r));
            __VdlySet__q_rd_r__v0 = 1U;
            __VdlyVal__q_cnt_r__v0 = (0x0000000fU & 
                                      ((IData)(vlSelfRef.__PVT__q_cnt_r
                                               [(0x0000001fU 
                                                 & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                       - (IData)(1U)));
            __VdlyDim0__q_cnt_r__v0 = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__pop_idx_r));
            __VdlySet__q_cnt_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__pop_ret_v_r) {
            __VdlyVal__lb_hold_r__v0 = vlSelfRef.__PVT__q_rdata_r;
            __VdlyDim0__lb_hold_r__v0 = vlSelfRef.__PVT__pop_ret_pair_r;
            __VdlySet__lb_hold_r__v0 = 1U;
        }
        vlSelfRef.map_rd_valid_o = 0U;
        if (vlSymsp->TOP.a_map_rd_en_i) {
            vlSelfRef.map_rd_valid_o = 1U;
            vlSelfRef.map_rd_data_o = (((IData)(vlSelfRef.__PVT__loop_fed_r) 
                                        << 0x0000000eU) 
                                       | (((IData)(vlSelfRef.__PVT__loop_mapped_w) 
                                           << 0x0000000dU) 
                                          | vlSelfRef.__PVT__map_r
                                          [vlSymsp->TOP.a_map_rd_addr_i]));
        }
        vlSelfRef.lb_dup_cnt_o = ((0x00010000U & vlSelfRef.__PVT__dup_sum_w)
                                   ? 0x0000ffffU : 
                                  (0x0000ffffU & vlSelfRef.__PVT__dup_sum_w));
        vlSelfRef.lb_skip_cnt_o = ((0x00010000U & vlSelfRef.__PVT__skip_sum_w)
                                    ? 0x0000ffffU : 
                                   (0x0000ffffU & vlSelfRef.__PVT__skip_sum_w));
        if (vlSymsp->TOP.i2s_pair_valid_i) {
            vlSelfRef.__PVT__i2s_hold_r = (((QData)((IData)(vlSymsp->TOP.i2s_l_i)) 
                                            << 0x00000018U) 
                                           | (QData)((IData)(vlSymsp->TOP.i2s_r_i)));
        }
        if (vlSelfRef.lb_tvalid_i) {
            if (vlSelfRef.__PVT__stash_open_w) {
                vlSelfRef.__PVT__stash_strm_r = vlSelfRef.lb_tuser_i;
                vlSelfRef.__PVT__stash_val_r = vlSelfRef.__PVT__lb_smp1_w;
                vlSelfRef.__PVT__stash_vld_r = 1U;
            } else {
                vlSelfRef.__PVT__stash_vld_r = 0U;
            }
            vlSelfRef.__PVT__lb_chpos_r = (0x0000000fU 
                                           & (((IData)(1U) 
                                               + (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                                              & ((- (IData)(
                                                            (1U 
                                                             & (~ (IData)(vlSelfRef.lb_tlast_i))))) 
                                                 & (- (IData)(
                                                              ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                               != 
                                                               (0x0000000fU 
                                                                & ((IData)(1U) 
                                                                   + (IData)(vlSelfRef.__PVT__lb_ch1_w)))))))));
            vlSelfRef.__PVT__loop_fed_r = 1U;
        }
        if ((2U & (IData)(vlSelfRef.__PVT__st_r))) {
            if ((1U & (IData)(vlSelfRef.__PVT__st_r))) {
                vlSelfRef.pair_valid_o = 0U;
                if ((0U == (IData)(vlSelfRef.__PVT__gap_r))) {
                    if ((0x1fU == (IData)(vlSelfRef.__PVT__slot_r))) {
                        __Vdly__st_r = 0U;
                    } else {
                        __Vdly__slot_r = (0x0000001fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSelfRef.__PVT__slot_r)));
                        __Vdly__st_r = 2U;
                    }
                } else {
                    vlSelfRef.__PVT__gap_r = (0x0000001fU 
                                              & ((IData)(vlSelfRef.__PVT__gap_r) 
                                                 - (IData)(1U)));
                }
            } else {
                vlSelfRef.__PVT__gap_r = 0x18U;
                vlSelfRef.pair_valid_o = 1U;
                vlSelfRef.pair_slot_o = vlSelfRef.__PVT__slot_r;
                __Vdly__st_r = 3U;
                vlSelfRef.pair_l_o = (0x00ffffffU & 
                                      ((0x00000800U 
                                        & vlSelfRef.__PVT__map_r
                                        [((IData)(vlSelfRef.__PVT__slot_r) 
                                          << 1U)]) ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30)
                                        : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30 
                                                   >> 0x00000018U))));
                vlSelfRef.pair_r_o = (0x00ffffffU & 
                                      ((0x00000800U 
                                        & vlSelfRef.__PVT__map_r
                                        [(1U | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                << 1U))])
                                        ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32)
                                        : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32 
                                                   >> 0x00000018U))));
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__st_r))) {
            if ((0x20U == (IData)(vlSelfRef.__PVT__pop_idx_r))) {
                __Vdly__st_r = 2U;
            } else {
                __Vdly__pop_idx_r = (0x0000003fU & 
                                     ((IData)(1U) + (IData)(vlSelfRef.__PVT__pop_idx_r)));
            }
        } else {
            vlSelfRef.pair_valid_o = 0U;
            if (vlSelfRef.__PVT__tick_pend_r) {
                __Vdly__slot_r = 0U;
                vlSelfRef.__PVT__tick_pend_r = 0U;
                __Vdly__pop_idx_r = 0U;
                __Vdly__st_r = 1U;
            }
        }
        if (vlSymsp->TOP.a_tick_i) {
            vlSelfRef.__PVT__tick_pend_r = 1U;
        }
        vlSelfRef.__PVT__pop_ret_pair_r = (0x0000001fU 
                                           & (IData)(vlSelfRef.__PVT__pop_idx_r));
        vlSelfRef.__PVT__q_rdata_r = vlSelfRef.__PVT__lb_q_r
            [((0x000000f8U & ((IData)(vlSelfRef.__PVT__pop_idx_r) 
                              << 3U)) | vlSelfRef.__PVT__q_rd_r
              [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))])];
        if (vlSelfRef.__PVT__stash_flush_w) {
            vlSelfRef.__PVT__stash_vld_r = 0U;
        }
    } else {
        __Vdly__skid_wp_r = 0U;
        __VdlySet__tdm_hold_r__v1 = 1U;
        vlSelfRef.__PVT__q_primed_r = 0U;
        __Vdly__skid_cnt_r = 0U;
        vlSelfRef.tdm_dup_cnt_o = 0U;
        vlSelfRef.tdm_skip_cnt_o = 0U;
        __VdlySet__map_r__v1 = 1U;
        vlSelfRef.__PVT__skid_v_r = 0U;
        __Vdly__skid_rp_r = 0U;
        __VdlySet__q_wr_r__v33 = 1U;
        __VdlySet__q_rd_r__v34 = 1U;
        __VdlySet__lb_hold_r__v33 = 1U;
        __VdlySet__q_cnt_r__v34 = 1U;
        vlSelfRef.map_rd_valid_o = 0U;
        vlSelfRef.lb_dup_cnt_o = 0U;
        vlSelfRef.lb_skip_cnt_o = 0U;
        vlSelfRef.__PVT__i2s_hold_r = 0ULL;
        vlSelfRef.__PVT__q_fed_r = 0U;
        vlSelfRef.map_rd_data_o = 0U;
        vlSelfRef.__PVT__stash_strm_r = 0U;
        vlSelfRef.__PVT__tick_pend_r = 0U;
        __Vdly__slot_r = 0U;
        vlSelfRef.__PVT__gap_r = 0U;
        __Vdly__st_r = 0U;
        __Vdly__pop_idx_r = 0U;
        vlSelfRef.pair_valid_o = 0U;
        vlSelfRef.pair_slot_o = 0U;
        vlSelfRef.pair_l_o = 0U;
        vlSelfRef.pair_r_o = 0U;
        vlSelfRef.tdm_frame_pend_r = 0U;
        vlSelfRef.tdm_fed_r = 0U;
        vlSelfRef.__PVT__pop_ret_pair_r = 0U;
        vlSelfRef.__PVT__q_rdata_r = 0ULL;
        vlSelfRef.__PVT__stash_vld_r = 0U;
        vlSelfRef.__PVT__stash_val_r = 0U;
        vlSelfRef.__PVT__lb_chpos_r = 0U;
        vlSelfRef.__PVT__loop_fed_r = 0U;
    }
    if (__VdlySet__tdm_hold_r__v0) {
        vlSelfRef.tdm_hold_r[__VdlyDim0__tdm_hold_r__v0] 
            = __VdlyVal__tdm_hold_r__v0;
    }
    if (__VdlySet__tdm_hold_r__v1) {
        vlSelfRef.tdm_hold_r[0U] = 0ULL;
        vlSelfRef.tdm_hold_r[1U] = 0ULL;
        vlSelfRef.tdm_hold_r[2U] = 0ULL;
        vlSelfRef.tdm_hold_r[3U] = 0ULL;
    }
    vlSelfRef.__PVT__skid_cnt_r = __Vdly__skid_cnt_r;
    if (__VdlySet__skid_strm_r__v0) {
        vlSelfRef.__PVT__skid_strm_r[__VdlyDim0__skid_strm_r__v0] 
            = __VdlyVal__skid_strm_r__v0;
    }
    if (__VdlySet__skid_strm_r__v1) {
        vlSelfRef.__PVT__skid_strm_r[__VdlyDim0__skid_strm_r__v1] 
            = __VdlyVal__skid_strm_r__v1;
    }
    if (__VdlySet__q_wr_r__v0) {
        vlSelfRef.__PVT__q_wr_r[__VdlyDim0__q_wr_r__v0] 
            = __VdlyVal__q_wr_r__v0;
    }
    if (__VdlySet__q_wr_r__v1) {
        vlSelfRef.__PVT__q_wr_r[0U] = 0U;
    }
    if (__VdlySet__q_wr_r__v2) {
        vlSelfRef.__PVT__q_wr_r[1U] = 0U;
    }
    if (__VdlySet__q_wr_r__v3) {
        vlSelfRef.__PVT__q_wr_r[2U] = 0U;
    }
    if (__VdlySet__q_wr_r__v4) {
        vlSelfRef.__PVT__q_wr_r[3U] = 0U;
    }
    if (__VdlySet__q_wr_r__v5) {
        vlSelfRef.__PVT__q_wr_r[4U] = 0U;
    }
    if (__VdlySet__q_wr_r__v6) {
        vlSelfRef.__PVT__q_wr_r[5U] = 0U;
    }
    if (__VdlySet__q_wr_r__v7) {
        vlSelfRef.__PVT__q_wr_r[6U] = 0U;
    }
    if (__VdlySet__q_wr_r__v8) {
        vlSelfRef.__PVT__q_wr_r[7U] = 0U;
    }
    if (__VdlySet__q_wr_r__v9) {
        vlSelfRef.__PVT__q_wr_r[8U] = 0U;
    }
    if (__VdlySet__q_wr_r__v10) {
        vlSelfRef.__PVT__q_wr_r[9U] = 0U;
    }
    if (__VdlySet__q_wr_r__v11) {
        vlSelfRef.__PVT__q_wr_r[10U] = 0U;
    }
    if (__VdlySet__q_wr_r__v12) {
        vlSelfRef.__PVT__q_wr_r[11U] = 0U;
    }
    if (__VdlySet__q_wr_r__v13) {
        vlSelfRef.__PVT__q_wr_r[12U] = 0U;
    }
    if (__VdlySet__q_wr_r__v14) {
        vlSelfRef.__PVT__q_wr_r[13U] = 0U;
    }
    if (__VdlySet__q_wr_r__v15) {
        vlSelfRef.__PVT__q_wr_r[14U] = 0U;
    }
    if (__VdlySet__q_wr_r__v16) {
        vlSelfRef.__PVT__q_wr_r[15U] = 0U;
    }
    if (__VdlySet__q_wr_r__v17) {
        vlSelfRef.__PVT__q_wr_r[16U] = 0U;
    }
    if (__VdlySet__q_wr_r__v18) {
        vlSelfRef.__PVT__q_wr_r[17U] = 0U;
    }
    if (__VdlySet__q_wr_r__v19) {
        vlSelfRef.__PVT__q_wr_r[18U] = 0U;
    }
    if (__VdlySet__q_wr_r__v20) {
        vlSelfRef.__PVT__q_wr_r[19U] = 0U;
    }
    if (__VdlySet__q_wr_r__v21) {
        vlSelfRef.__PVT__q_wr_r[20U] = 0U;
    }
    if (__VdlySet__q_wr_r__v22) {
        vlSelfRef.__PVT__q_wr_r[21U] = 0U;
    }
    if (__VdlySet__q_wr_r__v23) {
        vlSelfRef.__PVT__q_wr_r[22U] = 0U;
    }
    if (__VdlySet__q_wr_r__v24) {
        vlSelfRef.__PVT__q_wr_r[23U] = 0U;
    }
    if (__VdlySet__q_wr_r__v25) {
        vlSelfRef.__PVT__q_wr_r[24U] = 0U;
    }
    if (__VdlySet__q_wr_r__v26) {
        vlSelfRef.__PVT__q_wr_r[25U] = 0U;
    }
    if (__VdlySet__q_wr_r__v27) {
        vlSelfRef.__PVT__q_wr_r[26U] = 0U;
    }
    if (__VdlySet__q_wr_r__v28) {
        vlSelfRef.__PVT__q_wr_r[27U] = 0U;
    }
    if (__VdlySet__q_wr_r__v29) {
        vlSelfRef.__PVT__q_wr_r[28U] = 0U;
    }
    if (__VdlySet__q_wr_r__v30) {
        vlSelfRef.__PVT__q_wr_r[29U] = 0U;
    }
    if (__VdlySet__q_wr_r__v31) {
        vlSelfRef.__PVT__q_wr_r[30U] = 0U;
    }
    if (__VdlySet__q_wr_r__v32) {
        vlSelfRef.__PVT__q_wr_r[31U] = 0U;
    }
    if (__VdlySet__q_wr_r__v33) {
        vlSelfRef.__PVT__q_wr_r[0U] = 0U;
        vlSelfRef.__PVT__q_wr_r[1U] = 0U;
        vlSelfRef.__PVT__q_wr_r[2U] = 0U;
        vlSelfRef.__PVT__q_wr_r[3U] = 0U;
        vlSelfRef.__PVT__q_wr_r[4U] = 0U;
        vlSelfRef.__PVT__q_wr_r[5U] = 0U;
        vlSelfRef.__PVT__q_wr_r[6U] = 0U;
        vlSelfRef.__PVT__q_wr_r[7U] = 0U;
        vlSelfRef.__PVT__q_wr_r[8U] = 0U;
        vlSelfRef.__PVT__q_wr_r[9U] = 0U;
        vlSelfRef.__PVT__q_wr_r[10U] = 0U;
        vlSelfRef.__PVT__q_wr_r[11U] = 0U;
        vlSelfRef.__PVT__q_wr_r[12U] = 0U;
        vlSelfRef.__PVT__q_wr_r[13U] = 0U;
        vlSelfRef.__PVT__q_wr_r[14U] = 0U;
        vlSelfRef.__PVT__q_wr_r[15U] = 0U;
        vlSelfRef.__PVT__q_wr_r[16U] = 0U;
        vlSelfRef.__PVT__q_wr_r[17U] = 0U;
        vlSelfRef.__PVT__q_wr_r[18U] = 0U;
        vlSelfRef.__PVT__q_wr_r[19U] = 0U;
        vlSelfRef.__PVT__q_wr_r[20U] = 0U;
        vlSelfRef.__PVT__q_wr_r[21U] = 0U;
        vlSelfRef.__PVT__q_wr_r[22U] = 0U;
        vlSelfRef.__PVT__q_wr_r[23U] = 0U;
        vlSelfRef.__PVT__q_wr_r[24U] = 0U;
        vlSelfRef.__PVT__q_wr_r[25U] = 0U;
        vlSelfRef.__PVT__q_wr_r[26U] = 0U;
        vlSelfRef.__PVT__q_wr_r[27U] = 0U;
        vlSelfRef.__PVT__q_wr_r[28U] = 0U;
        vlSelfRef.__PVT__q_wr_r[29U] = 0U;
        vlSelfRef.__PVT__q_wr_r[30U] = 0U;
        vlSelfRef.__PVT__q_wr_r[31U] = 0U;
    }
    if (__VdlySet__lb_hold_r__v0) {
        vlSelfRef.__PVT__lb_hold_r[__VdlyDim0__lb_hold_r__v0] 
            = __VdlyVal__lb_hold_r__v0;
    }
    if (__VdlySet__lb_hold_r__v1) {
        vlSelfRef.__PVT__lb_hold_r[0U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v2) {
        vlSelfRef.__PVT__lb_hold_r[1U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v3) {
        vlSelfRef.__PVT__lb_hold_r[2U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v4) {
        vlSelfRef.__PVT__lb_hold_r[3U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v5) {
        vlSelfRef.__PVT__lb_hold_r[4U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v6) {
        vlSelfRef.__PVT__lb_hold_r[5U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v7) {
        vlSelfRef.__PVT__lb_hold_r[6U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v8) {
        vlSelfRef.__PVT__lb_hold_r[7U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v9) {
        vlSelfRef.__PVT__lb_hold_r[8U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v10) {
        vlSelfRef.__PVT__lb_hold_r[9U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v11) {
        vlSelfRef.__PVT__lb_hold_r[10U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v12) {
        vlSelfRef.__PVT__lb_hold_r[11U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v13) {
        vlSelfRef.__PVT__lb_hold_r[12U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v14) {
        vlSelfRef.__PVT__lb_hold_r[13U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v15) {
        vlSelfRef.__PVT__lb_hold_r[14U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v16) {
        vlSelfRef.__PVT__lb_hold_r[15U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v17) {
        vlSelfRef.__PVT__lb_hold_r[16U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v18) {
        vlSelfRef.__PVT__lb_hold_r[17U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v19) {
        vlSelfRef.__PVT__lb_hold_r[18U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v20) {
        vlSelfRef.__PVT__lb_hold_r[19U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v21) {
        vlSelfRef.__PVT__lb_hold_r[20U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v22) {
        vlSelfRef.__PVT__lb_hold_r[21U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v23) {
        vlSelfRef.__PVT__lb_hold_r[22U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v24) {
        vlSelfRef.__PVT__lb_hold_r[23U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v25) {
        vlSelfRef.__PVT__lb_hold_r[24U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v26) {
        vlSelfRef.__PVT__lb_hold_r[25U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v27) {
        vlSelfRef.__PVT__lb_hold_r[26U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v28) {
        vlSelfRef.__PVT__lb_hold_r[27U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v29) {
        vlSelfRef.__PVT__lb_hold_r[28U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v30) {
        vlSelfRef.__PVT__lb_hold_r[29U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v31) {
        vlSelfRef.__PVT__lb_hold_r[30U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v32) {
        vlSelfRef.__PVT__lb_hold_r[31U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v33) {
        vlSelfRef.__PVT__lb_hold_r[0U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[1U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[2U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[3U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[4U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[5U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[6U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[7U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[8U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[9U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[10U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[11U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[12U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[13U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[14U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[15U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[16U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[17U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[18U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[19U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[20U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[21U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[22U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[23U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[24U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[25U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[26U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[27U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[28U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[29U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[30U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[31U] = 0ULL;
    }
    if (__VdlySet__q_cnt_r__v0) {
        vlSelfRef.__PVT__q_cnt_r[__VdlyDim0__q_cnt_r__v0] 
            = __VdlyVal__q_cnt_r__v0;
    }
    if (__VdlySet__q_cnt_r__v1) {
        vlSelfRef.__PVT__q_cnt_r[__VdlyDim0__q_cnt_r__v1] 
            = __VdlyVal__q_cnt_r__v1;
    }
    if (__VdlySet__q_cnt_r__v2) {
        vlSelfRef.__PVT__q_cnt_r[0U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v3) {
        vlSelfRef.__PVT__q_cnt_r[1U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v4) {
        vlSelfRef.__PVT__q_cnt_r[2U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v5) {
        vlSelfRef.__PVT__q_cnt_r[3U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v6) {
        vlSelfRef.__PVT__q_cnt_r[4U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v7) {
        vlSelfRef.__PVT__q_cnt_r[5U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v8) {
        vlSelfRef.__PVT__q_cnt_r[6U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v9) {
        vlSelfRef.__PVT__q_cnt_r[7U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v10) {
        vlSelfRef.__PVT__q_cnt_r[8U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v11) {
        vlSelfRef.__PVT__q_cnt_r[9U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v12) {
        vlSelfRef.__PVT__q_cnt_r[10U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v13) {
        vlSelfRef.__PVT__q_cnt_r[11U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v14) {
        vlSelfRef.__PVT__q_cnt_r[12U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v15) {
        vlSelfRef.__PVT__q_cnt_r[13U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v16) {
        vlSelfRef.__PVT__q_cnt_r[14U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v17) {
        vlSelfRef.__PVT__q_cnt_r[15U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v18) {
        vlSelfRef.__PVT__q_cnt_r[16U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v19) {
        vlSelfRef.__PVT__q_cnt_r[17U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v20) {
        vlSelfRef.__PVT__q_cnt_r[18U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v21) {
        vlSelfRef.__PVT__q_cnt_r[19U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v22) {
        vlSelfRef.__PVT__q_cnt_r[20U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v23) {
        vlSelfRef.__PVT__q_cnt_r[21U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v24) {
        vlSelfRef.__PVT__q_cnt_r[22U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v25) {
        vlSelfRef.__PVT__q_cnt_r[23U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v26) {
        vlSelfRef.__PVT__q_cnt_r[24U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v27) {
        vlSelfRef.__PVT__q_cnt_r[25U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v28) {
        vlSelfRef.__PVT__q_cnt_r[26U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v29) {
        vlSelfRef.__PVT__q_cnt_r[27U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v30) {
        vlSelfRef.__PVT__q_cnt_r[28U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v31) {
        vlSelfRef.__PVT__q_cnt_r[29U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v32) {
        vlSelfRef.__PVT__q_cnt_r[30U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v33) {
        vlSelfRef.__PVT__q_cnt_r[31U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v34) {
        vlSelfRef.__PVT__q_cnt_r[0U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[1U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[2U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[3U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[4U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[5U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[6U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[7U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[8U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[9U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[10U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[11U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[12U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[13U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[14U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[15U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[16U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[17U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[18U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[19U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[20U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[21U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[22U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[23U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[24U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[25U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[26U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[27U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[28U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[29U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[30U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[31U] = 0U;
    }
    vlSelfRef.__PVT__skid_wp_r = __Vdly__skid_wp_r;
    if (__VdlySet__skid_data_r__v0) {
        vlSelfRef.__PVT__skid_data_r[__VdlyDim0__skid_data_r__v0] 
            = __VdlyVal__skid_data_r__v0;
    }
    if (__VdlySet__skid_data_r__v1) {
        vlSelfRef.__PVT__skid_data_r[__VdlyDim0__skid_data_r__v1] 
            = __VdlyVal__skid_data_r__v1;
    }
    if (__VdlySet__skid_addr_r__v0) {
        vlSelfRef.__PVT__skid_addr_r[__VdlyDim0__skid_addr_r__v0] 
            = __VdlyVal__skid_addr_r__v0;
    }
    if (__VdlySet__skid_addr_r__v1) {
        vlSelfRef.__PVT__skid_addr_r[__VdlyDim0__skid_addr_r__v1] 
            = __VdlyVal__skid_addr_r__v1;
    }
    vlSelfRef.__PVT__skid_rp_r = __Vdly__skid_rp_r;
    vlSelfRef.__PVT__st_r = __Vdly__st_r;
    vlSelfRef.__PVT__slot_r = __Vdly__slot_r;
    if (__VdlySet__map_r__v0) {
        vlSelfRef.__PVT__map_r[__VdlyDim0__map_r__v0] 
            = __VdlyVal__map_r__v0;
    }
    if (__VdlySet__map_r__v1) {
        __Vilp1 = 0U;
        while ((__Vilp1 <= 0x0000003fU)) {
            vlSelfRef.__PVT__map_r[__Vilp1] = 0U;
            __Vilp1 = ((IData)(1U) + __Vilp1);
        }
    }
    vlSelfRef.__PVT__skid_free_w = (7U & (((IData)(4U) 
                                           - (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                          + (1U & (- (IData)(
                                                             (0U 
                                                              != (IData)(vlSelfRef.__PVT__skid_cnt_r)))))));
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    vlSelfRef.__PVT__pop_ret_v_r = ((IData)(vlSymsp->TOP.rst_n) 
                                    && ((IData)(vlSelfRef.__PVT__pop_act_w) 
                                        & (~ (vlSelfRef.__PVT__flush_clr_w 
                                              >> (0x0000001fU 
                                                  & (IData)(vlSelfRef.__PVT__pop_idx_r))))));
    vlSelfRef.__PVT__push_ram_w = ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                   & ((IData)(vlSelfRef.__PVT__skid_v_r) 
                                      >> (IData)(vlSelfRef.__PVT__skid_rp_r)));
    vlSelfRef.__PVT__loop_mapped_w = 0U;
    if (((vlSelfRef.__PVT__map_r[0U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[0U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[1U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[1U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[2U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[2U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[3U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[3U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[4U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[4U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[5U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[5U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[6U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[6U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[7U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[7U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[8U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[8U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[9U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[9U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[10U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[10U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[11U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[11U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[12U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[12U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[13U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[13U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[14U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[14U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[15U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[15U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[16U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[16U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[17U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[17U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[18U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[18U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[19U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[19U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[20U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[20U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[21U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[21U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[22U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[22U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[23U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[23U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[24U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[24U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[25U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[25U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[26U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[26U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[27U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[27U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[28U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[28U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[29U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[29U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[30U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[30U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[31U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[31U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[32U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[32U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[33U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[33U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[34U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[34U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[35U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[35U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[36U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[36U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[37U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[37U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[38U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[38U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[39U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[39U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[40U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[40U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[41U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[41U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[42U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[42U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[43U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[43U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[44U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[44U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[45U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[45U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[46U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[46U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[47U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[47U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[48U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[48U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[49U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[49U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[50U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[50U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[51U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[51U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[52U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[52U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[53U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[53U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[54U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[54U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[55U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[55U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[56U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[56U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[57U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[57U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[58U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[58U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[59U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[59U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[60U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[60U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[61U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[61U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[62U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[62U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[63U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[63U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    (1U 
                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U))] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    (1U 
                                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                        << 1U))] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10 = (7U 
                                                 & ((vlSelfRef.__PVT__map_r
                                                     [
                                                     ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U)] 
                                                     >> 8U) 
                                                    & (- (IData)(
                                                                 (1U 
                                                                  & (vlSelfRef.__PVT__map_r
                                                                     [
                                                                     ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                      << 1U)] 
                                                                     >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [((IData)(vlSelfRef.__PVT__slot_r) 
                                                   << 1U)]);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [(1U 
                                                   | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U))]);
    if (__VdlySet__lb_q_r__v0) {
        vlSelfRef.__PVT__lb_q_r[__VdlyDim0__lb_q_r__v0] 
            = __VdlyVal__lb_q_r__v0;
    }
    if (__VdlySet__q_rd_r__v0) {
        vlSelfRef.__PVT__q_rd_r[__VdlyDim0__q_rd_r__v0] 
            = __VdlyVal__q_rd_r__v0;
    }
    if (__VdlySet__q_rd_r__v1) {
        vlSelfRef.__PVT__q_rd_r[__VdlyDim0__q_rd_r__v1] 
            = __VdlyVal__q_rd_r__v1;
    }
    if (__VdlySet__q_rd_r__v2) {
        vlSelfRef.__PVT__q_rd_r[0U] = 0U;
    }
    if (__VdlySet__q_rd_r__v3) {
        vlSelfRef.__PVT__q_rd_r[1U] = 0U;
    }
    if (__VdlySet__q_rd_r__v4) {
        vlSelfRef.__PVT__q_rd_r[2U] = 0U;
    }
    if (__VdlySet__q_rd_r__v5) {
        vlSelfRef.__PVT__q_rd_r[3U] = 0U;
    }
    if (__VdlySet__q_rd_r__v6) {
        vlSelfRef.__PVT__q_rd_r[4U] = 0U;
    }
    if (__VdlySet__q_rd_r__v7) {
        vlSelfRef.__PVT__q_rd_r[5U] = 0U;
    }
    if (__VdlySet__q_rd_r__v8) {
        vlSelfRef.__PVT__q_rd_r[6U] = 0U;
    }
    if (__VdlySet__q_rd_r__v9) {
        vlSelfRef.__PVT__q_rd_r[7U] = 0U;
    }
    if (__VdlySet__q_rd_r__v10) {
        vlSelfRef.__PVT__q_rd_r[8U] = 0U;
    }
    if (__VdlySet__q_rd_r__v11) {
        vlSelfRef.__PVT__q_rd_r[9U] = 0U;
    }
    if (__VdlySet__q_rd_r__v12) {
        vlSelfRef.__PVT__q_rd_r[10U] = 0U;
    }
    if (__VdlySet__q_rd_r__v13) {
        vlSelfRef.__PVT__q_rd_r[11U] = 0U;
    }
    if (__VdlySet__q_rd_r__v14) {
        vlSelfRef.__PVT__q_rd_r[12U] = 0U;
    }
    if (__VdlySet__q_rd_r__v15) {
        vlSelfRef.__PVT__q_rd_r[13U] = 0U;
    }
    if (__VdlySet__q_rd_r__v16) {
        vlSelfRef.__PVT__q_rd_r[14U] = 0U;
    }
    if (__VdlySet__q_rd_r__v17) {
        vlSelfRef.__PVT__q_rd_r[15U] = 0U;
    }
    if (__VdlySet__q_rd_r__v18) {
        vlSelfRef.__PVT__q_rd_r[16U] = 0U;
    }
    if (__VdlySet__q_rd_r__v19) {
        vlSelfRef.__PVT__q_rd_r[17U] = 0U;
    }
    if (__VdlySet__q_rd_r__v20) {
        vlSelfRef.__PVT__q_rd_r[18U] = 0U;
    }
    if (__VdlySet__q_rd_r__v21) {
        vlSelfRef.__PVT__q_rd_r[19U] = 0U;
    }
    if (__VdlySet__q_rd_r__v22) {
        vlSelfRef.__PVT__q_rd_r[20U] = 0U;
    }
    if (__VdlySet__q_rd_r__v23) {
        vlSelfRef.__PVT__q_rd_r[21U] = 0U;
    }
    if (__VdlySet__q_rd_r__v24) {
        vlSelfRef.__PVT__q_rd_r[22U] = 0U;
    }
    if (__VdlySet__q_rd_r__v25) {
        vlSelfRef.__PVT__q_rd_r[23U] = 0U;
    }
    if (__VdlySet__q_rd_r__v26) {
        vlSelfRef.__PVT__q_rd_r[24U] = 0U;
    }
    if (__VdlySet__q_rd_r__v27) {
        vlSelfRef.__PVT__q_rd_r[25U] = 0U;
    }
    if (__VdlySet__q_rd_r__v28) {
        vlSelfRef.__PVT__q_rd_r[26U] = 0U;
    }
    if (__VdlySet__q_rd_r__v29) {
        vlSelfRef.__PVT__q_rd_r[27U] = 0U;
    }
    if (__VdlySet__q_rd_r__v30) {
        vlSelfRef.__PVT__q_rd_r[28U] = 0U;
    }
    if (__VdlySet__q_rd_r__v31) {
        vlSelfRef.__PVT__q_rd_r[29U] = 0U;
    }
    if (__VdlySet__q_rd_r__v32) {
        vlSelfRef.__PVT__q_rd_r[30U] = 0U;
    }
    if (__VdlySet__q_rd_r__v33) {
        vlSelfRef.__PVT__q_rd_r[31U] = 0U;
    }
    if (__VdlySet__q_rd_r__v34) {
        vlSelfRef.__PVT__q_rd_r[0U] = 0U;
        vlSelfRef.__PVT__q_rd_r[1U] = 0U;
        vlSelfRef.__PVT__q_rd_r[2U] = 0U;
        vlSelfRef.__PVT__q_rd_r[3U] = 0U;
        vlSelfRef.__PVT__q_rd_r[4U] = 0U;
        vlSelfRef.__PVT__q_rd_r[5U] = 0U;
        vlSelfRef.__PVT__q_rd_r[6U] = 0U;
        vlSelfRef.__PVT__q_rd_r[7U] = 0U;
        vlSelfRef.__PVT__q_rd_r[8U] = 0U;
        vlSelfRef.__PVT__q_rd_r[9U] = 0U;
        vlSelfRef.__PVT__q_rd_r[10U] = 0U;
        vlSelfRef.__PVT__q_rd_r[11U] = 0U;
        vlSelfRef.__PVT__q_rd_r[12U] = 0U;
        vlSelfRef.__PVT__q_rd_r[13U] = 0U;
        vlSelfRef.__PVT__q_rd_r[14U] = 0U;
        vlSelfRef.__PVT__q_rd_r[15U] = 0U;
        vlSelfRef.__PVT__q_rd_r[16U] = 0U;
        vlSelfRef.__PVT__q_rd_r[17U] = 0U;
        vlSelfRef.__PVT__q_rd_r[18U] = 0U;
        vlSelfRef.__PVT__q_rd_r[19U] = 0U;
        vlSelfRef.__PVT__q_rd_r[20U] = 0U;
        vlSelfRef.__PVT__q_rd_r[21U] = 0U;
        vlSelfRef.__PVT__q_rd_r[22U] = 0U;
        vlSelfRef.__PVT__q_rd_r[23U] = 0U;
        vlSelfRef.__PVT__q_rd_r[24U] = 0U;
        vlSelfRef.__PVT__q_rd_r[25U] = 0U;
        vlSelfRef.__PVT__q_rd_r[26U] = 0U;
        vlSelfRef.__PVT__q_rd_r[27U] = 0U;
        vlSelfRef.__PVT__q_rd_r[28U] = 0U;
        vlSelfRef.__PVT__q_rd_r[29U] = 0U;
        vlSelfRef.__PVT__q_rd_r[30U] = 0U;
        vlSelfRef.__PVT__q_rd_r[31U] = 0U;
    }
    vlSelfRef.__PVT__pop_idx_r = __Vdly__pop_idx_r;
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)))))))));
    __VdfgRegularize_h6e95ff9d_0_56 = ((vlSelfRef.__PVT__q_primed_r 
                                        >> (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & ((1U == (IData)(vlSelfRef.__PVT__st_r)) 
                                          & (0x20U 
                                             > (IData)(vlSelfRef.__PVT__pop_idx_r))));
    vlSelfRef.__PVT__lb_a0_w = (0x0000001fU & (((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                >> 1U) 
                                               + (0x0000001cU 
                                                  & ((IData)(vlSelfRef.lb_tuser_i) 
                                                     << 2U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
    vlSelfRef.__PVT__lb_w0_w = ((8U > (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__dup_sum_w = (0x0001ffffU & (((IData)(__VdfgRegularize_h6e95ff9d_0_56) 
                                                  & ((vlSelfRef.__PVT__q_fed_r 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                                     & (0U 
                                                        == vlSelfRef.__PVT__q_cnt_r
                                                        [
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__PVT__pop_idx_r))]))) 
                                                 + (IData)(vlSelfRef.lb_dup_cnt_o)));
    vlSelfRef.__PVT__pop_act_w = ((0U != vlSelfRef.__PVT__q_cnt_r
                                   [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_56));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    vlSelfRef.__PVT__push_same_w = ((IData)(vlSelfRef.__PVT__push_ram_w) 
                                    & ((vlSelfRef.__PVT__skid_addr_r
                                        [vlSelfRef.__PVT__skid_rp_r] 
                                        == (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & (IData)(vlSelfRef.__PVT__pop_act_w)));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__push_cnt1_w = (0x0000000fU & ((IData)(vlSelfRef.__PVT__q_cnt_r
                                                           [vlSelfRef.__PVT__skid_addr_r
                                                           [vlSelfRef.__PVT__skid_rp_r]]) 
                                                   - (IData)(vlSelfRef.__PVT__push_same_w)));
    if (vlSelfRef.__PVT__lb_pair01_w) {
        vlSelfRef.__PVT__cm1_data_w = (((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)));
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__lb_a0_w));
    } else {
        vlSelfRef.__PVT__cm1_data_w = ((QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)) 
                                       << 0x00000018U);
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                           >> 1U) + 
                                          (0x0000001cU 
                                           & ((IData)(vlSelfRef.lb_tuser_i) 
                                              << 2U))));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58));
    vlSelfRef.__PVT__push_drop_w = ((8U == (IData)(vlSelfRef.__PVT__push_cnt1_w)) 
                                    & (IData)(vlSelfRef.__PVT__push_ram_w));
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60));
    __VdfgRegularize_h6e95ff9d_0_57 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_57));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_57)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__1(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__1\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)))))))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__4(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__4\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.lb_flush_i = vlSymsp->TOP.b_lb_flush_i;
    vlSelfRef.__PVT__flush_clr_w = 0U;
    if ((1U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (1U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (2U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (4U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (8U | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((2U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000010U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000020U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000040U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000080U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((4U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000100U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000200U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000400U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000800U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((8U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00001000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00002000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00004000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00008000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000010U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00010000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00020000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00040000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00080000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000020U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00100000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00200000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00400000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00800000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000040U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x01000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x02000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x04000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x08000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000080U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x10000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x20000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x40000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x80000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__1(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__1\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __PVT__lb_chans_raw_w;
    __PVT__lb_chans_raw_w = 0;
    // Body
    __PVT__lb_chans_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & vlSelfRef.lb_wire_chans_i);
    }
    if ((1U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x18U));
    }
    if ((7U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (vlSelfRef.lb_wire_chans_i 
                                 >> 0x1cU);
    }
    vlSelfRef.__PVT__lb_chans_w = ((0U == (IData)(__PVT__lb_chans_raw_w))
                                    ? 2U : (IData)(__PVT__lb_chans_raw_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__4(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__4\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    // Body
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU & ((IData)(vlSelfRef.__PVT__lb_pair01_w)
                                                   ? (IData)(vlSelfRef.__PVT__lb_a0_w)
                                                   : 
                                                  (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                    >> 1U) 
                                                   + 
                                                   (0x0000001cU 
                                                    & ((IData)(vlSelfRef.lb_tuser_i) 
                                                       << 2U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__5(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__5\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__7(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__7\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__8(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__8\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53));
}

void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__9(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__9\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_50;
    __VdfgRegularize_h6e95ff9d_0_50 = 0;
    // Body
    __VdfgRegularize_h6e95ff9d_0_50 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_50));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_50)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}

void Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_49;
    __VdfgRegularize_h6e95ff9d_0_49 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_50;
    __VdfgRegularize_h6e95ff9d_0_50 = 0;
    CData/*1:0*/ __Vdly__skid_wp_r;
    __Vdly__skid_wp_r = 0;
    CData/*1:0*/ __Vdly__skid_rp_r;
    __Vdly__skid_rp_r = 0;
    CData/*2:0*/ __Vdly__skid_cnt_r;
    __Vdly__skid_cnt_r = 0;
    CData/*1:0*/ __Vdly__st_r;
    __Vdly__st_r = 0;
    CData/*4:0*/ __Vdly__slot_r;
    __Vdly__slot_r = 0;
    CData/*5:0*/ __Vdly__pop_idx_r;
    __Vdly__pop_idx_r = 0;
    SData/*12:0*/ __VdlyVal__map_r__v0;
    __VdlyVal__map_r__v0 = 0;
    CData/*5:0*/ __VdlyDim0__map_r__v0;
    __VdlyDim0__map_r__v0 = 0;
    CData/*0:0*/ __VdlySet__map_r__v0;
    __VdlySet__map_r__v0 = 0;
    CData/*0:0*/ __VdlySet__map_r__v1;
    __VdlySet__map_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__tdm_hold_r__v0;
    __VdlyVal__tdm_hold_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__tdm_hold_r__v0;
    __VdlyDim0__tdm_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__tdm_hold_r__v0;
    __VdlySet__tdm_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__tdm_hold_r__v1;
    __VdlySet__tdm_hold_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__lb_hold_r__v0;
    __VdlyVal__lb_hold_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__lb_hold_r__v0;
    __VdlyDim0__lb_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v0;
    __VdlySet__lb_hold_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v1;
    __VdlySet__lb_hold_r__v1 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v2;
    __VdlySet__lb_hold_r__v2 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v3;
    __VdlySet__lb_hold_r__v3 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v4;
    __VdlySet__lb_hold_r__v4 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v5;
    __VdlySet__lb_hold_r__v5 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v6;
    __VdlySet__lb_hold_r__v6 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v7;
    __VdlySet__lb_hold_r__v7 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v8;
    __VdlySet__lb_hold_r__v8 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v9;
    __VdlySet__lb_hold_r__v9 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v10;
    __VdlySet__lb_hold_r__v10 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v11;
    __VdlySet__lb_hold_r__v11 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v12;
    __VdlySet__lb_hold_r__v12 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v13;
    __VdlySet__lb_hold_r__v13 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v14;
    __VdlySet__lb_hold_r__v14 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v15;
    __VdlySet__lb_hold_r__v15 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v16;
    __VdlySet__lb_hold_r__v16 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v17;
    __VdlySet__lb_hold_r__v17 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v18;
    __VdlySet__lb_hold_r__v18 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v19;
    __VdlySet__lb_hold_r__v19 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v20;
    __VdlySet__lb_hold_r__v20 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v21;
    __VdlySet__lb_hold_r__v21 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v22;
    __VdlySet__lb_hold_r__v22 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v23;
    __VdlySet__lb_hold_r__v23 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v24;
    __VdlySet__lb_hold_r__v24 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v25;
    __VdlySet__lb_hold_r__v25 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v26;
    __VdlySet__lb_hold_r__v26 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v27;
    __VdlySet__lb_hold_r__v27 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v28;
    __VdlySet__lb_hold_r__v28 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v29;
    __VdlySet__lb_hold_r__v29 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v30;
    __VdlySet__lb_hold_r__v30 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v31;
    __VdlySet__lb_hold_r__v31 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v32;
    __VdlySet__lb_hold_r__v32 = 0;
    CData/*0:0*/ __VdlySet__lb_hold_r__v33;
    __VdlySet__lb_hold_r__v33 = 0;
    CData/*2:0*/ __VdlyVal__q_wr_r__v0;
    __VdlyVal__q_wr_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_wr_r__v0;
    __VdlyDim0__q_wr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v0;
    __VdlySet__q_wr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v1;
    __VdlySet__q_wr_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v2;
    __VdlySet__q_wr_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v3;
    __VdlySet__q_wr_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v4;
    __VdlySet__q_wr_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v5;
    __VdlySet__q_wr_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v6;
    __VdlySet__q_wr_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v7;
    __VdlySet__q_wr_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v8;
    __VdlySet__q_wr_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v9;
    __VdlySet__q_wr_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v10;
    __VdlySet__q_wr_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v11;
    __VdlySet__q_wr_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v12;
    __VdlySet__q_wr_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v13;
    __VdlySet__q_wr_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v14;
    __VdlySet__q_wr_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v15;
    __VdlySet__q_wr_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v16;
    __VdlySet__q_wr_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v17;
    __VdlySet__q_wr_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v18;
    __VdlySet__q_wr_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v19;
    __VdlySet__q_wr_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v20;
    __VdlySet__q_wr_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v21;
    __VdlySet__q_wr_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v22;
    __VdlySet__q_wr_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v23;
    __VdlySet__q_wr_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v24;
    __VdlySet__q_wr_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v25;
    __VdlySet__q_wr_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v26;
    __VdlySet__q_wr_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v27;
    __VdlySet__q_wr_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v28;
    __VdlySet__q_wr_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v29;
    __VdlySet__q_wr_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v30;
    __VdlySet__q_wr_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v31;
    __VdlySet__q_wr_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v32;
    __VdlySet__q_wr_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_wr_r__v33;
    __VdlySet__q_wr_r__v33 = 0;
    CData/*3:0*/ __VdlyVal__q_cnt_r__v0;
    __VdlyVal__q_cnt_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_cnt_r__v0;
    __VdlyDim0__q_cnt_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v0;
    __VdlySet__q_cnt_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__q_cnt_r__v1;
    __VdlyVal__q_cnt_r__v1 = 0;
    CData/*4:0*/ __VdlyDim0__q_cnt_r__v1;
    __VdlyDim0__q_cnt_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v1;
    __VdlySet__q_cnt_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v2;
    __VdlySet__q_cnt_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v3;
    __VdlySet__q_cnt_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v4;
    __VdlySet__q_cnt_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v5;
    __VdlySet__q_cnt_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v6;
    __VdlySet__q_cnt_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v7;
    __VdlySet__q_cnt_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v8;
    __VdlySet__q_cnt_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v9;
    __VdlySet__q_cnt_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v10;
    __VdlySet__q_cnt_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v11;
    __VdlySet__q_cnt_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v12;
    __VdlySet__q_cnt_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v13;
    __VdlySet__q_cnt_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v14;
    __VdlySet__q_cnt_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v15;
    __VdlySet__q_cnt_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v16;
    __VdlySet__q_cnt_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v17;
    __VdlySet__q_cnt_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v18;
    __VdlySet__q_cnt_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v19;
    __VdlySet__q_cnt_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v20;
    __VdlySet__q_cnt_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v21;
    __VdlySet__q_cnt_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v22;
    __VdlySet__q_cnt_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v23;
    __VdlySet__q_cnt_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v24;
    __VdlySet__q_cnt_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v25;
    __VdlySet__q_cnt_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v26;
    __VdlySet__q_cnt_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v27;
    __VdlySet__q_cnt_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v28;
    __VdlySet__q_cnt_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v29;
    __VdlySet__q_cnt_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v30;
    __VdlySet__q_cnt_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v31;
    __VdlySet__q_cnt_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v32;
    __VdlySet__q_cnt_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v33;
    __VdlySet__q_cnt_r__v33 = 0;
    CData/*0:0*/ __VdlySet__q_cnt_r__v34;
    __VdlySet__q_cnt_r__v34 = 0;
    CData/*2:0*/ __VdlyVal__q_rd_r__v0;
    __VdlyVal__q_rd_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__q_rd_r__v0;
    __VdlyDim0__q_rd_r__v0 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v0;
    __VdlySet__q_rd_r__v0 = 0;
    CData/*2:0*/ __VdlyVal__q_rd_r__v1;
    __VdlyVal__q_rd_r__v1 = 0;
    CData/*4:0*/ __VdlyDim0__q_rd_r__v1;
    __VdlyDim0__q_rd_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v1;
    __VdlySet__q_rd_r__v1 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v2;
    __VdlySet__q_rd_r__v2 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v3;
    __VdlySet__q_rd_r__v3 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v4;
    __VdlySet__q_rd_r__v4 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v5;
    __VdlySet__q_rd_r__v5 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v6;
    __VdlySet__q_rd_r__v6 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v7;
    __VdlySet__q_rd_r__v7 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v8;
    __VdlySet__q_rd_r__v8 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v9;
    __VdlySet__q_rd_r__v9 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v10;
    __VdlySet__q_rd_r__v10 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v11;
    __VdlySet__q_rd_r__v11 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v12;
    __VdlySet__q_rd_r__v12 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v13;
    __VdlySet__q_rd_r__v13 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v14;
    __VdlySet__q_rd_r__v14 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v15;
    __VdlySet__q_rd_r__v15 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v16;
    __VdlySet__q_rd_r__v16 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v17;
    __VdlySet__q_rd_r__v17 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v18;
    __VdlySet__q_rd_r__v18 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v19;
    __VdlySet__q_rd_r__v19 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v20;
    __VdlySet__q_rd_r__v20 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v21;
    __VdlySet__q_rd_r__v21 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v22;
    __VdlySet__q_rd_r__v22 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v23;
    __VdlySet__q_rd_r__v23 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v24;
    __VdlySet__q_rd_r__v24 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v25;
    __VdlySet__q_rd_r__v25 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v26;
    __VdlySet__q_rd_r__v26 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v27;
    __VdlySet__q_rd_r__v27 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v28;
    __VdlySet__q_rd_r__v28 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v29;
    __VdlySet__q_rd_r__v29 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v30;
    __VdlySet__q_rd_r__v30 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v31;
    __VdlySet__q_rd_r__v31 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v32;
    __VdlySet__q_rd_r__v32 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v33;
    __VdlySet__q_rd_r__v33 = 0;
    CData/*0:0*/ __VdlySet__q_rd_r__v34;
    __VdlySet__q_rd_r__v34 = 0;
    CData/*4:0*/ __VdlyVal__skid_addr_r__v0;
    __VdlyVal__skid_addr_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_addr_r__v0;
    __VdlyDim0__skid_addr_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_addr_r__v0;
    __VdlySet__skid_addr_r__v0 = 0;
    CData/*4:0*/ __VdlyVal__skid_addr_r__v1;
    __VdlyVal__skid_addr_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_addr_r__v1;
    __VdlyDim0__skid_addr_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_addr_r__v1;
    __VdlySet__skid_addr_r__v1 = 0;
    CData/*3:0*/ __VdlyVal__skid_strm_r__v0;
    __VdlyVal__skid_strm_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_strm_r__v0;
    __VdlyDim0__skid_strm_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_strm_r__v0;
    __VdlySet__skid_strm_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__skid_strm_r__v1;
    __VdlyVal__skid_strm_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_strm_r__v1;
    __VdlyDim0__skid_strm_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_strm_r__v1;
    __VdlySet__skid_strm_r__v1 = 0;
    QData/*47:0*/ __VdlyVal__lb_q_r__v0;
    __VdlyVal__lb_q_r__v0 = 0;
    CData/*7:0*/ __VdlyDim0__lb_q_r__v0;
    __VdlyDim0__lb_q_r__v0 = 0;
    CData/*0:0*/ __VdlySet__lb_q_r__v0;
    __VdlySet__lb_q_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__skid_data_r__v0;
    __VdlyVal__skid_data_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__skid_data_r__v0;
    __VdlyDim0__skid_data_r__v0 = 0;
    CData/*0:0*/ __VdlySet__skid_data_r__v0;
    __VdlySet__skid_data_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__skid_data_r__v1;
    __VdlyVal__skid_data_r__v1 = 0;
    CData/*1:0*/ __VdlyDim0__skid_data_r__v1;
    __VdlyDim0__skid_data_r__v1 = 0;
    CData/*0:0*/ __VdlySet__skid_data_r__v1;
    __VdlySet__skid_data_r__v1 = 0;
    IData/*31:0*/ __Vilp1;
    // Body
    __Vdly__skid_wp_r = vlSelfRef.__PVT__skid_wp_r;
    __VdlySet__tdm_hold_r__v0 = 0U;
    __VdlySet__tdm_hold_r__v1 = 0U;
    __VdlySet__lb_q_r__v0 = 0U;
    __Vdly__skid_cnt_r = vlSelfRef.__PVT__skid_cnt_r;
    __VdlySet__map_r__v0 = 0U;
    __VdlySet__map_r__v1 = 0U;
    __VdlySet__skid_addr_r__v0 = 0U;
    __VdlySet__skid_addr_r__v1 = 0U;
    __Vdly__skid_rp_r = vlSelfRef.__PVT__skid_rp_r;
    __Vdly__st_r = vlSelfRef.__PVT__st_r;
    __Vdly__slot_r = vlSelfRef.__PVT__slot_r;
    __Vdly__pop_idx_r = vlSelfRef.__PVT__pop_idx_r;
    __VdlySet__skid_strm_r__v0 = 0U;
    __VdlySet__skid_strm_r__v1 = 0U;
    __VdlySet__q_wr_r__v0 = 0U;
    __VdlySet__q_wr_r__v1 = 0U;
    __VdlySet__q_wr_r__v2 = 0U;
    __VdlySet__q_wr_r__v3 = 0U;
    __VdlySet__q_wr_r__v4 = 0U;
    __VdlySet__q_wr_r__v5 = 0U;
    __VdlySet__q_wr_r__v6 = 0U;
    __VdlySet__q_wr_r__v7 = 0U;
    __VdlySet__q_wr_r__v8 = 0U;
    __VdlySet__q_wr_r__v9 = 0U;
    __VdlySet__q_wr_r__v10 = 0U;
    __VdlySet__q_wr_r__v11 = 0U;
    __VdlySet__q_wr_r__v12 = 0U;
    __VdlySet__q_wr_r__v13 = 0U;
    __VdlySet__q_wr_r__v14 = 0U;
    __VdlySet__q_wr_r__v15 = 0U;
    __VdlySet__q_wr_r__v16 = 0U;
    __VdlySet__q_wr_r__v17 = 0U;
    __VdlySet__q_wr_r__v18 = 0U;
    __VdlySet__q_wr_r__v19 = 0U;
    __VdlySet__q_wr_r__v20 = 0U;
    __VdlySet__q_wr_r__v21 = 0U;
    __VdlySet__q_wr_r__v22 = 0U;
    __VdlySet__q_wr_r__v23 = 0U;
    __VdlySet__q_wr_r__v24 = 0U;
    __VdlySet__q_wr_r__v25 = 0U;
    __VdlySet__q_wr_r__v26 = 0U;
    __VdlySet__q_wr_r__v27 = 0U;
    __VdlySet__q_wr_r__v28 = 0U;
    __VdlySet__q_wr_r__v29 = 0U;
    __VdlySet__q_wr_r__v30 = 0U;
    __VdlySet__q_wr_r__v31 = 0U;
    __VdlySet__q_wr_r__v32 = 0U;
    __VdlySet__q_wr_r__v33 = 0U;
    __VdlySet__q_rd_r__v0 = 0U;
    __VdlySet__q_rd_r__v1 = 0U;
    __VdlySet__q_rd_r__v2 = 0U;
    __VdlySet__q_rd_r__v3 = 0U;
    __VdlySet__q_rd_r__v4 = 0U;
    __VdlySet__q_rd_r__v5 = 0U;
    __VdlySet__q_rd_r__v6 = 0U;
    __VdlySet__q_rd_r__v7 = 0U;
    __VdlySet__q_rd_r__v8 = 0U;
    __VdlySet__q_rd_r__v9 = 0U;
    __VdlySet__q_rd_r__v10 = 0U;
    __VdlySet__q_rd_r__v11 = 0U;
    __VdlySet__q_rd_r__v12 = 0U;
    __VdlySet__q_rd_r__v13 = 0U;
    __VdlySet__q_rd_r__v14 = 0U;
    __VdlySet__q_rd_r__v15 = 0U;
    __VdlySet__q_rd_r__v16 = 0U;
    __VdlySet__q_rd_r__v17 = 0U;
    __VdlySet__q_rd_r__v18 = 0U;
    __VdlySet__q_rd_r__v19 = 0U;
    __VdlySet__q_rd_r__v20 = 0U;
    __VdlySet__q_rd_r__v21 = 0U;
    __VdlySet__q_rd_r__v22 = 0U;
    __VdlySet__q_rd_r__v23 = 0U;
    __VdlySet__q_rd_r__v24 = 0U;
    __VdlySet__q_rd_r__v25 = 0U;
    __VdlySet__q_rd_r__v26 = 0U;
    __VdlySet__q_rd_r__v27 = 0U;
    __VdlySet__q_rd_r__v28 = 0U;
    __VdlySet__q_rd_r__v29 = 0U;
    __VdlySet__q_rd_r__v30 = 0U;
    __VdlySet__q_rd_r__v31 = 0U;
    __VdlySet__q_rd_r__v32 = 0U;
    __VdlySet__q_rd_r__v33 = 0U;
    __VdlySet__q_rd_r__v34 = 0U;
    __VdlySet__lb_hold_r__v0 = 0U;
    __VdlySet__lb_hold_r__v1 = 0U;
    __VdlySet__lb_hold_r__v2 = 0U;
    __VdlySet__lb_hold_r__v3 = 0U;
    __VdlySet__lb_hold_r__v4 = 0U;
    __VdlySet__lb_hold_r__v5 = 0U;
    __VdlySet__lb_hold_r__v6 = 0U;
    __VdlySet__lb_hold_r__v7 = 0U;
    __VdlySet__lb_hold_r__v8 = 0U;
    __VdlySet__lb_hold_r__v9 = 0U;
    __VdlySet__lb_hold_r__v10 = 0U;
    __VdlySet__lb_hold_r__v11 = 0U;
    __VdlySet__lb_hold_r__v12 = 0U;
    __VdlySet__lb_hold_r__v13 = 0U;
    __VdlySet__lb_hold_r__v14 = 0U;
    __VdlySet__lb_hold_r__v15 = 0U;
    __VdlySet__lb_hold_r__v16 = 0U;
    __VdlySet__lb_hold_r__v17 = 0U;
    __VdlySet__lb_hold_r__v18 = 0U;
    __VdlySet__lb_hold_r__v19 = 0U;
    __VdlySet__lb_hold_r__v20 = 0U;
    __VdlySet__lb_hold_r__v21 = 0U;
    __VdlySet__lb_hold_r__v22 = 0U;
    __VdlySet__lb_hold_r__v23 = 0U;
    __VdlySet__lb_hold_r__v24 = 0U;
    __VdlySet__lb_hold_r__v25 = 0U;
    __VdlySet__lb_hold_r__v26 = 0U;
    __VdlySet__lb_hold_r__v27 = 0U;
    __VdlySet__lb_hold_r__v28 = 0U;
    __VdlySet__lb_hold_r__v29 = 0U;
    __VdlySet__lb_hold_r__v30 = 0U;
    __VdlySet__lb_hold_r__v31 = 0U;
    __VdlySet__lb_hold_r__v32 = 0U;
    __VdlySet__lb_hold_r__v33 = 0U;
    __VdlySet__q_cnt_r__v0 = 0U;
    __VdlySet__q_cnt_r__v1 = 0U;
    __VdlySet__q_cnt_r__v2 = 0U;
    __VdlySet__q_cnt_r__v3 = 0U;
    __VdlySet__q_cnt_r__v4 = 0U;
    __VdlySet__q_cnt_r__v5 = 0U;
    __VdlySet__q_cnt_r__v6 = 0U;
    __VdlySet__q_cnt_r__v7 = 0U;
    __VdlySet__q_cnt_r__v8 = 0U;
    __VdlySet__q_cnt_r__v9 = 0U;
    __VdlySet__q_cnt_r__v10 = 0U;
    __VdlySet__q_cnt_r__v11 = 0U;
    __VdlySet__q_cnt_r__v12 = 0U;
    __VdlySet__q_cnt_r__v13 = 0U;
    __VdlySet__q_cnt_r__v14 = 0U;
    __VdlySet__q_cnt_r__v15 = 0U;
    __VdlySet__q_cnt_r__v16 = 0U;
    __VdlySet__q_cnt_r__v17 = 0U;
    __VdlySet__q_cnt_r__v18 = 0U;
    __VdlySet__q_cnt_r__v19 = 0U;
    __VdlySet__q_cnt_r__v20 = 0U;
    __VdlySet__q_cnt_r__v21 = 0U;
    __VdlySet__q_cnt_r__v22 = 0U;
    __VdlySet__q_cnt_r__v23 = 0U;
    __VdlySet__q_cnt_r__v24 = 0U;
    __VdlySet__q_cnt_r__v25 = 0U;
    __VdlySet__q_cnt_r__v26 = 0U;
    __VdlySet__q_cnt_r__v27 = 0U;
    __VdlySet__q_cnt_r__v28 = 0U;
    __VdlySet__q_cnt_r__v29 = 0U;
    __VdlySet__q_cnt_r__v30 = 0U;
    __VdlySet__q_cnt_r__v31 = 0U;
    __VdlySet__q_cnt_r__v32 = 0U;
    __VdlySet__q_cnt_r__v33 = 0U;
    __VdlySet__q_cnt_r__v34 = 0U;
    __VdlySet__skid_data_r__v0 = 0U;
    __VdlySet__skid_data_r__v1 = 0U;
    if (vlSymsp->TOP.rst_n) {
        __Vdly__skid_wp_r = (3U & ((IData)(vlSelfRef.__PVT__skid_wp_r) 
                                   + (IData)(vlSelfRef.__PVT__skid_enq_n_w)));
        if (((IData)(vlSymsp->TOP.tdm_pair_valid_i) 
             & (4U > (IData)(vlSymsp->TOP.tdm_pair_slot_i)))) {
            __VdlyVal__tdm_hold_r__v0 = (((QData)((IData)(vlSymsp->TOP.tdm_l_i)) 
                                          << 0x00000018U) 
                                         | (QData)((IData)(vlSymsp->TOP.tdm_r_i)));
            __VdlyDim0__tdm_hold_r__v0 = (3U & (IData)(vlSymsp->TOP.tdm_pair_slot_i));
            __VdlySet__tdm_hold_r__v0 = 1U;
        }
        vlSelfRef.__PVT__q_primed_r = ((vlSelfRef.__PVT__q_primed_r 
                                        | vlSelfRef.__PVT__prime_set_w) 
                                       & (~ vlSelfRef.__PVT__flush_clr_w));
        if (vlSelfRef.__PVT__push_ram_w) {
            __VdlyVal__lb_q_r__v0 = vlSelfRef.__PVT__skid_data_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlyDim0__lb_q_r__v0 = (((IData)(vlSelfRef.__PVT__skid_addr_r
                                               [vlSelfRef.__PVT__skid_rp_r]) 
                                       << 3U) | vlSelfRef.__PVT__q_wr_r
                                      [vlSelfRef.__PVT__skid_addr_r
                                      [vlSelfRef.__PVT__skid_rp_r]]);
            __VdlySet__lb_q_r__v0 = 1U;
            __VdlyVal__q_wr_r__v0 = (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__q_wr_r
                                                     [vlSelfRef.__PVT__skid_addr_r
                                                     [vlSelfRef.__PVT__skid_rp_r]])));
            __VdlyDim0__q_wr_r__v0 = vlSelfRef.__PVT__skid_addr_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlySet__q_wr_r__v0 = 1U;
            if (vlSelfRef.__PVT__push_drop_w) {
                __VdlyVal__q_rd_r__v1 = (7U & ((IData)(1U) 
                                               + ((IData)(vlSelfRef.__PVT__q_rd_r
                                                          [vlSelfRef.__PVT__skid_addr_r
                                                          [vlSelfRef.__PVT__skid_rp_r]]) 
                                                  + (IData)(vlSelfRef.__PVT__push_same_w))));
                __VdlyDim0__q_rd_r__v1 = vlSelfRef.__PVT__skid_addr_r
                    [vlSelfRef.__PVT__skid_rp_r];
                __VdlySet__q_rd_r__v1 = 1U;
                __VdlyVal__q_cnt_r__v1 = (0x0000000fU 
                                          & (IData)(vlSelfRef.__PVT__push_cnt1_w));
            } else {
                __VdlyVal__q_cnt_r__v1 = (0x0000000fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSelfRef.__PVT__push_cnt1_w)));
            }
            __VdlyDim0__q_cnt_r__v1 = vlSelfRef.__PVT__skid_addr_r
                [vlSelfRef.__PVT__skid_rp_r];
            __VdlySet__q_cnt_r__v1 = 1U;
            vlSelfRef.__PVT__q_fed_r = (vlSelfRef.__PVT__q_fed_r 
                                        | (0x00000000ffffffffULL 
                                           & ((IData)(1U) 
                                              << vlSelfRef.__PVT__skid_addr_r
                                              [vlSelfRef.__PVT__skid_rp_r])));
        }
        __Vdly__skid_cnt_r = (7U & (((IData)(vlSelfRef.__PVT__skid_cnt_r) 
                                     + (IData)(vlSelfRef.__PVT__skid_enq_n_w)) 
                                    - ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                        ? 1U : 0U)));
        if (vlSymsp->TOP.b_map_wr_en_i) {
            __VdlyVal__map_r__v0 = vlSymsp->TOP.b_map_wr_data_i;
            __VdlyDim0__map_r__v0 = vlSymsp->TOP.b_map_wr_addr_i;
            __VdlySet__map_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__enq0_v_w) {
            if (vlSelfRef.__PVT__cm0_v_w) {
                __VdlyVal__skid_addr_r__v0 = vlSelfRef.__PVT__lb_a0_w;
                __VdlyVal__skid_data_r__v0 = ((1U & (IData)(vlSelfRef.__PVT__lb_chpos_r))
                                               ? (((QData)((IData)(
                                                                   (vlSelfRef.__PVT__stash_val_r 
                                                                    & (- (IData)((IData)(vlSelfRef.__PVT__stash_vld_r)))))) 
                                                   << 0x00000018U) 
                                                  | (QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)))
                                               : ((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                                  << 0x00000018U));
            } else {
                __VdlyVal__skid_addr_r__v0 = vlSelfRef.__PVT__cm1_addr_w;
                __VdlyVal__skid_data_r__v0 = vlSelfRef.__PVT__cm1_data_w;
            }
            __VdlyDim0__skid_addr_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_addr_r__v0 = 1U;
            __VdlyVal__skid_strm_r__v0 = vlSelfRef.lb_tuser_i;
            __VdlyDim0__skid_strm_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_strm_r__v0 = 1U;
            __VdlyDim0__skid_data_r__v0 = vlSelfRef.__PVT__skid_wp_r;
            __VdlySet__skid_data_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__enq1_v_w) {
            __VdlyVal__skid_addr_r__v1 = vlSelfRef.__PVT__cm1_addr_w;
            __VdlyDim0__skid_addr_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_addr_r__v1 = 1U;
            __VdlyVal__skid_strm_r__v1 = vlSelfRef.lb_tuser_i;
            __VdlyDim0__skid_strm_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_strm_r__v1 = 1U;
            __VdlyVal__skid_data_r__v1 = vlSelfRef.__PVT__cm1_data_w;
            __VdlyDim0__skid_data_r__v1 = (3U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__skid_wp_r)));
            __VdlySet__skid_data_r__v1 = 1U;
        }
        __Vdly__skid_rp_r = (3U & ((IData)(vlSelfRef.__PVT__skid_rp_r) 
                                   + ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                       ? 1U : 0U)));
        vlSelfRef.__PVT__skid_v_r = (0x0000000fU & 
                                     (((((IData)(vlSelfRef.__PVT__skid_v_r) 
                                         & (~ ((0U 
                                                != (IData)(vlSelfRef.__PVT__skid_cnt_r))
                                                ? ((IData)(1U) 
                                                   << (IData)(vlSelfRef.__PVT__skid_rp_r))
                                                : 0U))) 
                                        & (~ (IData)(vlSelfRef.__PVT__skid_kill_w))) 
                                       | ((IData)(vlSelfRef.__PVT__enq0_v_w)
                                           ? ((IData)(1U) 
                                              << (IData)(vlSelfRef.__PVT__skid_wp_r))
                                           : 0U)) | 
                                      ((IData)(vlSelfRef.__PVT__enq1_v_w)
                                        ? ((IData)(1U) 
                                           << (3U & 
                                               ((IData)(1U) 
                                                + (IData)(vlSelfRef.__PVT__skid_wp_r))))
                                        : 0U)));
        if ((1U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v1 = 1U;
            __VdlySet__q_rd_r__v2 = 1U;
            __VdlySet__lb_hold_r__v1 = 1U;
            __VdlySet__q_cnt_r__v2 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffeU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((2U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v2 = 1U;
            __VdlySet__q_rd_r__v3 = 1U;
            __VdlySet__lb_hold_r__v2 = 1U;
            __VdlySet__q_cnt_r__v3 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffdU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((4U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v3 = 1U;
            __VdlySet__q_rd_r__v4 = 1U;
            __VdlySet__lb_hold_r__v3 = 1U;
            __VdlySet__q_cnt_r__v4 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffffbU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((8U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v4 = 1U;
            __VdlySet__q_rd_r__v5 = 1U;
            __VdlySet__lb_hold_r__v4 = 1U;
            __VdlySet__q_cnt_r__v5 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffff7U 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000010U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v5 = 1U;
            __VdlySet__q_rd_r__v6 = 1U;
            __VdlySet__lb_hold_r__v5 = 1U;
            __VdlySet__q_cnt_r__v6 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffefU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000020U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v6 = 1U;
            __VdlySet__q_rd_r__v7 = 1U;
            __VdlySet__lb_hold_r__v6 = 1U;
            __VdlySet__q_cnt_r__v7 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffdfU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000040U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v7 = 1U;
            __VdlySet__q_rd_r__v8 = 1U;
            __VdlySet__lb_hold_r__v7 = 1U;
            __VdlySet__q_cnt_r__v8 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffffbfU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000080U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v8 = 1U;
            __VdlySet__q_rd_r__v9 = 1U;
            __VdlySet__lb_hold_r__v8 = 1U;
            __VdlySet__q_cnt_r__v9 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffff7fU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000100U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v9 = 1U;
            __VdlySet__q_rd_r__v10 = 1U;
            __VdlySet__lb_hold_r__v9 = 1U;
            __VdlySet__q_cnt_r__v10 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffeffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000200U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v10 = 1U;
            __VdlySet__q_rd_r__v11 = 1U;
            __VdlySet__lb_hold_r__v10 = 1U;
            __VdlySet__q_cnt_r__v11 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffdffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000400U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v11 = 1U;
            __VdlySet__q_rd_r__v12 = 1U;
            __VdlySet__lb_hold_r__v11 = 1U;
            __VdlySet__q_cnt_r__v12 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffffbffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00000800U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v12 = 1U;
            __VdlySet__q_rd_r__v13 = 1U;
            __VdlySet__lb_hold_r__v12 = 1U;
            __VdlySet__q_cnt_r__v13 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffff7ffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00001000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v13 = 1U;
            __VdlySet__q_rd_r__v14 = 1U;
            __VdlySet__lb_hold_r__v13 = 1U;
            __VdlySet__q_cnt_r__v14 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffefffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00002000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v14 = 1U;
            __VdlySet__q_rd_r__v15 = 1U;
            __VdlySet__lb_hold_r__v14 = 1U;
            __VdlySet__q_cnt_r__v15 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffdfffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00004000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v15 = 1U;
            __VdlySet__q_rd_r__v16 = 1U;
            __VdlySet__lb_hold_r__v15 = 1U;
            __VdlySet__q_cnt_r__v16 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffffbfffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00008000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v16 = 1U;
            __VdlySet__q_rd_r__v17 = 1U;
            __VdlySet__lb_hold_r__v16 = 1U;
            __VdlySet__q_cnt_r__v17 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffff7fffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00010000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v17 = 1U;
            __VdlySet__q_rd_r__v18 = 1U;
            __VdlySet__lb_hold_r__v17 = 1U;
            __VdlySet__q_cnt_r__v18 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffeffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00020000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v18 = 1U;
            __VdlySet__q_rd_r__v19 = 1U;
            __VdlySet__lb_hold_r__v18 = 1U;
            __VdlySet__q_cnt_r__v19 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffdffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00040000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v19 = 1U;
            __VdlySet__q_rd_r__v20 = 1U;
            __VdlySet__lb_hold_r__v19 = 1U;
            __VdlySet__q_cnt_r__v20 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfffbffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00080000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v20 = 1U;
            __VdlySet__q_rd_r__v21 = 1U;
            __VdlySet__lb_hold_r__v20 = 1U;
            __VdlySet__q_cnt_r__v21 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfff7ffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00100000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v21 = 1U;
            __VdlySet__q_rd_r__v22 = 1U;
            __VdlySet__lb_hold_r__v21 = 1U;
            __VdlySet__q_cnt_r__v22 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffefffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00200000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v22 = 1U;
            __VdlySet__q_rd_r__v23 = 1U;
            __VdlySet__lb_hold_r__v22 = 1U;
            __VdlySet__q_cnt_r__v23 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffdfffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00400000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v23 = 1U;
            __VdlySet__q_rd_r__v24 = 1U;
            __VdlySet__lb_hold_r__v23 = 1U;
            __VdlySet__q_cnt_r__v24 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xffbfffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x00800000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v24 = 1U;
            __VdlySet__q_rd_r__v25 = 1U;
            __VdlySet__lb_hold_r__v24 = 1U;
            __VdlySet__q_cnt_r__v25 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xff7fffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x01000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v25 = 1U;
            __VdlySet__q_rd_r__v26 = 1U;
            __VdlySet__lb_hold_r__v25 = 1U;
            __VdlySet__q_cnt_r__v26 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfeffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x02000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v26 = 1U;
            __VdlySet__q_rd_r__v27 = 1U;
            __VdlySet__lb_hold_r__v26 = 1U;
            __VdlySet__q_cnt_r__v27 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfdffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x04000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v27 = 1U;
            __VdlySet__q_rd_r__v28 = 1U;
            __VdlySet__lb_hold_r__v27 = 1U;
            __VdlySet__q_cnt_r__v28 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xfbffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x08000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v28 = 1U;
            __VdlySet__q_rd_r__v29 = 1U;
            __VdlySet__lb_hold_r__v28 = 1U;
            __VdlySet__q_cnt_r__v29 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xf7ffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x10000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v29 = 1U;
            __VdlySet__q_rd_r__v30 = 1U;
            __VdlySet__lb_hold_r__v29 = 1U;
            __VdlySet__q_cnt_r__v30 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xefffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x20000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v30 = 1U;
            __VdlySet__q_rd_r__v31 = 1U;
            __VdlySet__lb_hold_r__v30 = 1U;
            __VdlySet__q_cnt_r__v31 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xdfffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((0x40000000U & vlSelfRef.__PVT__flush_clr_w)) {
            __VdlySet__q_wr_r__v31 = 1U;
            __VdlySet__q_rd_r__v32 = 1U;
            __VdlySet__lb_hold_r__v31 = 1U;
            __VdlySet__q_cnt_r__v32 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0xbfffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if ((vlSelfRef.__PVT__flush_clr_w >> 0x1fU)) {
            __VdlySet__q_wr_r__v32 = 1U;
            __VdlySet__q_rd_r__v33 = 1U;
            __VdlySet__lb_hold_r__v32 = 1U;
            __VdlySet__q_cnt_r__v33 = 1U;
            vlSelfRef.__PVT__q_fed_r = (0x7fffffffU 
                                        & vlSelfRef.__PVT__q_fed_r);
        }
        if (vlSelfRef.__PVT__pop_act_w) {
            __VdlyVal__q_rd_r__v0 = (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__q_rd_r
                                                     [
                                                     (0x0000001fU 
                                                      & (IData)(vlSelfRef.__PVT__pop_idx_r))])));
            __VdlyDim0__q_rd_r__v0 = (0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r));
            __VdlySet__q_rd_r__v0 = 1U;
            __VdlyVal__q_cnt_r__v0 = (0x0000000fU & 
                                      ((IData)(vlSelfRef.__PVT__q_cnt_r
                                               [(0x0000001fU 
                                                 & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                       - (IData)(1U)));
            __VdlyDim0__q_cnt_r__v0 = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__pop_idx_r));
            __VdlySet__q_cnt_r__v0 = 1U;
        }
        if (vlSelfRef.__PVT__pop_ret_v_r) {
            __VdlyVal__lb_hold_r__v0 = vlSelfRef.__PVT__q_rdata_r;
            __VdlyDim0__lb_hold_r__v0 = vlSelfRef.__PVT__pop_ret_pair_r;
            __VdlySet__lb_hold_r__v0 = 1U;
        }
        vlSelfRef.map_rd_valid_o = 0U;
        if (vlSymsp->TOP.b_map_rd_en_i) {
            vlSelfRef.map_rd_valid_o = 1U;
            vlSelfRef.map_rd_data_o = (((IData)(vlSelfRef.__PVT__loop_fed_r) 
                                        << 0x0000000eU) 
                                       | (((IData)(vlSelfRef.__PVT__loop_mapped_w) 
                                           << 0x0000000dU) 
                                          | vlSelfRef.__PVT__map_r
                                          [vlSymsp->TOP.b_map_rd_addr_i]));
        }
        if ((2U == (((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.__PVT__tdm_frame_ev_w) 
                     << 1U) | (IData)(vlSymsp->TOP.b_tick_i)))) {
            vlSelfRef.tdm_fed_r = 1U;
            vlSelfRef.tdm_frame_pend_r = 1U;
        } else {
            if ((1U != (((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.__PVT__tdm_frame_ev_w) 
                         << 1U) | (IData)(vlSymsp->TOP.b_tick_i)))) {
                if ((3U == (((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.__PVT__tdm_frame_ev_w) 
                             << 1U) | (IData)(vlSymsp->TOP.b_tick_i)))) {
                    vlSelfRef.tdm_fed_r = 1U;
                }
            }
            if ((1U == (((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.__PVT__tdm_frame_ev_w) 
                         << 1U) | (IData)(vlSymsp->TOP.b_tick_i)))) {
                vlSelfRef.tdm_frame_pend_r = 0U;
            } else if ((3U == (((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.__PVT__tdm_frame_ev_w) 
                                << 1U) | (IData)(vlSymsp->TOP.b_tick_i)))) {
                vlSelfRef.tdm_frame_pend_r = 0U;
            }
        }
        vlSelfRef.lb_dup_cnt_o = ((0x00010000U & vlSelfRef.__PVT__dup_sum_w)
                                   ? 0x0000ffffU : 
                                  (0x0000ffffU & vlSelfRef.__PVT__dup_sum_w));
        vlSelfRef.lb_skip_cnt_o = ((0x00010000U & vlSelfRef.__PVT__skip_sum_w)
                                    ? 0x0000ffffU : 
                                   (0x0000ffffU & vlSelfRef.__PVT__skip_sum_w));
        if (vlSymsp->TOP.i2s_pair_valid_i) {
            vlSelfRef.__PVT__i2s_hold_r = (((QData)((IData)(vlSymsp->TOP.i2s_l_i)) 
                                            << 0x00000018U) 
                                           | (QData)((IData)(vlSymsp->TOP.i2s_r_i)));
        }
        if (vlSelfRef.lb_tvalid_i) {
            if (vlSelfRef.__PVT__stash_open_w) {
                vlSelfRef.__PVT__stash_strm_r = vlSelfRef.lb_tuser_i;
                vlSelfRef.__PVT__stash_val_r = vlSelfRef.__PVT__lb_smp1_w;
                vlSelfRef.__PVT__stash_vld_r = 1U;
            } else {
                vlSelfRef.__PVT__stash_vld_r = 0U;
            }
            vlSelfRef.__PVT__lb_chpos_r = (0x0000000fU 
                                           & (((IData)(1U) 
                                               + (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                                              & ((- (IData)(
                                                            (1U 
                                                             & (~ (IData)(vlSelfRef.lb_tlast_i))))) 
                                                 & (- (IData)(
                                                              ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                               != 
                                                               (0x0000000fU 
                                                                & ((IData)(1U) 
                                                                   + (IData)(vlSelfRef.__PVT__lb_ch1_w)))))))));
            vlSelfRef.__PVT__loop_fed_r = 1U;
        }
        if ((2U & (IData)(vlSelfRef.__PVT__st_r))) {
            if ((1U & (IData)(vlSelfRef.__PVT__st_r))) {
                vlSelfRef.pair_valid_o = 0U;
                if ((0U == (IData)(vlSelfRef.__PVT__gap_r))) {
                    if ((0x1fU == (IData)(vlSelfRef.__PVT__slot_r))) {
                        __Vdly__st_r = 0U;
                    } else {
                        __Vdly__slot_r = (0x0000001fU 
                                          & ((IData)(1U) 
                                             + (IData)(vlSelfRef.__PVT__slot_r)));
                        __Vdly__st_r = 2U;
                    }
                } else {
                    vlSelfRef.__PVT__gap_r = (0x0000001fU 
                                              & ((IData)(vlSelfRef.__PVT__gap_r) 
                                                 - (IData)(1U)));
                }
            } else {
                vlSelfRef.__PVT__gap_r = 0x18U;
                vlSelfRef.pair_valid_o = 1U;
                vlSelfRef.pair_slot_o = vlSelfRef.__PVT__slot_r;
                __Vdly__st_r = 3U;
                vlSelfRef.pair_l_o = (0x00ffffffU & 
                                      ((0x00000800U 
                                        & vlSelfRef.__PVT__map_r
                                        [((IData)(vlSelfRef.__PVT__slot_r) 
                                          << 1U)]) ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34)
                                        : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34 
                                                   >> 0x00000018U))));
                vlSelfRef.pair_r_o = (0x00ffffffU & 
                                      ((0x00000800U 
                                        & vlSelfRef.__PVT__map_r
                                        [(1U | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                << 1U))])
                                        ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)
                                        : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 
                                                   >> 0x00000018U))));
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__st_r))) {
            if ((0x20U == (IData)(vlSelfRef.__PVT__pop_idx_r))) {
                __Vdly__st_r = 2U;
            } else {
                __Vdly__pop_idx_r = (0x0000003fU & 
                                     ((IData)(1U) + (IData)(vlSelfRef.__PVT__pop_idx_r)));
            }
        } else {
            vlSelfRef.pair_valid_o = 0U;
            if (vlSelfRef.__PVT__tick_pend_r) {
                __Vdly__slot_r = 0U;
                vlSelfRef.__PVT__tick_pend_r = 0U;
                __Vdly__pop_idx_r = 0U;
                __Vdly__st_r = 1U;
            }
        }
        if (vlSymsp->TOP.b_tick_i) {
            vlSelfRef.__PVT__tick_pend_r = 1U;
        }
        vlSelfRef.__PVT__pop_ret_pair_r = (0x0000001fU 
                                           & (IData)(vlSelfRef.__PVT__pop_idx_r));
        vlSelfRef.__PVT__q_rdata_r = vlSelfRef.__PVT__lb_q_r
            [((0x000000f8U & ((IData)(vlSelfRef.__PVT__pop_idx_r) 
                              << 3U)) | vlSelfRef.__PVT__q_rd_r
              [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))])];
        if (vlSelfRef.__PVT__stash_flush_w) {
            vlSelfRef.__PVT__stash_vld_r = 0U;
        }
    } else {
        __Vdly__skid_wp_r = 0U;
        __VdlySet__tdm_hold_r__v1 = 1U;
        vlSelfRef.__PVT__q_primed_r = 0U;
        __Vdly__skid_cnt_r = 0U;
        __VdlySet__map_r__v1 = 1U;
        vlSelfRef.__PVT__skid_v_r = 0U;
        __Vdly__skid_rp_r = 0U;
        __VdlySet__q_wr_r__v33 = 1U;
        __VdlySet__q_rd_r__v34 = 1U;
        __VdlySet__lb_hold_r__v33 = 1U;
        __VdlySet__q_cnt_r__v34 = 1U;
        vlSelfRef.map_rd_valid_o = 0U;
        vlSelfRef.tdm_fed_r = 0U;
        vlSelfRef.tdm_frame_pend_r = 0U;
        vlSelfRef.lb_dup_cnt_o = 0U;
        vlSelfRef.lb_skip_cnt_o = 0U;
        vlSelfRef.__PVT__i2s_hold_r = 0ULL;
        vlSelfRef.__PVT__q_fed_r = 0U;
        vlSelfRef.map_rd_data_o = 0U;
        vlSelfRef.__PVT__stash_strm_r = 0U;
        vlSelfRef.__PVT__tick_pend_r = 0U;
        __Vdly__slot_r = 0U;
        vlSelfRef.__PVT__gap_r = 0U;
        __Vdly__st_r = 0U;
        __Vdly__pop_idx_r = 0U;
        vlSelfRef.pair_valid_o = 0U;
        vlSelfRef.pair_slot_o = 0U;
        vlSelfRef.pair_l_o = 0U;
        vlSelfRef.pair_r_o = 0U;
        vlSelfRef.__PVT__pop_ret_pair_r = 0U;
        vlSelfRef.__PVT__q_rdata_r = 0ULL;
        vlSelfRef.__PVT__stash_vld_r = 0U;
        vlSelfRef.__PVT__stash_val_r = 0U;
        vlSelfRef.__PVT__lb_chpos_r = 0U;
        vlSelfRef.__PVT__loop_fed_r = 0U;
    }
    if (__VdlySet__tdm_hold_r__v0) {
        vlSelfRef.tdm_hold_r[__VdlyDim0__tdm_hold_r__v0] 
            = __VdlyVal__tdm_hold_r__v0;
    }
    if (__VdlySet__tdm_hold_r__v1) {
        vlSelfRef.tdm_hold_r[0U] = 0ULL;
        vlSelfRef.tdm_hold_r[1U] = 0ULL;
        vlSelfRef.tdm_hold_r[2U] = 0ULL;
        vlSelfRef.tdm_hold_r[3U] = 0ULL;
    }
    vlSelfRef.__PVT__skid_cnt_r = __Vdly__skid_cnt_r;
    if (__VdlySet__skid_strm_r__v0) {
        vlSelfRef.__PVT__skid_strm_r[__VdlyDim0__skid_strm_r__v0] 
            = __VdlyVal__skid_strm_r__v0;
    }
    if (__VdlySet__skid_strm_r__v1) {
        vlSelfRef.__PVT__skid_strm_r[__VdlyDim0__skid_strm_r__v1] 
            = __VdlyVal__skid_strm_r__v1;
    }
    if (__VdlySet__q_wr_r__v0) {
        vlSelfRef.__PVT__q_wr_r[__VdlyDim0__q_wr_r__v0] 
            = __VdlyVal__q_wr_r__v0;
    }
    if (__VdlySet__q_wr_r__v1) {
        vlSelfRef.__PVT__q_wr_r[0U] = 0U;
    }
    if (__VdlySet__q_wr_r__v2) {
        vlSelfRef.__PVT__q_wr_r[1U] = 0U;
    }
    if (__VdlySet__q_wr_r__v3) {
        vlSelfRef.__PVT__q_wr_r[2U] = 0U;
    }
    if (__VdlySet__q_wr_r__v4) {
        vlSelfRef.__PVT__q_wr_r[3U] = 0U;
    }
    if (__VdlySet__q_wr_r__v5) {
        vlSelfRef.__PVT__q_wr_r[4U] = 0U;
    }
    if (__VdlySet__q_wr_r__v6) {
        vlSelfRef.__PVT__q_wr_r[5U] = 0U;
    }
    if (__VdlySet__q_wr_r__v7) {
        vlSelfRef.__PVT__q_wr_r[6U] = 0U;
    }
    if (__VdlySet__q_wr_r__v8) {
        vlSelfRef.__PVT__q_wr_r[7U] = 0U;
    }
    if (__VdlySet__q_wr_r__v9) {
        vlSelfRef.__PVT__q_wr_r[8U] = 0U;
    }
    if (__VdlySet__q_wr_r__v10) {
        vlSelfRef.__PVT__q_wr_r[9U] = 0U;
    }
    if (__VdlySet__q_wr_r__v11) {
        vlSelfRef.__PVT__q_wr_r[10U] = 0U;
    }
    if (__VdlySet__q_wr_r__v12) {
        vlSelfRef.__PVT__q_wr_r[11U] = 0U;
    }
    if (__VdlySet__q_wr_r__v13) {
        vlSelfRef.__PVT__q_wr_r[12U] = 0U;
    }
    if (__VdlySet__q_wr_r__v14) {
        vlSelfRef.__PVT__q_wr_r[13U] = 0U;
    }
    if (__VdlySet__q_wr_r__v15) {
        vlSelfRef.__PVT__q_wr_r[14U] = 0U;
    }
    if (__VdlySet__q_wr_r__v16) {
        vlSelfRef.__PVT__q_wr_r[15U] = 0U;
    }
    if (__VdlySet__q_wr_r__v17) {
        vlSelfRef.__PVT__q_wr_r[16U] = 0U;
    }
    if (__VdlySet__q_wr_r__v18) {
        vlSelfRef.__PVT__q_wr_r[17U] = 0U;
    }
    if (__VdlySet__q_wr_r__v19) {
        vlSelfRef.__PVT__q_wr_r[18U] = 0U;
    }
    if (__VdlySet__q_wr_r__v20) {
        vlSelfRef.__PVT__q_wr_r[19U] = 0U;
    }
    if (__VdlySet__q_wr_r__v21) {
        vlSelfRef.__PVT__q_wr_r[20U] = 0U;
    }
    if (__VdlySet__q_wr_r__v22) {
        vlSelfRef.__PVT__q_wr_r[21U] = 0U;
    }
    if (__VdlySet__q_wr_r__v23) {
        vlSelfRef.__PVT__q_wr_r[22U] = 0U;
    }
    if (__VdlySet__q_wr_r__v24) {
        vlSelfRef.__PVT__q_wr_r[23U] = 0U;
    }
    if (__VdlySet__q_wr_r__v25) {
        vlSelfRef.__PVT__q_wr_r[24U] = 0U;
    }
    if (__VdlySet__q_wr_r__v26) {
        vlSelfRef.__PVT__q_wr_r[25U] = 0U;
    }
    if (__VdlySet__q_wr_r__v27) {
        vlSelfRef.__PVT__q_wr_r[26U] = 0U;
    }
    if (__VdlySet__q_wr_r__v28) {
        vlSelfRef.__PVT__q_wr_r[27U] = 0U;
    }
    if (__VdlySet__q_wr_r__v29) {
        vlSelfRef.__PVT__q_wr_r[28U] = 0U;
    }
    if (__VdlySet__q_wr_r__v30) {
        vlSelfRef.__PVT__q_wr_r[29U] = 0U;
    }
    if (__VdlySet__q_wr_r__v31) {
        vlSelfRef.__PVT__q_wr_r[30U] = 0U;
    }
    if (__VdlySet__q_wr_r__v32) {
        vlSelfRef.__PVT__q_wr_r[31U] = 0U;
    }
    if (__VdlySet__q_wr_r__v33) {
        vlSelfRef.__PVT__q_wr_r[0U] = 0U;
        vlSelfRef.__PVT__q_wr_r[1U] = 0U;
        vlSelfRef.__PVT__q_wr_r[2U] = 0U;
        vlSelfRef.__PVT__q_wr_r[3U] = 0U;
        vlSelfRef.__PVT__q_wr_r[4U] = 0U;
        vlSelfRef.__PVT__q_wr_r[5U] = 0U;
        vlSelfRef.__PVT__q_wr_r[6U] = 0U;
        vlSelfRef.__PVT__q_wr_r[7U] = 0U;
        vlSelfRef.__PVT__q_wr_r[8U] = 0U;
        vlSelfRef.__PVT__q_wr_r[9U] = 0U;
        vlSelfRef.__PVT__q_wr_r[10U] = 0U;
        vlSelfRef.__PVT__q_wr_r[11U] = 0U;
        vlSelfRef.__PVT__q_wr_r[12U] = 0U;
        vlSelfRef.__PVT__q_wr_r[13U] = 0U;
        vlSelfRef.__PVT__q_wr_r[14U] = 0U;
        vlSelfRef.__PVT__q_wr_r[15U] = 0U;
        vlSelfRef.__PVT__q_wr_r[16U] = 0U;
        vlSelfRef.__PVT__q_wr_r[17U] = 0U;
        vlSelfRef.__PVT__q_wr_r[18U] = 0U;
        vlSelfRef.__PVT__q_wr_r[19U] = 0U;
        vlSelfRef.__PVT__q_wr_r[20U] = 0U;
        vlSelfRef.__PVT__q_wr_r[21U] = 0U;
        vlSelfRef.__PVT__q_wr_r[22U] = 0U;
        vlSelfRef.__PVT__q_wr_r[23U] = 0U;
        vlSelfRef.__PVT__q_wr_r[24U] = 0U;
        vlSelfRef.__PVT__q_wr_r[25U] = 0U;
        vlSelfRef.__PVT__q_wr_r[26U] = 0U;
        vlSelfRef.__PVT__q_wr_r[27U] = 0U;
        vlSelfRef.__PVT__q_wr_r[28U] = 0U;
        vlSelfRef.__PVT__q_wr_r[29U] = 0U;
        vlSelfRef.__PVT__q_wr_r[30U] = 0U;
        vlSelfRef.__PVT__q_wr_r[31U] = 0U;
    }
    if (__VdlySet__lb_hold_r__v0) {
        vlSelfRef.__PVT__lb_hold_r[__VdlyDim0__lb_hold_r__v0] 
            = __VdlyVal__lb_hold_r__v0;
    }
    if (__VdlySet__lb_hold_r__v1) {
        vlSelfRef.__PVT__lb_hold_r[0U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v2) {
        vlSelfRef.__PVT__lb_hold_r[1U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v3) {
        vlSelfRef.__PVT__lb_hold_r[2U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v4) {
        vlSelfRef.__PVT__lb_hold_r[3U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v5) {
        vlSelfRef.__PVT__lb_hold_r[4U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v6) {
        vlSelfRef.__PVT__lb_hold_r[5U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v7) {
        vlSelfRef.__PVT__lb_hold_r[6U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v8) {
        vlSelfRef.__PVT__lb_hold_r[7U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v9) {
        vlSelfRef.__PVT__lb_hold_r[8U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v10) {
        vlSelfRef.__PVT__lb_hold_r[9U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v11) {
        vlSelfRef.__PVT__lb_hold_r[10U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v12) {
        vlSelfRef.__PVT__lb_hold_r[11U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v13) {
        vlSelfRef.__PVT__lb_hold_r[12U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v14) {
        vlSelfRef.__PVT__lb_hold_r[13U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v15) {
        vlSelfRef.__PVT__lb_hold_r[14U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v16) {
        vlSelfRef.__PVT__lb_hold_r[15U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v17) {
        vlSelfRef.__PVT__lb_hold_r[16U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v18) {
        vlSelfRef.__PVT__lb_hold_r[17U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v19) {
        vlSelfRef.__PVT__lb_hold_r[18U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v20) {
        vlSelfRef.__PVT__lb_hold_r[19U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v21) {
        vlSelfRef.__PVT__lb_hold_r[20U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v22) {
        vlSelfRef.__PVT__lb_hold_r[21U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v23) {
        vlSelfRef.__PVT__lb_hold_r[22U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v24) {
        vlSelfRef.__PVT__lb_hold_r[23U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v25) {
        vlSelfRef.__PVT__lb_hold_r[24U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v26) {
        vlSelfRef.__PVT__lb_hold_r[25U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v27) {
        vlSelfRef.__PVT__lb_hold_r[26U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v28) {
        vlSelfRef.__PVT__lb_hold_r[27U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v29) {
        vlSelfRef.__PVT__lb_hold_r[28U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v30) {
        vlSelfRef.__PVT__lb_hold_r[29U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v31) {
        vlSelfRef.__PVT__lb_hold_r[30U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v32) {
        vlSelfRef.__PVT__lb_hold_r[31U] = 0ULL;
    }
    if (__VdlySet__lb_hold_r__v33) {
        vlSelfRef.__PVT__lb_hold_r[0U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[1U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[2U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[3U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[4U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[5U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[6U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[7U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[8U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[9U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[10U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[11U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[12U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[13U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[14U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[15U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[16U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[17U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[18U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[19U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[20U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[21U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[22U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[23U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[24U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[25U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[26U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[27U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[28U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[29U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[30U] = 0ULL;
        vlSelfRef.__PVT__lb_hold_r[31U] = 0ULL;
    }
    if (__VdlySet__q_cnt_r__v0) {
        vlSelfRef.__PVT__q_cnt_r[__VdlyDim0__q_cnt_r__v0] 
            = __VdlyVal__q_cnt_r__v0;
    }
    if (__VdlySet__q_cnt_r__v1) {
        vlSelfRef.__PVT__q_cnt_r[__VdlyDim0__q_cnt_r__v1] 
            = __VdlyVal__q_cnt_r__v1;
    }
    if (__VdlySet__q_cnt_r__v2) {
        vlSelfRef.__PVT__q_cnt_r[0U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v3) {
        vlSelfRef.__PVT__q_cnt_r[1U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v4) {
        vlSelfRef.__PVT__q_cnt_r[2U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v5) {
        vlSelfRef.__PVT__q_cnt_r[3U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v6) {
        vlSelfRef.__PVT__q_cnt_r[4U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v7) {
        vlSelfRef.__PVT__q_cnt_r[5U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v8) {
        vlSelfRef.__PVT__q_cnt_r[6U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v9) {
        vlSelfRef.__PVT__q_cnt_r[7U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v10) {
        vlSelfRef.__PVT__q_cnt_r[8U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v11) {
        vlSelfRef.__PVT__q_cnt_r[9U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v12) {
        vlSelfRef.__PVT__q_cnt_r[10U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v13) {
        vlSelfRef.__PVT__q_cnt_r[11U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v14) {
        vlSelfRef.__PVT__q_cnt_r[12U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v15) {
        vlSelfRef.__PVT__q_cnt_r[13U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v16) {
        vlSelfRef.__PVT__q_cnt_r[14U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v17) {
        vlSelfRef.__PVT__q_cnt_r[15U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v18) {
        vlSelfRef.__PVT__q_cnt_r[16U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v19) {
        vlSelfRef.__PVT__q_cnt_r[17U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v20) {
        vlSelfRef.__PVT__q_cnt_r[18U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v21) {
        vlSelfRef.__PVT__q_cnt_r[19U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v22) {
        vlSelfRef.__PVT__q_cnt_r[20U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v23) {
        vlSelfRef.__PVT__q_cnt_r[21U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v24) {
        vlSelfRef.__PVT__q_cnt_r[22U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v25) {
        vlSelfRef.__PVT__q_cnt_r[23U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v26) {
        vlSelfRef.__PVT__q_cnt_r[24U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v27) {
        vlSelfRef.__PVT__q_cnt_r[25U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v28) {
        vlSelfRef.__PVT__q_cnt_r[26U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v29) {
        vlSelfRef.__PVT__q_cnt_r[27U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v30) {
        vlSelfRef.__PVT__q_cnt_r[28U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v31) {
        vlSelfRef.__PVT__q_cnt_r[29U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v32) {
        vlSelfRef.__PVT__q_cnt_r[30U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v33) {
        vlSelfRef.__PVT__q_cnt_r[31U] = 0U;
    }
    if (__VdlySet__q_cnt_r__v34) {
        vlSelfRef.__PVT__q_cnt_r[0U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[1U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[2U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[3U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[4U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[5U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[6U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[7U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[8U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[9U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[10U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[11U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[12U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[13U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[14U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[15U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[16U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[17U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[18U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[19U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[20U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[21U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[22U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[23U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[24U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[25U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[26U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[27U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[28U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[29U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[30U] = 0U;
        vlSelfRef.__PVT__q_cnt_r[31U] = 0U;
    }
    vlSelfRef.__PVT__skid_wp_r = __Vdly__skid_wp_r;
    if (__VdlySet__skid_data_r__v0) {
        vlSelfRef.__PVT__skid_data_r[__VdlyDim0__skid_data_r__v0] 
            = __VdlyVal__skid_data_r__v0;
    }
    if (__VdlySet__skid_data_r__v1) {
        vlSelfRef.__PVT__skid_data_r[__VdlyDim0__skid_data_r__v1] 
            = __VdlyVal__skid_data_r__v1;
    }
    if (__VdlySet__skid_addr_r__v0) {
        vlSelfRef.__PVT__skid_addr_r[__VdlyDim0__skid_addr_r__v0] 
            = __VdlyVal__skid_addr_r__v0;
    }
    if (__VdlySet__skid_addr_r__v1) {
        vlSelfRef.__PVT__skid_addr_r[__VdlyDim0__skid_addr_r__v1] 
            = __VdlyVal__skid_addr_r__v1;
    }
    vlSelfRef.__PVT__skid_rp_r = __Vdly__skid_rp_r;
    vlSelfRef.__PVT__st_r = __Vdly__st_r;
    vlSelfRef.__PVT__slot_r = __Vdly__slot_r;
    if (__VdlySet__map_r__v0) {
        vlSelfRef.__PVT__map_r[__VdlyDim0__map_r__v0] 
            = __VdlyVal__map_r__v0;
    }
    if (__VdlySet__map_r__v1) {
        __Vilp1 = 0U;
        while ((__Vilp1 <= 0x0000003fU)) {
            vlSelfRef.__PVT__map_r[__Vilp1] = 0U;
            __Vilp1 = ((IData)(1U) + __Vilp1);
        }
    }
    vlSelfRef.__PVT__skid_free_w = (7U & (((IData)(4U) 
                                           - (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                          + (1U & (- (IData)(
                                                             (0U 
                                                              != (IData)(vlSelfRef.__PVT__skid_cnt_r)))))));
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    vlSelfRef.__PVT__pop_ret_v_r = ((IData)(vlSymsp->TOP.rst_n) 
                                    && ((IData)(vlSelfRef.__PVT__pop_act_w) 
                                        & (~ (vlSelfRef.__PVT__flush_clr_w 
                                              >> (0x0000001fU 
                                                  & (IData)(vlSelfRef.__PVT__pop_idx_r))))));
    vlSelfRef.__PVT__push_ram_w = ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                   & ((IData)(vlSelfRef.__PVT__skid_v_r) 
                                      >> (IData)(vlSelfRef.__PVT__skid_rp_r)));
    vlSelfRef.__PVT__loop_mapped_w = 0U;
    if (((vlSelfRef.__PVT__map_r[0U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[0U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[1U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[1U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[2U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[2U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[3U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[3U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[4U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[4U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[5U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[5U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[6U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[6U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[7U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[7U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[8U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[8U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[9U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[9U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[10U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[10U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[11U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[11U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[12U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[12U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[13U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[13U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[14U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[14U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[15U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[15U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[16U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[16U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[17U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[17U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[18U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[18U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[19U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[19U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[20U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[20U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[21U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[21U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[22U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[22U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[23U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[23U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[24U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[24U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[25U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[25U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[26U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[26U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[27U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[27U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[28U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[28U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[29U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[29U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[30U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[30U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[31U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[31U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[32U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[32U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[33U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[33U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[34U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[34U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[35U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[35U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[36U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[36U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[37U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[37U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[38U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[38U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[39U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[39U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[40U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[40U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[41U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[41U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[42U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[42U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[43U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[43U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[44U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[44U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[45U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[45U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[46U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[46U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[47U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[47U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[48U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[48U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[49U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[49U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[50U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[50U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[51U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[51U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[52U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[52U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[53U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[53U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[54U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[54U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[55U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[55U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[56U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[56U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[57U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[57U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[58U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[58U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[59U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[59U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[60U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[60U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[61U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[61U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[62U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[62U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[63U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[63U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    (1U 
                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U))] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    (1U 
                                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                        << 1U))] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    ((IData)(vlSelfRef.__PVT__slot_r) 
                                                     << 1U)] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                     << 1U)] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [((IData)(vlSelfRef.__PVT__slot_r) 
                                                   << 1U)]);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [(1U 
                                                   | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U))]);
    if (__VdlySet__lb_q_r__v0) {
        vlSelfRef.__PVT__lb_q_r[__VdlyDim0__lb_q_r__v0] 
            = __VdlyVal__lb_q_r__v0;
    }
    if (__VdlySet__q_rd_r__v0) {
        vlSelfRef.__PVT__q_rd_r[__VdlyDim0__q_rd_r__v0] 
            = __VdlyVal__q_rd_r__v0;
    }
    if (__VdlySet__q_rd_r__v1) {
        vlSelfRef.__PVT__q_rd_r[__VdlyDim0__q_rd_r__v1] 
            = __VdlyVal__q_rd_r__v1;
    }
    if (__VdlySet__q_rd_r__v2) {
        vlSelfRef.__PVT__q_rd_r[0U] = 0U;
    }
    if (__VdlySet__q_rd_r__v3) {
        vlSelfRef.__PVT__q_rd_r[1U] = 0U;
    }
    if (__VdlySet__q_rd_r__v4) {
        vlSelfRef.__PVT__q_rd_r[2U] = 0U;
    }
    if (__VdlySet__q_rd_r__v5) {
        vlSelfRef.__PVT__q_rd_r[3U] = 0U;
    }
    if (__VdlySet__q_rd_r__v6) {
        vlSelfRef.__PVT__q_rd_r[4U] = 0U;
    }
    if (__VdlySet__q_rd_r__v7) {
        vlSelfRef.__PVT__q_rd_r[5U] = 0U;
    }
    if (__VdlySet__q_rd_r__v8) {
        vlSelfRef.__PVT__q_rd_r[6U] = 0U;
    }
    if (__VdlySet__q_rd_r__v9) {
        vlSelfRef.__PVT__q_rd_r[7U] = 0U;
    }
    if (__VdlySet__q_rd_r__v10) {
        vlSelfRef.__PVT__q_rd_r[8U] = 0U;
    }
    if (__VdlySet__q_rd_r__v11) {
        vlSelfRef.__PVT__q_rd_r[9U] = 0U;
    }
    if (__VdlySet__q_rd_r__v12) {
        vlSelfRef.__PVT__q_rd_r[10U] = 0U;
    }
    if (__VdlySet__q_rd_r__v13) {
        vlSelfRef.__PVT__q_rd_r[11U] = 0U;
    }
    if (__VdlySet__q_rd_r__v14) {
        vlSelfRef.__PVT__q_rd_r[12U] = 0U;
    }
    if (__VdlySet__q_rd_r__v15) {
        vlSelfRef.__PVT__q_rd_r[13U] = 0U;
    }
    if (__VdlySet__q_rd_r__v16) {
        vlSelfRef.__PVT__q_rd_r[14U] = 0U;
    }
    if (__VdlySet__q_rd_r__v17) {
        vlSelfRef.__PVT__q_rd_r[15U] = 0U;
    }
    if (__VdlySet__q_rd_r__v18) {
        vlSelfRef.__PVT__q_rd_r[16U] = 0U;
    }
    if (__VdlySet__q_rd_r__v19) {
        vlSelfRef.__PVT__q_rd_r[17U] = 0U;
    }
    if (__VdlySet__q_rd_r__v20) {
        vlSelfRef.__PVT__q_rd_r[18U] = 0U;
    }
    if (__VdlySet__q_rd_r__v21) {
        vlSelfRef.__PVT__q_rd_r[19U] = 0U;
    }
    if (__VdlySet__q_rd_r__v22) {
        vlSelfRef.__PVT__q_rd_r[20U] = 0U;
    }
    if (__VdlySet__q_rd_r__v23) {
        vlSelfRef.__PVT__q_rd_r[21U] = 0U;
    }
    if (__VdlySet__q_rd_r__v24) {
        vlSelfRef.__PVT__q_rd_r[22U] = 0U;
    }
    if (__VdlySet__q_rd_r__v25) {
        vlSelfRef.__PVT__q_rd_r[23U] = 0U;
    }
    if (__VdlySet__q_rd_r__v26) {
        vlSelfRef.__PVT__q_rd_r[24U] = 0U;
    }
    if (__VdlySet__q_rd_r__v27) {
        vlSelfRef.__PVT__q_rd_r[25U] = 0U;
    }
    if (__VdlySet__q_rd_r__v28) {
        vlSelfRef.__PVT__q_rd_r[26U] = 0U;
    }
    if (__VdlySet__q_rd_r__v29) {
        vlSelfRef.__PVT__q_rd_r[27U] = 0U;
    }
    if (__VdlySet__q_rd_r__v30) {
        vlSelfRef.__PVT__q_rd_r[28U] = 0U;
    }
    if (__VdlySet__q_rd_r__v31) {
        vlSelfRef.__PVT__q_rd_r[29U] = 0U;
    }
    if (__VdlySet__q_rd_r__v32) {
        vlSelfRef.__PVT__q_rd_r[30U] = 0U;
    }
    if (__VdlySet__q_rd_r__v33) {
        vlSelfRef.__PVT__q_rd_r[31U] = 0U;
    }
    if (__VdlySet__q_rd_r__v34) {
        vlSelfRef.__PVT__q_rd_r[0U] = 0U;
        vlSelfRef.__PVT__q_rd_r[1U] = 0U;
        vlSelfRef.__PVT__q_rd_r[2U] = 0U;
        vlSelfRef.__PVT__q_rd_r[3U] = 0U;
        vlSelfRef.__PVT__q_rd_r[4U] = 0U;
        vlSelfRef.__PVT__q_rd_r[5U] = 0U;
        vlSelfRef.__PVT__q_rd_r[6U] = 0U;
        vlSelfRef.__PVT__q_rd_r[7U] = 0U;
        vlSelfRef.__PVT__q_rd_r[8U] = 0U;
        vlSelfRef.__PVT__q_rd_r[9U] = 0U;
        vlSelfRef.__PVT__q_rd_r[10U] = 0U;
        vlSelfRef.__PVT__q_rd_r[11U] = 0U;
        vlSelfRef.__PVT__q_rd_r[12U] = 0U;
        vlSelfRef.__PVT__q_rd_r[13U] = 0U;
        vlSelfRef.__PVT__q_rd_r[14U] = 0U;
        vlSelfRef.__PVT__q_rd_r[15U] = 0U;
        vlSelfRef.__PVT__q_rd_r[16U] = 0U;
        vlSelfRef.__PVT__q_rd_r[17U] = 0U;
        vlSelfRef.__PVT__q_rd_r[18U] = 0U;
        vlSelfRef.__PVT__q_rd_r[19U] = 0U;
        vlSelfRef.__PVT__q_rd_r[20U] = 0U;
        vlSelfRef.__PVT__q_rd_r[21U] = 0U;
        vlSelfRef.__PVT__q_rd_r[22U] = 0U;
        vlSelfRef.__PVT__q_rd_r[23U] = 0U;
        vlSelfRef.__PVT__q_rd_r[24U] = 0U;
        vlSelfRef.__PVT__q_rd_r[25U] = 0U;
        vlSelfRef.__PVT__q_rd_r[26U] = 0U;
        vlSelfRef.__PVT__q_rd_r[27U] = 0U;
        vlSelfRef.__PVT__q_rd_r[28U] = 0U;
        vlSelfRef.__PVT__q_rd_r[29U] = 0U;
        vlSelfRef.__PVT__q_rd_r[30U] = 0U;
        vlSelfRef.__PVT__q_rd_r[31U] = 0U;
    }
    vlSelfRef.__PVT__pop_idx_r = __Vdly__pop_idx_r;
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)))))))));
    __VdfgRegularize_h6e95ff9d_0_49 = ((vlSelfRef.__PVT__q_primed_r 
                                        >> (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & ((1U == (IData)(vlSelfRef.__PVT__st_r)) 
                                          & (0x20U 
                                             > (IData)(vlSelfRef.__PVT__pop_idx_r))));
    vlSelfRef.__PVT__lb_a0_w = (0x0000001fU & (((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                >> 1U) 
                                               + (0x0000001cU 
                                                  & ((IData)(vlSelfRef.lb_tuser_i) 
                                                     << 2U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
    vlSelfRef.__PVT__lb_w0_w = ((8U > (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__dup_sum_w = (0x0001ffffU & (((IData)(__VdfgRegularize_h6e95ff9d_0_49) 
                                                  & ((vlSelfRef.__PVT__q_fed_r 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                                     & (0U 
                                                        == vlSelfRef.__PVT__q_cnt_r
                                                        [
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__PVT__pop_idx_r))]))) 
                                                 + (IData)(vlSelfRef.lb_dup_cnt_o)));
    vlSelfRef.__PVT__pop_act_w = ((0U != vlSelfRef.__PVT__q_cnt_r
                                   [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_49));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    vlSelfRef.__PVT__push_same_w = ((IData)(vlSelfRef.__PVT__push_ram_w) 
                                    & ((vlSelfRef.__PVT__skid_addr_r
                                        [vlSelfRef.__PVT__skid_rp_r] 
                                        == (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & (IData)(vlSelfRef.__PVT__pop_act_w)));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__push_cnt1_w = (0x0000000fU & ((IData)(vlSelfRef.__PVT__q_cnt_r
                                                           [vlSelfRef.__PVT__skid_addr_r
                                                           [vlSelfRef.__PVT__skid_rp_r]]) 
                                                   - (IData)(vlSelfRef.__PVT__push_same_w)));
    if (vlSelfRef.__PVT__lb_pair01_w) {
        vlSelfRef.__PVT__cm1_data_w = (((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)));
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__lb_a0_w));
    } else {
        vlSelfRef.__PVT__cm1_data_w = ((QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)) 
                                       << 0x00000018U);
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                           >> 1U) + 
                                          (0x0000001cU 
                                           & ((IData)(vlSelfRef.lb_tuser_i) 
                                              << 2U))));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51));
    vlSelfRef.__PVT__push_drop_w = ((8U == (IData)(vlSelfRef.__PVT__push_cnt1_w)) 
                                    & (IData)(vlSelfRef.__PVT__push_ram_w));
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53));
    __VdfgRegularize_h6e95ff9d_0_50 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_50));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_50)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}
